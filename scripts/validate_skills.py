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

# Templates may defer runtime-filled fields to decision brief / document contract.
PLACEHOLDER_FROM_CONTRACT = "<from-document-contract>"
PLACEHOLDER_FROM_BRIEF = "<from-decision-brief>"
ALLOWED_STATUS_PLACEHOLDERS = {PLACEHOLDER_FROM_CONTRACT}
ALLOWED_BRIEF_PLACEHOLDERS = {PLACEHOLDER_FROM_BRIEF}
ALLOWED_CYNEFIN_DOMAINS = {
    "confused",
    "clear",
    "complicated",
    "complex",
    "chaotic",
}
ALLOWED_CONFIDENCE = {"low", "medium", "high"}
REQUIRED_TEMPLATE_FIELDS = {
    "type",
    "status",
    "version",
    "cynefin_domain",
    "confidence",
    "behavior_mode",
    "source_decision_brief",
}
def get_enums(value):
    if not isinstance(value, str):
        return []
    return [item.strip() for item in value.split("|")]


def is_placeholder(value, allowed):
    return isinstance(value, str) and value in allowed


def load_frontmatter(path):
    with path.open() as file:
        content = file.read()
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return None
    return yaml.safe_load(match.group(1))


def validate(root=None):
    errors = []
    root = Path(root) if root else Path(__file__).resolve().parents[1]
    base_dir = root / ".agents/skills"
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

    template_types = set()
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

        missing_fields = REQUIRED_TEMPLATE_FIELDS - frontmatter.keys()
        for field in sorted(missing_fields):
            errors.append(f"[Template] {template_file.name} missing field: {field}")

        status = frontmatter.get("status")
        confidence = frontmatter.get("confidence")
        behavior_mode = frontmatter.get("behavior_mode")
        cynefin_domain = frontmatter.get("cynefin_domain")

        template_type = frontmatter.get("type")
        # None is already reported as a missing field; keeping it out of the set
        # avoids sorting str against None later.
        if template_type is not None:
            template_types.add(template_type)
        if template_type not in meta_types:
            errors.append(
                f"[Template] {template_file.name} has invalid type: "
                f"{template_type!r}"
            )
        if status not in meta_status and not is_placeholder(
            status, ALLOWED_STATUS_PLACEHOLDERS
        ):
            errors.append(
                f"[Template] {template_file.name} has invalid status: {status!r}"
            )
        if behavior_mode not in ALLOWED_BEHAVIORS and not is_placeholder(
            behavior_mode, ALLOWED_BRIEF_PLACEHOLDERS
        ):
            errors.append(
                f"[Template] {template_file.name} has invalid behavior_mode: "
                f"{behavior_mode!r}"
            )
        if cynefin_domain is not None and not is_placeholder(
            cynefin_domain, ALLOWED_BRIEF_PLACEHOLDERS
        ):
            if cynefin_domain not in ALLOWED_CYNEFIN_DOMAINS:
                errors.append(
                    f"[Template] {template_file.name} has invalid "
                    f"cynefin_domain: {cynefin_domain!r}"
                )
        if confidence is not None and not is_placeholder(
            confidence, ALLOWED_BRIEF_PLACEHOLDERS
        ):
            if confidence not in ALLOWED_CONFIDENCE:
                errors.append(
                    f"[Template] {template_file.name} has invalid "
                    f"confidence: {confidence!r}"
                )
        # Concrete low confidence must stay exploratory; placeholders are
        # resolved at document creation time by engineering-documents.
        if (
            confidence == "low"
            and status not in {None, "exploratory-draft"}
            and not is_placeholder(status, ALLOWED_STATUS_PLACEHOLDERS)
        ):
            errors.append(
                f"[Template] {template_file.name} cannot use status "
                f"{status!r} with low confidence"
            )

        body = template_file.read_text()
        if re.search(r"^#{1,6}\s*$", body, re.MULTILINE):
            errors.append(f"[Template] {template_file.name} contains an empty heading")

    # exploratory-prd intentionally reuses the prd template.
    template_types_with_aliases = set(template_types)
    if "prd" in template_types:
        template_types_with_aliases.add("exploratory-prd")
    missing_templates = meta_types - template_types_with_aliases
    extra_templates = template_types - meta_types
    if missing_templates:
        errors.append(f"[Template] Missing templates for types: {sorted(missing_templates)}")
    if extra_templates:
        errors.append(f"[Template] Unknown template types: {sorted(extra_templates)}")

    contract_required = {
        "type",
        "status",
        "purpose",
        "required_sections",
        "prohibited_sections",
        "source_decision_brief",
    }
    missing_contract_fields = contract_required - doc_contract.keys()
    for field in sorted(missing_contract_fields):
        errors.append(f"[Contract] document_contract missing field: {field}")
    for field in ("required_sections", "prohibited_sections"):
        if field in doc_contract and not isinstance(doc_contract[field], list):
            errors.append(f"[Contract] {field} must be a list")

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
    root = sys.argv[1] if len(sys.argv) > 1 else None
    sys.exit(validate(root))
