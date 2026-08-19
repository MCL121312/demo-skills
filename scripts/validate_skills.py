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

# Shared baseline documents every skill may reference. Missing any of them turns
# the cross-skill references into broken links.
REQUIRED_SHARED_FILES = {
    "conventions.md",
    "cynefin.md",
    "engagement-and-behavior.md",
    "information-layers.md",
    "stakeholder-conflict.md",
}

# Markdown inside a skill directory uses skill-relative paths.
SKILL_RELATIVE_REFERENCE = re.compile(
    r"`((?:references/|\.\./\.\./shared/)[^`]+)`"
)
# README and docs/ use repository-root-relative paths.
ROOT_REFERENCE = re.compile(
    r"`((?:\.agents/|\.github/|docs/|scripts/|tests/)[^`]+)`"
)
# YAML comments cannot rely on the skill-relative form, because they sit one
# level deeper than SKILL.md; they use repository-root-relative paths instead.
YAML_ROOT_REFERENCE = re.compile(r"(\.agents/[A-Za-z0-9._/-]+)")


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


def check_shared_documents(root, errors):
    shared_dir = root / ".agents/shared"
    for name in sorted(REQUIRED_SHARED_FILES):
        if not (shared_dir / name).exists():
            errors.append(
                f"[Shared] Required shared document not found: "
                f".agents/shared/{name}"
            )


def check_enum_alignment(doc_metadata, errors):
    """Keep the enums hardcoded here in sync with document-metadata.yaml."""
    for field, allowed in (
        ("behavior_mode", ALLOWED_BEHAVIORS),
        ("cynefin_domain", ALLOWED_CYNEFIN_DOMAINS),
        ("confidence", ALLOWED_CONFIDENCE),
    ):
        declared = set(get_enums(doc_metadata.get(field)))
        if declared != allowed:
            errors.append(
                f"[Enum Mismatch] {field} differs between validator and "
                f"document-metadata.yaml: {sorted(declared ^ allowed)}"
            )


def check_schema_files_parse(base_dir, errors):
    for schema_file in sorted(base_dir.glob("*/references/*.yaml")):
        try:
            with schema_file.open() as file:
                yaml.safe_load(file)
        except yaml.YAMLError as exc:
            errors.append(
                f"[Schema] {schema_file.parent.parent.name}/references/"
                f"{schema_file.name} YAML error: {exc}"
            )


def check_references(root, base_dir, errors):
    for skill_dir in sorted(path for path in base_dir.glob("*") if path.is_dir()):
        for markdown in sorted(skill_dir.glob("*.md")):
            content = markdown.read_text()
            for reference in SKILL_RELATIVE_REFERENCE.findall(content):
                if not (skill_dir / reference).resolve().exists():
                    errors.append(
                        f"[Reference] Broken link in {skill_dir.name}/"
                        f"{markdown.name}: '{reference}'"
                    )

    root_documents = [root / "README.md"] + sorted((root / "docs").glob("*.md"))
    for markdown in root_documents:
        if not markdown.exists():
            errors.append(f"[Reference] Expected document not found: {markdown}")
            continue
        for reference in ROOT_REFERENCE.findall(markdown.read_text()):
            if not (root / reference).exists():
                errors.append(
                    f"[Reference] Broken link in {markdown.name}: '{reference}'"
                )

    for schema_file in sorted(base_dir.glob("*/references/*.yaml")):
        for reference in YAML_ROOT_REFERENCE.findall(schema_file.read_text()):
            if not (root / reference).exists():
                errors.append(
                    f"[Reference] Broken link in "
                    f"{schema_file.parent.parent.name}/references/"
                    f"{schema_file.name}: '{reference}'"
                )


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

    # Parsing must be verified before the eager loads below, otherwise a broken
    # schema surfaces as a traceback instead of a validation error.
    check_schema_files_parse(base_dir, errors)
    if errors:
        print_errors(errors)
        return 1

    with doc_metadata_path.open() as file:
        doc_metadata = yaml.safe_load(file)["document"]
    with doc_contract_path.open() as file:
        doc_contract = yaml.safe_load(file)["document_contract"]
    with decision_schema_path.open() as file:
        decision_schema = yaml.safe_load(file)["decision_brief"]

    check_shared_documents(root, errors)
    check_enum_alignment(doc_metadata, errors)
    check_references(root, base_dir, errors)

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

        # Reference links are checked for every markdown file by
        # check_references, so this loop only covers frontmatter.
        if not isinstance(frontmatter, dict):
            errors.append(f"[Skill] {skill_md.parent.name}/SKILL.md missing frontmatter")
            continue

        name = frontmatter.get("name")
        if not name or not frontmatter.get("description"):
            errors.append(
                f"[Skill] {skill_md.parent.name}/SKILL.md missing name or description"
            )
        elif name != skill_md.parent.name:
            errors.append(
                f"[Skill] {skill_md.parent.name}/SKILL.md declares name {name!r}, "
                f"which does not match its directory name"
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
