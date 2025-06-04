Name:           python-varlink
Version:        31.0.0
Release:        12%{?dist}
Summary:        Python implementation of Varlink
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/varlink/%{name}
Source0: 	https://files.pythonhosted.org/packages/e6/90/172069117da79f1b62a29417dac7c7e544dda82bfb28af18167d1fb3aaaf/varlink-%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-rpm-macros
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm

%global _description \
An python module for Varlink with client and server support.

%description %_description

%package -n python3-varlink
Summary:       %summary
%{?python_provide:%python_provide python3-varlink}
# The varlink copr had this package under the "python-varlink"
# name. Add Obsoletes to make it easy to upgrade.
Obsoletes:     python-varlink <= 3-1.git.61.1bc637d.fc27

%description -n python3-varlink %_description

%prep
%autosetup -n varlink-%{version}
# varlink also supports python-2.7 but python3 is required here
sed -i -e 's#env python#env python3#' varlink/tests/test_certification.py
# varlink also supports python-2.7 but python3 is required here
sed -i -e 's#env python#env python3#' varlink/tests/test_orgexamplemore.py

%build
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%py3_build

%check
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
CFLAGS="%{optflags}" %{__python3} %{py_setup} %{?py_setup_args} check

%install
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%py3_install

%files -n python3-varlink
%license LICENSE.txt
%doc README.md
%{python3_sitelib}/*

%changelog
* Tue Dec 24 2024 Akhila Guruju <v-guakhila@microsoft.com> - 31.0.0-12
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 31.0.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 31.0.0-10
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 31.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 31.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 31.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 31.0.0-6
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 31.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 31.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 31.0.0-3
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 31.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 07 2021 Harald Hoyer <harald@hoyer.xyz> - 31.0.0-1
- Update to 31.0.0

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 30.3.1-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 30.3.1-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 30.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Oct 02 2020 Harald Hoyer <harald@redhat.com> - 30.3.1-1
- Update to 30.3.1

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 30.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Harald Hoyer <harald@redhat.com> - 30.3.0-1
- add python3-setuptools to BuildRequires
- add python3-setuptools_scm to BuildRequires
- Update to 30.3.0

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 29.0.0-7
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 29.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 29.0.0-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 29.0.0-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 29.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 29.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 10 2018 Harald Hoyer <harald@redhat.com> - 29.0.0-1
- fixed interface name grammar

* Mon Oct 08 2018 Harald Hoyer <harald@redhat.com> - 28.0.0-1
- python-varlink-28.0.0-1
- fixed grammar

* Mon Aug 06 2018 Harald Hoyer <harald@redhat.com> - 27.1.1-1
- python-varlink-27.1.1-1
- fixed varlink.cli bridge

* Fri Jul 20 2018 Harald Hoyer <harald@redhat.com> - 27.1.0-1
+ python-varlink-27.1.0-1
- add "varlink.cli bridge" support

* Fri Jul 20 2018 Harald Hoyer <harald@redhat.com> - 27.0.0-1
- python-varlink-27.0.0-1

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 26.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 26.1.0-2
- Rebuilt for Python 3.7

* Thu Jun 14 2018 Harald Hoyer <harald@redhat.com> - 26.1.0-1
- python-varlink 26.1.0

* Fri May 25 2018 Harald Hoyer <harald@redhat.com> - 26.0.2-1
- python-varlink 26.0.2

* Mon May 14 2018 Harald Hoyer <harald@redhat.com> - 26-1
- python-varlink 26

* Fri May 11 2018 Harald Hoyer <harald@redhat.com> - 25-1
- python-varlink 25

* Mon May 07 2018 Harald Hoyer <harald@redhat.com> - 23-1
- python-varlink 23

* Wed Apr 25 2018 Harald Hoyer <harald@redhat.com> - 22-1
- python-varlink-22

* Wed Apr 18 2018 Harald Hoyer <harald@redhat.com> - 19-1
- python-varlink 19

* Thu Apr 12 2018 Harald Hoyer <harald@redhat.com> - 18-1
- python-varlink 18

* Wed Apr 11 2018 Harald Hoyer <harald@redhat.com> - 17-1
- python-varlink 17

* Fri Mar 23 2018 Harald Hoyer <harald@redhat.com> - 15-1
- python-varlink 15

* Mon Mar 19 2018 Harald Hoyer <harald@redhat.com> - 14-1
- python-varlink 14

* Mon Feb 26 2018 Harald Hoyer <harald@redhat.com> - 13-1
- python-varlink 13

* Wed Feb 14 2018 Harald Hoyer <harald@redhat.com> - 12-1
- python-varlink 12

* Fri Feb 09 2018 Harald Hoyer <harald@redhat.com> - 11-1
- python-varlink 11

* Fri Feb 09 2018 Harald Hoyer <harald@redhat.com> - 10-1
- python-varlink 10

* Fri Feb 09 2018 Harald Hoyer <harald@redhat.com> - 9-1
- python-varlink 9

* Thu Feb 08 2018 Harald Hoyer <harald@redhat.com> - 8-1
- python-varlink 8

* Thu Feb 08 2018 Harald Hoyer <harald@redhat.com> - 7-1
- python-varlink 7

* Thu Feb 08 2018 Harald Hoyer <harald@redhat.com> - 4-1
- python-varlink 4

* Fri Feb 02 2018 Harald Hoyer <harald@redhat.com> - 3-2
- bump release

* Fri Feb  2 2018 Harald Hoyer <harald@redhat.com> - 3-1
- python-varlink 3

* Thu Dec 14 2017 Harald Hoyer <harald@redhat.com> - 2-1
- python-varlink 2

* Tue Aug 29 2017 <info@varlink.org> 1-1
- python-varlink 1
