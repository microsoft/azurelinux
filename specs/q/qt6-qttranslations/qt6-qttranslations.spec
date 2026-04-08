# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global qt_module qttranslations

#global unstable 0
%if 0%{?unstable}
%global prerelease rc
%endif

Summary: Qt6 - QtTranslations module
Name:    qt6-%{qt_module}
Version: 6.10.2
Release: 1%{?dist}

License: GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
%global  qt_version %(echo %{version} | cut -d~ -f1)

%if 0%{?unstable}
Source0: https://download.qt.io/development_releases/qt/%{majmin}/%{qt_version}/submodules/%{qt_module}-everywhere-src-%{qt_version}-%{prerelease}.tar.xz
%else
Source0: https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz
%endif

BuildArch: noarch

BuildRequires: cmake
BuildRequires: ninja-build
## versioning recently dropped, but could do >= %%majmin if needed --rex
BuildRequires: qt6-qtbase-devel
# for lrelease
BuildRequires: qt6-linguist
BuildRequires: qt6-qttools-devel

# help system-config-language and dnf/yum langpacks pull these in
%if 0%{?_qt6:1}
Provides: %{_qt6}-ar = %{version}-%{release}
Provides: %{_qt6}-ca = %{version}-%{release}
Provides: %{_qt6}-cs = %{version}-%{release}
Provides: %{_qt6}-da = %{version}-%{release}
Provides: %{_qt6}-de = %{version}-%{release}
Provides: %{_qt6}-es = %{version}-%{release}
Provides: %{_qt6}-fa = %{version}-%{release}
Provides: %{_qt6}-fi = %{version}-%{release}
Provides: %{_qt6}-fr = %{version}-%{release}
Provides: %{_qt6}-gl = %{version}-%{release}
Provides: %{_qt6}-gd = %{version}-%{release}
Provides: %{_qt6}-he = %{version}-%{release}
Provides: %{_qt6}-hu = %{version}-%{release}
Provides: %{_qt6}-hr = %{version}-%{release}
Provides: %{_qt6}-it = %{version}-%{release}
Provides: %{_qt6}-ja = %{version}-%{release}
Provides: %{_qt6}-ka = %{version}-%{release}
Provides: %{_qt6}-ko = %{version}-%{release}
Provides: %{_qt6}-lg = %{version}-%{release}
Provides: %{_qt6}-lt = %{version}-%{release}
Provides: %{_qt6}-lv = %{version}-%{release}
Provides: %{_qt6}-nl = %{version}-%{release}
Provides: %{_qt6}-nn = %{version}-%{release}
Provides: %{_qt6}-pl = %{version}-%{release}
Provides: %{_qt6}-pt_BR = %{version}-%{release}
Provides: %{_qt6}-pt_PT = %{version}-%{release}
Provides: %{_qt6}-ru = %{version}-%{release}
Provides: %{_qt6}-sk = %{version}-%{release}
Provides: %{_qt6}-sl = %{version}-%{release}
Provides: %{_qt6}-sv = %{version}-%{release}
Provides: %{_qt6}-uk = %{version}-%{release}
Provides: %{_qt6}-zh_CN = %{version}-%{release}
Provides: %{_qt6}-zh_TW = %{version}-%{release}
%endif

%description
%{summary}.


%prep
%autosetup -n %{qt_module}-everywhere-src-%{qt_version}%{?unstable:-%{prerelease}} -p1


%build
%cmake_qt6

%cmake_build


%install
%cmake_install

# not used currently, since we track locales manually to keep %%files/Provides sync'd -- rex
#find_lang qttranslations --all-name --with-qt --without-mo

