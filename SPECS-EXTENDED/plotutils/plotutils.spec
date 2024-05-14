Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:      plotutils
Version:   2.6
Release:   25%{?dist}
Summary:   GNU vector and raster graphics utilities and libraries

# libxmi is GPLv2+
# rest is GPLv3+
License:   GPLv2+ and GPLv3+
URL:       https://www.gnu.org/software/plotutils/
Source0:   ftp://ftp.gnu.org/gnu/plotutils/plotutils-%{version}.tar.gz
Patch0:    plotutils-2.6-png15.patch
Patch1:    plotutils-aarch64.patch
Patch2:    plotutils-werror-format-security.patch

BuildRequires:   gcc-c++
BuildRequires:   make
BuildRequires:   flex
BuildRequires:   libpng-devel
BuildRequires:   xorg-x11-proto-devel
BuildRequires:   libX11-devel
BuildRequires:   libXaw-devel
BuildRequires:   libXt-devel
BuildRequires:   libXext-devel
BuildRequires:   byacc

%description
The GNU plotutils package contains software for both programmers and
technical users. Its centerpiece is libplot, a powerful C/C++ function
library for exporting 2-D vector graphics in many file formats, both
vector and raster. It can also do vector graphics animations. Besides
libplot, the package contains command-line programs for plotting
scientific data. Many of them use libplot to export graphics


%package devel
Summary:     Headers for developing programs that will use %{name}
Requires:    %{name} = %{version}-%{release}


%description devel
This package contains the header files needed for developing %{name}
applications


%prep
%setup -q
%patch 0 -p1 -b .png15
%patch 1 -p1 -b .aarch64
%patch 2 -p1 -b .format-security

%build
%configure --disable-static --enable-libplotter --enable-libxmi --enable-ps-fonts-in-pcl

# fix rpath handling
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
rm -rf docs-to-include
make install DESTDIR=$RPM_BUILD_ROOT
mkdir docs-to-include
mv ${RPM_BUILD_ROOT}%{_datadir}/ode docs-to-include
mv ${RPM_BUILD_ROOT}%{_datadir}/pic2plot docs-to-include
mv ${RPM_BUILD_ROOT}%{_datadir}/libplot docs-to-include
mv ${RPM_BUILD_ROOT}%{_datadir}/tek2plot docs-to-include
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%files
%doc AUTHORS COMPAT COPYING NEWS THANKS README PROBLEMS KNOWN_BUGS
%doc docs-to-include/*
%{_bindir}/graph
%{_bindir}/ode
%{_bindir}/double
%{_bindir}/plot
%{_bindir}/pic2plot
%{_bindir}/plotfont
%{_bindir}/spline
%{_bindir}/tek2plot
%{_bindir}/hersheydemo
%{_libdir}/*.so.*
%{_mandir}/man1/*
%{_infodir}/*.info*


%files devel
%doc TODO
%{_includedir}/*.h
%{_libdir}/*.so


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.6-25
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 19 2018 Michael Simacek <msimacek@redhat.com> - 2.6-20
- Add BR on gcc-c++ and make
- Remove deprecated Group tag

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.6-13
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Dec 04 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.6-10
- Fix FTBFS when "-Werror=format-security" is used

* Tue Nov 26 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.6-9
- Apply aarch64 support patch (#926356)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 19 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.6-6
- Fix license tag (upstream relicensed in version 2.5.1)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 22 2012 Tom Callaway <spot@fedoraproject.org> - 2.6-4
- fix build against libpng15

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 2.6-2
- Rebuild for new libpng

* Wed Mar  2 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.6-1
- Update to 2.6

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.5-5
- Autorebuild for GCC 4.3

* Mon Aug 20 2007 Denis Leroy <denis@poolshark.org> - 2.5-4
- License tag update

* Mon Aug 28 2006 Denis Leroy <denis@poolshark.org> - 2.5-3
- FE6 Rebuild

* Thu Aug 10 2006 Denis Leroy <denis@poolshark.org> - 2.5-2
- Some reformatting, added ldconfig Req

* Wed Aug  9 2006 Denis Leroy <denis@poolshark.org> - 2.5-1
- Initial version
