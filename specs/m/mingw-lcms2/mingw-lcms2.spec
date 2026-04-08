# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

%global mingw_pkg_name lcms2
#global prerelease rc3

Name:           mingw-%{mingw_pkg_name}
Version:        2.14
#Release:        0.2.%{prerelease}%{?dist}
Release:        8%{?dist}
Summary:        MinGW Color Management Engine
License:        MIT
URL:            http://www.littlecms.com/
#Source0:        http://www.littlecms.com/%{mingw_pkg_name}-%{version}%{prerelease}.tar.gz
Source0:        https://sourceforge.net/projects/lcms/files/lcms/%{version}/%{mingw_pkg_name}-%{version}.tar.gz

BuildRequires: make
BuildRequires:  mingw32-filesystem
BuildRequires:  mingw64-filesystem
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw32-libjpeg
BuildRequires:  mingw64-libjpeg
BuildRequires:  mingw32-libtiff
BuildRequires:  mingw64-libtiff
BuildRequires:  mingw32-zlib
BuildRequires:  mingw64-zlib
BuildArch:      noarch

%description
LittleCMS intends to be a small-footprint, speed optimized color management
engine in open source form. LCMS2 is the current version of LCMS, and can be
parallel installed with the original (deprecated) lcms.

# Mingw32
%package -n mingw32-%{mingw_pkg_name}
Summary:                %{summary}

%description -n mingw32-%{mingw_pkg_name}
LittleCMS intends to be a small-footprint, speed optimized color management
engine in open source form. LCMS2 is the current version of LCMS, and can be
parallel installed with the original (deprecated) lcms.

%package -n mingw32-%{mingw_pkg_name}-static
Summary:  Static libraries for mingw32-%{mingw_pkg_name} development
Requires: mingw32-%{mingw_pkg_name} = %{version}-%{release}

%description -n mingw32-%{mingw_pkg_name}-static
The mingw32-%{mingw_pkg_name}-static package contains static library for
mingw32-%{mingw_pkg_name} development.

# Mingw64
%package -n mingw64-%{mingw_pkg_name}
Summary:                %{summary}

%description -n mingw64-%{mingw_pkg_name}
LittleCMS intends to be a small-footprint, speed optimized color management
engine in open source form. LCMS2 is the current version of LCMS, and can be
parallel installed with the original (deprecated) lcms.

%package -n mingw64-%{mingw_pkg_name}-static
Summary:  Static libraries for mingw64-%{mingw_pkg_name} development
Requires: mingw64-%{mingw_pkg_name} = %{version}-%{release}

%description -n mingw64-%{mingw_pkg_name}-static
The mingw64-%{mingw_pkg_name}-static package contains static library for
mingw64-%{mingw_pkg_name} development.

%{?mingw_debug_package}

%prep
#setup -q -n %{mingw_pkg_name}-%{version}%{prerelease}
%setup -q -n %{mingw_pkg_name}-%{version}
iconv -f ISO-8859-1 -t UTF-8 AUTHORS > AUTHORS.x
mv -f AUTHORS.x AUTHORS

%build
%mingw_configure --enable-static --program-suffix=2

%mingw_make %{?_smp_mflags}

%install
%mingw_make install DESTDIR=${RPM_BUILD_ROOT} INSTALL="install -p"
find ${RPM_BUILD_ROOT} -type f -name "*.la" -exec rm -f {} ';'
find ${RPM_BUILD_ROOT} -type f -name "*.exe" -exec rm -f {} ';'
install -D -m 644 include/lcms2.h $RPM_BUILD_ROOT%{mingw32_includedir}/lcms2.h
install -D -m 644 include/lcms2.h $RPM_BUILD_ROOT%{mingw64_includedir}/lcms2.h
install -D -m 644 include/lcms2_plugin.h $RPM_BUILD_ROOT%{mingw32_includedir}/lcms2_plugin.h
install -D -m 644 include/lcms2_plugin.h $RPM_BUILD_ROOT%{mingw64_includedir}/lcms2_plugin.h
rm -rf ${RPM_BUILD_ROOT}/%{mingw32_mandir}
rm -rf ${RPM_BUILD_ROOT}/%{mingw64_mandir}


%files -n mingw32-%{mingw_pkg_name}
%doc AUTHORS COPYING
%{mingw32_includedir}/*
%{mingw32_libdir}/liblcms2.dll.a
%{mingw32_bindir}/liblcms2-2.dll
%{mingw32_libdir}/pkgconfig/%{mingw_pkg_name}.pc

%files -n mingw32-%{mingw_pkg_name}-static
%{mingw32_libdir}/liblcms2.a

%files -n mingw64-%{mingw_pkg_name}
%doc AUTHORS COPYING
%{mingw64_includedir}/*
%{mingw64_libdir}/liblcms2.dll.a
%{mingw64_bindir}/liblcms2-2.dll
%{mingw64_libdir}/pkgconfig/%{mingw_pkg_name}.pc

%files -n mingw64-%{mingw_pkg_name}-static
%{mingw64_libdir}/liblcms2.a

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.14-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 05 2023 Orion Poplawski <orion@nwra.com> - 2.14-1
- Update to 2.14

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 2.12-4
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Feb 07 2021 Thomas Sailer <t.sailer@alumni.ethz.ch> - 2.12-1
- update to 2.12

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jun 17 2020 Thomas Sailer <t.sailer@alumni.ethz.ch> - 2.11-1
- update to 2.11

* Sat Jun 06 2020 Thomas Sailer <t.sailer@alumni.ethz.ch> - 2.10-2
- update to re-released 2.10

* Sun May 31 2020 Thomas Sailer <t.sailer@alumni.ethz.ch> - 2.10-1
- update to 2.10

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 06 2017 Thomas Sailer <t.sailer@alumni.ethz.ch> - 2.9-1
- update to 2.9

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Aug 16 2016 Thomas Sailer <t.sailer@alumni.ethz.ch> - 2.8-2
- apply fix for #1367359

* Mon Aug 08 2016 Thomas Sailer <t.sailer@alumni.ethz.ch> - 2.8-1
- update to 2.8

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May  4 2015 Thomas Sailer <t.sailer@alumni.ethz.ch> - 2.7-1
- update to 2.7

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-0.2.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar  6 2014 Thomas Sailer <t.sailer@alumni.ethz.ch> - 2.6-0.1.rc3
- update to 2.6rc3

* Tue Sep  3 2013 Thomas Sailer <t.sailer@alumni.ethz.ch> - 2.5-1
- update to 2.5

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 20 2012 Thomas Sailer <t.sailer@alumni.ethz.ch> - 2.4-1
- update to 2.4
- fix according to Greg Hellings' reviewer comments

* Thu Aug 23 2012 Thomas Sailer <t.sailer@alumni.ethz.ch> - 2.3-1
- create from native package

