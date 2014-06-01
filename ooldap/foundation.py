from logging import getLogger

import os

import ldap

from ooldap import exceptions, Connection
from ooldap.objects import Group


URI = os.environ['LDAP_CONNECTION_URI']
BIND_DN = os.environ['LDAP_CONNECTION_DN']
PASSWORD = os.environ['LDAP_CONNECTION_PASSWORD']


log = getLogger('ooldap.foundation')


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

    @propery
    def cn(self):
        return self.get_attribute('cn')

    @property
    def memberOf(self):
        return self.get_attribute('memberOf')

    @property
    def description(self):
        return self.get_attribute('description')

    def add_to_group(self, group):
        group.add_member(self)

    def remove_from_group(self, group):
        group.remove_member(self)
