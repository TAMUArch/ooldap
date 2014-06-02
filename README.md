Using the python-ldap library: http://www.python-ldap.org/


Provides the foundation for manipulating ldap
taking a highly object oriented approach.


Use the provided object types, override them, or create your own.


Add the three following environmental variables:

- LDAP_CONNECTION_URI
- LDAP_CONNECTION_DN
- LDAP_CONNECTION_PASSWORD


Here is an example:

```python
import os


os.environ['LDAP_CONNECTION_URI'] = 'example.com'
os.environ['LDAP_CONNECTION_DN'] = 'CN=<username>,OU=People,DC=EXAMPLE,DC=COM'
os.environ['LDAP_CONNECTION_PASSWORD'] = '<password>'


from ooldap.foundation import LDAPObject


ldapobject = LDAPObject('CN=johndoe,OU=People,DC=EXAMPLE,DC=COM')

ldapobject.data
ldapobject.description
ldapobject.get_attribute('mail')
```
