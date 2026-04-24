# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gitcommit 2a3605a2182218ab5017beff064c81ae7936832f
%global gitshortcommit %(c=%{gitcommit}; echo ${c:0:7})
%global snapshotdate 20250925

Name: kdump-anaconda-addon
Version: 006
Release: 17.%{snapshotdate}git%{gitshortcommit}%{?dist}
Url: https://github.com/rhinstaller/kdump-anaconda-addon
License: GPL-2.0-only
Summary: Kdump configuration anaconda addon

BuildArch: noarch
Requires: anaconda-core >= 34.13
Requires: hicolor-icon-theme
BuildRequires: intltool gettext
BuildRequires: make
Obsoletes: kexec-tools-anaconda-addon < 2.0.17-9
Provides: kexec-tools-anaconda-addon = %{version}-%{release}

Source0: https://github.com/rhinstaller/kdump-anaconda-addon/archive/%{gitcommit}/kdump-anaconda-addon-%{gitshortcommit}.tar.gz

%description
Kdump anaconda addon

%prep
%autosetup -n %{name}-%{gitcommit}

%build

%install
%make_install

%find_lang kdump-anaconda-addon

%files -f kdump-anaconda-addon.lang
%doc README
%license LICENSE
%{_datadir}/anaconda/addons/com_redhat_kdump
%{_datadir}/anaconda/dbus/confs/org.fedoraproject.Anaconda.Addons.Kdump.conf
%{_datadir}/anaconda/dbus/services/org.fedoraproject.Anaconda.Addons.Kdump.service
%{_datadir}/icons/hicolor/scalable/apps/kdump.svg

%changelog
* Thu Sep 25 2025 Coiby Xu <coxu@redhat.com> - 006-16.20250925git2a3605a
- Feature: Set up crypttab for encrypted dump target

* Wed Jul 30 2025 Adam Williamson <awilliam@redhat.com> - 006-15.20220714git7ca2d3e
- Depend on anaconda-core not anaconda

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 006-14.20220714git7ca2d3e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 006-13.20220714git7ca2d3e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 006-12.20220714git7ca2d3e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 006-11.20220714git7ca2d3e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 006-10.20220714git7ca2d3e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 006-9.20220714git7ca2d3e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 006-8.20220714git7ca2d3e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 006-7.20220714git7ca2d3e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 14 2022 Coiby <coxu@redhat.com> - 006-1.20220714git7ca2d3e
- Update to latest git snapshot (20220714).

* Thu Jan 20 2022 Coiby <coxu@redhat.com> - 006-1.20220128git9603258
- Update to latest git snapshot (20220128).

* Thu Jan 20 2022 Coiby <coxu@redhat.com> - 006-1.20220120git44fe737
- Update to latest git snapshot (20220120)

* Thu Jan 13 2022 Coiby <coxu@redhat.com> - 006-1.20220113git4c5a91d
- Update to latest git snapshot (20220113)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 006-3.20201128git4ba507e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 006-2.20201128git4ba507e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Nov 28 2020 Kairui Song <kasong@redhat.com> - 006-1.20201128git4ba507e
- Update to latest git snapshot (20201128)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 005-9.20200220git80aab11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Feb 20 2020 Kairui Song <kasong@redhat.com> - 005-8.20200220git80aab11
- Update to latest git snapshot (20200220)

* Tue Jan 14 2020 Kairui Song <kasong@redhat.com> - 005-7.20200114git122ccd9
- Update to latest git snapshot (20200114)

* Wed Aug 7 2019 Kairui Song <kasong@redhat.com> - 005-6.20190730gitc109552
- Update to latest git snapshot (20190723)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 005-5.20190103gitb16ea2c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 005-4.20190103gitb16ea2c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 3 2019 Kairui Song <kasong@redhat.com> - 005-3.20190103gitb16ea2c
- Update to latest git snapshot (20190103)

* Tue Aug 7 2018 Kairui Song <kasong@redhat.com> - 005-2.20180730git966223e
- Bump obsoleted kexec-tools-anaconda-addon version
- Remove redundant source files

* Tue Aug 7 2018 Kairui Song <kasong@redhat.com> - 005-1.20180730git966223e
- Update to latest git snapshot (20180730)

* Mon Jul 9 2018 Kairui Song <kasong@redhat.com> - 005-1.20180626git8b243e3
- Initial package for kdump-anaconda-addon
