# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           frei0r-plugins
Version:        2.4.0
Release:        1%{?dist}
Summary:        Frei0r - a minimalist plugin API for video effects

# Automatically converted from old format: GPLv2+ - review is highly recommended.
License:        GPL-2.0-or-later
URL:            https://frei0r.dyne.org/
Source0:        https://github.com/dyne/frei0r/archive/v%{version}/frei0r-plugins-%{version}.tar.gz


Buildrequires:  cmake

BuildRequires:  gcc-c++
BuildRequires:  gavl-devel >= 0.2.3
BuildRequires:  opencv-devel >= 1.0.0
BuildRequires:  cairo-devel >= 1.0.0
     

%description
It is a minimalist plugin API for video sources and filters. The behavior of
the effects can be controlled from the host by simple parameters. The intent is
to solve the recurring re-implementation or adaptation issue of standard effect

%package	opencv
Summary:	Frei0r plugins using OpenCV
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description opencv
Frei0r plugins that use the OpenCV computer vision framework.

%package -n     frei0r-devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n frei0r-devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -n frei0r-%{version} -p1


%build
%cmake -DCMAKE_INSTALL_LIBDIR=%{_lib} \

%cmake_build


%install
%cmake_install

#Remove installed doc
rm -rf %{buildroot}%{_docdir}/%{name}


%files
%doc ChangeLog README.md
%license COPYING
%dir %{_libdir}/frei0r-1
%exclude %{_libdir}/frei0r-1/facebl0r.so
%exclude %{_libdir}/frei0r-1/facedetect.so
%{_libdir}/frei0r-1/*.so

%files opencv
%{_libdir}/frei0r-1/facebl0r.so
%{_libdir}/frei0r-1/facedetect.so

%files -n frei0r-devel
%{_includedir}/frei0r.h
%{_includedir}/frei0r.hpp
%dir %{_includedir}/frei0r
%{_includedir}/frei0r/*.h
%{_libdir}/pkgconfig/frei0r.pc

%changelog
* Tue Sep 16 2025 Nicolas Chauvet <kwizart@gmail.com> - 2.4.0-1
- Update to 2.4.0

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Feb 04 2025 Sérgio Basto <sergio@serjux.com> - 2.3.3-6
- Rebuild for opencv-4.11.0

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 25 2024 Sérgio Basto <sergio@serjux.com> - 2.3.3-4
- Rebuild for opencv 4.10.0

* Thu Jul 25 2024 Miroslav Suchý <msuchy@redhat.com> - 2.3.3-3
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jul 04 2024 Nicolas Chauvet <kwizart@gmail.com> - 2.3.3-1
- Update to 2.3.3

* Mon Feb 05 2024 Sérgio Basto <sergio@serjux.com> - 2.3.2-4
- Rebuild for opencv 4.9.0

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 11 2023 Nicolas Chauvet <kwizart@gmail.com> - 2.3.2-1
- Update to 2.3.2

* Mon Aug 07 2023 Sérgio Basto <sergio@serjux.com> - 2.3.1-2
- Rebuild for opencv 4.8.0

* Sun Aug 06 2023 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-1
- Update to 2.3.1

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon May 22 2023 Nicolas Chauvet <kwizart@gmail.com> - 2.3.0-1
- Update to 2.3.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023 Sérgio Basto <sergio@serjux.com> - 2.2.0-2
- Rebuild for opencv 4.7.0

* Mon Jan 09 2023 Nicolas Chauvet <kwizart@gmail.com> - 2.2.0-1
- Update to 2.2.0

* Mon Jan 02 2023 Nicolas Chauvet <kwizart@gmail.com> - 2.1.0-1
- Update to 2.1.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 21 2022 Sérgio Basto <sergio@serjux.com> - 1.8.0-2
- Rebuilt for opencv 4.6.0

* Wed Mar 30 2022 Nicolas Chauvet <kwizart@gmail.com> - 1.8.0-1
- Update to 1.8.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct 22 2020 Nicolas Chauvet <kwizart@gmail.com> - 1.7.0-11
- Rebuilt for OpenCV

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-10
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
- Fix cmake build

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 04 2020 Nicolas Chauvet <kwizart@gmail.com> - 1.7.0-8
- Rebuilt for OpenCV 4.3

* Mon May 25 2020 Nicolas Chauvet <kwizart@gmail.com> - 1.7.0-7
- Apply patches from PR toward opencv4 support
- Switch to cmake

* Fri Mar 06 2020 Nicolas Chauvet <kwizart@gmail.com> - 1.7.0-6
- Update wip opencv patch

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 28 2020 Nicolas Chauvet <kwizart@gmail.com> - 1.7.0-4
- Rebuild for OpenCV 4.2

* Mon Jan 20 2020 Nicolas Chauvet <kwizart@gmail.com>
- Rebuilt without OpenCV

* Mon Dec 30 2019 Nicolas Chauvet <kwizart@gmail.com> - 1.7.0-2
- Rebuilt for opencv4

* Sun Dec 15 2019 Nicolas Chauvet <kwizart@gmail.com> - 1.7.0-1
- Update to 1.7.0

* Wed Sep 11 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.1-9
- Rebuild for opencv (with vtk disabled)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
- Fix fails to build with opencv 3.4.2 (https://github.com/dyne/frei0r/issues/26)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 05 2018 Adam Williamson <awilliam@redhat.com> - 1.6.1-5
- Rebuild for opencv soname bump

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Dec 24 2017 Sérgio Basto <sergio@serjux.com> - 1.6.1-3
- Rebuild (opencv-3.3.1)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Nicolas Chauvet <kwizart@gmail.com> - 1.6.1-1
- Update to 1.6.1

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Feb 28 2017 Nicolas Chauvet <kwizart@gmail.com> - 1.5-6
- Rebuilt for OpenCV 3.2.0
- Modernize spec file

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue May 10 2016 Sérgio Basto <sergio@serjux.com> - 1.5-2
- Rebuild (opencv)

* Wed May 04 2016 Sérgio Basto <sergio@serjux.com> - 1.5-1
- New upstream release
- Spec modernization

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.4-4
- Rebuilt for GCC 5 C++11 ABI change

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Nov 13 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.4-1
- Update to 1.4

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Matthias Clasen <mclasen@redhat.com> 1.3-11
- Fix source url

* Mon May 06 2013 Adam Jackson <ajax@redhat.com> 1.3-10
- Move OpenCV plugins to a subpackage

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 10 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.3-8
- Rebuilt for opencv built without nonfree/gpu modules
- Improve description

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.3-6
- Rebuilt for OpenCV 2.4.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 10 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.3-4
- Fix unowned directory - rhbz#744889

* Sun Aug 21 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.3-3
- Rebuild for OpenCV 2.3.1

* Fri May 27 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.3-1
- Update to 1.3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 06 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.2.1-2
- Rebuild for OpenCV 2.2

* Fri Nov 26 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.2.1-1
- Update to 1.2.1

* Sat Jun 26 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.1.22-5
- Rebuilt for opencv

* Sat Feb 27 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.1.22-4
- Rebuild for opencv SO version change

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 22 2009 kwizart < kwizart at gmail.com > - 1.1.22-2
- Rebuild for opencv

* Tue Mar 24 2009 kwizart < kwizart at gmail.com > - 1.1.22-1
- Update to 1.1.22
- Prevent timestamp change when installing

* Tue Jul 22 2008 kwizart < kwizart at gmail.com > - 1.1.21-2
- Add gcc43 patches

* Sat Jun  7 2008 kwizart < kwizart at gmail.com > - 1.1.21-1
- Initial spec file for Fedora.

