# Auto-Update README Workflow

This GitHub Actions workflow automatically updates your profile README with your current active projects.

## How it works

The workflow consists of two main components:

### 1. Scheduled Updates (`update-readme.yml`)
- Runs daily at 6 AM UTC
- Can be triggered manually from GitHub Actions tab
- Fetches your most recently updated repositories
- Updates the "Current Projects" section in your README

### 2. Activity-Based Updates (`update-on-activity.yml`)
- Triggers when you push to main branches
- Can be triggered manually or via API
- Ensures your README stays current with recent activity

## Configuration

You can customize the behavior by editing `.github/scripts/config.yml`:

- `max_projects`: Number of projects to display (default: 5)
- `activity_threshold_months`: How recent a project needs to be (default: 6 months)
- `excluded_projects`: Repositories to never show
- `pinned_projects`: Projects to always include
- `custom_descriptions`: Override project descriptions

## Manual Trigger

You can manually trigger the update by:

1. Going to the "Actions" tab in your repository
2. Selecting "Update README with Current Projects"
3. Clicking "Run workflow"

## What gets updated

The workflow automatically updates the section between these comments in your README:

```markdown
<!-- PROJECTS-START -->
[Your current projects will appear here]
<!-- PROJECTS-END -->
```

## Features

- ✅ Shows only active projects (updated within last 6 months)
- ✅ Displays programming language for each project
- ✅ Shows when each project was last updated
- ✅ Automatically excludes forks and your profile repository
- ✅ Responsive to your development activity
- ✅ Customizable through configuration file

## Setup

The workflow is already configured and will start working automatically. No additional setup required!

## Troubleshooting

If the workflow isn't updating:

1. Check the Actions tab for any failed runs
2. Ensure the README has the correct comment markers
3. Verify repository permissions allow Actions to write to the repository

## Security

The workflow uses only the default `GITHUB_TOKEN` with minimal permissions. It cannot access private repositories or sensitive information.
