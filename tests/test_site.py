"""Static asset and hosted browser checks for the offline Sarissa demo."""
from pathlib import Path
import hashlib, json, subprocess, functools, threading, http.server
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[1] / 'site'
EXPECTED = {'portrait.webp':'e08db5e4e8a35e66749f32635faee78e3dc85fde6f8c9d04292be8130f443d33','ambient.webp':'666352700ebd0b15bbbea2d1d3fc61696b3ad614d32e186803c41307fd2a4105','canon.png':'279460314e845ef9dcda65bf4ab0ddd2008082aed1e50f70cb0872f44e156907','wordmark.webp':'0cca9c5e47de245d49d3202a1b3ff32ad7f3d705a8e6589d23e89f95e1ea4a6c'}
for name, digest in EXPECTED.items():
    assert hashlib.sha256((ROOT/'assets'/name).read_bytes()).hexdigest() == digest, name
html=(ROOT/'index.html').read_text()
assert ';base64,' not in html
for js in sorted((ROOT/'assets').glob('*.js')):
    subprocess.run(['node','--check',str(js)],check=True)
    assert 'assets/'+js.name in html
policy=next(line.strip().split(': ',1)[1] for line in (ROOT/'_headers').read_text().splitlines() if line.strip().startswith('Content-Security-Policy:'))
class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Content-Security-Policy',policy)
        super().end_headers()
    def log_message(self,*args): pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/'
with sync_playwright() as pw:
    browser=pw.chromium.launch()
    for w,h in [(1536,864),(390,844),(320,568),(768,1024),(1440,900)]:
        page=browser.new_page(viewport={'width':w,'height':h},reduced_motion='reduce')
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
        page.goto(url)
        assert page.locator('body').get_attribute('data-route')=='home'
        assert page.evaluate('document.documentElement.scrollWidth===innerWidth')
        assert page.evaluate('document.documentElement.scrollHeight<=innerHeight+1')
        assert page.locator('#world').bounding_box()['height']==h
        if w in [1536,390]:
            for k in ['overview','capabilities','cases','resources','request','access','detect','strategize','respond','report','search']:
                page.goto(url)
                page.locator(f'[data-open="{k}"]:visible').first.click()
                if k=='search':
                    assert page.locator('#info').evaluate('(x)=>x.open')
                    page.fill('#query','report')
                    assert page.locator('#searchlist button').count()>0
                else:
                    assert page.locator('body').get_attribute('data-route')==('access' if k in ['detect','strategize','respond','report'] else k),k
            page.goto(url+'#request')
            page.select_option('#request-role','analyst')
            page.select_option('#request-purpose','training')
            page.locator('#request-form button[type=submit]').click()
            with page.expect_download() as dl: page.click('#download-request')
            assert json.loads(Path(dl.value.path()).read_text())['status']=='UNSUBMITTED'
            page.goto(url+'#access')
            page.select_option('#entry-role','observer')
            page.locator('#entry-form button[type=submit]').click()
            assert page.locator('#launch-demo').is_disabled()
            page.check('#scope-agree')
            page.click('#launch-demo')
            page.fill('#summary','Fictional smoke-test event')
            page.locator('#eventForm button[type=submit]').click()
            page.click('[data-tab="respond"]')
            assert page.locator('#approve').is_disabled()
            page.click('[data-tab="strategize"]')
            page.click('#plan')
            page.click('[data-tab="respond"]')
            assert page.locator('#approve').is_disabled()
            page.check('#review')
            page.click('#approve')
            page.click('[data-tab="report"]')
            with page.expect_download() as dl: page.click('#export')
            record=json.loads(Path(dl.value.path()).read_text())
            assert record['decision']['status']=='approved-local-only'
            assert record['decision']['externalAction'] is False
        assert not errors,errors
        print(f'PASS {w}x{h}')
        page.close()
    page=browser.new_page(viewport={'width':390,'height':844})
    page.goto(url)
    page.wait_for_function("Number(document.querySelector('.portrait-world canvas').dataset.frames)>0")
    a=int(page.locator('.portrait-world canvas').get_attribute('data-frames'))
    page.wait_for_function("(before)=>Number(document.querySelector('.portrait-world canvas').dataset.frames)>before",arg=a)
    print('PASS motion')
    browser.close()
server.shutdown()
