%global major 60
Summary:        SpiderMonkey JavaScript library
Name:           mozjs%{major}
Version:        60.9.0
Release:        11%{?dist}
License:        MPLv2.0 AND MPLv1.1 AND BSD AND GPLv2+ AND GPLv3+ AND LGPLv2+ AND AFL AND ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey
#Source0:      https://ftp.mozilla.org/pub/firefox/releases/60.9.0esr/source/firefox-60.9.0esr.source.tar.xz
Source0:        https://ftp.mozilla.org/pub/firefox/releases/%{version}esr/source/%{name}-%{version}.tar.xz
Patch0:         init_patch.patch
Patch1:         emitter.patch
Patch2:         fix-soname.patch
Patch3:         copy-headers.patch
Patch4:         Always-use-the-equivalent-year-to-determine-the-time-zone.patch
Patch5:         icu_sources_data.py-Decouple-from-Mozilla-build-system.patch
Patch6:         icu_sources_data-Write-command-output-to-our-stderr.patch
Patch7:    CVE-2023-22895.patch
BuildRequires:  autoconf213
BuildRequires:  gcc
BuildRequires:  libffi
BuildRequires:  perl
BuildRequires:  python-xml
BuildRequires:  python2-devel
BuildRequires:  readline-devel
BuildRequires:  zlib
# Firefox does not allow to build with system version of jemalloc
Provides:       bundled(jemalloc) = 4.3.1

%description
SpiderMonkey is the code-name for Mozilla Firefox's C++ implementation of
JavaScript. It is intended to be embedded in other applications
that provide host environments for JavaScript.

%package devel
Summary:        Development files for %{name}
Group:          Development/Tools
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}

%prep
%setup -q -n firefox-%{version}/js/src

pushd ../..
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
# make sure we don't ever accidentally link against bundled security libs
rm -rf ../../security/
popd

# Remove zlib directory (to be sure using system version)
rm -rf ../../modules/zlib

%build
# Enable LTO
export AR=%{_bindir}/gcc-ar
export RANLIB=%{_bindir}/gcc-ranlib
export NM=%{_bindir}/gcc-nm

export CFLAGS="%{optflags}"

export CXXFLAGS="$CFLAGS"
export LINKFLAGS="%{?__global_ldflags}"

autoconf-2.13
%configure \
  --without-system-icu \
  --enable-posix-nspr-emulation \
  --with-system-zlib \
  --disable-strip \
  --with-intl-api \
  --enable-readline \
  --enable-shared-js \
  --disable-optimize \
  --enable-pie \
  --disable-jemalloc \

%make_build
cp ../../LICENSE .

%install
%make_install

# Remove unneeded files
rm %{buildroot}%{_bindir}/js%{major}-config
rm %{buildroot}%{_libdir}/libjs_static.ajs

# Rename library and create symlinks, following fix-soname.patch
mv %{buildroot}%{_libdir}/libmozjs-%{major}.so \
   %{buildroot}%{_libdir}/libmozjs-%{major}.so.0.0.0
ln -s libmozjs-%{major}.so.0.0.0 %{buildroot}%{_libdir}/libmozjs-%{major}.so.0
ln -s libmozjs-%{major}.so.0 %{buildroot}%{_libdir}/libmozjs-%{major}.so

%check
# Run SpiderMonkey tests
python2 tests/jstests.py -d -s -t 1800 --no-progress ../../js/src/js/src/shell/js
# Run basic JIT tests
python2 jit-test/jit_test.py -s -t 1800 --no-progress ../../js/src/js/src/shell/js basic

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSE
%{_libdir}/libmozjs-%{major}.so.0*

%files devel
%defattr(-,root,root)
%{_bindir}/js%{major}
%{_libdir}/libmozjs-%{major}.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/mozjs-%{major}/

%changelog
* Tue Jan 17 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 60.9.0-11
- Add patch for CVE-2023-22895

* Mon Jul 26 2021 Shane Guan <shaneguan@microsoft.com> - 60.9.0-10
- Make a symlink to /run/shm called /dev/shm so this spec will work on WSL.
- Spec linting.

*   Tue Jan 05 2021 Andrew Phelps <anphel@microsoft.com> 60.9.0-9
-   Fix calls to python2 in check section

*   Thu May 28 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 60.9.0-8
-   Removing unused "/usr/bin/zip" built-time requirement.

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 60.9.0-7
-   Added %%license line automatically

*   Wed Apr 15 2020 Nicolas Ontiveros <niontive@microsoft.com> 60.9.0-6
-   Initial CBL-Mariner import from Fedora 32 (license: MIT).
-   License verified.
-   Remove unused patches.
-   Remove big endian support.

*   Mon Feb 17 2020 Kalev Lember <klember@redhat.com> - 60.9.0-5
-   Update enddianness.patch with more s390x fixes
-   Enable tests on s390x again 

*   Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 60.9.0-4
-   Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

*   Tue Sep 10 2019 Kalev Lember <klember@redhat.com> - 60.9.0-3
-   Fix multilib conflicts in js-config.h 

*   Sat Sep 07 2019 Kalev Lember <klember@redhat.com> - 60.9.0-2
-   Backport patches for s390x support 

*   Tue Sep 03 2019 Kalev Lember <klember@redhat.com> - 60.9.0-1
-   Update to 60.9.0 

