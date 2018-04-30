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
import datetime
from PyQt5 import QtWidgets

from PyQt5.QtCore import Qt

from .bar import ToolBarWidget
from .text import NameEditor


class LabelTop(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super(LabelTop, self).__init__(parent)
        self.setObjectName('notesLabelTop')


class LabelBottom(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super(LabelBottom, self).__init__(parent)
        self.setObjectName('notesLabelBottom')


class QCustomQWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(QCustomQWidget, self).__init__(parent)
        self.textQVBoxLayout = QtWidgets.QVBoxLayout()
        self.textQVBoxLayout.setContentsMargins(10, 10, 0, 10)

        self.textUpQLabel = LabelTop()
        self.textQVBoxLayout.addWidget(self.textUpQLabel)

        self.textDownQLabel = LabelBottom()
        self.textQVBoxLayout.addWidget(self.textDownQLabel)

        self.setLayout(self.textQVBoxLayout)

    def setTextUp(self, text=None):
        self.textUpQLabel.setText(text)

    def getTextUp(self):
        return self.textUpQLabel.text()

    def setTextDown(self, text=None):
        self.textDownQLabel.setText(text)

    def getTextDown(self):
        return self.textDownQLabel.text()

    def resizeEvent(self, event):
        width = event.size().width()
        self.textDownQLabel.setFixedWidth(width - 20)
        super(QCustomQWidget, self).resizeEvent(event)


class NoteItem(QtWidgets.QListWidgetItem):

    def __init__(self, entity=None, widget=None):
        super(NoteItem, self).__init__()
        
        widget.setTextUp(entity.name)
        
        date = datetime.datetime.now()
        widget.setTextDown(date.strftime("%d.%m.%Y %H:%M"))
        
        self._entity = entity
        self._widget = widget

    @property
    def widget(self):
        return self._widget

    @property
    def entity(self):
        return self._entity

    @entity.setter
    def entity(self, entity=None):
        self._widget.setTextUp(entity.name)
        
        date = datetime.datetime.now()
        self._widget.setTextDown(date.strftime("%d.%m.%Y %H:%M"))
        self._entity = entity

    def resizeEvent(self, event):
        self._widget.resizeEvent(event)


class ItemList(QtWidgets.QListWidget):

    def __init__(self, parent=None):
        """
        
        :param parent: 
        """
        super(ItemList, self).__init__(parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.setContentsMargins(0, 0, 0, 0)
        self.setMinimumWidth(200)
        self.setWordWrap(True)

    def addLine(self, entity=None):
        """
        
        :param name: 
        :param descrption: 
        :return: 
        """

        item = NoteItem(entity, QCustomQWidget())
        item.setSizeHint(item.widget.sizeHint())

        self.addItem(item)
        self.setItemWidget(item, item.widget)

    def resizeEvent(self, event):
        for i in range(0, self.count()):
            item = self.item(i)
            if item is None:
                continue
            item.resizeEvent(event)
        super(ItemList, self).resizeEvent(event)


class RecordList(QtWidgets.QSplitter):

    @inject.params(dispatcher='event_dispatcher', storage='storage')
    def __init__(self, parent=None, dispatcher=None, storage=None):
        super(RecordList, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)

        self._folder = None

        self.toolbar = ToolBarWidget(self)
        self.addWidget(self.toolbar)

        layout = QtWidgets.QGridLayout()
        layout.setContentsMargins(0, 10, 0, 0)
        
        self.folderEditor = NameEditor()
        layout.addWidget(self.folderEditor, 0, 1, 1, 1)
        
        self.list = ItemList()
        layout.addWidget(self.list, 1, 1)

        content = QtWidgets.QWidget()
        content.setContentsMargins(0, 0, 0, 0)
        content.setLayout(layout)
        
        self.addWidget(content)

        self.setCollapsible(0, True)
        self.setCollapsible(1, False)

    @property
    def entity(self):
        for index in self.list.selectedIndexes():
            item = self.list.itemFromIndex(index)
            if item is not None and item.entity is not None:
                return item.entity
        return None

    @property
    def folder(self):
        return self._folder

    def setFolder(self, folder=None):
        if folder is None:
            self.folderEditor.setVisible(False)
            return None

        self._folder = folder
        self.folderEditor.setText(folder.name)
        self.folderEditor.setVisible(True)

    def addLine(self, entity=None):
        self.list.addLine(entity)

    def selectedIndexes(self):
        return self.list.selectedIndexes()

    def itemFromIndex(self, index=None):
        if index is None:
            return None

        return self.list.itemFromIndex(index)

    def takeItem(self, index=None):
        if index is None:
            return None

        self.list.takeItem(index.row())
