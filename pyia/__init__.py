from comtypes.client import GetModule
GetModule('oleacc.dll')
from comtypes.gen.Accessibility import IAccessible
del GetModule
import accessible
from utils import *
from constants import *
