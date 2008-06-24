import constants
from ctypes import CFUNCTYPE, c_int, c_voidp, windll
from comtypes.client import PumpEvents

class Registry(object):
    def __init__(self):
        self.clients = {}
        self.hook_ids = []
        self._c_handleEvent = CFUNCTYPE(
                c_voidp,c_int,c_int,c_int,c_int,c_int,c_int,c_int)(
                    self._handleEvent)

    def _handleEvent(self, handle, eventID, window, objectID, childID, 
                     threadID, timestamp):
        for client, event_type in self.clients:
            if event_type == eventID:
                client(handle, eventID, window, objectID, 
                       childID, threadID, timestamp)
            
    def registerEventListener(self, client, *event_types):
        for event_type in event_types:
            if self.clients.has_key((client, event_type)):
                continue
            hook_id = \
                windll.user32.SetWinEventHook(
                    event_type, event_type, 0, self._c_handleEvent, 0, 0, 0)
            if hook_id:
                self.clients[(client, event_type)] = hook_id
            else:
                print "Could not register callback for %s" % \
                    constants.winEventIDsToEventNames(event_type)

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

    def start(self):
        while True:
            PumpEvents(5)

def print_event(handle, eventID, window, objectID, 
                childID, threadID, timestamp):
    print handle, eventID, window, objectID, childID, \
        threadID, timestamp, constants.winEventIDsToEventNames[eventID]
