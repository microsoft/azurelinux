Vendor:         Microsoft Corporation
Distribution:   Mariner
%define pkg_version 6.0
%define api_version 0.7.0

%bcond_without python3
%bcond_with python2

%{!?tcl_version: %global tcl_version %(echo 'puts $tcl_version' | tclsh)}
%{!?tcl_sitearch: %global tcl_sitearch %{_prefix}/%{_lib}/tcl%{tcl_version}}

# without speech dispatcher
%define with_speech_dispatcher 0

# without espeak support
%define with_espeak 0

%global with_ocaml 1

# Filter private libraries
%global _privatelibs libbrltty.+\.so.*
%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$

Name: brltty
Version: %{pkg_version}
Release: 15%{?dist}
License: LGPLv2+
URL: http://brltty.app/
Source0: http://brltty.app/archive/%{name}-%{version}.tar.xz
Source1: brltty.service
Patch1: brltty-6.0-loadLibrary.patch
# libspeechd.h moved in latest speech-dispatch (NOT sent upstream)
Patch2: brltty-5.0-libspeechd.patch
Patch3: brltty-6.0-alsa-1.1.9-fix.patch
Summary: Braille display driver for Linux/Unix
BuildRequires: byacc, glibc-kernheaders, bluez-libs-devel, systemd
BuildRequires: gettext, at-spi2-core-devel, alsa-lib-devel
%if %{with_espeak}
BuildRequires: espeak-devel
%endif
BuildRequires: espeak-ng-devel
BuildRequires: /usr/bin/2to3
BuildRequires: autoconf

Requires: brlapi%{?_isa} = %{api_version}-%{release}
# work around a bug in the install process:
Requires(post): coreutils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
BRLTTY is a background process (daemon) which provides
access to the Linux/Unix console (when in text mode)
for a blind person using a refreshable braille display.
It drives the braille display and provides complete
screen review functionality.
%if %{with_speech_dispatcher}
BRLTTY can also work with speech synthesizers; if you want to use it with
Speech Dispatcher, please install also package %{name}-speech-dispatcher.

%package speech-dispatcher
Summary: Speech Dispatcher driver for BRLTTY
License: LGPLv2+
BuildRequires: speech-dispatcher-devel
Requires: %{name}%{?_isa} = %{pkg_version}-%{release}
%description speech-dispatcher
This package provides the Speech Dispatcher driver for BRLTTY.
%endif

%package docs
Summary: Documentation for BRLTTY
License: LGPLv2+
Requires: %{name} = %{pkg_version}-%{release}
BuildArch: noarch
%description docs
This package provides the documentation for BRLTTY.

%package xw
Summary: XWindow driver for BRLTTY
License: LGPLv2+
BuildRequires: libSM-devel libICE-devel libX11-devel libXaw-devel libXext-devel libXt-devel libXtst-devel
Requires: %{name}%{?_isa} = %{pkg_version}-%{release}
Requires: xorg-x11-fonts-misc, ucs-miscfixed-fonts
%description xw
This package provides the XWindow driver for BRLTTY.

%package at-spi2
Summary: AtSpi2 driver for BRLTTY
License: LGPLv2+
Requires: %{name}%{?_isa} = %{pkg_version}-%{release}
%description at-spi2
This package provides the AtSpi2 driver for BRLTTY.

%if %{with_espeak}
%package espeak
Summary: eSpeak driver for BRLTTY
License: LGPLv2+
Requires: %{name}%{?_isa} = %{pkg_version}-%{release}
%description espeak
This package provides the eSpeak driver for BRLTTY.
%endif

%package espeak-ng
Summary: eSpeak-NG driver for BRLTTY
License: LGPLv2+
Requires: %{name}%{?_isa} = %{pkg_version}-%{release}
%if ! %{with_espeak}
Obsoletes: brltty-espeak <= 5.6-5
%endif
%description espeak-ng
This package provides the eSpeak-NG driver for BRLTTY.

%package -n brlapi
Version: %{api_version}
License: LGPLv2+
Summary: Application Programming Interface for BRLTTY
Requires: %{name}%{?_isa} = %{pkg_version}-%{release}
Requires(pre): glibc-common, shadow-utils
Requires(post): coreutils, util-linux
%description -n brlapi
This package provides the run-time support for the Application
Programming Interface to BRLTTY.

Install this package if you have an application which directly accesses
a refreshable braille display.

%package -n brlapi-devel
Version: %{api_version}
License: LGPLv2+
Requires: brlapi%{?_isa} = %{api_version}-%{release}
Summary: Headers, static archive, and documentation for BrlAPI

