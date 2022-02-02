Summary:        libmetalink is a Metalink library written in C language. It is intended to provide the programs written in C to add Metalink functionality such as parsing Metalink XML files.
Name:           libmetalink
Version:        0.1.3
Release:        1%{?dist}
License:        MIT
URL:            https://launchpad.net/libmetalink
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://launchpad.net/%{name}/trunk/%{name}-%{version}/+download/%{name}-%{version}.tar.gz
Patch0:         libmetalink-0.1.3-ns_uri.patch

BuildRequires:  glibc-devel
BuildRequires:  gcc
Requires:       glibc

%description
%{summary}

%package devel
Summary:        Header files and libraries for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains the header files
and libraries for use with %{name}.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install

find %{buildroot} -name '*.a'  -delete -print
find %{buildroot} -name '*.la' -delete -print

%files
%doc README
%license COPYING
%defattr(-,root,root)
%{_libdir}/%{name}.so.3*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/%{name}.so
%{_mandir}/man3/*

%changelog
* Fri Dec 10 2021 Mateusz Malisz <mamalisz@microsoft.com> 0.1.3-1
- Original version for CBL-Mariner
- License verified
