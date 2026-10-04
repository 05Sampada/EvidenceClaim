from rules import check_line, verdict

EV = {"start": "2026-09-10", "end": "2026-09-12"}
OK, MINOR, REVIEW = "Evidence complete", "Minor issues", "Review before approval"

def doc(amount, date="2026-09-11", no=None):
    d = {"amount": amount, "date": date}
    if no:
        d["no"] = no
    return d

def full(amt=5000, no="INV-1", **kw):
    line = {"claimed": amt, "invoice": doc(amt, no=no),
            "receipt": doc(amt), "payment_proof": doc(amt)}
    line.update(kw)
    return line

cases = [
    ("1 all matched", full(), OK, set()),
    ("2 payment proof missing",
     {"claimed": 5000, "invoice": doc(5000, no="A"), "receipt": doc(5000)}, REVIEW, set()),
    ("3 receipt missing",
     {"claimed": 5000, "invoice": doc(5000, no="A"), "payment_proof": doc(5000)}, REVIEW, set()),
    ("4 invoice missing",
     {"claimed": 5000, "receipt": doc(5000), "payment_proof": doc(5000)}, REVIEW, set()),
    ("5 receipt amount differs", full(receipt=doc(4500)), REVIEW, set()),
    ("6 invoice differs from claim", full(invoice=doc(4800, no="A")), REVIEW, set()),
    ("7 payment proof differs", full(payment_proof=doc(4000)), REVIEW, set()),
    ("8 claim differs from all docs", full(claimed=7000), REVIEW, set()),
    ("9 invoice date after event", full(invoice=doc(5000, "2026-09-20", "A")), MINOR, set()),
    ("10 invoice date before event", full(invoice=doc(5000, "2026-09-01", "A")), MINOR, set()),
    ("11 receipt date outside", full(receipt=doc(5000, "2026-09-25")), MINOR, set()),
    ("12 payment date outside", full(payment_proof=doc(5000, "2026-09-30")), MINOR, set()),
    ("13 invoice above quote", full(6000, quote=doc(5000)), MINOR, set()),
    ("14 invoice equals quote", full(5000, quote=doc(5000)), OK, set()),
    ("15 invoice below quote", full(4500, quote=doc(5000)), OK, set()),
    ("16 duplicate invoice ID", full(no="INV-9"), REVIEW, {"INV-9"}),
    ("17 invoice ID not a duplicate", full(no="INV-9"), OK, {"INV-1"}),
    ("18 no invoice number given", full(no=None), OK, set()),
    ("19 boundary dates inside window",
     full(invoice=doc(5000, "2026-09-10", "A"), receipt=doc(5000, "2026-09-12")), OK, set()),
    ("20 two problems at once",
     {"claimed": 5000, "invoice": doc(5000, "2026-09-20", "A"), "receipt": doc(5000)},
     REVIEW, set()),
]

passed = 0
for name, line, expected, prior in cases:
    got = verdict(check_line(line, EV, set(prior)))
    ok = got == expected
    passed += ok
    print("PASS" if ok else "FAIL", name, "->", got)

print(f"\n{passed}/{len(cases)} passed")