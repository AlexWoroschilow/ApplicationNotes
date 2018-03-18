# -*- coding: utf-8 -*-
# Copyright 2015 Alex Woroschilow (alex.woroschilow@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import inject
from PyQt5 import QtCore

from lib.plugin import Loader
from PyQt5 import QtWidgets
from .gui.widget import SearchField


class Loader(Loader):
    @property
    def enabled(self):
        """

        :return:
        """
        return True

    def config(self, binder=None):
        """

        :param binder:
        :return:
        """

    @inject.params(dispatcher='event_dispatcher')
    def boot(self, dispatcher=None):
        """

        :param dispatcher:.
        :return:.
        """
        dispatcher.add_listener('window.header.content', self._onWindowHeader)

    @inject.params(storage='storage')
    def _onNotepadFolderNew(self, event=None, dispather=None, storage=None):
        """

        :param event: 
        :param dispather: 
        :return: 
        """
        name, description = event.data
        storage.addFolder(name, description)

    @inject.params(storage='storage')
    def _onWindowHeader(self, event=None, dispather=None, storage=None):
        """

        :param event: 
        :param dispather: 
        :return: 

        """
        event.data.addWidget(SearchField(), -1)