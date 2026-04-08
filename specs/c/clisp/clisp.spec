# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Upstream has not made a new release since 2010
%global srcname clisp
%global commit  f66220939ea7d36fd085384afa4a0ec44597d499
%global date    20250504
%global forgeurl https://gitlab.com/gnu-clisp/clisp

# There is a plus on the end for unreleased versions, not for released versions
%global instdir %{name}-%{version}+

# This package uses toplevel ASMs which are incompatible with LTO
%global _lto_cflags %{nil}

%bcond gtk2 %[!(0%{?rhel} > 9)]

Name:		clisp
Summary:	ANSI Common Lisp implementation
Version:	2.49.95

%forgemeta

# The project as a whole is GPL-2.0-or-later.  Exceptions:
# - Some documentation is dual-licensed as GPL-2.0-or-later OR GFDL-1.2-or-later
# - src/gllib is LGPL-2.1-or-later
# - src/socket.d and modules/clx/mit-clx/doc.lisp are HPND
# - src/xthread.d and modules/asdf/asdf.lisp are X11
License:	GPL-2.0-or-later AND (GPL-2.0-or-later OR GFDL-1.2-or-later) AND LGPL-2.1-or-later AND HPND AND X11
Release:	5%{?dist}
URL:		http://www.clisp.org/
VCS:		git:%{forgeurl}.git
Source0:	%{forgesource}
# Upstream dropped this file from the distribution
Source1:	https://gitlab.com/sam-s/clhs/-/raw/master/clhs.el
# Updated translations
Source2:	http://translationproject.org/latest/clisp/sv.po
Source3:	http://translationproject.org/latest/clisp/de.po
# https://sourceforge.net/p/clisp/patches/32/
Patch0:		%{name}-format.patch
# The combination of register and volatile is nonsensical
Patch1:		%{name}-register-volatile.patch
# A test that writes to /dev/pts/0 succeeds or fails apparently at random.
# I can only guess that /dev/pts/0 may or may not be what the test expects.
# Perhaps we are racing with something else that allocates a pty.  Disable
# the test for now.
Patch2:		%{name}-pts-access.patch
# Do not call the deprecated siginterrupt function
Patch3:		%{name}-siginterrupt.patch
# Fix an iconv leak in stream.d
Patch4:		%{name}-iconv-close.patch
# Fix a memory leak in encoding.d
# https://gitlab.com/gnu-clisp/clisp/-/merge_requests/11
Patch5:		%{name}-encoding-leak.patch
# Fix undefined behavior in SORT
Patch6:		%{name}-undefined-behavior-sort.patch
# Fix undefined behavior in interpret_bytecode_
Patch7:		%{name}-undefined-behavior-eval.patch
# Fix undefined behavior in pr_array
Patch8:		%{name}-undefined-behavior-io.patch
# Fix misaligned memory accesses on ppc64le
Patch9:		%{name}-ppc64le-alignment.patch
# Fix some mismatched readline function declarations
# https://gitlab.com/gnu-clisp/clisp/-/merge_requests/13
Patch10:	%{name}-readline.patch

# Work around a problem inlining a function on ppc64le
# See https://bugzilla.redhat.com/show_bug.cgi?id=2049371
Patch100:	%{name}-no-inline.patch

BuildRequires:	dbus-devel
BuildRequires:	diffutils
BuildRequires:	emacs
BuildRequires:	fcgi-devel
BuildRequires:	ffcall-devel
BuildRequires:	gcc
BuildRequires:	gdbm-devel
BuildRequires:	gettext-devel
BuildRequires:	ghostscript
BuildRequires:	glibc-langpack-en
BuildRequires:	glibc-langpack-fr
BuildRequires:	glibc-langpack-ja
BuildRequires:	glibc-langpack-zh
BuildRequires:	groff
%if %{with gtk2}
BuildRequires:	gtk2-devel
BuildRequires:	libglade2-devel
%endif
BuildRequires:	libXaw-devel
BuildRequires:	libXft-devel
BuildRequires:	libdb-devel
BuildRequires:	libsigsegv-devel
BuildRequires:	libsvm-devel
BuildRequires:	libunistring-devel
BuildRequires:	libxcrypt-devel
BuildRequires:	make
BuildRequires:	pari-devel
BuildRequires:	pari-gp
BuildRequires:	libpq-devel
BuildRequires:	readline-devel
BuildRequires:	vim-filesystem
BuildRequires:	zlib-devel

