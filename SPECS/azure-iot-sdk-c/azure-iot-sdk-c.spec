Summary:        Azure IoT C SDKs and Libraries
Name:           azure-iot-sdk-c
# azure-iot-sdk-c uses three different versioning schemes.
# On vcpkg, they use a date based versioning scheme, like yyyy-mm-dd.v, which corresponds to the LTS-mm_yyyy_Refv tag.
# We use yyyy.mm.dd.v since hyphens are prohibits in spec versions.
# For apt-get packages they fix the version number to 0.2.0 and increase the release number with each release.
# Since we want to control the release number as thr distribution, this scheme is not applicable for us.
# They also used to use a regular versioning scheme like 1.3.7 but they did not tag their latest LTS with a version like that.
Version:        2022.01.21
Release:        2%{?dist}
License:        MIT
Group:          Applications/File
URL:            https://github.com/Azure/azure-iot-sdk-c
Vendor:         Microsoft Corporation
Distribution:   Mariner
# Source0: https://github.com/Azure/%{name}/archive/LTS_01_2022_Ref01.tar.gz
# The below tarball includes all submodules.

# This tarball is created using the following command:
# git clone --recursive --single-branch --branch LTS_01_2022_Ref01 --depth 1 https://github.com/Azure/azure-iot-sdk-c.git
# tar cjvf azure-iot-sdk-c-2022.01.21.tar.bz2 azure-iot-sdk-c/
Source0:        %{name}-%{version}.tar.bz2
Patch0:         CVE-2024-21646.patch
BuildRequires:  cmake
BuildRequires:  build-essential
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  util-linux-devel
BuildRequires:  valgrind
Requires:       util-linux
Requires:       curl
Requires:       openssl

%description
The Microsoft Azure IoT device libraries for C contain code that facilitates
building devices and applications that connect to and are managed by Azure IoT Hub services.

The device library consists of a set of reusable components with abstract
interfaces that enable pluggability between stock and custom modules.

To meet the wide range of device requirements in the Internet of Things space,
the C libraries are provided in source code form to support multiple form factors,
operating systems, tools sets, protocols and communications patterns widely in use today.

%global debug_package %{nil}

%prep
%autosetup -p1 -n %{name}

%build
mkdir cmake
cd cmake

# Squelch warnings from being errors
export CFLAGS=" %{build_cflags}        \
    -Wno-error=unused-variable         \
    -Wno-error=missing-braces          \
    -Wno-error=unused-but-set-variable \
    -Wno-error=strict-aliasing         \
    -Wno-error=unknown-pragmas         \
    -Wno-error=enum-compare            \
    -Wno-error=unused-function         \
    -Wno-error=maybe-uninitialized     \
    -Wno-error=array-parameter         \
    -Wno-error=stringop-truncation"

cmake \
    -Duse_prov_client:BOOL=ON \
    -DCMAKE_SYSTEM_NAME=Linux \
    -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} ..
make %{?_smp_mflags}

%install
cd cmake
make DESTDIR=%{buildroot} install

install -d -m755 %{buildroot}%{_bindir}
install -p -m 755 provisioning_client/tools/tpm_device_provision/tpm_device_provision  %{buildroot}%{_bindir}/tpm_device_provision

%files
%defattr(-, root, root, -)
%license LICENSE
%{_includedir}/*
%{_bindir}/tpm_device_provision
%{_libdir}/*
/usr/cmake/*

%changelog
*   Tue Jan 16 2024 Minghe Ren <mingheren@microsoft.com> - 2022.01.21-2
-   Add patch for CVE-2024-21646

*   Mon Jan 24 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 2022.01.21-1
-   Upgrade to 2022.01.21.

*   Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2020.02.04.1-8
-   Removing the explicit %%clean stage.

*   Thu Nov 11 2021 Andrew Phelps <anphel@microsoft.com> 2020.02.04.1-7
-   Fix build with gcc11
*   Mon Jun 22 2020 Saravanan Somasundaram <sarsoma@microsoft.com> 2020.02.04.1-6
-   Removing the Conflict reference to azure-iot-sdk-c-public-preview.
*   Sun May 31 2020 Henry Beberman <henry.beberman@microsoft.com> 2020.02.04.1-5
-   Add -Wno-error to cflags to fix compilation with updated -Werror default.
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2020.02.04.1-4
-   Added %%license line automatically
*   Mon May 04 2020 Eric Li <eli@microsoft.com> 2020.02.04.1-3
-   Add #Source0: and license verified.
*   Wed Apr 29 2020 Emre Girgin <mrgirgin@microsoft.com> 2020.02.04.1-2
-   Build the provisioning client, add tpm_device_provision to the package.
*   Mon Apr 27 2020 Emre Girgin <mrgirgin@microsoft.com> 2020.02.04.1-1
-   Original version for CBL-Mariner.
