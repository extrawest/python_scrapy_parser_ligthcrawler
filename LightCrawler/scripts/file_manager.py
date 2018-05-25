# -*- coding: utf-8 -*-
import os
from LightCrawler.settings import BASE_DIR


class FileManager(object):
    """
    Manages directories
    """
    _media_file_dir = os.path.join(BASE_DIR, 'media')

    def __init__(self, name=''):
        self.name = name

    def _file_name(self, ext='csv'):
        """
        create csv file name
        """
        return '{file_name}.{ext}'.format(file_name=self.name, ext=ext)

    def file(self, ext='csv'):
        """
        The method checks the existence of the directory, in case of absence
        it creates and returns the full file name
        """
        if not os.path.exists(self._media_file_dir):
            os.makedirs(self._media_file_dir)
        return os.path.join(self._media_file_dir, self._file_name(ext=ext))
