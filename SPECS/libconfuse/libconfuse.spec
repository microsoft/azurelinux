Summary:        Configuration file parser library
Name:           libconfuse
Version:        3.3
Release:        1%{?dist}
License:        ISC
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries
URL:            https://github.com/libconfuse/libconfuse
Source0:        https://github.com/libconfuse/libconfuse/releases/download/v%{version}/confuse-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
libConfuse is a configuration file parser library written in C.
It supports sections and (lists of) values, as well as other features
such as single/double quoted strings, environment variable expansion,
functions and nested include statements. Values can be strings,
integers, floats, booleans, and sections.

%package devel
Summary:        Development headers for libconfuse.
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
%{summary}

%prep
%autosetup -p1 -n confuse-%{version}

%build
%configure
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%{_libdir}/*.so*

%files devel
%license LICENSE
%doc README.md
%exclude %{_libdir}/libconfuse.a
%exclude %{_datadir}/locale
%{_docdir}
%{_includedir}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/libconfuse.pc

%changelog
* Mon Feb 08 2021 Henry Beberman <henry.beberman@microsoft.com> 3.3-1
- Add libconfuse spec
- License verified
- Original version for CBL-Mariner
