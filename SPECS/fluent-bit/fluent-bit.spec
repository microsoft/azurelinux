Summary:        Fast and Lightweight Log processor and forwarder for Linux, BSD and OSX
Name:           fluent-bit
Version:        3.0.6
Release:        2%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://fluentbit.io
Source0:        https://github.com/fluent/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         CVE-2024-34250.patch
Patch1:         CVE-2024-25629.patch
Patch2:         CVE-2024-28182.patch
Patch3:         CVE-2024-25431.patch
Patch4:         CVE-2024-27532.patch
Patch5:         CVE-2024-50608.patch
Patch6:         CVE-2024-50609.patch
BuildRequires:  bison
BuildRequires:  cmake
BuildRequires:  cyrus-sasl-devel
BuildRequires:  doxygen
BuildRequires:  flex
BuildRequires:  gcc-c++
BuildRequires:  gnutls-devel
BuildRequires:  graphviz
BuildRequires:  libpq-devel
BuildRequires:  libyaml-devel
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig
BuildRequires:  systemd-devel
BuildRequires:  systemd-rpm-macros
BuildRequires:  zlib-devel

%description

Fluent Bit is a fast Log Processor and Forwarder for Linux, Embedded Linux, MacOS and BSD
family operating systems. It's part of the Fluentd Ecosystem and a CNCF sub-project.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}

%description devel
Development files for %{name}

%prep
%autosetup -p1

%build

%cmake\
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DFLB_EXAMPLES=Off \
    -DFLB_OUT_SLACK=Off \
    -DFLB_IN_SYSTEMD=On \
    -DFLB_OUT_TD=Off \
    -DFLB_OUT_ES=Off \
    -DFLB_SHARED_LIB=On \
%if %{with_check}
    -DFLB_TESTS_RUNTIME=On \
    -DFLB_TESTS_INTERNAL=On \
%endif
    -DFLB_RELEASE=On \
    -DFLB_DEBUG=Off \
    -DFLB_TLS=On \
    -DFLB_JEMALLOC=On \

%cmake_build

%install
%cmake_install

%check
%ctest --exclude-regex "flb-rt-in_podman_metrics|.*\\.sh"

%files
%license LICENSE
%doc README.md
%exclude %{_prefix}/src/debug
%{_unitdir}/fluent-bit.service
%{_bindir}/*
%{_prefix}%{_sysconfdir}/fluent-bit/*
%exclude %{_bindir}/luajit
%exclude %{_libdir}/libluajit.a

%files devel
%{_includedir}/*
%{_libdir}/fluent-bit/*.so

%changelog
* Thu Feb 27 2025 Kshitiz Godara <kgodara@microsoft.com> - 3.0.6-2
- Address CVE-2024-50608 and CVE-2024-50609

* Fri Jan 17 2025 Sudipta Pandit <sudpandit@microsoft.com> - 3.0.6-1
- Bump version to 3.0.6
- Add patches for multiple CVEs for the current version
- Remove patches for multiple fixes not required for this version

* Fri Jan 10 2025 Kshitiz Godara <kgodara@microsoft.com> - 2.2.3-7
- Enable luajit support
- Exclude luajit binary from final package to remove conflict with luajit package
- Exclude luajit static library from package as not needed

* Tue Dec 10 2024 Sudipta Pandit <sudpandit@microsoft.com> - 2.2.3-6
- Backport fix for CVE-2024-27532

* Fri Nov 15 2024 Ankita Pareek <ankitapareek@microsoft.com> - 2.2.3-5
- Address CVE-2024-25431

* Tue Oct 15 2024 Chris Gunn <chrisgun@microsoft.com> - 2.2.3-4
- CVE-2024-26455
- CVE-2024-25629

* Wed Jun 05 2024 Sindhu Karri <lakarri@microsoft.com> - 2.2.3-3
- Apply patch in_emitter_fix_issue_8198.patch to fix #8198 ( Potential log loss during high load at Multiline & Rewrite Tag Filter (in_emitter) )
- Fix issue #8025 with a patch ( in_tail: missing log for offset processing due to non-existent old inodes in sqlite )

* Thu May 30 2024 Sindhu Karri <lakarri@microsoft.com> - 2.2.3-2
- Fix CVE-2024-34250 with a patch

* Tue May 28 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.2.3-1
- Auto-upgrade to 2.2.3 - CVE-2024-4323

* Wed Apr 03 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.2.2-1
- Auto-upgrade to 2.2.2 - CVE-2024-23722

* Wed Jan 10 2024 Henry Li <lihl@microsoft.com> - 2.1.10-3
- Address CVE-2023-52284
- Change to autosetup

* Wed Dec 06 2023 Chris Gunn <chrisgun@Microsoft.com> - 2.1.10-2
- CVE-2023-48105

* Tue Oct 31 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.1.10-1
- Auto-upgrade to 2.1.10 - upgrade to latest

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.0.9-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Fri Feb 24 2023 Olivia Crain <oliviacrain@microsoft.com> - 2.0.9-1
- Upgrade version to 2.0.9
- Use SPDX license expression in license tag
- Explicitly disable luajit

* Wed Aug 03 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.9.6-1
- Upgrade version to 1.9.6
- Add build time dependency libyaml-devel

* Sat Feb 19 2022 Sriram Nambakam <snambakam@microsoft.com> - 1.8.12-2
- Compile with -DFLB_JEMALLOC=on.

* Tue Feb 01 2022 Cameron Baird <cameronbaird@microsoft.com> - 1.8.12-1
- Update to version 1.8.12

* Mon May 24 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.5.2-1
- Update to version 1.5.2

* Mon Oct 19 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4.1-2
- License verified.
- Fixed source URL.
- Added 'Vendor' and 'Distribution' tags.

* Mon Mar 30 2020 Jonathan Chiu <jochi@microsoft.com> - 1.4.1-1
- Original version for CBL-Mariner.
