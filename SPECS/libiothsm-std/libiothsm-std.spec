
%global debug_package %{nil}

Summary:        Azure IoT standard mode HSM lib
Name:           libiothsm-std
Version:        1.1.8
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Libraries
URL:            https://github.com/azure/iotedge
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
Source0:        azure-iotedge-%{version}.tar.gz
Patch1:         hmac.c-fix-mismatching-function-prototype.patch
BuildRequires:  cmake
BuildRequires:  curl-devel
BuildRequires:  readline-devel
Requires:       openssl

%description
Azure IoT standard mode Hardware Security Module library.
This library is used to interface with the TPM from Azure IoT Edge.

%prep
%setup -q -n azure-iotedge-%{version}/edgelet/hsm-sys/azure-iot-hsm-c
%patch1 -p1 -d deps/c-shared

%build
cmake -DCMAKE_BUILD_TYPE="Release" -DBUILD_SHARED="ON" -Duse_emulator="OFF" -Duse_default_uuid=On -Duse_http=Off -DCMAKE_INSTALL_LIBDIR="%{_libdir}" .
%make_build

%install
%make_install

%files
%defattr(-,root,root)
%license LICENSE
%{_libdir}/libiothsm.so*

%changelog
* Fri Nov 12 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.8-1
- Update to version 1.1.8 to be compatible with GCC 11.
- Applying a GCC 11 patch.
- Removing invalid 'Source0' comment.

* Fri May 14 2021 Andrew Phelps <anphel@microsoft.com> - 1.1.2-1
- Update to version 1.1.2

* Tue Feb 23 2021 Andrew Phelps <anphel@microsoft.com> - 1.1.0-1
- Update to version 1.1.0

* Wed May 27 2020 Andrew Phelps <anphel@microsoft.com> - 1.0.9.1-1
- Update to version 1.0.9.1. Fix tarball build notes.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.0.9-3
- Added %%license line automatically

* Sat Apr 11 2020 Mohan Datla <mdatla@microsoft.com> - 1.0.9-1
- Update to 1.0.9. License verified.

* Tue Dec 3 2019 Henry Beberman <hebeberm@microsoft.com> - 1.0.8.4-1
- Original version for CBL-Mariner.
