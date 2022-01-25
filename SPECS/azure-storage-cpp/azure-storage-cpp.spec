%define _build_id_links none

Name:           azure-storage-cpp
Summary:        Azure Storage Client Library for C++
Version:        7.5.0
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://azure.github.io/azure-storage-cpp/
Vendor:         Microsoft Corporation
Distribution:   Mariner
#Source0:       https://github.com/Azure/azure-storage-cpp/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  util-linux-devel
BuildRequires:  openssl-devel
BuildRequires:  boost-devel
BuildRequires:  libxml2-devel
BuildRequires:  cpprest-devel
BuildRequires:  cmake

Requires:       openssl
Requires:       libxml2
Requires:       cpprest
Requires:       util-linux
Requires:       boost

%description
The Azure Storage Client Library for C++ allows you to build applications against Microsoft Azure Storage.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}
Requires:       cpprest-devel

%description devel
The Azure Storage Client Library for C++ allows you to build applications against Microsoft Azure Storage.

%prep
%setup -q

%build
CMAKE_OPTS="\
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
"

mkdir -pv Microsoft.WindowsAzure.Storage/build
cd Microsoft.WindowsAzure.Storage/build
cmake $CMAKE_OPTS ..
make %{?_smp_mflags}

%install
cd Microsoft.WindowsAzure.Storage/build
make %{?_smp_mflags} DESTDIR=%{buildroot} install

%files
%license LICENSE.txt
%doc README.md
%{_libdir}/*.so.*

%files devel
%{_includedir}/was/*
%{_includedir}/wascore/*
%{_libdir}/libazurestorage.so

%changelog
*   Mon Jan 24 2022 Nicolas Guibourge <nicolasg@microsoft.com> 7.5.0-1
-   Upgrade to 7.5.0.

*   Fri Oct 16 2020 Jonathan Slobodzian <joslobo@microsoft.com> 7.3.0-2
-   License Verified.  Update Source0 Location.  Integrated into Mariner Core.

*   Mon Mar 30 2020 Jonathan Chiu <jochi@microsoft.com> 7.3.0-1
-   Original version for CBL-Mariner.

