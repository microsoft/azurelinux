Summary:        Small data compression library
Name:           liblzf
Version:        3.6
Release:        24%{?dist}
License:        BSD OR GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://oldhome.schmorp.de/marc/liblzf.html
Source0:        https://dist.schmorp.de/liblzf/liblzf-%{version}.tar.gz
# Adds autoconf and in particular support for building shared libraries.
# 7th Feb 2011 - Mail sent upstream to author. Awaiting conclusion.
Patch0:         liblzf-%{version}-autoconf-20140314.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  make

%description
LibLZF is a very small data compression library. It consists
of only two .c and two .h files and is very easy to
incorporate into your own programs.  The compression algorithm
is very, very fast, yet still written in portable C.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The liblzf-devel package contains libraries and header files for
developing applications that use liblzf.

%prep
%setup -q
%patch 0 -p1

%build
sh ./bootstrap.sh
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
# Binary does different things depending
# on the name it is called by.
pushd %{buildroot}%{_bindir}
ln -s lzf unlzf
popd
rm -f %{buildroot}%{_libdir}/liblzf.la

%ldconfig_scriptlets

%files
%license LICENSE
%{_bindir}/lzf
%{_bindir}/unlzf
%{_libdir}/liblzf.so.*
# The cs directory contains a .net implementation of lzf.
# Will happily add a .net sub package if given a patch.
%doc README Changes cs

%files devel
%{_includedir}/lzf.h
%{_includedir}/lzfP.h
%{_libdir}/liblzf.so
%{_libdir}/pkgconfig/liblzf.pc

%changelog
* Tue Nov 01 2022 Riken Maharjan <rmaharjan@microsoft.com> - 3.6-24
- Move to core

* Wed Jan 26 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.6-23
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified.

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 13 2014 Steve Traylen <steve.traylen@cern.ch> - 3.6-7
- Add lzfP.h file to package rhbz#1075911.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 14 2011 Steve Traylen <steve.traylen@cern.ch> - 3.6-2
- Add a .pc file in autoconf patch as well.
- Drop lzcat since conflicts with xz-lzma-compat

* Mon Feb 7 2011 Steve Traylen <steve.traylen@cern.ch> - 3.6-1
- First version of package.
