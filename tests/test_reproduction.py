import json,unittest,tempfile
from pathlib import Path
import numpy as np
from reproduction import verify,processing,tables
from reproduction.data import record,array,ROOT

class ReproductionTests(unittest.TestCase):
    def test_hashes(self):self.assertGreater(verify.check_inputs(),20)
    def test_all_tables(self):self.assertEqual(verify.check_numbers()['display_cells'],282)
    def test_proof_table_mapping(self):
        self.assertEqual(tables.LABELS[5],'tab:eos_summary')
        self.assertEqual(tables.LABELS[6],'tab:hypdelta_chi')
    def test_raw_damping_preserved(self):
        raw=array('tau','ka_UK100');selected=processing.tau_pts('ka_UK100')
        self.assertGreater(len(raw),len(selected))
        self.assertTrue(np.all(np.abs(selected[:,2])>=1e-16))
        self.assertTrue(np.any(np.abs(raw[:,2])<1e-16))
    def test_below_onset_splice(self):
        mass,freq,onset=processing.spliced_freq('nydelta','npemu')
        bm,bf=processing.g1_stable('npemu');selection=bm<onset
        np.testing.assert_array_equal(mass[mass<onset],bm[selection])
        np.testing.assert_array_equal(freq[mass<onset],bf[selection])
    def test_display_override_scope(self):
        overrides=record('published_display.json');self.assertEqual(len(overrides),2)
        for r in overrides:self.assertLess(abs(float(r['published_display'])-r['checkpoint_value_Hz']),.006)
    def test_no_false_terminal_maxima(self):
        rows=tables.generate()[5]
        self.assertNotIn('dagger',rows[0][1])
        self.assertTrue(all('dagger' in row[1] for row in rows[1:]))
    def test_tidal_upper_bound_and_missing_model(self):
        rows=tables.generate()[7]
        self.assertTrue(rows[0][-1].startswith(r'\lesssim'))
        self.assertEqual(rows[-1][-2:],['--','--'])
    def test_table_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            tables.write(Path(tmp))
            self.assertEqual(len(list(Path(tmp).glob('*.tex'))),8)
            for p in Path(tmp).glob('*.tex'):
                text=p.read_text();self.assertEqual(text.count('$')%2,0)

if __name__=='__main__':unittest.main()