%description -n brlapi-devel
This package provides the header files, static archive, shared object
linker reference, and reference documentation for BrlAPI (the
Application Programming Interface to BRLTTY).  It enables the
implementation of applications which take direct advantage of a
refreshable braille display in order to present information in ways
which are more appropriate for blind users and/or to provide user
interfaces which are more specifically attuned to their needs.

Install this package if you are developing or maintaining an application
which directly accesses a refreshable braille display.

%package -n tcl-brlapi
Version: %{api_version}
License: LGPLv2+
Requires: brlapi%{?_isa} = %{api_version}-%{release}
BuildRequires: tcl-devel
Summary: Tcl binding for BrlAPI
%description -n tcl-brlapi
This package provides the Tcl binding for BrlAPI.

%if %{with python2}
%package -n python2-brlapi
%{?python_provide:%python_provide python2-brlapi}
Version: %{api_version}
License: LGPLv2+
Requires: brlapi%{?_isa} = %{api_version}-%{release}
BuildRequires: Cython
BuildRequires: python2-devel
BuildRequires: python2-setuptools
Summary: Python binding for BrlAPI
%description -n python2-brlapi
This package provides the Python 2 binding for BrlAPI.
%endif

%if %{with python3}
%package -n python3-brlapi
%{?python_provide:%python_provide python3-brlapi}
Version: %{api_version}
License: LGPLv2+
Requires: brlapi%{?_isa} = %{api_version}-%{release}
BuildRequires: python3-Cython
BuildRequires: python3-devel
%if %{without python2}
Obsoletes:     python2-brlapi < %{api_version}-%{release}
Obsoletes:     python-brlapi < %{api_version}-%{release}
%endif
Summary: Python 3 binding for BrlAPI
%description -n python3-brlapi
This package provides the Python 3 binding for BrlAPI.
%endif

%package -n brlapi-java
Version: %{api_version}
License: LGPLv2+
Requires: brlapi%{?_isa} = %{api_version}-%{release}
BuildRequires: jpackage-utils
BuildRequires: java-devel
Summary: Java binding for BrlAPI
%description -n brlapi-java
This package provides the Java binding for BrlAPI.

%if 0%{?with_ocaml}
%package -n ocaml-brlapi
Version: %{api_version}
License: LGPLv2+
Requires: brlapi%{?_isa} = %{api_version}-%{release}
BuildRequires: ocaml
Summary: OCaml binding for BrlAPI
%description -n ocaml-brlapi
This package provides the OCaml binding for BrlAPI.
%endif

%package dracut
Summary: brltty module for Dracut
Requires: %{name}%{?_isa} = %{pkg_version}-%{release}
Requires: dracut
%description dracut
This package provides brltty module for Dracut.

%define version %{pkg_version}

%prep
%setup -qc
mv %{name}-%{version} python2

pushd python2
%patch1 -p1 -b .loadLibrary
%patch2 -p1 -b .libspeechd
%patch3 -p1 -b .alsa-1.1.9-fix

# remove packaged binary file
rm -f Programs/brltty-ktb
popd

# Make a copy of the source tree for building the Python 3 module
# Make it all time, we just gonna ignore python2 or python3 when not needed
cp -a python2 python3


%build
# If MAKEFLAGS=-jN is set it would break local builds.
unset MAKEFLAGS

# Add the openjdk include directories to CPPFLAGS
for i in -I/usr/lib/jvm/java/include{,/linux}; do
      java_inc="$java_inc $i"
done
export CPPFLAGS="$java_inc"

export LDFLAGS="%{?build_ldflags}"
export CFLAGS="%{optflags} -fno-strict-aliasing $LDFLAGS"
export CXXFLAGS="%{optflags} -fno-strict-aliasing $LDFLAGS"

# there is no curses packages in BuildRequires, so the package builds
# without them in mock; let's express this decision explicitly
configure_opts=" \
  --disable-stripping \
  --without-curses \
%if %{with_speech_dispatcher}
  --with-speechd=%{_prefix} \
%endif
%if ! %{with_espeak}
  --without-espeak \
%endif
  --with-install-root=$RPM_BUILD_ROOT
  JAVA_JAR_DIR=%{_jnidir} \
  JAVA_JNI_DIR=%{_libdir}/brltty \
  JAVA_JNI=yes"

export PYTHONCOERCECLOCALE=0

PYTHONS=

%if %{with python2}
# First build everything with Python 2 support
pushd python2
./autogen
%configure $configure_opts PYTHON=%{__python2}
# Parallel build seems broken, thus disabling it
make
popd
PYTHONS="$PYTHONS python2"
%endif

%if %{with python3}
# ... and then do it again for the Python 3 module
pushd python3
./autogen
%configure $configure_opts PYTHON=%{__python3} CYTHON=%{_bindir}/cython
make
popd
PYTHONS="$PYTHONS python3"
%endif


