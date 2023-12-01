Summary:        Package manager
Name:           rpm
Version:        4.18.0
Release:        4%{?dist}
License:        GPLv2+ AND LGPLv2+ AND BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://rpm.org
Source0:        http://ftp.rpm.org/releases/%{name}-%(echo %{version} | cut -d'.' -f1-2).x/%{name}-%{version}.tar.bz2
# The license for the files below is the same as for RPM as they have originally came from rpm.
# The git repo is hosted by centos. The version below is centos 8 stable.
Source3:        https://git.centos.org/rpms/python-rpm-generators/raw/c8s/f/SOURCES/python.attr
Source4:        https://git.centos.org/rpms/python-rpm-generators/raw/c8s/f/SOURCES/pythondeps.sh
Source5:        https://git.centos.org/rpms/python-rpm-generators/raw/c8s/f/SOURCES/pythondistdeps.py
Patch0:         remove-docs-from-makefile.patch
Patch1:         define-RPM_LD_FLAGS.patch
Patch2:         fix_RPM_GNUC_DEPRECATED_headers.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  awk
BuildRequires:  debugedit
BuildRequires:  elfutils-devel
BuildRequires:  file-devel
BuildRequires:  gettext
BuildRequires:  libarchive-devel
BuildRequires:  libcap-devel
BuildRequires:  libselinux-devel
BuildRequires:  libtool
BuildRequires:  lua-devel
BuildRequires:  openssl-devel
BuildRequires:  popt-devel
BuildRequires:  python3-devel
BuildRequires:  sqlite-devel
BuildRequires:  xz-devel
BuildRequires:  zstd-devel
Requires:       bash
Requires:       libarchive
Requires:       libselinux
Requires:       lua-libs
Requires:       rpm-libs = %{version}-%{release}

%description
RPM package manager

%package devel
Summary:        Libraries and header files for rpm
Requires:       %{name} = %{version}-%{release}

%description devel
Static libraries and header files for the support library for rpm

%package libs
Summary:        Libraries for rpm
Requires:       bzip2-libs
Requires:       elfutils-libelf
Requires:       libcap
Requires:       libgcc
Requires:       popt
Requires:       xz-libs
Requires:       zlib
Requires:       zstd-libs

%description    libs
Shared libraries librpm and librpmio

%package build-libs
Summary:        Librpmbuild.so.* libraries needed to build rpms.
Requires:       %{name}-libs = %{version}-%{release}

%description build-libs
%{summary}

%package build
Summary:        Binaries, scripts and libraries needed to build rpms.
Requires:       %{name}-build-libs = %{version}-%{release}
Requires:       %{name}-devel = %{version}-%{release}
Requires:       bzip2
Requires:       cpio
Requires:       debugedit
Requires:       diffutils
Requires:       elfutils-devel
Requires:       elfutils-libelf
Requires:       file
Requires:       gzip
Requires:       lua
Requires:       mariner-rpm-macros >= 2.0-22
Requires:       patch
Requires:       sed
Requires:       tar
Requires:       unzip
Requires:       util-linux
Requires:       xz
Provides:       %{name}-sign = %{version}-%{release}

%description build
%{summary}

%package lang
Summary:        Additional language files for rpm
Group:          Applications/System
Requires:       %{name} = %{version}-%{release}

%description lang
These are the additional language files of rpm.

%package -n     python3-rpm
Summary:        Python 3 bindings for rpm.
Group:          Development/Libraries
Requires:       %{name}-build-libs = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}
Requires:       python3
Provides:       %{name}-python3 = %{version}-%{release}

%description -n python3-rpm
Python3 rpm.

%prep
%autosetup -n %{name}-%{version} -p1

%build
# pass -L opts to gcc as well to prioritize it over standard libs
sed -i 's/-Wl,-L//g' python/setup.py.in
sed -i '/library_dirs/d' python/setup.py.in
sed -i 's/extra_link_args/library_dirs/g' python/setup.py.in

./autogen.sh --noconfigure

%configure \
    CPPFLAGS='-DLUA_COMPAT_APIINTCASTS' \
    --program-prefix= \
    --with-crypto=openssl \
    --enable-ndb \
    --disable-dependency-tracking \
    --disable-static \
    --with-vendor=mariner \
    --enable-python \
    --with-cap \
    --disable-silent-rules \
    --with-selinux \
    --with-audit=no

# Remove manpages translations
rm -r docs/man/{fr,ja,ko,pl,ru,sk}

%make_build

pushd python
%py3_build
popd

# Set provided python versions
sed -i 's/@MAJORVER-PROVIDES-VERSIONS@/%{python3_version}/' %{SOURCE3}

# Fix the interpreter path for python replacing the first line
sed -i '1 s:.*:#!%{_bindir}/python3:' %{SOURCE5}

