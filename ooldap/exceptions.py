from logging import getLogger


log = getLogger('ooldap.exceptions')


class ObjectNotFound(Exception):
    log.error('object not found in ldap' % self.dn)
    pass


class MultipleObjectsFound(Exception):
    log.error('found multiple objects in ldap' % self.dn)
    pass
