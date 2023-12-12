%undefine __cmake_in_source_build
%define _tdnfpluginsdir %{_libdir}/tdnf-plugins
%define _tdnf_history_db_dir %{_libdir}/sysimage/tdnf

Summary:        dnf/yum equivalent using C libs
Name:           tdnf
Version:        3.5.2
Release:        3%{?dist}
License:        LGPLv2.1 AND GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/RPM
URL:            https://github.com/vmware/tdnf/wiki
#Source0:       https://github.com/vmware/tdnf/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Source1:        cache-updateinfo
Source2:        cache-updateinfo.service
Source3:        cache-updateinfo.timer
Source4:        tdnfrepogpgcheck.conf
Patch0:         tdnf-mandatory-space-list-output.patch
Patch1:         tdnf-default-mariner-release.patch
Patch2:         tdnf-enable-plugins-by-default.patch
# Patch to be removed once we upgrade to a version of tdnf which contains the upstream fix
# https://github.com/vmware/tdnf/commit/d62d7097c009ee867bee992840334dbc12f4f0f3
Patch3:         tdnf-printf-fix.patch
# Patch to be removed once we upgrade to a version of tdnf which contains the upstream fix
# https://github.com/vmware/tdnf/commit/5311b5ed0867a40ceb71b89358d70290bc2d0c51
Patch4:         tdnf-sqlite-library.patch
# Patch to be removed once we upgrade to a version of tdnf which contains the upstream fix
# https://github.com/vmware/tdnf/pull/432
Patch5:         tdnf-GetRepoMD-fix.patch
Patch6:		tdnf-dotarch.patch
#Cmake requires binutils
BuildRequires:  binutils
BuildRequires:  cmake
BuildRequires:  curl-devel
#Cmake requires gcc,glibc-devel
BuildRequires:  gcc
BuildRequires:  glibc-devel
#plugin repogpgcheck
BuildRequires:  gpgme-devel
BuildRequires:  libsolv-devel
BuildRequires:  libxml2-devel
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  popt-devel
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  rpm-devel
BuildRequires:  sqlite-devel
BuildRequires:  zlib-devel
Requires:       curl-libs
Requires:       libsolv
Requires:       openssl-libs
Requires:       rpm-libs
Requires:       tdnf-cli-libs = %{version}-%{release}
Requires:       zlib
Obsoletes:      yum
Provides:       yum
%if %{with_check}
BuildRequires:  createrepo_c
BuildRequires:  glib
BuildRequires:  libxml2
BuildRequires:  python3-pip
BuildRequires:  python3-requests
BuildRequires:  python3-xml
%endif

%description
tdnf is a yum/dnf equivalent which uses libsolv and libcurl

%package    devel
Summary:        A Library providing C API for tdnf
Group:          Development/Libraries
Requires:       libsolv-devel
Requires:       %{name} = %{version}-%{release}

%description devel
Development files for tdnf

%package        cli-libs
Summary:        Library providing cli libs for tdnf like clients
Group:          Development/Libraries

%description cli-libs
Library providing cli libs for tdnf like clients.

%package plugin-metalink
Summary:        tdnf plugin providing metalink functionality for repo configurations
Group:          Applications/RPM
Requires:       %{name} = %{version}-%{release}
Requires:       libxml2

%description plugin-metalink
tdnf plugin providing metalink functionality for repo configurations

%package        plugin-repogpgcheck
Summary:        tdnf plugin providing gpg verification for repository metadata
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       gpgme

%description plugin-repogpgcheck
tdnf plugin providing gpg verification for repository metadata

%package        python
Summary:        python bindings for tdnf
Group:          Development/Libraries
Requires:       python3

%description python
python bindings for tdnf

%package        autoupdate
Summary:        systemd services for periodic automatic update
Group:          Applications/RPM
Requires:       %{name} = %{version}-%{release}

%description autoupdate
systemd services for periodic automatic update

%prep
%autosetup -p1

%build
%cmake \
    -DCMAKE_BUILD_TYPE=Debug \
    -DBUILD_SHARED_LIBS=OFF \
    -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir} \
    -DHISTORY_DB_DIR=%{_tdnf_history_db_dir}

%cmake_build

cd %{__cmake_builddir}
%make_build python