*   Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 60.8.0-3
-   Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild 

*   Wed Jul 10 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 60.8.0-2
-   Enable LTO 

*   Tue Jul 09 2019 Frantisek Zatloukal <fzatlouk@redhat.com> - 60.8.0-1
-   Update to 60.8.0 

*   Sat Jun 22 2019 Frantisek Zatloukal <fzatlouk@redhat.com> - 60.7.2-1
-   Update to 60.7.2

*   Wed Jun 19 2019 Frantisek Zatloukal <fzatlouk@redhat.com> - 60.7.1-1
-   Update to 60.7.1 

*   Tue May 21 2019 Kalev Lember <klember@redhat.com> - 60.7.0-1
-   Update to 60.7.0 

*   Mon Apr 15 2019 Frantisek Zatloukal <fzatlouk@redhat.com> - 60.6.1-2
-   Backport two Firefox 61 patches and allow compiler optimizations on aarch64 

*   Sun Apr 14 2019 Frantisek Zatloukal <fzatlouk@redhat.com> - 60.6.1-1
-   Update to 60.6.1 

*   Thu Feb 21 2019 Frantisek Zatloukal <fzatlouk@redhat.com> - 60.4.0-5
-   Re-enable null pointer gcc optimization 

*   Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 60.4.0-4
-   Rebuild for readline 8.0 

*   Thu Feb 14 2019 Frantisek Zatloukal <fzatlouk@redhat.com> - 60.4.0-3
-   Build aarch64 with -O0 because of rhbz#1676292 

*   Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 60.4.0-2
-   Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild 

*   Wed Jan 02 2019 Frantisek Zatloukal <fzatlouk@redhat.com> - 60.4.0-1
-   Update to 60.4.0

*   Mon Nov 12 2018 Kalev Lember <klember@redhat.com> - 60.3.0-1
-   Update to 60.3.0 

*   Thu Oct 04 2018 Kalev Lember <klember@redhat.com> - 60.2.2-1
-   Update to 60.2.2 

*   Fri Sep 28 2018 Kalev Lember <klember@redhat.com> - 60.2.1-1
-   Update to 60.2.1 

*   Tue Sep 11 2018 Kalev Lember <klember@redhat.com> - 60.2.0-1
-   Update to 60.2.0

*   Tue Sep 04 2018 Frantisek Zatloukal <fzatlouk@redhat.com> - 60.1.0-1
-   Update to 60.1.0 

*   Wed Jul 25 2018 Kalev Lember <klember@redhat.com> - 52.9.0-1
-   Update to 52.9.0 

*   Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 52.8.0-3
-   Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild 

*   Mon Jun 11 2018 Ray Strode <rstrode@redhat.com> - 52.8.0-2
-   safeguard against linking against bundled nss
-   Related: #1563708

*   Fri May 11 2018 Kalev Lember <klember@redhat.com> - 52.8.0-1
-   Update to 52.8.0
-   Fix the build on ppc
-   Disable JS Helper threads on ppc64le (#1523121)

*   Sat Apr 07 2018 Kalev Lember <klember@redhat.com> - 52.7.3-1
-   Update to 52.7.3 

*   Tue Mar 20 2018 Kalev Lember <klember@redhat.com> - 52.7.2-1
-   Update to 52.7.2
-   Switch to %%ldconfig_scriptlets

*   Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 52.6.0-2
-   Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild 

*   Tue Jan 23 2018 Kalev Lember <klember@redhat.com> - 52.6.0-1
-   Update to 52.6.0 

*   Fri Nov 24 2017 Bjรถrn Esser <besser82@fedoraproject.org> - 52.5.0-5
-   SpiderMonkey tests have regressions on %%{power64}, too 

*   Fri Nov 24 2017 Bjรถrn Esser <besser82@fedoraproject.org> - 52.5.0-4
-   SpiderMonkey tests have regressions on big endian platforms 

*   Fri Nov 24 2017 Bjรถrn Esser <besser82@fedoraproject.org> - 52.5.0-3
-   SpiderMonkey tests do not fail on any arch
-   Basic JIT tests are failing on s390 arches, only
-   Use macro for ppc64 arches
-   Run tests using Python2 explicitly
-   Simplify %%check
-   Use the %%{major} macro consequently
-   Replace %%define with %%global

*   Fri Nov 24 2017 Bjรถrn Esser <besser82@fedoraproject.org> - 52.5.0-2
-   Use macro for Python 2 interpreter
-   Use proper export and quoting 

*   Tue Nov 14 2017 Kalev Lember <klember@redhat.com> - 52.5.0-1
-   Update to 52.5.0 

*   Tue Oct 31 2017 Kalev Lember <klember@redhat.com> - 52.4.0-3
-   Include standalone /usr/bin/js52 interpreter

*   Tue Oct 31 2017 Kalev Lember <klember@redhat.com> - 52.4.0-2
-   Various secondary arch fixes 

*   Thu Sep 28 2017 Kalev Lember <klember@redhat.com> - 52.4.0-1
-   Update to 52.4.0 

*   Wed Sep 20 2017 Kalev Lember <klember@redhat.com> - 52.3.0-1
-   Initial Fedora packaging, based on earlier mozjs45 work
