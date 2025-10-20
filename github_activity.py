#!/usr/bin/env python3
"""
GitHub User Activity CLI with Filtering
Fetches and displays recent activity for a GitHub user with filter options

Usage: 
  python github_activity.py <username>
  python github_activity.py <username> --type push
  python github_activity.py <username> --type issues --limit 5
  python github_activity.py <username> --repo developer-roadmap
  python github_activity.py <username> --date 2024-01-01
"""

import sys
import urllib.request
import json
from datetime import datetime, timedelta


# Map of friendly filter names to GitHub event types
EVENT_TYPE_MAP = {
    'push': 'PushEvent',
    'create': 'CreateEvent',
    'delete': 'DeleteEvent',
    'issues': 'IssuesEvent',
    'issue_comment': 'IssueCommentEvent',
    'star': 'WatchEvent',
    'watch': 'WatchEvent',
    'fork': 'ForkEvent',
    'pr': 'PullRequestEvent',
    'pull_request': 'PullRequestEvent',
    'pr_review': 'PullRequestReviewEvent',
    'pr_comment': 'PullRequestReviewCommentEvent',
    'release': 'ReleaseEvent',
    'member': 'MemberEvent'
}


def fetch_user_activity(username):
    """
    Fetch recent activity for a GitHub user
    
    Args:
        username: GitHub username to fetch activity for
        
    Returns:
        List of activity events (as dictionaries)
    """
    url = f"https://api.github.com/users/{username}/events"
    
    try:
        request = urllib.request.Request(
            url,
            headers={'User-Agent': 'GitHub-Activity-CLI'}
        )
        
        with urllib.request.urlopen(request) as response:
            data = response.read()
            events = json.loads(data)
            return events
            
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: User '{username}' not found.")
        else:
            print(f"Error: HTTP {e.code} - {e.reason}")
        sys.exit(1)
        
    except urllib.error.URLError as e:
        print(f"Error: Could not connect to GitHub. Check your internet connection.")
        print(f"Details: {e.reason}")
        sys.exit(1)
        
    except json.JSONDecodeError:
        print("Error: Received invalid data from GitHub.")
        sys.exit(1)


def filter_events(events, filters):
    """
    Filter events based on specified criteria
    
    Args:
        events: List of event dictionaries
        filters: Dictionary containing filter criteria
                 - event_type: Type of event to filter (e.g., 'PushEvent')
                 - repo: Repository name to filter
                 - date_from: Only show events after this date
                 - limit: Maximum number of events to return
        
    Returns:
        Filtered list of events
    """
    filtered = events
    
    # Filter by event type
    if filters.get('event_type'):
        event_type = filters['event_type']
        filtered = [e for e in filtered if e.get('type') == event_type]
    
    # Filter by repository name
    if filters.get('repo'):
        repo_filter = filters['repo'].lower()
        filtered = [
            e for e in filtered 
            if repo_filter in e.get('repo', {}).get('name', '').lower()
        ]
    
    # Filter by date
    if filters.get('date_from'):
        date_from = filters['date_from']
        filtered = [
            e for e in filtered
            if parse_event_date(e) >= date_from
        ]
    
    # Limit number of results
    if filters.get('limit'):
        filtered = filtered[:filters['limit']]
    
    return filtered


def parse_event_date(event):
    """
    Parse the event date string into a datetime object
    
    Args:
        event: Event dictionary
        
    Returns:
        datetime object
    """
    date_str = event.get('created_at', '')
    try:
        # GitHub uses ISO 8601 format: 2024-01-15T10:30:00Z
        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        return datetime.min


def format_event(event, show_date=False):
    """
    Format a single event into a readable string
    
    Args:
        event: Dictionary containing event data
        show_date: Whether to include the date in the output
        
    Returns:
        Formatted string describing the event
    """
    event_type = event.get('type')
    repo_name = event.get('repo', {}).get('name', 'unknown repo')
    
    # Format the main event description
    if event_type == 'PushEvent':
        commits = event.get('payload', {}).get('commits', [])
        commit_count = len(commits)
        description = f"Pushed {commit_count} commit(s) to {repo_name}"
    
    elif event_type == 'CreateEvent':
        ref_type = event.get('payload', {}).get('ref_type', 'repository')
        description = f"Created {ref_type} in {repo_name}"
    
    elif event_type == 'DeleteEvent':
        ref_type = event.get('payload', {}).get('ref_type', 'branch')
        description = f"Deleted {ref_type} in {repo_name}"
    
    elif event_type == 'IssuesEvent':
        action = event.get('payload', {}).get('action', 'updated')
        description = f"{action.capitalize()} an issue in {repo_name}"
    
    elif event_type == 'IssueCommentEvent':
        description = f"Commented on an issue in {repo_name}"
    
    elif event_type == 'WatchEvent':
        description = f"Starred {repo_name}"
    
    elif event_type == 'ForkEvent':
        description = f"Forked {repo_name}"
    
    elif event_type == 'PullRequestEvent':
        action = event.get('payload', {}).get('action', 'updated')
        description = f"{action.capitalize()} a pull request in {repo_name}"
    
    elif event_type == 'PullRequestReviewEvent':
        description = f"Reviewed a pull request in {repo_name}"
    
    elif event_type == 'PullRequestReviewCommentEvent':
        description = f"Commented on a pull request in {repo_name}"
    
    elif event_type == 'ReleaseEvent':
        action = event.get('payload', {}).get('action', 'published')
        description = f"{action.capitalize()} a release in {repo_name}"
    
    elif event_type == 'MemberEvent':
        description = f"Added a collaborator to {repo_name}"
    
    else:
        description = f"{event_type.replace('Event', '')} in {repo_name}"
    
    # Add date if requested
    if show_date:
        event_date = parse_event_date(event)
        time_ago = get_time_ago(event_date)
        description += f" ({time_ago})"
    
    return description


