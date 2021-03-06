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
import pydux
import inject

from .actions import StorageActions


class Loader(object):
    order = 99
    actions = StorageActions()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __store(self):
        """
        Store constructor, default reducer does nothing
        :return:
        """

        def default(state, action):
            return state

        return pydux.create_store(default, {})

    def configure(self, binder, options, args):
        """
        Configure service container for the dependency injections
        :param binder:
        :param options:
        :param args:
        :return:
        """
        binder.bind_to_constructor('store', self.__store)

    @inject.params(store='store')
    def boot(self, options, args, store):
        """
        Do staff after the service container was build
        :param options:
        :param args:
        :param store:
        :return:
        """
        store.replace_reducer(self.update)

    def update(self, state=None, action=None):

        if action.get('type') == '@@redux/INIT':
            return self.actions.initAction(state, action)

        if action.get('type') == '@@app/search/index/progress':
            return self.actions.searchIndexProgressAction(state, action)

        if action.get('type') == '@@app/search/index/rebuild':
            return self.actions.searchIndexAction(state, action)

        if action.get('type') == '@@app/storage/location/switch':
            return self.actions.locationSwitchAction(state, action)

        if action.get('type') == '@@app/search/request':
            return self.actions.searchAction(state, action)

        if action.get('type') == '@@app/storage/resource/selected/document':
            return self.actions.selectDocumentEvent(state, action)

        if action.get('type') == '@@app/storage/resource/found/document':
            return self.actions.foundDocumentEvent(state, action)

        if action.get('type') == '@@app/storage/resource/selected/group':
            return self.actions.selectGroupEvent(state, action)

        if action.get('type') == '@@app/storage/resource/create/document':
            return self.actions.createDocumentEvent(state, action)

        if action.get('type') == '@@app/storage/resource/create/group':
            return self.actions.createGroupEvent(state, action)

        if action.get('type') == '@@app/storage/resource/update/document':
            return self.actions.updateDocumentEvent(state, action)

        if action.get('type') == '@@app/storage/resource/remove':
            return self.actions.removeResourceEvent(state, action)

        if action.get('type') == '@@app/storage/resource/clone':
            return self.actions.cloneResourceEvent(state, action)

        if action.get('type') == '@@app/storage/resource/move':
            return self.actions.moveResourceEvent(state, action)

        if action.get('type') == '@@app/storage/resource/rename':
            return self.actions.renameResourceEvent(state, action)

        return state


module = Loader()
