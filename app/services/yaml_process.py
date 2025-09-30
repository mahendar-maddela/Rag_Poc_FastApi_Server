import os
import re
import yaml
import logging

USER_RULES_PATH = "yamls/user_rules.yml"
os.makedirs("yamls", exist_ok=True)


class YamlFileProcessor:
    @staticmethod
    def create_yaml_from_extract(extract_str: str, file_path: str = USER_RULES_PATH) -> str:
        """
        Create or update YAML cleaning rules from a comma-separated string.
        Only adds rules; preserves existing ones.
        """
        patterns = [item.strip() for item in extract_str.split(",") if item.strip()]

        # Load existing rules or start fresh
        rules = {}
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    loaded = yaml.safe_load(f)
                    if isinstance(loaded, dict):
                        rules = loaded
                except yaml.YAMLError:
                    rules = {}

        # Ensure correct structure
        if "cleaning_user_rules" not in rules or not isinstance(rules["cleaning_user_rules"], dict):
            rules["cleaning_user_rules"] = {}
        if "elements" not in rules["cleaning_user_rules"] or not isinstance(rules["cleaning_user_rules"]["elements"], list):
            rules["cleaning_user_rules"]["elements"] = []

        # Add new patterns
        for p in patterns:
            rules["cleaning_user_rules"]["elements"].append({"pattern": p, "replacement": ""})

        # Write back to YAML
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(rules, f, sort_keys=False, allow_unicode=True, indent=2)

        return file_path

    @staticmethod
    def clean_md_text(text: str) -> str:
        """
        Clean Markdown text using ONLY user-defined YAML rules.
        Preserves tables and images.
        """
        if not text:
            return ""

        # Load rules from YAML if available
        rules_yaml = {}
        if os.path.exists(USER_RULES_PATH):
            with open(USER_RULES_PATH, "r", encoding="utf-8") as f:
                loaded = yaml.safe_load(f)
                if isinstance(loaded, dict):
                    rules_yaml = loaded

        rules = rules_yaml.get("cleaning_user_rules", {}).get("elements", [])

        cleaned_lines = []
        in_table = False

        for line in text.splitlines():
            stripped = line.strip()

            # Preserve tables and images without modification
            if stripped.startswith("|") and stripped.endswith("|"):
                cleaned_lines.append(line)
                in_table = True
                continue
            if in_table and not stripped:
                in_table = False
            if stripped.startswith("![Image_"):
                cleaned_lines.append(line)
                continue

            # Apply ONLY the YAML rules
            for rule in rules:
                pattern = rule.get("pattern")
                replacement = rule.get("replacement", "")
                if pattern:
                    try:
                        line = re.sub(pattern, replacement, line)
                    except re.error as e:
                        logging.warning(f"Invalid regex '{pattern}': {e}")

            cleaned_lines.append(line)

        return "\n".join(cleaned_lines).strip()
