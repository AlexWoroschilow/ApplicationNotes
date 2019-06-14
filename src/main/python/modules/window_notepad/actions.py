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
import functools

from PyQt5 import QtWidgets
from PyQt5 import QtGui


class ModuleActions(object):

    def onActionFileRenamed(self, source, old, new, widget):
        return self.onActionNoteSelect((source, old, new), widget=widget)

    def onActionNoteSelect(self, event=None, widget=None):
        return self.onActionNoteEdit(widget.current, widget=widget)

    def onActionClone(self, event=None, widget=None):
        return self.onActionCopy(widget.tree.current, widget=widget)

    def onActionRemove(self, event=None, widget=None):
        return self.onActionDelete(widget.tree.current, widget=widget)

    @inject.params(storage='storage', logger='logger')
    def onActionNoteEdit(self, index, storage, logger, widget):
        try:
            if storage.isDir(index):
                return widget.group(index)
            if storage.isFile(index):
                return widget.note(index)
            return widget.demo()
        except Exception as ex:
            logger.exception(ex)

    @inject.params(config='config', storage='storage', logger='logger')
    def onActionNoteCreate(self, event, config, widget, storage, logger):
        try:
            index = widget.current
            if index is None or not index:
                index = config.get('storage.location')
                index = storage.index(index)

            if not storage.isDir(index):
                index = config.get('storage.location')
                index = storage.index(index)

            if storage.isFile(index):
                index = config.get('storage.location')
                index = storage.index(index)

            index = storage.touch(index, 'New note')
            if index is None or not index: return None
            widget.created.emit(index)
        except Exception as ex:
            logger.exception(ex)

    @inject.params(storage='storage', search='search', logger='logger')
    def onActionCopy(self, index, widget, storage, search, logger):
        try:
            index = storage.clone(index)
            if index is None: return None
            widget.created.emit(index)
        except Exception as ex:
            logger.exception(ex)

    @inject.params(storage='storage', dashboard='notepad.dashboard', logger='logger')
    def onActionSave(self, event, storage, dashboard, logger, widget):
        try:
            index, content = event
            if index is None: return None
            index = storage.setFileContent(index, content)
            if index is None or not index: return None
            dashboard.updated.emit(index)
        except Exception as ex:
            logger.exception(ex)

    @inject.params(storage='storage', config='config', logger='logger')
    def onActionFolderCreate(self, event, widget, storage, config, logger):
        try:
            index = widget.tree.current
            if index is None or not index:
                index = config.get('storage.location')
                index = storage.index(index)

            if not storage.isDir(index):
                index = config.get('storage.location')
                index = storage.index(index)

            if storage.isFile(index):
                index = config.get('storage.location')
                index = storage.index(index)

            index = storage.mkdir(index, 'New group')
            return widget.group(index)
        except Exception as ex:
            logger.exception(ex)

    @inject.params(window='window', editor='notepad.editor', storage='storage')
    def onActionFullScreen(self, event, widget, window, editor, storage):
        try:
            editor.index = widget.index
            name = storage.fileName(widget.index)
            window.tab.emit((editor, name))
        except Exception as ex:
            print(ex)

    @inject.params(storage='storage', search='search', logger='logger')
    def onActionDelete(self, index, widget, storage, search, logger):

        message = widget.tr("Are you sure you want to remove this element: {} ?".format(
            storage.fileName(index)
        ))

        reply = QtWidgets.QMessageBox.question(
            widget, 'Remove {}'.format('Group' if storage.isDir(index) else 'Note'),
            message, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.No:
            return None

        try:
            if index is None: return None
            widget.removed.emit(index)
            return storage.remove(index)
        except Exception as ex:
            logger.exception(ex)

    @inject.params(config='config', logger='logger')
    def onActionConfigUpdated(self, event, config=None, widget=None, logger=None):

        try:
            visible = int(config.get('folders.toolbar'))
            widget.toolbar.setVisible(visible)
        except AttributeError as ex:
            logger.exception(ex)

        self.onActionConfigUpdatedEditor(event, widget=widget.editor)

    @inject.params(config='config', logger='logger')
    def onActionConfigUpdatedEditor(self, event, widget, config, logger):

        try:
            visible = int(config.get('editor.formatbar'))
            widget.formatbar.setVisible(visible)
        except AttributeError as ex:
            logger.exception(ex)

        try:
            visible = int(config.get('editor.leftbar'))
            widget.leftbar.setVisible(visible)
        except AttributeError as ex:
            logger.exception(ex)

        try:
            visible = int(config.get('editor.rightbar'))
            widget.rightbar.setVisible(visible)
        except AttributeError as ex:
            logger.exception(ex)

    @inject.params(storage='storage')
    def onActionContextMenu(self, event, widget, storage):

        menu = QtWidgets.QMenu()

        if widget.current and not storage.isDir(widget.current) and widget.editor:
            action = functools.partial(self.onActionFullScreen, event=None, widget=widget.editor)
            menu.addAction(QtGui.QIcon("icons/tab-new"), 'Open in a new tab', action)
            menu.addSeparator()

        action = functools.partial(self.onActionNoteCreate, event=None, widget=widget)
        menu.addAction(QtGui.QIcon("icons/note"), 'Create new note', action)

        action = functools.partial(self.onActionFolderCreate, event=None, widget=widget)
        menu.addAction(QtGui.QIcon("icons/book"), 'Create new group', action)
        menu.addSeparator()

        if widget.current is not None and widget.current:
            action = functools.partial(self.onActionClone, event=None, widget=widget)
            menu.addAction(QtGui.QIcon("icons/copy"), 'Clone selected element', action)

            action = functools.partial(self.onActionRemove, event=None, widget=widget)
            menu.addAction(QtGui.QIcon("icons/trash"), 'Remove selected element', action)

        menu.exec_(widget.tree.mapToGlobal(event))

    @inject.params(storage='storage', config='config')
    def onActionNoteImport(self, event=None, storage=None, config=None, widget=None):
        if widget is None or storage is None or config is None: return None

        currentwd = config.get('storage.lastimport', os.path.expanduser('~'))
        selector = QtWidgets.QFileDialog(None, 'Select file', currentwd)
        if not selector.exec_(): return None

        for path in selector.selectedFiles():
            if not os.path.exists(path) or os.path.isdir(path): continue
            config.set('storage.lastimport', os.path.dirname(path))

            if os.path.getsize(path) / 1000000 >= 1:
                message = "The file  '{}' is about {:>.2f} Mb, are you sure?".format(path,
                                                                                     os.path.getsize(path) / 1000000)
                reply = QtWidgets.QMessageBox.question(widget, 'Message', message, QtWidgets.QMessageBox.Yes,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No: continue

            with open(path, 'r') as source:

                index = widget.current
                if index is None or not index:
                    index = config.get('storage.location')
                    index = storage.index(index)

                if not storage.isDir(index):
                    index = config.get('storage.location')
                    index = storage.index(index)

                if storage.isFile(index):
                    index = config.get('storage.location')
                    index = storage.index(index)

                name = os.path.basename(path)
                index = storage.touch(index, name)
                if index is None: return None
                storage.setFileContent(index, source.read())

                if index is None: return None
                widget.created.emit(index)

                source.close()

    @inject.params(storage='storage', dashboard='notepad.dashboard')
    def onActionStorageChanged(self, destination, storage, dashboard, widget):

        print(destination, storage, dashboard)

        dashboard.tree.setModel(storage)

        index = storage.setRootPath(destination)
        dashboard.tree.setRootIndex(index)
        dashboard.tree.expandAll()

        dashboard.group(index)