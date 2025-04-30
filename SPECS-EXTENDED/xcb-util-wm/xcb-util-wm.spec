Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:		xcb-util-wm
Version:	0.4.2
Release:	7%{?dist}
Summary:	Client and window-manager helper library on top of libxcb
License:	MIT
URL:		https://xcb.freedesktop.org
Source0:	https://xcb.freedesktop.org/dist/%{name}-%{version}.tar.xz
BuildRequires:	make
BuildRequires:	gcc
BuildRequires:	pkgconfig(xcb-util) >= 0.3.8
BuildRequires:	m4

%description
XCB util-wm module provides the following libraries:

  - ewmh: Both client and window-manager helpers for EWMH.
  - icccm: Both client and window-manager helpers for ICCCM.

%package	devel
Summary:	Development and header files for xcb-util-vm
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	devel
Development files for xcb-util-wm.

%prep
%setup -q

%build
%configure --with-pic --disable-static --disable-silent-rules
%make_build

%check
make check

%install
%make_install
rm %{buildroot}%{_libdir}/*.la

%ldconfig_post

%ldconfig_postun

%files
%doc README.md
%if 0%{?_licensedir:1}
%license COPYING
%else
%doc COPYING
%endif
%{_libdir}/*.so.*

%files devel
%doc NEWS
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_includedir}/xcb/*.h

%changelog
* Thu Dec 26 2024 Aninda Pradhan <v-anipradhan@microsoft.com> - 0.4.2-7
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License Verified

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Sep 07 2023 José Expósito <jexposit@redhat.com> - 0.4.2-4
- SPDX Migration

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec  1 2022 Thomas Moschny <thomas.moschny@gmx.de> - 0.4.2-1
- Update to 0.4.2.

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Tom Stellard <tstellar@redhat.com> - 0.4.1-18
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Thomas Moschny <thomas.moschny@gmx.de> - 0.4.1-13
- Use ldconfig scriptlet macros.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Dec  5 2015 Thomas Moschny <thomas.moschny@gmx.de> - 0.4.1-7
- Mark license with %%license.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Oct 22 2014 Thomas Moschny <thomas.moschny@gmx.de> - 0.4.1-5
- Include COPYING.

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 17 2014 Thomas Moschny <thomas.moschny@gmx.de> - 0.4.1-2
- Disable silent build.

* Wed Apr 16 2014 Hans de Goede <hdegoede@redhat.com> - 0.4.1-1
- Update to 0.4.1 (rhbz#1059674)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug 20 2012 Thomas Moschny <thomas.moschny@gmx.de> - 0.3.9-1
- Update to 0.3.9.

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr  5 2012 Thomas Moschny <thomas.moschny@gmx.de> - 0.3.8-2
- Specfile cleanups as suggested in the review.
- Remove unneeded BR on pkgconfig.
- Remove unneeded chrpath call.

* Mon Dec  5 2011 Thomas Moschny <thomas.moschny@gmx.de> - 0.3.8-1
- New package.
