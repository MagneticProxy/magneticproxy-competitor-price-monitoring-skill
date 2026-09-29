#!/usr/bin/env python3
"""Compare the skill's CSV snapshots; retain coverage and require live rechecks."""
import argparse
import csv
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path

IDENTITY = ('product_id', 'variant_id', 'source_url', 'requested_country')
CONTEXT = ('currency', 'seller', 'shipping', 'tax_context', 'promotion_context', 'normalization_rule', 'availability')


def identity(row):
    if any(not str(row.get(k, '')).strip() for k in IDENTITY):
        raise ValueError('Every observation needs product_id, variant_id, source_url and requested_country')
    return tuple(str(row[k]).strip().upper() if k == 'requested_country' else str(row[k]).strip() for k in IDENTITY)


def index(rows):
    result = {}
    for row in rows:
        key = identity(row)
        if key in result:
            raise ValueError('Duplicate snapshot identity; disambiguate offers before comparison')
        result[key] = row
    return result


def observation_problem(row):
    if str(row.get('comparison_status', '')).lower() != 'confirmed':
        return 'observation_not_confirmed'
    if str(row.get('requested_country', '')).upper() != str(row.get('observed_country', '')).upper():
        return 'exit_country_mismatch'
    if not all(row.get(k) for k in ('evidence', 'observed_at_utc')):
        return 'missing_evidence_or_time'
    return None


def compare(previous, current, threshold=Decimal('5')):
    threshold = Decimal(str(threshold))
    if not threshold.is_finite() or threshold < 0:
        raise ValueError('Threshold must be finite and nonnegative')
    old, new = index(previous), index(current)
    output = []
    for key, row in new.items():
        prior = old.get(key)
        item = {'identity': list(key), 'current': row, 'previous': prior, 'outcome': None,
                'reason': None, 'change_pct': None, 'requires_recheck': False}
        problem = observation_problem(row)
        if problem:
            item.update(outcome='unverified', reason=problem)
        elif prior is None:
            item.update(outcome='new_observation', reason='no_previous_snapshot')
        elif observation_problem(prior):
            item.update(outcome='unverified', reason='previous_' + observation_problem(prior))
        elif any(row.get(k) in (None, '') or prior.get(k) in (None, '') for k in CONTEXT):
            item.update(outcome='not_comparable', reason='missing_commercial_context')
        elif any(row[k] != prior[k] for k in CONTEXT):
            item.update(outcome='context_changed', reason='different_comparison_basis', requires_recheck=True)
        else:
            try:
                before, after = Decimal(str(prior.get('normalized_price'))), Decimal(str(row.get('normalized_price')))
                if not before.is_finite() or not after.is_finite() or before <= 0 or after < 0:
                    raise ValueError('invalid_price')
                pct = (after-before) / before * 100
                item['change_pct'] = format(pct, '.2f')
                if before == after:
                    item['outcome'] = 'unchanged'
                elif abs(pct) < threshold:
                    item['outcome'] = 'below_threshold'
                else:
                    item.update(outcome='candidate_price_change', requires_recheck=True)
            except (InvalidOperation, ValueError):
                item.update(outcome='not_comparable', reason='invalid_or_missing_normalized_price')
        output.append(item)
    for key, prior in old.items():
        if key not in new:
            output.append({'identity': list(key), 'current': None, 'previous': prior,
                           'outcome': 'missing_current_observation', 'reason': 'not_proof_of_delisting_or_stock',
                           'change_pct': None, 'requires_recheck': False})
    return {'previous_count': len(previous), 'current_count': len(current), 'coverage_count': len(output),
            'threshold_pct': str(threshold), 'observations': output,
            'live_collection_performed': False, 'confirmed_price_alerts': 0}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('previous', type=Path)
    p.add_argument('current', type=Path)
    p.add_argument('--threshold-pct', type=Decimal, default=Decimal('5'))
    a = p.parse_args()
    def read(path):
        with path.open(encoding='utf-8-sig', newline='') as f:
            return list(csv.DictReader(f))
    print(json.dumps(compare(read(a.previous), read(a.current), a.threshold_pct), indent=2))


if __name__ == '__main__':
    main()
