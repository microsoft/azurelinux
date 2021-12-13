Vendor:         Microsoft Corporation
Distribution:   Mariner
%global gitcommit 80aab11a01382e1c12499c34ad227b895870db70
%global gitshortcommit %(c=%{gitcommit}; echo ${c:0:7})

Name: kdump-anaconda-addon
Version: 005
Release: 9%{?dist}
Url: https://github.com/daveyoung/kdump-anaconda-addon
License: GPLv2
Summary: Kdump configuration anaconda addon

BuildArch: noarch
Requires: anaconda >= 21.33
Requires: hicolor-icon-theme
BuildRequires: intltool gettext
Obsoletes: kexec-tools-anaconda-addon < 2.0.17-9
Provides: kexec-tools-anaconda-addon = %{version}-%{release}

Source0: https://github.com/daveyoung/kdump-anaconda-addon/archive/%{gitcommit}/kdump-anaconda-addon-%{gitshortcommit}.tar.gz

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
%{_datadir}/icons/hicolor/scalable/apps/kdump.svg

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 005-9
- Initial CBL-Mariner import from Fedora 31 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

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
