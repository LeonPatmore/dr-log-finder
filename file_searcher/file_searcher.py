import json
import os
import glob
from json import JSONDecodeError

from logger.logger import logger


class _JsonCache(object):

    def __init__(self, jsons: list):
        self.jsons = jsons


class FileSearcher(object):

    def __init__(self, cache_offset: bool=False, cache_jsons: bool=False):
        if self.cache_offset is False and cache_jsons is True:
            logger.warning("Caching JSONs without caching offsets will lead to massive cache duplications!")
        self.cache_offset = cache_offset
        self.cache_jsons = cache_jsons
        self.json_cache = dict()
        self.offset_cache = dict()

    @staticmethod
    def get_files_by_regex(path_regex: str) -> list:
        return glob.glob(path_regex, recursive=True)

    def file_to_jsons(self, file_path: str) -> list:
        jsons = list()
        if self.cache_jsons:
            jsons = self._get_cached_jsons(file_path)
        lines = self._get_new_file_lines(file_path)
        jsons.extend(self._read_as_jsons(lines))
        if self.cache_jsons:
            self.json_cache.update({file_path: _JsonCache(jsons)})
        return jsons

    def _get_new_file_lines(self, file_path: str) -> list:
        offset = 0
        if self.cache_offset:
            offset = self._get_cached_offset(file_path)
        new_offset, reversed_lines = self._reverse_read_lines(file_path, until_offset=offset)
        lines = self.reverse_list(reversed_lines)
        if self.cache_offset:
            self.offset_cache.update({file_path: new_offset})
        return lines

    @staticmethod
    def reverse_list(a: list) -> list:
        return list(reversed(a))

    @staticmethod
    def _reverse_read_lines(filepath: str, buf_size: int=8192, until_offset: int=0) -> tuple:
        logger.info("Searching [ {} ] until offset [ {} ]".format(filepath, until_offset))
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
                logger.info("Current offset is now [ {} ] out of [ {} ]".format(current_offset, file_size))

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

    def _get_cached_offset(self, file_name: str) -> int:
        if file_name in self.offset_cache:
            return self.offset_cache.get(file_name)
        return 0

    def _get_cached_jsons(self, file_name: str) -> list:
        if file_name in self.json_cache:
            return self.json_cache.get(file_name).jsons
        return list()
