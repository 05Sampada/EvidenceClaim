REQUIRED = ["invoice", "receipt", "payment_proof"]

def check_line(line, event, seen_invoices):
    f = []
    for doc in REQUIRED:
        if not line.get(doc):
            f.append(("fail", f"{doc.replace('_', ' ')} missing"))

    amounts = {d: line[d]["amount"] for d in REQUIRED
               if line.get(d) and line[d].get("amount") is not None}
    if line.get("claimed") is not None:
        amounts["claimed"] = line["claimed"]
    if len(set(amounts.values())) > 1:
        f.append(("fail", f"amount conflict: {amounts}"))

    q, inv = line.get("quote"), line.get("invoice")
    if q and inv and inv["amount"] > q["amount"]:
        f.append(("warn", f"invoice ₹{inv['amount']} is above quote ₹{q['amount']}"))

    for d in REQUIRED:
        dt = (line.get(d) or {}).get("date")
        if dt and not (event["start"] <= dt <= event["end"]):
            f.append(("warn", f"{d} date {dt} is outside the event window"))

    no = inv.get("no") if inv else None
    if no:
        if no in seen_invoices:
            f.append(("fail", f"invoice {no} already used in another line"))
        seen_invoices.add(no)

    return f

def verdict(findings):
    levels = {lvl for lvl, _ in findings}
    if "fail" in levels:
        return "Review before approval"
    return "Minor issues" if "warn" in levels else "Evidence complete"