%bcond_without tests

Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           jimtcl
Version:        0.83
Release:        3%{?dist}
Summary:        A small embeddable Tcl interpreter

License:        BSD-2-Clause-Views
URL:            http://jim.tcl.tk
Source:         https://github.com/msteveb/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
# readline expects applications to include stdio.h, jimtcl was not
Patch:          https://github.com/msteveb/jimtcl/commit/35e0e1f9b1f018666e5170a35366c5fc3b97309c.patch#/jimtcl-stdio-for-readline.diff

BuildRequires:  gcc-c++
BuildRequires:  asciidoc
BuildRequires:  make
# Extension dependencies
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(zlib)
%if %{with tests}
BuildRequires:  hostname
%endif

%global _description %{expand:
Jim is an opensource small-footprint implementation of the Tcl programming
language. It implements a large subset of Tcl and adds new features like 
references with garbage collection, closures, built-in Object Oriented 
Programming system, Functional Programming commands, first-class arrays and 
UTF-8 support.}

%description %{_description}


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel %{_description}

The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup
rm -rf sqlite3

%build
#configure is not able to locate the needed binaries, so specify it manualy
# export CC=gcc
# export LD=ld
export AR=ar
export RANLIB=ranlib
export STRIP=strip

# compile extensions that are disabled by default
# as modules
# see ./configure --extinfo for list
%configure --shared --disable-option-checking \
  --allextmod \
%ifarch s390x # zlib test fails on s390x
  --without-ext=zlib \
%endif
  --docdir=%{_datadir}/doc/%{name}
%make_build


%install
%make_install INSTALL_DOCS=nodocs
rm %{buildroot}/%{_libdir}/jim/README.extensions


%if %{with tests}
%check
# remove tests that require network access
rm tests/ssl.test
make test
%endif


%files
%license LICENSE
%doc AUTHORS README README.*
%doc EastAsianWidth.txt
%doc %{_datadir}/doc/%{name}/Tcl.html
%{_bindir}/jimdb
%{_bindir}/jimsh
%dir %{_libdir}/jim
%{_libdir}/jim/*.tcl
%{_libdir}/jim/*.so
%{_libdir}/libjim.so.*


%files devel
%doc CONTRIBUTING.md STYLE
%{_includedir}/*
%{_bindir}/build-jim-ext
%{_libdir}/libjim.so
%{_libdir}/pkgconfig/jimtcl.pc

%changelog
* Mon May 12 2025 Archana Shettigar <v-shettigara@microsoft.com> - 0.83-3
- Initial Azure Linux import from Fedora 42 (license: MIT).
- License verified

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.83-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Sep 20 2024 Michel Lind <salimma@fedoraproject.org> - 0.83-1
- Update to version 0.83; Fixes: RHBZ#2309077

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.82-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.82-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.82-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.82-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Feb 28 2023 Michel Alexandre Salim <salimma@fedoraproject.org> - 0.82-2
- Properly disable zlib extension on s390x
- move README files meant for programming with jimtcl to main package

* Tue Feb 28 2023 Michel Alexandre Salim <salimma@fedoraproject.org> - 0.82-1
- Update to 0.82
- enable more extensions
- update license to use SPDX

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.81-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.81-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.81-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 07 2022 Michel Alexandre Salim <salimma@fedoraproject.org> - 0.81-2
- Disable zlib module on s390x (tests fail)

* Fri Jan 07 2022 Michel Alexandre Salim <salimma@fedoraproject.org> - 0.81-1
- Update to 0.81
- Ship extensions that are disabled by default as modules
- Opt in to rpmautospec

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.78-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.78-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Aug 06 2020 Jeff Law <law@redhat.com> - 0.78-6
- Depend on g++

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.78-6
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.78-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.78-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.78-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.78-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jul 18 2018 Lubomir Rintel <lkundrak@v3.sk> - 0.78-1
- new upstream release 0.78

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.77-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.77-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.77-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.77-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.77-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Sep 22 2016 Markus Mayer <lotharlutz@gmx.de> - 0.77-1
- new upstream release 0.77

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.76-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.76-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.76-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Feb 01 2015 Markus Mayer <lotharlutz@gmx.de> - 0.76-1
- new upstream release 0.76

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.75-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.75-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 01 2014 Markus Mayer <lotharlutz@gmx.de> - 0.75-1
- new upstream release 0.75
- rebase jimtcl-fix_doc_paths.patch
- drop utf-8 conversion in prep (upstream uses utf now)

* Sat Sep 07 2013 Markus Mayer <lotharlutz@gmx.de> - 0.74-1
- new upstream release 0.74
- drop patches merges upstream
- rebase jimtcl-fix_doc_paths.patch

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.73-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 06 2013 Markus Mayer <lotharlutz@gmx.de> - 0.73-4
- Change soname to libjim.0.73 (as suggested by upstream)

* Sun May 05 2013 Markus Mayer <lotharlutz@gmx.de> - 0.73-3
- fix source url
- add symlink to library to devel package

* Sun May 05 2013 Markus Mayer <lotharlutz@gmx.de> - 0.73-2
- fix source url
- convert LICENSE and AUTHORS to UTF-8
- remove not needed 'defattr(-,root,root,-)' and 'rm -rf $RPM_BUILD_ROOT'
- add add soname to lib(jimtcl-add_soname.patch)
- add README.* files to doc
- add STYLE file to doc

* Sun May 05 2013 Markus Mayer <lotharlutz@gmx.de> - 0.73-1
- inital prm release
