"""Exercise observable scaffold safety and validator failure detection using temporary copies."""
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'plugins/vern-workspace/scripts'


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


new_case = load('new_case')
validator = load('validate_workspace')


class WorkspaceTests(unittest.TestCase):
    def test_shipped_workspace_passes(self):
        self.assertEqual(validator.validate(ROOT), [])

    def test_creates_blank_case_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            case = new_case.create_case(Path(tmp), 'sample-case')
            self.assertTrue((case / 'outputs').is_dir())
            self.assertEqual(len((case / 'tasks.csv').read_text(encoding='utf-8').splitlines()), 1)
            (case / 'brief.md').write_text('Keep this user edit', encoding='utf-8')
            with self.assertRaises(FileExistsError):
                new_case.create_case(Path(tmp), 'sample-case')
            self.assertEqual((case / 'brief.md').read_text(encoding='utf-8'), 'Keep this user edit')

    def test_rejects_path_escape_and_windows_devices(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in ('../escape', '/absolute', 'a/b', 'a\\b', 'con', 'com1', ''):
                with self.subTest(name=name), self.assertRaises(ValueError):
                    new_case.create_case(Path(tmp), name)
            self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_detects_manifest_drift_and_broken_reference(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / 'Vern'
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns('__pycache__', 'cases', '.git'))
            portable = copy / 'plugins/vern-workspace/plugin.json'
            manifest = json.loads(portable.read_text(encoding='utf-8'))
            manifest['version'] = '0.2.0'
            portable.write_text(json.dumps(manifest), encoding='utf-8')
            (copy / 'plugins/vern-workspace/references/working-principles.md').unlink()
            errors = validator.validate(copy)
            self.assertTrue(any('identity mismatch' in e for e in errors))
            self.assertTrue(any('missing or escaping link' in e for e in errors))


if __name__ == '__main__':
    unittest.main()
