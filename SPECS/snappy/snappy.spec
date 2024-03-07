Summary:        Fast compression and decompression library
Name:           snappy
Version:        1.1.9
Release:        3%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System/Libraries
URL:            https://github.com/google/snappy

# A buildable snappy environment needs functioning submodules that do not work from the archive download
# To recreate the tar.gz run the following
#  sudo git clone https://github.com/google/snappy
#  git checkout <commitid-for-version>
#  pushd snappy
#  sudo git submodule update --init --recursive
#  popd
#  sudo mv %{name} %{name}-%{version}
#  sudo tar -cvf %{name}-%{version}.tar.gz %{name}-%{version}/
Source0:        https://github.com/google/snappy/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

Patch0:         snappy-inline.patch
Patch1:         detect_system_gtest.patch
Patch2:         build-with-rtti.patch
BuildRequires:  cmake >= 3.3
BuildRequires:  gmock-devel
BuildRequires:  gtest-devel

%description
Snappy is a compression/decompression library. It does not aim for maximum
compression, or compatibility with any other compression library; instead, it
aims for very high speeds and reasonable compression. For instance, compared to
the fastest mode of zlib, Snappy is an order of magnitude faster for most
inputs, but the resulting compressed files are anywhere from 20% to 100%
bigger.

%package	devel
Summary:	 Header and development files
Requires:	 %{name} = %{version}

%description	devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
mkdir build && cd build
%cmake -DSNAPPY_BUILD_BENCHMARKS:BOOL=OFF ..
%make_build

%install
%make_install -C build

%check
cd build
make test

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%doc AUTHORS
%{_libdir}/libsnappy.so.*

%files devel
%defattr(-,root,root)
%doc format_description.txt framing_format.txt
%{_includedir}/snappy*.h
%{_libdir}/libsnappy.so
%{_libdir}/cmake/Snappy/

%changelog
* Thu Nov 02 2023 Bala <balakumaran.kannan@microsoft.com> - 1.1.9-3
- Patch to fix build with RTTI enabled.

* Wed Mar 23 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 1.1.9-2
- Do not provide gtest/gmock headers and binaries.

* Wed Feb 09 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.1.9-1
- Update to version 1.1.9.
- Add patch for fixing compiler error due to missing 'inline'.

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.7-6
- Removing the explicit %%clean stage.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.1.7-5
- Added %%license line automatically

* Fri Apr 10 2020 Nick Samson <nisamson@microsoft.com> 1.1.7-4
- Updated Source0, URL, license info. Removed licenses not mentioned in source. Removed sha1.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.1.7-3
- Initial CBL-Mariner import from Photon (license: Apache2).

*  Wed Jan 09 2019 Michelle Wang <michellew@vmware.com> 1.1.7-2
-  Fix make check for snappy.

*  Wed Sep 19 2018 Srinidhi Rao <srinidhir@vmware.com> 1.1.7-1
-  Updating the version to 1.1.7.

*  Fri Dec 16 2016 Dheeraj Shetty <Dheerajs@vmware.com> 1.1.3-1
-  Initial build. First version.
