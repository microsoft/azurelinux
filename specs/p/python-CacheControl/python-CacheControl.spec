# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name CacheControl
%global pypi_name_lower cachecontrol

%global common_description %{expand:
CacheControl is a port of the caching algorithms in httplib2 for use with
requests session object. It was written because httplib2's better support
for caching is often mitigated by its lack of thread safety. The same is
true of requests in terms of caching.}

Name:           python-%{pypi_name}
Summary:        httplib2 caching for requests
Version:        0.14.3
Release: 6%{?dist}
License:        MIT

URL:            https://github.com/ionrock/cachecontrol
Source0:        %{url}/archive/v%{version}/%{pypi_name_lower}-%{version}.tar.gz

BuildArch:      noarch

%description %{common_description}


%package -n     python3-%{pypi_name}
Summary:        httplib2 caching for requests

BuildRequires:  python3-devel
BuildRequires:  python3-cherrypy
BuildRequires:  python3-pytest

Recommends:  python3-%{pypi_name}+filecache
Recommends:  python3-%{pypi_name}+redis

%description -n python3-%{pypi_name} %{common_description}

%pyproject_extras_subpkg -n python3-%{pypi_name} filecache redis

%prep
%autosetup -n %{pypi_name_lower}-%{version} -p1


%generate_buildrequires
%pyproject_buildrequires -x filecache,redis


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files cachecontrol


%check
%pytest


%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.rst
%license LICENSE.txt

%{_bindir}/doesitcache


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.14.3-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.14.3-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.14.3-2
- Rebuilt for Python 3.14

* Sat May 03 2025 Romain Geissler <romain.geissler@amadeus.com> - 0.14.3-1
- Update to 0.14.3
- Fixes: rhbz#2363147

* Fri Mar 14 2025 Romain Geissler <romain.geissler@amadeus.com> - 0.14.2-1
- Update to 0.14.2
- Fixes: rhbz#2336159

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Nov 05 2024 Tomáš Hrnčiar <thrnciar@redhat.com> - 0.14.1-1
- Update to 0.14.1
- Fixes: rhbz#2323813

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 0.14.0-2
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Sep 04 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 0.13.1-1
- Update to 0.13.1
- Fixes: rhbz#2126334

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jul 01 2023 Python Maint <python-maint@redhat.com> - 0.12.11-5
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 0.12.11-2
- Rebuilt for Python 3.11

* Mon May 09 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 0.12.11-1
- Update to 0.12.11
- Fixes: rhbz#2077079

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 13 2021 Tomáš Hrnčiar <thrnciar@redhat.com> - 0.12.10-1
- Update to 0.12.10

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.12.6-8
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Miro Hrončok <mhroncok@redhat.com> - 0.12.6-5
- Add cachecontrol[filecache] and cachecontrol[redis] subpackages

* Fri Jun 05 2020 Miro Hrončok <mhroncok@redhat.com> - 0.12.6-4
- Rebuilt with cherrypy tests

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.12.6-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Dec 22 2019 Fabio Valentini <decathorpe@gmail.com> - 0.12.6-1
- Update to version 0.12.6.

* Fri Dec 13 2019 Fabio Valentini <decathorpe@gmail.com> - 0.12.5-7
- Recommend optional dependencies.

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.12.5-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Tue Aug 20 2019 Fabio Valentini <decathorpe@gmail.com> - 0.12.5-5
- Port to pytest >=4.0.

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.12.5-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug 16 2018 Miro Hrončok <mhroncok@redhat.com> - 0.12.5-1
- Update to 0.12.5
- Remove python2 subpackage

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.12.3-5
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 15 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.12.3-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Sep 13 2017 Iryna Shcherbina <ishcherb@redhat.com> - 0.10.0-2
- Fix Python 2 dependency from python3-CacheControl (rhbz#1490893)

* Wed Aug 23 2017 Tomas Krizek <tkrizek@redhat.com> - 0.12.3-1
- Update to 0.12.3

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.11.5-8
- Python 2 binary package renamed to python2-cachecontrol
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.11.5-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.5-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.5-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Jun 19 2015 Slavek Kabrda <bkabrda@redhat.com> - 0.11.5-1
- Update to 0.11.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 04 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.10.1-1
- Initial package.

