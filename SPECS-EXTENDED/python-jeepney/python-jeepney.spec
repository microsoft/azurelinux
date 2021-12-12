Vendor:         Microsoft Corporation
Distribution:   Mariner
%global pypi_name jeepney

Name:           python-%{pypi_name}
Version:        0.4.3
Release:        2%{?dist}
Summary:        Low-level, pure Python DBus protocol wrapper
License:        MIT
URL:            https://gitlab.com/takluyver/jeepney
Source0:        %pypi_source
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-setuptools
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx_rtd_theme
BuildRequires:  python3-testpath

%description
This is a low-level, pure Python DBus protocol client. It has an I/O-free core,
and integration modules for different event loops.


%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
This is a low-level, pure Python DBus protocol client. It has an I/O-free core,
and integration modules for different event loops.


%prep
%autosetup -n %{pypi_name}-%{version}

%build
%py3_build

make -C docs SPHINXBUILD=sphinx-build-3 html
rm -rf docs/_build/html/{.buildinfo,_sources}

%install
%py3_install

%check
%{__python3} -m pytest -v

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst examples/ docs/_build/html/
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.4.3-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Mar  4 2020 Göran Uddeborg <goeran@uddeborg.se> - 0.4.3-1
- Upgrade to 0.4.3 (#1809631)

* Thu Feb 13 2020 Christopher Tubbs <ctubbsii@fedoraproject.org> - 0.4.2-1
- Upgrade to 0.4.2

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Sep 10 2019 Göran Uddeborg <goeran@uddeborg.se> - 0.4.1-1
- Upgrade to 0.4.1

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Sep 24 2018 Miro Hrončok <mhroncok@redhat.com> - 0.4-1
- Initial package
