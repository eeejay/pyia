'''
A registry, sort of like AT-SPI has. For now it's just an entry point for 
registering liteners for MSAA events.

Inspired by pyatspi:
http://live.gnome.org/GAP/PythonATSPI

@author: Eitan Isaacson
@copyright: Copyright (c) 2008, Eitan Isaacson
@license: LGPL

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Library General Public
License as published by the Free Software Foundation; either
version 2 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Library General Public License for more details.

You should have received a copy of the GNU Library General Public
License along with this library; if not, write to the
Free Software Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.
'''

from . import constants
import traceback
from ctypes import CFUNCTYPE, c_int, c_voidp, windll
from comtypes.client import PumpEvents
from .event import Event
from .utils import accessibleObjectFromEvent

class Registry(object):
    def __init__(self):
        self.clients = {}
        self.hook_ids = []
        self._c_handleEvent = CFUNCTYPE(
                c_voidp,c_int,c_int,c_int,c_int,c_int,c_int,c_int)(
                    self._handleEvent)

    def __call__(self):
        return self

    def _handleEvent(self, handle, eventID, window, objectID, childID, 
                     threadID, timestamp):
        e = Event(eventID, window, objectID, childID, threadID, timestamp)
        for client, event_type in list(self.clients.keys()):
            if event_type == eventID:
                try:
                    client(e)
                except Exception:
                    traceback.print_exc()
            
    def registerEventListener(self, client, *event_types):
        for event_type in event_types:
            if (client, event_type) in self.clients:
                continue
            hook_id = \
                windll.user32.SetWinEventHook(
                    event_type, event_type, 0, self._c_handleEvent, 0, 0, 
                    constants.WINEVENT_OUTOFCONTEXT)
            if hook_id:
                self.clients[(client, event_type)] = hook_id
            else:
                print("Could not register callback for %s" % \
                    constants.winEventIDsToEventNames.get(event_type, event_type))

    def deregisterEventListener(self, client, *event_types):
        for event_type in event_types:
            try:
                windll.user32.UnhookWinEvent(
                    self.clients[(client, event_type)])
                del self.clients[(client, event_type)]
            except KeyError:
                pass

    def clearListeners(self):
        while True:
            try:
                client_tuple, hook_id = self.clients.popitem()
            except KeyError:
                break
            else:
                windll.user32.UnhookWinEvent(hook_id)


    def iter_loop(self, timeout=1):
        PumpEvents(timeout)
        
    def start(self):
        while True:
            try:
                self.iter_loop(5)
            except KeyboardInterrupt:
                self.clearListeners()
                break