%check
pip3 install pytest requests pyOpenSSL
cd build && make %{?_smp_mflags} check

%install
%cmake_install
find %{buildroot} -name '*.a' -delete -print
mkdir -p %{buildroot}%{_var}/cache/tdnf
mkdir -p %{buildroot}%{_tdnf_history_db_dir}
ln -sf %{_bindir}/tdnf %{buildroot}%{_bindir}/tyum
ln -sf %{_bindir}/tdnf %{buildroot}%{_bindir}/tdnfj
install -v -D -m 0755 %{SOURCE1} %{buildroot}%{_bindir}/tdnf-cache-updateinfo
install -v -D -m 0644 %{SOURCE2} %{buildroot}%{_libdir}/systemd/system/tdnf-cache-updateinfo.service
install -v -D -m 0644 %{SOURCE3} %{buildroot}%{_libdir}/systemd/system/tdnf-cache-updateinfo.timer
install -v -D -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/tdnf/pluginconf.d/tdnfrepogpgcheck.conf
rm -f %{buildroot}%{_bindir}/jsondumptest
rm -rf %{buildroot}%{_datadir}/tdnf

mkdir -p %{buildroot}%{_sysconfdir}/%{name}/protected.d

pushd %{__cmake_builddir}/python
%py3_install
popd
find %{buildroot} -name '*.pyc' -delete

%post
/sbin/ldconfig
# Required step to ensure new history util from version 3.4.1 does not fail
if [[ ! -f %{_tdnf_history_db_dir}/history.db ]]; then
    %{_libdir}/tdnf/tdnf-history-util init
fi

%preun
if [ "$1" = 0 ] && [[ $(readlink $(rpm --eval %{_bindir})/yum) == tdnf ]]; then
    rm $(rpm --eval %{_bindir})/yum
fi

%postun
/sbin/ldconfig

%posttrans
# Make the decision to update yum sym link during post script
# not package build. Some workloads want to disable tdnf, so
# decision should not be made during build but during install
# of package.
if [ ! -e $(rpm --eval %{_bindir})/yum ]; then
    ln -sf tdnf $(rpm --eval %{_bindir})/yum
fi

%files
%license COPYING
%defattr(-,root,root,0755)
%config(noreplace) %{_sysconfdir}/tdnf/tdnf.conf
%dir %{_tdnf_history_db_dir}
%dir %{_var}/cache/tdnf
%{_bindir}/tdnf
%{_bindir}/tdnf-cache-updateinfo
%{_bindir}/tdnf-config
%{_bindir}/tdnfj
%{_bindir}/tyum
%{_datadir}/bash-completion/completions/tdnf
%{_libdir}/libtdnf.so.3
%{_libdir}/libtdnf.so.3.*
%{_libdir}/tdnf/tdnf-history-util

