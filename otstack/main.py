import argparse

from otstack.OtStackClient import OtStackClient


def main() -> None:
    parser = argparse.ArgumentParser(description="OtStack - PR dependency management")
    subparsers = parser.add_subparsers(dest="command", required=True)

    tree_parser = subparsers.add_parser("tree", help="Show PR dependency tree")
    tree_parser.add_argument(
        "--repo",
        type=str,
        required=False,
        help="Repository name (e.g., 'repo-name'). If not provided, detects from git remote.",
    )

    sync_parser = subparsers.add_parser("sync", help="Sync all local PRs")
    sync_parser.add_argument(
        "--repo",
        type=str,
        required=False,
        help="Repository name (e.g., 'repo-name'). If not provided, detects from git remote.",
    )

    args = parser.parse_args()

    try:
        with OtStackClient() as client:
            repo_name = args.repo
            if repo_name is None:
                repo_name = client.detect_repo_name()
                if repo_name is None:
                    print(
                        "Could not detect repository. Please specify --repo or run "
                        "from within a git repository with a GitHub remote."
                    )
                    exit(-1)
                print(f"Detected repository: {repo_name}")
            repo = client.get_repo(repo_name)

            if args.command == "tree":
                print(f"Repository: {repo_name}\n")
                client.tree(repo)
            elif args.command == "sync":
                print(f"Syncing repository: {repo_name}\n")
                if client.sync(repo):
                    print("All PRs synced successfully!")
                else:
                    exit(1)
    except ValueError as e:
        print(e)
        exit(-1)


if __name__ == "__main__":
    main()
