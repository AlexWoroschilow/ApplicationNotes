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
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui


class TextWriter(QtWidgets.QScrollArea):

    @inject.params(editor='text_editor')
    def __init__(self, parent=None, editor=None):
        super(TextWriter, self).__init__(parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignHCenter)
        self.setContentsMargins(0, 0, 0, 0)

        self.text = editor
        self.setWidgetResizable(True)
        self.setWidget(self.text)

        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setBlurRadius(10)
        effect.setOffset(0)

        self.setGraphicsEffect(effect)

        self._entity = None

    def document(self):
        if self.text is not None:
            return self.text.document()
        return None

    def setDocument(self, document=None):
        if document is None:
            return None
        if self.text is None:
            return None

        self.text.setDocument(document)
        self.focus()
        return None

    def focus(self):
        if self.text is not None:
            self.text.setFocus()
        return self

    def zoomIn(self, value):
        if self.text is None:
            return None
        self.text.zoomIn(value)

    def zoomOut(self, value):
        if self.text is None:
            return None
        self.text.zoomOut(value)

    def html(self):
        return self.text.toHtml()

    def event(self, QEvent):
        if QEvent.type() == QtCore.QEvent.Enter:
            effect = QtWidgets.QGraphicsDropShadowEffect()
            effect.setColor(QtGui.QColor('#6cccfc'))
            effect.setBlurRadius(20)
            effect.setOffset(0)

            self.setGraphicsEffect(effect)
        if QEvent.type() == QtCore.QEvent.Leave:
            effect = QtWidgets.QGraphicsDropShadowEffect()
            effect.setBlurRadius(10)
            effect.setOffset(0)
            self.setGraphicsEffect(effect)

        if QEvent.type() == QtCore.QEvent.MouseButtonRelease:
            effect = QtWidgets.QGraphicsDropShadowEffect()
            effect.setColor(QtGui.QColor('#6cccfc'))
            effect.setBlurRadius(20)
            effect.setOffset(0)

        return super(TextWriter, self).event(QEvent)
