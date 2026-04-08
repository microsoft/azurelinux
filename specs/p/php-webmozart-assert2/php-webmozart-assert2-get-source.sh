#/bin/sh

GIT=`which git`
RPM=`which rpm`

if [ -z "$GIT" ]
then
    echo "ERROR: 'git' command not found" 1>&2
    exit 1
elif [ -z "$RPM" ]
then
    echo "ERROR: 'rpm' command not found" 1>&2
    exit 1
fi

function print {
    echo -e "\e[0;33m>>>>> ${1}\e[0m"
}

if [ -x "$1" ]
then
    SPEC=$1
else
    SPEC=`ls *.spec | head -1`
fi

SPEC_DIR=`pwd`

print "SPEC_DIR = $SPEC_DIR"

NAME=`echo $SPEC | sed 's#\.spec##'`
VERSION=`egrep '%global\s*github_version' $SPEC | awk '{print $3}'`

print "SPEC = $SPEC"
print "NAME = $NAME"

GIT_OWNER=`egrep '%global\s*github_owner' $SPEC | awk '{print $3}'`
GIT_NAME=`egrep '%global\s*github_name' $SPEC | awk '{print $3}'`
GIT_COMMIT=`egrep '%global\s*github_commit' $SPEC | awk '{print $3}'`
GIT_REPO=https://github.com/${GIT_OWNER}/${GIT_NAME}
GIT_DIR=`echo $GIT_REPO | sed 's#.*/##'`

print "GIT_OWNER = $GIT_OWNER"
print "GIT_NAME = $GIT_NAME"
print "GIT_COMMIT = $GIT_COMMIT"
print "GIT_REPO = $GIT_REPO"
print "GIT_DIR = $GIT_DIR"

TEMP_DIR=$(mktemp --dir)

pushd $TEMP_DIR
    print "Cloning git repo..."
    $GIT clone $GIT_REPO

    pushd $GIT_DIR
        print "Checking out commit..."
        $GIT checkout $GIT_COMMIT || exit 1
        cp composer.json ${SPEC_DIR}
    popd

    TAR_DIR=${GIT_NAME}-${GIT_COMMIT}
    print "TAR_DIR = $TAR_DIR"

    mv $GIT_DIR $TAR_DIR

    TAR_FILE=${SPEC_DIR}/${NAME}-${VERSION}-${GIT_COMMIT:0:7}.tar.gz
    print "TAR_FILE = $TAR_FILE"

    [ -e $TAR_FILE ] && rm -f $TAR_FILE
    tar --exclude-vcs -czf $TAR_FILE $TAR_DIR
    chmod 0644 $TAR_FILE
popd

rm -rf $TEMP_DIR
