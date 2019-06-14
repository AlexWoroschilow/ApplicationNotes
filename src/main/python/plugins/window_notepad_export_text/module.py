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

from lib.plugin import Loader
from lib.widget.button import ToolBarButton

from .actions import ModuleActions


class Loader(Loader):
    actions = ModuleActions()

    def enabled(self, options=None, args=None):
        return options.console is None

    @inject.params(factory='toolbar_factory.leftbar')
    def boot(self, options=None, args=None, factory=None):
        factory.addWidget(self._constructor)

    def _constructor(self):
        widget = ToolBarButton()
        widget.setIcon(QtGui.QIcon("icons/text.svg"))
        widget.setToolTip(widget.tr("Export document to text"))
        widget.clickedEvent = self.clickedEvent
        return widget

    def clickedEvent(self, event=None, widget=None):
        self.actions.onActionButtonPressed(widget)