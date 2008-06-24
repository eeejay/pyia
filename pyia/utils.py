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
        print 'child', varChild.value
        child=varChild.value
        return ptr
    else:
        return None

