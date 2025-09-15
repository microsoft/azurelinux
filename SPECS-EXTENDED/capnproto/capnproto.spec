# Force out of source build
%undefine __cmake_in_source_build

%global modulename %{name}-c++

Name:           capnproto
Version:        1.0.1
Release:        4%{?dist}
Summary:        A data interchange format and capability-based RPC system

License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://capnproto.org

Source0:        https://capnproto.org/%{modulename}-%{version}.tar.gz

# We need C++
BuildRequires:  gcc-c++
BuildRequires:  cmake >= 3.1

# Ensure that we use matching version of libraries
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description
Cap’n Proto is an insanely fast data interchange format
and capability-based RPC system. Think JSON, except binary.
Or think Protocol Buffers, except faster. In fact, in benchmarks,
Cap’n Proto is INFINITY TIMES faster than Protocol Buffers.

This package contains the schema compiler and command-line
encoder/decoder tools.

%package        libs
Summary:        Libraries for %{name}

%description    libs
The %{name}-libs package contains the libraries for using %{name}
in applications.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -n %{modulename}-%{version} -p2

# Disable broken test
## Cf. https://github.com/capnproto/capnproto/issues/1349
## Cf. https://github.com/capnproto/capnproto/issues/1398
sed -e '/TEST(AsyncIo, AncillaryMessageHandler)/,/^}/s/^/\/\//' -i src/kj/async-io-test.c++


%build
# The tests are randomly failing due to poor sparsing support in the build system
export CFLAGS="%{build_cflags} -DHOLES_NOT_SUPPORTED=1"
export CXXFLAGS="%{build_cxxflags} -DHOLES_NOT_SUPPORTED=1"

%cmake -DBUILD_TESTING=ON
%cmake_build


%check
%ctest


%install
%cmake_install
find %{buildroot} -name '*.la' -delete


%files
%{_bindir}/capnp
%{_bindir}/capnpc
%{_bindir}/capnpc-c++
%{_bindir}/capnpc-capnp

%files libs
%license LICENSE.txt
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/CapnProto/

%changelog
* Fri Jun 14 2024 Henry Beberman <henry.beberman@microsoft.com> - 1.0.1-4
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 08 2023 Neal Gompa <ngompa@fedoraproject.org> - 1.0.1-1
- Rebase to 1.0.1

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Feb 28 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.10.3-3
- Backport upstream fix for missing headers for g++13
- Backport upstream fix for operator!= removal for C++20

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 02 2022 Fabio Valentini <decathorpe@gmail.com> - 0.10.3-1
- Update to version 0.10.3
- Fixes RHBZ#2149787
- Addresses CVE-2022-46149

* Tue Nov 29 2022 Neal Gompa <ngompa@fedoraproject.org> - 0.10.2-1
- Rebase to 0.10.2
- Drop backported patch

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 21 2021 Neal Gompa <ngompa@fedoraproject.org> - 0.9.1-1
- Rebase to 0.9.1
- Add patch to fix running tests
- Disable flaky/broken test per upstream guidance

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 18 2020 Neal Gompa <ngompa13@gmail.com> - 0.8.0-1
- Update to 0.8.0 (#1827443)
- Drop backported patches

* Thu Mar 12 2020 Neal Gompa <ngompa13@gmail.com> - 0.7.0-6
- Backport patch to fix aliasing violation breaking builds on GCC 10 on ARM (#1807872)
- Disable "DiskFile holes" test to stop build failures

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Björn Esser <besser82@fedoraproject.org> - 0.7.0-2
- Append curdir to CMake invokation. (#1668512)

* Sun Sep 23 2018 Neal Gompa <ngompa13@gmail.com> - 0.7.0-1
- Update to 0.7.0
- Drop upstreamed patches
- Drop obsolete ldconfig scriptlets

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Aug 06 2017 Björn Esser <besser82@fedoraproject.org> - 0.6.1-6
- Rebuilt for AutoReq cmake-filesystem

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun 09 2017 Neal Gompa <ngompa13@gmail.com> - 0.6.1-3
- Update patch based on upstream feedback

* Fri Jun 09 2017 Neal Gompa <ngompa13@gmail.com> - 0.6.1-2
- Adjust soversion patch to maintain binary compat across patch versions

* Fri Jun 09 2017 Neal Gompa <ngompa13@gmail.com> - 0.6.1-1
- Update to 0.6.1

* Mon Feb 27 2017 Neal Gompa <ngompa13@gmail.com> - 0.5.3-4
- Add patch to fix FTBFS with GCC 7 (#1423291)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Apr 28 2016 Neal Gompa <ngompa13@gmail.com> - 0.5.3-2
- Add patches to fix ppc builds

* Tue Apr 26 2016 Neal Gompa <ngompa13@gmail.com> - 0.5.3-1
- Initial packaging
