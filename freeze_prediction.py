# -*- coding: utf-8 -*-
"""Freeze a blind prediction: Be2H4 gas-phase equilibrium structure.

WHY THIS SPECIES. Beryllium is the ITER first-wall material and neutron
multiplier, and beryllium-hydride chemistry governs tritium retention in it.
The monomer BeH2 has been measured to high precision in a discharge-furnace
source (r_e = 1.326407(3) A). The first oligomer on the path from monomer to
the polymeric solid, Be2H4, has been studied computationally but we could
find NO experimental gas-phase structure determination. The same apparatus
that produced BeH2 is a plausible route to it, which makes this a prediction
someone can actually go and check.

WHY IT IS A REAL TEST. A method with derived constants can predict outside
any measured range because nothing in it was fitted to a measured range. A
method fitted to existing data has, by construction, nothing to say there.
This is that difference, made falsifiable.

METHOD AND ITS HONEST LIMITS. MP2 in a minimal basis with constants derived
rather than measured. That method is short by 1.99% on the measured monomer
bond, so the raw geometry is scaled by the monomer calibration factor and the
uncertainty bands below are set by how far that transfer can be trusted:
tightest for the terminal bond, which is the same bond type as the calibrant,
loosest for the three-centre bridge and the Be-Be separation, which are not.
"""
import hashlib, json, os, time

HERE = os.path.dirname(os.path.abspath(__file__))
raw = json.load(open(os.path.join(HERE, "results", "be2h4_raw.json"), encoding="utf-8"))
c = raw["calibrated"]

PREDICTION = {
    "species": "Be2H4",
    "state": "gas-phase equilibrium structure, D2h bridged, singlet ground state",
    "registered_against": "absence of any experimental gas-phase structure "
                          "determination we could locate as of 2026-09-09. "
                          "Computational values exist in the literature "
                          "(DFT/G4); this is registered as blind against "
                          "EXPERIMENT only.",
    "predicted": {
        "r_Be_Be_ang":        {"value": round(c["r_BeBe"], 3),        "uncertainty": 0.08},
        "r_Be_Hbridge_ang":   {"value": round(c["r_BeHbridge"], 3),   "uncertainty": 0.06},
        "r_Be_Hterminal_ang": {"value": round(c["r_BeHterm"], 3),     "uncertainty": 0.02},
        "angle_Be_Hb_Be_deg": {"value": round(c["angle_BeHbBe_deg"], 1), "uncertainty": 4.0},
        "dimerisation_energy_eV": {"value": round(c["dimerisation_eV"], 2),
                                   "uncertainty": 0.5,
                                   "reaction": "2 BeH2(g) -> Be2H4(g), electronic, no ZPE"},
    },
    "method": {
        "theory": "MP2, minimal basis, in-house engine",
        "constants": "derived from the model's own structure, no CODATA input",
        "calibration": {
            "calibrant": "BeH2 monomer",
            "computed_r_ang": 1.3000,
            "measured_r_ang": 1.326407,
            "method_offset_pct": -1.99,
            "scale_factor_applied": round(raw["calibration_factor"], 5),
        },
    },
    "falsified_if": [
        "the equilibrium structure is not the D2h bridged form",
        "any predicted distance falls outside its stated band",
        "the dimerisation energy has the opposite sign, i.e. Be2H4 is unbound "
        "with respect to two monomers",
    ],
    "scoring_rule": "Score every entry. Do not score a subset. A hit on the "
                    "terminal bond alone is not a success, because that bond "
                    "is the calibrant's own bond type and is the easy case.",
}

if __name__ == "__main__":
    payload = json.dumps(PREDICTION, sort_keys=True, separators=(",", ":")).encode()
    rec = {
        "card": "BLIND PREDICTION - frozen",
        "frozen_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "team": "Merlin Digital",
        "track": "fusion structural materials",
        "sha256": hashlib.sha256(payload).hexdigest(),
        "prediction": PREDICTION,
    }
    p = os.path.join(HERE, "results", "PREREG_be2h4_blind.json")
    json.dump(rec, open(p, "w"), indent=1)
    print("=" * 70)
    print("BLIND PREDICTION FROZEN")
    print("=" * 70)
    print("  species : Be2H4, gas-phase equilibrium structure, D2h bridged")
    for k, v in PREDICTION["predicted"].items():
        print("  %-24s %8.3f  +/- %.2f" % (k, v["value"], v["uncertainty"]))
    print("\n  calibrated on the measured monomer (method offset -1.99%)")
    print("  frozen  : %s" % rec["frozen_utc"])
    print("  sha256  : %s" % rec["sha256"])
    print("  file    : results/PREREG_be2h4_blind.json")
    print("=" * 70)
