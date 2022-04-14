Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           gavl
Version:        1.4.0
Release:        17%{?dist}
Summary:        A library for handling uncompressed audio and video data

License:        GPLv3+
URL:            http://gmerlin.sourceforge.net/
Source0:        http://downloads.sourceforge.net/gmerlin/gavl-%{version}.tar.gz
Patch1:         gavl-1.1.1-system_libgdither.patch

BuildRequires:  libtool

BuildRequires:  doxygen

BuildRequires:  libpng-devel >= 1.0.8
BuildRequires:  libgdither-devel
# Gavl use an internal tweaked libsamplerate version
# ufortunately the libsamplerate doesn't want a patch 
# that will break ABI
#BuildRequires: libsamplerate-devel



%description
Gavl is a library for handling and converting uncompressed audio and
video data. It provides datatypes for audio/video formats and standardized
structures to store the data. It supports converting between all formats.
Some conversion functions are available in multiple versions (MMX...),
which are selected by compile time configuration, CPU autodetection and
user options.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch1 -p1 -b .gdither

#Disable buildtime cpu detection
sed -i -i 's/LQT_TRY_CFLAGS/dnl LQT_TRY_CFLAGS/g' configure.ac
sed -i -i 's/LQT_OPT_CFLAGS/dnl LQT_OPT_CFLAGS/g' configure.ac

#Regenerate build tool
sh autogen.sh



%build
%configure \
  --disable-static \
  --disable-cpu-clip \
  --enable-libgdither


make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Prevent timestamps build difference
touch -r include/gavl/gavl.h $RPM_BUILD_ROOT%{_includedir}/gavl/gavl_version.h



%ldconfig_scriptlets


%files
%doc AUTHORS COPYING README TODO
%exclude %{_docdir}/gavl/apiref
%{_libdir}/*.so.*

%files devel
%doc %{_docdir}/gavl/apiref/
%{_includedir}/gavl/
%{_libdir}/*.so
%{_libdir}/pkgconfig/gavl.pc


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4.0-17
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Oct 07 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.4.0-4
- Fix apiref bundled as %%doc in main - rhbz#1014820

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Sep 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.4.0-1
- Update to 1.4.0

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Mar 26 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.2.0-1
- update to 1.2.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat May 01 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.1.2-1
- Update to 1.1.2

* Tue Oct 27 2009 kwizart < kwizart at gmail.com > - 1.1.1-1
- Update to 1.1.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 24 2009 kwizart < kwizart at gmail.com > - 1.1.0-1
- Update to 1.1.0
- Disable buildtime CPU detection.

* Tue Jul 29 2008 kwizart < kwizart at gmail.com > - 1.0.1-1
- Update to 1.0.1

* Tue Jul 22 2008 kwizart < kwizart at gmail.com > - 1.0.0-2
- Add --enable-libgdither for system libgdither
- Add --enable-debug to disable LQT_OPT_CFLAGS
- Add -DHAVE_GAVLCONFIG_H to include gavlconfig.h when needed

* Mon May 19 2008 kwizart < kwizart at gmail.com > - 1.0.0-1
- Update to 1.0.0 api stable

* Mon May 19 2008 kwizart < kwizart at gmail.com > - 0.2.7-4
- Initial package for Fedora
