%global pypi_name pluggy
%global _description\
The plugin manager stripped of pytest specific details.

Summary:        The plugin manager stripped of pytest specific details
Name:           python-pluggy
Version:        1.3.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/pytest-dev/pluggy
Source0:        https://pypi.python.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
%if %{with_check}
BuildRequires:  python3-atomicwrites
BuildRequires:  python3-attrs
BuildRequires:  python3-pytest
%endif

%description %{_description}

%package -n python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name}
The plugin manager stripped of pytest specific details.

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install more-itertools

# TODO investigate test_load_setuptools_instantiation failure
PYTHONPATH=%{buildroot}%{python3_sitelib} python3 -m pytest testing -k "not test_load_setuptools_instantiation"

%files -n python3-%{pypi_name}
%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info/
%doc README.rst
%license LICENSE

%changelog
* Tue Jan 23 2024 Andrew Phelps <anphel@microsoft.com> - 1.3.0-1
- Upgrade to version 1.3.0

* Mon Mar 28 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.0-3
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified.

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Aug 27 2021 Matthias Runge <mrunge@redhat.com> - 1.0.0-1
- update to 1.0.0 (rhbz#1997706)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 0.13.1-5
- Rebuilt for Python 3.10

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 0.13.1-4
- Bootstrap for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 05 2020 Matthias Runge <mrunge@redhat.com> - 0.13.1-1
- update to 0.13.1

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 0.13.0-4
- Rebuilt for Python 3.9

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 0.13.0-3
- Bootstrap for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 18 2019 Patrik Kopkan <pkopkan@redhat.com> - 0.13.0-1
- Update to 0.13.0 (#1750961)

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.12.0-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 0.12.0-4
- Rebuilt for Python 3.8

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 0.12.0-3
- Bootstrap for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 26 2019 Miro Hrončok <mhroncok@redhat.com> - 0.12.0-1
- Update to 0.12.0 (#1714369)
- Move python2-pluggy to a separate package

* Tue May 14 2019 Thomas Moschny <thomas.moschny@gmx.de> - 0.11.0-1
- Update to 0.11.0.

* Tue Mar 12 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.0-1
- Update to 0.9.0 (#1680414)

* Fri Feb 08 2019 Alfredo Moralejo <amoralej@redhat.com> - 0.8.1-1
- Update to 0.8.1.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 11 2018 Thomas Moschny <thomas.moschny@gmx.de> - 0.8.0-1
- Update to 0.8.0.

* Sat Oct  6 2018 Thomas Moschny <thomas.moschny@gmx.de> - 0.7.1-1
- Update to 0.7.1.
- Update BRs.
- Use source URL to released archive containing pluggy/_version.py.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 14 2018 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-4
- Rebuilt for Python 3.7

* Thu Jun 14 2018 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-3
- Bootstrap for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 29 2018 Matthias Runge <mrunge@redhat.com> - 0.6.0-1
- update to 0.6.0
- requirement renames to meet python2 names

* Tue Jan 23 2018 Karsten Hopp <karsten@redhat.com> - 0.3.1-10
- fix conditional

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.3.1-9
- Python 2 binary package renamed to python2-pluggy
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.3.1-6
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 16 2015 Matthias Runge <mrunge@redhat.com> - 0.3.1-3
- make tests pass again on Python 3.5

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Sep 21 2015 Matthias Runge <mrunge@redhat.com> - 0.3.1-1
- update to 0.3.1

* Tue Aug 25 2015 Matthias Runge <mrunge@redhat.com> - 0.3.0-3
- fix python3 builds

* Fri Aug 21 2015 Matthias Runge <mrunge@redhat.com> - 0.3.0-2
- add python2_sitelib macros and BR to setuptools (rhbz#1254484)

* Fri Aug 14 2015 Matthias Runge <mrunge@redhat.com> - 0.3.0-1
- version based on the inital proposal of Adam Young
