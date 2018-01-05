"""
Let's examine Grok's REST support.

  >>> from zope.publisher.browser import TestRequest
  >>> from zope.component import getMultiAdapter
  >>> from grokcore.rest.rest import GrokMethodNotAllowed

  >>> erview = getMultiAdapter((GrokMethodNotAllowed(None, None),
  ...      TestRequest()), name="index.html")

  >>> erview
  <grokcore.rest.rest.MethodNotAllowedView object at 0...>

Let's create a simple application with REST support::

  >>> from grokcore.rest.ftests.rest.rest import MyApp
  >>> root = getRootFolder()
  >>> root['app'] = MyApp()
  >>> root['app']['alpha'] = MyContent()

Issue a GET request::

  >>> response = http_call(wsgi_app(), 'GET', 'http://localhost/++rest++a/app')
  >>> bprint(response.getBody())
  GET

Issue a POST request::

  >>> response = http_call(wsgi_app(), 'POST', 'http://localhost/++rest++a/app')
  >>> bprint(response.getBody())
  POST

Issue a PUT request::

  >>> response = http_call(wsgi_app(), 'PUT', 'http://localhost/++rest++a/app')
  >>> bprint(response.getBody())
  PUT

Issue a DELETE request::

  >>> response = http_call(wsgi_app(), 'DELETE', 'http://localhost/++rest++a/app')
  >>> bprint(response.getBody())
  DELETE

Let's examine a rest protocol b which has no POST or DELETE request defined::

The GET request works as expected::

  >>> response = http_call(wsgi_app(), 'GET', 'http://localhost/++rest++b/app')
  >>> bprint(response.getBody())
  GET

So does the PUT request::

  >>> response = http_call(wsgi_app(), 'PUT', 'http://localhost/++rest++b/app')
  >>> bprint(response.getBody())
  PUT

POST is not defined, however, and we should get a 405 (Method not
allowed) error::

  >>> response = http_call(wsgi_app(), 'POST', 'http://localhost/++rest++b/app')
  Traceback (most recent call last):
    ...
  grokcore.rest.rest.GrokMethodNotAllowed: \
  <grokcore.rest.ftests.rest.rest.MyApp object at ...>,
  <zope.publisher.browser.BrowserRequest instance URL=http://localhost/++rest++b/app>

DELETE is also not defined, so we also expect a 405 error::

  >>> response = http_call(wsgi_app(), 'DELETE', 'http://localhost/++rest++b/app')
  Traceback (most recent call last):
    ...
  grokcore.rest.rest.GrokMethodNotAllowed: \
  <grokcore.rest.ftests.rest.rest.MyApp object at ...>,
  <zope.publisher.http.HTTPRequest instance URL=http://localhost/++rest++b/app>

Let's examine protocol c where no method is allowed::

  >>> response = http_call(wsgi_app(), 'GET', 'http://localhost/++rest++c/app')
  Traceback (most recent call last):
    ...
  grokcore.rest.rest.GrokMethodNotAllowed: \
  <grokcore.rest.ftests.rest.rest.MyApp object at ...
  >>> response = http_call(wsgi_app(), 'POST', 'http://localhost/++rest++c/app')
  Traceback (most recent call last):
    ...
  grokcore.rest.rest.GrokMethodNotAllowed: \
  <grokcore.rest.ftests.rest.rest.MyApp object at ...
  >>> response = http_call(wsgi_app(), 'PUT', 'http://localhost/++rest++c/app')
  Traceback (most recent call last):
    ...
  grokcore.rest.rest.GrokMethodNotAllowed: \
  <grokcore.rest.ftests.rest.rest.MyApp object at ...
  >>> response = http_call(wsgi_app(), 'DELETE', 'http://localhost/++rest++c/app')
  Traceback (most recent call last):
    ...
  grokcore.rest.rest.GrokMethodNotAllowed: \
  <grokcore.rest.ftests.rest.rest.MyApp object at ...

Let's examine the default protocol d, where nothing should work as well::

  >>> response = http_call(wsgi_app(), 'GET', 'http://localhost/++rest++d/app')
  Traceback (most recent call last):
    ...
  grokcore.rest.rest.GrokMethodNotAllowed: \
  <grokcore.rest.ftests.rest.rest.MyApp object at ...
  >>> response = http_call(wsgi_app(), 'POST', 'http://localhost/++rest++d/app')
  Traceback (most recent call last):
    ...
  grokcore.rest.rest.GrokMethodNotAllowed: \
  <grokcore.rest.ftests.rest.rest.MyApp object at ...
  >>> response = http_call(wsgi_app(), 'PUT', 'http://localhost/++rest++d/app')
  Traceback (most recent call last):
    ...
  grokcore.rest.rest.GrokMethodNotAllowed: \
  <grokcore.rest.ftests.rest.rest.MyApp object at ...
  >>> response = http_call(wsgi_app(), 'DELETE', 'http://localhost/++rest++d/app')
  Traceback (most recent call last):
    ...
  grokcore.rest.rest.GrokMethodNotAllowed: \
  <grokcore.rest.ftests.rest.rest.MyApp object at ...

We have added support for GET for the ``alpha`` subobject only, in
the default rest layer::

  >>> response = http_call(wsgi_app(), 'GET', 'http://localhost/++rest++d/app/alpha')
  >>> bprint(response.getBody())
  GET2

But not for POST::

  >>> response = http_call(wsgi_app(), 'POST', 'http://localhost/++rest++d/app/alpha')
  Traceback (most recent call last):
    ...
  grokcore.rest.rest.GrokMethodNotAllowed: \
  <grokcore.rest.ftests.rest.rest.MyContent object at ...

According to the HTTP spec, in case of a 405 Method Not Allowed error,
the response MUST include an Allow header containing a list of valid
methods for the requested resource::

  >>> print(http(wsgi_app(), b'POST /++rest++b/app HTTP/1.1'))
  HTTP/1.0 405 Method Not Allowed
  Allow: GET, PUT
  Content-Length: 18
  Content-Type: text/plain;charset=utf-8
  <BLANKLINE>
  Method Not Allowed

  >>> print(http(wsgi_app(), b'DELETE /++rest++b/app HTTP/1.1'))
  HTTP/1.0 405 Method Not Allowed
  Allow: GET, PUT
  Content-Length: 18
  <BLANKLINE>
  Method Not Allowed

  >>> print(http(wsgi_app(), b'POST /++rest++c/app HTTP/1.1'))
  HTTP/1.0 405 Method Not Allowed
  Allow:
  Content-Length: 18
  Content-Type: text/plain;charset=utf-8
  <BLANKLINE>
  Method Not Allowed

We can also try this with a completely made-up request method, like FROG::

  >>> print(http(wsgi_app(), b'FROG /++rest++b/app HTTP/1.1'))
  HTTP/1.0 405 Method Not Allowed
  Content-Length: 18
  Allow: GET, PUT
  <BLANKLINE>
  Method Not Allowed

Let's now see whether security works properly with REST. GET should
be public::

  >>> print(http(wsgi_app(), b'GET /++rest++e/app/alpha HTTP/1.1'))
  HTTP/1.0 200 Ok
  Content-Length: 4
  Content-Type: text/plain;charset=utf-8
  <BLANKLINE>
  GET3

POST, PUT and DELETE however are not public::

  >>> print(http(wsgi_app(), b'POST /++rest++e/app/alpha HTTP/1.1'))
  HTTP/1.0 401 Unauthorized
  Content-Length: 0
  Content-Type: text/plain;charset=utf-8
  WWW-Authenticate: basic realm="Zope"
  <BLANKLINE>

  >>> print(http(wsgi_app(), b'PUT /++rest++e/app/alpha HTTP/1.1'))
  HTTP/1.0 401 Unauthorized
  Content-Length: 0
  WWW-Authenticate: basic realm="Zope"
  <BLANKLINE>

  >>> print(http(wsgi_app(), b'DELETE /++rest++e/app/alpha HTTP/1.1'))
  HTTP/1.0 401 Unauthorized
  Content-Length: 0
  WWW-Authenticate: basic realm="Zope"
  <BLANKLINE>

Normally when we POST or PUT a request, we expect some content. This
content is sent along as the request body. In the normal case for POST
we tend to retrieve this information from a web form (request.form),
but with REST often the POST body contains a description of an
entirely new resource, similar to what is contained in a PUT body. We
therefore need to have some easy way to get to this information. The 'body'
attribute on the REST view contains the uploaded data::

  >>> bprint(http_call(
  ...     wsgi_app(), 'POST', 'http://localhost/++rest++f/app/alpha',
  ...     b'this is the POST body'))
  HTTP/1.0 200 Ok
  Content-Length: 21
  Content-Type: text/plain;charset=utf-8
  <BLANKLINE>
  this is the POST body

This works with PUT as well::

  >>> bprint(http_call(
  ...    wsgi_app(), 'PUT', 'http://localhost/++rest++f/app/alpha',
  ...    b'this is the PUT body'))
  HTTP/1.0 200 Ok
  Allow:
  Content-Length: 20
  <BLANKLINE>
  this is the PUT body

Opening up the publication for REST doesn't mean we can just delete
random objects without access:

  >>> print(http(wsgi_app(), b'DELETE /app HTTP/1.1'))
  HTTP/1.0 405 Method Not Allowed
  Allow:
  Content-Length: 18
  Method Not Allowed

  >>> print(http(wsgi_app(), b'DELETE /app/alpha HTTP/1.1'))
  HTTP/1.0 405 Method Not Allowed
  Content-Length: 18
  Allow:
  Method Not Allowed

 We shouldn't be allowed to PUT either::

  >>> print(http(wsgi_app(), b'PUT /app/beta HTTP/1.1'))
  HTTP/1.0 404 Not Found
  Content-Length: 0

XXX shouldn't this really give a FORBIDDEN response?

Let's add another two pieces of content, one for which a REST view is
declared on the IFoo interface, and another one where this is also the
case, but a more specific REST view is declared on the class itself::

  >>> root['app']['one'] = MyInterfaceContent()
  >>> root['app']['two'] = MyNoInterfaceContent()

We should get a different result for the GET request::

  >>> response = http_call(wsgi_app(), 'GET', 'http://localhost/++rest++g/app/one')
  >>> bprint(response.getBody())
  GET interface registered
  >>> response = http_call(wsgi_app(), 'GET', 'http://localhost/++rest++g/app/two')
  >>> bprint(response.getBody())
  GET directly registered

We should also get a different result for the PUT request::

  >>> response = http_call(wsgi_app(), 'PUT', 'http://localhost/++rest++g/app/one')
  >>> bprint(response.getBody())
  PUT interface registered
  >>> response = http_call(wsgi_app(), 'PUT', 'http://localhost/++rest++g/app/two')
  >>> bprint(response.getBody())
  PUT directly registered

We expect POST and DELETE to be the same on both. For the directly
registered object (two) it should fall back to the interface as there
is none more specifically declared::

  >>> response = http_call(wsgi_app(), 'POST', 'http://localhost/++rest++g/app/one')
  >>> bprint(response.getBody())
  POST interface registered
  >>> response = http_call(wsgi_app(), 'POST', 'http://localhost/++rest++g/app/two')
  >>> bprint(response.getBody())
  POST interface registered

  >>> response = http_call(wsgi_app(), 'DELETE', 'http://localhost/++rest++g/app/one')
  >>> bprint(response.getBody())
  DELETE interface registered
  >>> response = http_call(wsgi_app(), 'DELETE', 'http://localhost/++rest++g/app/two')
  >>> bprint(response.getBody())
  DELETE interface registered

Todo:

* Support for OPTIONS, HEAD, other methods?

* Content-Type header is there for GET/POST, but not for PUT/DELETE...
"""

