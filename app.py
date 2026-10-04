from datetime import date
import html
import pandas as pd
import streamlit as st
from rules import check_line, verdict

# ---- Rename the product here (first part white, second part blue) ----
BRAND_A, BRAND_B = "EVIDENCE", "CLAIM"
TAGLINE = "Verify claims before they become a problem."

st.set_page_config(page_title=f"{BRAND_A.title()}{BRAND_B.title()}",
                   page_icon="🧾", layout="wide")

st.markdown("""
<style>
#MainMenu, footer, header[data-testid="stHeader"] { visibility:hidden; height:0; }
.stApp { background:#E8EFFA; }
.block-container { max-width:1180px; padding-top:1.2rem; padding-bottom:3rem; }
html, body, [class*="css"] { font-family:'Inter','Segoe UI',system-ui,sans-serif; }

.hero { background:#0B1F3A; border-radius:22px; padding:52px 40px 40px;
  text-align:center; border-top:6px solid #2563EB; margin-bottom:30px; }
.hero-title { font-size:56px; font-weight:800; letter-spacing:3px; color:#fff; line-height:1.1; }
.hero-title span { color:#60A5FA; }
.hero-tag { font-size:20px; color:#D6E2F5; margin-top:14px; font-weight:500; }
.chips { margin-top:24px; display:flex; flex-wrap:wrap; gap:10px; justify-content:center; }
.chip { background:rgba(255,255,255,.10); color:#DCE8FA; font-size:13px; font-weight:600;
  padding:7px 14px; border-radius:999px; border:1px solid rgba(255,255,255,.16); }
.hero-note { margin-top:20px; font-size:12.5px; color:#8FA6C8; }

.step { display:flex; align-items:center; gap:12px; margin:30px 0 4px; }
.step .n { background:#2563EB; color:#fff; width:30px; height:30px; border-radius:50%;
  display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:700; }
.step .t { font-size:22px; font-weight:800; color:#0B1F3A; }
.step-sub { color:#5B6B82; font-size:14px; margin:0 0 14px 42px; }

.metric { background:#fff; border-radius:16px; padding:22px; min-height:132px;
  box-shadow:0 1px 3px rgba(11,31,58,.08); border-top:4px solid #2563EB; }
.metric.amber { border-top-color:#E0A100; }
.metric.red { border-top-color:#D64545; }
.m-label { font-size:11.5px; letter-spacing:.1em; font-weight:700; color:#5B6B82; }
.m-num { font-size:38px; font-weight:800; color:#0B1F3A; line-height:1.2; margin-top:4px; }
.m-num.green { color:#1E9E5A; } .m-num.amber { color:#C58A00; } .m-num.red { color:#D64545; }
.m-sub { font-size:13px; color:#64748B; }
.bar { background:#E3E8F0; height:8px; border-radius:6px; overflow:hidden; margin-top:12px; }
.bar > div { background:#2563EB; height:100%; border-radius:6px; }

.risk { background:#0B1F3A; color:#fff; border-radius:16px; padding:18px 24px;
  margin:18px 0; display:flex; justify-content:space-between;
  align-items:center; flex-wrap:wrap; gap:10px; }
.risk .lab { font-size:12px; letter-spacing:.1em; color:#9FB3D1; font-weight:700; }
.risk .amt { font-size:30px; font-weight:800; }
.risk .of { font-size:16px; color:#9FB3D1; font-weight:500; }
.risk .note { color:#9FB3D1; font-size:13px; max-width:340px; }

.matrix { width:100%; border-collapse:separate; border-spacing:0; background:#fff;
  border-radius:16px; overflow:hidden; box-shadow:0 1px 3px rgba(11,31,58,.08);
  margin-bottom:22px; }
.matrix th { background:#EEF3FB; color:#334155; font-size:12px; letter-spacing:.05em;
  padding:12px 10px; text-align:center; }
.matrix td { padding:12px 10px; text-align:center; border-top:1px solid #E6ECF5;
  font-size:14px; color:#1F3350; }
.matrix th:first-child, .matrix td:first-child { text-align:left; padding-left:18px; font-weight:700; }
.matrix td.y { color:#1E9E5A; font-weight:800; }
.matrix td.n { color:#D64545; font-weight:800; }

.rcard { background:#fff; border-radius:16px; padding:20px 22px; margin-bottom:16px;
  box-shadow:0 1px 3px rgba(11,31,58,.08); border-left:6px solid #CBD5E1; }
.rcard.ok { border-left-color:#1E9E5A; }
.rcard.warn { border-left-color:#E0A100; }
.rcard.bad { border-left-color:#D64545; }
.rhead { display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; }
.rname { font-size:19px; font-weight:800; color:#0B1F3A; }
.badge { font-size:11px; font-weight:800; letter-spacing:.07em; padding:5px 11px; border-radius:999px; }
.badge.ok { background:#E6F6EC; color:#157A45; }
.badge.warn { background:#FFF5D9; color:#8A6400; }
.badge.bad { background:#FDE8E8; color:#A32626; }
.issue { background:#F7F9FC; border-radius:10px; padding:10px 12px; margin-top:8px; }
.issue .msg { font-size:14px; font-weight:600; color:#1F3350; }
.issue .fix { font-size:12.5px; color:#64748B; margin-top:3px; }

.empty { background:#fff; border:1.5px dashed #B9C6DA; border-radius:16px;
  padding:34px; text-align:center; color:#5B6B82; }
.foot { text-align:center; color:#7A8AA3; font-size:12.5px; margin-top:34px; line-height:1.7; }

button[kind="primary"], div[data-testid="stBaseButton-primary"] {
  background:#2563EB; border:0; border-radius:10px; font-weight:700; }
button[kind="secondary"], div[data-testid="stBaseButton-secondary"] {
  border:1.5px solid #2563EB; color:#2563EB; background:#fff;
  border-radius:10px; font-weight:600; white-space:nowrap; }
</style>
""", unsafe_allow_html=True)

