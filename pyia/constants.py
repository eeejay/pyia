'''
Useful constants.

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
# Child ID.
CHILDID_SELF = 0
# Accessible Roles 
# TODO: Is there a way to retrieve this at runtime or build time?
#
ROLE_SYSTEM_ALERT = 8
ROLE_SYSTEM_ANIMATION = 54
ROLE_SYSTEM_APPLICATION = 14
ROLE_SYSTEM_BORDER = 19
ROLE_SYSTEM_BUTTONDROPDOWN  = 56
ROLE_SYSTEM_BUTTONDROPDOWNGRID = 58
ROLE_SYSTEM_BUTTONMENU = 57
ROLE_SYSTEM_CARET = 7
ROLE_SYSTEM_CELL = 29
ROLE_SYSTEM_CHARACTER = 32
ROLE_SYSTEM_CHART = 17
ROLE_SYSTEM_CHECKBUTTON = 44
ROLE_SYSTEM_CLIENT = 10
ROLE_SYSTEM_CLOCK = 61
ROLE_SYSTEM_COLUMN = 27
ROLE_SYSTEM_COLUMNHEADER = 25
ROLE_SYSTEM_COMBOBOX = 46
ROLE_SYSTEM_CURSOR = 6
ROLE_SYSTEM_DIAGRAM = 53
ROLE_SYSTEM_DIAL = 49
ROLE_SYSTEM_DIALOG = 18
ROLE_SYSTEM_DOCUMENT = 15
ROLE_SYSTEM_DROPLIST = 47
ROLE_SYSTEM_EQUATION = 55
ROLE_SYSTEM_GRAPHIC = 40
ROLE_SYSTEM_GRIP = 4
ROLE_SYSTEM_GROUPING = 20
ROLE_SYSTEM_HELPBALLOON = 31
ROLE_SYSTEM_HOTKEYFIELD = 50
ROLE_SYSTEM_INDICATOR = 39
ROLE_SYSTEM_LINK = 30
ROLE_SYSTEM_LIST = 33
ROLE_SYSTEM_LISTITEM = 34
ROLE_SYSTEM_MENUBAR = 2
ROLE_SYSTEM_MENUITEM = 12
ROLE_SYSTEM_MENUPOPUP = 11
ROLE_SYSTEM_OUTLINE = 35
ROLE_SYSTEM_OUTLINEITEM = 36
ROLE_SYSTEM_PAGETAB = 37
ROLE_SYSTEM_PAGETABLIST = 60
ROLE_SYSTEM_PANE = 16
ROLE_SYSTEM_PROGRESSBAR = 48
ROLE_SYSTEM_PROPERTYPAGE = 38
ROLE_SYSTEM_PUSHBUTTON = 43
ROLE_SYSTEM_RADIOBUTTON = 45
ROLE_SYSTEM_ROW = 28
ROLE_SYSTEM_ROWHEADER = 26
ROLE_SYSTEM_SCROLLBAR = 3
ROLE_SYSTEM_SEPARATOR = 21
ROLE_SYSTEM_SLIDER = 51
ROLE_SYSTEM_SOUND = 5
ROLE_SYSTEM_SPINBUTTON = 52
ROLE_SYSTEM_STATICTEXT = 41
ROLE_SYSTEM_STATUSBAR = 23
ROLE_SYSTEM_TABLE = 24
ROLE_SYSTEM_TEXT = 42
ROLE_SYSTEM_TITLEBAR = 1
ROLE_SYSTEM_TOOLBAR = 22
ROLE_SYSTEM_TOOLTIP = 13
ROLE_SYSTEM_WHITESPACE = 59
ROLE_SYSTEM_WINDOW = 9

# Unlocalized role strings
UNLOCALIZED_ROLE_NAMES = {
    1: u'title bar',
    2: u'menu bar',
    3: u'scroll bar',
    4: u'grip',
    5: u'sound',
    6: u'cursor',
    7: u'caret',
    8: u'alert',
    9: u'window',
    10: u'client',
    11: u'popup menu',
    12: u'menu item',
    13: u'tool tip',
    14: u'application',
    15: u'document',
    16: u'pane',
    17: u'chart',
    18: u'dialog',
    19: u'border',
    20: u'grouping',
    21: u'separator',
    22: u'tool bar',
    23: u'status bar',
    24: u'table',
    25: u'column header',
    26: u'row header',
    27: u'column',
    28: u'row',
    29: u'cell',
    30: u'link',
    31: u'help balloon',
    32: u'character',
    33: u'list',
    34: u'list item',
    35: u'outline',
    36: u'outline item',
    37: u'page tab',
    38: u'property page',
    39: u'indicator',
    40: u'graphic',
    41: u'text',
    42: u'editable text',
    43: u'push button',
    44: u'check box',
    45: u'radio button',
    46: u'combo box',
    47: u'drop down',
    48: u'progress bar',
    49: u'dial',
    50: u'hot key field',
    51: u'slider',
    52: u'spin box',
    53: u'diagram',
    54: u'animation',
    55: u'equation',
    56: u'drop down button',
    57: u'menu button',
    58: u'grid drop down button',
    59: u'white space',
    60: u'page tab list',
    61: u'clock'}


# Navigation constants
NAVDIR_DOWN = 2
NAVDIR_FIRSTCHILD = 7
NAVDIR_LASTCHILD = 8
NAVDIR_LEFT = 3
NAVDIR_NEXT = 5
NAVDIR_PREVIOUS = 6
NAVDIR_RIGHT = 4
NAVDIR_UP = 1

STATE_SYSTEM_UNAVAILABLE = 0x1
STATE_SYSTEM_SELECTED = 0x2
STATE_SYSTEM_FOCUSED = 0x4
STATE_SYSTEM_PRESSED = 0x8
STATE_SYSTEM_CHECKED = 0x10
STATE_SYSTEM_MIXED = 0x20
STATE_SYSTEM_READONLY = 0x40
STATE_SYSTEM_HOTTRACKED = 0x80
STATE_SYSTEM_DEFAULT = 0x100
STATE_SYSTEM_EXPANDED = 0x200
STATE_SYSTEM_COLLAPSED = 0x400
STATE_SYSTEM_BUSY = 0x800
STATE_SYSTEM_FLOATING = 0x1000
STATE_SYSTEM_MARQUEED = 0x2000
STATE_SYSTEM_ANIMATED = 0x4000
STATE_SYSTEM_INVISIBLE = 0x8000
STATE_SYSTEM_OFFSCREEN = 0x10000
STATE_SYSTEM_SIZEABLE = 0x20000
STATE_SYSTEM_MOVEABLE = 0x40000
STATE_SYSTEM_SELFVOICING = 0x80000
STATE_SYSTEM_FOCUSABLE = 0x100000
STATE_SYSTEM_SELECTABLE = 0x200000
STATE_SYSTEM_LINKED = 0x400000
STATE_SYSTEM_TRAVERSED = 0x800000
STATE_SYSTEM_MULTISELECTABLE = 0x1000000
STATE_SYSTEM_EXTSELECTABLE = 0x2000000
STATE_SYSTEM_HASSUBMENU = 0x4000000
STATE_SYSTEM_ALERT_LOW = 0x4000000
STATE_SYSTEM_ALERT_MEDIUM = 0x8000000
STATE_SYSTEM_ALERT_HIGH = 0x10000000
STATE_SYSTEM_PROTECTED = 0x20000000
STATE_SYSTEM_HASPOPUP = 0x40000000
STATE_SYSTEM_VALID = 0x1fffffff

# Unlocalized state strings
UNLOCALIZED_STATE_NAMES = {
    1:          u'unavailable',
    2:          u'selected',
    4:          u'focused',
    8:          u'pressed',
    16:         u'checked',
    32:         u'mixed',
    64:         u'read only',
    128:        u'hot tracked',
    256:        u'default',
    512:        u'expanded',
    1024:       u'collapsed',
    2048:       u'busy',
    4096:       u'floating',
    8192:       u'marqueed',
    16384:      u'animated',
    32768:      u'invisible',
    65536:      u'offscreen',
    131072:     u'sizeable',
    262144:     u'moveable',
    524288:     u'self voicing',
    1048576:    u'focusable',
    2097152:    u'selectable',
    4194304:    u'linked',
    8388608:    u'traversed',
    16777216:   u'multiple selectable',
    33554432:   u'extended selectable',
    67108864:   u'alert low',
    134217728:  u'alert medium',
    268435456:  u'alert high',
    536870912:  u'protected',
    1073741824: u'has popup'}

# SetWinEventHook() flags
WINEVENT_OUTOFCONTEXT = 0x0
WINEVENT_SKIPOWNTHREAD =0x1
WINEVENT_SKIPOWNPROCESS = 0x2
WINEVENT_INCONTEXT = 0x4

#win events
EVENT_SYSTEM_SOUND = 0x1
EVENT_SYSTEM_ALERT = 0x2
EVENT_SYSTEM_FOREGROUND = 0x3
EVENT_SYSTEM_MENUSTART = 0x4
EVENT_SYSTEM_MENUEND = 0x5
EVENT_SYSTEM_MENUPOPUPSTART = 0x6
EVENT_SYSTEM_MENUPOPUPEND = 0x7
EVENT_SYSTEM_CAPTURESTART = 0x8
EVENT_SYSTEM_CAPTUREEND = 0x9
EVENT_SYSTEM_MOVESIZESTART = 0xa
EVENT_SYSTEM_MOVESIZEEND = 0xb
EVENT_SYSTEM_CONTEXTHELPSTART = 0xc
EVENT_SYSTEM_CONTEXTHELPEND = 0xd
EVENT_SYSTEM_DRAGDROPSTART = 0xe
EVENT_SYSTEM_DRAGDROPEND = 0xf
EVENT_SYSTEM_DIALOGSTART = 0x10
EVENT_SYSTEM_DIALOGEND = 0x11
EVENT_SYSTEM_SCROLLINGSTART = 0x12
EVENT_SYSTEM_SCROLLINGEND = 0x13
EVENT_SYSTEM_SWITCHSTART = 0x14
EVENT_SYSTEM_SWITCHEND = 0x15
EVENT_SYSTEM_MINIMIZESTART = 0x16
EVENT_SYSTEM_MINIMIZEEND = 0x17
EVENT_OBJECT_CREATE = 0x8000
EVENT_OBJECT_DESTROY = 0x8001
EVENT_OBJECT_SHOW = 0x8002
EVENT_OBJECT_HIDE = 0x8003
EVENT_OBJECT_REORDER = 0x8004
EVENT_OBJECT_FOCUS = 0x8005
EVENT_OBJECT_SELECTION = 0x8006
EVENT_OBJECT_SELECTIONADD = 0x8007
EVENT_OBJECT_SELECTIONREMOVE = 0x8008
EVENT_OBJECT_SELECTIONWITHIN = 0x8009
EVENT_OBJECT_STATECHANGE = 0x800a
EVENT_OBJECT_LOCATIONCHANGE = 0x800b
EVENT_OBJECT_NAMECHANGE = 0x800c
EVENT_OBJECT_DESCRIPTIONCHANGE = 0x800d
EVENT_OBJECT_VALUECHANGE = 0x800e
EVENT_OBJECT_PARENTCHANGE = 0x800f
EVENT_OBJECT_HELPCHANGE = 0x8010
EVENT_OBJECT_DEFACTIONCHANGE = 0x8011
EVENT_OBJECT_ACCELERATORCHANGE = 0x8012
EVENT_CONSOLE_CARET = 0x4001
EVENT_CONSOLE_UPDATE_REGION = 0x4002
EVENT_CONSOLE_UPDATE_SIMPLE = 0x4003
EVENT_CONSOLE_UPDATE_SCROLL = 0x4004
EVENT_CONSOLE_LAYOUT = 0x4005
EVENT_CONSOLE_START_APPLICATION = 0x4006
EVENT_CONSOLE_END_APPLICATION = 0x4007

winEventIDsToEventNames={}

for _sym, _val in locals().items():
    if _sym.startswith('EVENT_'):
        winEventIDsToEventNames[_val] = _sym
