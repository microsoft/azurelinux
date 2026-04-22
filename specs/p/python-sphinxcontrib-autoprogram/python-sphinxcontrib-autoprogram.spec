# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name sphinxcontrib-autoprogram
%global pypi_shortname autoprogram

Name:           python-%{pypi_name}
Version:        0.1.9
Release: 12%{?dist}
Summary:        Sphinx extension for documenting CLI programs

License:        LicenseRef-Callaway-BSD
URL:            https://sphinxcontrib-autoprogram.readthedocs.io/en/stable/
Source0:        https://github.com/sphinx-contrib/%{pypi_shortname}/archive/refs/tags/%{version}.tar.gz
Patch0:         python-sphinxcontrib-autoprogram-test.patch

BuildArch:      noarch

BuildRequires:  python3-sphinx

BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-six

%generate_buildrequires
%pyproject_buildrequires -t

%description
This extension provides an automated way to document CLI programs.
It scans ArgumentParser objects and then expands it into a set of
program and option directives.


%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

Requires:       python3-sphinx >= 1.2
Requires:       python3-six
%description -n python3-%{pypi_name}
This extension provides an automated way to document CLI programs.
It scans ArgumentParser objects and then expands it into a set of
program and option directives.

%prep
%autosetup -p 1 -n %{pypi_shortname}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install.
%py3_install


%check
%{py3_test_envvars} %{python3} -m unittest -v sphinxcontrib.autoprogram.suite

%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/sphinxcontrib
%{python3_sitelib}/sphinxcontrib_autoprogram-%{version}-py%{python3_version}-nspkg.pth
%{python3_sitelib}/sphinxcontrib_autoprogram-%{version}-py%{python3_version}.egg-info

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.1.9-11
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.1.9-10
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.1.9-8
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Dec 05 2024 Romain Geissler <romain.geissler@amadeus.com> - 0.1.9-6
- Remove python3-zombie-imp dependency as upstream no longer uses it

* Wed Dec 04 2024 mh <mh+fedora@scrit.ch> <msuchy@redhat.com> - 0.1.9-5
- Fix working with newer setuptools (bz#2319720)
- Adapt to correct licens


* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 0.1.9-4
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.1.9-2
- Rebuilt for Python 3.13

* Fri Mar 15 2024 mh <mh+fedora@scrit.ch> - 0.1.9-1
- Update to 0.1.9 (#2169100)

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 07 2023 mh <mh+fedora@scrit.ch> - 0.1.8-1
- Update to 0.1.8 (#2169100)
- remove the upstreamed patch for argparse
- Require python3-zombie-imp as a stopgap to workaround #2220964

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 0.1.7-8
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.1.7-5
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.1.7-2
- Rebuilt for Python 3.10

* Wed Feb 10 2021 mh <mh+fedora@scrit.ch> - 0.1.7-1
- Update to 0.1.7 (#1578601)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.1.5-11
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.1.5-9
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.1.5-8
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 12 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.1.5-5
- Python2 binary package has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.1.5-3
- Rebuilt for Python 3.7

* Thu May 17 2018 mh <mh+fedora@scrit.ch> - 0.1.5-1
- Update to latest upstream (#1578601)

* Sun Apr  1 2018 Tom Hughes <tom@compton.nu> - 0.1.4-1
- Update to 0.1.4 upstream release

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.1.3-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 20 2017 mh <mh+fedora@scrit.ch> - 0.1.3-1
- Update to latest upstream

* Fri Sep 09 2016 mh <mh+fedora@scrit.ch> - 0.1.2-1
- Initial package.

