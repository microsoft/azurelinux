Vendor:         Microsoft Corporation
Distribution:   Azure Linux

%global origname manpages-zh

Summary: Chinese Man Pages from Chinese Man Pages Project
Name:       man-pages-zh-CN
Version:    1.6.3.6
Release:    11%{?dist}
License:    GFDL-1.2-no-invariants-or-later
#Vendor:    From CMPP (Chinese Man Pages Project)
URL:        https://github.com/man-pages-zh/
Source0:    https://github.com/man-pages-zh/%{origname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArchitectures: noarch
Summary(zh_CN): 中文 man pages

Provides: man-pages-zh_CN = %{version}-%{release}

BuildRequires: make
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gnome-common
BuildRequires: opencc-tools
BuildRequires: python3
Requires: man-pages-reader
Supplements: (man-pages and langpacks-zh_CN)


%description
manpages-zh is a sub-project from i18n-zh, from the Chinese Man Pages
Project (CMPP). However, the original CMPP seems inactive, nor can the
original home page (cmpp.linuxforum.net) be visited.

This project revives and maintains the remains of CMPP.

So far the simplified Chinese is packed.

%description -l zh_CN
本项目(manpages-zh)为 i18n-zh 的子项目，从 CMPP (中文 Man Pages 计划) 分支而来。
CMPP 项目现在可能已经死亡，原主页(cmpp.linuxforum.net)已不能访问。

本项目的目的是维护 CMPP 遗留下的成果，并对其错误/漏洞进行修改。

%prep
%setup -q -n %{origname}-%{version}

%build 
# Disable zh_TW, as it requires dependencies only available in Debian.
gnome-autogen.sh
%configure --disable-zhtw
make %{?_smp_mflags}


%install
mkdir -p $RPM_BUILD_ROOT%{_mandir}/zh_CN
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
# Include the COPYRIGHT file in %doc macro
rm $RPM_BUILD_ROOT%{_datadir}/doc/manpages-zh/COPYRIGHT
# Remove file conflict
%global manDest $RPM_BUILD_ROOT%{_mandir}/zh_CN
rm -f %{manDest}/man1/newgrp.1


%files
%doc README NEWS COPYRIGHT
%license COPYING
%{_mandir}/zh_CN/man*/*

%changelog
* Tue Apr 29 2025 Archana Shettigar <v-shettigara@microsoft.com> - 1.6.3.6-11
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon May 22 2023 Peng Wu <pwu@redhat.com> - 1.6.3.6-6
- Rebuild the package

* Mon May 22 2023 Peng Wu <pwu@redhat.com> - 1.6.3.6-5
- Migrate to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Oct 27 2021 Peng Wu <pwu@redhat.com> - 1.6.3.6-1
- Update to 1.6.3.6

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Feb  1 2021 Peng Wu <pwu@redhat.com> - 1.6.3.4-1
- Update to 1.6.3.4

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Apr 28 2018 Till Maas <opensource@till.name> - 1.6.2.1-4
- Add missing python3 BR

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 27 2017 Peng Wu <pwu@redhat.com> - 1.6.2.1-1
- Change upstream and update to 1.6.2.1

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Feb 23 2016 Parag Nemade <pnemade AT redhat DOT com> - 1.5.2-11
- Add Supplements: for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 31 2015 Ding-Yi Chen <dchen at redhat dot com> - 1.5.2-8
- Add BuildRequire: autoconf, automake

* Tue Mar 31 2015 Ding-Yi Chen <dchen at redhat dot com> - 1.5.2-7
- Update source URL
- Provide man-pages-zh_CN

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 04 2013 Ding-Yi Chen <dchen at redhat dot com> - 0:1.5.1-4
- Fixed Bug 981001 - man-pages-zh-CN : Conflicts with man-db

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 12 2012 Peng Wu <pwu@redhat.com> - 1.5.2-2
- Clean up spec

* Thu Aug 23 2012  Peng Wu <pwu@redhat.com> - 1.5.2-1
- Update to 1.5.2

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Ding-Yi Chen <dchen at redhat dot com> - 0:1.5.1-3
- Remove Epoch tag.

* Wed Dec 08 2010 Ding-Yi Chen <dchen at redhat dot com> - 0:1.5.1-2
- Initial Fedora package.

