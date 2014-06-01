from ooldap.foundation import LDAPObject


class Group(LDAPObject):
    @property
    def members(self):
        data = self.data()
        if not data:
            return []
        if 'members' not in data:
            return []
        return data['members']
