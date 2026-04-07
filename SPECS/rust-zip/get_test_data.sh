#!/bin/sh
set -o nounset
set -o errexit

FORGEURL='https://github.com/zip-rs/zip2'

# These are test data files that have been audited for obvious issues. What
# kind of issues might there be?
#
# - Acceptable license, but no license text
# - No known license / presumed or explicitly proprietary
# - Mysterious precompiled binaries
#
# Files we have determined we should *not* include:
#
# - chinese.zip:
#   The single text file it contains, 七个房间.txt, contains a significant
#   amount of narrative text in GB2312 encoding: some kind of story, or an
#   excerpt from one, perhaps a work of fiction. It’s not clear what the origin
#   is or what license, if any, might apply.
# - lin-ub_iwd-v11.zip:
#   LICENSE.lin-ub_iwd-v11.zip.txt clearly shows that this is at *best* not
#   under a license acceptable in Fedora.
# - omni.ja:
#   This is a Firefox application resource bundle,
#   https://udn.realityripple.com/docs/Mozilla/About_omni.ja_(formerly_omni.jar).
#   It is very likely that everything in it is properly licensed for Fedora,
#   but it is complex to audit, and we would rather not do all that work to
#   confirm it’s OK when the alternative is just disabling a single test.
# - pandoc_soft_links.zip:
#   Contains a copy of pandoc 3.2 compiled for aarch64: pandoc itself is
#   open-source, but who can say what was linked into it? The complete list of
#   applicable licenses is not knowable.
OK_FILES="$(grep -vE '^(#|$)' <<EOF
# Contents are trivial: symlinks, zero-bytes files, sample text files
# containing only a few words, etc.
#
# From the source for the applicable tests, the password is "helloworld":
aes_archive.zip
comment_garbage.zip
data_descriptor.zip
extended_timestamp.zip
extended_timestamp_bad.zip
files_and_dirs.zip
linux-7z.zip
mimetype.zip
misaligned_comment.zip
non_utf8.zip
ntfs.zip
ppmd.zip
symlink.zip
windows-7zip.zip
xz.zip
zip64_demo.zip
zip64_magic_in_filename_1.zip
zip64_magic_in_filename_2.zip
zip64_magic_in_filename_4.zip
zip64_magic_in_filename_5.zip

# These are derived from the Project Gutenberg text of Shakespeare’s Hamlet,
# https://www.gutenberg.org/cache/epub/1524/pg1524.txt. Both the play and the
# print edition upon which the text is based are old enough to be unprotected
# by copyright in the US, and probably worldwide. Fedora Legal has determined
# that the “Project Gutenberg License” is “not a license” and content that is
# actually in the public domain can be treated as such,
# https://gitlab.com/fedora/legal/fedora-license-data/-/issues/676.
legacy/implode_hamlet_2048.out
legacy/implode_hamlet_256.bin
legacy/implode_hamlet_256.out
legacy/implode.zip
legacy/reduce_hamlet_2048.bin
legacy/reduce_zero_reduced.bin
legacy/reduce.zip
legacy/shrink.zip

# The interesting part here is the file binary.wmv, which is a bit over a
# minute of spoken-word audio from some kind of talk or lecture. Upstream
# claims (via folder/LICENSE.binary.wmv.txt) that the license is MIT. The text
# file first.txt is taken from Project Gutenberg text of Shakespeare’s Hamlet,
# discussed above.
deflate64.zip
folder/LICENSE.binary.wmv.txt
folder/binary.wmv
folder/first.txt
lzma.zip

# These don’t unzip with the "unzip" tool or the "7z" tool, so they are
# difficult to audit, but their sizes are only from a few dozen to a few
# hundred bytes, so we assume their contents are very likely to be
# unproblematic.
#
deflate64_issue_25.zip
ignore_encryption_flag.zip
invalid_cde_number_of_files_allocation_greater_offset.zip
invalid_cde_number_of_files_allocation_smaller_offset.zip
invalid_offset.zip
invalid_offset2.zip
raw_deflate64_index_out_of_bounds.zip
zip64_magic_in_filename_3.zip
EOF
)"


print_help()
{
	cat <<EOF
Usage: $1 VERSION

Generate a copy of the GitHub source archive for zip-rs/zip2, with everything
but the test/data/ subdirectory removed, and additionally, in which only test
data files that have been audited for obvious license issues are included.  The
result will be named zip2-\${VERSION}-filtered.tar.gz and will be written into
the current working directory.
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
SOURCE0="${FORGEURL}/archive/v${VERSION}/zip2-${VERSION}.tar.gz"
TARNAME="$(basename "${SOURCE0}")"
TARDIR="$(basename "${SOURCE0}" '.tar.gz')"
NEWTAR="${TARDIR}-filtered.tar.gz"

SAVEDIR="${PWD}"
XDIR="$(mktemp -d)"
trap "rm -rf '${XDIR}'" INT TERM EXIT

cd "${XDIR}"
curl -L -O "${SOURCE0}"
tar -xzf "${TARNAME}"
MTIME="$(stat -c '%Y' "${TARDIR}")"
# Remove everything but tests/data
find "${TARDIR}" -mindepth 1 -maxdepth 1 ! -name tests -execdir rm -r '{}' '+'
find "${TARDIR}/tests" -mindepth 1 -maxdepth 1 ! -name data \
    -execdir rm -r '{}' '+'
# Empty tests/data (keeping the files in a duplicate tree), then move the files
# we want back in.
cp -lrp "${TARDIR}/tests/data" data_unfiltered
find "${TARDIR}/tests/data" -type f -delete
echo "${OK_FILES}" | while read -r fn
do
  mkdir -p "${TARDIR}/tests/data/$(dirname "${fn}")"
  mv "data_unfiltered/${fn}" "${TARDIR}/tests/data/${fn}"
done
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
  gzip -9 > "${NEWTAR}"
touch -d @"${MTIME}" "${NEWTAR}"

cd "${SAVEDIR}"
mv -v "${XDIR}/${NEWTAR}" .
