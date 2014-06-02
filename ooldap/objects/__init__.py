from logging import getLogger

import ldap

from ooldap import GLOBAL_GROUP
from ooldap.foundation import LDAPObject


log = getLogger('ooldap.objects')


class Group(LDAPObject):
    def create(self, name, scope=GLOBAL_GROUP):
        attr = {}
        attr['objectClass'] = ['group', 'top']
        attr['groupType'] = self.scope
        attr['cn'] = str(name)
        attr['name'] = str(name)
        attr['sAMAccountName'] = str(name)

        add_group = ldap.modlist.addModlist(attr)

        self.connection.bind()

        try:
            log.debug('creating group %s' % self.dn)
            self.connection.stream.add_s(self.dn, add_group)
        except ldap.ALREADY_EXISTS:
            pass
        except:
            log.exception('Error creating group %s' % self.dn)

        self.connection.unbind()

    @property
    def members(self):
        return self.get_attribute('member')

    def add_member(self, new_member):
        self.connection.bind()
        try:
            self.connection.stream.modify_s(self.dn,
                       [(ldap.MOD_ADD, 'member', str(new_member.dn))])
        except ldap.ALREADY_EXISTS:
            pass
        except:
            log.exception('Error adding %s to %s' % (new_member.dn, self.dn))
        self.connection.unbind()

    def remove_member(self, member):
        self.connection.bind()
        try:
            self.connection.stream.modify_s(self.dn,
                       [(ldap.MOD_DELETE, 'member', str(member.dn))])
        except ldap.NO_SUCH_OBJECT:
            pass
        except:
            log.exception('Error removing %s from %s' % (member.dn, self.dn))
        self.connection.unbind()
