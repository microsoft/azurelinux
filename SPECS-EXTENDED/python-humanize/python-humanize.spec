Vendor:         Microsoft Corporation
Distribution:   Mariner
%bcond_without check

Name:           python-humanize
Version:        0.5.1
Release:        23%{?dist}
Summary:        Turns dates in to human readable format, e.g '3 minutes ago'

License:        MIT
URL:            https://github.com/jmoiron/humanize
Source0:        %{url}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with check}
BuildRequires:  python3-mock
%endif


%global _description\
This modest package contains various common humanization utilities, like turning\
a number into a fuzzy human readable duration ('3 minutes ago') or into a human\
readable size or throughput.\


%description %_description

%package -n python3-humanize
Summary: %summary
%{?python_provide:%python_provide python3-humanize}

%description -n python3-humanize
This modest package contains various common humanization utilities, like turning
a number into a fuzzy human readable duration ('3 minutes ago') or into a human
readable size or throughput.

%prep
%setup -q -n humanize-%{version}

# Remove shebangs from libs.
for lib in humanize/time.py humanize/filesize.py humanize/number.py; do
 sed '1{\@^#!/usr/bin/env python@d}' $lib > $lib.new &&
 touch -r $lib $lib.new && mv $lib.new $lib
done

%build
%py3_build

%install
%py3_install

%find_lang humanize


%if %{with check}
%check
%{__python3} setup.py test
%endif

%files -n python3-humanize -f humanize.lang
%doc README.rst LICENCE
%dir %{python3_sitelib}/humanize
%{python3_sitelib}/humanize/*.py
%{python3_sitelib}/humanize/__pycache__
%{python3_sitelib}/humanize-%{version}-py%{python3_version}.egg-info
%dir %{python3_sitelib}/humanize/locale
%dir %{python3_sitelib}/humanize/locale/*
%dir %{python3_sitelib}/humanize/locale/*/LC_MESSAGES
%{python3_sitelib}/humanize/locale/*/LC_MESSAGES/*.mo
%exclude %{python3_sitelib}/humanize/locale/*/LC_MESSAGES/*.po

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.5.1-23
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 14 2019 Steve Traylen <steve.traylen@cern.ch> 0.5-21
- #1527195 - rpm own locale directories

* Thu Nov 14 2019 Steve Traylen <steve.traylen@cern.ch> 0.5-20
- #1527195 - rpm own locale directories

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.5.1-19
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 0.5.1-18
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.5.1-15
- Clean spec, remove python2 subpackage
- Run tests

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 16 2018 Miro Hrončok <mhroncok@redhat.com> - 0.5.1-13
- Rebuilt for Python 3.7

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.5.1-12
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Dec 07 2017 Merlin Mathesius <mmathesi@redhat.com> - 0.5.1-10
- Cleanup spec file conditionals

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.5.1-9
- Python 2 binary package renamed to python2-humanize
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.5.1-6
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 06 2015 Robert Kuska <rkuska@redhat.com> - 0.5.1-3
- Rebuilt for Python3.5 rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 1 2015 Steve Traylen <steve.traylen@cern.ch> 0.5.1-1
- New 0.5.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed May 14 2014 Steve Traylen <steve.traylen@cern.ch> 0.5-4
- lang fixes for .el6 target.

* Wed Apr 23 2014 Steve Traylen <steve.traylen@cern.ch> 0.5-3
- Use __python2 rather than __python throughout. - rhbz#1088882

* Tue Apr 22 2014 Steve Traylen <steve.traylen@cern.ch> 0.5-2
- Add python3 package - rhbz#1088882.

* Thu Apr 17 2014 Steve Traylen <steve.traylen@cern.ch> 0.5-1
- First release

