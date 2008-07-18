'''
Creates functions at import time that are mixed into the 
IAccessible base class to make it more Pythonic.

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

import new
import types
from comtypes.automation import VARIANT, VT_I4, VT_DISPATCH
from ctypes import c_long, oledll, byref, create_unicode_buffer
from comtypes.gen.Accessibility import IAccessible
from comtypes import named_property, COMError, hresult
from constants import CHILDID_SELF

def _makeExceptionHandler(func):
    '''
    Builds a function calling the one it wraps in try/except statements catching
    COMError exceptions.
  
    @return: Function calling the method being wrapped
    @rtype: function
    '''
    def _inner(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except COMError, e:
            # TODO: Translate COMErrors to more pythonic equivalents.
            raise
    return _inner

def _mixExceptions(cls):
    '''
    Wraps all methods and properties in a class with handlers for CORBA 
    exceptions.
    
    @param cls: Class to mix interface methods into
    @type cls: class
    '''
    # get a method type as a reference from a known method
    # loop over all names in the new class
    for name in cls.__dict__.keys():
        obj = cls.__dict__[name]
        # check if we're on a protected or private method
        if name.startswith('_'):
            continue
        # check if we're on a method
        elif isinstance(obj, new.instancemethod):
            # wrap the function in an exception handler
            method = _makeExceptionHandler(obj)
            # add the wrapped function to the class
            setattr(cls, name, method)
        elif isinstance(obj, named_property):
            # wrap the function in an exception handler
            if obj.getter is not None:
                obj.getter = _makeExceptionHandler(obj.getter)
            if obj.setter is not None:
                obj.setter = _makeExceptionHandler(obj.setter)
        # check if we're on a property
        elif isinstance(obj, property):
            # wrap the getters and setters
            if obj.fget and obj.fget.__name__ != '_inner':
                getter = _makeExceptionHandler(obj.fget)
            else:
                getter = None
            if obj.fset and obj.fset.__name__ != '_inner':
                setter = _makeExceptionHandler(obj.fset)
            else:
                setter = None
            setattr(cls, name, property(getter, setter))

def _mixClass(cls, new_cls, ignore=[]):
    '''
    Adds the methods in new_cls to cls. After mixing, all instances of cls will
    have the new methods. If there is a method name clash, the method already 
    in cls will be prefixed with '_mix_' before the new method of the same 
    name is mixed in.
    
    @note: _ is not the prefix because if you wind up with __ in front of a 
    variable, it becomes private and mangled when an instance is created. 
    Difficult to invoke from the mixin class.
    
    @param cls: Existing class to mix features into
    @type cls: class
    @param new_cls: Class containing features to add
    @type new_cls: class
    @param ignore: Ignore these methods from the mixin
    @type ignore: iterable
    '''
    # loop over all names in the new class
    for name, func in new_cls.__dict__.items():
        if name in ignore:
            continue
        if isinstance(func, types.FunctionType):
            # build a new function that is a clone of the one from new_cls
            method = new.function(func.func_code, func.func_globals, name, 
                                  func.func_defaults, func.func_closure)
            try:
                # check if a method of the same name already exists in the 
                # target
                old_method = getattr(cls, name)
            except AttributeError:
                pass
            else:
                # rename the old method so we can still call it if need be
                setattr(cls, '_mix_'+name, old_method)
            # add the clone to cls
            setattr(cls, name, method)
        elif isinstance(func, staticmethod):
            try:
                # check if a method of the same name already exists 
                # in the target
                old_method = getattr(cls, name)
            except AttributeError:
                pass
            else:
                # rename the old method so we can still call it if need be
                setattr(cls, '_mix_'+name, old_method)
            setattr(cls, name, func)
        elif isinstance(func, property):
            try:
                # check if a method of the same name already exists 
                # in the target
                old_prop = getattr(cls, name)
            except AttributeError:
                pass
            else:
                # IMPORTANT: We save the old property before overwriting it, 
                # even though we never end up calling the old prop from our 
                # mixin class If we don't save the old one, we seem to 
                # introduce a Python ref count problem where the property 
                # get/set methods disappear before we can use them at a later 
                # time. This is a minor waste of memory because a property is 
                # a class object and we only overwrite a few of them.
                setattr(cls, '_mix_'+name, old_prop)
            setattr(cls, name, func)


class _IAccessibleMixin(object):
    def __getitem__(self, index):
        n = self.accChildCount
        if index >= n or index < -n:
            raise IndexError
        elif index < 0:
            index += n
        children = (VARIANT*1)()
        pcObtained = c_long()
        oledll.oleacc.AccessibleChildren(
            self, index, 1, children, byref(pcObtained))
        child = children[0]
        if child.vt == VT_I4:
            try:
                return \
                    self.accChild(child).QueryInterface(IAccessible)
            except:
                raise IndexError
        elif child.vt == VT_DISPATCH:
            return child.value.QueryInterface(IAccessible)
        else:
            for i, item in enumerate(self):
                if i == index:
                    return item
        raise IndexError


    def __iter__(self):
        accChildCount = self.accChildCount
        VariantArrayType = VARIANT * accChildCount
        rgvarChildren = VariantArrayType()
        pcObtained = c_long()
        oledll.oleacc.AccessibleChildren(self, 0, accChildCount, rgvarChildren,
                                  byref(pcObtained))
        for child in rgvarChildren:
            if child.vt == VT_I4:
                try:
                    ppdispChild = ia.accChild(child)
                    if ppdispChild:
                        yield ppdispChild.QueryInterface(IAccessible)
                except:
                    pass
            elif child.vt == VT_DISPATCH:
                yield child.value.QueryInterface(IAccessible)

    def __str__(self):
        try:
            return u'[%s | %s]' % (self.accRoleName(), 
                                   self.accName(CHILDID_SELF) or '')
        except:
            raise
            return u'[DEAD]'

    def __len__(self):
        return self.accChildCount

    def accStateName(self):
        states = []
        state = self.accState(CHILDID_SELF)
        for shift in xrange(64):
            state_bit = 1 << shift
            if state_bit & state:
                states.append(self._getStateText(state_bit & state))
        return ' '.join(states)

    def _getStateText(self, state_bit):
        stateLen = oledll.oleacc.GetStateTextW(state_bit,0,0)
        if stateLen:
            buf = create_unicode_buffer(stateLen + 2)
            oledll.oleacc.GetStateTextW(state_bit, buf, stateLen + 1)
            return buf.value
        else:
            return ''
        
    def accRoleName(self):
        role = self.accRole(CHILDID_SELF)
        roleLen = oledll.oleacc.GetRoleTextW(role,0,0)
        if roleLen:
            buf = create_unicode_buffer(roleLen + 2)
            oledll.oleacc.GetRoleTextW(role, buf, roleLen + 1)
            return buf.value
        else:
            return ''

_mixExceptions(IAccessible)
_mixClass(IAccessible, _IAccessibleMixin)
