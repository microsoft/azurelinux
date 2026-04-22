# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global somajor 4

# Tests are flaky in Koji
%bcond_with tests

Name:           librist
Version:        0.2.7
Release: 11%{?dist}
Summary:        Library for Reliable Internet Stream Transport (RIST) protocol

# Everything used is BSD-2-Clause except getopt-shim, which is ISC as well
License:        BSD-2-Clause and ISC
URL:            https://code.videolan.org/rist/librist
Source0:        %{url}/-/archive/v%{version}/librist-v%{version}.tar.gz

# Backport from upstream
## From: https://code.videolan.org/rist/librist/-/commit/809390b3b75a259a704079d0fb4d8f1b5f7fa956
Patch0001:      0001-meson.build-fix-reference-to-libcjson-pc-file.patch

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  libcmocka-devel
BuildRequires:  mbedtls-devel
BuildRequires:  pkgconfig(libcjson)

%description
A library that can be used to speak the RIST protocol (as defined by Video
Services Forum (VSF) Technical Recommendations TR-06-1 and TR-06-2).


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        doc
Summary:        Technical documentation for %{name}
BuildArch:      noarch

%description    doc
The %{name}-doc package contains technical documentation for
developing applications that use %{name}.


%package -n     rist-tools
Summary:        User tools for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n rist-tools
This package contains the user tools for the RIST protocol library.


%prep
%autosetup -n %{name}-v%{version} -p1


%build
%meson
%meson_build


%install
%meson_install
# Strip unwanted executable bits
chmod -x %{buildroot}%{_includedir}/%{name}/*.h
chmod -x docs/*

# Install documentation
mkdir -p %{buildroot}%{_docdir}/%{name}
cp -av docs/* %{buildroot}%{_docdir}/%{name}


%if %{with tests}
%check
%meson_test
%endif


%files
%doc README.md CONTRIBUTING.md
%license COPYING
%{_libdir}/*.so.%{somajor}{,.*}

%files devel
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files doc
%license COPYING
# Co-own with librist package
%dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/VSF_TR-06-1.pdf
%doc %{_docdir}/%{name}/VSF_TR-06-2.pdf
%doc %{_docdir}/%{name}/librist_logo.png

%files -n rist-tools
%{_bindir}/rist*


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Mar 19 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 0.2.7-9
- Rebuild for mbedtls 3.6

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Sep 03 2024 Morten Stevens <mstevens@fedoraproject.org> - 0.2.7-6
- Rebuilt for mbedTLS 3.6.1

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Feb 15 2023 Neal Gompa <ngompa@fedoraproject.org> - 0.2.7-1
- Initial package
