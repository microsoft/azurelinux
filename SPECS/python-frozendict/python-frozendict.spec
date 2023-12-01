%global srcname frozendict
%global _description %{expand:
frozendict is an immutable wrapper around dictionaries that implements
the complete mapping interface. It can be used as a drop-in
replacement for dictionaries where immutability is desired.}
Summary:        An immutable dictionary
Name:           python-%{srcname}
Version:        2.3.0
Release:        1%{?dist}
License:        LGPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://pypi.python.org/pypi/frozendict
Source0:        https://github.com/Marco-Sulla/%{name}/releases/download/v%{version}/%{srcname}-%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  python3-pip
%endif

%description %{_description}

%package -n python3-%{srcname}
%{?python_provide:%python_provide python3-%{srcname}}
Summary:        %{summary}
Requires:       python3

%description -n python3-%{srcname} %{_description}

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install pytest
cd test
PYTHONPATH=%{buildroot}%{python3_sitelib} python3 -m pytest

%files -n python3-%{srcname}
%license LICENSE.txt
%doc README.md
%{python3_sitelib}/%{srcname}-*.egg-info/
%{python3_sitelib}/%{srcname}/

%changelog
* Mon Mar 14 2022 Olivia Crain <oliviacrain@microsoft.com> - 2.3.0-1
- Upgrade to latest version in forked repo
- Remove noarch specification (package now comes with a C extension)
- Add package test
- Remove upstreamed py39 compatibility patches
- Switch source from PyPI to GitHub

* Wed Jun 23 2021 Rachel Menge <rachelmenge@microsoft.com> - 1.2-19
- Initial CBL-Mariner import from Fedora 34 (license: MIT)
- License verified

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.2-16
- Rebuilt for Python 3.9

* Tue Feb  4 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.2-15
- Fix compatibility with python3.9 (#1797691)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2-13
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2-12
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2-9
- Subpackage python2-frozendict has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Wed Dec 26 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.2-8
- Enable python dependency generator

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.2-6
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 22 2016 Miro Hrončok <mhroncok@redhat.com> - 1.2-2
- Rebuild for Python 3.6

* Mon Dec 19 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.2-1
- Initial package
