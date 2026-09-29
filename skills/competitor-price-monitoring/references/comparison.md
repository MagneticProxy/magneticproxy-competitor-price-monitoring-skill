# Comparable price observations

Use the columns in [output.csv](../assets/output.csv) for both snapshots. Preserve a stable product ID, variant ID, source URL and requested country. A duplicate key stops the comparison so ambiguous offers cannot silently overwrite each other. Use a canonical variant-specific source URL consistently.

`raw_price` retains the original display. `normalized_price` is a plain decimal calculated under an explicit `normalization_rule`; the script does not parse localized prices or convert currency. Use explicit known contexts such as `shipping excluded`, `tax excluded` and `public non-member price`. An empty field means unknown, never zero.

Price comparison requires confirmed observations with matching requested/observed country, evidence and timestamps in both snapshots. Seller, currency, shipping, tax, promotion, normalization and availability must be known and identical. Different values yield a context change; missing values yield not comparable. Invalid/NaN/infinite prices never trigger a price alert.

A missing current observation means missing coverage, not delisting or out of stock. Coverage includes every current identity plus every previous identity absent now. Review the full ledger; an empty candidate list is not evidence that collection succeeded.

`candidate_price_change` is a proposed change. Reobserve once through a permitted verified route, compare the same context, attach the new evidence and only then mark a business alert confirmed. Never schedule or send an alert merely because the helper returned a candidate.
