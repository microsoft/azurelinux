# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global framework syndication

# uncomment to enable bootstrap mode
#global bootstrap 1

%if !0%{?bootstrap}
%global tests 1
%endif

Name:    kf5-%{framework}
Epoch:   1
Version: 5.116.0
Release: 5%{?dist}
Summary: The Syndication Library

License: BSD-2-Clause AND CC0-1.0 AND GPL-2.0-or-later AND LGPL-2.0-or-later
URL:     https://invent.kde.org/frameworks/%{framework}

%global majmin %majmin_ver_kf5
%global stable %stable_kf5
Source0: http://download.kde.org/%{stable}/frameworks/%{majmin}/%{framework}-%{version}.tar.xz

BuildRequires: make
BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-rpm-macros
BuildRequires:  kf5-kio-devel >= %{version}
BuildRequires:  kf5-kcodecs-devel >= %{version}

BuildRequires:  qt5-qtbase-devel

%if 0%{?tests}
#BuildRequires: dbus-x11
BuildRequires:  time
#BuildRequires: xorg-x11-server-Xvfb
%endif

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}
%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -n %{framework}-%{version} -p1


%build
%{cmake_kf5} \
  -DBUILD_TESTING:BOOL=%{?tests:ON}%{!?tests:OFF}
%cmake_build


%install
%cmake_install


%check
%if 0%{?tests}
DBUS_SESSION_BUS_ADDRESS=
DISPLAY=
export CTEST_OUTPUT_ON_FAILURE=1
%ctest ||:
%endif


%ldconfig_scriptlets

