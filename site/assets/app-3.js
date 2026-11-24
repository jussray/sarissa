(()=>{
'use strict';
const pages=new Set(['home','overview','capabilities','cases','resources','access','orientation','request','request-review',...workspaceKeys]);
const nav=document.getElementById('glass-nav'), front=document.getElementById('home'), flow=document.querySelector('.glass-flow'), foot=document.querySelector('.foot');
const canonical=document.querySelectorAll('#world .canon-nav,#world .canon-hero,#world .canon-waterline');
function route(){let key=location.hash.slice(1);if(workspaceKeys.includes(key)&&!demo){target=key;key='access'}if(key==='orientation'&&!entryRole)key='access';if(key==='request-review'&&!requestDraft)key='request';return pages.has(key)?key:'home'}
function pageFor(key){return document.getElementById(workspaceKeys.includes(key)?'workspace-page':key)}
function show(){const key=route(), home=key==='home';document.body.dataset.route=key;document.body.classList.toggle('scrolled',!home);front.hidden=!home;flow.hidden=home;foot.hidden=home;nav.inert=home;canonical.forEach(el=>el.inert=!home);document.querySelectorAll('.glass-page').forEach(el=>el.hidden=el!==pageFor(key));if(workspaceKeys.includes(key))render(key);nav.querySelectorAll('[data-open]').forEach(el=>{if(el.dataset.open===key)el.setAttribute('aria-current','page');else el.removeAttribute('aria-current')});window.scrollTo({top:0,behavior:'instant'});document.title=home?'Sarissa | Precision · Strategy · Controlled Response':pageFor(key).querySelector('h2').textContent+' | Sarissa';}
window.sarissaNavigate=function(key){if(!pages.has(key))return;const next=key==='home'?'#home':'#'+key;if(location.hash!==next)history.pushState(null,'',next);show();if(key!=='home'){const heading=pageFor(route()).querySelector('h2');heading.tabIndex=-1;heading.focus({preventScroll:true});}};
addEventListener('popstate',show);addEventListener('hashchange',show);show();
})();