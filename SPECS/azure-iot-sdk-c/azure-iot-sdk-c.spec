Summary:        Azure IoT C SDKs and Libraries
Name:           azure-iot-sdk-c
# azure-iot-sdk-c uses three different versioning schemes.
# On vcpkg, they use a date based versioning scheme, like yyyy-mm-dd.v, which corresponds to the LTS-mm_yyyy_Refv tag.
# We use yyyy.mm.dd.v since hyphens are prohibits in spec versions.
# For apt-get packages they fix the version number to 0.2.0 and increase the release number with each release.
# Since we want to control the release number as thr distribution, this scheme is not applicable for us.
# They also used to use a regular versioning scheme like 1.3.7 but they did not tag their latest LTS with a version like that.
Version:        2020.02.04.1
Release:        7%{?dist}
# Source0: https://github.com/Azure/%{name}/archive/LTS_02_2020_Ref01.tar.gz
# The below tarball includes all submodules.

# This tarball is created using the following command:
# git clone --recursive --single-branch --branch LTS_02_2020_Ref01 --depth 1 https://github.com/Azure/azure-iot-sdk-c.git
# tar cjvf azure-iot-sdk-c-2020.02.04.1.tar.bz2 azure-iot-sdk-c/
Source0:        %{name}-%{version}.tar.bz2
License:        MIT
Group:          Applications/File
URL:            https://github.com/Azure/azure-iot-sdk-c
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  cmake
BuildRequires:  build-essential
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  util-linux-devel
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
%setup -qn %{name}

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
    -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} ..
make %{?_smp_mflags}

%install
cd cmake
make DESTDIR=%{buildroot} install

install -d -m755 %{buildroot}%{_bindir}
install -p -m 755 provisioning_client/tools/tpm_device_provision/tpm_device_provision  %{buildroot}%{_bindir}/tpm_device_provision

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root, -)
%license LICENSE
%dir %{_includedir}/azureiot
%{_includedir}/azureiot/*
%dir %{_includedir}/iothub_service_client
%{_includedir}/iothub_service_client/*
%dir %{_includedir}/umock_c
%{_includedir}/umock_c/*
%dir %{_includedir}/azure_macro_utils
%{_includedir}/azure_macro_utils/*
%dir %{_includedir}/azure_prov_client
%{_includedir}/azure_prov_client/*
%{_bindir}/tpm_device_provision
%{_lib64dir}/*
/usr/cmake/*

%changelog
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
