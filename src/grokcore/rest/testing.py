##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
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
"""Grok test helpers
"""
from zope.configuration.config import ConfigurationMachine
from grokcore.component import zcml


def grok(module_name):
    config = ConfigurationMachine()
    zcml.do_grok('grokcore.component.meta', config)
    zcml.do_grok('grokcore.security.meta', config)
    zcml.do_grok('grokcore.view.meta', config)
    zcml.do_grok('grokcore.rest.meta', config)
    zcml.do_grok(module_name, config)
    config.execute_actions()


def bprint(data):
    """Python 2 and 3 doctest compatible print.

    http://python3porting.com/problems.html#string-representation
    """
    if not isinstance(data, str):
        data = data.decode()
    print(data.strip())
