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

from .actions import ModuleActions
from .gui.preview.list import PreviewScrollArea

from .decorators import service_settings_decorator


class Loader(object):
    actions = ModuleActions()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @service_settings_decorator
    @inject.params(store='store')
    def boot(self, options, args, store):
        store.subscribe(self.update)

    @inject.params(store='store', window='window')
    def update(self, store=None, window=None):
        state = store.get_state()
        if state is None:
            return None

        if 'document' in state.keys():
            document = state['document']
            return self.actions. \
                onActionDocumentUpdate(document)

        if 'search' not in state.keys():
            return None

        print(state)
        for search in state['search']:
            if search is None:
                continue

            preview = PreviewScrollArea(window)
            preview.setTitle(search['title'])
            preview.selectAction.connect(self.actions.onActionSelect)
            preview.setPreview(search['documents'])

            window.newTabAction.emit((preview, search['title']))
