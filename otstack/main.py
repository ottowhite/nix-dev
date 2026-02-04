from otstack.OtStackClient import OtStackClient


if __name__ == "__main__":
    try:
        with OtStackClient() as client:
            for repo in client.github.get_user_repos():
                print(repo.name)
    except ValueError as e:
        print(e)
        exit(-1)
