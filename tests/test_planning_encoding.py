"""Exercise real planning I/O with Python UTF-8 mode disabled."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PlanningEncodingTests(unittest.TestCase):
    def test_validator_under_non_utf8_locale(self):
        env = {**os.environ, 'LC_ALL': 'C', 'LANG': 'C',
               'PYTHONCOERCECLOCALE': '0', 'PYTHONUTF8': '0'}
        result = subprocess.run(
            [sys.executable, '-X', 'utf8=0', 'scripts/validate_planning.py'],
            cwd=ROOT, env=env, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr.decode('ascii', errors='replace'))

    def test_json_writer_uses_utf8_bytes(self):
        sys.path.insert(0, str(ROOT / 'scripts'))
        from render_backlog import write_json
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'data.json'
            write_json(path, {'name': '\u2014\u00e9'})
            self.assertIn('\u2014\u00e9'.encode('utf-8'), path.read_bytes())


if __name__ == '__main__':
    unittest.main()
