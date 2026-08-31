# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global libcurl_version 7.52.0

%undefine __cmake_in_source_build

%if 0%{?rhel}
%bcond_with zchunk
%else
%bcond_without zchunk
%endif

%if 0%{?fedora} >= 39 || 0%{?rhel} >= 10
%bcond_with use_gpgme
%bcond_with use_selinux
%else
%bcond_without use_gpgme
%bcond_without use_selinux
%endif

# Needs to match how gnupg2 is compiled
%bcond_with run_gnupg_user_socket

%bcond_with sanitizers

%if %{with use_gpgme} && %{with use_selinux}
%global need_selinux 1
%else
%global need_selinux 0
%endif

%global dnf_conflict 2.8.8

Name:           librepo
Version:        1.20.0
Release:        4%{?dist}
Summary:        Repodata downloading library

License:        LGPL-2.1-or-later
URL:            https://github.com/rpm-software-management/librepo
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  check-devel
BuildRequires:  doxygen
BuildRequires:  pkgconfig(glib-2.0) >= 2.66
%if %{with use_gpgme}
BuildRequires:  gpgme-devel
%else
BuildRequires:  pkgconfig(rpm) >= 4.18.0
%endif
BuildRequires:  libattr-devel
BuildRequires:  libcurl-devel >= %{libcurl_version}
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libcrypto)
%if %{need_selinux}
BuildRequires:  pkgconfig(libselinux)
%endif
BuildRequires:  pkgconfig(openssl)
%if %{with zchunk}
BuildRequires:  pkgconfig(zck) >= 0.9.11
%endif
Requires:       libcurl%{?_isa} >= %{libcurl_version}

%if %{with sanitizers}
BuildRequires:  libasan
BuildRequires:  liblsan
BuildRequires:  libubsan
%endif

%description
A library providing C and Python (libcURL like) API to downloading repository
metadata.

%package devel
Summary:        Repodata downloading library
Requires:       %{name}%{?_isa} = %{version}-%{release}
%if %{with zchunk}
Requires:       zchunk-devel%{?_isa}
%endif

%description devel
Development files for librepo.

%package -n python3-%{name}
Summary:        Python 3 bindings for the librepo library
%{?python_provide:%python_provide python3-%{name}}
BuildRequires:  python3-devel
BuildRequires:  python3-gpg
BuildRequires:  python3-pyxattr
BuildRequires:  python3-requests
BuildRequires:  python3-sphinx
Requires:       %{name}%{?_isa} = %{version}-%{release}
# Obsoletes Fedora 27 package
Obsoletes:      platform-python-%{name} < %{version}-%{release}
Conflicts:      python3-dnf < %{dnf_conflict}

%description -n python3-%{name}
Python 3 bindings for the librepo library.

%prep
%autosetup -p1

%build
%cmake \
    -DWITH_ZCHUNK=%{?with_zchunk:ON}%{!?with_zchunk:OFF} \
    -DUSE_GPGME=%{?with_use_gpgme:ON}%{!?with_use_gpgme:OFF} \
    -DUSE_RUN_GNUPG_USER_SOCKET=%{?with_run_gnupg_user_socket:ON}%{!?with_run_gnupg_user_socket:OFF} \
    -DWITH_SANITIZERS=%{?with_sanitizers:ON}%{!?with_sanitizers:OFF} \
%if %{need_selinux}
    -DENABLE_SELINUX=ON
%else
    -DENABLE_SELINUX=OFF
%endif
%cmake_build

%check
%ctest

%install
%cmake_install

%if 0%{?rhel} && 0%{?rhel} <= 7
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%else
%ldconfig_scriptlets
%endif

%files
%license COPYING
%doc README.md
%{_libdir}/%{name}.so.*

%files devel
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/

%files -n python3-%{name}
%{python3_sitearch}/%{name}/

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.20.0-4
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.20.0-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jun 20 2025 Ales Matej <amatej@redhat.com> - 1.20.0-1
- Update to 1.20.0
- Fix and update lr_download_metadata API to enable parallel downloading of repos

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.19.0-4
- Rebuilt for Python 3.14

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Nov 04 2024 Evan Goode <egoode@redhat.com> - 1.19.0-1
- Fix input termination for pgpParsePkts
- Convert all xattr strings to lower case to be compatible to Amazon S3 buckets
- Introduce entropy for fastestmirror option