Requires:	emacs-filesystem
Requires:	vim-filesystem

# clisp contains a copy of gnulib, which has been granted a bundling exception:
# https://fedoraproject.org/wiki/Packaging:No_Bundled_Libraries#Packages_granted_exceptions
Provides:	bundled(gnulib)

%description
ANSI Common Lisp is a high-level, general-purpose programming language.  GNU
CLISP is a Common Lisp implementation by Bruno Haible of Karlsruhe University
and Michael Stoll of Munich University, both in Germany.  It mostly supports
the Lisp described in the ANSI Common Lisp standard.  It runs on most Unix
workstations (GNU/Linux, FreeBSD, NetBSD, OpenBSD, Solaris, Tru64, HP-UX,
BeOS, NeXTstep, IRIX, AIX and others) and on other systems (Windows NT/2000/XP,
Windows 95/98/ME) and needs only 4 MiB of RAM.

It is Free Software and may be distributed under the terms of GNU GPL, while
it is possible to distribute commercial proprietary applications compiled with
GNU CLISP.

The user interface comes in English, German, French, Spanish, Dutch, Russian
and Danish, and can be changed at run time.  GNU CLISP includes an
interpreter, a compiler, a debugger, CLOS, MOP, a foreign language interface,
sockets, i18n, fast bignums and more.  An X11 interface is available through
CLX, Garnet, CLUE/CLIO.  GNU CLISP runs Maxima, ACL2 and many other Common
Lisp packages.


%package devel
Summary:	Development files for CLISP
Provides:	%{name}-static = %{version}-%{release} 
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	libsigsegv-devel%{?_isa}

%description devel
Files necessary for linking CLISP programs.


%prep
%forgesetup
%autopatch -M99 -p0
%ifarch %{power64}
%autopatch 100 -p0
%endif

%conf
cp -p %{SOURCE1} emacs
cp -p %{SOURCE2} %{SOURCE3} src/po

# We only link against libraries in system directories, so we need -L dir in
# place of -Wl,-rpath -Wl,dir
cp -p src/build-aux/config.rpath config.rpath.orig
sed -i -e 's/${wl}-rpath ${wl}/-L/g' src/build-aux/config.rpath

# Do not use -Werror, or we get build failures on every new gcc version
sed -i '/CFLAGS -Werror/d' modules/berkeley-db/configure

# Do not override our choice of optimization flags
sed -i "/CFLAGS/s/'-O'/''/;/Z_XCFLAGS/s/' -O'//" src/makemake.in

# When building modules, put -Wl,--as-needed before the libraries to link
sed -i "s/CC='\${CC}'/CC='\${CC} -Wl,--as-needed'/" src/makemake.in

# Enable firefox to be the default browser for displaying documentation
sed -i 's/;; \((setq \*browser\* .*)\)/\1/' src/cfgunix.lisp

# Unpack the CLX manual
tar -C modules/clx -xzf modules/clx/clx-manual.tar.gz
chmod -R go+r modules/clx/clx-manual
chmod a-x modules/clx/clx-manual/html/doc-index.cgi

# On some koji builders, something is already listening on port 9090, which
# causes a spurious test failure.  Change to port 9096 for the test.
sed -i 's/9090/9096/g' tests/socket.tst

%build
# Do not need to specify base modules: i18n, readline, regexp, syscalls.
# The dirkey module currently can only be built on Windows/Cygwin/MinGW.
# The editor module is not in good enough shape to use.
# The matlab, netica, and oracle modules require proprietary code to build.
# The queens module is intended as an example only, not for actual use.
./configure --prefix=%{_prefix} \
	    --libdir=%{_libdir} \
	    --mandir=%{_mandir} \
	    --infodir=%{_infodir} \
	    --docdir=%{_pkgdocdir} \
	    --fsstnd=redhat \
	    --with-module=asdf \
	    --with-module=berkeley-db \
	    --with-module=bindings/glibc \
	    --with-module=clx/new-clx \
	    --with-module=dbus \
	    --with-module=fastcgi \
	    --with-module=gdbm \
%if %{with gtk2}
	    --with-module=gtk2 \
%endif
	    --with-module=libsvm \
	    --with-module=pari \
	    --with-module=postgresql \
	    --with-module=rawsock \
	    --with-module=zlib \
	    --with-libreadline-prefix=$PWD/readline \
	    --with-ffcall \
	    --config \
	    build \
	    CPPFLAGS='-I/usr/include/libsvm' \
	    CFLAGS='%{build_cflags} -Wa,--noexecstack' \
	    LDFLAGS='-Wl,--as-needed -Wl,-z,relro -Wl,-z,noexecstack'

