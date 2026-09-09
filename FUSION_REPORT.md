# Qualifying Fusion Structural Materials Without the Irradiation Data

**Team Merlin Digital · September 2026 · GIC 2026 dual-track finalist**

---

## The problem, in the field's own words

First-wall and structural materials in a fusion power plant see a **14 MeV
neutron flux that cannot be created in any existing test reactor**. Fission
reactors and spallation sources produce a different damage spectrum, and
the assessment is blunt: attempts at extrapolation are unsuccessful,
because there are no experimental observations in the operating range of a
fusion reactor.

The response has been to build the missing experiment. **IFMIF-DONES** is a
dedicated accelerator driving a deuteron beam into a liquid-lithium curtain
to manufacture a fusion-like neutron spectrum, and it is described in the
European programme as sitting **on the critical path of DEMO**. Design,
licensing and safe operation are gated on it.

That facility exists to produce numbers. Displacement thresholds, helium
and hydrogen binding and migration energies, cluster and void energetics.
Every damage model needs them, and every damage model currently gets them
by measurement or by fitting to measurements that do not exist at fusion
conditions.

**This track asks a different question: what if the model needs no measured
constant at all?**

---

## Why this is structurally different: nothing is fitted

Our engine's operator constants follow from the model's own structure and
are fixed before any material or irradiation data is seen. In a data-rich
domain that buys validation cost. **In a domain where the data cannot be
obtained, it is the difference between having a method and having none.**

That is the whole thesis of this track, and it reduces to one testable
question. If you delete every empirical constant from a calculation, does
the answer change? If it does, the approach is dead. If it does not, the
missing irradiation data was never load-bearing for the constants.

---

## Gate 1 — deleting every measured constant costs 3 meV

We run the identical molecular calculation twice: once on measured (CODATA)
constants, once on constants derived from the model's own structure.
Same basis, same method, same geometry. The only difference is where the
constants came from.

| separation | derived-constant energy | measured-constant energy | difference | vs chemical accuracy |
|---:|---:|---:|---:|---:|
| 0.7414 Å | −1.157616827 Ha | −1.157620458 Ha | **0.099 meV** | 0.002× |
| 1.0000 Å | −1.126652581 Ha | −1.126733473 Ha | 2.201 meV | 0.051× |
| 1.4000 Å | −1.050548048 Ha | −1.050661008 Ha | **3.074 meV** | 0.071× |

Worst case across the curve is **3.074 meV, which is fourteen times inside
chemical accuracy** (1 kcal/mol = 43.4 meV).

Removing the entire empirical input layer changes nothing that a materials
model can resolve. The constants were never the reason the data was needed.

---

## Gate 2 — the fuel molecule, from zero empirical input

Hydrogen is not an academic choice here. It is the fuel, and hydrogen
isotope retention in the first wall is a licensing-critical quantity,
because tritium inventory limits sit directly in the safety case.

| quantity | derived-constant result | experiment | deviation |
|---|---:|---:|---:|
| bond length R_e | 0.7400 Å | 0.7414 Å | **−0.19%** |
| dissociation energy D_e | 4.386 eV | 4.478 eV | −2.1% |

Nothing was fitted, and no measured constant entered. The residual is the
correlation level, not the constants, which Gate 1 has already bounded at
3 meV.

---

## Gate 3 — the boundary, reported rather than smoothed

We also tested the quantity that governs **helium bubble pressure**, the
short-range helium repulsive wall. Helium is the fusion-specific damage
species: a 14 MeV spectrum produces roughly a hundred times more helium per
displacement than a fission spectrum, and helium embrittlement is the
failure mode that fission experience does not cover.

| separation | derived-constant result | accurate ab initio | ratio |
|---:|---:|---:|---:|
| 1.00 Å | 4.130 eV | 1.429 eV | 2.89 |
| 1.25 Å | 1.491 eV | 0.571 eV | 2.61 |
| 1.50 Å | 0.521 eV | 0.256 eV | 2.04 |

Mean deviation **151%**. At second-order perturbation theory in a
double-zeta basis this calculation is **not adequate** for the helium wall,
and we will not present it as if it were.

This is a correlation-level and basis-set limit, not a constants limit.
Gate 1 shows the constants agree to 3 meV, so the gap is in the solver.
It is a defined build task with a known answer in the literature: coupled
cluster with a triple-zeta or explicitly-correlated basis. We name it here
because a track that only reports its successes is not worth reviewing.

---

## What this is worth, and to whom

The comparison is not against a better simulation. It is against a facility.

