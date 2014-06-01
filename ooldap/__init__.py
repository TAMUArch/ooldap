import ldap


GLOBAL_GROUP = '-2147483646'
UNIVERSAL_GROUP = '-2147483640'


class Connection(object):
    def __init__(self, uri, dn, password):
        self.uri = uri
        self.dn = dn
        self.password = password
        assert uri and dn and password

    def bind(self):
        self.stream = ldap.initialize(uri)
        self.stream.simple_bind_s(self.dn, self.password)

    def unbind(self):
        self.stream.unbind_s()
