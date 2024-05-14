%{!?python3_sitearch: %define python3_sitearch %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}
%{!?__python3: %global __python3 /usr/bin/python3}
%{!?py3_build: %define py3_build CFLAGS="%{optflags}" %{__python3} setup.py build}
%{!?py3_install: %define py3_install %{__python3} setup.py install --skip-build --root %{buildroot}}

%global pypi_name pyrsistent

%global common_description %{expand:
Pyrsistent is a number of persistent collections (by some referred to as
functional data structures). Persistent in the sense that they are
immutable.

All methods on a data structure that would normally mutate it instead
return a new copy of the structure containing the requested updates. The
original structure is left untouched.}

Name:           python-%{pypi_name}
Summary:        Persistent/Functional/Immutable data structures
Version:        0.17.3
Release:        2%{?dist}
License:        MIT
URL:            https://github.com/tobgu/pyrsistent/
Vendor:         Microsoft
Distribution:   Azure Linux
Source0:        https://files.pythonhosted.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# relax dependencies specified in setup.py
Patch0:         00-relax-dependencies.patch
BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  python3-hypothesis
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-runner
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
BuildRequires:  python3-xml

%description %{common_description}

%package -n     python3-%{pypi_name}
Summary:        %{summary}

%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name} %{common_description}

%prep
%autosetup -n %{pypi_name}-%{version} -p1

# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%check
%{__python3} setup.py test

%files -n python3-%{pypi_name}
%doc README.rst
%license LICENCE.mit

%{python3_sitearch}/_pyrsistent_version.py
%{python3_sitearch}/__pycache__/*

%{python3_sitearch}/%{pypi_name}/
%{python3_sitearch}/pvectorc.cpython-3*.so
%{python3_sitearch}/%{pypi_name}-%{version}-py%{python3_version}.egg-info/

%changelog
* Thu Oct 22 2020 Steve Laughman <steve.laughman@microsoft.com> - 0.17.3-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT)

* Sun Sep 27 2020 José Lemos Neto <LemosJoseX@protonmail.com> - 0.17.3-1
- update to version 0.17.3

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 0.16.0-2
- Rebuilt for Python 3.9

* Tue Apr 14 2020 Fabio Valentini <decathorpe@gmail.com> - 0.16.0-1
- Update to version 0.16.0.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 10 2020 Fabio Valentini <decathorpe@gmail.com> - 0.15.7-1
- Update to version 0.15.7.

* Sun Nov 24 2019 Fabio Valentini <decathorpe@gmail.com> - 0.15.6-1
- Update to version 0.15.6.

* Thu Oct 31 2019 Fabio Valentini <decathorpe@gmail.com> - 0.15.5-1
- Update to version 0.15.5.

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.15.4-3
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 0.15.4-2
- Rebuilt for Python 3.8

* Fri Aug 02 2019 Fabio Valentini <decathorpe@gmail.com> - 0.15.4-1
- Update to version 0.15.4.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 08 2019 Fabio Valentini <decathorpe@gmail.com> - 0.15.3-1
- Update to version 0.15.3.

* Fri May 17 2019 Fabio Valentini <decathorpe@gmail.com> - 0.15.2-1
- Update to version 0.15.2.

* Fri Apr 26 2019 Fabio Valentini <decathorpe@gmail.com> - 0.15.1-1
- Update to version 0.15.1.

* Fri Feb 22 2019 Fabio Valentini <decathorpe@gmail.com> - 0.14.11-1
- Update to version 0.14.11.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Fabio Valentini <decathorpe@gmail.com> - 0.14.9-1
- Update to version 0.14.9.
- Enable the test suite.

* Thu Oct 11 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.14.2-6
- Python2 binary package has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.14.2-4
- Rebuilt for Python 3.7

* Mon Apr 16 2018 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.14.2-3
- add missing dist-tag

* Fri Apr 13 2018 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.14.2-2
- disable tests for now

* Thu Mar 01 2018 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.14.2-1
- new version 0.14.2

* Wed Sep 14 2016 Devrim Gündüz <devrim@gunduz.org> 0.11.13-2
- Fix packaging errors, that would own /usr/lib64 or so.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> 0.11.13-1
- Initial packaging for PostgreSQL YUM repository, to satisfy
  pgadmin4 dependency.
