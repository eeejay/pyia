import new
import types
from comtypes.automation import VARIANT, VT_I4, VT_DISPATCH
from ctypes import c_long, oledll, byref, create_unicode_buffer
from comtypes.gen.Accessibility import IAccessible

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
        # TODO: Getting a child with cChildren=1 with a desktop client 
        # container returns nothing. So we are doing this the bone headed way.
        for i, child in enumerate(self):
            if i == index:
                return child
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
            return '[%s | %s]' % (self.accRoleName(), self.accName() or '')
        except:
            return '[DEAD]'

    def __len__(self):
        return self.accChildCount

    def accStateName(self):
        states = []
        state = self.accState()
        state_bit = 1
        for shift in xrange(64):
            state_bit = state_bit << shift
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
        role = self.accRole()
        roleLen = oledll.oleacc.GetRoleTextW(role,0,0)
        if roleLen:
            buf = create_unicode_buffer(roleLen + 2)
            oledll.oleacc.GetRoleTextW(role, buf, roleLen + 1)
            return buf.value
        else:
            return ''

_mixClass(IAccessible, _IAccessibleMixin)
