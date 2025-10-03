#!/usr/bin/env python3
"""
GitHub Action script to automatically update README with current projects.
Fetches the most recently updated repositories and formats them for display.
"""

import requests
import re
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

def get_recent_projects(username, max_projects=5):
    """
    Fetch the most recently updated repositories for a user.

    Args:
        username (str): GitHub username
        max_projects (int): Maximum number of projects to return

    Returns:
        list: List of repository dictionaries
    """
    url = f"https://api.github.com/users/{username}/repos"
    params = {
        'sort': 'updated',
        'direction': 'desc',
        'per_page': 50,
        'type': 'owner'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        repos = response.json()

        # Filter out forks and profile repositories, focus on active projects
        active_repos = []
        for repo in repos:
            # Skip forks and the profile repository itself
            if repo['fork'] or repo['name'] == username:
                continue

            # Check if repository has been updated recently (within last 6 months)
            updated_at = datetime.fromisoformat(repo['updated_at'].replace('Z', '+00:00'))
            six_months_ago = datetime.now(timezone.utc) - relativedelta(months=6)

            if updated_at > six_months_ago:
                active_repos.append(repo)

        return active_repos[:max_projects]

    except requests.RequestException as e:
        print(f"Error fetching repositories: {e}")
        return []

def format_project_section(projects):
    """
    Format the projects list into markdown for README.

    Args:
        projects (list): List of repository dictionaries

    Returns:
        str: Formatted markdown string
    """
    if not projects:
        return "<!-- No recent projects found -->"

    content = []
    content.append("**🚀 Active Projects:**")
    content.append("")

    for repo in projects:
        # Get basic repo info
        name = repo['name']
        description = repo['description'] or "No description available"
        html_url = repo['html_url']
        language = repo['language'] or "Markdown"
        updated_at = datetime.fromisoformat(repo['updated_at'].replace('Z', '+00:00'))

        # Format last updated
        now = datetime.now(timezone.utc)
        diff = now - updated_at

        if diff.days == 0:
            last_updated = "Today"
        elif diff.days == 1:
            last_updated = "Yesterday"
        elif diff.days < 7:
            last_updated = f"{diff.days} days ago"
        elif diff.days < 30:
            weeks = diff.days // 7
            last_updated = f"{weeks} week{'s' if weeks > 1 else ''} ago"
        else:
            months = diff.days // 30
            last_updated = f"{months} month{'s' if months > 1 else ''} ago"

        # Create project entry
        project_line = f"- **[{name}]({html_url})** - {description}"
        if language:
            project_line += f"  \n  `{language}` • *Updated {last_updated}*"
        else:
            project_line += f"  \n  *Updated {last_updated}*"

        content.append(project_line)
        content.append("")

    # Add last updated timestamp
    content.append(f"*Last updated: {datetime.now(timezone.utc).strftime('%B %d, %Y at %H:%M UTC')}*")

    return "\n".join(content)

def update_readme(projects_content):
    """
    Update the README.md file with new projects content.

    Args:
        projects_content (str): Formatted projects markdown content
    """
    try:
        with open('README.md', 'r', encoding='utf-8') as file:
            content = file.read()

        # Pattern to match the projects section
        pattern = r'<!-- PROJECTS-START -->.*?<!-- PROJECTS-END -->'
        replacement = f'<!-- PROJECTS-START -->\n{projects_content}\n<!-- PROJECTS-END -->'

        # Replace the section
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

        # Write back to file
        with open('README.md', 'w', encoding='utf-8') as file:
            file.write(new_content)

        print("✅ README.md updated successfully!")

    except FileNotFoundError:
        print("❌ README.md file not found!")
    except Exception as e:
        print(f"❌ Error updating README.md: {e}")

def main():
    """Main function to run the update process."""
    username = "ayanalamMOON"

    print(f"🔍 Fetching recent projects for {username}...")
    projects = get_recent_projects(username)

    if projects:
        print(f"📋 Found {len(projects)} active projects")
        for project in projects:
            print(f"  - {project['name']} ({project['language'] or 'N/A'})")
    else:
        print("⚠️  No recent projects found")

    print("📝 Formatting projects content...")
    projects_content = format_project_section(projects)

    print("🔄 Updating README.md...")
    update_readme(projects_content)

    print("🎉 Process completed!")

if __name__ == "__main__":
    main()