COLS = ["item", "claimed", "invoice_no", "invoice_amount",
        "receipt_amount", "payment_amount", "date"]

EXAMPLE = pd.DataFrame([
    ["Catering", 20000.0, "INV-221", 20000.0, 20000.0, 20000.0, date(2026, 9, 11)],
    ["Printing", 8500.0, "INV-305", 7800.0, 7800.0, 7800.0, date(2026, 9, 11)],
    ["Transport", 4000.0, "", 0.0, 0.0, 4000.0, date(2026, 9, 12)],
    ["Decoration", 12000.0, "INV-221", 12000.0, 12000.0, 12000.0, date(2026, 9, 20)],
], columns=COLS)

if "df" not in st.session_state:
    st.session_state.df = EXAMPLE.copy()
    st.session_state.ver = 0
if "results" not in st.session_state:
    st.session_state.results = None


def num(x):
    return float(x) if pd.notna(x) else 0.0


def to_iso(d):
    return pd.to_datetime(d).date().isoformat() if pd.notna(d) else None


def friendly(msg, line):
    low = msg.lower()
    if low.startswith("amount conflict"):
        parts = [f"claimed ₹{line['claimed']:,.0f}"]
        for k, label in [("invoice", "invoice"), ("receipt", "receipt"),
                         ("payment_proof", "payment proof")]:
            if line.get(k):
                parts.append(f"{label} ₹{line[k]['amount']:,.0f}")
        return ("Amounts don't match: " + ", ".join(parts),
                "Ask for a corrected document or claim the matching amount.")
    if low.endswith("missing"):
        doc = msg[: -len(" missing")]
        return (f"{doc.capitalize()} missing", f"Attach the {doc} before approval.")
    if "already used" in low:
        return (msg[0].upper() + msg[1:],
                "Check that this invoice isn't being claimed twice.")
    if "outside the event window" in low:
        return (msg[0].upper() + msg[1:],
                "Confirm the expense belongs to this event.")
    return (msg[0].upper() + msg[1:], "Review this manually.")


def step(n, title, sub):
    st.markdown(f'<div class="step"><span class="n">{n}</span>'
                f'<span class="t">{title}</span></div>'
                f'<div class="step-sub">{sub}</div>', unsafe_allow_html=True)


