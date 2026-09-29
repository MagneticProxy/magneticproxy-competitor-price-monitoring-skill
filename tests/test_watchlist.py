import importlib.util
import unittest
from pathlib import Path
spec = importlib.util.spec_from_file_location('watchlist', Path(__file__).resolve().parents[1] / 'skills/competitor-price-monitoring/scripts/compare_watchlist.py')
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)


def row(**kw):
    r = dict(product_id='p1', variant_id='v1', source_url='https://example.com/p1', requested_country='US', observed_country='US', comparison_status='confirmed', observed_at_utc='2026-09-29T12:00:00Z', evidence='synthetic-1', normalized_price='100', currency='USD', seller='store1', shipping='excluded', tax_context='excluded', promotion_context='public non-member', normalization_rule='unit price USD; no conversion', availability='in stock')
    r.update(kw)
    return r


class WatchlistTests(unittest.TestCase):
    def result(self, **kw):
        return w.compare([row()], [row(**kw)])['observations'][0]
    def test_same_context_delta_requires_confirmation(self):
        r=self.result(normalized_price='90')
        self.assertEqual(r['outcome'], 'candidate_price_change')
        self.assertEqual(r['change_pct'], '-10.00')
        self.assertTrue(r['requires_recheck'])
    def test_changed_commercial_context_never_price_alert(self):
        for field in w.CONTEXT:
            with self.subTest(field=field):
                self.assertEqual(self.result(normalized_price='90', **{field:'different'})['outcome'], 'context_changed')
    def test_missing_context_never_comparable(self):
        for field in w.CONTEXT:
            self.assertEqual(self.result(**{field:''})['outcome'], 'not_comparable')
    def test_wrong_exit_retained_without_price_alert(self):
        r=self.result(observed_country='CA', normalized_price='90')
        self.assertEqual(r['outcome'], 'unverified')
        self.assertEqual(r['reason'], 'exit_country_mismatch')
    def test_blocked_row_retained(self):
        self.assertEqual(self.result(comparison_status='blocked')['outcome'], 'unverified')
    def test_previous_unverified_not_baseline(self):
        self.assertEqual(w.compare([row(comparison_status='blocked')], [row()])['observations'][0]['outcome'], 'unverified')
    def test_missing_time_or_evidence_unverified(self):
        for field in ('evidence','observed_at_utc'):
            self.assertEqual(self.result(**{field:''})['outcome'], 'unverified')
    def test_unknown_or_nonfinite_price_not_alert(self):
        for value in ('',None,'NaN','Infinity','-1','$90'):
            self.assertEqual(self.result(normalized_price=value)['outcome'], 'not_comparable')
    def test_unchanged_and_threshold(self):
        self.assertEqual(self.result()['outcome'], 'unchanged')
        self.assertEqual(self.result(normalized_price='99')['outcome'], 'below_threshold')
    def test_new_and_missing_observations_preserved(self):
        r=w.compare([row()], [row(product_id='p2')])
        self.assertEqual(r['coverage_count'],2)
        self.assertEqual([x['outcome'] for x in r['observations']], ['new_observation','missing_current_observation'])
    def test_duplicate_identity_stops(self):
        for before,after in (([row(),row()], [row()]),([row()],[row(),row()])):
            with self.assertRaises(ValueError): w.compare(before,after)
    def test_missing_identity_stops(self):
        with self.assertRaises(ValueError): w.compare([], [row(variant_id='')])
    def test_invalid_threshold_stops(self):
        for t in ('NaN','Infinity','-1'):
            with self.assertRaises(ValueError): w.compare([], [], t)
    def test_country_case_equivalent(self):
        self.assertEqual(self.result(requested_country='us')['outcome'], 'unchanged')
