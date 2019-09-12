import logging
import sys

import requests

import settings
from models import Commit, Author, File


class GithubManager:
    __UNAUTHORIZED_AUTHOR_ID_PREFIX = '__unauthorized__'

    _author_id_to_author = {}
    _file_sha_name_to_file = {}
    _commits = []

    def __init__(self):
        self.api = GithubAPI()

    @classmethod
    def get_authors(cls):
        return cls._author_id_to_author.values()

    @classmethod
    def get_files(cls):
        return cls._file_sha_name_to_file.values()

    @staticmethod
    def _show_progress(count, total, suffix=''):
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '#' * filled_len + '-' * (bar_len - filled_len)

        sys.stdout.write(f'[{bar}] {percents}%...{suffix}\r')
        sys.stdout.flush()

    def load_commits(self, user_name, repo_name, limit=None, show_progress=True):
        row_simple_commits = self.api.get_commits(user_name, repo_name, limit)
        commits = []

        for index, row_simple_commit in enumerate(row_simple_commits):
            try:
                row_commit = self.api.get_commit(user_name, repo_name, row_simple_commit['sha'])
                logging.info(f'Success request: info for {row_commit["sha"]}')

                if show_progress:
                    self._show_progress(index+1, len(row_simple_commits), suffix='loading')
            except GithubAPIException:
                logging.warning(f'Getting a commit failed for user={user_name} repo={repo_name} '
                                f'sha={row_simple_commit["sha"]}, skipping...')
                continue

            row_author = row_simple_commit['author']
            if not row_author:
                row_author_name = row_simple_commit['commit']['author']['name']
                row_author = {
                    'id': f'{self.__UNAUTHORIZED_AUTHOR_ID_PREFIX}{row_author_name}',
                    'login': row_author_name
                }
                is_authorized_author = False
            else:
                is_authorized_author = True

            row_files = row_commit['files']

            author = None
            if row_author:
                author = self._author_id_to_author.get(row_author['id'])
                if not author:
                    author = Author(row_author['id'], row_author['login'], is_authorized_author)
                    self._author_id_to_author[author.id] = author

            files = []
            curr_changes_cnt = 0

            if row_files:
                for row_file in row_files:
                    if not row_file.get('patch'):
                        continue  # we are interested only in changed files, not fully added

                    file_sha_name = f'{row_file["sha"]}.{row_file["filename"]}'

                    file = self._file_sha_name_to_file.get(file_sha_name)
                    if not file:
                        file = File(row_file['sha'], row_file['filename'], row_file['changes'])
                        self._file_sha_name_to_file[file_sha_name] = file

                    file.patches.append(row_file['patch'])
                    files.append(file)

                    curr_changes_cnt += file.changes_cnt

            sha = row_commit['sha']
            commit = Commit(sha, author, files)
            commits.append(commit)

            if author:
                author.changes_cnt += curr_changes_cnt
                author.commits.append(commit)

        sys.stdout.write('\nAll available commits are loaded\n')

        self._commits += commits
        return commits


class GithubAPI:
    ROOT_URL = 'https://api.github.com'

    def get_commit(self, user_name, repo_name, commit_sha):
        result = self._make_request(f'/repos/{user_name}/{repo_name}/commits/{commit_sha}')
        return result

    def get_commits(self, user_name, repo_name, limit=None, page=1):
        result = self._make_request(f'/repos/{user_name}/{repo_name}/commits?page={page}')
        commits = result[:limit]
        commits = list(filter(lambda c: len(c.get('parents', [])) <= 1, commits))

        if len(commits) < limit and result:
            commits += self.get_commits(user_name, repo_name, limit-len(commits), page=page+1)

        return commits

    def _make_request(self, path, method='get'):
        token = settings.get('token')
        headers = {'Authorization': f'token {token}'} if token else None

        url = f'{self.ROOT_URL}{path}'
        response = requests.request(method, url, headers=headers)
        if response.status_code != 200:
            logging.warning(f'Unable to request data from {url}, response={response.text}')
            raise GithubAPIException

        response_data = response.json()
        return response_data


class GithubAPIException(Exception):
    pass
