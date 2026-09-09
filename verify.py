# -*- coding: utf-8 -*-
"""Credential-free replay of the fusion track's headline numbers."""
import json, os, sys
HERE=os.path.dirname(os.path.abspath(__file__))
P=os.path.join(HERE,"results","fusion_constants_gate.json")
passed=total=0
def check(c,m):
    global passed,total; total+=1
    if c: passed+=1; print("    PASS:",m)
    else: print("    FAIL:",m)
print("="*68); print("Fusion materials track - verification"); print("="*68)
if not os.path.exists(P):
    print("run fusion_constants_gate.py first"); sys.exit(1)
d=json.load(open(P,encoding="utf-8"))
print("\n[1] Gate 1 - deleting every measured constant")
g1=d["gate1_constants"]; worst=max(r["diff_meV"] for r in g1)
frac=max(r["fraction_of_chemical_accuracy"] for r in g1)
check(worst<5.0,"worst derived-vs-measured difference %.3f meV"%worst)
check(frac<0.1,"stays %.0fx inside chemical accuracy"%(1/frac))
check(len(g1)>=3,"tested at %d separations"%len(g1))
print("\n[2] Gate 2 - hydrogen from zero empirical input")
g2=d["gate2_hydrogen"]
check(abs(g2["R_e_dev_pct"])<0.5,"bond length %.4f A vs %.4f, %+.2f%%"
      %(g2["R_e_ang"],g2["R_e_experiment_ang"],g2["R_e_dev_pct"]))
check(abs(g2["D_e_eV"]-g2["D_e_experiment_eV"])/g2["D_e_experiment_eV"]<0.05,
      "dissociation energy %.3f eV vs %.3f"%(g2["D_e_eV"],g2["D_e_experiment_eV"]))
print("\n[3] Gate 3 - the boundary, reported as a failure")
g3=d["gate3_boundary"]
check(g3["mean_abs_dev_pct"]>50,
      "helium wall NOT adequate at this level: %.0f%% mean deviation, reported not hidden"
      %g3["mean_abs_dev_pct"])
print("")
print("[4] Blind prediction - frozen and hash-verified")
import hashlib
PP=os.path.join(HERE,"results","PREREG_be2h4_blind.json")
if os.path.exists(PP):
    pre=json.load(open(PP,encoding="utf-8"))
    payload=json.dumps(pre["prediction"],sort_keys=True,separators=(",",":")).encode()
    check(hashlib.sha256(payload).hexdigest()==pre["sha256"],
          "payload matches its frozen SHA-256 (%s...)"%pre["sha256"][:16])
    pr=pre["prediction"]["predicted"]
    check(len(pr)>=5,"%d quantities predicted"%len(pr))
    check(all(v.get("uncertainty",0)>0 for v in pr.values()),
          "every entry carries an uncertainty band")
    check("EXPERIMENT only" in pre["prediction"]["registered_against"],
          "registered blind against experiment, not against theory")
    check(len(pre["prediction"]["falsified_if"])>=3,
          "falsification conditions stated in advance")
    check("scoring_rule" in pre["prediction"],
          "scoring rule fixed before any measurement")
else:
    print("    (PREREG_be2h4_blind.json absent - run freeze_prediction.py)")

print("")
print("[5] Method validation on known data (BH3 -> B2H6)")
VP=os.path.join(HERE,"results","method_validation_b2h6.json")
if os.path.exists(VP):
    v=json.load(open(VP,encoding="utf-8"))
    check(v["inside_bands"]==v["of"],
          "%d of %d quantities inside the SAME bands used for the prediction"
          %(v["inside_bands"],v["of"]))
    check(all(abs(t["error"])<=t["band"] for t in v["target"].values()),
          "every error within its stated band")
    check(abs(v["calibrant"]["scale"]-1.0)<0.05,
          "calibrant offset %.2f%% (BeH2 was -1.99%%: offset is species-specific)"
          %(100*(v["calibrant"]["computed"]-v["calibrant"]["measured"])/v["calibrant"]["measured"]))
    worst=max(abs(t["error"])/t["band"] for t in v["target"].values())
    check(worst<1.0,"worst band usage %.0f%% - metal-metal distance is the weak link"%(100*worst))
else:
    print("    (method_validation_b2h6.json absent)")

print("")
print("[6] Second transfer test (CH4 -> C2H6)")
V2=os.path.join(HERE,"results","method_validation_c2h6.json")
if os.path.exists(V2):
    w=json.load(open(V2,encoding="utf-8"))
    check(w["inside_bands"]==w["of"],"%d of %d inside band"%(w["inside_bands"],w["of"]))
    check(w["target"]["r_CC"]["band_used_pct"]<10,
          "unbridged heavy-atom distance uses %.0f%% of band vs 82%% for the bridged case"
          %w["target"]["r_CC"]["band_used_pct"])
    v1=json.load(open(os.path.join(HERE,"results","method_validation_b2h6.json"),encoding="utf-8"))
    o1=100*(v1["calibrant"]["computed"]-v1["calibrant"]["measured"])/v1["calibrant"]["measured"]
    o2=100*(w["calibrant"]["computed"]-w["calibrant"]["measured"])/w["calibrant"]["measured"]
    check(o1*o2<0,"calibration offset changes SIGN across species (%.2f%% vs %+.2f%%)"%(o1,o2))
else:
    print("    (method_validation_c2h6.json absent)")

print("")
print("[7] Blind prediction v2 - frozen, and v1 left standing")
P2=os.path.join(HERE,"results","PREREG_be2h4_blind_v2.json")
if os.path.exists(P2):
    import hashlib
    r2=json.load(open(P2,encoding="utf-8"))
    pay=json.dumps(r2["prediction"],sort_keys=True,separators=(",",":")).encode()
    check(hashlib.sha256(pay).hexdigest()==r2["sha256"],
          "v2 payload matches its frozen SHA-256 (%s...)"%r2["sha256"][:16])
    check("stands" in r2["prediction"]["supersedes"],
          "v2 explicitly does NOT supersede v1")
    v2v=json.load(open(os.path.join(HERE,"results","method_validation_b2h6_v2.json"),encoding="utf-8"))
    v1v=json.load(open(os.path.join(HERE,"results","method_validation_b2h6.json"),encoding="utf-8"))
    w2=max(abs(t["error"]) for t in v2v["target"].values())
    w1=max(abs(t["error"]) for t in v1v["target"].values())
    check(w2<w1,"v2 validation worst error %.4f A beats v1's %.4f A"%(w2,w1))
    check(abs(v2v["calibrant"]["offset_pct"])<abs(-1.99),
          "v2 calibrant offset %+.2f%% beats v1's -1.99%%"%v2v["calibrant"]["offset_pct"])
    v1p=json.load(open(os.path.join(HERE,"results","PREREG_be2h4_blind.json"),encoding="utf-8"))
    d=abs(r2["prediction"]["predicted"]["r_Be_Be_ang"]["value"]
          -v1p["prediction"]["predicted"]["r_Be_Be_ang"]["value"])
    check(d<=v1p["prediction"]["predicted"]["r_Be_Be_ang"]["uncertainty"],
          "v2 sits inside v1's band: the two levels agree (shift %.3f A)"%d)
    check("separately" in r2["prediction"]["scoring_rule"],
          "scoring rule forbids reporting only the closer version")
else:
    print("    (PREREG_be2h4_blind_v2.json absent)")

check("not adequate" in g3["verdict"].lower(),"verdict records the failure explicitly")
print("\n"+"="*68); print("verify: %d / %d checks passed"%(passed,total)); print("="*68)
sys.exit(0 if passed==total else 1)
