## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 6;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# This specfile is almost identical with Mlichvars
# specfile for guile 2.2, in ideal world, we would
# just rebase guile 2.2 to guile 3.0 but we do not
# live in ideal world and we need to maintain both
# guile 2.2 and guile 3 in Fedora. Thus this note
# is giving credit to Mlichvar for all the delicate
# mechanisms in this package.

# Guile produces ELF images that are just containers for guile and don't
# include build-ids. https://wingolog.org/archives/2014/01/19/elf-in-guile
%undefine _missing_build_ids_terminate_build

%global mver 3.0

Name: guile30
Version: 3.0.9
Release: %autorelease
Summary: A GNU implementation of Scheme for application extensibility
# Automatically converted from old format: LGPLv3+ and MIT and Public Domain and GPL+ and GPLv3+ - review is highly recommended.
License: LGPL-3.0-or-later AND LicenseRef-Callaway-MIT AND LicenseRef-Callaway-Public-Domain AND GPL-1.0-or-later AND GPL-3.0-or-later
Source: https://ftp.gnu.org/gnu/guile/guile-%{version}.tar.gz
URL: https://www.gnu.org/software/guile/

BuildRequires: libtool libtool-ltdl-devel pkgconfig(gmp) pkgconfig(readline)
BuildRequires: gettext-devel libunistring-devel pkgconfig(libffi) pkgconfig(bdw-gc)
BuildRequires: make gcc
BuildRequires: autoconf 
BuildRequires: pkgconfig
BuildRequires: libxcrypt-devel
Requires: coreutils

# Guile ships a patched version of localcharset from gnulib
# its version is v0.1-1157-gb03f418
Provides: bundled(gnulib)

# Our glibc is not compatible with expectations of guiles upstream
# some macros are undefined and that results in inability to compile.
# This patch forces guile to use bundled header with all neccessary macros.
Patch0: guile-3.0.7-headers.patch

# Out of memory test is not stable, so disable it.
Patch1: guile-3.0.7-disable-oom-test.patch

# add chdir call before chroot to make it more secure
Patch2: guile-3.0.7-chroot.patch

# Disable unstable stack overflow test
Patch4: guile-3.0.7-disable-stackoverflow-test.patch

