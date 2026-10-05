# System Architecture and Components

The Framework's conceptual triad is the Living Library (knowledge), Rings (independent perspectives) and United Hub (coordination). Deployment follows Cathedral/Core plus independent specialized satellites. `nextxus.online` is the intended content authority; this brain repository is a portable map, not proof that every site already consumes it.

## Boundaries

- Cathedral holds the directive baseline and provenance. The sealed v1.1 text is `00-immutable/directives.yaml`, with checksum declarations in `00-immutable/SEAL.yaml`.
- The Library records source, type, version, timestamp and relationships. `framework/INDEX/master_index.yaml` indexes repository paths, not the entire external Library.
- `01-rings/rings.yaml` defines the recorded public Six/Twelve roles. `framework/ARCHETYPES/ring_definitions.yaml` is a historical crosswalk with unresolved aliases, not a Senate roster.
- Agent Zero has two separately described functions in `01-rings/rings.yaml`: nonvoting verifier and interactive braider. No untested endpoint is claimed as universal enforcement.
- United Hub is intended to coordinate navigation, synchronization and communication, but no specific deployment is certified here. Satellites retain identity and exchange verified records; they cannot override directives.
- `framework/LATTICE/lattice_state.yaml` is an initial snapshot ledger, not real-time telemetry. A checked file is not a verified operational implementation.
- Legacy Seed requires independent copies and plain-language recovery. A backup requirement is not evidence that copies currently exist.

Recovery sequence: recover archives, restore principles, rebuild knowledge, restore intelligences, reconnect components and verify integrity. Public files may point to private repositories, but must not reproduce private content.

## Provenance

```yaml
sources:
  - document: The Immutable HumanCodex NextXus, Federation Framework
    chapters: [2, 23, 29, 30, 31, 35, 46, 55, 71, 72, 74, 108, 109, 111, 310, 311, 312, 313, 314, 320, 451, 452, 453, 454, 456, 458, 460, 485, 486, 487, 488, 489, 490]
  - document: 00-immutable/directives.yaml, Cathedral v1.1
    directives: [DIR-047, DIR-051, DIR-053, DIR-062, DIR-063, DIR-064, DIR-071, DIR-072]
  - document: BRIEF.md
conflicts:
  - Framework proposes automatic forced rollback and universal live verification hooks; Cathedral DIR-047 mandates returning to a stable state without granting automatic mutation authority. Both are design goals until proven deployed.
```
