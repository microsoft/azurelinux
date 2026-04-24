# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Bump this as appropriate when doing release updates, check i.e. with abi_compliance_checker
# First digit: major, bump when incompatible changes were performed
# Second digit: minor, bump when interface was extended
%global lib_ver 2.0.0
#global pre beta

%if 0%{?rhel}
%bcond_with qt6
%else
%bcond_without qt6
%endif

Name:           qcustomplot
Version:        2.1.1
Release: 15%{?dist}
Summary:        Qt widget for plotting and data visualization

License:        GPL-3.0-or-later
URL:            http://www.qcustomplot.com/
Source0:        http://www.qcustomplot.com/release/%{version}%{?pre:-%pre}/QCustomPlot.tar.gz
Source1:        CMakeLists.txt

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc-c++
BuildRequires:  qt5-qtbase-devel
%if %{with qt6}
BuildRequires:  qt6-qtbase-devel
%endif


%description
QCustomPlot is a Qt C++ widget for plotting and data visualization.
This plotting library focuses on making good looking, publication quality 2D
plots, graphs and charts, as well as offering high performance for realtime
visualization applications.

This package contains the Qt4 version.


%package        qt5
Summary:        Qt widget for plotting and data visualization

%description    qt5
QCustomPlot is a Qt C++ widget for plotting and data visualization.
This plotting library focuses on making good looking, publication quality 2D
plots, graphs and charts, as well as offering high performance for realtime
visualization applications.

This package contains the Qt5 version.


%package        qt5-devel
Summary:        Development files for %{name} (Qt5)
Requires:       %{name}-qt5%{?_isa} = %{version}-%{release}

%description    qt5-devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name} (Qt5).


%if %{with qt6}
%package        qt6
Summary:        Qt widget for plotting and data visualization

%description    qt6
QCustomPlot is a Qt C++ widget for plotting and data visualization.
This plotting library focuses on making good looking, publication quality 2D
plots, graphs and charts, as well as offering high performance for realtime
visualization applications.

This package contains the Qt6 version.


%package        qt6-devel
Summary:        Development files for %{name} (Qt6)
Requires:       %{name}-qt6%{?_isa} = %{version}-%{release}

%description    qt6-devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name} (Qt6).
%endif


%package        doc
Summary:        Documentation and examples for %{name}
BuildArch:      noarch

%description    doc
The %{name}-doc package contains the documentation and examples for
%{name}.


%prep
%autosetup -p1 -n %{name}
cp -a %{SOURCE1} .


%build
%define _vpath_builddir %{_target_platform}-qt5
%cmake -DQT_VER=5 -DLIB_VER=%{lib_ver}
%cmake_build

%if %{with qt6}
%define _vpath_builddir %{_target_platform}-qt6
%cmake -DQT_VER=6 -DLIB_VER=%{lib_ver}
%cmake_build
%endif


%install
%define _vpath_builddir %{_target_platform}-qt5
%cmake_install

install -d %{buildroot}%{_libdir}/pkgconfig/

cat > %{buildroot}%{_libdir}/pkgconfig/%{name}-qt5.pc <<EOF
libdir=%{_libdir}
includedir=%{_includedir}

Name: %{name}
Description: %{summary}
Version: %{version}
Cflags: -I\${includedir}
Libs: -L\${libdir} -lqcustomplot-qt5
EOF

%if %{with qt6}
%define _vpath_builddir %{_target_platform}-qt6
%cmake_install

cat > %{buildroot}%{_libdir}/pkgconfig/%{name}-qt6.pc <<EOF
libdir=%{_libdir}
includedir=%{_includedir}

Name: %{name}
Description: %{summary}
Version: %{version}
Cflags: -I\${includedir}
Libs: -L\${libdir} -lqcustomplot-qt6
EOF
%endif


%files qt5
%license GPL.txt
%{_libdir}/libqcustomplot-qt5.so.*

%files qt5-devel
%{_includedir}/qcustomplot.h
%{_libdir}/libqcustomplot-qt5.so
%{_libdir}/pkgconfig/%{name}-qt5.pc

%if %{with qt6}
%files qt6
%license GPL.txt
%{_libdir}/libqcustomplot-qt6.so.*

%files qt6-devel
%{_includedir}/qcustomplot.h
%{_libdir}/libqcustomplot-qt6.so
%{_libdir}/pkgconfig/%{name}-qt6.pc
%endif

%files doc
%license GPL.txt
%doc changelog.txt
%doc documentation examples


%changelog
* Sun Oct 12 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 2.1.1-14
- Fix dependencies

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 17 2025 Sandro Mani <manisandro@gmail.com> - 2.1.1-12
- Raise minimum CMake version, use GNUInstallDirs

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 05 2023 Sandro Mani <manisandro@gmail.com> - 2.1.1-7
- Conditionalize qt6 build

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 29 2022 Sandro Mani <manisandro@gmail.com> - 2.1.1-4
- Set CMAKE_AUTOMOC to ON
- Fix lib version take two

* Mon Nov 28 2022 Sandro Mani <manisandro@gmail.com> - 2.1.1-3
- Fix lib version

* Mon Nov 28 2022 Sandro Mani <manisandro@gmail.com> - 2.1.1-2
- Add Qt6 build, drop Qt4 build

* Wed Nov 09 2022 Sandro Mani <manisandro@gmail.com> - 2.1.1-1
- Update to 2.1.1

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Mar 29 2021 Sandro Mani <manisandro@gmail.com> - 2.1.0-1
- Update to 2.1.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 25 2018 Sandro Mani <manisandro@gmail.com> - 2.0.1-1
- Update to 2.0.1

* Mon Feb 19 2018 Sandro Mani <manisandro@gmail.com> - 2.0.0-1
- Update to 2.0.0
- Add missing BR: gcc-c++, make

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-0.2.beta
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Aug 20 2017 Sandro Mani <manisandro@gmail.com> - 2.0.0-0.1.beta
- Update to 2.0.0-beta

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 22 2015 Sandro Mani <manisandro@gmail.com> - 1.3.2-1
- Update to 1.3.2

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 30 2015 Sandro Mani <manisandro@gmail.com> - 1.3.1-3
- Fix qcustomplot-qt5.pc

* Wed Apr 29 2015 Sandro Mani <manisandro@gmail.com> - 1.3.1-2
- Also build a qt5 version

* Sat Apr 25 2015 Sandro Mani <manisandro@gmail.com> - 1.3.1-1
- Update to 1.3.1

* Sun Dec 28 2014 Sandro Mani <manisandro@gmail.com> - 1.3.0-1
- Update to 1.3.0

* Fri Dec 19 2014 Sandro Mani <manisandro@gmail.com> - 1.2.1-2
- BuildRequires: qt-devel -> qt4-devel
- Use %%license
- Don't abuse version as so version
- Use -Wl,--as-needed

* Sat Aug 09 2014 Sandro Mani <manisandro@gmail.com> - 1.2.1-1
- Initial package
