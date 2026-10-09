"""Documentation and generated-artifact contract checks."""

import unittest

from scripts import build_prompt, validate


class DocumentationTests(unittest.TestCase):
    def test_documented_installation_and_development_entry_points(self):
        self.assertEqual(validate.validate_documentation(validate.ROOT), [])

    def test_standalone_prompt_exactly_matches_all_sources(self):
        self.assertEqual(validate.validate_prompt(validate.ROOT), [])

    def test_standalone_prompt_has_no_installed_skill_file_dependencies(self):
        prompt = build_prompt.render_prompt(validate.ROOT)
        targets, undefined = validate.markdown_links(prompt)
        self.assertEqual(undefined, [])
        for target in targets:
            with self.subTest(target=target):
                parsed = validate.urlsplit(target)
                if not parsed.scheme and not parsed.netloc:
                    self.assertEqual(parsed.path, "", "bundled local links must become in-document anchors")
                    self.assertIn(parsed.fragment, validate.markdown_anchors(prompt))


if __name__ == "__main__":
    unittest.main()
