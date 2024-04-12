%global protoc_path %{_builddir}/%{name}-%{version}/cmake/protoc

Summary:        Google's data interchange format
Name:           protobuf
Version:        25.3
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Libraries
URL:            https://developers.google.com/protocol-buffers/
Source0:        https://github.com/protocolbuffers/protobuf/releases/download/v%{version}/%{name}-%{version}.tar.gz
BuildRequires:  abseil-cpp-devel
BuildRequires:  cmake
BuildRequires:  curl
BuildRequires:  libstdc++
BuildRequires:  unzip

%if %{with_check}
BuildRequires:  gtest-devel
BuildRequires:  gmock-devel
%endif

Provides:       %{name}-compiler = %{version}-%{release}
Provides:       %{name}-lite = %{version}-%{release}

%description
Protocol Buffers (a.k.a., protobuf) are Google's language-neutral, platform-neutral, extensible mechanism for serializing structured data. You can find protobuf's documentation on the Google Developers site.

%package        devel
Summary:        Development files for protobuf
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-lite-devel = %{version}-%{release}

%description    devel
The protobuf-devel package contains libraries and header files for
developing applications that use protobuf.

%package        static
Summary:        protobuf static lib
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-lite-static = %{version}-%{release}

%description    static
The protobuf-static package contains static protobuf libraries.

%package -n     python3-%{name}
Summary:        protobuf python3 lib
Group:          Development/Libraries
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       python3-libs
Provides:       %{name}-python3 = %{version}-%{release}

%description -n python3-%{name}
This contains protobuf python3 libraries.

%prep
%autosetup

%build
%{cmake} \
%if 0%{with_check}
    -Dprotobuf_USE_EXTERNAL_GTEST=ON \
%else
    -Dprotobuf_BUILD_TESTS=OFF \
%endif
    -Dprotobuf_ABSL_PROVIDER=package \
    -Dprotobuf_ABSL_MIN=20240116.0 \
    -Dprotobuf_BUILD_SHARED_LIBS=ON \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir}

%{cmake_build}

export PROTOC="%{protoc_path}"

pushd python
%{py3_build}
popd

%install
%{cmake_install}

export PROTOC="%{protoc_path}"

pushd python
%{py3_install}
popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%check
ctest --progress --output-on-failure

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/protoc*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_libdir}/cmake/*

%files static
%defattr(-,root,root)
%{_libdir}/*.a

%files -n python3-%{name}
%{python3_sitelib}/*

%changelog
* Thu Mar 21 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 25.3-1
- Upgraded to version 25.3.
- Switching to building with cmake and producing cmake package files.
- Updated the %%check stage.

* Mon Mar 20 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 3.17.3-2
- Added check section for running tests

* Fri Jul 23 2021 Thomas Crain <thcrain@microsoft.com> - 3.17.3-1
- Upgrade to latest upstream version, using upstream release tarball
- Add soname version to %%file packaging
- Remove protobuf-m2-%{version}.tar.gz source tarball (no longer needed with java removal)
- Change python3 subpackage name to python3-protobuf, to match Mariner naming conventions
- Remove python 2 subpackage
- Lint spec

* Mon Dec 07 2020 Joe Schmitt <joschmit@microsoft.com> - 3.6.1-9
- Remove java subpackage.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 3.6.1-8
- Added %%license line automatically

*   Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 3.6.1-7
-   Renaming apache-maven to maven

*   Wed Apr 29 2020 Nicolas Guibourge <nicolasg@microsoft.com> 3.6.1-6
-   Add add JAVA_HOME and path to libjli.so in LD_LIBRARY_PATH

*   Mon Apr 13 2020 Jon Slobodzian <joslobo@microsoft.com> 3.6.1-5
-   Verified license. Removed sha1. Fixed Source0 URL. Updated URL.

*   Thu Apr 09 2020 Andrew Phelps <anphel@microsoft.com> 3.6.1-4
-   Support building offline.

*   Thu Feb 27 2020 Andrew Phelps <anphel@microsoft.com> 3.6.1-3
-   Removed "--build=unknown-unknown-linux" configure flag

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.6.1-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Tue Sep 18 2018 Tapas Kundu <tkundu@vmware.com> 3.6.1-1
-   Update to version 3.6.1

*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 3.2.0-6
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.2.0-5
-   Use python2 explicitly while building

*   Thu May 18 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.2.0-4
-   Renamed openjdk to openjdk8

*   Fri Apr 28 2017 Siju Maliakkal <smaliakkal@vmware.com> 3.2.0-3
-   Update python3 version

*   Thu Apr 13 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.2.0-2
-   Build protobuf-java.

*   Fri Mar 31 2017 Rongrong Qiu <rqiu@vmware.com> 3.2.0-1
-   Upgrade to 3.2.0

*   Tue Mar 28 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.1-3
-   Build protobuf-python.

*   Mon Mar 20 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.1-2
-   Build static lib.

*   Fri Mar 03 2017 Xiaolin Li <xiaolinl@vmware.com> 2.6.1-1
-   Initial packaging for Photon
