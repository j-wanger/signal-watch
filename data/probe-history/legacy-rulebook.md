# SYNTHETIC — Northbridge Bank Legacy Transaction Monitoring Rulebook

> **SYNTHETIC PROBE FIXTURE.** Every institution, rule, threshold, entity, and figure in this
> document is invented for the Phase-48 history-decomposition probe. No real customer,
> transaction, alert, or institutional data appears here or anywhere in `data/probe-history/`.
> This document is deliberately authored ADVISORY-SHAPED so it derives through the existing
> frozen gate unchanged — see the shape caveat in `docs/probe-history.md`.

## Overview

This rulebook consolidates the legacy rules deployed in the Northbridge Bank (a fictitious
institution) transaction monitoring system between 2014 and 2025. Each rule entry records the
rule identifier, the detection logic with its operating thresholds, and the underlying
indicator the rule was designed to detect. The indicator statements below are the derivation
surface: each describes the customer or transaction behaviour the rule encodes.

## Monitoring Rule Red Flag Indicators

**Rule TM-101 — Structuring below the reporting threshold.**
Logic: three or more cash deposits each between $8,000 and $9,999 into one account within any
rolling 7-day window.
Indicator: A customer makes multiple cash deposits just below the currency transaction
reporting threshold within a short period, in a pattern consistent with structuring to avoid
the filing requirement.

**Rule TM-102 — Rapid movement of funds.**
Logic: incoming credits ≥ $20,000 followed by outgoing debits of 90% or more of the credited
amount within 48 hours, twice in 30 days.
Indicator: Funds are deposited and then promptly withdrawn or transferred out within one to two
business days, leaving a minimal balance and showing no apparent business or personal purpose
for the pass-through activity.

**Rule TM-103 — Dormant account reactivation.**
Logic: no customer-initiated activity for 12 months, then aggregate transactions ≥ $50,000
within 30 days.
Indicator: A long-dormant account suddenly resumes activity with high-value incoming wires
followed by rapid disbursement, inconsistent with the account's historical profile.

**Rule TM-104 — Unexplained high-risk geography wires.**
Logic: any wire ≥ $10,000 to or from a jurisdiction on the institution's high-risk country
list where the customer profile records no business or family connection to that jurisdiction.
Indicator: A customer sends or receives international wire transfers involving high-risk
jurisdictions with no documented economic purpose or relationship to the destination country.

**Rule TM-105 — Repeated round-amount transfers.**
Logic: five or more transfers of identical round amounts (multiples of $1,000) to the same
beneficiary within 60 days.
Indicator: An account shows repeated transfers of identical round-dollar amounts to a single
beneficiary, a pattern inconsistent with commercial invoicing or payroll behaviour.

**Rule TM-106 — Cash activity inconsistent with business profile.**
Logic: monthly cash deposits exceeding 200% of the declared expected cash volume recorded at
onboarding, for two consecutive months.
Indicator: A business customer's cash deposit volume substantially and persistently exceeds
the expected activity stated in its onboarding profile, without a corresponding change in the
declared nature of the business.

**Rule TM-107 — Unrelated third-party deposits.**
Logic: deposits from four or more distinct third-party originators into a single personal
account within 30 days, aggregate ≥ $15,000.
Indicator: Multiple apparently unrelated third parties deposit funds into one personal
account, which is then drawn down by the account holder, suggesting use of the account to
pool or relay funds on behalf of others.

**Rule TM-108 — Transaction velocity spike.**
Logic: transaction count in any 7-day window exceeding six times the trailing 90-day weekly
average, minimum 25 transactions.
Indicator: An account exhibits a sudden spike in transaction frequency relative to its own
historical baseline that is not explained by seasonality or a documented life event.

**Rule TM-109 — Funnel account pattern.**
Logic: cash deposits into one account at branches in three or more distinct cities within
14 days, followed by consolidation and withdrawal or transfer in a different region.
Indicator: An account receives cash deposits in multiple geographically dispersed locations
followed by prompt consolidated withdrawal or onward transfer elsewhere, consistent with
funnel account activity used to move illicit proceeds across regions.

**Rule TM-110 — Incomplete originator information on incoming wires.**
Logic: two or more incoming wires within 90 days where originator name, address, or account
fields are missing, truncated, or populated with filler characters.
Indicator: Incoming wire transfers repeatedly arrive with missing or incomplete originator
information, suggesting deliberate stripping of payment details to obscure the source of
funds.

**Rule TM-111 — Adverse-media customer in new products.**
Logic: a customer carrying an adverse-media flag in the case management system opens or first
uses a product class (private banking, trade finance, virtual asset transfers) within 90 days
of the flag.
Indicator: A customer who is the subject of credible adverse media regarding financial crime
begins using new product lines or channels that materially increase the complexity or
opacity of their activity.

**Rule TM-112 — Split international remittances across MSBs.**
Logic: outgoing remittances from one customer through two or more money services business
counterparties to the same beneficiary country, each below $3,000, aggregate ≥ $9,000 in
30 days.
Indicator: A customer splits international remittances into multiple below-threshold
transactions routed through different money services businesses to the same destination,
consistent with deliberate fragmentation to avoid scrutiny.

For further information about this rulebook consult the Northbridge Bank model inventory
record NB-TM-2014-001 (SYNTHETIC — this document and that record are invented probe fixtures).

## Appendix A — Disposition codes used in the alert history (SYNTHETIC)

dismissed (closed, no suspicion documented) · escalated (referred to investigations) ·
sar_filed (escalation resulted in a regulatory filing) · data_requested (review paused
pending additional customer information, e.g. KYC refresh).
