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

    args = parser.parse_args()

    try:
        with OtStackClient() as client:
            if args.command == "tree":
                repo_name = args.repo
                if repo_name is None:
                    repo_name = client.detect_repo_name()
                    if repo_name is None:
                        print(
                            "Could not detect repository. Please specify --repo or run "
                            "from within a git repository with a GitHub remote."
                        )
                        exit(-1)
                repo = client.get_repo(repo_name)
                client.tree(repo)
    except ValueError as e:
        print(e)
        exit(-1)


if __name__ == "__main__":
    main()
