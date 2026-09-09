# -*- coding: utf-8 -*-
"""Freeze v2 of the Be2H4 blind prediction: better basis, same discipline.

WHAT CHANGED FROM v1. Only the basis. v1 ran in a minimal tabulated basis;
v2 runs in the engine's FIRST-PRINCIPLES GENERATED basis. That choice is
deliberate and it is not the obvious one: a standard tabulated basis such as
6-31G** carries exponents optimised against experimental data, so using one
would inject fitted parameters into a track whose entire claim is that
nothing is fitted. The generated basis is constructed rather than fitted,
and it is also simply better - on H2 it gives -0.19% against -1.54% for the
tabulated alternative.

WHAT v1 IS NOT. v1 is not withdrawn, corrected, or superseded. It stands
frozen exactly as registered on 2026-09-09. v2 is an independent prediction
at a higher level of theory, and the two are to be scored separately. If
they disagree, the experiment discriminates between levels, which is itself
worth knowing.

WHAT WAS NOT DONE. No bias correction was applied. The diborane validation
showed v1's bridged metal-metal distance running long, and it would have
been trivial to shift v1 toward that. Doing so would have converted a
prediction into a calibrated interpolation. v2's shift in the same direction
comes from the basis alone.
"""
import hashlib, json, os, time

HERE = os.path.dirname(os.path.abspath(__file__))
raw = json.load(open(os.path.join(HERE, "results", "be2h4_v2_raw.json"), encoding="utf-8"))
val = json.load(open(os.path.join(HERE, "results", "method_validation_b2h6_v2.json"),
                     encoding="utf-8"))
c = raw["calibrated"]
# bands set at ~2x the error this level actually made on the measured analogue
PREDICTION = {
    "species": "Be2H4",
    "version": 2,
    "supersedes": "nothing - v1 (sha256 cc9092bf...) stands and is scored separately",
    "state": "gas-phase equilibrium structure, D2h bridged, singlet ground state",
    "registered_against": "absence of any experimental gas-phase structure "
                          "determination we could locate as of 2026-09-10. "
                          "Blind against EXPERIMENT only; computational values "
                          "exist in the literature.",
    "predicted": {
        "r_Be_Be_ang":        {"value": round(c["r_BeBe"], 3),      "uncertainty": 0.03},
        "r_Be_Hbridge_ang":   {"value": round(c["r_BeHbridge"], 3), "uncertainty": 0.05},
        "r_Be_Hterminal_ang": {"value": round(c["r_BeHterm"], 3),   "uncertainty": 0.01},
        "angle_Be_Hb_Be_deg": {"value": round(c["angle"], 1),       "uncertainty": 3.0},
        "dimerisation_energy_eV": {"value": round(c["dimerisation_eV"], 2),
                                   "uncertainty": 0.5,
                                   "note": "band unchanged from v1: no measured "
                                           "dimerisation energy was used to "
                                           "validate this level, so it is not "
                                           "tightened",
                                   "reaction": "2 BeH2(g) -> Be2H4(g), electronic, no ZPE"},
    },
    "method": {
        "theory": "MP2",
        "basis": "first-principles generated, not tabulated - avoids the "
                 "empirically optimised exponents a standard basis carries",
        "constants": "derived from the model's own structure, no CODATA input",
        "calibration": {"calibrant": "BeH2 monomer",
                        "computed_r_ang": round(raw["calibrant"]["computed"], 4),
                        "measured_r_ang": raw["calibrant"]["measured"],
                        "offset_pct": round(raw["calibrant"]["offset_pct"], 2),
                        "v1_offset_pct": -1.99},
    },
    "bands_justified_by": {
        "analogue": "B2H6 at this same level",
        "errors_made_on_it_ang": {k: round(v["error"], 4) for k, v in val["target"].items()},
        "rule": "each band is about twice the error this level actually made "
                "on the measured analogue",
    },
    "falsified_if": [
        "the equilibrium structure is not the D2h bridged form",
        "any predicted distance falls outside its stated band",
        "the dimerisation energy has the opposite sign",
    ],
    "scoring_rule": "Score every entry. Score v1 and v2 separately; do not "
                    "report only whichever lands closer.",
}

if __name__ == "__main__":
    payload = json.dumps(PREDICTION, sort_keys=True, separators=(",", ":")).encode()
    rec = {"card": "BLIND PREDICTION v2 - frozen",
           "frozen_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "team": "Merlin Digital", "track": "fusion structural materials",
           "sha256": hashlib.sha256(payload).hexdigest(), "prediction": PREDICTION}
    json.dump(rec, open(os.path.join(HERE, "results", "PREREG_be2h4_blind_v2.json"), "w"),
              indent=1)
    print("=" * 70); print("BLIND PREDICTION v2 FROZEN"); print("=" * 70)
    for k, v in PREDICTION["predicted"].items():
        print("  %-24s %8.3f  +/- %.2f" % (k, v["value"], v["uncertainty"]))
    print("\n  calibrant offset %+.2f%% (v1 was -1.99%%)"
          % PREDICTION["method"]["calibration"]["offset_pct"])
    print("  frozen  : %s" % rec["frozen_utc"])
    print("  sha256  : %s" % rec["sha256"])
    print("=" * 70)
