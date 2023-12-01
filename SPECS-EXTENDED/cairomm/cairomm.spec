Summary:        C++ API for the cairo graphics library
Name:           cairomm
Version:        1.12.0
Release:        15%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.cairographics.org
Source:         http://www.cairographics.org/releases/%{name}-%{version}.tar.gz
%global apiver 1.0
%global cairo_version 1.10.0
%global libsigc_version 2.5.1
BuildRequires:  cairo-devel >= %{cairo_version}
BuildRequires:  gcc-c++
BuildRequires:  libsigc++20-devel >= %{libsigc_version}
BuildRequires:  perl-interpreter
BuildRequires:  pkgconfig
BuildRequires:  perl(Getopt::Long)
Requires:       cairo%{?_isa} >= %{cairo_version}
Requires:       libsigc++20%{?_isa} >= %{libsigc_version}

%description
Cairomm is the C++ API for the cairo graphics library. It offers all the power
of cairo with an interface familiar to C++ developers, including use of the
Standard Template Library where it makes sense.

%package        devel
Summary:        Headers for developing programs that will use %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Cairomm is the C++ API for the cairo graphics library. It offers all the power
of cairo with an interface familiar to C++ developers, including use of the
Standard Template Library where it makes sense.

This package contains the libraries and header files needed for
developing %{name} applications.

%package        doc
Summary:        Developer's documentation for the cairomm library
Requires:       %{name} = %{version}-%{release}
Requires:       libsigc++20-doc
BuildArch:      noarch

%description      doc
This package contains developer's documentation for the cairomm
library. Cairomm is the C++ API for the cairo graphics library.

The documentation can be viewed either through the devhelp
documentation browser or through a web browser.

If using a web browser the documentation is installed in the gtk-doc
hierarchy and can be found at %{_docdir}/cairomm-1.0

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

%ldconfig_scriptlets

%files
%license COPYING
%doc AUTHORS README NEWS
%{_libdir}/lib*.so.*

%files devel
%doc ChangeLog
%{_includedir}/%{name}-%{apiver}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_libdir}/%{name}-%{apiver}

%files doc
%doc %{_docdir}/%{name}-%{apiver}/
%doc %{_datadir}/devhelp/

%changelog
* Wed Oct 26 2022 Muhammad Falak <mwani@microsoft.com> - 1.12.0-15
- License verified

* Wed Oct 06 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.12.0-14
- Bringing back the dependency on 'cairo'.

* Thu Jun 17 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.12.0-13
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Use UI-cairo instead of cairo to avoid runtime conflicts

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Feb 04 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.12.0-7
- Switch to %%ldconfig_scriptlets

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Sep 22 2015 Kalev Lember <klember@redhat.com> - 1.12.0-1
- Update to 1.12.0
- Drop manual requires that are automatically handled by pkgconfig dep gen
- Use license macro for COPYING
- Tighten -devel subpackage deps with the _isa macro
- Use make_install macro

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.10.0-11
- Rebuilt for GCC 5 C++11 ABI change

* Sat Mar 07 2015 Kalev Lember <kalevlember@gmail.com> - 1.10.0-10
- Rebuilt for gcc5 ABI change

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-4
- Rebuilt for c++ ABI breakage

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.10.0-2
- Rebuild for new libpng

* Fri Jul 29 2011 Kalev Lember <kalevlember@gmail.com> - 1.10.0-1
- Update to 1.10.0
- Have the -doc subpackage depend on the base package
- Modernize the spec file
- Really own /usr/share/devhelp directory

* Mon Feb 21 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 1.9.8-2
- fix documentation location
- co-own /usr/share/devhelp

* Mon Feb 14 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 1.9.8-1
- upstream 1.9.8
- fix issues with f15/rawhide (RHBZ #676878)
- drop gtk-doc dependency (RHBZ #604169)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 14 2010 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.9.1-1
- New upstream release
- Removed html docs from -devel package
- Seperated requires into one per line
- Fixed devhelp docs

* Tue Nov 17 2009 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.8.4-1
- New upstream release
- Added cairommconfig.h file
- Added doc subpackage

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.8.0-1
- Update to 1.8.0
- Added libsigc++20-devel dependency

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Aug 29 2008 Denis Leroy <denis@poolshark.org> - 1.6.2-1
- Update to upstream 1.6.2
- atsui patch upstreamed

* Sun Mar 23 2008 Denis Leroy <denis@poolshark.org> - 1.5.0-1
- Update to 1.5.0
- Added patch from Mamoru Tasaka to fix font type enum (#438600)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.4.4-2
- Autorebuild for GCC 4.3

* Fri Aug 17 2007 Denis Leroy <denis@poolshark.org> - 1.4.4-1
- Update to upstream version 1.4.4
- Fixed License tag

* Fri Jul 20 2007 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.4.2-1
- New upstream release
- Changed install to preserve timestamps
- Removed mv of docs/reference and include files directly

* Wed Jan 17 2007 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.2.4-1
- New release

* Sat Oct 14 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.2.2-1
- New upstream release

* Sun Aug 27 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.2.0-4
- Bumped release for make tag

* Sun Aug 27 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.2.0-3
- Bumped release for mass rebuild

* Sun Aug 20 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.2.0-2
- Bumped release for make tag

* Sun Aug 20 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.2.0-1
- New upstream release
- Updated summary and description

* Thu Aug  3 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 1.1.10-1
- First release for cairo 1.2
- Adjusted cairo dependencies for new version
- Docs were in html, moved to reference/html

* Sun Apr  9 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.6.0-1
- New upstream version should fix the upstream issues like AUTHORS and README
- Added pkgconfig to cairomm BuildRequires and cairomm-devel Requires
- Replaced makeinstall
- Fixed devel package description
- Modified includedir syntax
- docs included via the mv in install and in the devel files as html dir

* Sun Mar  5 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.5.0-10
- Removed duplicate Group tag in devel
- Disabled docs till they're fixed upstream 

* Sun Mar  5 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.5.0-9
- Removed requires since BuildRequires is present
- Cleaned up Source tag

* Fri Feb 24 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.5.0-7
- Fixed URL and SOURCE tags
- Fixed header include directory

* Fri Feb 24 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.5.0-6
- Fixed URL tag

* Wed Feb 22 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.5.0-5
- Remove epoch 'leftovers'

* Wed Feb 22 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.5.0-4
- Cleanup for FE

* Wed Feb 22 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.5.0-3
- Added pre-release alphatag

* Wed Feb 22 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.5.0-2
- Updated to current cairomm CVS
- Added documentation to devel package

* Fri Feb 03 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.5.0-1
- Updated to current cairomm CVS

* Fri Jan 27 2006 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0.4.0-1
- Initial creation from papyrus.spec.in