for python in $PYTHONS
  do pushd $python
    find . -name '*.sgml' |
    while read file; do
       iconv -f iso8859-1 -t utf-8 $file > $file.conv && mv -f $file.conv $file
    done
    find . -name '*.txt' |
    while read file; do
       iconv -f iso8859-1 -t utf-8 $file > $file.conv && mv -f $file.conv $file
    done
    find . -name 'README*' |
    while read file; do
       iconv -f iso8859-1 -t utf-8 $file > $file.conv && mv -f $file.conv $file
    done

    find . \( -path ./doc -o -path ./Documents \) -prune -o \
      \( -name 'README*' -o -name '*.txt' -o -name '*.html' -o \
         -name '*.sgml' -o -name '*.patch' -o \
         \( -path './Bootdisks/*' -type f -perm /ugo=x \) \) -print |
    while read file; do
       mkdir -p ../doc/${file%/*} && cp -rp $file ../doc/$file || exit 1
    done
  popd
done

%install
%if 0%{?with_ocaml}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs
%endif

%if %{with python2}
# Python 2
pushd python2
make install JAVA_JAR_DIR=%{_jnidir} \
             JAVA_JNI_DIR=%{_libdir}/brltty \
             JAVA_JNI=yes
popd
%endif

%if %{with python3}
# Python 3
pushd python3
make install JAVA_JAR_DIR=%{_jnidir} \
             JAVA_JNI_DIR=%{_libdir}/brltty \
             JAVA_JNI=yes
popd
%endif

%if %{with python3}
# just use the higher number here
pushd python3
%else
pushd python2
%endif

install -d -m 755 "${RPM_BUILD_ROOT}%{_sysconfdir}" "$RPM_BUILD_ROOT%{_mandir}/man5"
install -m 644 Documents/brltty.conf "${RPM_BUILD_ROOT}%{_sysconfdir}"
echo ".so man1/brltty.1" > $RPM_BUILD_ROOT%{_mandir}/man5/brltty.conf.5

install -Dpm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}/brltty.service

cp -p LICENSE* ../

# clean up the manuals:
rm Documents/Manual-*/*/{*.mk,*.made,Makefile*}
mv Documents/BrlAPIref/{html,BrlAPIref}

for i in Drivers/Speech/SpeechDispatcher/README \
         Documents/ChangeLog Documents/TODO \
         Documents/Manual-BRLTTY \
         Drivers/Braille/XWindow/README \
         Drivers/Braille/XWindow/README \
         Documents/Manual-BrlAPI \
         Documents/BrlAPIref/BrlAPIref \
; do
   mkdir -p ../${i%/*} && cp -rp $i ../$i || exit 1
done

# Don't want static lib
rm -rf $RPM_BUILD_ROOT/%{_libdir}/libbrlapi.a

# ghost brlapi.key
touch ${RPM_BUILD_ROOT}%{_sysconfdir}/brlapi.key

# disable xbrlapi gdm autostart, there is already orca
rm -f ${RPM_BUILD_ROOT}%{_datadir}/gdm/greeter/autostart/xbrlapi.desktop

# make brltty-config executable
chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/brltty-config

# handle locales
%find_lang %{name}
cp -p %{name}.lang ../

#Use python 3 for latex-access, BZ 1465657.
/usr/bin/2to3 -wn ${RPM_BUILD_ROOT}/etc/brltty/Contraction/latex-access.ctb
sed -i 's|/usr/bin/python|%{__python3}|g' ${RPM_BUILD_ROOT}/etc/brltty/Contraction/latex-access.ctb

# install dracut module
make install-dracut

popd

# drop documentation already instaled by the dracut subpackage
rm -f doc/Initramfs/Dracut/README*
rmdir doc/Initramfs/Dracut doc/Initramfs

%post
%systemd_post brltty.service

%preun
%systemd_preun brltty.service

%postun
%systemd_postun_with_restart brltty.service

%pre -n brlapi
getent group brlapi >/dev/null || groupadd -r brlapi >/dev/null

%post -n brlapi
if [ ! -e %{_sysconfdir}/brlapi.key ]; then
  mcookie > %{_sysconfdir}/brlapi.key
  chgrp brlapi %{_sysconfdir}/brlapi.key
  chmod 0640 %{_sysconfdir}/brlapi.key
fi
%{?ldconfig}

%ldconfig_postun -n brlapi

%files -f %{name}.lang
%config(noreplace) %{_sysconfdir}/brltty.conf
%{_sysconfdir}/brltty/
%exclude %{_sysconfdir}/brltty/Initramfs
%{_unitdir}/brltty.service
%{_bindir}/brltty
%{_bindir}/brltty-*
%{_libdir}/brltty/
%exclude %{_libdir}/brltty/libbrlttybba.so
%exclude %{_libdir}/brltty/libbrlttybxw.so
%exclude %{_libdir}/brltty/libbrlttyxa2.so
%exclude %{_libdir}/brltty/libbrlttysen.so
%exclude %{_libdir}/brltty/libbrlttyses.so
%exclude %{_libdir}/brltty/libbrlapi_java.so
%if %{with_speech_dispatcher}
%exclude %{_libdir}/brltty/libbrlttyssd.so
%endif
%license LICENSE-LGPL
%doc %{_mandir}/man[15]/brltty.*
%{_sysconfdir}/X11/Xsession.d/60xbrlapi
#%%{_datadir}/metainfo/org.a11y.brltty.metainfo.xml
%{_datadir}/polkit-1/actions/org.a11y.brlapi.policy


%if %{with_speech_dispatcher}
%files speech-dispatcher
%doc Drivers/Speech/SpeechDispatcher/README
%{_libdir}/brltty/libbrlttyssd.so
%endif

%files docs
%doc Documents/ChangeLog Documents/TODO
%doc Documents/Manual-BRLTTY/
%doc doc/*

%files xw
%doc Drivers/Braille/XWindow/README
%{_libdir}/brltty/libbrlttybxw.so

%files at-spi2
%{_libdir}/brltty/libbrlttyxa2.so

%if %{with_espeak}
%files espeak
%{_libdir}/brltty/libbrlttyses.so
%endif

%files espeak-ng
%{_libdir}/brltty/libbrlttysen.so

%files -n brlapi
%{_bindir}/vstp
%{_bindir}/eutp
%{_bindir}/xbrlapi
%{_libdir}/brltty/libbrlttybba.so
%{_libdir}/libbrlapi.so.*
%ghost %{_sysconfdir}/brlapi.key
%doc Drivers/Braille/XWindow/README
%doc Documents/Manual-BrlAPI/
%doc %{_mandir}/man1/xbrlapi.*
%doc %{_mandir}/man1/vstp.*
%doc %{_mandir}/man1/eutp.*

%files -n brlapi-devel
%{_libdir}/libbrlapi.so
%{_includedir}/brltty
%{_includedir}/brlapi*.h
%doc %{_mandir}/man3/brlapi_*.3*
%doc Documents/BrlAPIref/BrlAPIref/

%files -n tcl-brlapi
%{tcl_sitearch}/brlapi-%{api_version}

%if %{with python2}
%files -n python2-brlapi
%{python2_sitearch}/brlapi.so
%{python2_sitearch}/Brlapi-%{api_version}-*.egg-info
%endif

%if %{with python3}
%files -n python3-brlapi
%{python3_sitearch}/brlapi.cpython-*.so
%{python3_sitearch}/Brlapi-%{api_version}-*.egg-info
%endif

%files -n brlapi-java
%{_libdir}/brltty/libbrlapi_java.so
%{_jnidir}/brlapi.jar

%if 0%{?with_ocaml}
%files -n ocaml-brlapi
%{_libdir}/ocaml/brlapi/
%{_libdir}/ocaml/stublibs/
%endif

%files dracut
%{_prefix}/lib/dracut/modules.d/99brltty/
%dir %{_sysconfdir}/brltty/Initramfs
%config(noreplace) %verify(not size md5 mtime) %{_sysconfdir}/brltty/Initramfs/dracut.conf
%config(noreplace) %verify(not size md5 mtime) %{_sysconfdir}/brltty/Initramfs/cmdline

%changelog
* Wed Aug 11 2021 Thomas Crain <thcrain@microsoft.com> - 6.0-15
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Turn off espeak-ng, speech-dispatcher support

* Thu Apr 02 2020 Richard W.M. Jones <rjones@redhat.com> - 6.0-14
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 6.0-13
- OCaml 4.10.0 final.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 18 2020 Richard W.M. Jones <rjones@redhat.com> - 6.0-11
- OCaml 4.10.0+beta1 rebuild.

* Wed Jan 08 2020 Richard W.M. Jones <rjones@redhat.com> - 6.0-10
- OCaml 4.09.0 for riscv64

* Fri Dec 06 2019 Richard W.M. Jones <rjones@redhat.com> - 6.0-9
- OCaml 4.09.0 (final) rebuild.

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 6.0-8
- Rebuilt for Python 3.8

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 6.0-7
- OCaml 4.08.1 (final) rebuild.

* Wed Jul 31 2019 Richard W.M. Jones <rjones@redhat.com> - 6.0-6
- OCaml 4.08.1 (rc2) rebuild.

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Richard W.M. Jones <rjones@redhat.com> - 6.0-4
- OCaml 4.08.0 (final) rebuild.

* Fri Jun  7 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 6.0-3
- Fixed build with alsa-1.1.9
  Resolves: rhbz#1716389

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 6.0-2
- OCaml 4.08.0 (beta 3) rebuild.

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.6-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Dec 11 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 5.6-31
- Do not package documentation for dracut module twice

* Tue Dec 11 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 5.6-30
- Rebased dracut support to upstream version
- Added requires to subpackages

* Wed Dec  5 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 5.6-29
- Improved CFLAGS handling when building Ocaml bindings

* Wed Dec  5 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 5.6-28
- Built OCaml bindings with distribution CFLAGS and consolidated patches
- Fixed Cython build requires
- Used macro for python3 path

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.6-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 5.6-26
- OCaml 4.07.0 (final) rebuild.

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 5.6-25
- Rebuilt for Python 3.7

* Thu Jun 21 2018 Paolo Bonzini <pbonzini@redhat.com> - 5.6-24
- Remove unnecessary dependency from brlapi and brltty-docs to brltty

* Wed Jun 20 2018 Richard W.M. Jones <rjones@redhat.com> - 5.6-23
- OCaml 4.07.0-rc1 rebuild.

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 5.6-22
- Rebuilt for Python 3.7

* Mon Jun 11 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 5.6-21
- Improved brltty service to start before display manager and getty

* Fri Jun  8 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 5.6-20
- Fixed installation of multiple drivers and text tables in Dracut module
  if environment variables are used

* Mon Jun  4 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 5.6-19
- Fixed Dracut module requirements

* Mon Jun  4 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 5.6-18
- Improved Dracut module to support more boot command line arguments

* Fri Jun  1 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 5.6-17
- Updated URL and Source

* Thu May 31 2018 Tomas Korbar <tomas.korb@seznam.cz> - 5.6-16
- Added Dracut module

* Tue May 29 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 5.6-15
- Added support for ALSA

* Thu May 24 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 5.6-14
- Also enabled systemd service in rescue target

* Thu May 24 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 5.6-13
- Systemd service is now installed to default and emergency targets,
  because assistive technology should be available there

* Tue May 22 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 5.6-12
- Switched to upstream patch adding LDFLAGS to more libraries
  Related: rhbz#1543490

* Mon May 21 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 5.6-11
- Added LDFLAGS to more libraries
  Related: rhbz#1543490

* Thu Apr 26 2018 Richard W.M. Jones <rjones@redhat.com> - 5.6-10
- OCaml 4.07.0-beta2 rebuild.

* Wed Apr 25 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 5.6-9
- Switched to upstream patch fixing building with distro's LDFLAGS
  Related: rhbz#1543490

* Tue Apr 24 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 5.6-8
- Build with distro's LDFLAGS
  Related: rhbz#1543490

* Fri Mar 16 2018 Miro Hrončok <mhroncok@redhat.com> - 5.6-7
- Don't build Python 2 subpackage on EL > 7 and Fedora > 28
- Use bconditionals

* Thu Mar 08 2018 Ondřej Lysoněk <olysonek@redhat.com> - 5.6-6
- Build with espeak support only on Fedora

* Tue Mar 06 2018 Ondřej Lysoněk <olysonek@redhat.com> - 5.6-5
- Add support for eSpeak-NG

* Tue Mar 06 2018 Ondřej Lysoněk <olysonek@redhat.com> - 5.6-4
- Fix the License tags. The license of whole brltty is LGPLv2+ since
  the 5.6 release.

* Mon Feb 26 2018 Ondřej Lysoněk <olysonek@redhat.com> - 5.6-3
- Fix generating the brltty-debugsource package

* Mon Feb 12 2018 Gwyn Ciesla <limburgher@gmail.com> - 5.6-2
- Flag fixes.

* Tue Feb 06 2018 Gwyn Ciesla <limburgher@gmail.com> - 5.6-1
- 5.6

* Fri Dec 15 2017 Iryna Shcherbina <ishcherb@redhat.com> - 5.5-12
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Nov 17 2017 Richard W.M. Jones <rjones@redhat.com> - 5.5-11
- OCaml 4.06.0 rebuild.

* Wed Oct 04 2017 Troy Dawson <tdawson@redhat.com> - 5.5-10
- Cleanup spec file conditionals

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 5.5-9
- Python 2 binary package renamed to python2-brltty
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Tue Aug 08 2017 Richard W.M. Jones <rjones@redhat.com> - 5.5-8
- OCaml 4.05.0 rebuild.

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 11 2017 Gwyn Ciesla <limburgher@gmail.com> - 5.5-5
- Use python 3 for latex-access, BZ 1465657.

* Tue Jun 27 2017 Gwyn Ciesla <limburgher@gmail.com> - 5.5-4
- OCaml 4.04.2 rebuild.

* Thu Jun 22 2017 Gwyn Ciesla <limburgher@gmail.com> - 5.5-3
- Fix Python-related FTBFS.

* Fri May 12 2017 Richard W.M. Jones <rjones@redhat.com> - 5.5-2
- OCaml 4.04.1 rebuild.

* Wed Apr 19 2017 Gwyn Ciesla <limburgher@gmail.com> - 5.5-1
- 5.5, BZ 1443262.

* Fri Mar 17 2017 Stephen Gallagher <sgallagh@redhat.com> - 5.4-8
- Don't pass unnecessary -Wno-format to Python bindings
- Fixes FTBFS on gcc7

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 5.4-6
- Rebuild for Python 3.6

* Wed Nov  9 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 5.4-5
- Used upstream fix for OCaml 4.04

* Tue Nov 08 2016 Richard W.M. Jones <rjones@redhat.com> - 5.4-4
- Add fix for OCaml 4.04 (thanks: Jaroslav Škarvada).

* Sat Nov 05 2016 Richard W.M. Jones <rjones@redhat.com> - 5.4-3
- Rebuild for OCaml 4.04.0.

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.4-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jun 29 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 5.4-1
- New version
  Resolves: rhbz#1350990
- Dropped xw-fonts-fix and async-wait patches (both upstreamed)

* Fri May 13 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 5.3.1-8
- Fixed async wait to handle zero timeouts (by async-wait patch)

* Wed May  4 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 5.3.1-7
- Made brltty-config executable, currently useless, but FHS compliant
  Resolves: rhbz#1332981

* Mon Apr 11 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 5.3.1-6
- Improved fix for XW driver not showing Braille characters
  Related: rhbz#1324669

* Thu Apr  7 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 5.3.1-5
- Fixed XW driver to show Braille characters
  Related: rhbz#1324669
- No need to explicitly harden
- Added architecture to subpackages requirements
- Made brltty main package to explicitly requires specific brlapi version
- Renumbered patches

* Tue Apr  5 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 5.3.1-4
- Dropped man-fix patch (upstreamed)
- Hardened build
  Related: rhbz#1092547

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 23 2015 Jon Ciesla <limburgher@gmail.com> - 5.3.1-2
- Bump rel, api is the same.

* Wed Dec 23 2015 Jon Ciesla <limburgher@gmail.com> - 5.3.1-1
- 5.3.1, BZ 1293612.

* Tue Dec 15 2015 Jon Ciesla <limburgher@gmail.com> - 5.3-1
- 5.3, BZ 1291657.
- Man fix upstreamed.

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2-12
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 5.2-11
- OCaml 4.02.3 rebuild.

* Wed Jun 24 2015 Richard W.M. Jones <rjones@redhat.com> - 5.2-10
- ocaml-4.02.2 final rebuild.

* Wed Jun 17 2015 Richard W.M. Jones <rjones@redhat.com> - 5.2-9
- ocaml-4.02.2 rebuild.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 25 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 5.2-7
- Fixed manual page
  Resolves: rhbz#1224661

* Mon Mar 23 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 5.2-6
- Dropped AtSpi driver
  Related: rhbz#1204462

* Mon Mar 23 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 5.2-5
- Added support for AtSpi2 driver
  Resolves: rhbz#1204462
- Added support for eSpeak driver
- Filtered private libraries from provides/requires

* Tue Feb 17 2015 Richard W.M. Jones <rjones@redhat.com> - 5.2-4
- ocaml-4.02.1 rebuild.

* Tue Feb 17 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 5.2-3
- Rebuilt for new ocaml

* Mon Jan 26 2015 David Tardon <dtardon@redhat.com> - 5.2-2
- rebuild for ICU 54.1

* Wed Nov 12 2014 Jon Ciesla <limburgher@gmail.com> - 5.2-1
- 5.2, BZ 1163112.

* Sun Aug 31 2014 Richard W.M. Jones <rjones@redhat.com> - 5.1-12
- ocaml-4.02.0 final rebuild.

* Tue Aug 26 2014 David Tardon <dtardon@redhat.com> - 5.1-11
- rebuild for ICU 53.1

* Sat Aug 23 2014 Richard W.M. Jones <rjones@redhat.com> - 5.1-10
- ocaml-4.02.0+rc1 rebuild.

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 02 2014 Richard W.M. Jones <rjones@redhat.com> - 5.1-8
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Mon Jul 21 2014 Richard W.M. Jones <rjones@redhat.com> - 5.1-7
- OCaml 4.02.0 beta rebuild (with fixed compiler).

* Mon Jul 14 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 5.1-6
- Rebuilt for new ocaml

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue May 20 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 5.1-3
- Rebuilt for tcl/tk8.6

* Tue Apr 15 2014 Richard W.M. Jones <rjones@redhat.com> - 5.1-2
- Remove ocaml_arches macro (RHBZ#1087794).

* Thu Mar 27 2014 Jon Ciesla <limburgher@gmail.com> - 5.1-1
- 5.1, BZ 1081459.
- Fixed Source URL.

* Thu Feb 20 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 5.0-1
- New version
  Resolves: rhbz#1067337
- Dropped man-fix patch (upstreamed)
- De-fuzzified libspeechd patch
- Handled locales
- Switched to xz compressed sources

* Thu Feb 13 2014 Jon Ciesla <limburgher@gmail.com> - 4.5-10
- libicu rebuild.
- Add python-setuptools BR.

* Mon Sep 23 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 4.5-9
- The brlapi.key is now preset, users in the brlapi group have access
  Resolves: rhbz#1010656

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 4.5-8
- Rebuild for OCaml 4.01.0.
- Create stublibs directory for OCaml, else install fails.
- Unset MAKEFLAGS so that MAKEFLAGS=-j<N> does not break local builds.
- In new speech-dispatcher, <libspeechd.h> has moved to a subdirectory.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 4.5-6
- Updated man page

* Fri May 10 2013 Jon Ciesla <limburgher@gmail.com> - 4.5-5
- Add systemd unit file, BZ 916628.
- Drop spurious post scripts.
- Move eveything but man pages and license files top -docs.

* Thu May  9 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 4.5-4
- Conditionally build python3

* Tue Apr 30 2013 Jon Ciesla <limburgher@gmail.com> - 4.5-3
- Add bluetooth support, BZ 916628.

* Thu Apr 04 2013 Kalev Lember <kalevlember@gmail.com> - 4.5-2
- Don't install the library in /lib now that we have UsrMove

* Thu Apr 04 2013 Kalev Lember <kalevlember@gmail.com> - 4.5-1
- Update to 4.5
- Add Python 3 support (python3-brlapi)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  8 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 4.3-12
- Build with -fno-strict-aliasing

* Wed Dec 19 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 4.3-11
- revbump after jnidir change

* Wed Dec 12 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 4.3-10
- Fixed directories, install to /usr prefix

* Wed Dec 12 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 4.3-9
- Fix up java subpackage installation directories
- Fix java JNI loading code

* Wed Oct 17 2012 Jon Ciesla <limburgher@gmail.com> - 4.3-8
- Bump and rebuild for new ocaml.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Jon Ciesla <limburgher@gmail.com> - 4.3-6
- Bump and rebuild for ocaml 4.00.0.

* Fri Mar 23 2012 Dan Horák <dan[at]danny.cz> - 4.3-5
- conditionalize ocaml support
- fix build on 64-bit arches

* Mon Feb 06 2012 Jon Ciesla <limburgher@gmail.com> - 4.3-4
- Added ocaml subpackage, BZ 702724.

* Fri Feb 03 2012 Jon Ciesla <limburgher@gmail.com> - 4.3-3
- Fixed libbrlapi.so symlink, BZ 558132.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 18 2011 Jon Ciesla <limb@jcomserv.net> - 4.3-1
- New upstream.
- S_ISCHR patch upstreamed.
- parallel patch updated.
- Cleaned up some file encodings.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri May 21 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 4.2-2
- rework parallel patch slightly and reapply

* Fri May 21 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 4.2-1
- update to 4.2
- drop static lib (bz 556041)
- fix undefined S_ISCHR call

* Wed Jan 20 2010 Stepan Kasal <skasal@redhat.com> - 4.1-5
- requires(post): coreutils to work around an installator bug
- Resolves: #540437

* Wed Jan 13 2010 Stepan Kasal <skasal@redhat.com> - 4.1-4
- limit building against speech-dispatcher to Fedora
- Resolves: rhbz#553795

* Sun Nov  1 2009 Stepan Kasal <skasal@redhat.com> - 4.1-3
- build the TTY driver (it was disabled since it first appered in 3.7.2-1)
- build with speech-dispatcher, packed into a separate sub-package

* Fri Oct 30 2009 Stepan Kasal <skasal@redhat.com> - 4.1-2
- move data-directory back to default: /etc/brltty
- move brltty to /bin and /lib, so that it can be used to repair the system
  without /usr mounted (#276181)
- move vstp and libbrlttybba.so to brlapi
- brltty no longer requires brlapi
- brlapi now requires brltty from the same build

* Wed Oct 28 2009 Stepan Kasal <skasal@redhat.com> - 4.1-1
- new upstream version
- use --disable-stripping instead of make variable override
- install the default brltty-pm.conf to docdir only (#526168)
- remove the duplicate copies of rhmkboot and rhmkroot from docdir
- patch configure so that the dirs in summary are not garbled:
  brltty-autoconf-quote.patch
- move data-directory to ${datadir}/brltty

* Tue Oct 20 2009 Stepan Kasal <skasal@redhat.com> - 4.0-2
- escape rpm macros in the rpm change log
- add requires to bind subpackages from one build together

* Wed Oct  7 2009 Stepan Kasal <skasal@redhat.com> - 4.0-1
- new upstream version
- drop upstreamed patches; ./autogen not needed anymore
- pack the xbrlapi server; move its man page to brlapi package
- add man-page for brltty.conf (#526168)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 12 2009 Stepan Kasal <skasal@redhat.com> - 3.10-5
- rebuild after java-1.5.0-gcj rebuild

* Thu Apr 30 2009 Stepan Kasal <skasal@redhat.com> - 3.10-4
- own the tcl subdirectory (#474032)
- set CPPFLAGS to java include dirs, so that the java bindings build with
  any java implementation (#498964)
- add --without-curses; there is no curses package BuildRequired anyway

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 3.10-2
- Rebuild for Python 2.6

* Sat Sep 13 2008 Stepan Kasal <skasal@redhat.com> - 3.10-1
- new upstream release
- drop brltty-3.9-java-svn.patch, brltty-3.9-tcl85path.patch,
  and brltty-3.9-pyxfix.patch, they are upstream
- fix BuildRoot
- fix many sub-packages' Requires on brlapi

* Wed Sep 10 2008 Stepan Kasal <skasal@redhat.com> - 3.9-3
- add brltty-3.9-autoconf.patch to fix to build with Autoconf 2.62
- add brltty-3.9-parallel.patch to fix race condition with parallel make
- add brltty-3.9-pyxfix.patch to fix build with current pyrex
- Summary lines shall not end with a dot

* Thu Feb 28 2008 Tomas Janousek <tjanouse@redhat.com> - 3.9-2.2
- glibc build fixes
- applied java reorganisations from svn

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.9-2.1
- Autorebuild for GCC 4.3

* Wed Jan 09 2008 Tomas Janousek <tjanouse@redhat.com> - 3.9-1.1
- specfile update to comply with tcl packaging guidelines

* Mon Jan 07 2008 Tomas Janousek <tjanouse@redhat.com> - 3.9-1
- update to latest upstream (3.9)

* Tue Sep 18 2007 Tomas Janousek <tjanouse@redhat.com> - 3.8-2.svn3231
- update to r3231 from svn
- added java binding subpackage

* Wed Aug 29 2007 Tomas Janousek <tjanouse@redhat.com> - 3.8-2.svn3231
- update to r3231 from svn

* Tue Aug 21 2007 Tomas Janousek <tjanouse@redhat.com> - 3.8-1
- update to latest upstream
- added the at-spi driver, tcl and python bindings
- fixed the license tags

* Mon Mar 05 2007 Tomas Janousek <tjanouse@redhat.com> - 3.7.2-3
- added the XWindow driver
- build fix for newer byacc

* Tue Jan 30 2007 Tomas Janousek <tjanouse@redhat.com> - 3.7.2-2.1
- quiet postinstall scriptlet, really fixes #224570

* Tue Jan 30 2007 Tomas Janousek <tjanouse@redhat.com> - 3.7.2-2
- failsafe postinstall script, fixes #224570
- makefile fix - debuginfo extraction now works

* Thu Jan 25 2007 Tomas Janousek <tjanouse@redhat.com> - 3.7.2-1.1
- fix building with newer kernel-headers (#224149)

* Wed Jul 12 2006 Petr Rockai <prockai@redhat.com> - 3.7.2-1
- upgrade to latest upstream version
- split off brlapi and brlapi-devel packages

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.2-12.1
- rebuild

* Sun Jul 02 2006 Florian La Roche <laroche@redhat.com>
- for the post script require coreutils

* Mon Jun 05 2006 Jesse Keating <jkeating@redhat.com> - 3.2-11
- Added byacc BuildRequires, removed prereq, coreutils is always there

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.2-10.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.2-10.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar 16 2005 Bill Nottingham <notting@redhat.com> 3.2-10
- rebuild

* Fri Nov 26 2004 Florian La Roche <laroche@redhat.com>
- add a %%clean into .spec

* Thu Oct 14 2004 Adrian Havill <havill@redhat.com> 3.2-5
- chmod a-x for conf file (#116244)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Sep 30 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- prereq coreutils for mknod/chown/chmod

* Mon Jul 07 2003 Adrian Havill <havill@redhat.com> 3.2-2
- changed spec "Copyright" to "License"
- use %%configure macro, %%{_libdir} for non-ia32 archs
- removed unnecessary set and unset, assumed/default spec headers
- fixed unpackaged man page, duplicate /bin and /lib entries
- use plain install vs scripts for non-i386 buildsys