def get_time_ago(date):
    """
    Convert a datetime to a human-readable "time ago" string
    
    Args:
        date: datetime object
        
    Returns:
        String like "2 hours ago" or "3 days ago"
    """
    now = datetime.utcnow()
    diff = now - date
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif seconds < 2592000:  # 30 days
        days = int(seconds / 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"
    else:
        months = int(seconds / 2592000)
        return f"{months} month{'s' if months != 1 else ''} ago"


def display_activity(events, filters):
    """
    Display formatted activity events
    
    Args:
        events: List of event dictionaries
        filters: Dictionary of applied filters (for display)
    """
    if not events:
        print("No activity found matching the filters.")
        return
    
    # Show what filters are applied
    filter_desc = []
    if filters.get('event_type'):
        friendly_name = get_friendly_event_name(filters['event_type'])
        filter_desc.append(f"Type: {friendly_name}")
    if filters.get('repo'):
        filter_desc.append(f"Repo: {filters['repo']}")
    if filters.get('date_from'):
        filter_desc.append(f"Since: {filters['date_from'].strftime('%Y-%m-%d')}")
    
    print(f"\nRecent Activity ({len(events)} events)")
    if filter_desc:
        print(f"Filters: {', '.join(filter_desc)}")
    print("-" * 60)
    
    # Show dates if filtering by date
    show_dates = filters.get('date_from') is not None
    
    for event in events:
        formatted = format_event(event, show_date=show_dates)
        print(f"- {formatted}")


def get_friendly_event_name(event_type):
    """
    Convert GitHub event type to friendly name
    
    Args:
        event_type: GitHub event type (e.g., 'PushEvent')
        
    Returns:
        Friendly name (e.g., 'Push')
    """
    for friendly, github_type in EVENT_TYPE_MAP.items():
        if github_type == event_type:
            return friendly.replace('_', ' ').title()
    return event_type.replace('Event', '')


def parse_arguments():
    """
    Parse command-line arguments
    
    Returns:
        Tuple of (username, filters_dict)
    """
    args = sys.argv[1:]
    
    if len(args) == 0:
        return None, {}
    
    username = args[0]
    filters = {}
    
    i = 1
    while i < len(args):
        arg = args[i]
        
        # --type filter
        if arg in ['--type', '-t']:
            if i + 1 < len(args):
                event_filter = args[i + 1].lower()
                if event_filter in EVENT_TYPE_MAP:
                    filters['event_type'] = EVENT_TYPE_MAP[event_filter]
                else:
                    print(f"Warning: Unknown event type '{event_filter}'. Ignoring.")
                i += 2
            else:
                print("Error: --type requires a value")
                sys.exit(1)
        
        # --repo filter
        elif arg in ['--repo', '-r']:
            if i + 1 < len(args):
                filters['repo'] = args[i + 1]
                i += 2
            else:
                print("Error: --repo requires a value")
                sys.exit(1)
        
        # --limit filter
        elif arg in ['--limit', '-l']:
            if i + 1 < len(args):
                try:
                    filters['limit'] = int(args[i + 1])
                except ValueError:
                    print(f"Error: --limit must be a number")
                    sys.exit(1)
                i += 2
            else:
                print("Error: --limit requires a value")
                sys.exit(1)
        
        # --date filter
        elif arg in ['--date', '-d']:
            if i + 1 < len(args):
                try:
                    date_str = args[i + 1]
                    filters['date_from'] = datetime.strptime(date_str, '%Y-%m-%d')
                except ValueError:
                    print(f"Error: --date must be in format YYYY-MM-DD")
                    sys.exit(1)
                i += 2
            else:
                print("Error: --date requires a value")
                sys.exit(1)
        
        # --today shortcut
        elif arg == '--today':
            today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            filters['date_from'] = today
            i += 1
        
        # --week shortcut
        elif arg == '--week':
            week_ago = datetime.utcnow() - timedelta(days=7)
            filters['date_from'] = week_ago
            i += 1
        
        else:
            print(f"Warning: Unknown argument '{arg}'. Ignoring.")
            i += 1
    
    return username, filters


def print_usage():
    """Print usage information"""
    print("GitHub User Activity CLI - Filter by event type, repo, or date")
    print("\nUsage:")
    print("  python github_activity.py <username> [options]")
    print("\nOptions:")
    print("  --type, -t <type>    Filter by event type")
    print("  --repo, -r <repo>    Filter by repository name")
    print("  --limit, -l <num>    Limit number of results")
    print("  --date, -d <date>    Show events after date (YYYY-MM-DD)")
    print("  --today              Show only today's events")
    print("  --week               Show events from last 7 days")
    print("\nEvent Types:")
    print("  push, create, delete, issues, issue_comment, star,")
    print("  fork, pr (pull_request), pr_review, pr_comment,")
    print("  release, member")
    print("\nExamples:")
    print("  python github_activity.py kamranahmedse")
    print("  python github_activity.py kamranahmedse --type push")
    print("  python github_activity.py kamranahmedse --type issues --limit 5")
    print("  python github_activity.py kamranahmedse --repo developer-roadmap")
    print("  python github_activity.py kamranahmedse --date 2024-01-01")
    print("  python github_activity.py kamranahmedse --week --type push")


def main():
    """Main function - entry point of the program"""
    username, filters = parse_arguments()
    
    if username is None:
        print_usage()
        sys.exit(1)
    
    print(f"Fetching activity for GitHub user: {username}...")
    
    # Fetch all activity
    events = fetch_user_activity(username)
    
    # Apply filters
    filtered_events = filter_events(events, filters)
    
    # Display the results
    display_activity(filtered_events, filters)


if __name__ == "__main__":
    main()