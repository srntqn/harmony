from git import Repo
from os import path


class GitRepo:
    def __init__(self, repo_name: str, repo_url: str, repo_branch: str, local_dir: str) -> None:
        self.repo_name = repo_name
        self.repo_url = repo_url
        self.repo_branch = repo_branch
        self.local_dir = local_dir
        self.repo = Repo

    def clone_git_repo(self) -> Repo:
        return self.repo.clone_from(self.repo_url, path.join(self.local_dir, self.repo_name), branch=self.repo_branch)

    def pull_git_repo(self):
        return self.repo(path.join(self.local_dir, self.repo_name)).remotes.origin.pull()
