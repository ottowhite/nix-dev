import argparse

from otstack.OtStackClient import OtStackClient


def main() -> None:
    parser = argparse.ArgumentParser(description="OtStack - PR dependency management")
    parser.add_argument(
        "--repo",
        type=str,
        help="Repository name (e.g., 'owner/repo') to show PR tree for",
    )
    args = parser.parse_args()

    try:
        with OtStackClient() as client:
            if args.repo:
                repo = client.get_repo(args.repo)
                client.tree(repo)
            else:
                for repo in client.github.get_user_repos():
                    print(repo.name)
    except ValueError as e:
        print(e)
        exit(-1)


if __name__ == "__main__":
    main()