import grokcore.component as grok
from grokcore import rest, view, security, content
from zope.interface import Interface, implementer

class IFoo(Interface):
    pass

class MyApp(content.Container):
    pass

class MyContent(grok.Context):
    pass

class LayerA(rest.IRESTLayer):
    rest.restskin('a')

class LayerB(rest.IRESTLayer):
    rest.restskin('b')

class LayerC(rest.IRESTLayer):
    rest.restskin('c')

class LayerSecurity(rest.IRESTLayer):
    rest.restskin('e')

class LayerContent(rest.IRESTLayer):
    rest.restskin('f')

class LayerInterface(rest.IRESTLayer):
    rest.restskin('g')

class D(rest.IRESTLayer):
    rest.restskin('d')

class ARest(rest.REST):
    view.layer(LayerA)
    grok.context(MyApp)

    def GET(self):
        return "GET"

    def POST(self):
        return "POST"

    def PUT(self):
        return b"PUT"

    def DELETE(self):
        return b"DELETE"

class BRest(rest.REST):
    view.layer(LayerB)
    grok.context(MyApp)

    def GET(self):
        return "GET"

    def PUT(self):
        return b"PUT"

class CRest(rest.REST):
    view.layer(LayerC)
    grok.context(MyApp)

    def some_method_thats_not_in_HTTP(self):
        pass

