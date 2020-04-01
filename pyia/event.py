'''
Useful event wrappers that make life easier.

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

from .constants import winEventIDsToEventNames
from .utils import accessibleObjectFromEvent

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
            (winEventIDsToEventNames.get(self.type, self.type), 
             self.source, self.hwnd, self.thread_id, self.timestamp)

    def _get_source(self):
        try:
            rv = self._source
        except AttributeError:
            rv = accessibleObjectFromEvent(self)
        return rv
    
    source = property(_get_source)
