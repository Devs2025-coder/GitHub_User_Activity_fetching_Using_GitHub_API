# GitHub User Activity CLI

> A powerful command-line tool to fetch and display GitHub user activity with advanced filtering capabilities.

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![GitHub API](https://img.shields.io/badge/GitHub-API%20v3-black)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Filter Options](#filter-options)
- [Examples](#examples)
- [Technical Details](#technical-details)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

GitHub User Activity CLI is a lightweight Python tool that retrieves and displays recent activity from any GitHub user's public profile. The application fetches data directly from the GitHub REST API and presents it in a clean, human-readable format in your terminal.

**Key Highlights:**
- Zero external dependencies - uses only Python standard library
- Smart filtering system for precise activity tracking
- Human-readable time formatting ("2 hours ago")
- Professional error handling
- Clean, well-documented code

## ✨ Features

- 📊 **Activity Display**: View commits, issues, PRs, stars, forks, and more
- 🔍 **Advanced Filtering**: Filter by event type, repository name, or date range
- ⏰ **Time Intelligence**: See when events occurred with relative timestamps
- 🎯 **Precision Control**: Limit results and combine multiple filters
- 🛡️ **Robust Error Handling**: Gracefully handles network issues and invalid inputs
- 🚀 **Fast & Lightweight**: No external dependencies, instant execution

## 📦 Installation

### Prerequisites

- Python 3.6 or higher
- Internet connection

### Quick Start

1. **Download the script:**
   ```bash
   # Clone the repository
   git clone https://github.com/yourusername/github-activity-cli.git
   cd github-activity-cli
   ```

2. **Make it executable (optional):**
   ```bash
   chmod +x github_activity.py
   ```

3. **Run it:**
   ```bash
   python github_activity.py <username>
   ```

That's it! No pip install, no virtual environment needed.

## 🚀 Usage

### Basic Syntax

```bash
python github_activity.py <username> [options]
```

### Quick Example

```bash
python github_activity.py kamranahmedse
```

**Output:**
```
Fetching activity for GitHub user: kamranahmedse...

Recent Activity (30 events)
------------------------------------------------------------
- Pushed 3 commit(s) to kamranahmedse/developer-roadmap
- Opened an issue in kamranahmedse/developer-roadmap
- Starred torvalds/linux
- Forked facebook/react
- Created branch in kamranahmedse/roadmap
...
```

## 🎛️ Filter Options

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--type` | `-t` | Filter by event type | `--type push` |
| `--repo` | `-r` | Filter by repository name | `--repo react` |
| `--limit` | `-l` | Limit number of results | `--limit 10` |
| `--date` | `-d` | Show events after date | `--date 2024-01-01` |
| `--today` | | Show only today's events | `--today` |
| `--week` | | Show events from last 7 days | `--week` |

### Supported Event Types

| Type | Description | Usage |
|------|-------------|-------|
| `push` | Code commits | `--type push` |
| `create` | Branch/repo creation | `--type create` |
| `delete` | Branch deletion | `--type delete` |
| `issues` | Issue activity | `--type issues` |
| `issue_comment` | Issue comments | `--type issue_comment` |
| `star` / `watch` | Starred repositories | `--type star` |
| `fork` | Forked repositories | `--type fork` |
| `pr` / `pull_request` | Pull requests | `--type pr` |
| `pr_review` | PR reviews | `--type pr_review` |
| `pr_comment` | PR comments | `--type pr_comment` |
| `release` | New releases | `--type release` |
| `member` | Collaborator additions | `--type member` |

## 💡 Examples

### Basic Usage

```bash
# View all activity for a user
python github_activity.py torvalds

# View activity with limited results
python github_activity.py gaearon --limit 10
```

### Filter by Event Type

```bash
# Show only push events (commits)
python github_activity.py kamranahmedse --type push

# Show only starred repositories
python github_activity.py kentcdodds --type star

# Show only pull request activity
python github_activity.py facebook --type pr
```

### Filter by Repository

```bash
# Show activity in a specific repository
python github_activity.py facebook --repo react

# Show push events in a specific repo
python github_activity.py microsoft --repo vscode --type push
```

### Filter by Date

```bash
# Show events from a specific date
python github_activity.py kamranahmedse --date 2024-01-01

# Show only today's activity
python github_activity.py nodejs --today

# Show activity from the last week
python github_activity.py rust-lang --week
```

### Combine Multiple Filters

```bash
# Push events in a specific repo, limited to 5
python github_activity.py kamranahmedse --type push --repo roadmap --limit 5

# Issues from the last week, limited to 10
python github_activity.py facebook --type issues --week --limit 10

# All activity in a repo from a specific date
python github_activity.py torvalds --repo linux --date 2024-10-01
```

## 🔧 Technical Details

### Architecture

The application is built with a modular architecture:

- **`fetch_user_activity()`**: Handles API requests to GitHub
- **`filter_events()`**: Applies user-specified filters to events
- **`format_event()`**: Converts raw event data to readable strings
- **`parse_arguments()`**: Processes command-line arguments
- **`display_activity()`**: Presents formatted results to the user

### API Endpoint

```
GET https://api.github.com/users/{username}/events
```

The application uses GitHub's public REST API v3, which provides the 30 most recent public events for any user.

### Response Handling

- Events are returned as JSON arrays
- Each event contains: `type`, `repo`, `payload`, `created_at`
- No authentication required for public data
- Rate limit: 60 requests per hour for unauthenticated requests

### Data Flow

```
User Input → Parse Arguments → Fetch from GitHub API → Parse JSON → 
Filter Events → Format Output → Display in Terminal
```

## 🛡️ Error Handling

The application handles various error scenarios:

| Error Type | Handling |
|------------|----------|
| User not found | Displays "User not found" message |
| Network issues | Reports connection error with details |
| Invalid JSON | Catches parsing errors gracefully |
| Missing arguments | Shows usage instructions |
| Invalid filters | Warns and ignores invalid options |

**Example Error Output:**
```bash
$ python github_activity.py nonexistentuser123
Fetching activity for GitHub user: nonexistentuser123...
Error: User 'nonexistentuser123' not found.
```

## 🎓 Learning Outcomes

This project demonstrates proficiency in:

- **API Integration**: Making HTTP requests and handling responses
- **Data Processing**: Parsing and transforming JSON data
- **CLI Development**: Building user-friendly command-line interfaces
- **Error Handling**: Implementing robust exception handling
- **Filtering Logic**: Creating complex data filtering systems
- **Code Organization**: Writing clean, modular, maintainable code
- **Documentation**: Providing clear usage instructions

## 🧪 Testing

### Test with Active Users

```bash
# Linux kernel maintainer
python github_activity.py torvalds

# React core team
python github_activity.py gaearon

# Node.js organization
python github_activity.py nodejs
```

### Test Error Handling

```bash
# Non-existent user
python github_activity.py thisuserdoesnotexist12345
```

# Missing username
python github_activity.py


## 📝 Requirements

- **Python**: 3.6 or higher
- **Libraries**: `urllib`, `json`, `sys`, `datetime` (all built-in)
- **Network**: Internet connection required
- **API**: GitHub REST API v3 (no authentication needed for public data)

## 🌟 Project Background

This project is inspired by the [roadmap.sh GitHub User Activity project](https://roadmap.sh/projects/github-user-activity), designed to help developers practice:
- Working with external APIs
- Processing JSON data
- Building CLI applications
- Implementing filtering logic
- Error handling and validation


## 🙏 Acknowledgments

- GitHub for providing an excellent public API
- The Python community for great documentation
- roadmap.sh for project inspiration

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/github-activity-cli/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/github-activity-cli/discussions)

---

**Made with ❤️ and Python**

[⭐ Star this repo](https://github.com/yourusername/github-activity-cli) | [🐛 Report Bug](https://github.com/yourusername/github-activity-cli/issues) | [✨ Request Feature](https://github.com/yourusername/github-activity-cli/issues)