class DRest(rest.REST):
    grok.context(MyContent)

    def GET(self):
        return "GET2"

class SecurityRest(rest.REST):
    grok.context(MyContent)
    view.layer(LayerSecurity)

    @security.require(security.Public)
    def GET(self):
        return "GET3"

    @security.require('zope.ManageContent')
    def POST(self):
        return "POST3"

    @security.require('zope.ManageContent')
    def PUT(self):
        return b"PUT3"

    @security.require('zope.ManageContent')
    def DELETE(self):
        return b"DELETE3"

class BodyTest(rest.REST):
    grok.context(MyContent)
    view.layer(LayerContent)

    def POST(self):
        return self.body

    def PUT(self):
        return self.body

@implementer(IFoo)
class MyInterfaceContent(grok.Context):
    pass

@implementer(IFoo)
class MyNoInterfaceContent(grok.Context):
    pass

class InterfaceRest(rest.REST):
    grok.context(IFoo)
    view.layer(LayerInterface)

    def GET(self):
        return "GET interface registered"

    def POST(self):
        return "POST interface registered"

    def PUT(self):
        return b"PUT interface registered"

    def DELETE(self):
        return b"DELETE interface registered"

class NoInterfaceRest(rest.REST):
    grok.context(MyNoInterfaceContent)
    view.layer(LayerInterface)

    def GET(self):
        return "GET directly registered"

    def PUT(self):
        return b"PUT directly registered"