%check
make check TESTSUITEFLAGS=-j%{_smp_build_ncpus}
check_result=$?
if [[ $check_result -ne 0 ]]; then
	cat tests/rpmtests.log || true
fi
make clean
[[ $check_result -eq 0 ]]

%install
%make_install

find %{buildroot} -type f -name "*.la" -delete -print
find %{buildroot} -name 'perl*' -delete

%find_lang %{name}
# System macros and prefix
install -dm 755 %{buildroot}%{_sysconfdir}/rpm
install -vm644 %{SOURCE3} %{buildroot}%{_fileattrsdir}/
install -vm755 %{SOURCE4} %{buildroot}%{_libdir}/rpm/
install -vm755 %{SOURCE5} %{buildroot}%{_libdir}/rpm/


pushd python
python3 setup.py install --skip-build --prefix=%{_prefix} --root=%{buildroot}
popd

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig
%post   build-libs -p /sbin/ldconfig
%postun build-libs -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/rpm
%{_bindir}/gendiff
%{_bindir}/rpm2archive
%{_bindir}/rpm2cpio
%{_bindir}/rpmdb
%{_bindir}/rpmgraph
%{_bindir}/rpmkeys
%{_bindir}/rpmquery
%{_bindir}/rpmverify

%{_libdir}/rpm/rpmpopt-*
%{_libdir}/rpm/rpmdb_*
%{_libdir}/rpm/rpm.daily
%{_libdir}/rpm/rpm.log
%{_libdir}/rpm/rpm.supp
%{_libdir}/rpm/rpmuncompress
%{_libdir}/rpm/rpm2cpio.sh
%{_libdir}/rpm/tgpg
%{_libdir}/rpm/platform
%{_libdir}/rpm-plugins/*
# Because of no doxygen dependency, we do not produce manpages that require it.
# %{_mandir}/man8/rpm.8.gz
# %{_mandir}/man8/rpm2cpio.8.gz
# %{_mandir}/man8/rpmdb.8.gz
# %{_mandir}/man8/rpmgraph.8.gz
# %{_mandir}/man8/rpmkeys.8.gz
# %{_mandir}/man8/rpm-misc.8.gz
# %{_mandir}/man8/rpm-plugin-systemd-inhibit.8.gz

%files libs
%defattr(-,root,root)
%{_libdir}/librpmio.so.*
%{_libdir}/librpm.so.*
%{_libdir}/rpm/macros
%{_libdir}/rpm/rpmrc
%{_libdir}/rpm/platform/*

%files build-libs
%{_libdir}/librpmbuild.so*

%files build
%{_bindir}/rpmbuild
%{_bindir}/rpmlua
%{_bindir}/rpmsign
%{_bindir}/rpmspec
%{_libdir}/rpm/macros.*
%{_libdir}/rpm/find-lang.sh
%{_libdir}/rpm/rpm_macros_provides.sh
%{_libdir}/rpm/find-provides
%{_libdir}/rpm/find-requires
%{_libdir}/rpm/brp-*
%{_libdir}/rpm/fileattrs/*
%{_libdir}/rpm/script.req
%{_libdir}/rpm/check-buildroot
%{_libdir}/rpm/check-files
%{_libdir}/rpm/check-prereqs
%{_libdir}/rpm/check-rpaths
%{_libdir}/rpm/check-rpaths-worker
%{_libdir}/rpm/elfdeps
%{_libdir}/rpm/mkinstalldirs
%{_libdir}/rpm/pkgconfigdeps.sh
%{_libdir}/rpm/*.prov
%{_libdir}/rpm/pythondistdeps.py

%{_libdir}/rpm/pythondeps.sh
%{_libdir}/rpm/ocamldeps.sh
%{_libdir}/rpm/rpmdeps
# Because of no doxygen dependency, we do not produce manpages that require it.
# %{_mandir}/man1/gendiff.1*
# %{_mandir}/man8/rpmbuild.8*
# %{_mandir}/man8/rpmdeps.8*
# %{_mandir}/man8/rpmspec.8*
# %{_mandir}/man8/rpmsign.8.gz

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/rpm.pc
%{_libdir}/librpmio.so
%{_libdir}/librpm.so
%{_libdir}/librpmsign.so
%{_libdir}/librpmsign.so.*

%files lang -f %{name}.lang
%defattr(-,root,root)

%files -n python3-rpm
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 4.18.0-4
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Jun 15 2023 Andrew Phelps <anphel@microsoft.com> - 4.18.0-3
- Remove brp-strip-debug-symbols and brp-strip-unneeded scripts

* Fri Sep 30 2022 Andy Caldwell <andycaldwell@microsoft> - 4.18.0-2
- Create versioned dependencies from `python3-rpm` -> `rpm-build-libs` -> `rpm-libs` to ensure ABI compatibility

* Wed Sep 21 2022 Daniel McIlvaney <damcilva@microsoft.com> - 4.18.0-1
- Update to 4.18.0 to resolve CVE-2021-35938, CVE-2021-35939, and CVE-2021-3521

* Mon Jul 18 2022 Nan Liu <liunan@microsoft.com> - 4.17.0-9
- Add missing dependencies to rpmbuild (sed and util-linux)

* Tue May 24 2022 Jon Slobodzian <joslobo@microsoft.com> - 4.17.0-8
- Move lua runtime dependency from main rpm package.  Move to rpm-build.
- Move python files to rpm-build package.  This removes the implied dependency on python3 by the rpm package.

* Fri May 13 2022 Andy Caldwell <andycaldwell@microsoft.com> - 4.17.0-7
- Add missing dependencies to rpmbuild (file, diff and patch)

* Thu Apr 28 2022 Andrew Phelps <anphel@microsoft.com> - 4.17.0-6
- Remove main package requires for rpm-build
- Move debugedit requires to rpm-build subpackage

* Thu Apr 21 2022 Daniel McIlvaney <damcilva@microsoft.com> - 4.17.0-5
- rpm-libs needs to run in container environments without systemd, audit was being
-   pulled in as an automatic dependency. Explicitly disable the audit config.

* Wed Apr 13 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 4.17.0-4
- Update required dependecies for rpm-libs and rpm-build sub-packages.

* Tue Feb 08 2022 Olivia Crain <oliviacrain@microsoft.com> - 4.17.0-3
- Remove manual pkgconfig(*) provides in toolchain specs

* Sat Jan 29 2022 Muhammad Falak <mwani@microsoft.com> - 4.17.0-2
- Fix ptest build by replacing `%make_build_check` with `make`

* Wed Sep 15 2021 Mateusz Malisz <mamalisz@microsoft.com> - 4.17.0-1
- Upgrade to version 4.17.0.  Remove libdb dependency.

* Mon Jun 07 2021 Olivia Crain <oliviacrain@microsoft.com> - 4.14.2.1-4
- Add patch to define "$RPM_LD_FLAGS" during spec %%build phases
- Remove %%python3_sitelib redefinition
- Remove %%clean section
- Remove duplicate build-time requirements

* Wed May 19 2021 Nick Samson <nisamson@microsoft.com> - 4.14.2.1-3
- Removed python-rpm python2 module support

* Fri Apr 30 2021 Olivia Crain <oliviacrain@microsoft.com> - 4.14.2.1-2
- Merge the following releases from 1.0 to dev branch
- niontive@microsoft.com, 4.14.2-11: Patch CVE-2021-20271 and CVE-2021-3421

* Thu Feb 25 2021 Joe Schmitt <joschmit@microsoft.com> - 4.14.2.1-1
- Upgrade to v4.14.2.1 to fix broken Lua library path.

* Thu Jan 14 2021 Ruying Chen <v-ruyche@microsoft.com> - 4.14.2-13
- Apply patch to correctly parse versions for python dist dependencies.

* Tue Jan 12 2021 Ruying Chen <v-ruyche@microsoft.com> - 4.14.2-12
- Provide rpm-sign.

* Fri Dec 11 2020 Joe Schmitt <joschmit@microsoft.com> - 4.14.2-11
- Provide rpm-python3 and rpm-python.

* Thu Jun 11 2020 Henry Beberman <henry.beberman@microsoft.com> - 4.14.2-10
- Add a vendor definition so rpm will search /usr/lib/rpm/<vendor> for macros.

* Tue Jun 09 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.14.2-9
- Removed 'rpm-build' dependency on 'perl'.
- Defined an 'rpm-build-libs' subpackage to prevent 'python3-rpm'
- from pulling in 'perl'.
- Made 'python3-rpm' dependency on 'rpm-build-libs' explicit.

* Thu May 28 2020 Ruying Chen <v-ruyche@microsoft.com> - 4.14.2-8
- Move macros to mariner-rpm-macros

* Wed May 20 2020 Henry Beberman <henry.beberman@microsoft.com> - 4.14.2-7
- Add BuildRequires and Requires for zstd support.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 4.14.2-6
- Added %%license line automatically

* Wed May 06 2020 Emre Girgin <mrgirgin@microsoft.com> - 4.14.2-5
- Enable built-in lua support.
- Update URL.
- License verified.

* Wed Apr 29 2020 Mateusz Malisz <mamalisz@microsoft.com> - 4.14.2-4
- Add packaging tools as runtime requirements for rpm-build

* Fri Apr 03 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 4.14.2-3
- Remove rpm-build from requires.

* Wed Sep 11 2019 Mateusz Malisz <mamalisz@microsoft.com> - 4.14.2-2
- Fix Dependency and include build in base package.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 4.14.2-1
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Oct 03 2018 Alexey Makhalov <amakhalov@vmware.com> - 4.14.2-4
- Clean up the file in accordance to spec file checker

* Mon Oct 01 2018 Alexey Makhalov <amakhalov@vmware.com> - 4.14.2-3
- Fix python libs dependencies to use current libs version (regression)

* Fri Sep 28 2018 Alexey Makhalov <amakhalov@vmware.com> - 4.14.2-2
- macros: set _build_id_links to alldebug

* Fri Sep 14 2018 Keerthana K <keerthanak@vmware.com> - 4.14.2-1
- Update to version 4.14.2

* Thu Dec 21 2017 Xiaolin Li <xiaolinl@vmware.com> - 4.13.0.1-7
- Fix CVE-2017-7501

* Wed Oct 04 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.13.0.1-6
- make python{,3}-rpm depend on current version of librpm

* Wed Jun 28 2017 Xiaolin Li <xiaolinl@vmware.com> - 4.13.0.1-5
- Add file-devel to BuildRequires

* Mon Jun 26 2017 Chang Lee <changlee@vmware.com> - 4.13.0.1-4
- Updated %check

* Mon Jun 05 2017 Bo Gan <ganb@vmware.com> - 4.13.0.1-3
- Fix Dependency

* Thu May 18 2017 Xiaolin Li <xiaolinl@vmware.com> - 4.13.0.1-2
- Remove python2 from requires of rpm-devel subpackages.

* Wed May 10 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 4.13.0.1-1
- Update to 4.13.0.1

* Fri Apr 21 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 4.13.0-1
- Update to 4.13.0

* Wed Apr 19 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.11.2-22
- Do not allow -debuginfo to own directories to avoid conflicts with
    filesystem package and between each other. Patch applied

* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.11.2-21
- rpm-libs requires nss-libs, xz-libs and bzip2-libs.

* Tue Mar 21 2017 Xiaolin Li <xiaolinl@vmware.com> - 4.11.2-20
- Added python3 packages and moved python2 site packages from devel to python-rpm.

* Tue Jan 10 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 4.11.2-19
- added buildrequires for xz-devel for PayloadIsLzma cap

* Thu Dec 15 2016 Xiaolin Li <xiaolinl@vmware.com> - 4.11.2-18
- Moved some files from rpm to rpm-build.

* Tue Dec 06 2016 Xiaolin Li <xiaolinl@vmware.com> - 4.11.2-17
- Added -lang subpackage.

* Wed Nov 23 2016 Alexey Makhalov <amakhalov@vmware.com> - 4.11.2-16
- Move rpmrc and macros into -libs subpackage
- Move zlib and elfutils-libelf dependency from rpm to rpm-libs
- Add bzip2 dependency to rpm-libs

* Thu Nov 17 2016 Alexey Makhalov <amakhalov@vmware.com> - 4.11.2-15
- Added -libs subpackage

* Tue Nov 15 2016 Alexey Makhalov <amakhalov@vmware.com> - 4.11.2-14
- Disable lua support

* Tue Oct 18 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 4.11.2-13
- Apply patch for CVE-2014-8118

* Wed Oct 05 2016 ChangLee <changlee@vmware.com> - 4.11.2-12
- Modified %check

* Fri Aug 26 2016 Alexey Makhalov <amakhalov@vmware.com> - 4.11.2-11
- find-debuginfo...patch: exclude non existing .build-id from packaging
- Move all files from rpm-system-configuring-scripts tarball to here

* Wed May 25 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 4.11.2-10
- Exclude .build-id/.1 and .build-id/.1.debug from debuginfo pkg

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 4.11.2-9
- GA - Bump release of all rpms

* Thu May 05 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 4.11.2-8
- Update rpm version in lock-step with lua update to 5.3.2

* Fri Apr 08 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> - 4.11.2-7
- Build rpm with capabilities.

* Wed Aug 05 2015 Sharath George <sharathg@vmware.com> - 4.11.2-6
- Moving build utils to a different package.

* Sat Jun 27 2015 Alexey Makhalov <amakhalov@vmware.com> - 4.11.2-5
- Update rpm-system-configuring-scripts. Use tar --no-same-owner for rpmbuild.

* Thu Jun 18 2015 Anish Swaminathan <anishs@vmware.com> - 4.11.2-4
- Add pkgconfig Provides directive

* Thu Jun 18 2015 Alexey Makhalov <amakhalov@vmware.com> - 4.11.2-3
- Do no strip debug info from .debug files

* Wed Jun 3 2015 Divya Thaluru <dthaluru@vmware.com> - 4.11.2-2
- Removing perl-module-scandeps package from run time required packages

* Tue Jan 13 2015 Divya Thaluru <dthaluru@vmware.com> - 4.11.2-1
- Initial build. First version
