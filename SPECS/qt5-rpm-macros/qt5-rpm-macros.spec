Summary:        RPM macros for building Qt5 and KDE Frameworks 5 packages
Name:           qt5-rpm-macros
Version:        5.12.5
Release:        3%{?dist}
License:        GPLv3
URL:            https://getfedora.org/
Source0:        macros.qt5
Source1:        qmake-qt5.sh
BuildArch:      noarch
Vendor:         Microsoft Corporation
Distribution:   Mariner

Conflicts: qt5
Conflicts: qt5-qtbase-devel < 5.6.0-0.23

%description
%{summary}.

%install
install -Dpm644 %{SOURCE0} %{buildroot}%{_rpmconfigdir}/macros.d/macros.qt5
install -Dpm755 %{SOURCE1} %{buildroot}%{_bindir}/qmake-qt5.sh
mkdir -p %{buildroot}%{_datadir}/qt5/wrappers
ln -s %{_bindir}/qmake-qt5.sh %{buildroot}%{_datadir}/qt5/wrappers/qmake-qt5
ln -s %{_bindir}/qmake-qt5.sh %{buildroot}%{_datadir}/qt5/wrappers/qmake

# substitute custom flags, and the path to binaries: binaries referenced from
# macros should not change if an application is built with a different prefix.
# %_libdir is left as /usr/%{_lib} (e.g.) so that the resulting macros are
# architecture independent, and don't hardcode /usr/lib or /usr/lib64.
sed -i \
  -e "s|@@QT5_CFLAGS@@|%{?qt5_cflags}|g" \
  -e "s|@@QT5_CXXFLAGS@@|%{?qt5_cxxflags}|g" \
  -e "s|@@QT5_RPM_LD_FLAGS@@|%{?qt5_rpm_ld_flags}|g" \
  -e "s|@@QT5_RPM_OPT_FLAGS@@|%{?qt5_rpm_opt_flags}|g" \
  -e "s|@@QMAKE@@|%{_prefix}/%%{_lib}/qt5/bin/qmake|g" \
  -e "s|@@QMAKE_QT5_WRAPPER@@|%{_bindir}/qmake-qt5.sh|g" \
  %{buildroot}%{_rpmconfigdir}/macros.d/macros.qt5

%files
%{_rpmconfigdir}/macros.d/macros.qt5
%{_bindir}/qmake-qt5.sh
%{_datadir}/qt5/wrappers/


%changelog
* Fri May 26 2023 Thien Trung Vuong <tvuong@microsoft.com> - 5.12.5-3
- Verified license.

* Thu Apr 02 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.12.5-2
- Initial CBL-Mariner import from Fedora 31 (license: MIT).
- Removing qt5 meta package bits and leaving only the macros.

* Tue Sep 24 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.5-1
- 5.12.5

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.12.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 11 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.4-1
- 5.12.4

* Tue Jun 04 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.3-1
- 5.12.3

* Thu Feb 14 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.1-1
- 5.12.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.11.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Dec 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.3-1
- 5.11.3

* Fri Sep 21 2018 Jan Grulich <jgrulich@redhat.com> - 5.11.2-1
- 5.11.2

* Tue Aug 21 2018 Owen Taylor <otaylor@redhat.com> - 5.11.1-4
- rpm-macros: always refer to binaries in their installed location, even if %%_libdir
  and %%_bindir are redefined.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.1-2
- %%_qt5_prefix=%%_prefix (was %%_libdir/qt5}

* Tue Jun 19 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.1-1
- 5.11.1

* Sat Jun 02 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.0-2
- rpm-macros: do not define _qt5_archdatadir, _qt5_bindir in terms of _qt5_prefix anymore

* Sat May 26 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.0-1
- 5.11.0

* Wed Mar 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.10.1-1
- 5.10.1
- rpm-macros: Requires: gcc-c++

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 24 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.10.0-4
- macros.qt5: fix path to qmake-qt5.sh wrapper

* Wed Jan 24 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.10.0-3
- use noarch-friendly paths for qmake-qt5.sh wrapper

* Wed Jan 24 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.10.0-2
- provide qmake-qt5.sh wrapper and new macro: %%qmake_qt5_wrapper

* Wed Jan 03 2018 Rex Dieter <rdieter@fedoraproject.org> 5.10.0-1
- 5.10.0

* Wed Jan 03 2018 Rex Dieter <rdieter@fedoraproject.org> 5.9.3-1
- 5.9.3

* Tue Oct 10 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.2-1
- 5.9.2

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.1-1
- 5.9.1

* Thu Jun 01 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.0-2
- drop -fno-delete-null-pointer-checks hack/workaround

* Sat Apr 15 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-1
- Up to match upcoming 5.9.0

* Fri Mar 31 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-3
- rebuild

* Fri Jan 27 2017 Helio Chissini de Castro <helio@kde.org> - 5.8.0-1
- Tie to new upstream release

* Mon Jan 02 2017 Rex Dieter <rdieter@math.unl.edu> - 5.7.1-2
- drop Requires: qt5-gstreamer qt5-qtacountsservice qt5-qtconfiguration (not from qtproject.org)

* Wed Nov 09 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.1-1
- Prepare for new release

* Tue Sep 27 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.0-10
- s/%%rhel/%%epel/ , cmake3 is only available in epel

* Wed Sep 14 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.0-9
- install the right macros.qt5-srpm file

* Wed Sep 14 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.0-8
- introduce -srpm-macros (initially defines %%qt5_qtwebengine_arches)
- -devel: drop Requires: qt5-qtwebengine-devel (since not all archs are supported)

* Sat Jul 23 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.0-7
- drop Requires: qt5-qtwebengine (not available on all archs)

* Tue Jul 12 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-6
- Fix macros with invalid substitutions.

* Wed Jul 06 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-5
- Fix typo. Thanks to Diego Herrera.
- Add macro qt5_includedir as more logical than headerdir. Old one still available

* Mon Jul 04 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-4
- Clang is not default anymore. End of experimentation phase

* Wed Jun 15 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-3
- Move package to be qt5 and create meta packages
- Add new macro for qml dir

* Mon Jun 13 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-2
- Test repositories using clang by default


* Thu Jun 09 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-1
- Decouple macros from main qtbase package
