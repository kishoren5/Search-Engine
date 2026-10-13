import json
import random
import time
from pathlib import Path

TICKERS = ["JPM", "GS", "MS", "BAC", "C", "WFC", "BNP", "DB", "HSBC", "BARC"]
JURISDICTIONS = ["US", "EU", "UK", "CH", "SG", "HK"]
RISK_LEVELS = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

AML_TEMPLATES = [
    (
        "AML Suspicious Activity Report: Cash Structuring & Smurfing under CTR Limit",
        "Compliance monitoring flagged multiple sequential transactions of ${amt:,.2f} executed within 48 hours for entity affiliated with {ticker}. Account activity exhibits classic smurfing patterns designed to circumvent Currency Transaction Reporting (CTR) thresholds under 31 CFR 1010.311. Correspondent wire originated from {jur} with immediate onward transfer to an offshore shell entity. Financial Crimes Enforcement Network (FinCEN) SAR filing initiated under Risk Category: {risk}.",
        "AML_SAR",
    ),
    (
        "AML Fraud Alert: Crypto Mixer Off-Ramp and Layering Operation",
        "Automated transaction monitoring detected high-velocity incoming transfers totaling ${amt:,.2f} originating from non-custodial privacy mixing protocols into commercial checking accounts held at {ticker} {jur} branch. Funds were immediately converted into euro-denominated commercial paper. Enhanced Due Diligence (EDD) triggered due to high risk of illicit layering and sanctions evasion. Risk level assigned: {risk}.",
        "AML_SAR",
    ),
    (
        "Sanctions Screening Alert: Potential OFAC SDN Nexus on Correspondent Wire",
        "SWIFT payment message MT103 of ${amt:,.2f} routed through {ticker} intermediate clearing house was paused for secondary compliance audit. Beneficiary institution located in {jur} possesses indirect ownership links to Specially Designated Nationals (SDN) on the OFAC blacklist. Automated screening identified fuzzy match on beneficial owner. Risk classification: {risk}.",
        "AML_SAR",
    ),
]

SEC_TEMPLATES = [
    (
        "SEC Form 10-K Filing: Basel III Capital Adequacy and CET1 Ratio Analysis",
        "In its annual regulatory disclosure, {ticker} reported a Common Equity Tier 1 (CET1) capital ratio of 14.8%, comfortably exceeding the minimum regulatory requirement of 10.5% under Basel III and Dodd-Frank stress capital buffer guidelines. Total risk-weighted assets (RWA) stood at ${amt:,.2f}. The bank maintained a Liquidity Coverage Ratio (LCR) of 132%, demonstrating strong buffer against 30-day liquidity stress scenarios across {jur} banking subsidiaries.",
        "SEC_FILING",
    ),
    (
        "SEC Form 10-Q Filing: Net Interest Margin and Commercial Real Estate Exposure",
        "Quarterly earnings disclosure for {ticker} indicates a Net Interest Margin (NIM) of 2.68% amid monetary policy shifts. Provisions for credit losses increased to ${amt:,.2f}, driven primarily by elevated loss-given-default assumptions on office commercial real estate (CRE) mezzanine debt holdings. Non-performing asset ratio rose modestly to 0.74% across portfolios in {jur}.",
        "SEC_FILING",
    ),
    (
        "SEC Form 8-K Filing: Material Derivative Exposure and Counterparty Credit Risk",
        "Current report on Form 8-K: {ticker} disclosed gross notional derivative exposure of ${amt:,.2f} across interest rate swaps, foreign exchange forwards, and credit default swaps (CDS). Centrally cleared through ICE and LCH with initial margin posting compliance under EMIR and CFTC Part 23 uncleared margin rules in {jur}.",
        "SEC_FILING",
    ),
]

