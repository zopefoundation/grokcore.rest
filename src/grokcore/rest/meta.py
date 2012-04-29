#############################################################################
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
"""Grokkers for Grok-configured components.

This `meta` module contains the actual grokker mechanisms for which the
Grok web framework is named.  A directive in the adjacent `meta.zcml`
file directs the `martian` library to scan this file, where it discovers
and registers the grokkers you see below.  The grokkers are then active
and available as `martian` recursively examines the packages and modules
of a Grok-based web application.

"""
from martian.error import GrokError
from zope import interface, component
from grokcore.view import make_checker
from zope.interface.interface import InterfaceClass

import martian
import grokcore.rest
import grokcore.component
import grokcore.component.util
import grokcore.view
import grokcore.security


class RESTGrokker(martian.MethodGrokker):
    """Grokker for methods of a `grok.REST` subclass.

    When an application defines a `grok.REST` view, we do not actually
    register the view with the Component Architecture.  Instead, we grok
    each of its methods separately, placing them each inside of a new
    class that we create on-the-fly by calling `type()`.  We make each
    method the `__call__()` method of its new class, since that is how
    Zope always invokes views.  And it is this new class that is then
    made the object of the two configuration actions that we schedule:
    one to activate it as a REST adapter for the context, and the other
    to prepare a security check for the adapter.

    This results in several registered views, typically with names like
    `GET`, `PUT`, and `POST` - one for each method that the `grok.REST`
    subclass defines.

    """
    martian.component(grokcore.rest.REST)
    martian.directive(grokcore.component.context)
    martian.directive(grokcore.view.layer, default=grokcore.rest.IRESTLayer)
    martian.directive(grokcore.security.require, name='permission')

    def execute(self, factory, method, config, permission, context,
                layer, **kw):
        name = method.__name__

        method_view = type(
            factory.__name__, (factory,),
            {'__call__': method})

        adapts = (context, layer)
        config.action(
            discriminator=('adapter', adapts, interface.Interface, name),
            callable=grokcore.component.util.provideAdapter,
            args=(method_view, adapts, interface.Interface, name),
            )
        config.action(
            discriminator=('protectName', method_view, '__call__'),
            callable=make_checker,
            args=(factory, method_view, permission),
            )
        return True


_restskin_not_used = object()


class RestskinInterfaceDirectiveGrokker(martian.InstanceGrokker):
    """Grokker for interfaces providing the `grok.restskin()` directive.

    Applications create REST skins by subclassing `grok.IRESTLayer`
    and providing the subclass with a `grok.restskin()` directive giving
    the prefix string which distinguishes that REST layers from others.
    This grokker registers those skins.

    """
    martian.component(InterfaceClass)

    def grok(self, name, interface, module_info, config, **kw):
        # This `InstanceGrokker` will be called for every instance of
        # `InterfaceClass` - that is, for every interface defined in an
        # application module!  So we have to do our own filtering, by
        # checking whether each interface includes the `grok.restskin()`
        # directive, and skipping those that do not.
        restskin = grokcore.rest.restskin.bind(default=_restskin_not_used
                                               ).get(interface)
        if restskin is _restskin_not_used:
            # The restskin directive is not actually used on the found
            # interface.
            return False

        if not interface.extends(grokcore.rest.IRESTLayer):
            # For REST layers it is required to extend IRESTLayer.
            raise GrokError(
                "The grok.restskin() directive is used on interface %r. "
                "However, %r does not extend IRESTLayer which is "
                "required for interfaces that are used as layers and are to "
                "be registered as a restskin."
                % (interface.__identifier__, interface.__identifier__),
                interface)

        config.action(
            discriminator=('restprotocol', restskin),
            callable=grokcore.component.util.provideInterface,
            args=(restskin, interface, grokcore.rest.IRESTSkinType))

        return True