%files
%license LICENSES/*
%{_prefix}/lib64/qt6/sbom/%{qt_module}-%{qt_version}.spdx
%{_qt6_datadir}/translations/catalogs.json
%lang(ar) %{_qt6_translationdir}/*_ar.qm
%lang(bg) %{_qt6_translationdir}/*_bg.qm
%lang(ca) %{_qt6_translationdir}/*_ca.qm
%lang(cs) %{_qt6_translationdir}/*_cs.qm
%lang(da) %{_qt6_translationdir}/*_da.qm
%lang(de) %{_qt6_translationdir}/*_de.qm
%lang(es) %{_qt6_translationdir}/*_es.qm
%lang(en) %{_qt6_translationdir}/*_en.qm
%lang(fa) %{_qt6_translationdir}/*_fa.qm
%lang(fi) %{_qt6_translationdir}/*_fi.qm
%lang(fr) %{_qt6_translationdir}/*_fr.qm
%lang(gd) %{_qt6_translationdir}/*_gd.qm
%lang(gl) %{_qt6_translationdir}/*_gl.qm
%lang(he) %{_qt6_translationdir}/*_he.qm
%lang(hu) %{_qt6_translationdir}/*_hu.qm
%lang(hr) %{_qt6_translationdir}/*_hr.qm
%lang(it) %{_qt6_translationdir}/*_it.qm
%lang(ja) %{_qt6_translationdir}/*_ja.qm
%lang(ka) %{_qt6_translationdir}/*_ka.qm
%lang(ko) %{_qt6_translationdir}/*_ko.qm
%lang(lg) %{_qt6_translationdir}/*_lg.qm
%lang(lt) %{_qt6_translationdir}/*_lt.qm
%lang(lv) %{_qt6_translationdir}/*_lv.qm
%lang(nl) %{_qt6_translationdir}/*_nl.qm
%lang(nn) %{_qt6_translationdir}/*_nn.qm
%lang(pl) %{_qt6_translationdir}/*_pl.qm
%lang(pt_BR) %{_qt6_translationdir}/*_pt_BR.qm
%lang(pt_PT) %{_qt6_translationdir}/*_pt_PT.qm
%lang(ru) %{_qt6_translationdir}/*_ru.qm
%lang(sk) %{_qt6_translationdir}/*_sk.qm
%lang(sl) %{_qt6_translationdir}/*_sl.qm
%lang(sv) %{_qt6_translationdir}/*_sv.qm
%lang(tr) %{_qt6_translationdir}/*_tr.qm
%lang(uk) %{_qt6_translationdir}/*_uk.qm
%lang(zh_CN) %{_qt6_translationdir}/*_zh_CN.qm
%lang(zh_TW) %{_qt6_translationdir}/*_zh_TW.qm


%changelog
* Mon Feb 09 2026 Jan Grulich <jgrulich@redhat.com> - 6.10.2-1
- 6.10.2

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 6.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Nov 20 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.1-1
- 6.10.1

* Tue Oct 07 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.0-1
- 6.10.0

* Thu Sep 25 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.0~rc-1
- 6.10.0 RC

* Thu Aug 28 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.2-1
- 6.9.2

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.1-1
- 6.9.1

* Wed Apr 02 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.0-1
- 6.9.0

* Mon Mar 24 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.0~rc-1
- 6.9.0 RC

* Fri Jan 31 2025 Jan Grulich <jgrulich@redhat.com> - 6.8.2-1
- 6.8.2

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Nov 28 2024 Jan Grulich <grulja@gmail.com> - 6.8.1-1
- 6.8.1

* Fri Oct 11 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.0-1
- 6.8.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 01 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.2-1
- 6.7.2

* Tue May 21 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.1-1
- 6.7.1

* Tue Apr 02 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.0-1
- 6.7.0

* Thu Feb 15 2024 Jan Grulich <jgrulich@redhat.com> - 6.6.2-1
- 6.6.2

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 27 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.1-1
- 6.6.1

* Tue Oct 10 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.0-1
- 6.6.0

* Sun Oct 01 2023 Justin Zobel <justin.zobel@gmail.com> - 6.5.3-1
- new version

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 21 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.2-1
- 6.5.2

* Wed Jul 12 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-2
- Rebuild for qtbase private API version change

* Mon May 22 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-1
- 6.5.1

* Tue Apr 04 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.0-1
- 6.5.0

* Thu Mar 23 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.3-1
- 6.4.3

* Tue Jan 31 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.2-3
- migrated to SPDX license

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.2-1
- 6.4.2

* Wed Nov 23 2022 Jan Grulich <jgrulich@redhat.com> - 6.4.1-1
- 6.4.1

* Mon Oct 31 2022 Jan Grulich <jgrulich@redhat.com> - 6.4.0-1
- 6.4.0

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 13 2022 Jan Grulich <jgrulich@redhat.com> - 6.3.1-1
- 6.3.1

* Wed Apr 13 2022 Jan Grulich <jgrulich@redhat.com> - 6.3.0-1
- 6.3.0

* Mon Jan 31 2022 Jan Grulich <jgrulich@redhat.com> - 6.2.3-1
- 6.2.3

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 14 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.2-1
- 6.2.2

* Fri Oct 29 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.1-1
- 6.2.1

* Thu Sep 30 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0-1
- 6.2.0

* Mon Sep 27 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~rc2-1
- 6.2.0 - rc2

* Sat Sep 18 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~rc-1
- 6.2.0 - rc

* Mon Sep 13 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~beta4-1
- 6.2.0 - beta4

* Thu Aug 12 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.2-1
- 6.1.2

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 07 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.1-1
- 6.1.1

* Thu May 06 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.0-1
- 6.1.0

* Mon Apr 05 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.3-1
- 6.0.3

* Thu Feb 04 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.1-1
- 6.0.1

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 14 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.0-1
- 6.0.0
