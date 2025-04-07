socat tunnel for encrypted rsync SST
====================================

`wsrep_sst_rsync_tunnel` is an extension of the rsync-based [SST](http://galeracluster.com/documentation-webpages/glossary.html#term-state-snapshot-transfer)
implementation that ships with mariadb. Its purpose is to encrypt
communication between the donor and the joiner during an SST.

Encryption is implemented by means of a socat tunnel, using OPENSSL
addresses. It can be configured via the regular openssl flags exposed
by socat.


## How to configure the script

This SST script can configured by setting a few keys in your favorite
mariadb option file in addition to the usual galera settings.

    [mysqld]
    ...
    bind_address=<node-name>
    wsrep_sst_method=rsync_tunnel
    ...
    
    [sst]
    tca=/path/to/your/ca-file.crt
    tcert=/path/to/node/certificate.crt
    tkey=/path/to/node/key.key
    sockopt=<openssl-address-options-as-per-socat-manual>

When a joiner node requests an SST, `wsrep_sst_rsync_tunnel` uses
socat to listen to incoming SSL connections on port 4444 in lieu of
the original rsync daemon. Received data will be forwarded to the
rscynd daemon started locally to replicate the database.

When a donor node serves the SST, `wsrep_sst_rsync_tunnel` makes
a series of rsync calls that target a locally started socat daemon.
The daemon tunnels all rsync traffic into an encrypted SSL connection
that targets the joiner's end of the socat tunnel.

Encryption parameters are specified under the `[sst]` group in the
mariadb option file, where `tkey` and `tcert` are respectively the key
and the certificate that are used by both sides of the socat tunnel.
Each node typically has a different key and cert. Both key and
certificate can be combined into a single PEM file and referenced by
`tcert`. Option `tca` holds a list of the trusted signing
certificates.

In case you need to tweak the creation of the SSL connection, you can
pass valid socat options (as per socat manual) via the `sockopt` key.
For debugging purpose, the exact socat command that is being executed
shows up in the mariadb log file.

Note that socat verifies that the certificate's commonName matches
that of the host that is being targeted. The target name comes from
the value configured in `bind_address`, so it's important that it
matches the certificate's commonName. An IP address can be used for
`bind_address`, but you may get into trouble in case different
hostnames resolve to the same IP (e.g. multiple networks per host).


## Examples of use

Suppose you're running a 3-node galera cluster
`node1.my.cluster`, `node2.my.cluster`, `node3.my.cluster`.

### Scenario: using self-signed certificates

On each node, create a key and a certificate, and bundle them into a
single PEM file. For instance on `node1.my.cluster`:

    openssl genrsa -out /tls/mysql-$(hostname -f).key 2048
    openssl req -new -key /tls/mysql-$(hostname -f).key -x509 -days 365000 -subj "/CN=$(hostname -f)" -out /tls/mysql-$(hostname -f).crt -batch
    cat /tls/mysql-$(hostname -f).key /tls/mysql-$(hostname -f).crt > /tls/mysql.pem

Then, on each node, create a cafile that will contain all the certs to
trust:

    for n in node1.my.cluster node2.my.cluster node3.my.cluster; do
       ssh $n 'cat /tls/mysql-$(hostname -f).crt' >> /tls/all-mysql.crt
    done

Once you have those two files on each host, you can configure the SST
appropriately. For instance from `/etc/my.cnf.d/galera.cnf`:

    [mysqld]
    ...
    
    [sst]
    tca=/tls/all-mysql.crt
    tcert=/tls/mysql.pem

### Scenario: using self-signed certificates, without verification

By default, when socat tries to establish a SSL connection to a peer,
it also verifies that it can trust the peer's certificate. If for some
reason you need to disable that feature, you can amend the previous
configuration with a sockopt option:

    [mysqld]
    ...
    
    [sst]
    tca=/tls/all-mysql.crt
    tcert=/tls/mysql.pem
    sockopt="verify=0"

The associated sockopt value is passed to socat when
the donor or the joiner configures his part of the tunnel.

Note: please do not do so in production, this is inherently insecure
as you will not verify the identity of the peer you're connecting to!

### Scenario: using certificates from a CA

Suppose you have a FreeIPA service which generated a key file and a
certificate file for the three galera nodes, respectively located at
/tls/mysql.key and /tls/mysql.crt.

Assuming that the certificate for the FreeIPA server is available at
/etc/ipa/ca.crt, you can configure you galera servers as follows:

    [sst]
    tca=/etc/ipa/ca.crt
    tcert=/tls/mysql.crt
    tkey=/tls/mysql.key

## License

Copyright © 2017 [Damien Ciabrini](https://github.com/dciabrin).
This work is derived from the original `wsrep_rsync_sst`, copyright
© 2010-2014 [Codership Oy](https://github.com/codership).
Released under the GNU GPLv2.
