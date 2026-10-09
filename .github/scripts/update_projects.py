#!/usr/bin/env python3
"""Refresh the profile README's recently updated public project list."""

from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import requests
import yaml
from dateutil.relativedelta import relativedelta

USERNAME_DEFAULT = "ayanalamMOON"
API_VERSION = "2022-11-28"
PROJECTS_START = "<!-- PROJECTS-START -->"
PROJECTS_END = "<!-- PROJECTS-END -->"
BACKTICK = chr(96)

DEFAULT_CONFIG = {
    "github_username": USERNAME_DEFAULT,
    "max_projects": 6,
    "activity_threshold_months": 6,
    "excluded_projects": [USERNAME_DEFAULT, ".github"],
    "pinned_projects": [],
    "custom_descriptions": {},
    "project_tags": {},
    "show_language": True,
    "show_last_updated": True,
    "show_stats": False,
    "timezone": "UTC",
}


def load_config() -> dict:
    """Load configuration safely and validate the expected shapes."""
    config_path = os.path.join(os.path.dirname(__file__), "config.yml")
    try:
        with open(config_path, "r", encoding="utf-8") as stream:
            loaded = yaml.safe_load(stream) or {}
    except FileNotFoundError:
        print(f"Warning: {config_path} is missing; using defaults.", file=sys.stderr)
        loaded = {}

    if not isinstance(loaded, dict):
        raise ValueError("config.yml must contain a YAML mapping.")
    config = {**DEFAULT_CONFIG, **loaded}
    config["max_projects"] = max(1, min(int(config["max_projects"]), 20))
    config["activity_threshold_months"] = max(1, int(config["activity_threshold_months"]))
    for key in ("excluded_projects", "pinned_projects"):
        if not isinstance(config.get(key), list):
            raise ValueError(f"config.yml field {key!r} must be a list.")
    for key in ("custom_descriptions", "project_tags"):
        if not isinstance(config.get(key), dict):
            raise ValueError(f"config.yml field {key!r} must be a mapping.")
    return config


