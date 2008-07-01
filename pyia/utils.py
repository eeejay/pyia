'''
A collection of useful functions to use in MSAA clients.

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

import constants
from ctypes import windll, oledll, POINTER, byref
from comtypes.automation import VARIANT
from comtypes.gen.Accessibility import IAccessible

def getDesktop():
    desktop_hwnd = windll.user32.GetDesktopWindow()
    desktop_window = accessibleObjectFromWindow(desktop_hwnd)
    for child in desktop_window:
        if child.accRole() == constants.ROLE_SYSTEM_CLIENT:
            return child
    return None

def accessibleObjectFromWindow(hwnd):
    ptr = POINTER(IAccessible)()
    res = oledll.oleacc.AccessibleObjectFromWindow(
        hwnd,0,
        byref(IAccessible._iid_),byref(ptr))
    return ptr

def accessibleObjectFromEvent(event):
    if not windll.user32.IsWindow(event.hwnd):
        return None
    ptr = POINTER(IAccessible)()
    varChild = VARIANT()
    res = windll.oleacc.AccessibleObjectFromEvent(
        event.hwnd, event.object_id, event.child_id,
        byref(ptr), byref(varChild))
    if res == 0:
        child=varChild.value
        return ptr.QueryInterface(IAccessible)
    else:
        return None


def findDescendant(acc, pred, breadth_first=False):
    '''
    Searches for a descendant node satisfying the given predicate starting at 
    this node. The search is performed in depth-first order by default or
    in breadth first order if breadth_first is True. For example,
    
    my_win = findDescendant(lambda x: x.name == 'My Window')
    
    will search all descendants of x until one is located with the name 'My
    Window' or all nodes are exausted. Calls L{_findDescendantDepth} or
    L{_findDescendantBreadth} to start the recursive search.
    
    @param acc: Root accessible of the search
    @type acc: Accessibility.Accessible
    @param pred: Search predicate returning True if accessible matches the 
    search criteria or False otherwise
    @type pred: callable
    @param breadth_first: Search breadth first (True) or depth first (False)?
    @type breadth_first: boolean
    @return: Accessible matching the criteria or None if not found
    @rtype: Accessibility.Accessible or None
    '''
    if breadth_first:
        return _findDescendantBreadth(acc, pred)
    
    for child in acc:
        try:
            ret = _findDescendantDepth(acc, pred)
        except Exception:
            ret = None
        if ret is not None: return ret

def _findDescendantBreadth(acc, pred):
    '''    
    Internal function for locating one descendant. Called by L{findDescendant} to
    start the search.
  
    @param acc: Root accessible of the search
    @type acc: Accessibility.Accessible
    @param pred: Search predicate returning True if accessible matches the 
    search criteria or False otherwise
    @type pred: callable
    @return: Matching node or None to keep searching
    @rtype: Accessibility.Accessible or None
    '''
    for child in acc:
        try:
            if pred(child): return child
        except Exception:
            pass
    for child in acc:
        try:
            ret = _findDescendantBreadth(child, pred)
        except Exception:
            ret = None
        if ret is not None: return ret

def _findDescendantDepth(acc, pred):
    '''
    Internal function for locating one descendant. Called by L{findDescendant} to
    start the search.
    
    @param acc: Root accessible of the search
    @type acc: Accessibility.Accessible
    @param pred: Search predicate returning True if accessible matches the 
    search criteria or False otherwise
    @type pred: callable
    @return: Matching node or None to keep searching
    @rtype: Accessibility.Accessible or None
    '''
    try:
        if pred(acc): return acc
    except Exception:
        pass
    for child in acc:
        try:
            ret = _findDescendantDepth(child, pred)
        except Exception:
            ret = None
        if ret is not None: return ret
    
def findAllDescendants(acc, pred):
  '''
  Searches for all descendant nodes satisfying the given predicate starting at 
  this node. Does an in-order traversal. For example,
  
  pred = lambda x: x.getRole() == pyatspi.ROLE_PUSH_BUTTON
  buttons = pyatspi.findAllDescendants(node, pred)
  
  will locate all push button descendants of node.
  
  @param acc: Root accessible of the search
  @type acc: Accessibility.Accessible
  @param pred: Search predicate returning True if accessible matches the 
      search criteria or False otherwise
  @type pred: callable
  @return: All nodes matching the search criteria
  @rtype: list
  '''
  matches = []
  _findAllDescendants(acc, pred, matches)
  return matches

def _findAllDescendants(acc, pred, matches):
  '''
  Internal method for collecting all descendants. Reuses the same matches
  list so a new one does not need to be built on each recursive step.
  '''
  for child in acc:
    try:
      if pred(child): matches.append(child)
    except Exception:
      pass
    _findAllDescendants(child, pred, matches)
