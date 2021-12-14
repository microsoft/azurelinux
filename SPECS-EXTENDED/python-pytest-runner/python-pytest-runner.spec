%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}
%{!?__python3: %global __python3 /usr/bin/python3}
%{!?py3_build: %define py3_build CFLAGS="%{optflags}" %{__python3} setup.py build}
%{!?py3_install: %define py3_install %{__python3} setup.py install --skip-build --root %{buildroot}}

%global modulename pytest-runner
%global _modulename pytest_runner

Summary:        Invoke py.test as distutils command with dependency resolution
Name:           python-%{modulename}
Version:        4.0
Release:        12%{?dist}
License:        MIT
URL:            https://pypi.python.org/pypi/pytest-runner
Vendor:         Microsoft
Distribution:   Mariner
# setuptools-scm requires a pypi tarball and doesn't like github tarball
Source0:        https://files.pythonhosted.org/packages/source/p/%{modulename}/%{modulename}-%{version}.tar.gz
BuildArch:      noarch

%global _description \
Setup scripts can use pytest-runner to add setup.py test support for pytest runner.

%description %{_description}

%package -n python3-%{modulename}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{modulename}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-pytest
Requires:       python3-pytest

%description -n python3-%{modulename} %{_description}

Python 3 version.

%prep
%autosetup -n %{modulename}-%{version}

%build
%py3_build

%install
%py3_install

%check
%{__python3} setup.py test

%files -n python3-%{modulename}
%doc README.rst
%license LICENSE
%{python3_sitelib}/ptr.py
%{python3_sitelib}/%{_modulename}-%{version}-py%{python3_version}.egg-info/
%{python3_sitelib}/__pycache__/ptr.*

%changelog
* Thu Oct 22 2020 Steve Laughman <steve.laughman@microsoft.com> - 4.0-12
- Initial CBL-Mariner import from Fedora 33 (license: MIT)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 4.0-10
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 29 2019 Miro Hrončok <mhroncok@redhat.com> - 4.0-8
- Subpackage python2-pytest-runner has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 4.0-7
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 4.0-6
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 4.0-2
- Rebuilt for Python 3.7

* Sun Feb 11 2018 Vadim Rutkovsky <vrutkovs@redhat.com> - 4.0-1
- Update to 4.0 (#1544167)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Nov 03 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.0-2
- Fix broken dep

* Thu Nov 02 2017 Vadim Rutkovsky  <vrutkovs@redhat.com> - 3.0-1
- Update to 3.0 (#1508216)

* Fri Oct 13 2017 Vadim Rutkovsky <vrutkovs@redhat.com> - 2.12.1-1
-  Update to 2.12.1 (#1487972)

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 2.9-6
- Cleanup spec file conditionals

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Mar 9 2017 Orion Poplawski <orion@cora.nwra.com> - 2.9-4
- Build python 3 version for EPEL

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 2.9-2
- Rebuild for Python 3.6

* Sat Aug 06 2016 Vadim Rutkovsky <vrutkovs@redhat.com> - 2.9-1
- Initial package
