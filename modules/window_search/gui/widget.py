#!/usr/bin/python3

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

from PyQt5 import QtWidgets


class SearchField(QtWidgets.QLineEdit):

    def __init__(self, parent=None):
        super(SearchField, self).__init__(parent)
        self.setPlaceholderText('Enter the search string...')
        self.setObjectName('searchSearchField')

        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setBlurRadius(3)
        effect.setOffset(0)

        self.setGraphicsEffect(effect)


class ActionButton(QtWidgets.QAction):

    def __init__(self, icon, name):
        super(ActionButton, self).__init__(icon, name)
