from logging import getLogger

import os

import ldap

from ooldap import exceptions


URI = os.environ['LDAP_CONNECTION_URI']
DN = os.environ['LDAP_CONNECTION_DN']
PASSWORD = os.environ['LDAP_CONNECTION_PASSWORD']


log = getLogger('ooldap.objects')


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
        self.connection.unbind_s()


class LDAPObject(object):
    connection = Connection(URI, DN, PASSWORD)

    def __init__(self, cn, ou):
        self.cn = cn
        self.ou = ou

    @property
    def data(self):
        self.connection.bind()
        result_id = self.connection.stream.search(self.ou,
                                                  ldap.SCOPE_SUBTREE,
                                                  'cn=%s' % self.cn,
                                                  None)
        type, data = self.connection.stream.result(result_id, 10)
        self.connection.unbind()
        if len(data) == 0:
            log.error('%s not found in ldap' % self.cn)
            raise exceptions.ObjectNotFound
        if len(data) > 1:
            log.error('%s found multiple users in ldap' % self.cn)
            raise exceptions.MultipleObjectsFound
        return data[0][1]

    @property
    def dn(self):
        if not self.data:
            return None
        if 'distinguishedName' not in self.data:
            return None
        return self.data['distinguishedName'][0]

    @property
    def memberOf(self):
        data = self.data()
        if not data:
            return []
        if 'memberOf' not in data:
            return []
        return data['memberOf']


class Group(LDAPObject):
    @property
    def members(self):
        data = self.data()
        if not data:
            return []
        if 'members' not in data:
            return []
        return data['members']


class User(LDAPObject):
    @property
    def 
