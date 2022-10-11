Vendor:         Microsoft Corporation
Distribution:   Mariner
%global pypi_name poetry

%global common_description %{expand:
Poetry helps you declare, manage and install dependencies of Python
projects, ensuring you have the right stack everywhere.}

Name:           %{pypi_name}
Summary:        Python dependency management and packaging made easy
Version:        1.1.9
Release:        1%{?dist}
License:        MIT

URL:            https://poetry.eustace.io/
Source0:        %{pypi_source}

# relax some too-strict dependencies that are specified in setup.py:
# - importlib-metadata (either removed or too old in fedora)
# - keyring (too new in fedora, but should be compatible)
# - pyrsistent (too new in fedora, but should be compatible)
# - requests-toolbelt (too new in fedora, but should be compatible)
Patch0:         00-setup-requirements-fixes.patch

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

Requires:       python3-%{pypi_name} = %{version}-%{release}

%description %{common_description}


%package -n     python3-%{pypi_name}
Summary:        %{summary}

# this is an optional dependency of CacheControl, but it's required by poetry
Requires:       python3dist(lockfile)

%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name} %{common_description}


%prep
%autosetup -p1


%build
%py3_build


%install
%py3_install


%files
%license LICENSE
%doc README.md

%{_bindir}/poetry

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.md

%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info/


%changelog
* Tue Oct 11 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.9-1
- Upgrade to 1.1.9

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.10-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jul 22 2020 Fabio Valentini <decathorpe@gmail.com> - 1.0.10-1
- Update to version 1.0.10.

* Sat Jul 04 2020 Fabio Valentini <decathorpe@gmail.com> - 1.0.9-1
- Update to version 1.0.9.
- Drop manual dependency generator enablement (it's enabled by default).

* Sat Feb 29 2020 Fabio Valentini <decathorpe@gmail.com> - 1.0.5-1
- Update to version 1.0.5.

* Fri Feb 28 2020 Fabio Valentini <decathorpe@gmail.com> - 1.0.4-1
- Update to version 1.0.4.

* Wed Feb 05 2020 Fabio Valentini <decathorpe@gmail.com> - 1.0.3-2
- Hard-code dependency on python3-lockfile.

* Sun Feb 02 2020 Fabio Valentini <decathorpe@gmail.com> - 1.0.3-1
- Update to version 1.0.3.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 15 2020 Fabio Valentini <decathorpe@gmail.com> - 1.0.2-1
- Update to version 1.0.2.

* Fri Dec 13 2019 Fabio Valentini <decathorpe@gmail.com> - 1.0.0-1
- Update to version 1.0.0.

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.12.17-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 26 2019 Fabio Valentini <decathorpe@gmail.com> - 0.12.17-4
- Relax dependency on cachy.

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.12.17-3
- Rebuilt for Python 3.8

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.12.17-2
- Add missing dependencies on lockfile and pip

* Sat Aug 10 2019 Fabio Valentini <decathorpe@gmail.com> - 0.12.17-1
- Update to version 0.12.17.

* Fri May 03 2019 Fabio Valentini <decathorpe@gmail.com> - 0.12.15-1
- Update to version 0.12.15.

* Fri Apr 26 2019 Fabio Valentini <decathorpe@gmail.com> - 0.12.14-1
- Update to version 0.12.14.

* Fri Apr 26 2019 Fabio Valentini <decathorpe@gmail.com> - 0.12.13-1
- Update to version 0.12.13.

* Fri Apr 12 2019 Fabio Valentini <decathorpe@gmail.com> - 0.12.12-1
- Update to version 0.12.12.

* Mon Jan 14 2019 Fabio Valentini <decathorpe@gmail.com> - 0.12.11-1
- Update to version 0.12.11.

* Wed Dec 12 2018 Fabio Valentini <decathorpe@gmail.com> - 0.12.10-1
- Initial package.

