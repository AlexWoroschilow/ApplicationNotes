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
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets


class Description(QtWidgets.QTextEdit):

    def __init__(self, text=None):
        super(Description, self).__init__()
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setEnabled(False)
        self.setHtml(text)
        self.show()

    def resizeEvent(self, *args, **kwargs):
        document = self.document()
        if document is None: return None
        size = document.size()
        if size is None: return None

        self.setFixedHeight(size.height())
        return QtWidgets.QTextEdit.resizeEvent(self, *args, **kwargs)