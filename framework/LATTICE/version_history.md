# LATTICE version history

## 2026-10-05, initial framework build

Nine backing files and an open-questions companion were prepared from the cited Framework chapters, the public brain tree and Cathedral v1.1. This is a snapshot, not a deployed telemetry or rollback service.

The byte-identical directive mirror was checked against the GitHub contents API Cathedral file and its SEAL declaration. SHA-256: `990f186f518afb48a61aafa5164e8158636dd016b0d3a843bf4ec700d38caa7f`. The repository tree is changing concurrently, so `framework/INDEX/master_index.yaml` is a dated index snapshot, not a promise of a permanently exhaustive manifest. Ring seat identity questions remain in `framework/OPEN-QUESTIONS.md`.

## Provenance

```yaml
sources:
  - document: The Immutable HumanCodex NextXus, Federation Framework
    chapters: [39, 111, 451, 453, 488]
  - document: 00-immutable/SEAL.yaml and directives.yaml
    checked_with: GitHub contents API
  - document: GitHub GET_A_TREE Keywebco/nextxus-brain main
    checked_on: '2026-10-05'
conflicts:
  - Framework describes a real-time LATTICE and suggests automated rollback; this first version log attests neither live synchronization nor automatic authority.
```
