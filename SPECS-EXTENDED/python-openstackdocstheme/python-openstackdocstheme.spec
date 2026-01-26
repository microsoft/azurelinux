Vendor:         Microsoft Corporation
Distribution:   Azure Linux

%global pypi_name openstackdocstheme

Name:           python-%{pypi_name}
Version:        3.0.0
Release:        9%{?dist}
Summary:        OpenStack Docs Theme

License:        Apache-2.0
URL:            https://docs.openstack.org/
Source0:        %{pypi_source}#/%{name}-%{version}.tar.gz
Patch0001:      0001-Remove-all-Google-Analytics-tracking.patch
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-sphinx
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
BuildRequires:  python3-dulwich
BuildRequires:  python3-pip
BuildRequires:  python3-extras
BuildRequires:  git-core
BuildRequires:  python3dist(wheel)

%global common_desc \
OpenStack docs.openstack.org Sphinx Theme\
\
Theme and extension support for Sphinx documentation that is published to\
docs.openstack.org. Intended for use by OpenStack projects.

%description
%{common_desc}


%package -n     python3-%{pypi_name}
Summary:        OpenStack Docs Theme
%{?python_provide:%python_provide python3-%{pypi_name}}
Provides:       bundled(js-jquery)

Requires: python3-sphinx >= 1.6.2
Requires: python3-babel

%description -n python3-%{pypi_name}
%{common_desc}

%package -n     python-%{pypi_name}-doc
Summary:        openstackdocstheme documentation
%description -n python-%{pypi_name}-doc
Documentation for openstackdocstheme


%generate_buildrequires
%pyproject_buildrequires


%prep
%autosetup -n %{pypi_name}-%{version} -p1 -S git
# Make sure there is no Google Analytics
sed -i 's/analytics_tracking_code.*/analytics_tracking_code\ =/' openstackdocstheme/theme/openstackdocs/theme.conf
# Prevent doc build warnings from causing a build failure
sed -i '/warning-is-error/d' setup.cfg

%build
%pyproject_wheel

export PYTHONPATH=.
sphinx-build -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
rm -f doc/build/html/_static/images/docs/license.png

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.rst
%license LICENSE
%{_bindir}/docstheme-build-pdf
%{_bindir}/docstheme-build-translated.sh
%{_bindir}/docstheme-lang-display-name.py

%files -n python-%{pypi_name}-doc
%doc doc/build/html

%changelog
* Wed Feb 19 2025 Archana Shettigar <v-shettigara@microsoft.com> - 3.0.0-9
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 3.0.0-7
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 3.0.0-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Aug 04 2022 Joel Capitao <jcapitao@redhat.com> - 3.0.0-1
- Update to latest release (rhbz#1672986)
- Take advantage of DynamicBuildRequires

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.3.0-5
- Rebuilt for Python 3.11

* Thu Jan 27 2022 Joel Capitao <jcapitao@redhat.com> - 2.3.0-4
- Requires autopage to fix F36/FTBFS

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 23 2021 Joel Capitao <jcapitao@redhat.com> - 2.3.0-1
- Update to latest release

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.2.6-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov 12 2020 Joel Capitao <jcapitao@redhat.com> - 2.2.6-2
- Use git-core as BR instead of git

* Thu Oct 29 2020 Joel Capitao <jcapitao@redhat.com> - 2.2.6-1
- Update to 2.2.6

* Mon Sep 14 2020 Joel Capitao <jcapitao@redhat.com> - 2.2.5-1
- Update to 2.2.5

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 01 2020 Alfredo Moralejo <amoralej@redhat.com> - 2.2.1-1
- Update to 2.2.1
- Remove python2 subpackage

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 1.29.0-8
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.29.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.29.0-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 1.29.0-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.29.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 26 2019 Javier Peña <jpena@redhat.com> - 1.29.0-3
- Remove the Python2 subpackage from Fedora

* Tue Feb 05 2019 Javier Peña <jpena@redhat.com> - 1.29.0-2
- Include the binaries in the python2 subpackage when not building with Python3, for CentOS 7 compatibility

* Tue Feb 05 2019 Javier Peña <jpena@redhat.com> - 1.29.0-1
- Update to upstream 1.29.0 (bz#1668948)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.23.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Sep 12 2018 Javier Peña <jpena@redhat.com> - 1.23.2-1
- Updated to  upstream 1.23.2 (bz#1552354)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.20.1-2
- Rebuilt for Python 3.7

* Tue Apr 17 2018 Alfredo Moralejo <amoralej@redhat.com> 1.20.1-1
- Update to 1.20.1

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 5 2018 Javier Peña <jpena@redhat.com> - 1.18.1-1
- Updated to upstream release 1.18.1 (bz#1533685)

* Fri Jan 26 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.11.0-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Sep 7 2017 Javier Peña <jpena@redhat.com> - 1.11.0-1
- Updated to upstream release 1.11.0 (bz#1435494)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.5.0-2
- Rebuild for Python 3.6

* Thu Sep 22 2016 Javier Peña <jpena@redhat.com> - 1.5.0-1
- Bumped to upstream release 1.5.0

* Fri Aug 19 2016 Javier Peña <jpena@redhat.com> - 1.4.0-2
- Use sphinx-build-2 for doc generation, there are issues with the Python3 version

* Fri Aug 19 2016 Javier Peña <jpena@redhat.com> - 1.4.0-1
- Bumped to upstream release 1.4.0
- Fixed source URL

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Apr 18 2016 Javier Peña <jpena@redhat.com> - 1.3.0-1
- Bumped to upstream release 1.3.0

* Thu Mar 03 2016 Javier Peña <jpena@redhat.com> - 1.2.7-2
- Fixed prep section
- Removed unneeded comments
- Added bundled(js-jquery) to provides

* Thu Mar 03 2016 jpena <jpena@redhat.com> - 1.2.7-1
- Initial package.
