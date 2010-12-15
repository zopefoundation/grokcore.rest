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
"""Grok publication factories and classes.

These factories, and the publication classes they return, make Grok
security different from the way that security normal operates during
Zope publication.  Instead of security proxies being wrapped around
every object generated during traversal, and then wrapped around the
final object before it is viewed, only a single security check is done
when Grok is in charge: a check to see whether the view selected at the
end of the traversal process is, in fact, permitted to display the
object.

"""
from grokcore.rest.rest import GrokMethodNotAllowed
from grokcore.view.publication import ZopePublicationSansProxy
from zope.security.proxy import removeSecurityProxy


from zope import component
from zope.security.checker import selectChecker
from zope.publisher.publish import mapply
from zope.publisher.interfaces.http import IHTTPException

from zope.app.publication.browser import BrowserPublication

from zope.app.publication.http import BaseHTTPPublication, HTTPPublication
from zope.app.publication.requestpublicationfactories import (
    BrowserFactory, HTTPFactory)



class GrokBrowserPublication(ZopePublicationSansProxy, BrowserPublication):
    """Combines `BrowserPublication` with the Grok sans-proxy mixin.

    In addition to the three methods that are overridden by the
    `ZopePublicationSansProxy`, this class overrides a fourth: the
    `getDefaultTraversal()` method, which strips the security proxy from
    the object being returned by the normal method.

    """
    def getDefaultTraversal(self, request, ob):
        obj, path = super(GrokBrowserPublication, self).getDefaultTraversal(
            request, ob)
        return removeSecurityProxy(obj), path


class GrokBrowserFactory(BrowserFactory):
    """Returns the classes Grok uses for browser requests and publication.

    When an instance of this class is called, it returns a 2-element
    tuple containing:

    - The request class that Grok uses for browser requests.
    - The publication class that Grok uses to publish to a browser.

    """
    def __call__(self):
        request, publication = super(GrokBrowserFactory, self).__call__()
        return request, GrokBrowserPublication
