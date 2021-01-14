# -*-coding:utf-8-*-
# Copyright (c) 2020 DJI.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the file LICENSE.txt or at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import collections
from . import logger


__all__ = ['Handler', 'Dispatcher']


class Handler(collections.namedtuple("Handler", ("obj name f"))):
    __slots__ = ()


class Dispatcher(object):

    def __init__(self):
        self._dispatcher_handlers = collections.defaultdict(list)

    def add_handler(self, obj, name, f):
        handler = Handler(obj, name, f)
        self._dispatcher_handlers[name] = handler
        logger.debug("Dispacher: add_handler {0}, _dispatcher_handlers:{1}".format(name, self._dispatcher_handlers))
        return handler

    def remove_handler(self, name):
        del self._dispatcher_handlers[name]

    def dispatch(self, msg, **kw):
        for name in self._dispatcher_handlers:
            handler = self._dispatcher_handlers[name]
            handler.f(handler.obj, msg)
