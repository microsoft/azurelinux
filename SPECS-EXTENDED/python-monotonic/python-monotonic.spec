Vendor:         Microsoft Corporation
Distribution:   Mariner
%global pypi_name monotonic


Name:           python-%{pypi_name}
Version:        1.5
Release:        7%{?dist}
Summary:        An implementation of time.monotonic() for Python 2 & < 3.3

# Missing license file from source package
# https://github.com/atdt/monotonic/pull/4
License:        ASL 2.0
URL:            https://github.com/atdt/%{pypi_name}
Source0:        https://files.pythonhosted.org/packages/source/m/%{pypi_name}/%{pypi_name}-%{version}.tar.gz#/python-%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch


%global _description\
This module provides a ``monotonic()`` function which\
returns the\
value (in fractional seconds) of a clock which never goes\
backwards.\
\
On Python 3.3 or newer, ``monotonic`` will be an alias of\
``time.monotonic`` from the standard library. On older versions,\
it will fall back to an equivalent platform specific implementation.\


%description %_description

%package -n python3-%{pypi_name}
Summary:        An implementation of time.monotonic() for Python 2 & < 3.3

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description -n python3-%{pypi_name}
This module provides a ``monotonic()`` function which
returns the
value (in fractional seconds) of a clock which never goes
backwards.

On Python 3.3 or newer, ``monotonic`` will be an alias of
``time.monotonic`` from the standard library. On older versions,
it will fall back to an equivalent platform specific implementation.


%prep
%autosetup -n %{pypi_name}-%{version}


%build

%py3_build


%install

%py3_install


%files -n python3-%{pypi_name}
%license LICENSE
%{python3_sitelib}/__pycache__/%{pypi_name}.*
%{python3_sitelib}/%{pypi_name}.py
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info/

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Sep 26 2019 Miro Hrončok <mhroncok@redhat.com> - 1.5-5
- Subpackage python2-monotonic has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.5-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 20 2018 Alfredo Moralejo <amoralej@redhat.com> - 1.5-1
- Update to version 1.5.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.2-10
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.2-8
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.2-7
- Python 2 binary package renamed to python2-monotonic
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.2-4
- Rebuild for Python 3.6

* Mon Aug 29 2016 Matthias Runge <mrunge@redhat.com> - 1.2-1
- update to 1.2, modernize packaging

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 19 2016 Alan Pevec <alan.pevec@redhat.com> 0.5-1
- Update to 0.5

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Aug 18 2015 Alan Pevec <alan.pevec@redhat.com> 0.3-1
- Update to upstream 0.3

* Thu Jun 18 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 0.1-1
- Initial package