%files devel
%defattr(-,root,root)
%exclude %{_libdir}/debug
%{_includedir}/tdnf/*.h
%{_libdir}/libtdnf.so
%{_libdir}/libtdnfcli.so
%{_libdir}/pkgconfig/tdnf-cli-libs.pc
%{_libdir}/pkgconfig/tdnf.pc

%files cli-libs
%defattr(-,root,root)
%{_libdir}/libtdnfcli.so.3
%{_libdir}/libtdnfcli.so.3.*

%files plugin-metalink
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/tdnf/pluginconf.d/tdnfmetalink.conf
%dir %{_sysconfdir}/tdnf/pluginconf.d
%{_tdnfpluginsdir}/libtdnfmetalink.so

%files plugin-repogpgcheck
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/tdnf/pluginconf.d/tdnfrepogpgcheck.conf
%dir %{_sysconfdir}/tdnf/pluginconf.d
%{_tdnfpluginsdir}/libtdnfrepogpgcheck.so

%files python
%defattr(-,root,root)
%{python3_sitelib}/*

%files autoupdate
%{_bindir}/tdnf-automatic
%{_libdir}/systemd/system/tdnf-cache-updateinfo*
%{_sysconfdir}/motdgen.d/02-tdnf-updateinfo.sh
%{_sysconfdir}/tdnf/automatic.conf
/%{_lib}/systemd/system/tdnf*

%changelog
* Fri Oct 06 2023 Andy Zaugg <azaugg@linkedin.com> - 3.5.2-3
- tdnf should only become default if a backend package manager has not previously been defined

* Thu Jun 15 2023 Sam Meluch <sammeluch@microsoft.com> - 3.5.2-2
- add patch for SELECTION_DOTARCH in solv/tdnfquery.c

* Wed Apr 12 2023 Sam Meluch <sammeluch@microsoft.com> - 3.5.2-1
- Update tdnf to version 3.5.2
- Remove tdnf download patch in favor of upstream --downloadonly functionality

* Tue May 03 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.2.2-4
- Reverting usage of "rpm" in RPM scripts since "/var/lib/rpm/.rpm.lock" is always taken.

* Wed Apr 13 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 3.2.2-3
- Update required dependecies for tdnf package which needs rpm-libs.

* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.2.2-2
- Installing Mariner GPG keys when present/installed.

* Wed Jan 12 2022 Mateusz Malisz <mamalisz@microsoft.com> - 3.2.2-1
- Update to 3.2.2 version
- Remove upstreamed patches
- Clean up the spec.
- Add libmetalink as a dependency

* Fri Dec 03 2021 Thomas Crain <thcrain@microsoft.com> - 2.1.0-8
- Replace easy_install usage with pip in %%check sections

* Mon Apr 26 2021 Thomas Crain <thcrain@microsoft.com> - 2.1.0-7
- Replace incorrect %%{_lib} usage with %%{_libdir}

* Mon Dec 28 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.1.0-6
- Patching TDNF to print at least one space between columns in 'tdnf list' output.
- Fixing whitelist warnings in previous patches.

* Mon Nov 16 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.1.0-5
- Extending 'BuildRequires' with "pytest's" dependencies to fix the package tests.

* Fri Aug 14 2020 Joe Schmitt <joschmit@microsoft.com> - 2.1.0-4
- Add tdnf-use-custom-keyring-for-gpg-checks.patch

* Thu Jul 30 2020 Joe Schmitt <joschmit@microsoft.com> - 2.1.0-3
- Add tdnf-add-download-no-deps-command.patch.

* Wed Jul 29 2020 Emre Girgin <mrgirgin@microsoft.com> - 2.1.0-2
- Fix 'repolist' command failure when gpgkey field is empty.

* Tue May 19 2020 Emre Girgin <mrgirgin@microsoft.com> - 2.1.0-1
- Update URL, and License.
- License verified.
- Upgrade to 2.1.0.
- Add support for multiple gpgkeys in the .repo file.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com>
- Added %%license line automatically

* Tue Apr 07 2020 Nicolas Ontiveros <niontive@microsoft.com> - 2.0.0-16
- Don't install updateinfo.sh to the motdgen directory.
- Remove motd triggers.
- Fixed Source0.

* Mon Nov 25 2019 Andrew Phelps <anphel@microsoft.com> - 2.0.0-15
- Fix $basearch and $releasever handling.

* Thu Nov 21 2019 Joe Schmitt <joschmit@microsoft.com> - 2.0.0-14
- Fix "showorder" output to match the rest of tdnf formatting.

* Wed Nov 20 2019 Joe Schmitt <joschmit@microsoft.com> - 2.0.0-13
- Add "download" command and "showorder" option.

* Wed Oct 30 2019 Emre Girgin <mrgirgin@microsoft.com> - 2.0.0-12
- Add support for SSL verification options in .repo files.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.0.0-11
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Mar 15 2019 Ankit Jain <ankitja@vmware.com> - 2.0.0-10
- Added skipconflicts and skipobsoletes to check command.

* Thu Mar 14 2019 Keerthana K <keerthanak@vmware.com> - 2.0.0-9
- GPGCheck fix on RPM version 4.14.2

* Mon Mar 04 2019 Keerthana K <keerthanak@vmware.com> - 2.0.0-8
- makecache and refresh command updates.

* Thu Feb 14 2019 Keerthana K <keerthanak@vmware.com> - 2.0.0-7
- Fix to address issues when no repos are enabled.

* Wed Jan 23 2019 Keerthana K <keerthanak@vmware.com> - 2.0.0-6
- Fix Memory leak and curl status type.

* Wed Jan 02 2019 Keerthana K <keerthanak@vmware.com> - 2.0.0-5
- Added make check.

* Tue Dec 04 2018 Keerthana K <keerthanak@vmware.com> - 2.0.0-4
- Add support for libsolv caching.
- Fix bug in tdnf updateinfo command.
- Fix bug on list available command.

* Wed Nov 21 2018 Keerthana K <keerthanak@vmware.com> - 2.0.0-3
- Update to 2.0.0 beta release.

* Mon Oct 08 2018 Keerthana K <keerthanak@vmware.com> - 2.0.0-2
- Fix bug on tdnf crash when photon-iso repo only enabled without mounting cdrom.

* Fri Feb 09 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.0.0-1
- update to 2.0.0

* Tue Jan 30 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.2.2-3
- patch to error out early for permission issues.

* Tue Oct 10 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.2.2-2
- Fix bug in obsolete protected packages.

* Wed Oct 4 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.2.2-1
- update to v1.2.2

* Sat Sep 30 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.2.1-5
- Output problems while resolving to stderr (instead of stdout)

* Wed Sep 27 2017 Bo Gan <ganb@vmware.com> - 1.2.1-4
- Improve suggestion in motd message

* Thu Sep 14 2017 Bo Gan <ganb@vmware.com> - 1.2.1-3
- Add suggestion in motd message

* Fri Jul 21 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.2.1-2
- Modify quiet patch.

* Tue Jul 18 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.2.1-1
- Update to v1.2.1

* Tue May 30 2017 Bo Gan <ganb@vmware.com> - 1.2.0-5
- Fix cache-updateinfo script again

* Fri May 12 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.2.0-4
- Patch repo refresh to allow quiet flags

* Wed May 10 2017 Bo Gan <ganb@vmware.com> - 1.2.0-3
- Fix cache-updateinfo script

* Fri May 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.2.0-2
- Fix Requires for cli-libs

* Wed May 03 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.2.0-1
- update to v1.2.0

* Sun Apr 30 2017 Bo Gan <ganb@vmware.com> - 1.1.0-5
- Do not write to stdout in motd triggers

* Thu Apr 20 2017 Bo Gan <ganb@vmware.com> - 1.1.0-4
- motd hooks/triggers for updateinfo notification

* Fri Apr 14 2017 Dheerajs Shetty <dheerajs@vmware.com> - 1.1.0-3
- Adding a patch to compile with latest hawkey version

* Mon Dec 19 2016 Xiaolin Li <xiaolinl@vmware.com> - 1.1.0-2
- BuildRequires libsolv-devel.

* Thu Dec 08 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.1.0-1
- update to v1.1.0

* Thu Nov 17 2016 Alexey Makhalov <amakhalov@vmware.com> - 1.0.9-3
- Use rpm-libs at runtime

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.0.9-2
- GA - Bump release of all rpms

* Fri May 20 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.0.9-1
- Update to 1.0.9. Contains fixes for updateinfo.

* Wed May 4 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.0.8-3
- Fix link installs, fix devel header dir

* Fri Apr 1 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.0.8-2
- Update version which was missed with 1.0.8-1, apply string limits

* Fri Apr 1 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.0.8-1
- Code scan fixes, autotest path fix, support --releasever

* Thu Jan 14 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.0.7
- Fix return codes on install and check-update
- Add tests for install existing and update

* Wed Jan 13 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.0.6
- Support distroverpkg and add tests to work with make check

* Mon Dec 14 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.0.5
- Support for multiple packages in alter commands
- Support url vars for releasever and basearch

* Fri Oct 2 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.0.4
- Fix upgrade to work without args, Engage distro-sync
- Fix install to resolve to latest available
- Fix formats, fix refresh on download output

* Tue Sep 8 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.0.3
- Fix metadata creation issues. Engage refresh flag.
- Do not check gpgkey when gpgcheck is turned off in repo.

* Thu Jul 23 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.0.2
- Support reinstalls in transaction. Handle non-existent packages correctly.

* Mon Jul 13 2015 Alexey Makhalov <amakhalov@vmware.com> - 1.0.1-2
- Create -debuginfo package. Use parallel make.

* Tue Jun 30 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.0.1
- Proxy support, keepcache fix, valgrind leaks fix

* Fri Jan 23 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.0
- Initial build.  First version
