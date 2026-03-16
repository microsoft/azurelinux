Summary:        Fast and Lightweight Log processor and forwarder for Linux, BSD and OSX
Name:           fluent-bit
Version:        3.1.10
Release:        4%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://fluentbit.io
Source0:        https://github.com/fluent/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         CVE-2024-34250.patch
Patch1:         CVE-2024-25431.patch
Patch2:         CVE-2024-27532.patch
Patch3:         CVE-2024-50608.patch
Patch4:         CVE-2024-50609.patch
Patch5:         CVE-2025-31498.patch
Patch6:         CVE-2025-54126.patch
Patch7:         CVE-2025-58749.patch
Patch8:         CVE-2025-12970.patch
Patch9:         CVE-2025-12977.patch
Patch10:        CVE-2025-12969.patch
Patch11:        CVE-2025-62408.patch
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
BuildRequires:  luajit-devel
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
%if 0%{?with_check}
    -DFLB_TESTS_RUNTIME=On \
    -DFLB_TESTS_INTERNAL=On \
%endif
    -DFLB_RELEASE=On \
    -DFLB_DEBUG=Off \
    -DFLB_TLS=On \
    -DFLB_JEMALLOC=On \
    -DFLB_PREFER_SYSTEM_LIBS=On

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

%files devel
%{_includedir}/*
%{_libdir}/fluent-bit/*.so

%changelog
* Wed Dec 17 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 3.1.10-4
- Patch for CVE-2025-62408

* Mon Dec 08 2025 BinduSri Adabala <v-badabala@microsoft.com> - 3.1.10-3
- Patch for CVE-2025-12977 and CVE-2025-12969

* Mon Dec 01 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 3.1.10-2
- Patch for CVE-2025-12970

* Mon Dec 01 2025 Kanishk Bansal <kanbansal@microsoft.com> - 3.1.10-1
- Upgrade to 3.1.10

* Thu Sep 25 2025 Aditya Singh <v-aditysing@microsoft.com> - 3.1.9-6
- Patch for CVE-2025-58749

* Wed Aug 06 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 3.1.9-5
- Patch for CVE-2025-54126

* Fri Apr 11 2025 Ankita Pareek <ankitapareek@microsoft.com> - 3.1.9-4
- Address CVE-2025-31498 with a patch

* Wed Feb 26 2025 Kshitiz Godara <kgodara@microsoft.com> - 3.1.9-3
- Address CVE-2024-50608 and CVE-2024-50609

* Tue Dec 10 2024 Sudipta Pandit <sudpandit@microsoft.com> - 3.1.9-2
- Backport fixes for CVE-2024-27532

* Tue Nov 23 2024 Paul Meyer <paul.meyer@microsoft.com> - 3.1.9-1
- Update to 3.1.9 to enable Lua filter plugin using system luajit library.
- Remove patches for CVE-2024-25629 and CVE-2024-28182 as they are fixed in 3.1.9.
- [Jon Slobodzian] Reconciled with Fasttrack/3.0 on 11/23, updated Changelog date from 11/5.

* Fri Nov 15 2024 Ankita Pareek <ankitapareek@microsoft.com> - 3.0.6-3
- Address CVE-2024-25431

* Tue Oct 15 2024 Chris Gunn <chrisgun@microsoft.com> - 3.0.6-2
- CVE-2024-34250
- CVE-2024-25629
- CVE-2024-28182

* Tue May 28 2024 Neha Agarwal <nehaagarwal@microsoft.com> - 3.0.6-1
- Update to v3.0.6 to fix CVE-2024-4323.

* Thu May 16 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.0.3-1
- Auto-upgrade to 3.0.3 - https://microsoft.visualstudio.com/OS/_workitems/edit/50531424

* Tue Feb 20 2024 Sumedh Sharma <sumsharma@microsoft.com> - 2.2.2-1
- Upgrade to version 2.2.2

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
