#!/usr/bin/env python3
"""Generate the architecture gallery, engineering activity feed, and project-health table."""

from __future__ import annotations

import base64
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import requests
import yaml
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / ".github" / "scripts" / "profile-portfolio.yml"
README_PATH = ROOT / "README.md"
NOTEBOOK_PATH = ROOT / "engineering-notebook" / "RECENT_ACTIVITY.md"
API_ROOT = "https://api.github.com"
FENCE = chr(96) * 3
GOOD_CONCLUSIONS = {"success", "skipped", "neutral"}
BAD_CONCLUSIONS = {"failure", "timed_out", "action_required", "startup_failure"}
SKIP_COMMIT_PATTERNS = (
    "chore(profile): refresh",
    "auto-update: current projects",
    "auto-update: current projects refreshed",
)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed.replace(tzinfo=timezone.utc) if parsed.tzinfo is None else parsed.astimezone(timezone.utc)


def clean(value: Any, limit: int = 180) -> str:
    text = " ".join(str(value or "").split()).replace("|", r"\|")
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def load_config() -> dict[str, Any]:
    with CONFIG_PATH.open("r", encoding="utf-8") as stream:
        config = yaml.safe_load(stream) or {}
    projects = config.get("featured_projects") if isinstance(config, dict) else None
    if not isinstance(projects, list) or not projects:
        raise ValueError("profile-portfolio.yml must define a non-empty featured_projects list.")
    seen = set()
    for project in projects:
        if not project.get("name") or not project.get("repo"):
            raise ValueError("Each featured project must define name and repo.")
        if project["repo"] in seen:
            raise ValueError(f"Duplicate repository configured: {project['repo']}")
        seen.add(project["repo"])
        nodes = project.get("architecture", {}).get("nodes")
        if not isinstance(nodes, list) or len(nodes) < 2:
            raise ValueError(f"{project['name']}: architecture needs at least two nodes.")
        for edge in project["architecture"].get("edges", []):
            if len(edge) < 2 or not all(isinstance(i, int) for i in edge[:2]):
                raise ValueError(f"{project['name']}: edges need integer source and target indexes.")
            if min(edge[0], edge[1]) < 0 or max(edge[0], edge[1]) >= len(nodes):
                raise ValueError(f"{project['name']}: an edge index is outside the node list.")
    return config


def build_session() -> requests.Session:
    session = requests.Session()
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    session.headers.update({
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "ayanalamMOON-profile-automation",
    })
    if token:
        session.headers["Authorization"] = f"Bearer {token}"
    retry = Retry(
        total=3, connect=3, read=3, backoff_factor=0.7,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET"]),
        respect_retry_after_header=True,
    )
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session


class GitHubAPI:
    def __init__(self, session: requests.Session):
        self.session = session
        self.cache: dict[str, Any] = {}

    def get(self, path: str, optional: bool = False) -> Any:
        url = path if path.startswith("https://") else API_ROOT + path
        if url in self.cache:
            return self.cache[url]
        response = self.session.get(url, timeout=25)
        if optional and response.status_code == 404:
            self.cache[url] = None
            return None
        response.raise_for_status()
        data = response.json()
        self.cache[url] = data
        return data


def mermaid_for(project: dict[str, Any]) -> str:
    architecture = project["architecture"]
    lines = ["flowchart LR"]
    for index, label in enumerate(architecture["nodes"]):
        text = str(label).replace(chr(34), "'").replace("\n", " ")
        lines.append(f"  N{index}[{json.dumps(text, ensure_ascii=False)}]")
    for edge in architecture.get("edges", []):
        source, target = edge[0], edge[1]
        label = clean(edge[2], 60) if len(edge) >= 3 else ""
        style = edge[3] if len(edge) >= 4 else ""
        if style == "feedback":
            lines.append(
                f"  N{source} -. {json.dumps(label, ensure_ascii=False)} .-> N{target}"
                if label else f"  N{source} -.-> N{target}"
            )
        else:
            lines.append(
                f"  N{source} -->|{label.replace(chr(124), '/')}| N{target}"
                if label else f"  N{source} --> N{target}"
            )
    return "\n".join(lines)


def architecture_markdown(items: list[dict[str, Any]]) -> str:
    content = [
        "The gallery prefers Mermaid diagrams documented in each project's README. If a README has no Mermaid diagram, it uses the corresponding high-level flow from the profile portfolio manifest.",
        "",
    ]
    for item in items:
        project = item["config"]
        name = clean(project["name"], 90)
        repo = project["repo"]
        description = clean(project.get("description", ""))
        diagram = item.get("readme_diagram") or mermaid_for(project)
        origin = "Source README diagram" if item.get("readme_diagram") else "Manifest fallback diagram"
        content.extend([
            "<details>",
            f"<summary><strong>{name}</strong> · <a href=\"https://github.com/{repo}\">repository</a></summary>",
            "",
            description,
            "",
            f"<sub>{origin}</sub>",
            "",
            FENCE + "mermaid",
            diagram,
            FENCE,
            "",
            "</details>",
            "",
        ])
    return "\n".join(content).strip()


