from os import path
from unittest import mock
from harmony.libs.version_file_storage import VersionFileStorage

repo_name = 'test_git_repo'
repo_url = 'git@github.com:srntqn/sample_harmony_version_file_source.git'
repo_branch = 'master'
local_dir = './'

git_repo = VersionFileStorage(repo_name,
                              repo_url,
                              repo_branch,
                              local_dir)


def test_clone_git_repo():
    git_repo.repo.clone_from = mock.MagicMock()
    git_repo.clone_git_repo()
    git_repo.repo.clone_from.assert_called_once_with(repo_url,
                                                     path.join(local_dir, repo_name),
                                                     branch=repo_branch)


def test_pull_git_repo():
    git_repo.repo = mock.MagicMock()
    git_repo.pull_git_repo()
    git_repo.repo.assert_called_once_with(path.join(local_dir, repo_name))
