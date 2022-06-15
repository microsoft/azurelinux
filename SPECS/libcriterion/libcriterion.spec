%define pr_name criterion
Summary:        A cross-platform C and C++ unit testing framework for the 21st century
Name:           lib%{pr_name}
Version:        2.4.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries
URL:            https://github.com/Snaipe/Criterion
Source:         https://github.com/Snaipe/Criterion/releases/download/v%{version}/%{pr_name}-%{version}.tar.xz
BuildRequires:  clang
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  libffi-devel
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build
Requires:       gcc

%description
A dead-simple, yet extensible, C and C++ unit testing framework.
Full documentation: http://criterion.readthedocs.org/

%prep
%setup -q -n %{pr_name}-%{version}

%build
%meson
%ninja_build -C %{_target_platform}

%install
%ninja_install -C %{_target_platform}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/*.so*
%{_libdir}/*.a*
%{_lib64dir}/*.a
%{_includedir}/%{pr_name}/*.h
%{_includedir}/%{pr_name}/new/*.h
%{_includedir}/%{pr_name}/internal/*.h
%{_includedir}/%{pr_name}/internal/*.hxx
%{_includedir}/%{pr_name}/internal/assert/*.h
%{_includedir}/%{pr_name}/internal/assert/*.hxx
%{_libdir}/pkgconfig/*.pc
%{_datadir}/locale/de/LC_MESSAGES/criterion.mo
%{_datadir}/locale/fr/LC_MESSAGES/criterion.mo

%changelog
* Wed Jun 15 2022 Bala <balakumaran.kannan@microsoft.com> - 2.4.1-0
- Add libcriterion spec
- License verified
- Original version for CBL-Mariner
