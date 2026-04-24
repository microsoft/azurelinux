# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:       ilbc
Summary:    Internet Low Bitrate Codec
Version:    3.0.4
Release: 18%{?dist}
License:    BSD-3-Clause
URL:        https://github.com/TimothyGu/libilbc

Source0:    %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:     %{name}-flags.patch
Patch1:     %{name}-s390.patch

BuildRequires:  abseil-cpp-devel
BuildRequires:  cmake
BuildRequires:  gcc-c++

%description
iLBC (internet Low Bitrate Codec) is a FREE speech codec suitable for robust
voice communication over IP. The codec is designed for narrow band speech and
results in a payload bit rate of 13.33 kbit/s with an encoding frame length of
30 ms and 15.20 kbps with an encoding length of 20 ms. The iLBC codec enables
graceful speech quality degradation in the case of lost frames, which occurs in
connection with lost or delayed IP packets.

%package    devel
Summary:    development files for %{name}
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
Additional header files for development with %{name}.

%prep
%autosetup -p1 -n libilbc-%{version}
# C++17 or later is required for absl::string_view based on std::string_view in
# abseil-cpp-20230125.0 and later. Setting -DCMAKE_CXX_STANDARD does not
# override CMakeLists.txt, so we patch it.
sed -r -i 's/(set\(CMAKE_CXX_STANDARD[[:blank:]]+)14\b/\117/' CMakeLists.txt

%build
%cmake -DBUILD_SHARED_LIBS=ON
%cmake_build

%install
%cmake_install

# Let RPM pick up the docs in the files section
rm -fr %{buildroot}%{_docdir}/libilbc

%files
%doc README.md NEWS.md
%license COPYING
%{_libdir}/lib%{name}.so.3
%{_libdir}/lib%{name}.so.%{version}

%files devel
%{_bindir}/%{name}_test
%{_includedir}/%{name}.h
%{_includedir}/%{name}_export.h
%{_libdir}/pkgconfig/lib%{name}.pc
%{_libdir}/lib%{name}.so

%changelog
* Mon Sep 08 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 3.0.4-17
- Rebuilt for abseil-cpp 20250814.0

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon May 26 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 3.0.4-15
- Rebuilt for abseil-cpp 20250512.0

* Tue Feb 25 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 3.0.4-14
- Rebuilt for abseil-cpp-20250127.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Aug 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 3.0.4-12
- Rebuilt for abseil-cpp-20240722.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 04 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 3.0.4-10
- Rebuilt for abseil-cpp-20240116.0

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Peter Lemenkov <lemenkov@gmail.com> - 3.0.4-8
- Switch to SPDX tag

* Wed Aug 30 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 3.0.4-7
- Rebuilt for abseil-cpp 20230802.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Mar 05 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 3.0.4-5
- Build as C++17 for abseil-cpp-20230125 compatibility

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Aug 22 2022 Peter Lemenkov <lemenkov@gmail.com> - 3.0.4-3
- Rebuilt for abseil-cpp 20220623.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed May 25 2022 Simone Caronni <negativo17@gmail.com> - 3.0.4-1
- Update to 3.0.4.
- Drop 2012 compatibility hacks.
- Trim changelog.

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 19 2019 Neal Gompa <ngompa13@gmail.com> - 1.1.1-16
- Modernize spec
- Drop EL5 specific stuff

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
