from logging import getLogger

import os

import ldap

from ooldap import exceptions, Connection


URI = os.environ['LDAP_CONNECTION_URI']
BIND_DN = os.environ['LDAP_CONNECTION_DN']
PASSWORD = os.environ['LDAP_CONNECTION_PASSWORD']


log = getLogger('ooldap.foundation')


class LDAPObject(object):

    def __init__(self, dn, uri=URI, bind_dn=BIND_DN, password=PASSWORD):
        self.dn = dn
        assert dn
        self.connection = Connection(uri, bind_dn, password)

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
            log.error('%s not found in ldap' % self.dn)
            raise exceptions.ObjectNotFound
        if len(data) > 1:
            log.error('%s found multiple users in ldap' % self.dn)
            raise exceptions.MultipleObjectsFound
        return data[0][1]

    def get_attribute(self, attribute):
        if not self.data:
            return None
        if attribute not in self.data:
            return None

        attribute = self.data[attribute]
        if len(attribute) == 1:
            return attribute[0]

        return attribute

    @property
    def cn(self):
        return self.get_attribute('cn')

    @property
    def memberOf(self):
        return self.get_attribute('memberOf')

    @property
    def description(self):
        return self.get_attribute('description')