%description
GUILE (GNU's Ubiquitous Intelligent Language for Extension) is a library
implementation of the Scheme programming language, written in C.  GUILE
provides a machine-independent execution platform that can be linked in
as a library during the building of extensible programs.

Install the guile package if you'd like to add extensibility to programs
that you are developing.

%package devel
Summary: Libraries and header files for the GUILE extensibility library
Requires: guile30%{?_isa} = %{version}-%{release} pkgconfig(gmp) pkgconfig(bdw-gc)
Requires: pkgconfig

%description devel
The guile-devel package includes the libraries, header files, etc.,
that you'll need to develop applications that are linked with the
GUILE extensibility library.

You need to install the guile-devel package if you want to develop
applications that will be linked to GUILE.  You'll also need to
install the guile package.

%prep
%autosetup -p1 -n guile-%version

%build
# guile is not ready for gnu23, reported upstream
# meanwhile revert standard back to gnu17
export CFLAGS="%{optflags} -std=gnu17"
autoreconf -fiv
%configure --disable-static --disable-error-on-warning --program-suffix=%{mver}

%make_build

%install
%make_install
mkdir -p %{buildroot}%{_datadir}/guile/site/%{mver}

rm -f %{buildroot}%{_libdir}/libguile*.la
rm -f %{buildroot}%{_infodir}/dir

for i in $(seq 1 11); do
  mv %{buildroot}%{_infodir}/guile{,-%{mver}}.info-$i
  sed -i -e 's/guile\.info/guile-%{mver}.info/' %{buildroot}%{_infodir}/guile-%{mver}.info-$i
  sed -i -e 's/\* Guile Reference: (guile)/* Guile %{mver} Reference: (guile-%{mver})/' %{buildroot}%{_infodir}/guile-%{mver}.info-$i
done
mv %{buildroot}%{_infodir}/guile{,-%{mver}}.info
sed -i -e 's/guile\.info/guile-%{mver}.info/' %{buildroot}%{_infodir}/guile-%{mver}.info
sed -i -e 's/\* Guile Reference: (guile)/* Guile %{mver} Reference: (guile-%{mver})/' %{buildroot}%{_infodir}/guile-%{mver}.info
mv %{buildroot}%{_infodir}/r5rs{,-%{mver}}.info
mv %{buildroot}%{_datadir}/aclocal/guile{,-%{mver}}.m4

# Our gdb doesn't support guile yet
rm -f %{buildroot}%{_libdir}/libguile*gdb.scm

for i in %{buildroot}%{_infodir}/goops.info; do
    iconv -f iso8859-1 -t utf-8 < $i > $i.utf8 && mv -f ${i}{.utf8,}
done

touch %{buildroot}%{_datadir}/guile/site/%{mver}/slibcat

# Adjust mtimes so they are all identical on all architectures.
# When guile.x86_64 and guile.i686 are installed at the same time on an x86_64 system,
# the *.scm files' timestamps change, as they normally reside in /usr/share/guile/.
# Their corresponding compiled *.go file go to /usr/lib64/, or /usr/lib/, depending on the arch.
# The mismatch in timestamps between *.scm and *.go files makes guile to compile itself
# everytime it's run. The following code adjusts the files so that their timestamps are the same
# for every file, but unique between builds.
# See https://bugzilla.redhat.com/show_bug.cgi?id=1208760.
find %{buildroot}%{_datadir} -name '*.scm' -exec touch -r "%{_specdir}/guile3.spec" '{}' \;
find %{buildroot}%{_libdir} -name '*.go' -exec touch -r "%{_specdir}/guile3.spec" '{}' \;

# Remove Libtool archive
rm %{buildroot}%{_libdir}/guile/%{mver}/extensions/guile-readline.la

%check
make %{?_smp_mflags} check || true

%triggerin -- slib >= 3b4-1
rm -f %{_datadir}/guile/site/%{mver}/slibcat
export SCHEME_LIBRARY_PATH=%{_datadir}/slib/

# Build SLIB catalog
%{_bindir}/guile%{mver} --fresh-auto-compile --no-auto-compile -c \
    "(use-modules (ice-9 slib)) (require 'new-catalog)" &> /dev/null || \
    rm -f %{_datadir}/guile/site/%{mver}/slibcat
:


%triggerun -- slib >= 3b4-1
if [ "$2" = 0 ]; then
    rm -f %{_datadir}/guile/site/%{mver}/slibcat
fi

%files
%license COPYING COPYING.LESSER LICENSE
%doc AUTHORS HACKING README THANKS
%{_bindir}/guild%{mver}
%{_bindir}/guile%{mver}
%{_bindir}/guile-tools%{mver}
%{_libdir}/libguile-%{mver}.so.1*
%{_libdir}/guile
%dir %{_datadir}/guile
%dir %{_datadir}/guile/site
%dir %{_datadir}/guile/%{mver}
%dir %{_datadir}/guile/site/%{mver}
%{_datadir}/guile/%{mver}/ice-9
%{_datadir}/guile/%{mver}/language
%{_datadir}/guile/%{mver}/oop
%{_datadir}/guile/%{mver}/rnrs
%{_datadir}/guile/%{mver}/scripts
%{_datadir}/guile/%{mver}/srfi
%{_datadir}/guile/%{mver}/sxml
%{_datadir}/guile/%{mver}/system
%{_datadir}/guile/%{mver}/texinfo
%{_datadir}/guile/%{mver}/web
%{_datadir}/guile/%{mver}/guile-procedures.txt
%{_datadir}/guile/%{mver}/*.scm
%{_datadir}/guile/%{mver}/scheme/*.scm
%dir %{_datadir}/guile/%{mver}/scheme
%ghost %{_datadir}/guile/site/%{mver}/slibcat
%{_infodir}/*
%{_mandir}/man1/guile%{?mver}*

%files devel
%{_bindir}/guile-config%{?mver}
%{_bindir}/guile-snarf%{?mver}
%{_datadir}/aclocal/*
%{_libdir}/libguile-%{mver}.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/guile

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 3.0.9-6
- test: add initial lock files

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Mar 10 2025 Tomas Korbar <tkorbar@redhat.com> - 3.0.9-4
- Bump release

* Mon Mar 10 2025 Tomas Korbar <tkorbar@redhat.com> - 3.0.9-3
- Bump release

* Mon Mar 10 2025 Tomas Korbar <tkorbar@redhat.com> - 3.0.9-2
- Bump release

* Mon Mar 03 2025 Tomas Korbar <tkorbar@redhat.com> - 3.0.9-1
- Revert rebase to 3.0.10 as the version is broken on i686

* Mon Mar 03 2025 Tomas Korbar <tkorbar@redhat.com> - 3.0.10-1
- Fix FTBFS and rebase to version 3.0.10

* Sat Feb 01 2025 Björn Esser <besser82@fedoraproject.org> - 3.0.9-6
- Add explicit BR: libxcrypt-devel

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 3.0.9-4
- convert license to SPDX

* Thu Aug 01 2024 Miro Hrončok <miro@hroncok.cz> - 3.0.9-3
- Rebuilt to regain libguile-3.0.so.1 RPM Provides
- Resolves: rhbz#2299414

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Mar 15 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 3.0.9-1
- Update to 3.0.9

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.7-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.7-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Oct 27 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 3.0.7-12
- Drop obsolete install-info scriptlets

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 13 2022 Florian Weimer <fweimer@redhat.com> - 3.0.7-9
- Port configure script to C99

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 14 2022 Tomas Korbar <tkorbar@redhat.com> - 3.0.7-6
- Fix license field

* Sat Jan 08 2022 Miro Hrončok <miro@hroncok.cz> - 3.0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/LIBFFI34

* Mon Aug 02 2021 Tomas Korbar <tkorbar@redhat.com> - 3.0.7-4
- Fix requires for devel package Resolves: rhbz#1989011

* Wed Jul 28 2021 Tomas Korbar <tkorbar@redhat.com> - 3.0.7-3
- Do not fail on test failure

* Wed Jul 28 2021 Tomas Korbar <tkorbar@redhat.com> - 3.0.7-2
- Fix sources

* Wed Jul 28 2021 Tomas Korbar <tkorbar@redhat.com> - 3.0.7-1
- Initial package
## END: Generated by rpmautospec