def parse_timestamp(value: str) -> datetime:
    """Parse GitHub ISO-8601 timestamps into timezone-aware UTC values."""
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def get_recent_projects(config: dict) -> list[dict]:
    """Fetch public owned repositories; prioritize configured pins, then recent activity."""
    username = config["github_username"]
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": API_VERSION,
        "User-Agent": f"Profile-README-Updater-{username}",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.get(
        f"https://api.github.com/users/{username}/repos",
        params={"sort": "updated", "direction": "desc", "per_page": 100, "type": "owner"},
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
    repos = response.json()
    if not isinstance(repos, list):
        raise ValueError("GitHub API returned an unexpected repository response.")

    excluded = set(config["excluded_projects"])
    available = {
        repo["name"]: repo
        for repo in repos
        if not repo.get("fork")
        and not repo.get("private", False)
        and not repo.get("archived", False)
        and repo["name"] not in excluded
    }

    pinned = []
    for name in config["pinned_projects"]:
        repo = available.get(name)
        if repo:
            pinned.append(repo)
        else:
            print(f"Warning: pinned project {name!r} was not found among accessible public repositories.")

    pinned_names = {repo["name"] for repo in pinned}
    cutoff = datetime.now(timezone.utc) - relativedelta(months=config["activity_threshold_months"])
    recent = [
        repo for repo in available.values()
        if repo["name"] not in pinned_names
        and parse_timestamp(repo["updated_at"]) >= cutoff
    ]
    recent.sort(key=lambda item: parse_timestamp(item["updated_at"]), reverse=True)
    return (pinned + recent)[: config["max_projects"]]


def relative_updated_label(updated_at: datetime, now: datetime) -> str:
    """Create a readable relative timestamp label."""
    days = max(0, (now - updated_at).days)
    if days == 0:
        return "Today"
    if days == 1:
        return "Yesterday"
    if days < 7:
        return f"{days} days ago"
    if days < 30:
        weeks = days // 7
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    months = max(1, (now.year - updated_at.year) * 12 + now.month - updated_at.month)
    if months < 12:
        return f"{months} month{'s' if months != 1 else ''} ago"
    years = months // 12
    return f"{years} year{'s' if years != 1 else ''} ago"


def clean_markdown_text(value: object) -> str:
    """Keep generated single-line metadata from breaking README formatting."""
    text = " ".join(str(value or "").split())
    return text.replace("|", r"\|")


def format_project_section(projects: list[dict], config: dict) -> str:
    """Render the dynamic project list using configured display options."""
    zone_name = config.get("timezone", "UTC")
    try:
        display_zone = ZoneInfo(zone_name)
    except Exception:
        print(f"Warning: unknown timezone {zone_name!r}; using UTC.", file=sys.stderr)
        display_zone = timezone.utc

    now_utc = datetime.now(timezone.utc)
    content = ["**Recently Updated Projects:**", ""]

    if not projects:
        content.extend(["_No public repositories matched the configured activity window._", ""])

    for repo in projects:
        name = clean_markdown_text(repo.get("name", "Repository"))
        url = repo.get("html_url", f"https://github.com/{config['github_username']}")
        description = config["custom_descriptions"].get(repo["name"]) or repo.get("description")
        description = clean_markdown_text(description or "Description not provided yet.")
        content.append(f"- **[{name}]({url})** — {description}")

        metadata = []
        language = repo.get("language")
        if config.get("show_language", True) and language:
            metadata.append(f"{BACKTICK}{clean_markdown_text(language)}{BACKTICK}")
        if config.get("show_last_updated", True):
            updated_at = parse_timestamp(repo["updated_at"])
            metadata.append(f"*Updated {relative_updated_label(updated_at, now_utc)}*")
        if config.get("show_stats", False):
            metadata.append(
                f"⭐ {int(repo.get('stargazers_count', 0)):,} · Forks {int(repo.get('forks_count', 0)):,}"
            )

        tags = config["project_tags"].get(repo["name"], [])
        if isinstance(tags, str):
            tags = [tags]
        if isinstance(tags, list):
            metadata.extend(
                f"{BACKTICK}{clean_markdown_text(tag)}{BACKTICK}"
                for tag in tags if str(tag).strip()
            )

        if metadata:
            content.append("  \n  " + " · ".join(metadata))
        content.append("")

    display_now = datetime.now(timezone.utc).astimezone(display_zone)
    content.append(f"*Last updated: {display_now.strftime('%B %d, %Y at %H:%M %Z')}*")
    return "\n".join(content)


def update_readme(projects_content: str) -> bool:
    """Replace exactly one marked block or fail safely without corrupting the README."""
    readme_path = "README.md"
    with open(readme_path, "r", encoding="utf-8") as stream:
        content = stream.read()

    if content.count(PROJECTS_START) != 1 or content.count(PROJECTS_END) != 1:
        raise ValueError("README.md must contain exactly one PROJECTS-START and PROJECTS-END marker.")

    start = content.index(PROJECTS_START) + len(PROJECTS_START)
    end = content.index(PROJECTS_END, start)
    if end < start:
        raise ValueError("README project markers are in the wrong order.")

    updated = content[:start] + "\n" + projects_content + "\n" + content[end:]
    if updated == content:
        print("README project section is already current.")
        return False

    with open(readme_path, "w", encoding="utf-8") as stream:
        stream.write(updated)
    print("README project section updated.")
    return True


def main() -> int:
    try:
        config = load_config()
        projects = get_recent_projects(config)
        print(f"Fetched {len(projects)} project(s) for {config['github_username']}.")
        update_readme(format_project_section(projects, config))
        return 0
    except (requests.RequestException, ValueError, OSError, KeyError) as exc:
        print(f"Profile update failed safely: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
