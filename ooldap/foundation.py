from logging import getLogger

import os

import ldap

from ooldap import exceptions, Connection


URI = os.environ['LDAP_CONNECTION_URI']
BIND_DN = os.environ['LDAP_CONNECTION_DN']
PASSWORD = os.environ['LDAP_CONNECTION_PASSWORD']


log = getLogger('ooldap.objects')


class LDAPObject(object):
    connection = Connection(URI, BIND_DN, PASSWORD)

    def __init__(self, dn):
        self.dn = dn
        assert dn

    @property
    def data(self):
        self.connection.bind()
        result_id = self.connection.stream.search(self.dn,
                                                  ldap.SCOPE_BASE,
                                                  '(&)',
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
    def memberOf(self):
        if not self.data:
            return []
        if 'memberOf' not in self.data:
            return []
        return self.data['memberOf']
