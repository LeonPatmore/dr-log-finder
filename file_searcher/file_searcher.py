import json
import os
from json import JSONDecodeError
import glob

from logger.logger import logger


class FileSearcher(object):

    def __init__(self):
        self.json_cache = dict()

    @staticmethod
    def get_files_by_regex(path_regex: str) -> list:
        return glob.glob(path_regex, recursive=True)

    def file_to_jsons(self, file_path: str) -> list:
        file_name = self._file_name_from_path(file_path)
        offset, jsons = self._get_cached_jsons(file_name)
        new_offset, reversed_lines = self._reverse_read_line(file_path, until_offset=offset)
        lines = self.reverse_list(reversed_lines)
        jsons.extend(self._read_as_jsons(lines))
        self.json_cache.update({file_name: _JsonCache(new_offset, jsons)})
        return jsons

    @staticmethod
    def reverse_list(a: list) -> list:
        return list(reversed(a))

    @staticmethod
    def _reverse_read_line(filepath: str, buf_size: int=8192, until_offset: int=0) -> tuple:
        final_lines = list()

        with open(filepath) as fh:
            fh.seek(0, os.SEEK_END)
            file_size = fh.tell()
            current_offset = file_size
            left_over = None

            while current_offset > until_offset:
                new_offset = max(current_offset - buf_size, until_offset)
                offset_change = current_offset - new_offset
                fh.seek(new_offset)
                buffer = fh.read(offset_change)
                logger.info("Buffering: " + buffer)

                lines = buffer.splitlines()

                if left_over is not None:
                    lines[-1] += left_over

                left_over = lines[0]

                for i in range(len(lines) - 1, 0, -1):
                    if lines[i]:
                        final_lines.append(lines[i])

                current_offset = new_offset

            if left_over is not None:
                final_lines.append(left_over)
        logger.info("Lines: " + ",".join(final_lines))
        return file_size, final_lines

    @staticmethod
    def _read_as_jsons(lines: list) -> list:
        jsons = list()
        for line in lines:
            try:
                jsons.append(json.loads(line))
            except JSONDecodeError:
                print("Could not decode line [ {} ] as a JSON!".format(line))
        return jsons

    def _get_cached_jsons(self, file_name: str) -> tuple:
        if file_name in self.json_cache:
            cache = self.json_cache.get(file_name)
            return cache.offset, cache.jsons
        return 0, list()

    @staticmethod
    def _file_name_from_path(file_path: str) -> str:
        return os.path.basename(file_path)


class _JsonCache(object):

    def __init__(self, offset: int, jsons: list):
        self.offset = offset
        self.jsons = jsons
