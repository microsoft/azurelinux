# Qt initialization script (sh)

# In multilib environments there is a preferred architecture, 64 bit over 32 bit in x86_64,
# ppc64. When a conflict is found between two packages corresponding with different arches,
# the installed file is the one from the preferred arch. This is very common for executables
# in /usr/bin, for example. If the file /usr/bin/foo is found  in an x86_64 package and in
# an i386 package, the executable from x86_64 will be installe

if [ -z "${QTDIR}" ]; then

case `uname -m` in
   x86_64 | ia64 | s390x | ppc64 | ppc64le)
      QT_PREFIXES="/usr/lib64/qt-3.3 /usr/lib/qt-3.3" ;;
   * )
      QT_PREFIXES="/usr/lib/qt-3.3 /usr/lib64/qt-3.3" ;;
esac

for QTDIR in ${QT_PREFIXES} ; do
  test -d "${QTDIR}" && break
done
unset QT_PREFIXES

case :$PATH: in
    *:$QTDIR/bin:*) ;;
    *) PATH=$QTDIR/bin:$PATH ;;
esac

QTINC="$QTDIR/include"
QTLIB="$QTDIR/lib"

export QTDIR QTINC QTLIB PATH

fi
