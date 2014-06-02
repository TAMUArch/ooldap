import ldap

from ooldap import GLOBAL_GROUP
from ooldap.foundation import LDAPObject


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
        self.connection.stream.add_s(self.dn, add_group)
        self.connection.unbind()

    @property
    def members(self):
        return self.get_attribute('member')

    def add_member(self, new_member):
        assert isinstance(new_member, LDAPObject)
        self.connection.bind()
        self.connection.stream.modify_s(self.dn,
                    [(ldap.MOD_ADD, 'member', str(new_member.dn))])
        self.connection.unbind()

    def remove_member(self, member):
        self.connection.bind()
        self.connection.stream.modify_s(self.dn,
                    [(ldap.MOD_DELETE, 'member', str(member.dn))])
        self.connection.unbind()