def activity_label(message: str) -> str:
    title = message.splitlines()[0].strip() if message else "Commit"
    match = re.match(r"^(feat|feature|fix|perf|test|docs|refactor|build|ci|chore)(?:\([^)]*\))?:", title, re.I)
    if match:
        return {
            "feat": "Feature", "feature": "Feature", "fix": "Fix", "perf": "Performance",
            "test": "Tests", "docs": "Docs", "refactor": "Refactor", "build": "Build",
            "ci": "Automation", "chore": "Maintenance",
        }[match.group(1).lower()]
    lower = title.lower()
    if any(word in lower for word in ("benchmark", "latency", "throughput", "profil")):
        return "Performance"
    if any(word in lower for word in ("test", "coverage", "regression")):
        return "Tests"
    if any(word in lower for word in ("readme", "documentation", "docs")):
        return "Docs"
    return "Change"


def extract_readme_mermaid(readme_text: str) -> str | None:
    """Return the first documented Mermaid diagram, if the repository README has one."""
    blocks = re.findall(r"\`\`\`mermaid[ \t]*\r?\n(.*?)\r?\n\`\`\`", readme_text, flags=re.IGNORECASE | re.DOTALL)
    for block in blocks:
        diagram = block.strip()
        if diagram.startswith(("flowchart ", "flowchart\n", "graph ", "sequenceDiagram")):
            return diagram
    return None


def get_project_data(api: GitHubAPI, project: dict[str, Any]) -> dict[str, Any]:
    repo_name = project["repo"]
    metadata = api.get(f"/repos/{repo_name}")
    branch = metadata.get("default_branch") or "main"
    readme_payload = api.get(f"/repos/{repo_name}/readme", optional=True)
    readme_text = ""
    if isinstance(readme_payload, dict) and readme_payload.get("content"):
        try:
            readme_text = base64.b64decode(readme_payload["content"]).decode("utf-8", errors="replace")
        except (ValueError, TypeError):
            readme_text = ""
    readme_diagram = extract_readme_mermaid(readme_text)
    commits = api.get(f"/repos/{repo_name}/commits?sha={branch}&per_page=6")
    if not isinstance(commits, list):
        raise ValueError(f"GitHub returned an unexpected commit response for {repo_name}.")
    latest = commits[0] if commits else None
    latest_sha = latest.get("sha") if latest else None
    checks = api.get(f"/repos/{repo_name}/commits/{latest_sha}/check-runs?per_page=50") if latest_sha else {"check_runs": []}
    statuses = api.get(f"/repos/{repo_name}/commits/{latest_sha}/status") if latest_sha else {"statuses": []}
    release = api.get(f"/repos/{repo_name}/releases/latest", optional=True)
    return {
        "config": project,
        "metadata": metadata,
        "commits": commits,
        "readme_diagram": readme_diagram,
        "latest_sha": latest_sha,
        "check_runs": checks.get("check_runs", []) if isinstance(checks, dict) else [],
        "status_data": statuses if isinstance(statuses, dict) else {},
        "release": release,
    }


def check_state(item: dict[str, Any]) -> str:
    runs = item["check_runs"]
    statuses = item["status_data"].get("statuses", []) or []
    states = [str(s.get("state", "")).lower() for s in statuses]
    if any(state in {"failure", "error"} for state in states):
        return "Failing"
    if any(state == "pending" for state in states):
        return "Pending"
    conclusions = [str(run.get("conclusion") or "").lower() for run in runs]
    run_states = [str(run.get("status") or "").lower() for run in runs]
    if any(conclusion in BAD_CONCLUSIONS for conclusion in conclusions):
        return "Failing"
    if any(state != "completed" for state in run_states):
        return "Pending"
    if runs and all(conclusion in GOOD_CONCLUSIONS for conclusion in conclusions):
        return "Passing"
    if statuses and all(state == "success" for state in states):
        return "Passing"
    if runs or statuses:
        return "Needs review"
    return "No checks reported"


def health_markdown(items: list[dict[str, Any]]) -> str:
    lines = [
        "| Project | Latest commit checks | License | Latest release | Last push (UTC) |",
        "|---|---|---|---|---|",
    ]
    for item in items:
        config = item["config"]
        metadata = item["metadata"]
        repo_url = metadata.get("html_url", f"https://github.com/{config['repo']}")
        sha = item.get("latest_sha")
        check = f"[{check_state(item)}]({repo_url}/commit/{sha}/checks)" if sha else "Unavailable"
        license_data = metadata.get("license")
        license_name = clean(license_data.get("spdx_id") if isinstance(license_data, dict) else None, 40) or "Not specified"
        if license_name.upper() in {"NOASSERTION", "NONE"}:
            license_name = "Not specified"
        release = item.get("release")
        if isinstance(release, dict) and release.get("tag_name"):
            release_cell = f"[{clean(release['tag_name'], 40)}]({release.get('html_url', repo_url + '/releases')})"
        else:
            release_cell = "None published"
        pushed = parse_time(metadata.get("pushed_at"))
        pushed_label = pushed.strftime("%Y-%m-%d") if pushed else "Unknown"
        lines.append(f"| [{clean(config['name'], 80)}]({repo_url}) | {check} | {license_name} | {release_cell} | {pushed_label} |")
    lines.extend([
        "",
        "<sub>Checks apply to the latest commit on each default branch. “No checks reported” means GitHub returned no check runs or commit statuses for that commit; it is not a passing result. Release and license values come from repository metadata.</sub>",
    ])
    return "\n".join(lines)


