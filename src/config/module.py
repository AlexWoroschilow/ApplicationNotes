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

from lib.plugin import Loader

from .services import ConfigService


class Loader(Loader):

    @property
    def enabled(self):
        return True
    
    def config(self, binder=None):
        binder.bind_to_constructor('config', self._bind_config)

    @inject.params(kernel='kernel', factory='settings_factory')
    def _bind_config(self, kernel=None, factory=None):

        factory.addWidget(self._widget_settings)
        factory.addWidget(self._widget_settings)
        factory.addWidget(self._widget_settings)
        factory.addWidget(self._widget_settings)
        factory.addWidget(self._widget_settings)
        
        return ConfigService(kernel.options.config)

    @inject.params(config='config')
    def _widget_settings(self, config=None):
        from .gui.settings.widget import WidgetSettings
        return WidgetSettings(config)

