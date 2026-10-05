# Operational Standards and Protocols

This is a procedure-level synthesis of the Framework; Cathedral wording remains in `framework/DIRECTIVES/directives.yaml`. A written procedure is not proof that its automation runs.

## Evidence and communication

Collect claim, evidence, analysis, independent cross-check, confidence score and revision history. Label FACT, INFERENCE, ASSUMPTION and UNKNOWN; a score is not proof. Inter-agent messages should carry sender, purpose, context, request, response, verification, confidence and timestamp. Preserve disagreement instead of smoothing it into false consensus. Mirror understanding before acceptance of a final record.

## Change and synchronization

Use human-readable YAML, JSON or Markdown with identifiers, version, classification, status, timestamps, dependencies, relationships and sources as applicable. Collect, verify, integrate, distribute, archive. The Framework proposes daily updates, weekly synchronization, monthly verification reports, quarterly high-impact review and annual core review. These are target cadences, not attested scheduled jobs. Record the actual check date and evidence; do not set `last_verified` from a planned cadence.

## Recovery

On drift or overload, invoke DIR-047 NEXRECAL, identify a verified stable state, log the delta and require review before consequential rollback. Keep versioned snapshots and attribution. No-delete means supersede or archive without losing audit history; it does not mean harmful private material must remain public. Back up independently and rehearse reconstruction. Use the Fast Ring for immediate stabilization only, followed by full review appropriate to risk.

Seal hashes should be checked against GitHub contents bytes rather than CDN-cached raw files. The initial LATTICE file is a snapshot, not a monitoring feed; untested satellite health is UNVERIFIED.

## Provenance

```yaml
sources:
  - document: The Immutable HumanCodex NextXus, Federation Framework
    chapters: [3, 24, 25, 33, 38, 39, 47, 48, 53, 55, 56, 74, 107, 109, 111, 312, 313, 314, 317, 319, 329, 338, 437, 441, 442, 443, 445, 451, 453, 470, 472, 482, 483, 488]
  - document: 00-immutable/directives.yaml, Cathedral v1.1
    directives: [DIR-000, DIR-005, DIR-024, DIR-047, DIR-049, DIR-051, DIR-055, DIR-062, DIR-068, DIR-072]
conflicts:
  - Framework chapters 306 and 313 propose forced or automatic rollback; Cathedral DIR-047 does not specify automatic write authority.
  - Framework chapter 437 treats 95 as a factual ingestion threshold; Cathedral DIR-000 defines internal output scoring for settled truth.
```
