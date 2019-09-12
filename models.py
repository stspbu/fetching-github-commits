class Commit:
    def __init__(self, sha, author=None, files=None):
        self.sha = sha
        self.author = author
        self.files = files


class Author:
    def __init__(self, id, name, is_authorized, commits=None):
        self.id = id
        self.name = name
        self.changes_cnt = 0
        self.commits = commits or []
        self.is_authorized = is_authorized


class File:
    def __init__(self, sha, file_name, changes_cnt, patches=None):
        self.sha = sha
        self.file_name = file_name
        self.changes_cnt = changes_cnt
        self.patches = patches or []
