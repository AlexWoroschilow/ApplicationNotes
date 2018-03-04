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
from .gui.widget import RecordList


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
        dispatcher.add_listener('window.first_tab.content', self._onWindowFirstTab)
        dispatcher.add_listener('window.notepad.note_update', self._onNotepadNoteUpdate)

    @inject.params(storage='storage')
    def _onWindowFirstTab(self, event=None, dispatcher=None, storage=None):
        """

        :param event: 
        :param dispatcher: 
        :return: 
        """

        self.list = RecordList()
        self.list.toolbar.newAction.triggered.connect(self._onNewEvent)
        self.list.toolbar.copyAction.triggered.connect(self._onCopyEvent)
        self.list.toolbar.savePdf.triggered.connect(self._onSavePdfEvent)
        self.list.toolbar.viewIcons.triggered.connect(self._onToggleView)

        self.list.list.selectionChanged = self._onNoteSelected

        for fields in storage.notes:
            index, date, name, text = fields
            self.list.addLine(index, name, text)
        event.data.addWidget(self.list, 3)

    @inject.params(dispatcher='event_dispatcher')
    def _onNoteSelected(self, event=None, selection=None, dispatcher=None):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """
        for index in self.list.list.selectedIndexes():
            item = self.list.list.itemFromIndex(index)
            widget = self.list.list.itemWidget(item)

            dispatcher.dispatch('window.notepad.note_edit', (
                item.index, widget.getTextUp(), widget.getTextDown()
            ))

    @inject.params(storage='storage')
    def _onNotepadNoteUpdate(self, event=None, dispather=None, storage=None):
        """

        :param event: 
        :param dispather: 
        :return: 
        """
        index, name, text = event.data
        for index in self.list.list.selectedIndexes():
            widget = self.list.list.itemWidget(
                self.list.list.itemFromIndex(index)
            )
            widget.setTextUp(name)
            widget.setTextDown(text)

    @inject.params(dispatcher='event_dispatcher')
    def _onNewEvent(self, event=None, dispatcher=None):
        """
        
        :param event: 
        :return: 
        """
        name = 'Note 1'
        description = 'Note description 1'
        self.list.addLine(None, name, description)
        dispatcher.dispatch('window.notepad.note_new', (
            name, description
        ))

    @inject.params(dispatcher='event_dispatcher')
    def _onCopyEvent(self, event=None, dispatcher=None):
        """

        :param event: 
        :return: 
        """
        dispatcher.dispatch('window.notepad.note_copy')

    @inject.params(dispatcher='event_dispatcher')
    def _onSavePdfEvent(self, event=None, dispatcher=None):
        """

        :param event: 
        :return: 
        """
        dispatcher.dispatch('window.notepad.note_export')

    @inject.params(dispatcher='event_dispatcher')
    def _onToggleView(self, event=None, dispatcher=None):
        """

        :param event: 
        :return: 
        """
        print('_onToggleView')
