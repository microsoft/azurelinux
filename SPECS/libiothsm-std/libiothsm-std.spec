Summary:        Azure IoT standard mode HSM lib
Name:           libiothsm-std
Version:        1.2.5
Release:        1%{?dist}

# A buildable azure-iotedge environments needs functioning submodules that do not work from the archive download
# Tracking github issue is: https://github.com/Azure/iotedge/issues/1685
# To recreate the tar.gz run the following
#  sudo git clone https://github.com/Azure/iotedge.git -b %%{version}
#  pushd iotedge
#  sudo git submodule update --init --recursive
#  popd
#  sudo mv iotedge azure-iotedge-%%{version}
#  sudo tar --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf azure-iotedge-%%{version}.tar.gz azure-iotedge-%%{version}
#
#   NOTES:
#       - You require GNU tar version 1.28+.
#       - The additional options enable generation of a tarball with the same hash every time regardless of the environment.
#         See: https://reproducible-builds.org/docs/archives/
#       - For the value of "--mtime" use the date "2021-04-26 00:00Z" to simplify future updates.

Source0:       azure-iotedge-%{version}.tar.gz
License:        MIT
Group:          Applications/Libraries
URL:            https://github.com/azure/iotedge
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  cmake
BuildRequires:  curl-devel
BuildRequires:  readline-devel
Requires:       openssl

%description
Azure IoT standard mode Hardware Security Module library.
This library is used to interface with the TPM from Azure IoT Edge.

%global debug_package %{nil}

%prep
%setup -q -n %{_topdir}/BUILD/azure-iotedge-%{version}/edgelet/hsm-sys/azure-iot-hsm-c

%build
cd %{_topdir}/BUILD/azure-iotedge-%{version}/edgelet/hsm-sys/azure-iot-hsm-c
cmake -DCMAKE_BUILD_TYPE="Release" -DBUILD_SHARED="ON" -Duse_emulator="OFF" -Duse_default_uuid=On -Duse_http=Off -DCMAKE_INSTALL_LIBDIR="%{buildroot}%{_libdir}" .
%make_build

%install
%make_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%license LICENSE
%{_libdir}/libiothsm.so*

%changelog
*   Fri Nov 12 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.5-1
-   Update to version 1.2.5 to be compatible with GCC 11.
-   Removing invalid 'Source0' comment.
*   Fri May 14 2021 Andrew Phelps <anphel@microsoft.com> 1.1.2-1
-   Update to version 1.1.2
*   Tue Feb 23 2021 Andrew Phelps <anphel@microsoft.com> 1.1.0-1
-   Update to version 1.1.0
*   Wed May 27 2020 Andrew Phelps <anphel@microsoft.com> 1.0.9.1-1
-   Update to version 1.0.9.1. Fix tarball build notes.
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.0.9-3
-   Added %%license line automatically
*   Sat Apr 11 2020 Mohan Datla <mdatla@microsoft.com> 1.0.9-1
-   Update to 1.0.9. License verified.
*   Tue Dec 3 2019 Henry Beberman <hebeberm@microsoft.com> 1.0.8.4-1
-   Original version for CBL-Mariner.
