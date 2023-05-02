%define _build_id_links none

Name:           fluent-bit
Summary:        Fast and Lightweight Log processor and forwarder for Linux, BSD and OSX
Version:        1.5.2
Release:        3%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://fluentbit.io
#Source0:       https://github.com/fluent/%{name}/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Patch0:    CVE-2021-46878.patch
Patch0:    CVE-2021-46879.patch

BuildRequires:  cmake
BuildRequires:  systemd-devel

%description
Fluent Bit is a fast Log Processor and Forwarder for Linux, Embedded Linux, MacOS and BSD 
family operating systems. It's part of the Fluentd Ecosystem and a CNCF sub-project.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}

%description devel
Development files for %{name}

%prep
%setup -q
%patch0 -p1
%patch0 -p1

%build
cd build
cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} -DFLB_IN_SYSTEMD=On ..
make %{?_smp_mflags}

%install
cd build
make install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%exclude /usr/src/debug
/lib/systemd/system/fluent-bit.service
%{_bindir}/*
/usr/etc/fluent-bit/*

%files devel
%{_includedir}/*
/usr/lib64/fluent-bit/*.so

%changelog
* Tue May 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.5.2-3
- Add patch for CVE-2021-46879, CVE-2021-46878

* Fri Sep 10 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> 1.5.2-2
- Enable plug-in for systemd support

* Mon May 24 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> 1.5.2-1
- Update to version 1.5.2

* Mon Oct 19 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.4.1-2
- License verified.
- Fixed source URL.
- Added 'Vendor' and 'Distribution' tags.
* Mon Mar 30 2020 Jonathan Chiu <jochi@microsoft.com> 1.4.1-1
- Original version for CBL-Mariner.

