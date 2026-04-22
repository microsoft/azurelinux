# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_without emacs
%global mver 1.8

Summary: A GNU implementation of Scheme for application extensibility
Name: compat-guile18
Version: %{mver}.8
Release: 49%{?dist}
Source: ftp://ftp.gnu.org/pub/gnu/guile/guile-%{version}.tar.gz
URL: http://www.gnu.org/software/guile/
Patch1: guile-1.8.7-multilib.patch
Patch2: guile-1.8.7-testsuite.patch
Patch3: guile-1.8.8-deplibs.patch
Patch4: guile-1.8.8-cve-2016-8605.patch
Patch5: guile-1.8.8-configure.patch
Patch6: guile-configure-tz-c99.patch
License: LGPL-2.1-or-later AND GPL-2.0-or-later AND MIT AND BSD-4-Clause-UC
BuildRequires: gcc libtool libtool-ltdl-devel gmp-devel readline-devel
BuildRequires: gettext-devel
BuildRequires: make
BuildRequires: chrpath
BuildRequires: libxcrypt-devel
%{?with_emacs:BuildRequires: emacs}
Provides: guile = 5:%{version}-7
Provides: guile%{?_isa} = 5:%{version}-7
Obsoletes: guile < 5:%{version}-7

%description
GUILE (GNU's Ubiquitous Intelligent Language for Extension) is a library
implementation of the Scheme programming language, written in C.  GUILE
provides a machine-independent execution platform that can be linked in
as a library during the building of extensible programs.

Install the compat-guile18 package if you'd like to add extensibility to
programs that you are developing.

%package devel
Summary: Libraries and header files for the GUILE extensibility library
Requires: %{name}%{?_isa} = %{version}-%{release} gmp-devel
Requires: pkgconfig
Provides: guile-devel = 5:%{version}-7
Provides: guile-devel%{?_isa} = 5:%{version}-7
Obsoletes: guile-devel < 5:%{version}-7

%description devel
The compat-guile18-devel package includes the libraries, header files, etc.,
that you'll need to develop applications that are linked with the
GUILE extensibility library.

You need to install the compat-guile18-devel package if you want to develop
applications that will be linked to GUILE.  You'll also need to install the
compat-guile18 package.

%prep
%setup -q -n guile-%{version}

%patch -P1 -p1 -b .multilib
%patch -P2 -p1 -b .testsuite
%patch -P3 -p1 -b .deplibs
%patch -P4 -p1 -b .cve-2016-8605
%patch -P5 -p1 -b .configure
%patch -P6 -p1

%build

export CFLAGS="$RPM_OPT_FLAGS -fwrapv -std=gnu17"
export LDFLAGS="$RPM_LD_FLAGS -Wl,--as-needed"
%configure --disable-static --disable-error-on-warning --disable-rpath

# Remove RPATH
sed -i 's|" $sys_lib_dlsearch_path "|" $sys_lib_dlsearch_path %{_libdir} "|' \
    {,guile-readline/}libtool

make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/guile/site

rm -f ${RPM_BUILD_ROOT}%{_libdir}/libguile*.la

# Necessary renaming and removing
rm -rf ${RPM_BUILD_ROOT}%{_infodir}
mv ${RPM_BUILD_ROOT}%{_bindir}/guile{,%{mver}}
mv ${RPM_BUILD_ROOT}%{_bindir}/guile{,%{mver}}-tools
mv ${RPM_BUILD_ROOT}%{_mandir}/man1/guile{,%{mver}}.1
mv ${RPM_BUILD_ROOT}%{_bindir}/guile{,%{mver}}-config
mv ${RPM_BUILD_ROOT}%{_bindir}/guile{,%{mver}}-snarf
mv ${RPM_BUILD_ROOT}%{_datadir}/aclocal/guile{,%{mver}}.m4
sed -i -e 's|/usr/bin/guile|/usr/bin/guile%{mver}|' \
    ${RPM_BUILD_ROOT}%{_bindir}/guile%{mver}-config
sed -i -e 's|guile-tools|guile%{mver}-tools|g' \
    ${RPM_BUILD_ROOT}%{_bindir}/guile%{mver}-tools
sed -i -e 's|guile-snarf|guile%{mver}-snarf|g' \
    ${RPM_BUILD_ROOT}%{_bindir}/guile%{mver}-snarf

ac=${RPM_BUILD_ROOT}%{_datadir}/aclocal/guile%{mver}.m4
sed -i -e 's|,guile|,guile%{mver}|g' $ac
sed -i -e 's|guile-tools|guile%{mver}-tools|g' $ac
sed -i -e 's|guile-config|guile%{mver}-config|g' $ac
sed -i -e 's|GUILE_PROGS|GUILE1_8_PROGS|g' $ac
sed -i -e 's|GUILE_FLAGS|GUILE1_8_FLAGS|g' $ac
sed -i -e 's|GUILE_SITE_DIR|GUILE1_8_SITE_DIR|g' $ac
sed -i -e 's|GUILE_CHECK|GUILE1_8_CHECK|g' $ac
sed -i -e 's|GUILE_MODULE_CHECK|GUILE1_8_MODULE_CHECK|g' $ac
sed -i -e 's|GUILE_MODULE_AVAILABLE|GUILE1_8_MODULE_AVAILABLE|g' $ac
sed -i -e 's|GUILE_MODULE_REQUIRED|GUILE1_8_MODULE_REQUIRED|g' $ac
sed -i -e 's|GUILE_MODULE_EXPORTS|GUILE1_8_MODULE_EXPORTS|g' $ac
sed -i -e 's|GUILE_MODULE_REQUIRED_EXPORT|GUILE1_8_MODULE_REQUIRED_EXPORT|g' $ac

# Compress large documentation
bzip2 NEWS

touch $RPM_BUILD_ROOT%{_datadir}/guile/%{mver}/slibcat
ln -s ../../slib $RPM_BUILD_ROOT%{_datadir}/guile/%{mver}/slib

chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libguile-srfi-srfi-1-v-3.so.3.0.2
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libguile-srfi-srfi-4-v-3.so.3.0.1
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libguile-srfi-srfi-13-14-v-3.so.3.0.1
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libguile-srfi-srfi-60-v-2.so.2.0.2
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/guile1.8

%check
make %{?_smp_mflags} check

%ldconfig_scriptlets

%triggerin -- slib
# Remove files created in guile < 1.8.3-2
rm -f %{_datadir}/guile/site/slib{,cat}

ln -sfT ../../slib %{_datadir}/guile/%{mver}/slib
rm -f %{_datadir}/guile/%{mver}/slibcat
export SCHEME_LIBRARY_PATH=%{_datadir}/slib/

# Build SLIB catalog
for pre in \
    "(use-modules (ice-9 slib))" \
    "(load \"%{_datadir}/slib/guile.init\")"
do
    %{_bindir}/guile%{mver} -c "$pre
        (set! implementation-vicinity (lambda ()
        \"%{_datadir}/guile/%{mver}/\"))
        (require 'new-catalog)" &> /dev/null && break
    rm -f %{_datadir}/guile/%{mver}/slibcat
done
:

%triggerun -- slib
if [ "$2" = 0 ]; then
    rm -f %{_datadir}/guile/%{mver}/slib{,cat}
fi

%files
%doc AUTHORS COPYING* ChangeLog HACKING NEWS.bz2 README THANKS
%{_bindir}/guile%{mver}
%{_bindir}/guile%{mver}-tools
%{_libdir}/libguile*.so.*
# The following unversioned libraries are needed in runtime
%{_libdir}/libguilereadline-*.so
%{_libdir}/libguile-srfi-srfi-*.so
%dir %{_datadir}/guile
%dir %{_datadir}/guile/%{mver}
%{_datadir}/guile/%{mver}/ice-9
%{_datadir}/guile/%{mver}/lang
%{_datadir}/guile/%{mver}/oop
%{_datadir}/guile/%{mver}/scripts
%{_datadir}/guile/%{mver}/srfi
%{_datadir}/guile/%{mver}/guile-procedures.txt
%ghost %{_datadir}/guile/%{mver}/slibcat
%ghost %{_datadir}/guile/%{mver}/slib
%dir %{_datadir}/guile/site
%if %{with emacs}
%dir %{_datadir}/emacs/site-lisp
%{_datadir}/emacs/site-lisp/*.el
%endif
%{_mandir}/man1/guile%{mver}.1*

%files devel
%{_bindir}/guile%{mver}-config
%{_bindir}/guile%{mver}-snarf
%{_datadir}/aclocal/*
%{_libdir}/libguile.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/guile
%{_includedir}/libguile
%{_includedir}/libguile.h

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Feb 01 2025 Björn Esser <besser82@fedoraproject.org> - 1.8.8-47
- Add explicit BR: libxcrypt-devel

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Mar 10 2023 Tomas Korbar <tkorbar@redhat.com> - 1.8.8-41
- List all licenses that are used in shipped files
- This is neccessary according to current interpretation
  of fedora packaging guidelines

* Wed Mar 01 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.8.8-40
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 12 2023 Florian Weimer <fweimer@redhat.com> - 1.8.8-38
- C99 compatibility fix for the configure script

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 27 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.8.8-34
- Disable RPATH.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Jeff Law <law@redhat.com> - 1.8.8-30
- Add noipa,noinline,noclone attributes to find_stack_direction to
  prevent it from being self-inlined and computing the wrong direction
  for stack growth

* Mon Aug 19 2019 Tomas Korbar <tkorbar@redhat.com> - 1.8.8-29
- 1735045 - compat-guile18: FTBFS in Fedora rawhide/f31
- Remove 'obsolete' tag containing architecture from devel subpackage

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.8.8-27
- Rebuild for readline 8.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 1.8.8-25
- Rebuilt for libcrypt.so.2 (#1666033)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue May 22 2018 Miroslav Lichvar <mlichvar@redhat.com> - 1.8.8-23
- Use macro for ldconfig scriptlets
- Add gcc to build requirements

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Feb  1 2018 Florian Weimer <fweimer@redhat.com> - 1.8.8-21
- Use LDFLAGS from redhat-rpm-config

* Mon Jan 29 2018 Miroslav Lichvar <mlichvar@redhat.com> - 1.8.8-20
- Remove incorrect arch-specific Obsoletes (#1537209)

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 1.8.8-19
- Rebuilt for switch to libxcrypt

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.8.8-15
- Rebuild for readline 7.x

* Wed Oct 12 2016 Miroslav Lichvar <mlichvar@redhat.com> - 1.8.8-14
- Remove thread-unsafe umask modification in mkdir (CVE-2016-8605)

* Wed Feb 17 2016 Miroslav Lichvar <mlichvar@redhat.com> - 1.8.8-13
- Add -fwrapv to CFLAGS (#1307394)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jul 15 2015 Miroslav Lichvar <mlichvar@redhat.com> - 1.8.8-11
- Fix building with new glibc (#1239406)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Jan Synáček <jsynacek@redhat.com> - 1.8.8-5
- Add additional Provides and Obsoletes with %%{?_isa} to fix upgrade path

* Fri Jan 18 2013 Jan Synáček <jsynacek@redhat.com> - 1.8.8-4
- Bump Provides/Obsoletes by a release
- Add Provides/Obsoletes to -devel package as well
- Add a comment about unversion libraries
- Fix mixed tabs/spaces (remove tabs)

* Thu Jan 17 2013 Jan Synáček <jsynacek@redhat.com> - 5:1.8.8-3
- Move .so files back to the main package (needed in runtime)

* Thu Jan 17 2013 Jan Synáček <jsynacek@redhat.com> - 5:1.8.8-2
- Move unversioned .so files to -devel package
- Remove unnecessary %%clear
- Use %%global instead of %%define
- Remove unnecessary (compatible) licenses
- Fix %%post onliner
- Compile with --as-needed
- Add _isa flag where appropriate
- Correctly specify Provides and Obsoletes
- Rename to guile-compat18

* Fri Oct 19 2012 Jan Synáček <jsynacek@redhat.com> - 5:1.8.8-1
- Make compat-package
