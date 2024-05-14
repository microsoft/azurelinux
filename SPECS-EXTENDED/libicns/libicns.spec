Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           libicns
Version:        0.8.1
Release:        20%{?dist}
Summary:        Library for manipulating Macintosh icns files

# libicns, icns2png and icontainer2icns are under LGPLv2+
# png2icns is under GPLv2+
License:        LGPLv2+ and GPLv2+
URL:            https://icns.sourceforge.net/
Source0:        https://downloads.sourceforge.net/icns/%{name}-%{version}.tar.gz
# Fix compiling with gcc6
# Patch is already in upstream git
Patch0:         %{name}-0.8.1-gcc6.patch

BuildRequires:  gcc
BuildRequires:  libpng-devel
BuildRequires:  jasper-devel

%description
libicns is a library providing functionality for easily reading and 
writing Macintosh icns files


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        utils
Summary:        Utilities for %{name}
Requires:       %{name} = %{version}-%{release}

%description    utils
icns2png - convert Mac OS icns files to png images
png2icns - convert png images to Mac OS icns files
icontainer2icns - extract icns files from icontainers 


%prep
%setup -q
%patch 0 -p1


%build
%configure --disable-static
# disable rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build


%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%ldconfig_scriptlets


%files
%doc AUTHORS NEWS README TODO
%license COPYING COPYING.LGPL-2 COPYING.LGPL-2.1
%{_libdir}/*.so.*

%files devel
%doc src/apidocs.*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc

%files utils
%{_bindir}/*
%{_mandir}/man1/*
%doc README


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.8.1-20
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 21 2018 Andrea Musuruane <musuruan@gmail.com> - 0.8.1-15
- Added gcc dependency
- Used %%ldconfig_scriptlets

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Dec 04 2016 Andrea Musuruane <musuruan@gmail.com> - 0.8.1-10
- Fix compiling with gcc6

* Sat Dec 03 2016 Andrea Musuruane <musuruan@gmail.com> - 0.8.1-9
- Rebuilt for jasper 2.0
- Dropped obsolete Group, Buildroot, %%clean and %%defattr
- Dropped cleaning at the beginning of %%install
- Correctly marked license files

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 17 2012 Andrea Musuruane <musuruan@gmail.com> - 0.8.1-1
- Updated to new upstream 0.8.1

* Sat Feb 04 2012 Andrea Musuruane <musuruan@gmail.com> - 0.8.0-1
- Updated to new upstream 0.8.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 09 2011 Andrea Musuruane <musuruan@gmail.com> - 0.7.1-4
- Fixed FTBFS for new libpng

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.7.1-3
- Rebuild for new libpng

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Nov 01 2009 Andrea Musuruane <musuruan@gmail.com> - 0.7.1-1
- Updated to new upstream 0.7.1

* Sun Aug 23 2009 Andrea Musuruane <musuruan@gmail.com> - 0.7.0-3
- Updated to new upstream 0.7.0 that was released without bumping the version

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 13 2009 Andrea Musuruane <musuruan@gmail.com> - 0.7.0-1
- Updated to upstream 0.7.0

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 07 2009 Andrea Musuruane <musuruan@gmail.com> - 0.6.2-1
- Updated to upstream 0.6.2

* Mon Jan 05 2009 Andrea Musuruane <musuruan@gmail.com> - 0.6.1-1
- Updated to upstream 0.6.1

* Sat Dec 20 2008 Andrea Musuruane <musuruan@gmail.com> - 0.6.0-2
- Fixed Source0 URL
- Added missing 'Requires: pkgconfig' to devel package

* Sat Dec 13 2008 Andrea Musuruane <musuruan@gmail.com> - 0.6.0-1
- First release for Fedora

