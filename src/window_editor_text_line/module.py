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
import functools

from PyQt5 import QtGui

from lib.plugin import Loader
from lib.widget.button import ToolBarButton


class Loader(Loader):

    @property
    def enabled(self):
        return True

    @inject.params(kernel='kernel')
    def boot(self, options=None, args=None, kernel=None):
        kernel.listen('window.notepad.formatbar', self._onWindowNotepadToolbar, 110)

    def _onWindowNotepadToolbar(self, event=None):
        widget = ToolBarButton()
        widget.editor, widget.toolbar = event.data
        if widget.editor is None or widget.toolbar is None:
            raise 'Editor or Toolbar object can not be empty'
        
        widget.setIcon(QtGui.QIcon("icons/line.svg"))
        widget.setToolTip(widget.tr('Add a line'))
        
        widget.clicked.connect(functools.partial(
            self._onButtonPressed, widget=widget
        ))

        widget.toolbar.addWidget(widget)

    def _onButtonPressed(self, event=None, widget=None):
        if widget is not None and widget.editor is not None:
            widget.editor.insertHtml('<hr>< /hr>')