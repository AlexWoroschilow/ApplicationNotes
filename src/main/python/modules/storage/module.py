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
import os
import inject

from lib.plugin import Loader
import functools
from .actions import ModuleActions


class Loader(Loader):
    actions = ModuleActions()

    def enabled(self, options=None, args=None):
        return True

    def config(self, binder=None):
        binder.bind_to_constructor('storage', self._storage)

    @inject.params(config='config')
    def _storage(self, config=None):
        if not len(config.get('storage.location')): return None

        storage = config.get('storage.location')
        if len(storage) and storage.find('~') >= 0:
            storage = os.path.expanduser(storage)
        if not os.path.exists(storage):
            if not os.path.exists(storage):
                os.makedirs(storage)

        from .service.storage import FilesystemStorage
        return FilesystemStorage(storage)

    @inject.params(config='config')
    def _widget_settings_storage(self, config=None):
        if config is None:
            return None

        from .gui.settings.storage import WidgetSettingsStorage

        widget = WidgetSettingsStorage()
        widget.location.setText(config.get('storage.location'))
        action = functools.partial(self.actions.onActionStorageLocationChange, widget=widget)
        widget.location.clicked.connect(action)

        return widget

    @inject.params(config='config', factory='settings_factory')
    def boot(self, options=None, args=None, config=None, factory=None):
        if options is None or args is None or factory is None:
            return None

        factory.addWidget(self._widget_settings_storage)
