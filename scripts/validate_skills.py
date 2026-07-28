import re
import sys
from pathlib import Path

import yaml


ALLOWED_BEHAVIORS = {
    "clarification",
    "direct-execution",
    "expert-analysis",
    "iterative-discovery",
    "stabilization",
    "review-and-alignment",
}


def get_enums(value):
    if not isinstance(value, str):
        return []
    return [item.strip() for item in value.split("|")]


def load_frontmatter(path):
    with path.open() as file:
        content = file.read()
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return None
    return yaml.safe_load(match.group(1))


def validate():
    errors = []
    base_dir = Path(".agents/skills")
    documents_dir = base_dir / "engineering-documents"
    template_dir = documents_dir / "templates"

    doc_metadata_path = documents_dir / "references/document-metadata.yaml"
    doc_contract_path = documents_dir / "references/document-contract.yaml"
    decision_schema_path = base_dir / "engineering-decision/references/decision-schema.yaml"

    required_paths = [doc_metadata_path, doc_contract_path, decision_schema_path]
    for path in required_paths:
        if not path.exists():
            errors.append(f"[File] Required file not found: {path}")

    if errors:
        print_errors(errors)
        return 1

    with doc_metadata_path.open() as file:
        doc_metadata = yaml.safe_load(file)["document"]
    with doc_contract_path.open() as file:
        doc_contract = yaml.safe_load(file)["document_contract"]
    with decision_schema_path.open() as file:
        decision_schema = yaml.safe_load(file)["decision_brief"]

    meta_types = set(get_enums(doc_metadata.get("type")))
    contract_types = set(get_enums(doc_contract.get("type")))
    if meta_types != contract_types:
        errors.append(
            f"[Enum Mismatch] Type mismatch: {meta_types ^ contract_types}"
        )

    meta_status = set(get_enums(doc_metadata.get("status")))
    contract_status = set(get_enums(doc_contract.get("status")))
    if meta_status != contract_status:
        errors.append(
            f"[Enum Mismatch] Status mismatch: {meta_status ^ contract_status}"
        )

    if "project_complexity" not in decision_schema:
        errors.append("[Schema] decision_brief must contain project_complexity")
    if not (template_dir / "prd.md").exists():
        errors.append("[Template] prd.md is required for prd and exploratory-prd")

    for template_file in sorted(template_dir.glob("*.md")):
        try:
            frontmatter = load_frontmatter(template_file)
        except yaml.YAMLError as exc:
            errors.append(
                f"[Template] {template_file.name} frontmatter YAML error: {exc}"
            )
            continue

        if not isinstance(frontmatter, dict):
            errors.append(f"[Template] {template_file.name} missing frontmatter")
            continue

        required_fields = {
            "type",
            "status",
            "version",
            "cynefin_domain",
            "confidence",
            "behavior_mode",
            "source_decision_brief",
        }
        missing_fields = required_fields - frontmatter.keys()
        for field in sorted(missing_fields):
            errors.append(f"[Template] {template_file.name} missing field: {field}")

        if frontmatter.get("type") not in meta_types:
            errors.append(
                f"[Template] {template_file.name} has invalid type: "
                f"{frontmatter.get('type')!r}"
            )
        if frontmatter.get("status") not in meta_status:
            errors.append(
                f"[Template] {template_file.name} has invalid status: "
                f"{frontmatter.get('status')!r}"
            )
        if frontmatter.get("behavior_mode") not in ALLOWED_BEHAVIORS:
            errors.append(
                f"[Template] {template_file.name} has invalid behavior_mode: "
                f"{frontmatter.get('behavior_mode')!r}"
            )
        if (
            frontmatter.get("confidence") == "low"
            and frontmatter.get("status") != "exploratory-draft"
        ):
            errors.append(
                f"[Template] {template_file.name} cannot use status "
                f"{frontmatter.get('status')!r} with low confidence"
            )

    for skill_md in sorted(base_dir.glob("*/SKILL.md")):
        try:
            frontmatter = load_frontmatter(skill_md)
        except yaml.YAMLError as exc:
            errors.append(
                f"[Skill] {skill_md.parent.name}/SKILL.md frontmatter YAML error: {exc}"
            )
            frontmatter = None

        if not isinstance(frontmatter, dict):
            errors.append(f"[Skill] {skill_md.parent.name}/SKILL.md missing frontmatter")
        elif not frontmatter.get("name") or not frontmatter.get("description"):
            errors.append(
                f"[Skill] {skill_md.parent.name}/SKILL.md missing name or description"
            )

        with skill_md.open() as file:
            content = file.read()
        references = re.findall(r"`references/([^`]+)`", content)
        for reference in references:
            reference_path = skill_md.parent / "references" / reference
            if not reference_path.exists():
                errors.append(
                    f"[Reference] Broken link in {skill_md.parent.name}/SKILL.md: "
                    f"'references/{reference}'"
                )

    if errors:
        print_errors(errors)
        return 1

    print("All validations passed!")
    return 0


def print_errors(errors):
    print("Validation failed with following errors:")
    for error in errors:
        print(f"  - {error}")


if __name__ == "__main__":
    sys.exit(validate())