def matrix_html(results):
    heads = ["Expense", "Invoice", "Receipt", "Payment proof",
             "Amounts match", "Date in window", "Not duplicate"]
    rows = ""
    for r in results:
        line = r["line"]
        msgs = [m.lower() for _, m in r["findings"]]
        checks = [
            "invoice" in line,
            "receipt" in line,
            "payment_proof" in line,
            not any(m.startswith("amount conflict") for m in msgs),
            not any("outside the event window" in m for m in msgs),
            not any("already used" in m for m in msgs),
        ]
        cells = "".join(
            f'<td class="{"y" if ok else "n"}">{"✓" if ok else "✗"}</td>'
            for ok in checks)
        rows += f'<tr><td>{html.escape(r["item"])}</td>{cells}</tr>'
    th = "".join(f"<th>{h}</th>" for h in heads)
    return f'<table class="matrix"><tr>{th}</tr>{rows}</table>'


# ---------- Hero ----------
st.markdown(f"""
<div class="hero">
  <div class="hero-title">{BRAND_A}<span>{BRAND_B}</span></div>
  <div class="hero-tag">{TAGLINE}</div>
  <div class="chips">
    <span class="chip">📄 Missing documents</span>
    <span class="chip">⚖️ Amount mismatch</span>
    <span class="chip">🔁 Duplicate invoices</span>
    <span class="chip">📅 Date outside event</span>
  </div>
  <div class="hero-note">You stay in control: nothing is approved or submitted for you.</div>
</div>
""", unsafe_allow_html=True)

# ---------- 1. Event window ----------
step(1, "Event window", "Expenses dated outside these days will be flagged.")
c1, c2 = st.columns(2)
event_start = c1.date_input("Event start", value=date(2026, 9, 10))
event_end = c2.date_input("Event end", value=date(2026, 9, 15))

# ---------- 2. Expense evidence ----------
step(2, "Expense evidence", "One row per expense. Use 0 where a document is missing.")
b1, b2, _ = st.columns([1.4, 1.4, 3])
check_button = b1.button("Run verification", type="primary", use_container_width=True)
example_button = b2.button("Load demo claim", use_container_width=True)

if example_button:
    st.session_state.df = EXAMPLE.copy()
    st.session_state.ver += 1
    st.session_state.results = None
    st.rerun()

table = st.data_editor(
    st.session_state.df, num_rows="dynamic", use_container_width=True,
    hide_index=True, key=f"editor{st.session_state.ver}",
    column_config={
        "item": st.column_config.TextColumn("Expense"),
        "claimed": st.column_config.NumberColumn("Claimed (₹)", format="%.0f"),
        "invoice_no": st.column_config.TextColumn("Invoice no."),
        "invoice_amount": st.column_config.NumberColumn("Invoice (₹)", format="%.0f"),
        "receipt_amount": st.column_config.NumberColumn("Receipt (₹)", format="%.0f"),
        "payment_amount": st.column_config.NumberColumn("Payment proof (₹)", format="%.0f"),
        "date": st.column_config.DateColumn("Date"),
    },
)

# ---------- Run checks ----------
if check_button:
    event = {"start": event_start.isoformat(), "end": event_end.isoformat()}
    seen_invoices, results = set(), []
    for _, row in table.iterrows():
        d = to_iso(row["date"])
        no = str(row["invoice_no"]).strip() if pd.notna(row["invoice_no"]) else ""
        name = str(row["item"]) if pd.notna(row["item"]) else "(unnamed)"
        line = {"claimed": num(row["claimed"])}
        if num(row["invoice_amount"]) > 0:
            line["invoice"] = {"amount": num(row["invoice_amount"]),
                               "date": d, "no": no or None}
        if num(row["receipt_amount"]) > 0:
            line["receipt"] = {"amount": num(row["receipt_amount"]), "date": d}
        if num(row["payment_amount"]) > 0:
            line["payment_proof"] = {"amount": num(row["payment_amount"]), "date": d}
        findings = check_line(line, event, seen_invoices)
        results.append({"item": name, "status": verdict(findings),
                        "findings": findings, "line": line})
    st.session_state.results = results

# ---------- 3. Results ----------
step(3, "Verification results", "Review each expense. The final decision is yours.")

