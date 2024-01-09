Summary:        GNU Ubiquitous Intelligent Language for Extensions
Name:           guile
Version:        3.0.9
Release:        1%{?dist}
License:        LGPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://www.gnu.org/software/guile/
Source0:        ftp://ftp.gnu.org/pub/gnu/guile/%{name}-%{version}.tar.gz
BuildRequires:  gc-devel
BuildRequires:  libffi-devel
BuildRequires:  libltdl-devel
BuildRequires:  libunistring-devel
Requires:       gc
Requires:       glibc-iconv
Requires:       gmp
Requires:       libffi
Requires:       libltdl
Requires:       libunistring

%description
GUILE (GNU's Ubiquitous Intelligent Language for Extension) is a library
implementation of the Scheme programming language, written in C.  GUILE
provides a machine-independent execution platform that can be linked in
as a library during the building of extensible programs.

%package devel
Summary:        Development libraries and header files for guile
Requires:       guile
Requires:       libltdl-devel
Requires:       libunistring-devel

%description devel
The package contains libraries and header files for
developing applications that use guile.

%prep
%setup -q

%build
./configure \
	--prefix=%{_prefix} \
	--disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete -print
rm %{buildroot}%{_libdir}/*.scm
rm %{buildroot}%{_infodir}/*

# Create symlinks for compatibility
ln -s guile %{buildroot}%{_bindir}/guile2
ln -s guile-tools %{buildroot}%{_bindir}/guile2-tools

%check
make  %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/guile/*
%{_mandir}/man1/*
%{_datadir}/aclocal/*.m4
%{_datadir}/guile/*

%files devel
%defattr(-,root,root)
%{_includedir}/guile/3.0/*.h
%{_includedir}/guile/3.0/libguile/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Jan 09 2024 Brian Fjeldstad <bfjelds@microsoft.com> 3.0.9-1
- Update to 3.0.9.

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.0.14-5
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Fri Sep 10 2021 Thomas Crain <thcrain@microsoft.com> - 2.0.14-4
- Remove libtool archive files from final packaging

* Tue Jan 05 2021 Joe Schmitt <joschmit@microsoft.com> - 2.0.14-3
- Add compatibility symlinks for guile and guile-tools binaries.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.0.14-2
- Added %%license line automatically

* Mon Mar 16 2020 Henry Beberman <henry.beberman@microsoft.com> 2.0.14-1
- Update to 2.0.14. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.0.13-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed May 03 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.0.13-2
- Adding glibc-iconv to Requires section

* Wed Jan 18 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.0.13-1
- Bumped to latest version 2.0.13 to handle CVE-2016-8606

* Thu Oct 06 2016 ChangLee <changlee@vmware.com> 2.0.11-3
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.11-2
- GA - Bump release of all rpms

* Thu Jun 18 2015 Divya Thaluru <dthaluru@vmware.com> 2.0.11-1
- Initial build. First version
