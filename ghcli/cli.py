"""Command line interface to manage GitHub issues."""
import argparse
import os

from .api import API


def create_parser() -> argparse.ArgumentParser:
    """Create an argparse parser with list and create subcommands."""
    parser = argparse.ArgumentParser(description="Create GitHub issues automatically.")
    subparsers = parser.add_subparsers(help="Commands", dest="command")

    # List command
    parser_list = subparsers.add_parser("list")
    parser_list.add_argument("owner", help="owner of the GitHub repository")
    parser_list.add_argument("repo", help="GitHub repository")
    parser_list.add_argument(
        "--token", default=os.environ.get("GITHUB_TOKEN"), help="GitHub API token"
    )

    # Create command
    parser_create = subparsers.add_parser("create")
    parser_create.add_argument("owner", help="owner of the GitHub repository")
    parser_create.add_argument("repo", help="GitHub repository")
    parser_create.add_argument("title", help="title of the GitHub issue")
    parser_create.add_argument("body", help="body of the GitHub issue")
    parser_create.add_argument(
        "--token", default=os.environ.get("GITHUB_TOKEN"), help="GitHub API token"
    )
    return parser


def main() -> None:
    """Entry point of the tool."""
    parser = create_parser()
    args = parser.parse_args()
    command = args.command
    delattr(args, "command")
    token = args.token
    delattr(args, "token")
    if token is None:
        parser.error(
            "Please set the GITHUB_TOKEN environment variable before calling ghcli or "
            "use the --token option"
        )
    api = API(token)
    if command == "list":
        issues = api.list_issues(**vars(args))
        print(f"Retrieved {len(issues)} issues")
        for issue in issues:
            print(f"{issue.title}: {issue.html_url}")
    elif command == "create":
        print(issue.html_url)
