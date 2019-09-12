import logging
import os

import settings


class Storager:
    def __init__(self):
        self.folder = settings.get('folder', 'files')

    def create_ts_dir_if_not_exists(self, ts):
        dir_path = os.path.join(os.getcwd(), self.folder)
        self.create_dir_if_not_exists(dir_path)

        dir_path = os.path.join(dir_path, str(ts))
        self.create_dir_if_not_exists(dir_path)

        return dir_path

    @staticmethod
    def create_dir_if_not_exists(dir_path):
        if not os.path.exists(dir_path):
            logging.info(f'Creating directory {dir_path}')
            os.mkdir(dir_path)


class PatchStorager(Storager):
    def store(self, files, ts):
        logging.info(f'Storing patches')
        dir_path = self.create_ts_dir_if_not_exists(ts)

        for index, item in enumerate(files):
            try:
                if not item.patches:
                    continue

                file_path = os.path.join(dir_path, f'{index+1}.txt')
                with open(file_path, 'a+') as f:
                    f.write(f'File name: {item.file_name}\n\n')
                    for patch in item.patches:
                        f.write(patch)
                        f.write('\n\n')
            except:
                logging.exception(f'Unable to store file {item.sha}')


class StatStorager(Storager):
    def __init__(self):
        super().__init__()
        self.file_name = settings.get('statfile', 'stat')

    def store(self, authors, files, ts):
        logging.info(f'Storing stats')

        dir_path = self.create_ts_dir_if_not_exists(ts)
        file_path = os.path.join(dir_path, f'{self.file_name}.txt')

        with open(file_path, 'a+') as f:
            if authors:
                authors_arr = sorted(authors, key=lambda a: a.changes_cnt)
                if int(settings.get('authorizedonly', 0)):
                    authors_arr = [author for author in authors_arr if author.is_authorized]

                least_code_changer = authors_arr[0]
                most_code_changer = authors_arr[-1]

                f.write('Github authors: \n')
                for a in sorted(authors_arr, key=lambda a: len(a.commits), reverse=True):
                    f.write(
                        f'{a.name}{"" if a.is_authorized else " (unauthorized)"}:'
                        f' {len(a.commits)} commits\n')

                f.write(f'Most code changer: {most_code_changer.name} {most_code_changer.changes_cnt} lines changed\n')
                f.write(f'Least code changer: {least_code_changer.name} {least_code_changer.changes_cnt} lines changed\n\n')
            else:
                f.write('No info about authors\n\n')

            file_arr = sorted(files, key=lambda f: len(f.patches), reverse=True)
            for file in file_arr:
                f.write(f'{file.file_name} changed {len(file.patches)} times\n')
