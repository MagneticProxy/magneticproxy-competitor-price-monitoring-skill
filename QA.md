# QA and maintenance

## Reproducible package checks

Run `python3 -m unittest discover -s tests -v`. Checks validate the installable folder, local references, CSV output contract and evaluation fixture structure. They do not execute an LLM, authenticate to the product or consume account capacity.

For a release, install this repository into an isolated project with `npx skills add MagneticProxy/magneticproxy-competitor-price-monitoring-skill --skill competitor-price-monitoring --agent codex --yes --copy`, then check that the SKILL, references and assets were all copied. Test other agents separately before claiming compatibility.

## Scenario evaluation

Use [the worked example](skills/competitor-price-monitoring/references/worked-example.md) and [evals.json](evals/scenarios.json). Record actual agent output and the observed product result privately. No-account and insufficient-capacity paths must not be described as completed verification or collection. No automatic purchase, outreach or access-control bypass is permitted.

## Live acceptance

Confirm account access, approved scope and credit or bandwidth ceiling. Observe a small task through the current UI or documented integration, reconcile the output and capture redacted evidence with timestamp. Never publish customer data in test fixtures. A passing CI check is not evidence this live acceptance step passed.

## Maintenance

Recheck product links, pricing routes, source terms and agent installation when releasing a change. Keep prices and promotions in the current product instead of copying them here. Keep a change log and capture the installed commit for a reproducible evaluation.
