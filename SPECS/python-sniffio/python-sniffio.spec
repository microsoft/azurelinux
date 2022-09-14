%global pypi_name sniffio

%global _description \
You're writing a library.  You've decided to be ambitious, and support multiple\
async I/O packages, like Trio, and asyncio, and ... You've written a bunch of\
clever code to handle all the differences.  But... how do you know which piece\
of clever code to run?  This is a tiny package whose only purpose is to let you\
detect which async library your code is running under.

Summary:        Sniff out which async library your code is running under
Name:           python-%{pypi_name}
Version:        1.3.0
Release:        1%{?dist}
License:        MIT or ASL 2.0
URL:            https://github.com/python-trio/sniffio
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%description %{_description}

%package -n python3-%{pypi_name}
Summary:        %{summary}
BuildRequires:  python3-curio
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
%endif
Requires:       python3

%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

%description -n python3-%{pypi_name} %{_description}

%prep
%autosetup -n %{pypi_name}-%{version}
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%check
%{python3} -m pip install -r test-requirements.txt
mkdir empty
cd empty
%pytest -W error -ra -v --pyargs sniffio --cov=sniffio --cov-config=../.coveragerc --verbose

%files -n python3-%{pypi_name}
%license LICENSE LICENSE.MIT LICENSE.APACHE2
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info

%changelog
* Wed Sep 14 2022 Sumedh Sharma <sumsharma@microsoft.com> - 1.3.0-1
- Move from SPECS-EXTENDED to SPECS
- Bump up version to 1.3.0
- License verified

* Fri Apr 29 2022 Muhamamd Falak <mwani@microsoft.com> - 1.1.0-11
- Drop BR on pytest & pip install latest deps
- Use `py.test` instead of `py.test-3` to enable ptest

* Tue Apr 26 2022 Mandeep Plaha <mandeepplaha@microsoft.com> - 1.1.0-10
- Updated source URL
- License verified

* Tue Jan 12 2021 Steve Laughman <steve.laughman@microsoft.com> - 1.1.0-9
- Correction to files declaration

* Tue Dec 08 2020 Steve Laughman <steve.laughman@microsoft.com> - 1.1.0-8
- Initial CBL-Mariner import from Fedora 33 (license: MIT)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-6
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 14 2019 Carl George <carl@george.computer> - 1.1.0-1
- Latest upstream

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Sep 12 2018 Carl George <carl@george.computer> - 1.0.0-1
- Initial package