* Wed Aug 14 2024 Evan Goode <egoode@redhat.com> - 1.18.1-1
- gpg: Check is_selinux_enabled() before trying to label
- spec: Correct setting -DENABLE_SELINUX cmake argument
- tests: Adapt to CURL without NTLM support
- Fix a memory leak in select_next_target()
- Fix memory leaks when using zchunk

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jul 11 2024 Petr Pisar <ppisar@redhat.com> - 1.18.0-2
- Handle PGP keys with librpm on RHEL ≥ 10

* Tue Jul 02 2024 Evan Goode <egoode@redhat.com> - 1.18.0-1
- Update to 1.18.0 (note: skipped 1.17.2 downstream)
- API: Add LRO_USERNAME and LRO_PASSWORD options
- Add a private dependency on zck to librepo.pc if zchunk support is enabled
- Hash cache: Improved work with extended file attributes
- Improve performance of large number of package downloads
- Fix error handling, Fix examples and build them

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.17.1-2
- Rebuilt for Python 3.13

* Tue Mar 26 2024 Jan Kolarik <jkolarik@redhat.com> - 1.17.1-1
- Update to 1.17.1
- gpg_gpgme.c: fix build errors with older gcc
- Change header files to match a configured ABI regarding a zchunk support
- Fix building zchunk code if zchunk is enabled
- Fix compiler warnings

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 18 2023 Jan Kolarik <jkolarik@redhat.com> - 1.17.0-1
- Update to 1.17.0
- lr_gpg_check_signature: Forward PGP error messages from RPM
- PGP: fix: Support importing binary public keys in librpm backend
- PGP: Enable creating a UID directory for GnuGP agent socket in /run/gnupg/user
- PGP: Set a default creation SELinux labels on GnuPG directories

* Wed Sep 20 2023 Adam Williamson <awilliam@redhat.com> - 1.16.0-2
- Rebuild with no changes for Bodhi reasons

* Fri Sep 01 2023 Jan Kolarik <jkolarik@redhat.com> - 1.16.0-1
- Update to 1.16.0
- Implement OpenPGP using librpm API

* Tue Aug 01 2023 Jan Kolarik <jkolarik@redhat.com> - 1.15.2-1
- Update to 1.15.2
- Fixes and optimizations in header files
- Fix lr_gpg_list_keys function when keys are empty
- Update PGP test vectors
- Fix CMake warnings
- Bump glib version

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 1.15.1-3
- Rebuilt for Python 3.12

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 09 2022 Jaroslav Rohel <jrohel@redhat.com> - 1.15.1-1
- Update to 1.15.1
- Adds API support for waiting on network in an event driven manner (new API function lr_handle_network_wait)
- OpenPGP API extension and fixes (new API functions lr_gpg_*)
- Update license format to "LGPL-2.1-or-later"

* Tue Aug 23 2022 Jaroslav Rohel <jrohel@redhat.com> - 1.14.4-1
- Update to 1.14.4
- Use nanosec precision for timestamp of checksum cache (RhBug:2077864)
- Fix alloc/free mismatches and memory leaks

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 15 2022 Python Maint <python-maint@redhat.com> - 1.14.3-2
- Rebuilt for Python 3.11

* Thu May 05 2022 Jaroslav Rohel <jrohel@redhat.com> - 1.14.3-1
- Update to 1.14.3
- Make error messages about repodata and rpm mismatch more user friendly

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Sep 23 2021 Pavla Kratochvilova <pkratoch@redhat.com> - 1.14.2-1
- Update to 1.14.2
- Fix covscan warnings and memory leak

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.14.1-3
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 15 2021 Pavla Kratochvilova <pkratoch@redhat.com> - 1.14.1-1
- Update to 1.14.1
- Recover from fsync fail on read-only filesystem (RhBug:1956361)
- Reduce time to load metadata
- Fix resource leaks

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 1.14.0-2
- Rebuilt for Python 3.10

