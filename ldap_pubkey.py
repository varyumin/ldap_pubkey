#!/usr/bin/python2
import sys
import os
from ldap3 import Server, Connection, ALL, NTLM

LDAP_SERVER = '10.210.17.116'
LDAP_PORT = 389
LDAP_USER = 'sberned\\ad'
LDAP_PASSWD = '1130688M@gic'
BASE_DN = 'OU=Sberned,DC=sberned,DC=lc'

search_name = sys.argv[1]

f = open('/etc/passwd', 'r')
line = f.readline()
while line:
    user = line.split(':')
    if user[6] == '/bin/bash\n':
        if user[0] == search_name:
            pub_key = os.path.expanduser('~%s' % search_name) + '/.ssh/authorized_keys'
            f = open(pub_key, 'r')
            print(f.read())
            sys.exit(0)
    line = f.readline()

server = Server(LDAP_SERVER, port=LDAP_PORT)
conn = Connection(server, user=LDAP_USER, password=LDAP_PASSWD,  authentication=NTLM)
conn.bind()

conn.search('{}'.format(BASE_DN), "(sAMAccountName={})".format(search_name), attributes=('info',))
entry = conn.entries[0]

for pubkey in entry.info.values:
    print(pubkey)
    sys.exit(0)
sys.exit(1)