%files
%license LICENSES/*.txt
%{_kf5_datadir}/qlogging-categories5/%{framework}.*
%{_kf5_libdir}/libKF5Syndication.so.*

%files devel

%{_kf5_includedir}/Syndication/
%{_kf5_libdir}/libKF5Syndication.so
%{_kf5_libdir}/cmake/KF5Syndication/
%{_kf5_archdatadir}/mkspecs/modules/qt_Syndication.pri


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.116.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.116.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.116.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun May 19 2024 Alessandro Astone <ales.astone@gmail.com> - 1:5.116.0-1
- 5.116.0

* Sat Feb 10 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 1:5.115.0-1
- 5.115.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.113.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.113.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 08 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 1:5.113.0-1
- 5.113.0

* Tue Oct 10 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 1:5.111.0-1
- 5.111.0

* Tue Sep 05 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 1:5.110.0-1
- 5.110.0

* Sat Aug 05 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 1:5.109.0-1
- 5.109.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.108.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jul 02 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 1:5.108.0-1
- 5.108.0

* Sat Jun 03 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 1:5.107.0-1
- 5.107.0

* Mon May 15 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 1:5.106.0-1
- 5.106.0

* Sun Apr 02 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 1:5.105.0-1
- 5.105.0

* Sat Mar 04 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 1:5.104.0-1
- 5.104.0

* Sun Feb 05 2023 Marc Deop <marcdeop@fedoraproject.org> - 1:5.103.0-1
- 5.103.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.102.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jan 14 2023 Marc Deop <marcdeop@fedoraproject.org> - 1:5.102.0-1
- 5.102.0

* Mon Dec 12 2022 Marc Deop <marcdeop@fedoraproject.org> - 1:5.101.0-1
- 5.101.0
- use new macros to simplify code

* Sun Nov 06 2022 Marc Deop <marcdeop@fedoraproject.org> - 1:5.100.0-1
- 5.100.0

* Fri Oct 14 2022 Marc Deop <marcdeop@fedoraproject.org> - 1:5.99.0-1
- 5.99.0

* Thu Sep 15 2022 Marc Deop <marcdeop@fedoraproject.org> - 1:5.98.0-1
- 5.98.0

* Sat Aug 13 2022 Justin Zobel <justin@1707.io> - 5.97.0-1
- Update to 5.97.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.96.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jul 03 2022 Marc Deop <marcdeop@fedoraproject.org> - 1:5.96.0-1
- 5.96.0

* Fri May 13 2022 Rex Dieter <rdieter@fedoraproject.org> - 1:5.94.0-1
- 5.94.0

* Sun Apr 10 2022 Justin Zobel <justin@1707.io> - 5.93-1
- Update to 5.93

* Thu Mar 10 2022 Rex Dieter <rdieter@fedoraproject.org> - 1:5.92.0-1
- 5.92.0

* Fri Feb 11 2022 Rex Dieter <rdieter@fedoraproject.org> - 1:5.91.0-1
- 5.91.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.90.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 04 2022 Marc Deop i Argemí (Private) <marc@marcdeop.com> - 1:5.90.0-1
- 5.90.0

* Wed Dec 08 2021 Rex Dieter <rdieter@fedoraproject.org> - 1:5.89.0-1
- 5.89.0

* Mon Nov 08 2021 Marc Deop <marcdeop@fedoraproject.org> - 1:5.88.0-1
- 5.88.0

* Tue Oct 05 2021 Rex Dieter <rdieter@fedoraproject.org> - 1:5.87.0-1
- 5.87.0

* Tue Sep 14 2021 Marc Deop <marcdeop@fedoraproject.org> - 1:5.86.0-1
- 5.86.0

* Thu Aug 12 2021 Rex Dieter <rdieter@fedoraproject.org> - 1:5.85.0-1
- 5.85.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.83.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 08 2021 Rex Dieter <rdieter@fedoraproject.org> - 1:5.83.0-1
- 5.83.0

* Mon May 03 2021 Rex Dieter <rdieter@fedoraproject.org> - 1:5.82.0-1
- 5.82.0

* Tue Apr 06 2021 Rex Dieter <rdieter@fedoraproject.org> - 1:5.81.0-1
- 5.81.0

* Tue Mar 09 2021 Rex Dieter <rdieter@fedoraproject.org> - 1:5.80.0-1
- 5.80.0

* Sat Feb 06 2021 Rex Dieter <rdieter@fedoraproject.org> - 1:5.79.0-2
- respin

* Sat Feb 06 2021 Rex Dieter <rdieter@fedoraproject.org> - 1:5.79.0-1
- 5.79.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.78.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan  4 08:59:59 CST 2021 Rex Dieter <rdieter@fedoraproject.org> - 1:5.78.0-1
- 5.78.0

* Sun Dec 13 14:22:29 CST 2020 Rex Dieter <rdieter@fedoraproject.org> - 1:5.77.0-1
- 5.77.0

* Thu Nov 19 09:16:28 CST 2020 Rex Dieter <rdieter@fedoraproject.org> - 1:5.76.0-1
- 5.76.0

* Wed Oct 14 10:10:24 CDT 2020 Rex Dieter <rdieter@fedoraproject.org> - 1:5.75.0-1
- 5.75.0

* Fri Sep 18 2020 Jan Grulich <jgrulich@redhat.com> - 1:5.74.0-1
- 5.74.0

* Mon Aug 03 2020 Rex Dieter <rdieter@fedoraproject.org> - 1:5.73.0-1
- 5.73.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.72.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 07 2020 Rex Dieter <rdieter@fedoraproject.org> - 1:5.72.0-1
- 5.72.0

* Tue Jun 16 2020 Rex Dieter <rdieter@fedoraproject.org> - 1:5.71.0-1
- 5.71.0

* Mon May 04 2020 Rex Dieter <rdieter@fedoraproject.org> - 1:5.70.0-1
- 5.70.0

* Tue Apr 21 2020 Rex Dieter <rdieter@fedoraproject.org> - 1:5.69.0-1
- 5.69.0

* Fri Mar 20 2020 Rex Dieter <rdieter@fedoraproject.org> - 1:5.68.0-1
- 5.68.0

* Mon Feb 03 2020 Rex Dieter <rdieter@fedoraproject.org> - 1:5.67.0-1
- 5.67.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.66.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 07 2020 Rex Dieter <rdieter@fedoraproject.org> - 1:5.66.0-1
- 5.66.0

* Tue Dec 17 2019 Rex Dieter <rdieter@fedoraproject.org> - 1:5.65.0-1
- 5.65.0

* Fri Nov 08 2019 Rex Dieter <rdieter@fedoraproject.org> - 1:5.64.0-1
- 5.64.0

* Tue Oct 22 2019 Rex Dieter <rdieter@fedoraproject.org> - 1:5.63.0-1
- 5.63.0

* Mon Sep 16 2019 Rex Dieter <rdieter@fedoraproject.org> - 1:5.62.0-1
- 5.62.0

* Wed Aug 07 2019 Rex Dieter <rdieter@fedoraproject.org> - 1:5.61.0-1
- 5.61.0

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.60.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jul 13 2019 Rex Dieter <rdieter@fedoraproject.org> - 1:5.60.0-1
- 5.60.0

* Thu Jun 06 2019 Rex Dieter <rdieter@fedoraproject.org> - 1:5.59.0-1
- 5.59.0

* Tue May 07 2019 Rex Dieter <rdieter@fedoraproject.org> - 1:5.58.0-1
- 5.58.0

* Tue Apr 09 2019 Rex Dieter <rdieter@fedoraproject.org> - 1:5.57.0-1
- 5.57.0

* Tue Mar 05 2019 Rex Dieter <rdieter@fedoraproject.org> - 1:5.56.0-1
- 5.56.0

* Mon Feb 04 2019 Rex Dieter <rdieter@fedoraproject.org> - 1:5.55.0-1
- 5.55.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.54.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 09 2019 Rex Dieter <rdieter@fedoraproject.org> - 1:5.54.0-1
- 5.54.0

* Sun Dec 09 2018 Rex Dieter <rdieter@fedoraproject.org> - 1:5.53.0-1
- 5.53.0

* Sun Nov 04 2018 Rex Dieter <rdieter@fedoraproject.org> - 1:5.52.0-1
- 5.52.0

* Wed Oct 10 2018 Rex Dieter <rdieter@fedoraproject.org> - 1:5.51.0-1
- 5.51.0

* Mon Sep 17 2018 Rex Dieter <rdieter@fedoraproject.org> - 1:5.50.0-2
- -devel: add epoch

* Wed Sep 05 2018 Rex Dieter <rdieter@fedoraproject.org> - 1:5.50-1
- kf5-syndication-5.50.0 (part of kde frameworks now), epoch++

* Fri Jul 13 2018 Rex Dieter <rdieter@fedoraproject.org> - 18.04.3-1
- 18.04.3

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 18.04.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 06 2018 Rex Dieter <rdieter@fedoraproject.org> - 18.04.2-1
- 18.04.2

* Wed May 09 2018 Rex Dieter <rdieter@fedoraproject.org> - 18.04.1-1
- 18.04.1

* Fri Apr 20 2018 Rex Dieter <rdieter@fedoraproject.org> - 18.04.0-1
- 18.04.0

* Tue Mar 06 2018 Rex Dieter <rdieter@fedoraproject.org> - 17.12.3-1
- 17.12.3

* Tue Feb 06 2018 Rex Dieter <rdieter@fedoraproject.org> - 17.12.2-1
- 17.12.2

* Thu Jan 11 2018 Rex Dieter <rdieter@fedoraproject.org> - 17.12.1-1
- 17.12.1

* Tue Dec 12 2017 Rex Dieter <rdieter@fedoraproject.org> - 17.12.0-1
- 17.12.0

* Wed Dec 06 2017 Rex Dieter <rdieter@fedoraproject.org> - 17.11.90-1
- 17.11.90

* Wed Nov 22 2017 Rex Dieter <rdieter@fedoraproject.org> - 17.11.80-1
- 17.11.80

* Wed Nov 08 2017 Rex Dieter <rdieter@fedoraproject.org> - 17.08.3-1
- 17.08.3

* Mon Sep 25 2017 Rex Dieter <rdieter@fedoraproject.org> - 17.08.1-1
- 17.08.1

* Fri Jul 28 2017 Rex Dieter <rdieter@fedoraproject.org> - 17.04.3-1
- 17.04.3

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 17.04.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 15 2017 Rex Dieter <rdieter@fedoraproject.org> - 17.04.2-1
- 17.04.2

* Thu May 11 2017 Rex Dieter <rdieter@fedoraproject.org> - 17.04.1-1
- 17.04.1

* Thu Mar 09 2017 Rex Dieter <rdieter@fedoraproject.org> - 16.12.3-1
- 16.12.3

* Thu Feb 09 2017 Rex Dieter <rdieter@fedoraproject.org> - 16.12.2-1
- 16.12.2

* Mon Jan 16 2017 Rex Dieter <rdieter@fedoraproject.org> - 16.12.1-1
- 16.12.1

* Mon Dec 05 2016 Rex Dieter <rdieter@fedoraproject.org> - 16.08.3-1
- 16.08.3

* Thu Oct 13 2016 Rex Dieter <rdieter@fedoraproject.org> - 16.08.2-1
- 16.08.2

* Thu Sep 08 2016 Rex Dieter <rdieter@fedoraproject.org> - 16.08.1-1
- 16.08.1

* Sun Sep 04 2016 Rex Dieter <rdieter@fedoraproject.org> - 16.08.0-1
- 16.08.0

* Sun Jul 10 2016 Rex Dieter <rdieter@fedoraproject.org> - 16.04.3-1
- 16.04.3

* Sun Jun 12 2016 Rex Dieter <rdieter@fedoraproject.org> - 16.04.2-1
- 16.04.2

* Wed May 25 2016 Rex Dieter <rdieter@fedoraproject.org> - 16.04.1-2
- %%check: polish, drop unused deps (dbus/xvfb), use test/fast
- bump kf5_ver

* Sun May 08 2016 Rex Dieter <rdieter@fedoraproject.org> - 16.04.1-1
- 16.04.1

* Sun May 01 2016 Rex Dieter <rdieter@fedoraproject.org> -  16.04.0-1
- 16.04.0

* Tue Mar 15 2016 Rex Dieter <rdieter@fedoraproject.org> - 15.12.3-1
- 15.12.3

* Sun Feb 14 2016 Rex Dieter <rdieter@fedoraproject.org> - 15.12.2-1
- 15.12.2

* Sat Feb 06 2016 Rex Dieter <rdieter@fedoraproject.org> 15.12.1-1
- 15.12.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 15.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 15 2015 Jan Grulich <jgrulich@redhat.com> - 15.12.0-2
- Remove obsoletes/conflicts with kdepimlibs

* Tue Dec 15 2015 Jan Grulich <jgrulich@redhat.com> - 15.12-0-1
- Update to 15.12.0

* Mon Dec 07 2015 Jan Grulich <jgrulich@redhat.com> - 15.11.90-1
- Update to 15.11.90

* Thu Dec 03 2015 Jan Grulich <jgrulich@redhat.com> - 15.11.80-1
- Update to 15.11.80

* Mon Aug 24 2015 Daniel Vrátil <dvratil@redhat.com> - 15.08.0-1
- Initial version