if st.session_state.results is None:
    st.markdown('<div class="empty">No results yet.<br>Click <b>Run verification</b> '
                'to check your claim, or <b>Load demo claim</b> to see how it works.</div>',
                unsafe_allow_html=True)
else:
    results = st.session_state.results
    total = len(results)
    verified = sum(1 for r in results if r["status"] == "Evidence complete")
    warnings = sum(1 for r in results if r["status"] == "Minor issues")
    review = sum(1 for r in results if r["status"] == "Review before approval")
    pct = int(verified / total * 100) if total else 0
    noun = "expense" if total == 1 else "expenses"

    m1, m2, m3, m4 = st.columns([1.6, 1, 1, 1])
    m1.markdown(f"""<div class="metric">
        <div class="m-label">VERIFICATION OVERVIEW</div>
        <div class="m-num">{verified} of {total}</div>
        <div class="m-sub">{noun} fully verified</div>
        <div class="bar"><div style="width:{pct}%"></div></div></div>""",
        unsafe_allow_html=True)
    m2.markdown(f"""<div class="metric">
        <div class="m-label">VERIFIED</div>
        <div class="m-num green">{verified}</div>
        <div class="m-sub">Evidence complete</div></div>""", unsafe_allow_html=True)
    m3.markdown(f"""<div class="metric amber">
        <div class="m-label">WARNINGS</div>
        <div class="m-num amber">{warnings}</div>
        <div class="m-sub">Minor issues</div></div>""", unsafe_allow_html=True)
    m4.markdown(f"""<div class="metric red">
        <div class="m-label">REVIEW REQUIRED</div>
        <div class="m-num red">{review}</div>
        <div class="m-sub">Needs your decision</div></div>""", unsafe_allow_html=True)

    claimed_total = sum(r["line"]["claimed"] for r in results)
    at_risk = sum(r["line"]["claimed"] for r in results
                  if r["status"] == "Review before approval")
    st.markdown(
        '<div class="risk"><div><div class="lab">CLAIMED AMOUNT NEEDING REVIEW</div>'
        f'<div class="amt">₹{at_risk:,.0f} <span class="of">of ₹{claimed_total:,.0f} claimed</span></div></div>'
        '<div class="note">Flagged for review, not rejected. You make the decision.</div></div>',
        unsafe_allow_html=True)
    st.markdown(matrix_html(results), unsafe_allow_html=True)

    order = {"Review before approval": 0, "Minor issues": 1, "Evidence complete": 2}
    ordered = sorted(results, key=lambda r: order[r["status"]])
    cols = st.columns(2)
    for i, r in enumerate(ordered):
        status = r["status"]
        if status == "Evidence complete":
            cls, label = "ok", "VERIFIED"
        elif status == "Minor issues":
            cls, label = "warn", "WARNING"
        else:
            cls, label = "bad", "REVIEW REQUIRED"
        body = ""
        for _, message in r["findings"]:
            msg, fix = friendly(message, r["line"])
            body += (f'<div class="issue"><div class="msg">{html.escape(msg)}</div>'
                     f'<div class="fix">→ {html.escape(fix)}</div></div>')
        if not body:
            body = ('<div class="issue"><div class="msg">'
                    'All required evidence checks passed.</div></div>')
        cols[i % 2].markdown(f"""<div class="rcard {cls}">
            <div class="rhead"><span class="rname">{html.escape(r["item"])}</span>
            <span class="badge {cls}">{label}</span></div>{body}</div>""",
            unsafe_allow_html=True)

    rows = []
    for r in results:
        issues = " | ".join(friendly(m, r["line"])[0] for _, m in r["findings"]) \
            if r["findings"] else "None"
        rows.append({"Expense": r["item"], "Status": r["status"], "Issues": issues})
    st.download_button("Download report (CSV)",
                       data=pd.DataFrame(rows).to_csv(index=False).encode("utf-8"),
                       file_name="evidenceclaim_report.csv", mime="text/csv")

st.markdown("""<div class="foot">Rule-based checks, not AI guesses.
Tested on 20 synthetic cases (20/20 passed).<br>
Flags and explains. A person makes every approval decision.</div>""",
            unsafe_allow_html=True)