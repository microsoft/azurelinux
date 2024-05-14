Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global srcname justbytes

Name:           python-%{srcname}
Version:        0.11
Release:        12%{?dist}
Summary:        Library for handling computation with address ranges in bytes

License:        GPLv2+
URL:            https://pypi.python.org/pypi/justbytes
Source0:        https://pypi.io/packages/source/%(n=%{srcname}; echo ${n:0:1})/%{srcname}/%{srcname}-%{version}.tar.gz#/python-%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-pip

%global _description \
A library for handling computations with address ranges. The library also offers\
a configurable way to extract the representation of a value.

%description %{_description}

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-hypothesis
BuildRequires:  python3-justbases
BuildRequires:  python3-six
Requires:       python3-justbases
Requires:       python3-six

%description -n python3-%{srcname} %{_description}

Python 3 version.

%prep
%autosetup -n %{srcname}-%{version}
rm -rf justbytes.egg-info

%build
%py3_build

%install
%py3_install

%check
pip3 install pytest sortedcontainers
pip3 install .
py.test -v tests

%files -n python3-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/justbytes/
%{python3_sitelib}/justbytes-%{version}-*.egg-info/

%changelog
* Wed Apr 27 2022 Muhammad Falak <mwani@microsoft.com> - 0.11-12
- Drop BR on pytest & pip install latest deps
- Use `py.test` instead of `py.test-3` to enable ptest
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.11-11
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.11-9
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.11-8
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 17 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.11-5
- Subpackage python2-justbytes has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.11-3
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 08 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.11-1
- Update to 0.11

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.10-2
- Rebuild for Python 3.6

* Wed Aug 10 2016 mulhern <amulhern@redhat.com> - 0.10
- New release

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Mar 23 2016 mulhern <amulhern@redhat.com> - 0.6
- Initial release
