"""
Compose classes.
"""

class NoProxyException(Exception):
    pass
    
class ProxyThing(object):
    """A proxy object that delegates method calls and lookups to another object."""

    def __init__(self, klass, name, thing):
        """The class which this proxy targets, the name of the thing it proxies and the thing it proxies."""
        self.klass = klass
        self.name = name
        self.thing = thing

    def __call__(self, *args, **kwargs):

        return self.thing(*args, **kwargs)

    def __str__(self):

        return "<ProxyThing {target: %s, name: %s, thing: %s}>" % (self.klass, self.name, self.thing)
        
class Compose(object):

    def __init__(self, *targets):

        self.targets = targets

    def _setup_init(self, old_init, proxy_dict):
        def init(instance, *args, **kwargs):
            old_init(instance, *args, **kwargs)
            instance.__dict__ = self._bind_proxies(instance, proxy_dict)
        return init

    def _bind_proxies(self, instance, proxy_dict):

        new_dict = {}
        for name, thing, target in self._locate_proxy_targets(instance):
            for proxyname, proxything in proxy_dict.iteritems():
                if isinstance(proxything, ProxyThing) and proxything.klass == target:
                    new_dict[proxyname] = getattr(thing, proxyname)
        return new_dict

    def _locate_proxy_targets(self, instance):

        for name, thing in instance.__dict__.iteritems():
            for target in self.targets:
                if isinstance(thing, target):
                    yield name, thing, target

    def _build_proxy_dict(self):

        proxy_dict = {}
        for target in self.targets:
            for name, thing in target.__dict__.iteritems():
                if self._proxy_this(name, thing):
                    proxy_dict[name] = ProxyThing(target, name, thing)
        return proxy_dict
        
    def __call__(self, klass):

        proxy_dict = self._build_proxy_dict()
        proxy_dict.update(klass.__dict__)
        proxy_dict["__init__"] = self._setup_init(klass.__init__, proxy_dict)
        return type(klass.__name__ + "Composition", (klass,), proxy_dict)

    def _proxy_this(self, name, thing):
        return not name.startswith("_")
