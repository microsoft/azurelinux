Vendor:         Microsoft Corporation
Distribution:   Mariner
%undefine __cmake_in_source_build

Name:          uchardet
Version:       0.0.6
Release:       17%{?dist}
Summary:       An encoding detector library ported from Mozilla

License:       MPLv1.1 or GPLv2+ or LGPLv2+
URL:           https://www.freedesktop.org/wiki/Software/%{name}
Source0:       https://www.freedesktop.org/software/%{name}/releases/%{name}-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake

%description
Uchardet is a C language binding of the original C++ implementation of the
universal charset detection library by Mozilla. Uchardet is an encoding
detector library, which takes a sequence of bytes in an unknown character
encoding without any additional information, and attempts to determine the
encoding of the text.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains headers and shared libraries
for developing tools for uchardet.

%prep
%autosetup

%build
%cmake \
  -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
  -DBUILD_STATIC=OFF
%cmake_build

%install
%cmake_install

%ldconfig_scriptlets

%check
pushd %{_vpath_builddir}
  ctest -VV \
  %ifarch %{ix86}
    || :
  %else
    ;
  %endif
popd

%files
%license COPYING
%doc AUTHORS
%{_bindir}/%{name}
%{_libdir}/lib%{name}.so.*
%{_mandir}/man1/%{name}.1*

%files devel
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Mon Apr 03 2023 Bala <balakumaran.kannan@microsoft.com> - 0.0.6-17
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- License verified

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed May 19 2021 Akira TAGOH <tagoh@redhat.com> - 0.0.6-13
- Correct License field.
  See COPYING file for more details.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.0.6-5
- Switch to %%ldconfig_scriptlets

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 22 2016 Ilya Gradina <ilya.gradina@gmail.com> - 0.0.6-1
- update version to 0.0.6
- changed upstream url

* Thu Jul 07 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.0.5-4
- Rebuild for f23 to fix i686

* Fri Feb 12 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.0.5-3
- Fixup summary in devel subpkg

* Mon Feb 08 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.0.5-2
- Fix building on i686 properly

* Sat Feb 6  2016 Ilya Gradina <ilya.gradina@gmail.com> - 0.0.5-1
- update version to 0.0.5

* Fri Nov 20 2015 Ilya Gradina <ilya.gradina@gmail.com> - 0.0.3-1
- update version to 0.0.3
- add tests

* Thu Oct  1 2015 Ilya Gradina <ilya.gradina@gmail.com> - 0.0.1-5
- remove macros srcname and sum

* Mon Sep 21 2015 Ilya Gradina <ilya.gradina@gmail.com> - 0.0.1-4
- fix enable debug packages
- fix add flag verbose for make
- fix change in build
- fix remove in libs from files
- fix add change for libs in post/postun
- fix version on 0.0.1 from git
- added macros

* Mon Sep 21 2015 Ilya Gradina <ilya.gradina@gmail.com> - 0.0.0-3
- fix description and summary for libs and libs-devel

* Mon Sep 21 2015 Ilya Gradina <ilya.gradina@gmail.com> - 0.0.0-2
- fix version on 0.0.0
- fix license path
- remove static lib
- fix description
- fix number packages

* Mon Sep 21 2015 Ilya Gradina <ilya.gradina@gmail.com> - 0.0.0-1
- Initial package
