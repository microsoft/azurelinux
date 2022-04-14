Vendor:         Microsoft Corporation
Distribution:   Mariner
%global maj 0
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:       sratom
Version:    0.6.4
Release:    3%{?dist}
Summary:    A C library for serializing LV2 plugins

License:    MIT
URL:        https://drobilla.net/software/sratom
Source0:    https://download.drobilla.net/%{name}-%{version}.tar.bz2
BuildRequires:  python3
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  sord-devel >= 0.14.0
BuildRequires:  serd-devel >= 0.30.0
BuildRequires:  lv2-devel >= 1.10.0
BuildRequires:  gcc

%description
%{name} is a new C library for serializing LV2 atoms to/from Turtle. It is 
intended to be a full serialization solution for LV2 atoms, allowing 
implementations to serialize binary atoms to strings and read them back again. 
This is particularly useful for saving plugin state, or implementing plugin 
control with network transparency.

%package devel
Summary:    Development libraries and headers for %{name}
Requires:   %{name}%{_isa} = %{version}-%{release}

%description devel
%{name} is a C library for serializing LV2 atoms to/from Turtle. It is 
intended to be a full serialization solution for LV2 atoms, allowing 
implementations to serialize binary atoms to strings and read them back again. 
This is particularly useful for saving plugin state, or implementing plugin 
control with network transparency.

This package contains the headers and development libraries for %{name}.

%prep
%setup -q 

# for packagers sake, build the tests with debug symbols
sed -i -e "s| '-ftest-coverage'\]|\
 '-ftest-coverage'\] + '%{optflags}'.split(' ')|" wscript

%build
%set_build_flags
python3 waf configure -v \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --datadir=%{_datadir} \
    --docdir=%{_pkgdocdir} \
    --test \
    --docs 
python3 waf build -v %{?_smp_mflags}

%install
DESTDIR=%{buildroot} python3 waf install
chmod +x %{buildroot}%{_libdir}/lib%{name}-0.so.*
install -pm 644 COPYING NEWS README.md %{buildroot}%{_pkgdocdir}

%check
./build/sratom_test

%files
%{_pkgdocdir}
%exclude %{_pkgdocdir}/%{name}-%{maj}/
%exclude %{_pkgdocdir}/COPYING
%license COPYING
%{_libdir}/lib%{name}-%{maj}.so.*

%files devel
%{_pkgdocdir}/%{name}-%{maj}/
%{_libdir}/lib%{name}-%{maj}.so
%{_libdir}/pkgconfig/%{name}-%{maj}.pc
%{_includedir}/%{name}-%{maj}/
%{_mandir}/man3/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.6.4-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 06 2019 Guido Aulisi <guido.aulisi@gmail.com> - 0.6.4-1
- Update to 0.6.4
- Use python3

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 0.6.2-2
- Rebuild with fixed binutils

* Mon Jul 30 2018 Guido Aulisi <guido.aulisi@gmail.com> - 0.6.2-1
- Update to 0.6.2
- Remove ldconfig scriptlets

* Sun Jul 15 2018 Guido Aulisi <guido.aulisi@gmail.com> - 0.6.0-6
- Fix FTBFS due to the move of /usr/bin/python into a separate package

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 14 2017 Guido Aulisi <guido.aulisi@gmail.com> - 0.6.0-1
- Update to 0.6.0
- Use hardened LDFLAGS
- Enable tests
- Use license macro

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Aug 20 2014 Kevin Fenzi <kevin@scrye.com> - 0.4.6-2
- Rebuild for rpm bug 1131892

* Wed Aug 20 2014 Brendan Jones <brendan.jones.it@gmail.com> 0.4.6-1
- Update to 0.4.6

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Jan 10 2014 Brendan Jones <brendan.jones.it@gmail.com> 0.4.4-1
- New upstream release

* Sun Dec 15 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.4.2-6
- Install docs to %%{_pkgdocdir} where available (#994105).

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 21 2013 Brendan Jones <brendan.jones.it@gmail.com> 0.4.2-4
- Rebuilt again

* Tue May 21 2013 Brendan Jones <brendan.jones.it@gmail.com> 0.4.2-3
- Rebuild for new sord

* Tue May 21 2013 Brendan Jones <brendan.jones.it@gmail.com> 0.4.2-2
- Rebuild for new sord

* Tue May 21 2013 Brendan Jones <brendan.jones.it@gmail.com> 0.4.2-1
- New upstream release

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat May 12 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.2.0-3
- Temporarily remove tests - http://dev.drobilla.net/ticket/832 

* Fri Apr 20 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.2.0-2
- Correct spelling and add missing build requires 

* Fri Apr 20 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.2.0-1
- Initial build 
