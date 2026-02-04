import argparse

from otstack.OtStackClient import OtStackClient


def main() -> None:
    parser = argparse.ArgumentParser(description="OtStack - PR dependency management")
    subparsers = parser.add_subparsers(dest="command", required=True)

    tree_parser = subparsers.add_parser("tree", help="Show PR dependency tree")
    tree_parser.add_argument(
        "--repo",
        type=str,
        required=True,
        help="Repository name (e.g., 'repo-name')",
    )

    args = parser.parse_args()

    try:
        with OtStackClient() as client:
            if args.command == "tree":
                repo = client.get_repo(args.repo)
                client.tree(repo)
    except ValueError as e:
        print(e)
        exit(-1)


if __name__ == "__main__":
    main()
