# Competitor Price Monitoring by Country with Magnetic Proxy | Agent Skill

A country-by-country price watchlist with confirmed changes, source URLs, timestamps, and reasons when a comparison is unsafe.

This public Agent Skill addresses **competitor price monitoring** with Magnetic Proxy residential routing where the job requires it. It is an independent use-case package, not an MCP or a claim that the product has completed an authenticated task.

## What you can ask an agent to do

> Monitor the same 500 ml product on three public stores in the US and Colombia. Alert me when the comparable displayed total changes by at least 5%.

**Example result (illustrative, not a live run):** Watchlist: 6 expected observations; 4 comparable, 1 blocked, 1 variant mismatch. US Store A: USD 24.00 → USD 26.00 (+8.3%), rechecked at 2026-09-28 15:00 UTC; evidence: URL and saved page excerpt. Colombia Store B: no comparison because the 2-pack variant differs. No external alert sent.

## Install

```bash
npx skills add MagneticProxy/magneticproxy-competitor-price-monitoring-skill --skill competitor-price-monitoring
```

Or copy this prompt into an agent that supports skill installation:

> Install the `competitor-price-monitoring` skill from https://github.com/MagneticProxy/magneticproxy-competitor-price-monitoring-skill and use it to help with: [describe your task]. Confirm installation, ask for my authorized inputs, and show me the proposed output before any external action.

Read the [skill instructions](skills/competitor-price-monitoring/SKILL.md). The agent needs compatible tools and access to your authenticated account to operate Magnetic Proxy; installation alone does not provide that access.

## Scope and trust

- **Input:** A user-approved watchlist of product URLs, canonical product/variant IDs, countries, comparison cadence, and alert threshold.
- **Output:** A country-by-country price watchlist with confirmed changes, source URLs, timestamps, and reasons when a comparison is unsafe.
- **Product:** [Magnetic Proxy Price Monitoring Capsule](https://www.magneticproxy.com/capsules/price-monitoring) and the [main product skill](https://github.com/MagneticProxy/magneticproxy-residential-proxy-agent-skills).
- **Current verification:** skill format and installation discovery are tested locally. An authenticated live product run has not yet been demonstrated for this repository.

The skill does not authorize purchases, scraping behind access controls, email sending, CRM writes, or publication. Third-party sites and product interfaces can change; the agent must observe the current state and report uncertainty.

## Review checklist

1. Does the agent request the right inputs and distinguish this job from the other use cases?
2. Does it make the product step observable and avoid inventing results?
3. Does the output preserve source rows/URLs, time, uncertainty, and a clear decision for the user?

Feedback and improvements can be filed as a GitHub issue in this repository.
