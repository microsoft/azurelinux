#!/bin/sh
set -o nounset
set -o errexit

FORGEURL='https://github.com/pdfminer/pdfminer.six'

print_help()
{
	cat <<EOF
Usage: $1 VERSION

Generate a source archive for pdfminer.six with questionably-licensed sample
PDFs removed. The result will be named pdfminer.six-\${VERSION}-filtered.tar.zst
and will be written into the current working directory.
EOF
}

if [ "$#" != '1' ]
then
	exec 1>&2
	print_help "${0}"
	exit 1
elif [ "${1-}" = '-h' ] || [ "${1-}" = '--help' ]
then
	print_help "${0}"
	exit 0
fi

VERSION="${1}"
SOURCE0="${FORGEURL}/archive/${VERSION}/pdfminer.six-${VERSION}.tar.gz"
TARNAME="$(basename "${SOURCE0}")"
TARDIR="$(basename "${SOURCE0}" '.tar.gz')"
NEWTAR="${TARDIR}-filtered.tar.zst"

SAVEDIR="${PWD}"
XDIR="$(mktemp -d)"
trap "rm -rvf '${XDIR}'" INT TERM EXIT

cd "${XDIR}"
curl -L -O "${SOURCE0}"
tar -xzvf "${TARNAME}"
MTIME="$(stat -c '%Y' "${TARDIR}")"
rm -rvf "${TARDIR}/samples"
if [ "$(find . -type d -name 'nonfree' | wc -l)" != '0' ]
then
	echo 'ERROR: did not properly remove problematic content' 1>&2
	exit 1
fi
# https://www.gnu.org/software/tar/manual/html_section/Reproducibility.html
# We reset all mtimes to that of the top-level extracted directory; since git
# archives don’t have meaningful per-file mtimes, nothing useful is lost.
TZ=UTC LC_ALL=C tar \
    --create --verbose \
    --sort=name \
    --format=posix \
    --numeric-owner --owner=0 --group=0 \
    --mode=go+u,go-w \
    --pax-option='delete=atime,delete=ctime' \
    --clamp-mtime --mtime="@${MTIME}" \
    "${TARDIR}/" |
  zstdmt --ultra -22 > "${NEWTAR}"
touch -d @"${MTIME}" "${NEWTAR}"

cd "${SAVEDIR}"
mv -v "${XDIR}/${NEWTAR}" .