SWIFT_TEMPLATES = [
    (
        "SWIFT MT103 Interbank Wire Transfer: High-Value Cross-Border FX Settlement",
        "Wholesale payment message confirmed: Sender BIC {ticker}{jur}XXXX executed outward remittance of ${amt:,.2f} via CHIPS / Fedwire real-time gross settlement. Payment details specify spot USD/EUR currency swap execution with continuous linked settlement (CLS) finality. Automated AML and fraud scoring completed with status approved; risk score: {risk}.",
        "SWIFT_TX",
    ),
    (
        "ISO 20022 Pacs.008 Credit Transfer: Liquidity Rebalancing",
        "Interbank institutional credit transfer: {ticker} treasury operations executed nocturnal liquidity transfer of ${amt:,.2f} to Central Bank reserve facility in {jur}. Purpose code: INTC (Intra-company liquidity sweep) in accordance with EBA intra-day liquidity reporting standards.",
        "SWIFT_TX",
    ),
]

CREDIT_TEMPLATES = [
    (
        "Commercial Underwriting Dossier: Syndicated Credit Facility Risk Assessment",
        "Credit underwriting committee evaluation for {ticker}: Senior secured revolving credit facility of ${amt:,.2f} proposed for prime corporate borrower in {jur}. Debt-to-EBITDA leverage multiple stands at 3.4x, Debt Service Coverage Ratio (DSCR) is 2.1x. First-lien collateral valuation covers 165% of drawn facility. Internal credit rating: A-, default probability: 0.28%. Overall risk: {risk}.",
        "CREDIT_UNDERWRITING",
    ),
    (
        "Counterparty Margin & Collateral Stress Test Dossier",
        "Stress testing results for prime brokerage client accounts at {ticker}: Simulated 300 bps interest rate shock and 20% equity volatility surge. Total uncollateralized margin deficit estimated at ${amt:,.2f}. Mandatory variation margin call dispatched with 2-hour cure period under ISDA Master Agreement Credit Support Annex (CSA) in {jur}.",
        "CREDIT_UNDERWRITING",
    ),
]

ALL_CATEGORIES = [AML_TEMPLATES, SEC_TEMPLATES, SWIFT_TEMPLATES, CREDIT_TEMPLATES]


def generate_fintech_corpus(output_path: Path, num_docs: int = 50000) -> None:
    """Generate 50,000 realistic Fintech & BFSI records in JSONL format."""
    print(f"[*] Generating {num_docs:,} Fintech & BFSI records at {output_path}...")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    random.seed(1337)
    start_time = time.perf_counter()

    with open(output_path, "w", encoding="utf-8") as f:
        for i in range(num_docs):
            ticker = random.choice(TICKERS)
            jur = random.choice(JURISDICTIONS)
            risk = random.choice(RISK_LEVELS)
            category = random.choice(ALL_CATEGORIES)
            title_tpl, body_tpl, doc_type = random.choice(category)

            # Generate realistic amounts based on doc_type
            if doc_type == "AML_SAR":
                amt = random.uniform(8_500, 4_500_000)
            elif doc_type == "SEC_FILING":
                amt = random.uniform(50_000_000, 2_500_000_000)
            elif doc_type == "SWIFT_TX":
                amt = random.uniform(250_000, 75_000_000)
            else:  # CREDIT_UNDERWRITING
                amt = random.uniform(5_000_000, 350_000_000)

            title = f"{title_tpl} ({ticker} - {jur})"
            text = body_tpl.format(ticker=ticker, jur=jur, risk=risk, amt=amt)

            doc = {
                "doc_id": f"FIN-{i+1:06d}",
                "title": title,
                "text": text,
                "ticker": ticker,
                "doc_type": doc_type,
                "risk_level": risk,
                "amount": round(amt, 2),
                "jurisdiction": jur,
                "url": f"https://compliance-terminal.internal/records/FIN-{i+1:06d}",
            }
            f.write(json.dumps(doc) + "\n")

    elapsed = time.perf_counter() - start_time
    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"[+] Generated {num_docs:,} BFSI records ({size_mb:.2f} MB) in {elapsed:.2f}s ({num_docs / max(elapsed, 0.001):,.1f} docs/sec)")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Fintech / BFSI Corpus Generator")
    parser.add_argument("--docs", type=int, default=50000, help="Number of documents to generate")
    parser.add_argument("--output", type=str, default="data/raw/fintech_50k.jsonl", help="Output path")
    args = parser.parse_args()

    generate_fintech_corpus(Path(args.output), num_docs=args.docs)
