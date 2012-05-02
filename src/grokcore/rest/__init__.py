##############################################################################
#
# Copyright (c) 2006-2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

from grokcore.component import *
from grokcore.security import *
from grokcore.view import *
from grokcore.rest.interfaces import IREST
from grokcore.rest.interfaces import IRESTLayer
from grokcore.rest.interfaces import IRESTSkinType
from grokcore.rest.components import REST
from grokcore.rest.directive import restskin
from zope.interface import moduleProvides
moduleProvides(IREST)
__all__ = list(IREST)
