# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global sovermajor 0

Name:           opencore-amr
Version:        0.1.6
Release:        9%{?dist}
Summary:        OpenCORE Adaptive Multi Rate Narrowband and Wideband speech lib
License:        Apache-2.0
URL:            http://sourceforge.net/projects/opencore-amr/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:         opencore-amr-0.1.3-fix_pc.patch

BuildRequires:  gcc-c++
BuildRequires:  make

%description
Library of OpenCORE Framework implementation of Adaptive Multi Rate Narrowband
and Wideband speech codec.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1
mv opencore/README opencore/README.opencore


%build
%configure --disable-static
%make_build


%install
%make_install
rm $RPM_BUILD_ROOT%{_libdir}/libopencore-amr??.la


%ldconfig_scriptlets


%files
%doc README opencore/ChangeLog opencore/NOTICE opencore/README.opencore
%license LICENSE
%{_libdir}/libopencore-amr??.so.%{sovermajor}{,.*}

%files devel
%{_includedir}/opencore-amr??
%{_libdir}/libopencore-amr??.so
%{_libdir}/pkgconfig/opencore-amr??.pc

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jan 24 2023 Neal Gompa <ngompa@fedoraproject.org> - 0.1.6-3
- Adapt for Fedora

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Wed Aug 03 2022 Leigh Scott <leigh123linux@gmail.com> - 0.1.6-1
- Update to 0.1.6

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.1.5-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.1.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.1.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.1.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Mar 11 2020 Leigh Scott <leigh123linux@gmail.com> - 0.1.5-10
- Rebuilt for i686

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.1.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Dec 11 2018 Nicolas Chauvet <kwizart@gmail.com> - 0.1.5-6
- Spec file clean-up

* Sun Aug 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.1.5-5
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 20 2017 Leigh Scott <leigh123linux@googlemail.com> - 0.1.5-1
- Update to 0.1.5

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 0.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.1.3-3
- Mass rebuilt for Fedora 19 Features

* Fri May 18 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.1.3-2
- Fix pkgconfig include

* Sun May 13 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.1.3-1
- Update to 0.1.3

* Fri Mar 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.1.2-3
- Rebuilt for c++ ABI breakage

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct  4 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1.2-1
- New upstream release 0.1.2

* Thu Jul 30 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1.1-1
- First version of the RPM Fusion package