* Thu Apr 15 2021 Nicola Sella <nsella@redhat.com> - 1.14.0-1
- Update to 1.14.0
- Fix: memory leaks
- Support multiple checksums in xattr (RhBz:1931904)
- Use macros to access extended attributes
- Remove problematic language
- CMake: Set minimum version for curl to 7.52.0

* Mon Mar 01 2021 Nicola Sella <nsella@redhat.com> - 1.13.0-1
- Update to 1.13.0
- Add support for working with certificates used with proxy
- Drop Python 2 support
- Fix: lr_perform() - Avoid 100% CPU usage
- Add support for pkcs11 certificate and key for repository authorization
- Fix default value for LRO_SSLVERIFYSTATUS
- Don't use max_ranges to determine if we expect zchunk callback
- Prefer HTTP over FTP mirrors when zchunk is enabled
- Fixed mem leaks and typos

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Oct 07 2020 Nicola Sella <nsella@redhat.com> - 1.12.1-1
* Update to 1.12.1
- Validate path read from repomd.xml (RhBug:1868639)

* Fri Aug 07 2020 Nicola Sella <nsella@redhat.com> - 1.12.0-4
spec: Fix building with new cmake macros

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 02 2020 Nicola Sella <nsella@redhat.com> - 1.12.0-1
- Update to 1.12.0
- Decode package URL when using for local filename (RhBug:1817130)
- Fix memory leak in lr_download_metadata() and lr_yum_download_remote()
- Download sources work when at least one of specified is working (RhBug:1775184)
- Enable building on OSX

* Mon May 25 2020 Miro Hrončok <mhroncok@redhat.com> - 1.11.3-3
- Rebuilt for Python 3.9

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 1.11.3-2
- Bootstrap for Python 3.9

* Wed Apr 01 2020 Ales Matej <amatej@fedoraproject.org> - 1.11.3-1
- Update to 1.11.3
- Prefer mirrorlist/metalink over baseurl (RhBug:1775184)

* Mon Feb 10 2020 Ales Matej <amatej@fedoraproject.org> - 1.11.1-4
- Fix calling Python API without holding GIL (RhBug:1788918)

* Wed Feb 05 2020 Lukas Slebodnik <lslebodn@fedoraproject.org> - 1.11.1-3
- Do not unref LrErr_Exception on exit (RhBug:1778854)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 09 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 1.11.1-1
- Update to 1.11.1
- Create a directory for gpg sockets in /run/user/ (RhBug:1769831,1771012)

* Wed Nov 06 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 1.11.0-1
- Update to 1.11.0
- Retry mirrorlist/metalink downloads several times (RhBug:1741931)
- Improve variable substitutions in URLs and add ${variable} support

* Tue Oct 01 2019 Ales Matej <amatej@redhat.com> - 1.10.6-1
- Update to 1.10.6
- Imporove handling of xattr to re-download damadged files (RhBug:1690894)
- Rephrase repository GPG check error message (RhBug:1741442)
- Add sleep before next try when all mirrors were tried (RhBug:1741931)
- Raise logging level of error messages (RhBug:1737709)

* Sun Aug 18 2019 Miro Hrončok <mhroncok@redhat.com> - 1.10.5-2
- Rebuilt for Python 3.8

* Mon Jul 29 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 1.10.5-1
- Update to 1.10.5
- Exit gpg-agent after repokey import (RhBug:1650266)
- Handle webservers that don't support ranges when downloading zck
- Define LRO_SUPPORTS_CACHEDIR only with zchunk (RhBug:1726141)
- Allow to use mirrors multiple times for a target (RhBug:1678588)
- Allow to try baseurl multiple times (RhBug:1678588)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 23 2019 Jonathan Dieter <jdieter@gmail.com> - 1.10.2-2
- Add upstream patch to make sure to check next transfer if current zck
  transfer already exists

* Mon May 20 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 1.10.2-1
- Update to 1.10.2
- Add an option to preserve timestamps of the downloaded files (RhBug:1688537)
- librepo: append the '?' part of repo URL after the path
- Fix librepo isn't able to load zchunk files from next server on failure

* Tue Apr 02 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 1.9.6-2
- Backport patch to fix segfault when using zchunk metadata

