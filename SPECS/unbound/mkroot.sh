#!/bin/sh

SOURCE="/usr/share/dns-root-data/root.key"
DEST="${1:-root.key}"

mk_key() {
echo "# Generated from $SOURCE"
echo "# Use /var/lib/unbound/root.key instead."
echo "trusted-keys {"
while read DOMAIN CLS TYPE FLAGS PROTO ALG KEYDATA COMMENT KEYTAG; do
echo "$DOMAIN $CLS $TYPE $FLAGS $PROTO $ALG \"$KEYDATA\" # $KEYTAG"
done < "$SOURCE"
echo "};"
}

mk_key > "$DEST"
touch -r "$SOURCE" "$DEST"
