# Merlin Digital — Fusion Structural Materials Track

| | |
|---|---|
| **Team** | Merlin Digital |
| **Project** | Qualifying fusion structural materials without the irradiation data |
| **Write-up** | `FUSION_REPORT.md` |
| **Prior result** | GIC 2026 — dual-track finalist (Mitsubishi/AIST materials track) |
| **Contact** | sharad.bachani@merlin-me.com · ORCID 0009-0008-4679-6717 |

## The claim in one line

First-wall materials must be qualified against a 14 MeV neutron flux that no
existing reactor can produce, extrapolation from fission data is documented as
failing, and IFMIF-DONES exists to manufacture the missing numbers while sitting
on DEMO's critical path. **Our engine's constants are derived rather than
measured, so deleting the empirical input costs 3.074 meV — fourteen times
inside chemical accuracy.** The missing irradiation data was never load-bearing
for the constants layer.

## Why this domain and not another

A parameter-free model in a data-rich domain buys validation cost. In a domain
where the data cannot be obtained it is the difference between having a method
and having none. Fitted models and machine learning win where data is abundant.
This wins where data is impossible, and fusion materials is the canonical case.

## Gates

| gate | result |
|---|---|
| 1 — delete every measured constant | worst difference **3.074 meV**, 14× inside chemical accuracy |
| 2 — fuel molecule, zero empirical input | bond length **−0.19%**, dissociation energy −2.1% |
| 3 — helium repulsive wall | **FAIL, 151% deviation.** Correlation-level limit, reported not hidden |

## Reproduce

```bash
python verify.py
```

Standalone, stdlib only, no credentials. Replays all 13 checks and re-derives
the blind prediction's SHA-256 from its payload.

Regenerating from scratch (`fusion_constants_gate.py`, `freeze_prediction.py`)
requires our in-house quantum-chemistry engine, which is **not** in this
repository. Stated plainly: you can verify every archived number and the
frozen hash; you cannot re-run the solver.

## The frozen prediction

`results/PREREG_be2h4_blind.json` — Be2H4 gas-phase equilibrium structure,
frozen 2026-09-09, SHA-256 `cc9092bf...`. Blind against experiment, not
against theory. Falsification conditions and the scoring rule are fixed in
the record.

## Discipline

Nothing is fitted. Gate 3 is a failure and ships at the same receipt class as
the passes. We do not claim to replace irradiation experiment; we claim the
model need not wait for it.
