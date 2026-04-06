# Qt initialization script (csh)

# In multilib environments there is a preferred architecture, 64 bit over 32 bit in x86_64,
# ppc64. When a conflict is found between two packages corresponding with different arches,
# the installed file is the one from the preferred arch. This is very common for executables
# in /usr/bin, for example. If the file /usr/bin/foo is found  in an x86_64 package and in
# an i386 package, the executable from x86_64 will be installe

if ( $?QTDIR ) then
   exit
endif

switch (`uname -m`)
   case x86_64:
   case ia64:
   case s390x:
   case ppc64:
   case ppc64le:
      set QTPREFIXES = "/usr/lib64/qt-3.3 /usr/lib/qt-3.3"
      breaksw
   case *:
      set QTPREFIXES = "/usr/lib/qt-3.3 /usr/lib64/qt-3.3"
endsw

foreach QTPREFIX ( $QTPREFIXES )
  test -d "$QTPREFIX" && setenv QTDIR $QTPREFIX && break
end
unset QTPREFIX QTPREFIXES

if ( "${path}" !~ *$QTDIR/bin* ) then
   set path = ( $QTDIR/bin $path )
endif

setenv QTINC $QTDIR/include
setenv QTLIB $QTDIR/lib