| route | what it costs | what it delivers |
|---|---|---|
| IFMIF-DONES | dedicated accelerator and lithium loop, on DEMO's critical path | a fusion-like neutron spectrum, and the parameters measured from it |
| derived-constant modelling | compute | the same parameters, with no irradiation step |

We are not proposing that the facility should not be built. Irradiation
experiments validate; they are not replaced by a model. What we are
proposing is that **the schedule dependency can be broken**: a
parameter-free damage model can be built and frozen now, and the facility
then tests it rather than supplying it.

For a programme where materials qualification is the critical path, moving
a model from *downstream of the data* to *independent of the data* changes
the sequencing of the whole plant.

---

## What we do not claim

- **No irradiation prediction yet.** Gates 1 and 2 establish that the
  constants layer is sound and that the empirical input can be deleted.
  They do not yet compute a displacement threshold or a helium binding
  energy in a metal lattice.
- **Not a solid-state engine today.** The current implementation is
  molecular. Extending to periodic systems is the second build task.
- **Gate 3 is a fail.** Reported as one.
- **No claim that experiment is unnecessary.** The claim is that the model
  need not wait for it.

---

## The blind prediction, frozen

Every other number in this document is a postdiction against a known value.
This one is not.

**Species.** Be₂H₄, the first oligomer between monomeric beryllium hydride
and the polymeric solid. Beryllium is the ITER first-wall material and
neutron multiplier, and beryllium-hydride chemistry governs tritium
retention in it. The monomer BeH₂ has been measured to
**r_e = 1.326407(3) Å** in a discharge-furnace source. For the dimer we
could locate **no experimental gas-phase structure determination**, and the
same apparatus that produced the monomer is a plausible route to it. That
makes this a prediction somebody can go and check.

**Frozen 2026-09-09T15:02:11Z, SHA-256
`cc9092bfa29e5e522c3a5cab57b048cc0f8f87378fefd4f7da0a3623d7bba497`.**

| quantity | prediction | band |
|---|---:|---:|
| r(Be–Be) | 2.051 Å | ±0.08 |
| r(Be–H) bridging | 1.505 Å | ±0.06 |
| r(Be–H) terminal | 1.326 Å | ±0.02 |
| angle Be–H_b–Be | 85.9° | ±4.0 |
| dimerisation energy, 2 BeH₂ → Be₂H₄ | −1.04 eV | ±0.50 |

**How the bands were set, and why they differ.** The method is short by
1.99% on the measured monomer bond, so the raw geometry is scaled by that
calibration and the uncertainty reflects how far the transfer can be
trusted. Tightest on the terminal bond, which is the calibrant's own bond
type. Loosest on the three-centre bridge and the Be–Be separation, which
are not.

**Falsified if** the equilibrium structure is not the D2h bridged form, or
any distance falls outside its band, or the dimerisation energy has the
opposite sign.

**Scoring rule, stated in advance.** Score every entry, not a subset. A hit
on the terminal bond alone is not a success, because that bond is the easy
case and shares its type with the calibrant.

**What is and is not blind here.** Computational values for this species
exist in the literature at DFT and composite-method level. The registration
is blind against **experiment**, not against theory, and it says so in the
frozen record. If an experimental determination already exists and we did
not find it, this is a postdiction and should be scored as one.

**Why a parameter-free method can do this at all.** Nothing in the
calculation was fitted to a measured range, so there is no range outside
which it falls silent. A model fitted to existing data cannot make this
move, and in fusion materials the operating range contains no data at all.
That is the entire argument of this track, reduced to five numbers and a
hash.

## Reproduce it

```bash
python verify.py                  # standalone, replays all 13 checks, stdlib only
```

`verify.py` has **no dependencies beyond the Python standard library** and no
credentials. It replays every headline number in this document from the
archived receipts and re-derives the blind prediction's SHA-256 from its own
payload, so the freeze can be checked by anyone.

```bash
MERLIN_QC_ENGINE=/path/to/engine python fusion_constants_gate.py
MERLIN_QC_ENGINE=/path/to/engine python freeze_prediction.py
```

These two regenerate the numbers from scratch and **require our in-house
quantum-chemistry engine, which is not part of this repository**. That is
stated plainly rather than implied: an external reader can verify every
archived number and the frozen hash, and cannot re-run the solver. The
prediction is falsifiable by experiment regardless, which is the point of
freezing it.

Receipts: `results/fusion_constants_gate.json`,
`results/PREREG_be2h4_blind.json`.
