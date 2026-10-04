# EvidenceClaim

**Verify claims before they become a problem.**

Track: Everyday Automation | WCC Launchpad 30

**Live app:** link- https://evidenceclaim.streamlit.app/

## The problem

Club and event reimbursements get delayed or rejected because of missing receipts, mismatched amounts, reused invoices, or expenses dated outside the event. Treasurers and approvers usually check all of this by hand, which is slow and easy to get wrong.

## What it does

For every expense in a claim, EvidenceClaim checks that:

- The invoice, receipt and payment proof are all present
- The claimed amount matches every document
- The invoice number is not reused in another expense
- The date falls inside the event window
- The invoice amount does not exceed the quote (when a quote is given)

For each expense it shows a status (verified, warning, or review required), a plain-language reason, and what to do next. It also shows the total claimed amount needing review, a checks grid, and a downloadable CSV report.

## How it works

The verdicts come from plain Python rules in `rules.py`, not from an AI model. This makes results consistent, testable, and explainable: every flag states exactly which rule fired. `app.py` is the Streamlit interface that collects the claim and displays the results.

## Responsible design

- Nothing is approved, rejected, or submitted automatically. Issues are flagged for review, and a person makes the decision.
- There is no login and no stored data. Everything stays in the browser session.
- All demo data is synthetic.
- Every flag is explained, so users can see why something was raised.

## Testing

`tests.py` runs 20 synthetic cases with known correct answers. They cover missing documents, amount conflicts, date problems, duplicate invoice numbers, quote comparison, boundary dates, and combined problems.

Result: **20 of 20 passed**.

These tests show the rules behave as designed. They do not measure performance on real-world documents.

## Evidence behind the checks

We did not complete a user survey, so we do not claim measured demand among club treasurers. The checks are based on published reimbursement and invoice rules:

- UCSF Expense Reimbursement FAQ: https://supplychain.ucsf.edu/payments/claim-expenses-reimbursement/expense-reimbursement-faq
- UNLV Receipt Policy: https://www.unlv.edu/controller/accountspayable/receipts
- Louisiana DHH Missing Receipt Form: https://ldh.la.gov/assets/docs/fiscal/Travel_Reimbursment_Request_Missing_Receipt_Form.pdf
- U.S. government reimbursement document: https://www.govinfo.gov/content/pkg/CHRG-111hhrg58123/pdf/CHRG-111hhrg58123.pdf
- HMRC, duplicate invoices: https://www.gov.uk/hmrc-internal-manuals/vat-trader-records/vatrec8010
- GST Council, duplicate claims: https://gstcouncil.gov.in/node/4620
- CBIC GST invoice rules: https://cbic-gst.gov.in/gst-invoice-rules.html

We spoke with 5 students involved in clubs; 3 reported a receipt or amount problem.
## Limitations

- Claims are entered in a table. Reading invoices from photos or PDFs is not built yet.
- Vendor names are not compared.
- The rules are generic and not tied to one college's policy.
- Tested on synthetic cases only.

## Run locally

    pip install -r requirements.txt
    streamlit run app.py
    python tests.py

## Files

- `app.py`: the Streamlit interface
- `rules.py`: the checking rules
- `tests.py`: the 20 test cases
- `requirements.txt`: dependencies

## Tools used
Python, Streamlit and pandas. AI assistants were used during the hackathon: Claude and ChatGPT for brainstorming, code help, debugging and writing this README, 
The rules in rules.py and the 20 test cases were run and verified by the team.
