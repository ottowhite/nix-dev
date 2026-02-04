from github import Github
from github import Auth
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv()
    access_token: str | None = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN", None)

    if access_token is None:
        print("Need to set GitHub personal access token in .env")
        exit(-1)
    else:
        auth = Auth.Token(access_token)
        github_client = Github(auth=auth)
        for repo in github_client.get_user().get_repos():
            print(repo.name)
        github_client.close()