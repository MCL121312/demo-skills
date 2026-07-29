import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_skills.py"


class ValidateSkillsTests(unittest.TestCase):
    def run_validator(self, root, cwd=None):
        return subprocess.run(
            [sys.executable, str(VALIDATOR), str(root)],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_repository_passes_from_another_working_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(ROOT)],
                cwd=temp_dir,
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("All validations passed!", result.stdout)

    def test_missing_template_type_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            copy_root = Path(temp_dir) / "repo"
            shutil.copytree(ROOT, copy_root)
            template = (
                copy_root
                / ".agents"
                / "skills"
                / "engineering-documents"
                / "templates"
                / "adr.md"
            )
            template.unlink()
            result = self.run_validator(copy_root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing templates", result.stdout)

    def test_malformed_template_frontmatter_is_reported(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            copy_root = Path(temp_dir) / "repo"
            shutil.copytree(ROOT, copy_root)
            template = (
                copy_root
                / ".agents"
                / "skills"
                / "engineering-documents"
                / "templates"
                / "adr.md"
            )
            template.write_text(
                template.read_text().replace("---\n", "---\nbad: [unclosed\n", 1)
            )
            result = self.run_validator(copy_root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("frontmatter YAML error", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_untyped_and_unknown_templates_are_reported_together(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            copy_root = Path(temp_dir) / "repo"
            shutil.copytree(ROOT, copy_root)
            template_dir = (
                copy_root
                / ".agents"
                / "skills"
                / "engineering-documents"
                / "templates"
            )
            adr = template_dir / "adr.md"
            adr.write_text(adr.read_text().replace("type: adr", "type: zzz-unknown", 1))
            srs = template_dir / "srs.md"
            srs.write_text(srs.read_text().replace("type: srs\n", "", 1))
            result = self.run_validator(copy_root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unknown template types", result.stdout)
        self.assertIn("missing field: type", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_empty_template_heading_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            copy_root = Path(temp_dir) / "repo"
            shutil.copytree(ROOT, copy_root)
            template = (
                copy_root
                / ".agents"
                / "skills"
                / "engineering-documents"
                / "templates"
                / "adr.md"
            )
            template.write_text(template.read_text() + "\n##\n")
            result = self.run_validator(copy_root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("empty heading", result.stdout)


if __name__ == "__main__":
    unittest.main()
