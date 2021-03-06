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


class ModuleActions(object):

    @inject.params(config='config')
    def onActionWindowResize(self, event=None, config=None):
        size = event.size()
        if size is None:
            return None

        width = size.width()
        if width is not None and width >= 1000:
            config.set('window.width', width)

        height = size.height()
        if height is not None and height >= 800:
            config.set('window.height', height)

        return event.accept()
