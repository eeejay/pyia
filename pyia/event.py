from constants import winEventIDsToEventNames
from utils import accessibleObjectFromEvent

class Event(object):
    def __init__(self, 
                 event_type, hwnd, object_id, child_id, thread_id, timestamp):
        self.type = event_type
        self.hwnd = hwnd
        self.object_id = object_id
        self.child_id = child_id
        self.thread_id = thread_id
        self.timestamp = timestamp

    def __str__(self):
        return '''\
%s
\tsource: %s
\twindow: %s
\tthread: %s
\ttstamp: %s''' % \
            (winEventIDsToEventNames[self.type], self.source, self.hwnd, 
             self.thread_id, self.timestamp)

    def _get_source(self):
        try:
            rv = self._source
        except AttributeError:
            rv = accessibleObjectFromEvent(self)
        return rv
    
    source = property(_get_source)
