# SSL CA certificates management

- [SSL CA certificates management](#ssl-ca-certificates-management)
  - [The `ca-certificates` package](#the-ca-certificates-package)
  - [Certificate locations](#certificate-locations)
  - [Tips and tricks](#tips-and-tricks)

## The `ca-certificates` package

This package contains the basic SSL CA certificates available to use on all images. The certificates are split into two sub packages:

- `ca-certificates-base` - package containing the minimal set of certificates required by the package management tools to authenticate the package repositories.
- `ca-certificates` - package containig a collection of Mozilla certificates listed in [Mozzila's certdata.txt file](https://hg.mozilla.org/releases/mozilla-release/file/tip/security/nss/lib/ckfw/builtins/certdata.txt). For exact version information please consult the [`ca-certificates.spec`](https://dev.azure.com/mariner-org/_git/mariner?path=%2FSPECS%2Fca-certificates%2Fca-certificates.spec). Installing this package will automatically pull in `ca-certificates-base`.

In addition to the certificates, the `ca-certificates-tools` package provides tooling for [installation of custom certificates](#custom-configuration-of-the-ca-certificates).

## Certificate locations

The directory /etc/pki/ca-trust/source/ contains CA certificates and 
trust settings in the PEM file format. The trust settings found here will be
interpreted with a high priority - higher than the ones found in 
/usr/share/pki/ca-trust-source/.

QUICK HELP: To add a certificate in the simple PEM or DER file formats to the list of CAs trusted on the system:
Copy it to the `/etc/pki/ca-trust/source/anchors/` subdirectory, and run the `update-ca-trust` command.

If your certificate is in the extended BEGIN TRUSTED file format, then place it into the main source/ directory instead.

Please refer to the [update-ca-trust(8)](https://www.systutorials.com/docs/linux/man/8-update-ca-certificates/) manual page for additional information.

## Tips and tricks

To get additional debug output when using p11-kit's `trust` or `p11-kit` commands set the `P11_KIT_DEBUG` environment variable and to not specify the `-v` parameter.

``` bash
export P11_KIT_DEBUG=all
export DEST=/etc/pki/ca-trust/extracted
sudo -E /usr/bin/p11-kit extract --format=pem-bundle --filter=ca-anchors --overwrite --comment --purpose server-auth $DEST/pem/tls-ca-bundle.pem
```