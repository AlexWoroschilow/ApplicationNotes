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

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from .preview import NotePreviewDescription


class NoteItem(QtWidgets.QListWidgetItem):

    def __init__(self, book=None):
        super(NoteItem, self).__init__()
        self.setSizeHint(QtCore.QSize(400, 500))
        self.setTextAlignment(Qt.AlignCenter)


class PreviewScrollArea(QtWidgets.QListWidget):
    editAction = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(PreviewScrollArea, self).__init__(parent)
        self.setViewMode(QtWidgets.QListView.IconMode)
        self.setResizeMode(QtWidgets.QListView.Adjust)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMovement(QtWidgets.QListView.Static)

        self.setMinimumWidth(400)

        self.itemClicked.connect(self.itemClickedEvent)

        self.hashmap_index = {}

    @inject.params(storage='storage')
    def addPreview(self, index=None, storage=None):
        if index is None: return self

        item = NoteItem()
        self.addItem(item)

        widget = NotePreviewDescription(index)
        widget.editAction.connect(self.editAction.emit)

        self.setItemWidget(item, widget)

        path = storage.filePath(index)
        if path is None: return self

        self.hashmap_index[path] = (item, widget)
        return self

    def itemClickedEvent(self, item):
        widget = self.itemWidget(item)
        if widget is None: return None
        return self.editAction.emit(widget.index)

    @inject.params(storage='storage')
    def document(self, index=None, storage=None):
        if index is None: return None

        path = storage.filePath(index)
        if path is None: return None

        if path not in self.hashmap_index.keys():
            return None

        item, widget = self.hashmap_index[path]
        if widget is None: return None
        if item is None: return None

        return widget.document()

    @inject.params(storage='storage')
    def getWidgetItemByIndex(self, index=None, storage=None):
        path = storage.filePath(index)
        if path is None: return None

        if path not in self.hashmap_index.keys():
            return None

        item, widget = self.hashmap_index[path]
        if widget is None: return None
        if item is None: return None

        return item

    @inject.params(storage='storage')
    def getWidgetByIndex(self, index=None, storage=None):
        path = storage.filePath(index)
        if path is None: return None

        if path not in self.hashmap_index.keys():
            return None

        item, widget = self.hashmap_index[path]
        if widget is None: return None
        if item is None: return None

        return widget

    def count(self):
        return len(self.hashmap_index.keys())