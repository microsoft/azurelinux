%global	major 78

Summary:        Mozilla's JavaScript engine.
Name:           mozjs
Version:        78.10.0
Release:        6%{?dist}
License:        BSD AND MIT AND MPLv2.0 AND Unicode
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey
Source0:        https://ftp.mozilla.org/pub/firefox/releases/%{version}esr/source/firefox-%{version}esr.source.tar.xz
Patch0:         emitter.patch
Patch1:         emitter_test.patch
# Build fixes
Patch2:         init_patch.patch
Patch3:         spidermonkey_checks_disable.patch
Patch4:         fix-soname.patch
Patch5:         CVE-2022-48285.patch

BuildRequires:  autoconf
BuildRequires:  gcc
BuildRequires:  icu-devel
BuildRequires:  llvm
BuildRequires:  llvm-devel
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-xml
BuildRequires:  rust
BuildRequires:  which
BuildRequires:  zlib-devel

%if %{with_check}
BuildRequires:  python3-six
%endif

Requires:       icu
Requires:       python3
Requires:       python3-libs

Obsoletes:      mozjs60
Obsoletes:      mozjs68
Obsoletes:      js

Provides:       mozjs%{major} = %{version}-%{release}

%description
Mozilla's JavaScript engine includes a just-in-time compiler (JIT) that compiles
JavaScript to machine code, for a significant speed increase.

%package       devel
Summary:        mozjs devel
Group:          Development/Tools

Requires:       %{name} = %{version}-%{release}

%description   devel
This contains development tools and libraries for SpiderMonkey.

%prep
%autosetup -p1 -n firefox-%{version}
rm -rf modules/zlib

%build
cd js/src

%configure \
    --with-system-icu \
    --enable-readline \
    --disable-jemalloc \
%if %{with_check}
    --enable-tests \
%else
    --disable-tests \
%endif
    --with-system-zlib
%make_build

%install
cd js/src

%make_install
chmod -x %{buildroot}%{_libdir}/pkgconfig/*.pc
# remove non required files
rm %{buildroot}%{_libdir}/libjs_static.ajs
rm -rf %{buildroot}%{_prefix}/src
find %{buildroot} -type f -name "*.la" -delete -print

# Re-naming library and adding symbolic links to follow typical conventions for libraries.
mv %{buildroot}%{_libdir}/libmozjs-%{major}.so \
   %{buildroot}%{_libdir}/libmozjs-%{major}.so.0.0.0
ln -s libmozjs-%{major}.so.0.0.0 %{buildroot}%{_libdir}/libmozjs-%{major}.so.0
ln -s libmozjs-%{major}.so.0 %{buildroot}%{_libdir}/libmozjs-%{major}.so

%check
cd js/src

TEST_RESULT=0
# Run SpiderMonkey tests
PYTHONPATH=tests/lib python3 tests/jstests.py -d -s -t 1800 --no-progress --wpt=disabled ../../js/src/dist/bin/js%{major} || TEST_RESULT=$?

# Run basic JIT tests
PYTHONPATH=tests/lib python3 jit-test/jit_test.py -s -t 1800 --no-progress ../../js/src/dist/bin/js%{major} basic || TEST_RESULT=$?

if [[ $TEST_RESULT -ne 0 ]]
then
    echo "At least one of the tests failed. Look for all tests, which assign a value to the 'TEST_RESULT' variable."
fi
[[ $TEST_RESULT -eq 0 ]]

%post
%ldconfig_scriptlets

%postun
%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/js%{major}
%{_bindir}/js%{major}-config
%{_libdir}/libmozjs-%{major}.so.0*

%files devel
%defattr(-,root,root)
%{_includedir}/mozjs-%{major}
%{_libdir}/libmozjs-%{major}.so
%{_libdir}/pkgconfig/mozjs-%{major}.pc

%changelog
* Mon Oct 23 2023 Andrew Phelps <anphel@microsoft.com> - 78.10.0-6
- Replace BR for autoconf213 with autoconf

* Thu Sep 07 2023 Daniel McIlvaney <damcilva@microsoft.com> - 78.10.0-5
- Bump package to rebuild with rust 1.72.0

* Tue Jun 27 2023 Minghe Ren <mingheren@microsoft.com> - 78.10.0-4
- Add patch for CVE-2022-48285

* Wed Aug 31 2022 Olivia Crain <oliviacrain@microsoft.com> - 78.10.0-3
- Bump package to rebuild with stable Rust compiler

* Wed Sep 22 2021 Jon Slobodzian <joslobo@microsoft.com> - 78.10.0-2
- Initial CBL-Mariner import from Photon (license: Apache2)
- Fixing minor changelog formatting issues.
- Adding the 'fix-soname.patch' fix using Fedora 34 (license: MIT) as guidance.
- License verified.

* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> - 78.10.0-1
- Automatic Version Bump

* Fri Feb 19 2021 Alexey Makhalov <amakhalov@vmware.com> - 78.3.1-2
- Remove python2 requirements

* Mon Oct 05 2020 Ankit Jain <ankitja@vmware.com> - 78.3.1-1
- Updated to 78.3.1

* Tue Aug 25 2020 Ankit Jain <ankitja@vmware.com> - 68.11.0-2
- Removed autoconf213 dependency and obsoletes js

* Sat Oct 26 2019 Ankit Jain <ankitja@vmware.com> - 68.11.0-1
- initial version
