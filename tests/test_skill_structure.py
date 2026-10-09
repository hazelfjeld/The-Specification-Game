"""Static installed-package checks, not evidence about model compliance."""

import unittest

from scripts import validate


class SkillStructureTests(unittest.TestCase):
    def test_portable_text_only_skill_and_metadata(self):
        self.assertEqual(validate.validate_skill(validate.ROOT), [])

    def test_all_local_markdown_links_and_anchors_resolve(self):
        self.assertEqual(validate.validate_links(validate.ROOT), [])

    def test_no_common_secret_patterns_in_repository_text(self):
        self.assertEqual(validate.scan_secrets(validate.ROOT), [])


if __name__ == "__main__":
    unittest.main()
