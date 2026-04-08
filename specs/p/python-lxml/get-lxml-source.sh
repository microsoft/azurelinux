#! /bin/bash -ex

# Download a release of lxml (if missing) and remove the isoschematron module from it

version=$1

if [ -z "${version}" ]; then
    echo "Usage: $0 VERSION" >& 2
    echo "" >& 2
    echo "example: $0 4.9.2" >& 2
    exit 1
fi

versionedname=lxml-${version}
orig_archive=${versionedname}.tar.gz
new_archive=${versionedname}-no-isoschematron-rng.tar.gz

if [ ! -e ${orig_archive} ]; then
    wget -N https://files.pythonhosted.org/packages/source/l/lxml/${orig_archive}
fi

deleted_directory=lxml-${version}/src/lxml/isoschematron/resources/rng

# tar --delete does not operate on compressed archives, so do
# gz decompression explicitly
gzip --decompress ${orig_archive}
tar -v --delete -f ${orig_archive//.gz} ${deleted_directory}
gzip -cf ${orig_archive//.gz} > ${new_archive}
