Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%bcond_with    python2
%bcond_without python3

%global pypi_name openstackdocstheme

Name:           python-%{pypi_name}
Version:        1.29.0
Release:        8%{?dist}
Summary:        OpenStack Docs Theme

License:        ASL 2.0
URL:            https://docs.openstack.org/
Source0:        https://pypi.io/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz#/python-%{pypi_name}-%{version}.tar.gz
Patch0001:      0001-Remove-all-Google-Analytics-tracking.patch
BuildArch:      noarch

%if %{with python2}
%package -n     python2-%{pypi_name}
Summary:        OpenStack Docs Theme
%{?python_provide:%python_provide python2-%{pypi_name}}
Provides:       bundled(js-jquery)

BuildRequires:  python2-devel
BuildRequires:  python2-dulwich
BuildRequires:  python2-setuptools
BuildRequires:  python2-pbr >= 1.8
BuildRequires:  python2-sphinx
BuildRequires:  git

Requires: python2-dulwich
Requires: python2-pbr
Requires: python2-sphinx >= 1.6.2

%description -n python2-%{pypi_name}
OpenStack docs.openstack.org Sphinx Theme

Theme and extension support for Sphinx documentation that is published to
docs.openstack.org. Intended for use by OpenStack projects.
%endif

%if %{with python3}
%package -n     python3-%{pypi_name}
Summary:        OpenStack Docs Theme
%{?python_provide:%python_provide python3-%{pypi_name}}
Provides:       bundled(js-jquery)

BuildRequires:  python3-devel
BuildRequires:  python3-dulwich
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr >= 1.8
BuildRequires:  python3-sphinx
BuildRequires:  git

Requires: python3-babel
Requires: python3-dulwich
Requires: python3-pbr
Requires: python3-sphinx >= 1.6.2
Requires: python3-extras

%description -n python3-%{pypi_name}
OpenStack docs.openstack.org Sphinx Theme

Theme and extension support for Sphinx documentation that is published to
docs.openstack.org. Intended for use by OpenStack projects.
%endif

%package -n python-%{pypi_name}-doc
Summary:        openstackdocstheme documentation
%description -n python-%{pypi_name}-doc
Documentation for openstackdocstheme

%description
OpenStack docs.openstack.org Sphinx Theme

Theme and extension support for Sphinx documentation that is published to
docs.openstack.org. Intended for use by OpenStack projects.

%prep
%autosetup -n %{pypi_name}-%{version} -p1 -S git

%build
# Make sure there is no Google Analytics
sed -i 's/analytics_tracking_code.*/analytics_tracking_code\ =/' openstackdocstheme/theme/openstackdocs/theme.conf
# Prevent doc build warnings from causing a build failure
sed -i '/warning-is-error/d' setup.cfg

%if %{with python2}
%py2_build
%endif
%if %{with python3}
%py3_build
%endif

%if %{with python2}
# generate html docs
%{__python2} setup.py build_sphinx
%endif
%if %{with python3}
%{__python3} setup.py build_sphinx
%endif
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%if %{with python2}
%py2_install
%endif
%if %{with python3}
%py3_install
%endif

%if %{with python2}
%files -n python2-%{pypi_name}
%doc README.rst
%license LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%{_bindir}/docstheme-build-translated.sh
%{_bindir}/docstheme-lang-display-name.py
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/docstheme-build-translated.sh
%{_bindir}/docstheme-lang-display-name.py
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif

%files -n python-%{pypi_name}-doc
%doc doc/build/html

%changelog
* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 1.29.0-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Add missing dependency on python3-extras

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
