# Security skill handoff — manual, evidence-only (v1)

This contract connects the three registries at the documentation layer. It is not a runtime, does not grant authority, and does not run or schedule security operations. Each repository retains its own canonical definition and history.

| Skill | Registered version | Repository | Responsibility |
|---|---|---|---|
| Aegis | 1.1 | jussray/aegis | Defensive review and remediation within scope |
| Sarissa | 1.0 | jussray/sarissa | Offline assessment planning and reporting |
| Medusa | 1.1.0 | jussray/juss-protect-me-2 | Offline reasoning and scrutiny of supplied evidence |

## Manual exchange

A reviewer may prepare an evidence-only handoff for the owner to inspect. No automatic file access, forwarding, cross-repository reads, active testing, or tool execution follows from receipt of a handoff. The owner must approve scope and any disclosure separately. Only explicitly approved, redacted evidence may be exchanged.

Required fields: schema_version (1), origin_skill, origin_version, target_ref, scope, evidence_origin (AUTHORED / OBSERVED / USER-REPORTED / VERIFIED), finding_status (VERIFIED / INFERRED / UNVERIFIED), safe_summary, evidence_reference (approved reference or null), observed_at_utc, unresolved_checks, owner_decision_required. Do not include credentials, personal data, exploit instructions, or authorization tokens. A reference or hash alone does not prove the underlying claim.

Aegis may independently review a defensive finding; Medusa may independently assess a proposed decision or remedy using supplied local material; Sarissa may document a planning concern. No role inherits another role's permission. A reported finding remains unverified until independently checked. If evidence or scope is missing, hold and record what is missing. A more restrictive advisory verdict takes precedence, but even a favorable verdict cannot authorize execution.

## Acceptance and rollback

A registry change is accepted only when its record, path and immutable source identity are checked. CI status and runtime outcome are separate evidence. No branch merge, deployment, external synchronization or active security integration is implied. Revert the contract commit to remove this documentation linkage without modifying original skill definitions.
