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
"""Grok interfaces
"""
from zope import interface
from zope.interface.interfaces import IInterface
from zope.publisher.interfaces.http import IHTTPRequest


# Expose interfaces from grokcore.* packages as well:
import grokcore.component.interfaces
import grokcore.security.interfaces
import grokcore.view.interfaces


class IBaseClasses(
    grokcore.component.interfaces.IBaseClasses,
    grokcore.view.interfaces.IBaseClasses,
    grokcore.security.interfaces.IBaseClasses
    ):
    REST = interface.Attribute("Base class for REST views.")


class IGrokcoreRestAPI(
    grokcore.component.interfaces.IGrokcoreComponentAPI,
    grokcore.security.interfaces.IGrokcoreSecurityAPI,
    grokcore.view.interfaces.IGrokcoreViewAPI,
    IBaseClasses
    ):

    IRESTSkinType = interface.Attribute('The REST skin type')

    body = interface.Attribute(
        """The text of the request body.""")

    context = interface.Attribute(
        "Object that the REST handler presents.")

    request = interface.Attribute(
        "Request that REST handler was looked up with.")


class IREST(interface.Interface):
    context = interface.Attribute("Object that the REST handler presents.")

    request = interface.Attribute(
        "Request that REST handler was looked up with.")


class IRESTLayer(IHTTPRequest):
    """REST-specific Request functionality.

    Base Interfaces for defining REST-layers.
    """


class IRESTSkinType(IInterface):
    """Skin type for REST requests.
    """