* Wed Mar 27 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 1.9.6-1
- Update to 1.9.6
- Fix memory leaks
- Fix CPU usage when downloading packages (RhBug:1691856)

* Mon Mar 11 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 1.9.5-1
- Update to 1.9.5
- Reduce download delays

* Wed Feb 13 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 1.9.4-1
- Update to 1.9.4-1
- Add zchunk support

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Miro Hrončok <mhroncok@redhat.com> - 1.9.2-2
- Subpackage python2-librepo has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Tue Sep 25 2018 Jaroslav Mracek <jmracek@redhat.com> - 1.9.2-1
- Update to 1.9.2
- Fix major performance regression with libcurl-7.61.1

* Mon Aug 13 2018 Daniel Mach <dmach@redhat.com> - 1.9.1-1
- Update to 1.9.1

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jaroslav Mracek <jmracek@redhat.com> - 1.9.0-3
- Rebuilt for Python 3.7

* Tue Jun 26 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.9.0-2
- Fix ldconfig_scriptlets once more

* Tue Jun 26 2018 Jaroslav Mracek <jmracek@redhat.com> - 1.9.0-1
- Update to 1.9.0

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 1.8.1-9
- Rebuilt for Python 3.7

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 1.8.1-8
- Bootstrap for Python 3.7

* Thu Feb 08 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.8.1-7
- Add if conditionals around pyxattr

* Wed Feb 07 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.8.1-6
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Jan 31 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.8.1-5
- Switch to %%ldconfig_scriptlets

* Tue Nov 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.8.1-4
- Use better Obsoletes for platform-python

* Sat Nov 04 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.8.1-3
- Fix typo in Obsoletes

* Fri Nov 03 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.8.1-2
- Remove platform-python subpackage

* Fri Sep 15 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.8.1-1
- Update to 1.8.1

* Fri Sep 01 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.8.0-2
- Disable platform python on old releases

* Wed Aug 23 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.8.0-1
- Update to 1.8.0

* Fri Aug 18 2017 Tomas Orsava <torsava@redhat.com> - 1.7.20-9
- Added Patch 0 to fix a tearDown failure in the test suite

* Thu Aug 10 2017 Petr Viktorin <pviktori@redhat.com> - 1.7.20-8
- Add subpackage for platform-python (https://fedoraproject.org/wiki/Changes/Platform_Python_Stack)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.20-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.20-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.7.20-4
- Enable tests

* Tue Dec 13 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.7.20-3
- Rebuild for Python 3.6
- Disable tests for now

* Sat Dec 10 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.7.20-2
- Rebuild for gpgme 1.18

* Thu Aug 25 2016 Tomas Mlcoch <tmlcoch@redhat.com> - 1.7.20-1
- Tests: Disable test_download_packages_with_resume_02 test
- Update build utils to match new fedora spec schema

* Wed Aug 24 2016 Tomas Mlcoch <tmlcoch@redhat.com> - 1.7.19-1
- Add yumrecord substitution mechanism (mluscon)
- Fix a memory leak in signature verification (cwalters)

* Tue Aug 09 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.7.18-4
- Add %%{?system_python_abi}
- Trim ton of changelog

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.18-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Apr 07 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.7.18-2
- Adopt to new packaging guidelines
- Cleanups in spec file

* Fri Mar  4 2016 Tomas Mlcoch <tmlcoch@redhat.com> - 1.7.18-1
- Add new option LRO_FTPUSEEPSV
- Update AUTHORS
- downloader prepare_next_transfer(): simplify long line
- downloader prepare_next_transfer(): add missing error check
- downloader prepare_next_transfer(): cleanup error path
- downloader prepare_next_transfer() - fix memory leak on error path (Alan Jenkins)
- handle: Don't use proxy cache for downloads of metalink/mirrorlist
- handle: Don't set CURLOPT_HTTPHEADER into curl handle immediately when specified
- downloader: Implement logic for no_cache param in LrDownloadTarget (RhBug: 1297762)
- Add no_cache param to LrDownloadTarget and lr_downloadtarget_new()
- New test: always try to download from the fastest mirror (Alexander Todorov)
- Doc: Fixed minor doc typo (Philippe Ombredanne)
- Doc: Other updates
- Doc: Update default values in doc to reflect reality
