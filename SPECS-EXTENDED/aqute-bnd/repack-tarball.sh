#!/bin/bash
VERSION=`sed -rn 's/^Version:\s*([0-9.]+)/\1/p' aqute-bnd.spec`
wget https://github.com/bndtools/bnd/archive/$VERSION.REL.tar.gz
gunzip $VERSION.REL.tar.gz
tar tf $VERSION.REL.tar | grep -E '\.(.ar|exe|tar\.(gz|bz2|xz)|zip)$' | xargs tar --delete --file $VERSION.REL.tar
gzip $VERSION.REL.tar