def recent_activity(items: list[dict[str, Any]], days: int = 60, limit: int = 10) -> list[dict[str, Any]]:
    cutoff = utc_now() - timedelta(days=days)
    activity = []
    for item in items:
        config = item["config"]
        metadata = item["metadata"]
        for commit in item["commits"]:
            commit_info = commit.get("commit", {})
            message = str(commit_info.get("message") or "").strip()
            title = message.splitlines()[0] if message else "Commit"
            if any(pattern in title.lower() for pattern in SKIP_COMMIT_PATTERNS):
                continue
            committer = commit_info.get("committer", {}) or {}
            date = parse_time(committer.get("date"))
            if not date or date < cutoff:
                continue
            activity.append({
                "project": config["name"],
                "repo_url": metadata.get("html_url", f"https://github.com/{config['repo']}"),
                "title": clean(title, 135),
                "url": commit.get("html_url", metadata.get("html_url", "")),
                "date": date,
                "kind": activity_label(title),
            })
    activity.sort(key=lambda entry: entry["date"], reverse=True)
    deduplicated = []
    seen = set()
    for entry in activity:
        if entry["title"].lower().startswith("merge "):
            continue
        key = (entry["repo_url"], entry["title"].casefold())
        if key in seen:
            continue
        seen.add(key)
        deduplicated.append(entry)
    return deduplicated[:limit]


def activity_markdown(activity: list[dict[str, Any]], days: int = 60) -> str:
    if not activity:
        return (
            f"No default-branch commits were found in the last {days} days across the configured projects. "
            "Explore historical development through the repository links in the architecture gallery."
        )
    lines = [
        f"Automatically indexed from the configured repositories' default branches, covering the last {days} days.",
        "",
    ]
    for entry in activity:
        date = entry["date"].strftime("%Y-%m-%d")
        lines.append(
            f"- **{date} · {entry['kind']} · [{entry['project']}]({entry['repo_url']})** — "
            f"[{entry['title']}]({entry['url']})"
        )
    lines.extend([
        "",
        "Labels are inferred from commit subjects and are navigation hints only. This feed does not claim that a benchmark, experiment, or correctness result passed.",
    ])
    return "\n".join(lines)


def replace_section(content: str, key: str, replacement: str) -> str:
    start_marker = f"<!-- {key}-START -->"
    end_marker = f"<!-- {key}-END -->"
    if content.count(start_marker) != 1 or content.count(end_marker) != 1:
        raise ValueError(f"README.md must contain exactly one marker pair for {key}.")
    start = content.index(start_marker) + len(start_marker)
    end = content.index(end_marker, start)
    if end < start:
        raise ValueError(f"README.md markers for {key} are out of order.")
    return content[:start] + "\n" + replacement.strip() + "\n" + content[end:]


def main() -> int:
    try:
        config = load_config()
        api = GitHubAPI(build_session())
        items = [get_project_data(api, project) for project in config["featured_projects"]]
        activity = recent_activity(items)
        architecture = architecture_markdown(items)
        activity_text = activity_markdown(activity)
        health = health_markdown(items)

        readme = README_PATH.read_text(encoding="utf-8")
        readme = replace_section(readme, "ARCHITECTURE-GALLERY", architecture)
        readme = replace_section(readme, "ENGINEERING-NOTEBOOK", activity_text)
        readme = replace_section(readme, "PROJECT-HEALTH", health)

        NOTEBOOK_PATH.parent.mkdir(parents=True, exist_ok=True)
        notebook_text = "\n".join([
            "# Recent Engineering Activity",
            "",
            "Generated by the profile portfolio script from recent commits on configured projects' default branches.",
            "",
            activity_text,
            "",
            "For reproducible experiments, hypotheses, measurements, and limitations, use EXPERIMENT_TEMPLATE.md. The feed never infers results from commit messages.",
            "",
        ])

        # All remote data is acquired and validated before either output is replaced.
        README_PATH.write_text(readme, encoding="utf-8")
        NOTEBOOK_PATH.write_text(notebook_text, encoding="utf-8")
        print(f"Generated architecture gallery and project health for {len(items)} projects; indexed {len(activity)} recent commits.")
        return 0
    except (requests.RequestException, ValueError, OSError, KeyError, TypeError) as exc:
        print(f"Profile portfolio generation failed safely: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
