Summary:        Utility and library for manipulating constant databases
Name:           tinycdb
Version:        0.78
Release:        15%{?dist}
License:        Public Domain
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.corpit.ru/mjt/tinycdb.html
Source0:        https://www.corpit.ru/mjt/%{name}/%{name}-%{version}.tar.gz
# taken from the 0.77 tarball
Source1:        libcdb.pc
BuildRequires:  gcc

%description
tinycdb is a small, fast and reliable utility and subroutine library for
creating and reading constant databases. The database structure is tuned
for fast reading.

This package contains tinycdb utility and shared library.

%package        devel
Summary:        Development files for tinycdb
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
tinycdb is a small, fast and reliable utility set and subroutine
library for creating and reading constant databases.

This package contains tinycdb development library and header file for
developing applications that use %{name}.

%prep
%setup -q
cp %{SOURCE1} debian/
# Fix libdir pathing in pkgconfig file.
sed -i -e 's\/lib\/%{_lib}\g' debian/libcdb.pc

%build
%make_build staticlib sharedlib cdb-shared CFLAGS="%{optflags}"

%install
mkdir -p %{buildroot}%{_libdir}
make DESTDIR=%{buildroot} prefix=%{_prefix} libdir=%{_libdir} mandir=%{_mandir} \
	install install-sharedlib INSTALLPROG=cdb-shared CP="cp -p"
chmod +x %{buildroot}%{_libdir}/*.so.*
rm -f %{buildroot}%{_libdir}/lib*.a
mkdir -p %{buildroot}%{_libdir}/pkgconfig
cp -p debian/libcdb.pc %{buildroot}%{_libdir}/pkgconfig/libcdb.pc

%ldconfig_scriptlets

%files
%license debian/copyright
%doc NEWS ChangeLog
%{_bindir}/cdb
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{_libdir}/*.so.*

%files devel
%{_includedir}/*.h
%{_mandir}/man3/*.3*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Dec 08 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.78-15
- License verified
- Lint spec

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.78-14
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.78-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.78-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.78-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.78-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.78-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.78-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.78-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.78-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.78-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.78-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.78-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.78-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 22 2014 Tom Callaway <spot@fedoraproject.org> - 0.78-1
- update to 0.78

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.77-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.77-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.77-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 26 2012 Tom Callaway <spot@fedoraproject.org> - 0.77-4
- revive

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.77-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 13 2010 Chen Lei <supercyper@163.com> - 0.77-2
- add pkgconfig file

* Wed Jul 07 2010 Chen Lei <supercyper@163.com> - 0.77-1
- initial rpm build
