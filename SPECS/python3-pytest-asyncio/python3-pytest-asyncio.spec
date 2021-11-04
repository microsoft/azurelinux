%global pypi_name pytest-asyncio
%global srcname pytest_asyncio
%global project_owner pytest-dev
%global github_name pytest-asyncio
%bcond_without  tests
Summary:        Pytest support for asyncio
Name:           python3-%{pypi_name}
Version:        0.14.0
Release:        3%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://pypi.python.org/pypi/pytest-asyncio
Source0:        https://github.com/%{project_owner}/%{github_name}/archive/v%{version}/%{github_name}-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildArch:      noarch
%if %{with_check}
BuildRequires:  python3-async-generator >= 1.3
BuildRequires:  python3-pip
%endif

%description
pytest-asyncio is an Apache2 licensed library, written in Python, for testing
asyncio code with pytest.

asyncio code is usually written in the form of coroutines, which makes it
slightly more difficult to test using normal testing tools. pytest-asyncio
provides useful fixtures and markers to make testing easier.

%prep
%setup -q -n %{github_name}-%{version}

# Don't treat all warnings as errors, there are DeprecationWarnings on 3.8
sed -i '/filterwarnings = error/d' setup.cfg

%build
%py3_build


%install
%py3_install


%if %{with tests}
%check
pip3 install atomicwrites>=1.3.0 \
    attrs>=19.1.0 \
    codecov>=2.0.15 \
    coverage>=4.5.3 \
    hypothesis==4.38.0 \
    more-itertools>=7.0.0 \
    pluggy>=0.11.0 \
    py>=1.8.0 \
    pytest-cov>=2.7.1 \
    pytest>=5.4.0 \
    six>=1.12.0 \
    uvloop>=0.14.0
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python3_sitelib} \
    python%{python3_version} -m pytest -v
%endif


%files
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{srcname}-%{version}-py%{python3_version}.egg-info/
%{python3_sitelib}/%{srcname}/

%changelog
* Mon Jun 21 2021 Rachel Menge <rachelmenge@microsoft.com> - 0.14.0-3
- Initial CBL-Mariner import from Fedora 34 (license: MIT)
- License verified

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 08 2020 Miro Hrončok <mhroncok@redhat.com> - 0.14.0-1
- Update to 0.14.0
- Fixes rhbz#1826108

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 25 2020 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-6
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Apr 18 2019 Carl George <carl@george.computer> - 0.10.0-1
- Latest upstream
- Run test suite

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Aug 01 2018 Julien Enselme <jujens@jujens.eu> - 0.9.0-1
- Update to 0.9.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-4.git18535c3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.8.0-3.git18535c3
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-2.git18535c3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Sep 26 2017 <jujens@jujens.eu> - 0.8.0-1.git18535c3
- Update to 0.8.0

* Thu Sep 14 2017 <jujens@jujens.eu> - 0.7.0-1.git2407487
- Update to 0.7.0

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2.git72a6c2b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 30 2017 Julien Enselme <jujens@jujens.eu> - 0.6.0-1.git72a6c2b
- Update to 0.6.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-4.git917d8a8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.5.0-3.git917d8a8
- Rebuild for Python 3.6

* Mon Oct 10 2016 Julien Enselme <jujens@jujens.eu> - 0.5.0-2.git917d8a8
- Bump version

* Wed Sep 07 2016 Julien Enselme <jujens@jujens.eu> - 0.5.0-1.git917d8a8
- Update to 0.5.0

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-2.git64b79e1
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sun Jun 05 2016 Julien Enselme <jujens@jujens.eu> - 0.4.1-1.git64b79e1
- Update to 0.4.1

* Wed Jun 01 2016 Julien Enselme <jujens@jujens.eu> - 0.4.0-1.gitb4a4bf8
- Update to 0.4.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-2.gitae9b430
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Dec 20 2015 Julien Enselme <jujens@jujens.eu> - 0.3.0-1.gitae9b430
- Update to 0.3.0 (bz:1293083)

* Thu Nov 5 2015 Julien Enselme <jujens@jujens.eu> - 0.1.3-3.git2a4c7e6
- Rebuilt for python 3.5

* Sun Aug 2 2015 Julien Enselme <jujens@jujens.eu> - 0.1.3-2.git2a4c7e6
- Add %%python_provide

* Sat Aug 1 2015 Julien Enselme <jujens@jujens.eu> - 0.1.3-1.git2a4c7e6
- Initial package
