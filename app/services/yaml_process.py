import os
import re
import yaml
import logging
import requests


USER_RULES_PATH = "yamls/user_rules.yml"
os.makedirs("yamls", exist_ok=True)



class YamlFileProcessor:
    @staticmethod
    def create_yaml_from_extract(extract_str: str, file_path: str = USER_RULES_PATH) -> str:
        """Create or update YAML cleaning rules from a comma-separated string."""
        patterns = [item.strip() for item in extract_str.split(",") if item.strip()]

        # Load existing rules or start fresh
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    rules = yaml.safe_load(f) or {}
                except yaml.YAMLError:
                    rules = {}
        else:
            rules = {}

        rules.setdefault("cleaning_user_rules", {}).setdefault("elements", [])

        for p in patterns:
            rules["cleaning_user_rules"]["elements"].append({"pattern": p, "replacement": ""})

        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(rules, f, sort_keys=False, allow_unicode=True, indent=2)

        return file_path

    @staticmethod
    def clean_md_text(text: str) -> str:
        """Clean Markdown text according to YAML rules."""
        if not text:
            return ""

        if os.path.exists(USER_RULES_PATH):
            with open(USER_RULES_PATH, "r", encoding="utf-8") as f:
                rules_yaml = yaml.safe_load(f) or {}
        else:
            rules_yaml = {}

        cleaned_lines = []
        in_table = False

        for line in text.splitlines():
            # Preserve tables and images
            stripped = line.strip()
            if stripped.startswith("|") and stripped.endswith("|"):
                cleaned_lines.append(line)
                in_table = True
                continue
            if in_table and not stripped:
                in_table = False
            if stripped.startswith("![Image_"):
                cleaned_lines.append(line)
                continue

            # Apply cleaning rules
            for rule in rules_yaml.get("cleaning_user_rules", {}).get("elements", []):
                pattern = rule.get("pattern")
                replacement = rule.get("replacement", "")
                if pattern:
                    try:
                        line = re.sub(pattern, replacement, line)
                    except re.error as e:
                        logging.warning(f"Invalid regex '{pattern}': {e}")

            if line.strip():  # Skip empty lines
                cleaned_lines.append(line)

        return "\n".join(cleaned_lines).strip()
