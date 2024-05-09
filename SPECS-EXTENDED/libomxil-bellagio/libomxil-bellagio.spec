Summary:        OpenMAX Integration Layer
Name:           libomxil-bellagio
Version:        0.9.3
Release:        29%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://omxil.sourceforge.net
Source0:        https://downloads.sourceforge.net/omxil/%{name}-%{version}.tar.gz
#https://sourceforge.net/tracker/?func=detail&aid=3477869&group_id=160680&atid=816817
Patch0:         libomxil-bellagio-0.9.3-fix_Werror.patch
Patch1:         libomxil-bellagio-0.9.3-unused.patch
#https://sourceforge.net/tracker/?func=detail&aid=3477871&group_id=160680&atid=816817
Patch2:         libomxil-bellagio-0.9.3-nodoc.patch
Patch3:         https://git.buildroot.net/buildroot/plain/package/multimedia/bellagio/bellagio-0.9.3-dynamicloader-linking.patch
Patch4:         https://git.buildroot.net/buildroot/plain/package/multimedia/bellagio/bellagio-0.9.3-parallel-build.patch
Patch5:         https://git.buildroot.net/buildroot/plain/package/multimedia/bellagio/bellagio-0.9.3-segfault-on-removeFromWaitResource.patch
Patch6:         omxil_version.patch
Patch7:         libomxil-bellagio-0.9.3-memcpy.patch
Patch8:         libomxil-bellagio-0.9.3-valgrind_register.patch
%define         _legacy_common_support 1
BuildRequires:  doxygen
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
The OpenMAX IL API defines a standardized media component interface to
enable developers and platform providers to integrate and communicate
with multimedia codecs implemented in hardware or software.

The libomxil shared library implements the OpenMAX IL Core functionalities.
Three dynamically loadable components are also included: OMX alsa sink
component, OMX mp3,aac,ogg decoder component and OMX volume control component.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        test
Summary:        Test cases for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    test
The %{name}-test package contains binaries for testing %{name}.

%prep
%setup -q
%patch 0 -p1 -b .fix_werror
%patch 1 -p1 -b .unused
%patch 2 -p1 -b .nodoc
%patch 3 -p1 -b .dynl
%patch 4 -p1 -b .pb
%patch 5 -p1 -b .sf
%patch 6  -b .orig
%patch 7 -p1 -b .memcpy
%patch 8  -b .register
sed -i -e 's/ -Werror//' configure.ac
autoreconf -vif


%build
%configure --disable-static

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

#Race condition with the library creation
make %{?_smp_mflags} || make %{?_smp_mflags}

#Build the tests files so they can be installed later
ln -sf src bellagio
make check LDFLAGS="-L$PWD/src/.libs" \
    CFLAGS="%{optflags} -I$PWD/include -I$PWD"


%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print


#Manually install test binaries
mkdir -p %{buildroot}%{_bindir}
for f in audio_effects/.libs/{omxaudiomixertest,omxvolcontroltest} resource_manager/.libs/{omxprioritytest,omxrmtest} ; do
  install -pm 0755 test/components/${f} %{buildroot}%{_bindir}
done

#Avoid docdir
rm -rf %{buildroot}%{_docdir}/%{name}


%ldconfig_scriptlets


%files
%doc AUTHORS ChangeLog NEWS README TODO
%license COPYING
%{_bindir}/omxregister-bellagio
%{_libdir}/*.so.*
%dir %{_libdir}/bellagio
%{_libdir}/bellagio/*.so*
%dir %{_libdir}/omxloaders
%{_libdir}/omxloaders/*.so*
%{_mandir}/man1/omxregister-bellagio.1.*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libomxil-bellagio.pc

%files test
%{_bindir}/omxaudiomixertest
%{_bindir}/omxprioritytest
%{_bindir}/omxrmtest
%{_bindir}/omxvolcontroltest

%changelog
* Thu Jan 05 2023 Suresh Thelkar <sthelkar@microsoft.com> - 0.9.3-29
- Initial CBL-Mariner import from Fedora 36 (license: MIT)
- License verified

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Feb 28 2020 Nicolas Chauvet <kwizart@gmail.com> - 0.9.3-24
- Drop Werror on configure.ac

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 20 2018 Nicolas Chauvet <kwizart@gmail.com> - 0.9.3-20
- Fix memcpy boundary error with gcc8
- Add patch by Emil Velikov to fix a valgrind issue - rhbz#1119235
- Fix dates in changelog

* Tue Jul 17 2018 Nicolas Chauvet <kwizart@gmail.com> - 0.9.3-19
- Add missng cc

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Nicolas Chauvet <kwizart@gmail.com> - 0.9.3-17
- Rebuilt

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jul 31 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.9.3-8
- Add back gst-omx
- Adjust docdir for %%fedora >= 20

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 16 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.9.3-6
- Fix registration error patch

* Sun Dec 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.9.3-5
- Fix registration error rhbz#882743
- Fix missing symbol rhbz#885402 - patch from qais.yousef@imgtec.com
- Fix paralle build - patch from qais.yousef@imgtec.com
- Fix segfault - patch from qais.yousef@imgtec.com

* Sat Sep 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.9.3-4
- Fix unused variable

* Tue Jul 24 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.9.3-3
- Avoid running autoreconf
- Avoid running make check
- Fix manual building of test binaries

* Mon Apr 23 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.9.3-2
- Fix build with -Werror - patch from Niels de Vos
- Convert nodoc fix to a patch
- Add BR doxygen
- Enable make check and create a -test subpackage

* Wed Jan 18 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.9.3-1
- Fedora spec file

* Wed Sep 17 2008 Giulio Urlini
- added jpeg encoder/decoder

* Mon Jul 07 2008 Giulio Urlini
- added clock source, video source, camera, frame buffer writer

* Thu Mar 06 2008 Marc-Andre Lureau
- copy&pasted some good practices from some other .spec.in
- changed components directory
- remove unnecessary plugins .la and .a files
- untested

* Wed Feb 27 2008 Giulio Urlini
- changed the library list.

* Fri Oct 19 2007 Giulio Urlini
- removed fbdev from file list. It is experimental,
  and not installed on any platform

* Mon Oct 01 2007 Giulio Urlini
- Minor update and name change of this file

* Mon Jun 04 2007 Giulio Urlini
- Bellagio 0.3.2 release

* Tue May 22 2007 Giulio Urlini
- Bellagio 0.3.1 release

* Fri Apr 06 2007 Giulio Urlini
- Bellagio 0.3 release

* Fri Feb 24 2006 David Siorpaes
- Fixed some minor issues in build process

* Mon Feb 6 2006 Giulio Urlini
- First build attempt
