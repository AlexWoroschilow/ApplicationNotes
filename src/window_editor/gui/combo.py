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

from PyQt5 import QtWidgets


class FolderBomboBox(QtWidgets.QComboBox):

    @inject.params(storage='storage', kernel='kernel')
    def __init__(self, storage=None, kernel=None):
        super(FolderBomboBox, self).__init__()
        self.setObjectName('folderBomboBox')
        self._note = None
        
        if kernel is None or storage is None:
            return None 

        for folder in storage.folders():
            self.addItem(folder.name, folder)

        kernel.listen('folder_update', self._OnFolderUpdate, 128)
        kernel.listen('window.notepad.folder_selected', self._OnFolderSelected, 128)
        kernel.listen('folder_remove', self._OnFolderRemove, 128)
        kernel.listen('folder_new', self._OnFolderNew, 128)

    @property
    def entity(self):
        if self.count() == 0:
            return None
        index = self.currentIndex()
        return self.itemData(index)

    @entity.setter
    def entity(self, entity=None):
        if entity is None:
            return None
        self.blockSignals(True)
        for index in range(0, self.count()):
            folder = self.itemData(index)
            if folder is not None and entity == folder:
                self.setCurrentIndex(index)
        self.blockSignals(False)

    def _OnFolderNew(self, event=None):
        entity, widget = event.data
        if entity is None or widget is None:
            return None
        self.addItem(entity.name, entity)

    def _OnFolderUpdate(self, event=None):
        entity, widget = event.data
        if entity is None or widget is None:
            return None
        for index in range(0, self.count()):
            folder = self.itemData(index)
            if folder is None:
                continue
            if folder != entity:
                continue
            self.setItemText(index, folder.name)

    def _OnFolderRemove(self, event=None):
        entity, widget = event.data
        if entity is None or widget is None:
            return None
        for index in range(0, self.count()):
            folder = self.itemData(index)
            if folder == entity:
                self.removeItem(index)

    def _OnFolderSelected(self, event):
        selected, string, note = event.data
        if selected is None :
            return None
        for index in range(0, self.count()):
            folder = self.itemData(index)
            if folder == selected:
                self.setCurrentIndex(index)