cd build
# Workaround libtool reordering -Wl,--as-needed after all the libraries.
sed -i 's|CC="\(.*g..\)"|CC="\1 -Wl,--as-needed"|' libtool
make
cd -

%install
make -C build DESTDIR=%{buildroot} install
cp -a build/full %{buildroot}%{_libdir}/%{instdir}
rm -f %{buildroot}%{_pkgdocdir}/doc/clisp.{dvi,1,ps}
rm -f %{buildroot}%{_pkgdocdir}/{COPYRIGHT,GNU-GPL}
cp -p doc/mop-spec.pdf %{buildroot}%{_pkgdocdir}/doc
cp -p doc/*.png %{buildroot}%{_pkgdocdir}/doc
cp -p doc/Why-CLISP* %{buildroot}%{_pkgdocdir}/doc
cp -p doc/regexp.html %{buildroot}%{_pkgdocdir}/doc
find %{buildroot}%{_libdir} -name '*.dvi' -exec rm -f {} \+
%find_lang %{name}
%find_lang %{name}low
cat %{name}low.lang >> %{name}.lang

# Compile the Emacs interface
pushd %{buildroot}%{_emacs_sitelispdir}
%{_emacs_bytecompile} *.el
popd

# Put back the original config.rpath
cp -p config.rpath.orig %{buildroot}%{_libdir}/%{instdir}/build-aux/config.rpath

# Fix a missing executable bit
chmod a+x %{buildroot}%{_libdir}/%{instdir}/build-aux/depcomp

# Fix paths in the Makefiles
for mk in $(find %{buildroot}%{_libdir} -name Makefile); do
  sed -e "s,$PWD/modules,%{_libdir}/%{instdir}," \
      -e "s,$PWD/build/clisp,%{_bindir}/clisp," \
      -e "s,$PWD/build/linkkit,%{_libdir}/%{instdir}/linkkit," \
      -i $mk
done
for mk in %{buildroot}%{_libdir}/%{instdir}/{base,full}/makevars; do
  sed -e "s, -I$PWD[^']*,," \
      -e "s,%{_libdir}/lib\([[:alnum:]]*\)\.so,-l\1,g" \
      -i $mk
done

# Install config.h, which is needed in some cases
for dir in %{buildroot}%{_libdir}/%{instdir}/*; do
  cp -p build/$(basename $dir)/config.h $dir || :
done
cp -p build/config.h %{buildroot}%{_libdir}/%{instdir}
cp -p build/clx/new-clx/config.h \
   %{buildroot}%{_libdir}/%{instdir}/clx/new-clx

# Fix broken symlinks in the full set
pushd %{buildroot}%{_libdir}/%{instdir}/full
for obj in calls gettext readline regexi; do
  rm -f ${obj}.o
  ln -s ../base/${obj}.o ${obj}.o
done
for obj in libgnu libnoreadline lisp; do
  rm -f ${obj}.a
  ln -s ../base/${obj}.a ${obj}.a
done
for obj in fastcgi fastcgi_wrappers; do
  rm -f ${obj}.o
  ln -s ../fastcgi/${obj}.o ${obj}.o
done
for obj in cpari pari; do
  rm -f ${obj}.o
  ln -s ../pari/${obj}.o ${obj}.o
done
rm -f bdb.o
ln -s ../berkeley-db/bdb.o bdb.o
rm -f clx.o
ln -s ../clx/new-clx/clx.o clx.o
rm -f dbus.o
ln -s ../dbus/dbus.o dbus.o
rm -f gdbm.o
ln -s ../gdbm/gdbm.o gdbm.o
%if %{with gtk2}
rm -f gtk.o
ln -s ../gtk2/gtk.o gtk.o
%endif
rm -f libsvm.o
ln -s ../libsvm/libsvm.o libsvm.o
rm -f linux.o
ln -s ../bindings/glibc/linux.o linux.o
rm -f postgresql.o
ln -s ../postgresql/postgresql.o postgresql.o
rm -f rawsock.o
ln -s ../rawsock/rawsock.o rawsock.o
rm -f zlib.o
ln -s ../zlib/zlib.o zlib.o
popd

# Help the debuginfo generator
ln -s ../../src/modules.c build/base/modules.c
ln -s ../../src/modules.c build/full/modules.c

%check
make -C build check
make -C build extracheck
make -C build base-mod-check

%files -f %{name}.lang
%license COPYRIGHT GNU-GPL
%{_bindir}/clisp
%{_mandir}/man1/clisp.1*
%{_pkgdocdir}/
%dir %{_libdir}/%{instdir}/
%dir %{_libdir}/%{instdir}/asdf/
%{_libdir}/%{instdir}/asdf/asdf.fas
%dir %{_libdir}/%{instdir}/base/
%{_libdir}/%{instdir}/base/lispinit.mem
%{_libdir}/%{instdir}/base/lisp.run
%dir %{_libdir}/%{instdir}/berkeley-db/
%{_libdir}/%{instdir}/berkeley-db/*.fas
%{_libdir}/%{instdir}/berkeley-db/preload.lisp
%dir %{_libdir}/%{instdir}/bindings/
%dir %{_libdir}/%{instdir}/bindings/glibc/
%{_libdir}/%{instdir}/bindings/glibc/*.fas
%dir %{_libdir}/%{instdir}/clx/
%dir %{_libdir}/%{instdir}/clx/new-clx/
%{_libdir}/%{instdir}/clx/new-clx/*.fas
%{_libdir}/%{instdir}/clx/new-clx/clx-preload.lisp
%{_libdir}/%{instdir}/data/
%dir %{_libdir}/%{instdir}/dbus/
%{_libdir}/%{instdir}/dbus/*.fas
%{_libdir}/%{instdir}/dynmod/
%dir %{_libdir}/%{instdir}/fastcgi/
%{_libdir}/%{instdir}/fastcgi/*.fas
%dir %{_libdir}/%{instdir}/full/
%{_libdir}/%{instdir}/full/lispinit.mem
%{_libdir}/%{instdir}/full/lisp.run
%dir %{_libdir}/%{instdir}/gdbm/
%{_libdir}/%{instdir}/gdbm/*.fas
%{_libdir}/%{instdir}/gdbm/preload.lisp
%if %{with gtk2}
%dir %{_libdir}/%{instdir}/gtk2/
%{_libdir}/%{instdir}/gtk2/*.fas
%{_libdir}/%{instdir}/gtk2/preload.lisp
%endif
%dir %{_libdir}/%{instdir}/libsvm/
%{_libdir}/%{instdir}/libsvm/*.fas
%{_libdir}/%{instdir}/libsvm/preload.lisp
%dir %{_libdir}/%{instdir}/pari/
%{_libdir}/%{instdir}/pari/*.fas
%{_libdir}/%{instdir}/pari/preload.lisp
%dir %{_libdir}/%{instdir}/postgresql/
%{_libdir}/%{instdir}/postgresql/*.fas
%dir %{_libdir}/%{instdir}/rawsock/
%{_libdir}/%{instdir}/rawsock/*.fas
%{_libdir}/%{instdir}/rawsock/preload.lisp
%dir %{_libdir}/%{instdir}/zlib/
%{_libdir}/%{instdir}/zlib/*.fas
%{_emacs_sitelispdir}/*
%{vimfiles_root}/after/syntax/*

%files devel
%doc modules/clx/clx-manual
%{_bindir}/clisp-link
%{_mandir}/man1/clisp-link.1*
%{_libdir}/%{instdir}/asdf/Makefile
%{_libdir}/%{instdir}/asdf/*.lisp
%{_libdir}/%{instdir}/asdf/*.sh
%{_libdir}/%{instdir}/base/*.a
%{_libdir}/%{instdir}/base/*.h
%{_libdir}/%{instdir}/base/*.o
%{_libdir}/%{instdir}/base/makevars
%{_libdir}/%{instdir}/berkeley-db/Makefile
%{_libdir}/%{instdir}/berkeley-db/*.h
%{_libdir}/%{instdir}/berkeley-db/dbi.lisp
%{_libdir}/%{instdir}/berkeley-db/*.o
%{_libdir}/%{instdir}/berkeley-db/*.sh
%{_libdir}/%{instdir}/bindings/glibc/Makefile
%{_libdir}/%{instdir}/bindings/glibc/*.lisp
%{_libdir}/%{instdir}/bindings/glibc/*.o
%{_libdir}/%{instdir}/bindings/glibc/*.sh
%{_libdir}/%{instdir}/build-aux/
%{_libdir}/%{instdir}/clx/new-clx/demos/
%{_libdir}/%{instdir}/clx/new-clx/README
%{_libdir}/%{instdir}/clx/new-clx/Makefile
%{_libdir}/%{instdir}/clx/new-clx/*.h
%{_libdir}/%{instdir}/clx/new-clx/clx.lisp
%{_libdir}/%{instdir}/clx/new-clx/image.lisp
%{_libdir}/%{instdir}/clx/new-clx/resource.lisp
%{_libdir}/%{instdir}/clx/new-clx/*.o
%{_libdir}/%{instdir}/clx/new-clx/*.sh
%{_libdir}/%{instdir}/config.h
%{_libdir}/%{instdir}/dbus/Makefile
%{_libdir}/%{instdir}/dbus/*.h
%{_libdir}/%{instdir}/dbus/*.lisp
%{_libdir}/%{instdir}/dbus/*.o
%{_libdir}/%{instdir}/dbus/*.sh
%{_libdir}/%{instdir}/fastcgi/README
%{_libdir}/%{instdir}/fastcgi/Makefile
%{_libdir}/%{instdir}/fastcgi/*.h
%{_libdir}/%{instdir}/fastcgi/*.lisp
%{_libdir}/%{instdir}/fastcgi/*.o
%{_libdir}/%{instdir}/fastcgi/*.sh
%{_libdir}/%{instdir}/full/*.a
%{_libdir}/%{instdir}/full/*.h
%{_libdir}/%{instdir}/full/*.o
%{_libdir}/%{instdir}/full/makevars
%{_libdir}/%{instdir}/gdbm/Makefile
%{_libdir}/%{instdir}/gdbm/*.h
%{_libdir}/%{instdir}/gdbm/gdbm.lisp
%{_libdir}/%{instdir}/gdbm/*.o
%{_libdir}/%{instdir}/gdbm/*.sh
%if %{with gtk2}
%{_libdir}/%{instdir}/gtk2/Makefile
%{_libdir}/%{instdir}/gtk2/*.cfg
%{_libdir}/%{instdir}/gtk2/*.glade
%{_libdir}/%{instdir}/gtk2/*.h
%{_libdir}/%{instdir}/gtk2/gtk.lisp
%{_libdir}/%{instdir}/gtk2/*.o
%{_libdir}/%{instdir}/gtk2/*.sh
%endif
%{_libdir}/%{instdir}/libsvm/README
%{_libdir}/%{instdir}/libsvm/Makefile
%{_libdir}/%{instdir}/libsvm/*.h
%{_libdir}/%{instdir}/libsvm/libsvm.lisp
%{_libdir}/%{instdir}/libsvm/*.o
%{_libdir}/%{instdir}/libsvm/*.sh
%{_libdir}/%{instdir}/linkkit/
%{_libdir}/%{instdir}/pari/README
%{_libdir}/%{instdir}/pari/Makefile
%{_libdir}/%{instdir}/pari/*.h
%{_libdir}/%{instdir}/pari/desc2lisp.lisp
%{_libdir}/%{instdir}/pari/pari.lisp
%{_libdir}/%{instdir}/pari/*.o
%{_libdir}/%{instdir}/pari/*.sh
%{_libdir}/%{instdir}/postgresql/README
%{_libdir}/%{instdir}/postgresql/Makefile
%{_libdir}/%{instdir}/postgresql/*.h
%{_libdir}/%{instdir}/postgresql/*.lisp
%{_libdir}/%{instdir}/postgresql/*.o
%{_libdir}/%{instdir}/postgresql/*.sh
%{_libdir}/%{instdir}/rawsock/demos/
%{_libdir}/%{instdir}/rawsock/Makefile
%{_libdir}/%{instdir}/rawsock/*.h
%{_libdir}/%{instdir}/rawsock/sock.lisp
%{_libdir}/%{instdir}/rawsock/*.o
%{_libdir}/%{instdir}/rawsock/*.sh
%{_libdir}/%{instdir}/zlib/Makefile
%{_libdir}/%{instdir}/zlib/*.h
%{_libdir}/%{instdir}/zlib/*.lisp
%{_libdir}/%{instdir}/zlib/*.o
%{_libdir}/%{instdir}/zlib/*.sh
%{_datadir}/aclocal/clisp.m4


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.95-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Jerry James <loganjerry@gmail.com> - 2.49.95-4
- Update to latest git snapshot
- Drop one upstreamed patch to fix undefined behavior

* Fri Feb 14 2025 Jerry James <loganjerry@gmail.com> - 2.49.95-3
- Add patches to fix more undefined behavior
- Fix misaligned memory accesses on ppc64le
- Fix mismatched readline function declarations

* Fri Feb  7 2025 Jerry James <loganjerry@gmail.com> - 2.49.95-3
- Add patch to fix undefined behavior (rhbz#2339979)
- Add two patches to fix memory leaks
- Do not force -O1

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.95-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Jan 13 2025 Jerry James <loganjerry@gmail.com> - 2.49.95-2
- Update to latest git snapshot
- Move configuration steps to %%conf

* Mon Nov 25 2024 Jerry James <loganjerry@gmail.com> - 2.49.95-1
- Version 2.49.95
- Drop upstreamed patches: db, c99, bdb-mismatched-pointer, new-clx, pari

* Sat Oct  5 2024 Jerry James <loganjerry@gmail.com> - 2.49.93-40
- Rebuild for pari 2.17.0

* Tue Sep  3 2024 Jerry James <loganjerry@gmail.com> - 2.49.93-39
- Update to latest git snapshot
- Add patch to fix FTBFS in the new-clx code
- Add patch to avoid calling the deprecated siginterrupt function
- Add VCS field
- Setting LC_ALL is no longer necessary

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.93-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.93-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.93-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec  1 2023 Jerry James <loganjerry@gmail.com> - 2.49.93-35
- Fix a mismatched pointer type error with GCC 14

* Wed Aug 16 2023 Jerry James <loganjerry@gmail.com> - 2.49.93-34
- Build without pcre support (rhbz#2128278)

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.93-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 18 2023 Jerry James <loganjerry@gmail.com> - 2.49.93-32
- Update to fix message typos

* Mon May 08 2023 Florian Weimer <fweimer@redhat.com> - 2.49.93-31
- Port to C99

* Tue Apr  4 2023 Jerry James <loganjerry@gmail.com> - 2.49.93-30
- Update to allow non-simple strings in FORMAT and FORMATTER
- Drop upstreamed ensure-6x patch
- Disable gtk2 support for RHEL 10 (thanks to Yaakov Selkowitz)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.93-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 10 2023 Jerry James <loganjerry@gmail.com> - 2.49.93-29
- Update to latest git snapshot for buffer overflow fix
- Drop upstreamed pari patch

* Mon Sep 19 2022 Jerry James <loganjerry@gmail.com> - 2.49.93-28
- Rebuild for pari 2.15.0

* Thu Aug 18 2022 Jerry James <loganjerry@gmail.com> - 2.49.93-27
- Rebuild for libsvm 3.3

* Mon Aug 15 2022 Jerry James <loganjerry@gmail.com> - 2.49.93-26
- Convert License tag to SPDX

* Wed Aug 10 2022 Jerry James <loganjerry@gmail.com> - 2.49.93-26
- Move preload.lisp files to the main package

* Mon Aug  8 2022 Jerry James <loganjerry@gmail.com> - 2.49.93-25
- Add -ensure-6x patch (rhbz#2115476)

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.93-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 18 2022 Jerry James <loganjerry@gmail.com> - 2.49.93-23
- Reduce the impact of the -no-inline patch

* Thu Feb  3 2022 Jerry James <loganjerry@gmail.com> - 2.49.93-23
- Add -no-inline patch to workaround bz 2049371 (ppc64le segfault)

* Fri Jan 28 2022 Jerry James <loganjerry@gmail.com> - 2.49.93-23
- Add -pts-access patch to fix FTBFS

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.93-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.93-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jul 16 2021 Jerry James <loganjerry@gmail.com> - 2.49.93-21.20210628gitde01f0f
- Update to latest git snapshot for autoconf + glib updates
- Drop upstreamed -setkey patch
- Use forge macros
- Use default HyperSpec URLs

* Thu Jun 17 2021 Jerry James <loganjerry@gmail.com> - 2.49.93-20.d9cbf22git
- Rebuild for ffcall 2.4 and multithreaded pari

* Tue May 25 2021 Florian Weimer <fweimer@redhat.com> - 2.49.93-19.d9cbf22git
- Rebuild with new binutils to fix ppc64le corruption (#1960730)

* Tue Mar 23 2021 Jerry James <loganjerry@gmail.com> - 2.49.93-18.d9cbf22git
- Update to latest git snapshot for autoconf + glib updates
- Fix broken symlinks in the full set

* Mon Feb 08 2021 Pavel Raiskup <praiskup@redhat.com> - 2.49.93-17.a9aeb80git
- rebuild for libpq ABI fix rhbz#1908268

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.93-16.a9aeb80git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov  9 2020 Jerry James <loganjerry@gmail.com> - 2.49.93-15.a9aeb80git
- Update to latest git snapshot for more HyperSpec fixes

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.93-14.c26de78git
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Jeff Law <law@redhat.com> - 2.49.93-13.c26de78git
- Disable LTO

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.93-12.c26de78git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.93-11.c26de78git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 17 2019 Jerry James <loganjerry@gmail.com> - 2.49.93-10.c26de78git
- Update to latest git snapshot for HyperSpec fixes

* Mon Aug 26 2019 Jerry James <loganjerry@gmail.com> - 2.49.93-9.dd40369git
- Update to latest git snapshot for bug fixes
- Add latest German translation

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.93-8.df3b9f6git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Mar 30 2019 Jerry James <loganjerry@gmail.com> - 2.49.93-7.df3b9f6git
- Update to latest git snapshot for bug fixes
- Add -register-volatile patch
- Build for s390x again now that bz 1689769 is fixed

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.49.93-6.90b3631git
- Rebuild for readline 8.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.93-5.90b3631git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 2.49.93-4.90b3631git
- Rebuilt for libcrypt.so.2 (#1666033)

* Fri Aug 10 2018 Jerry James <loganjerry@gmail.com> - 2.49.93-3.90b3631git
- Update to latest git snapshot for bug fixes

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.93-2.d1310adgit
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 21 2018 Jerry James <loganjerry@gmail.com> - 2.49.93-1.d1310adgit
- License change: GPLv2 to GPLv2+
- Build with readline 6 due to the new license
- Drop upstreamed -arm, -libsvm, -alias, and -linux patches
- Build for all architectures
- Bring back the pari module

* Mon Feb 26 2018 Tom Callaway <spot@fedoraproject.org> - 2.49.93-0.1.20180224hg
- update to latest in mercurial (lots of fixes)
- re-enable ppc64, aarch64
- disable s390x (builds, but does not run properly)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.49-27.20170224hg
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Jan 21 2018 Björn Esser <besser82@fedoraproject.org> - 2.49-26.20170224hg
- Explicitly BR: ffcall-devel and configure --with-ffcall

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 2.49-25.20170224hg
- Rebuilt for switch to libxcrypt

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.49-24.20170224hg
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.49-23.20170224hg
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 24 2017 Jerry James <loganjerry@gmail.com> - 2.49-22.20170224hg
- Update to latest mercurial snapshot
- Drop upstreamed -32bit patch
- Add -volatile, -negshift, and -alias patches

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.49-22.20161113hg
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 28 2017 Jerry James <loganjerry@gmail.com> - 2.49-21.20161113hg
- Update to latest mercurial snapshot

* Fri Nov 11 2016 Jerry James <loganjerry@gmail.com> - 2.49-20.20161111hg
- Update to latest mercurial snapshot (bz 1392563)
- Drop upstreamed -gcc5 patch
- Rebase all other patches
- Update config.guess and config.sub

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.49-19.20130208hg
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Sep 29 2015 Jerry James <loganjerry@gmail.com> - 2.49-18.20130208hg
- Install the full link set
- Fix installed Makefile paths
- Fix clx manual permissions

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.49-17.20130208hg
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr  3 2015 Jerry James <loganjerry@gmail.com> - 2.49-16.20130208hg
- Fix modules that need access to symbols in libgnu.a

* Wed Feb 11 2015 Jerry James <loganjerry@gmail.com> - 2.49-15.20130208hg
- Add -gcc5 patch to fix 32-bit build with gcc 5.0
- Use license macro

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.49-14.20130208hg
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.49-13.20130208hg
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Aug 30 2013 Jerry James <loganjerry@gmail.com> - 2.49-11.20130208hg
- clisp does not support aarch64 (bz 925155)
- Adapt to versionless docdir (bz 992605 and 993701)
- More stack space needed to install

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.49-11.20130208hg
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.49-10.20130208hg
- Perl 5.18 rebuild

* Mon Feb 18 2013 Jerry James <loganjerry@gmail.com> - 2.49-9.20130208hg
- Update to mercurial snapshot to fix FTBFS
- Drop upstreamed -hostname patch
- Build against libdb instead of libdb4
- Include the CLX manual in the -devel documentation
- Compile the Emacs Lisp interface
- Build the asdf module

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.49-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 25 2012 Jerry James <loganjerry@gmail.com> - 2.49-8
- Fix build for new libdb4-devel package.
- Fix ARM assembly (bz 812928)
- Add gnulib Provides (bz 821747)
- Disable the pari module for now; it does not compile against pari 2.5

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.49-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Mar 18 2012 Daniel E. Wilson <danw@bureau-13.org> - 2.49-6
- Changed build process to define the default browser.
- Fixed module directories to move only *.fas files.
- Moved build-aux directory to the development package.
- Replaced the clisp-* wildcards with the correct version.
- More stack space may be needed on all arches (Jerry James).

* Sun Jan  8 2012 Jerry James <loganjerry@gmail.com> - 2.49-5
- Rebuild for GCC 4.7
- Minor spec file cleanups

* Thu Jun 23 2011 Jerry James <loganjerry@gmail.com> - 2.49-4
- Add libsvm patch to fix FTBFS on Rawhide (bz 715970)
- Fix readline module to also use compat-readline5 instead of readline6
- Drop unnecessary spec file elements (clean script, etc.)

* Fri Feb 11 2011 Jerry James <loganjerry@gmail.com> - 2.49-3
- Build with compat-readline5 instead of readline (#511303)
- Build the libsvm module
- Get rid of the execstack flag on Lisp images

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.49-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Nov 28 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.49-1
- clisp-2.49 (#612469)
- -devel: Provides: %%name-static (#609602)

* Sun Nov 28 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.48-2
- rebuild (libsigsegv)

* Fri Feb 26 2010 Jerry James <loganjerry@gmail.com> - 2.48-1
- new release 2.48

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.47-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 22 2008 Gerard Milmeister <gemi@bluewin.ch> - 2.47-1
- new release 2.47

* Wed Jul  2 2008 Gerard Milmeister <gemi@bluewin.ch> - 2.46-1
- new release 2.46

* Fri Apr 18 2008 Gerard Milmeister <gemi@bluewin.ch> - 2.44.1-1
- new release 2.44.1

* Fri Feb 22 2008 Gerard Milmeister <gemi@bluewin.ch> - 2.43-5
- Compile with -O0 to avoid GCC 4.3 miscompilation

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.43-4
- Autorebuild for GCC 4.3

* Sat Nov 24 2007 Gerard Milmeister <gemi@bluewin.ch> - 2.43-1
- new release 2.43

* Tue Oct 16 2007 Gerard Milmeister <gemi@bluewin.ch> - 2.42-1
- new release 2.42

* Fri May  4 2007 David Woodhouse <dwmw2@infradead.org> - 2.41-6
- Revert to overriding stack limit in specfile

* Thu May  3 2007 David Woodhouse <dwmw2@infradead.org> - 2.41-5
- Exclude ppc64 for now

* Mon Apr 30 2007 David Woodhouse <dwmw2@infradead.org> - 2.41-4
- Fix stack size in configure, restore ppc build

* Sat Dec  9 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.41-3
- rebuild without berkeley-db for now

* Fri Oct 13 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.41-1
- new version 2.41

* Tue Oct  3 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.40-3
- Added patch for x86_64

* Mon Oct  2 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.40-1
- new version 2.40

* Mon Aug 28 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.39-4
- Rebuild for FE6

* Fri Jul 28 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.39-3
- changed url to canonical web page

* Mon Jul 24 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.39-2
- rebuild with updated libsigsegv
- set CFLAGS to ""

* Mon Jul 17 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.39-1
- new version 2.39

* Fri Feb 17 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.38-2
- Rebuild for Fedora Extras 5

* Sun Jan 29 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.38-1
- new version 2.38

* Tue Jan  3 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.37-1
- new version 2.37

* Wed Dec 28 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.36-1
- New Version 2.36

* Tue Aug 30 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.35-1
- New Version 2.35

* Thu Aug 18 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.34-5
- do the compilation in the "build" directory

* Thu Aug 18 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.34-4
- Use ulimit for the build to succeed on ppc

* Wed Aug 17 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.34-3
- Build fails on ppc, exclude for now

* Wed Aug 17 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.34-2
- Fix libdir for x86_64

* Tue Aug 16 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.34-1
- New Version 2.34
