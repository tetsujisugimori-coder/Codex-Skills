import hashlib
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class ManifestTest(unittest.TestCase):
    def test_complete_sources_match_manifest(self):
        data = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
        self.assertEqual(data['schema'], 'codex-skills/v1')
        expected = {'gh-review-merge', 'gh-review-merge-sync', 'gh-commit-submit-review', 'pull-main'}
        self.assertEqual({s['name'] for s in data['skills']}, expected)
        self.assertEqual(len(data['skills']), len(expected))
        seen = set()
        for skill in data['skills']:
            prefix = pathlib.PurePosixPath('skills') / skill['name']
            paths = set()
            for entry in skill['files']:
                rel = pathlib.PurePosixPath(entry['path'])
                self.assertFalse(rel.is_absolute())
                self.assertNotIn('..', rel.parts)
                self.assertEqual(rel.parts[:2], prefix.parts)
                self.assertNotIn(str(rel), seen)
                seen.add(str(rel)); paths.add(str(rel))
                file = ROOT / rel
                self.assertFalse(any(p.is_symlink() for p in [file, *file.parents]))
                self.assertTrue(file.is_file())
                content = file.read_bytes()
                self.assertEqual(len(content), entry['bytes'])
                self.assertEqual(hashlib.sha256(content).hexdigest(), entry['sha256'])
            actual = {p.relative_to(ROOT).as_posix() for p in (ROOT / prefix).rglob('*') if p.is_file()}
            self.assertEqual(paths, actual)
            for required in ['SKILL.md', 'agents/openai.yaml', 'assets/icon.svg']:
                self.assertIn(str(prefix / required), paths)
            text = (ROOT / prefix / 'SKILL.md').read_text(encoding='utf-8')
            self.assertIn('\nname: ' + skill['name'] + '\n', text)

if __name__ == '__main__':
    unittest.main()
