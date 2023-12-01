Summary:        fork of the original IJG libjpeg which uses SIMD.
Name:           libjpeg-turbo
Version:        2.1.4
Release:        1%{?dist}
License:        IJG
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://sourceforge.net/projects/libjpeg-turbo
Source0:        http://downloads.sourceforge.net/libjpeg-turbo/%{name}-%{version}.tar.gz
BuildRequires:  cmake
Provides:       libjpeg = 6b-47
Provides:       turbojpeg = %{version}-%{release}
Provides:       %{name}-utils = %{version}-%{release}
%ifarch x86_64
BuildRequires:  nasm
%endif

%description
libjpeg-turbo is a fork of the original IJG libjpeg which uses SIMD to accelerate baseline JPEG compression and decompression. libjpeg is a library that implements JPEG image encoding, decoding and transcoding.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Provides:       libjpeg-devel = 6b-47
Provides:       libjpeg-devel%{?_isa} = 6b-47
Provides:       turbojpeg-devel = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup

%build
mkdir build
pushd build
%cmake -DCMAKE_SKIP_RPATH:BOOL=YES \
       -DCMAKE_SKIP_INSTALL_RPATH:BOOL=YES \
       -DENABLE_STATIC:BOOL=NO ..
%make_build
popd

%install
pushd build
%make_install
popd

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license LICENSE.md
%{_bindir}/*
%{_libdir}/*.so.*
%{_datadir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/%{name}/%{name}*.cmake

%changelog
* Tue Sep 13 2022 Nan Liu <liunan@microsoft.com> - 2.1.4-1
- Upgrade to version 2.1.4 to fix CVE-2020-35538

* Fri Jan 07 2022 Henry Li <lihl@microsoft.com> - 2.1.2-1
- Upgrade to version 2.1.2
- Add related cmake files to libjpeg-turbo-devel pacakge
- License Verified

* Fri Jul 26 2021 Henry Beberman <henry.beberman@microsoft.com> - 2.0.0-9
- Patch CVE-2020-17541 (JOSLOBO: Dash rolled for merge)

* Fri Jul 23 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.0.0-8
- Add provides for turbojpeg, turbojpeg-devel packages, utils subpackage

* Thu Dec 10 2020 Joe Schmitt <joschmit@microsoft.com> - 2.0.0-7
- Provide libjpeg and libjpeg-devel along with an isa version of libjpeg-devel.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.0.0-6
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.0.0-5
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Mar 04 2019 Keerthana K <keerthanak@vmware.com> - 2.0.0-4
- Update BuildRequires nasm only for x86_64.

* Wed Feb 06 2019 Sujay G <gsujay@vmware.com> - 2.0.0-3
- Added patch to fix CVE-2018-19664

* Thu Jan 10 2019 Sujay G <gsujay@vmware.com> - 2.0.0-2
- Added patch to fix CVE-2018-20330

* Sun Sep 20 2018 Bo Gan <ganb@vmware.com> - 2.0.0-1
- Update to 2.0.0
- cmake build system

* Mon Dec 11 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.5.2-2
- Fix CVE-2017-15232

* Wed Aug 09 2017 Dheeraj Shetty <dheerajs@vmware.com> - 1.5.2-1
- Updated to version 1.5.2

* Tue Apr 11 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 1.5.1-1
- Updated to version 1.5.1

* Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> - 1.5.0-1
- Initial version
