Vendor:         Microsoft Corporation
Distribution:   Mariner
%global pypi_name importlib_metadata
%global pkg_name  importlib-metadata

Name:           python-%{pkg_name}
Version:        0.23
Release:        2%{?dist}
Summary:        Read metadata from Python packages

License:        ASL 2.0
URL:            http://importlib-metadata.readthedocs.io/
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-packaging
BuildRequires:  python3-zipp >= 0.5

%description
importlib_metadata is a library which provides an API for accessing an
installed package’s metadata, such as its entry points or its top-level name.
This functionality intends to replace most uses of pkg_resources entry point
API and metadata API. Along with importlib.resources in Python 3.7 and newer
(backported as importlib_resources for older versions of Python), this can
eliminate the need to use the older and less efficient pkg_resources package.


%package -n     python3-%{pkg_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pkg_name}}

%description -n python3-%{pkg_name}
importlib_metadata is a library which provides an API for accessing an
installed package’s metadata, such as its entry points or its top-level name.
This functionality intends to replace most uses of pkg_resources entry point
API and metadata API. Along with importlib.resources in Python 3.7 and newer
(backported as importlib_resources for older versions of Python), this can
eliminate the need to use the older and less efficient pkg_resources package.


%prep
%autosetup -n %{pypi_name}-%{version}

%build
%py3_build

%install
%py3_install

# Don't ship docs sources
rm -r %{buildroot}/%{python3_sitelib}/%{pypi_name}/docs/

%check
%{__python3} setup.py test

%files -n python3-%{pkg_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info/

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.23-2
- Initial CBL-Mariner import from Fedora 31 (license: MIT).

* Wed Sep 18 2019 Miro Hrončok <mhroncok@redhat.com> - 0.23-1
- Update to 0.23

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 26 2019 Miro Hrončok <mhroncok@redhat.com> - 0.18-1
- Initial package
