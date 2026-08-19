import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_skills.py"
# Local-only directories that are irrelevant to validation but dominate copy time.
IGNORED = shutil.ignore_patterns(".venv", ".git", "__pycache__", ".pytest_cache")


class ValidateSkillsTests(unittest.TestCase):
    def run_validator(self, root, cwd=None):
        return subprocess.run(
            [sys.executable, str(VALIDATOR), str(root)],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )

    def copy_repository(self, temp_dir):
        copy_root = Path(temp_dir) / "repo"
        shutil.copytree(ROOT, copy_root, ignore=IGNORED)
        return copy_root

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
            copy_root = self.copy_repository(temp_dir)
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
            copy_root = self.copy_repository(temp_dir)
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
            copy_root = self.copy_repository(temp_dir)
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
            copy_root = self.copy_repository(temp_dir)
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

    def test_missing_shared_document_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            copy_root = self.copy_repository(temp_dir)
            (copy_root / ".agents" / "shared" / "conventions.md").unlink()
            result = self.run_validator(copy_root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "Required shared document not found: .agents/shared/conventions.md",
            result.stdout,
        )

    def test_enum_drift_between_validator_and_metadata_is_reported(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            copy_root = self.copy_repository(temp_dir)
            metadata = (
                copy_root
                / ".agents"
                / "skills"
                / "engineering-documents"
                / "references"
                / "document-metadata.yaml"
            )
            metadata.write_text(
                metadata.read_text().replace(
                    "behavior_mode: clarification |", "behavior_mode: clarify |", 1
                )
            )
            result = self.run_validator(copy_root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("[Enum Mismatch] behavior_mode", result.stdout)

    def test_unparsable_reference_schema_is_reported(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            copy_root = self.copy_repository(temp_dir)
            schema = (
                copy_root
                / ".agents"
                / "skills"
                / "engineering-decision"
                / "references"
                / "decision-schema.yaml"
            )
            schema.write_text(schema.read_text() + "\nbroken: [unclosed\n")
            result = self.run_validator(copy_root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("[Schema]", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_broken_reference_in_examples_is_reported(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            copy_root = self.copy_repository(temp_dir)
            examples = (
                copy_root
                / ".agents"
                / "skills"
                / "engineering-decision"
                / "EXAMPLES.md"
            )
            backtick = chr(96)
            examples.write_text(
                examples.read_text()
                + "\n"
                + backtick
                + "references/does-not-exist.yaml"
                + backtick
                + "\n"
            )
            result = self.run_validator(copy_root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("references/does-not-exist.yaml", result.stdout)

    def test_skill_name_must_match_directory_name(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            copy_root = self.copy_repository(temp_dir)
            skill_md = (
                copy_root / ".agents" / "skills" / "engineering-decision" / "SKILL.md"
            )
            skill_md.write_text(
                skill_md.read_text().replace(
                    "name: engineering-decision", "name: engineering-decisions", 1
                )
            )
            result = self.run_validator(copy_root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not match its directory name", result.stdout)


if __name__ == "__main__":
    unittest.main()
