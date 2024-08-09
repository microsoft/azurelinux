#!/bin/sh
set -e
LOCALEGEN=/etc/locale-gen.conf
LOCALES=/usr/share/i18n/locales
if [ -n "$POSIXLY_CORRECT" ]; then
  unset POSIXLY_CORRECT
fi
[ -f $LOCALEGEN -a -s $LOCALEGEN ] || exit 0;
# Remove all old locale dir and locale-archive before generating new
# locale data.
rm -rf /usr/lib/locale/* || true
umask 022
is_entry_ok() {
  if [ -n "$locale" -a -n "$charset" ] ; then
    true
  else
    echo "error: Bad entry '$locale $charset'"
    false
  fi
}
echo "Generating locales..."
while read locale charset; do \
	case $locale in \#*) continue;; "") continue;; esac; \
	is_entry_ok || continue
	echo -n "  `echo $locale | sed 's/\([^.\@]*\).*/\1/'`"; \
	echo -n ".$charset"; \
	echo -n `echo $locale | sed 's/\([^\@]*\)\(\@.*\)*/\2/'`; \
	echo -n '...'; \
        if [ -f $LOCALES/$locale ]; then input=$locale; else \
        input=`echo $locale | sed 's/\([^.]*\)[^@]*\(.*\)/\1\2/'`; fi; \
	localedef -i $input -c -f $charset -A /usr/share/locale/locale.alias $locale; \
	echo ' done'; \
done < $LOCALEGEN
echo "Generation complete."