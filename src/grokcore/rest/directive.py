import martian
from grokcore.view.directive import TaggedValueStoreOnce


class restskin(martian.Directive):
    """The `grok.restskin()` directive.

    This directive is placed inside of `grok.IRESTLayer` subclasses to
    indicate what their layer name will be within a REST URL.  Giving
    the skin ``grok.restskin('b')``, for example, will enable URLs that
    look something like `http://localhost/++rest++b/app`.

    """
    # We cannot do any better than to check for a class scope. Ideally we
    # would've checked whether the context is indeed an Interface class.
    scope = martian.CLASS
    store = TaggedValueStoreOnce()
    validate = martian.validateText

    def factory(self, value=None):
        return value
