Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           jimtcl
Version:        0.78
Release:        5%{?dist}
Summary:        A small embeddable Tcl interpreter

License:        BSD
URL:            https://jim.tcl.tk
Source0:        https://github.com/msteveb/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
Patch0:         jimtcl-fix_doc_paths.patch

BuildRequires:  gcc
BuildRequires:  asciidoc

%description
Jim is an opensource small-footprint implementation of the Tcl programming 
language. It implements a large subset of Tcl and adds new features like 
references with garbage collection, closures, built-in Object Oriented 
Programming system, Functional Programming commands, first-class arrays and 
UTF-8 support.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch 0

rm -rf sqlite3

%build
#configure is not able to locate the needed binaries, so specify it manualy
export CC=gcc
export LD=ld
export AR=ar
export RANLIB=ranlib
export STRIP=strip

%configure --full --shared --disable-option-checking
make %{?_smp_mflags}

%check
make test

%install
%make_install
rm -rf %{buildroot}/%{_datadir}/doc/%{name}
rm -rf %{buildroot}/%{_libdir}/jim/tcltest.tcl
pushd %{buildroot}/%{_libdir}/
ln -s libjim.so.* libjim.so
popd

%ldconfig_scriptlets

%files
%doc LICENSE AUTHORS README Tcl.html
%{_bindir}/jimsh
%{_libdir}/libjim.so.*

%files devel
%doc DEVELOPING README.extensions README.metakit README.namespaces README.oo README.utf-8 STYLE
%{_includedir}/*
%{_bindir}/build-jim-ext
%{_libdir}/libjim.so
%{_libdir}/pkgconfig/jimtcl.pc

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.78-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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

