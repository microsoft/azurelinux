Summary:        Google's data interchange format - C implementation
Name:           protobuf-c
Version:        1.4.1
Release:        1%{?dist}
License:        BSD-3-Clause
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries
URL:            https://github.com/protobuf-c/protobuf-c
Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz
BuildRequires:  curl
BuildRequires:  libstdc++
BuildRequires:  make
BuildRequires:  pkg-config
BuildRequires:  unzip
BuildRequires:  pkgconfig(protobuf) >= 2.6.0
Requires:       protobuf
Provides:       %{name}-compiler = %{version}-%{release}

%description
Protocol Buffers (a.k.a., protobuf) are Google's language-neutral, platform-neutral, extensible mechanism for serializing structured data. You can find protobuf's documentation on the Google Developers site. This is the C implementation.

%package        devel
Summary:        Development files for protobuf
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The protobuf-c-devel package contains libraries and header files for
developing applications that use protobuf-c.

%package        static
Summary:        protobuf-c static lib
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    static
The protobuf-c-static package contains static protobuf-c libraries.

%prep
%autosetup -p1

%build
%configure --disable-silent-rules
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

%check
%make_build check

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/protoc-c
%{_bindir}/protoc-gen-c
%{_libdir}/libprotobuf-c.so.1*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/libprotobuf-c.so

%files static
%defattr(-,root,root)
%{_libdir}/libprotobuf-c.a

%changelog
* Mon Apr 24 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.4.1-1
- Auto-upgrade to 1.4.1 - to fix CVE-2022-48468
- Remove CVE-2022-33070 patch as not required for 1.4.1

* Thu Jul 21 2022 Henry Li <lihl@microsoft.com> - 1.4.0-2
- Add patch to resolve CVE-2022-33070

* Fri Jul 23 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.4.0-1
- Upgrade to latest upstream version
- Add check section
- Remove libtool archives from devel subpackage
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.3.1-4
- Added %%license line automatically

* Fri Mar 03 2020 Jon Slobodzian <joslobo@microsoft.com> - 1.20.2-3
- Fixed Source URL. Verified license. Fixed URL. Fixed Source URL.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.3.1-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Sep 19 2018 Tapas Kundu <tkundu@vmware.com> - 1.3.1-1
- Updated to release 1.3.1

* Thu Mar 30 2017 Vinay Kulkarni <kulkarniv@vmware.com> - 1.2.1-2
- Fix protobuf-c-static requires

* Sat Mar 18 2017 Vinay Kulkarni <kulkarniv@vmware.com> - 1.2.1-1
- Initial packaging for Photon
