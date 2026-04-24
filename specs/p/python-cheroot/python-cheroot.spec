# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Created by pyp2rpm-3.2.2
%global pypi_name cheroot
# sphinx-tabs not available in fedora for docs build
%bcond_with docs

Name:           python-%{pypi_name}
Version:        10.0.1
Release: 10%{?dist}
Summary:        Highly-optimized, pure-python HTTP server

# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
URL:            https://github.com/cherrypy/cheroot
Source0:        %{pypi_source}
BuildArch:      noarch

# https://github.com/cherrypy/cheroot/issues/645
# https://github.com/cherrypy/cheroot/pull/655
Patch0:		 0001-handle-openssl3-error-in-ssl-tests.patch

%description
Cheroot is the high-performance, pure-Python HTTP server used by CherryPy.

%package -n python3-%{pypi_name}
Summary:        %{summary}
Requires:       python3dist(six) >= 1.11
Requires:       python3dist(more-itertools) >= 2.6
Requires:       python3-pyOpenSSL
Requires:       python3dist(jaraco-functools)

BuildRequires:  python3-devel
BuildRequires:  python3-pyOpenSSL
BuildRequires:  python3dist(jaraco-functools)
BuildRequires:  python3dist(jaraco-text)
BuildRequires:  python3dist(portend)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-mock)
BuildRequires:  python3dist(pytest-forked)
BuildRequires:  python3dist(pytest-rerunfailures)
BuildRequires:  python3dist(requests-toolbelt)

%if 0%{?el8}
BuildRequires:  python3dist(more-itertools) >= 2.6
%endif

BuildRequires:  python3dist(requests)
BuildRequires:  python3dist(requests-unixsocket)
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(setuptools-scm)
BuildRequires:  python3dist(trustme)
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
Cheroot is the high-performance, pure-Python HTTP server used by CherryPy.

%if %{with docs}
%package -n python-%{pypi_name}-doc
Summary:        cheroot documentation

BuildRequires:  python3dist(sphinx)
BuildRequires:  python3-sphinx-theme-alabaster
BuildRequires:  python3dist(rst-linker)
BuildRequires:  python3dist(jaraco-packaging)
BuildRequires:  python3dist(docutils)

%description -n python-%{pypi_name}-doc
Documentation for cheroot
%endif

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

# Remove pytest processes directive
sed -i 's/ --numprocesses=auto//' pytest.ini
# Remove optional pytest-cov dependency
sed -i -e /--cov=/d -e '/--cov-report /d' pytest.ini
# drop setuptools_scm_git_archive
sed -i '/setuptools_scm_git_archive/d' setup.cfg
# RHEL 9 has setuptools_scm 6
sed -i 's/setuptools_scm >= 7.0.0/setuptools_scm >= 6.0.0/' setup.cfg

# doctor a few tests because of unpackaged deps in fedora
# pypytools
sed -i '/pypytools/d' cheroot/test/test_server.py
sed -i "/getfixturevalue('_garbage_bin')/d" cheroot/test/test_server.py
# jaraco.context
sed -i '/jaraco.context/d' cheroot/test/test_wsgi.py
sed -i '39 i @pytest.mark.skip()' cheroot/test/test_wsgi.py

%build
%py3_build
%if %{with docs}
sphinx-build -vvv docs html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%install
%py3_install

%check
LANG=C.utf-8 %{__python3} -m pytest --ignore=build -W ignore::DeprecationWarning -p no:unraisableexception

%files -n python3-%{pypi_name}
%license LICENSE.md
%doc README.rst
%{_bindir}/cheroot
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}*egg-info

%if %{with docs}
%files -n python-%{pypi_name}-doc
%license LICENSE.md
%doc html
%endif

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 10.0.1-9
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 10.0.1-8
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 10.0.1-6
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 10.0.1-4
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 10.0.1-2
- Rebuilt for Python 3.13

* Mon Apr 22 2024 Ken Dreyer <kdreyer@ibm.com> 10.0.1-1
- Update to 10.0.1

* Tue Apr 02 2024 Dan Radez <dradez@redhat.com> - 10.0.0-6
- adding patch to fix ssl unit tests rhbz#2270931

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 10.0.0-2
- Rebuilt for Python 3.12

* Mon Jun 19 2023 Dan Radez <dradez@redhat.com> - 10.0.0-1
- update to 10.0.0 (rhbz#2208818)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 23 2022 Dan Radez <dradez@redhat.com> - 9.0.0-1
- update to 9.0.0 (rhbz#2144238)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 8.6.0-7
- Rebuilt for Python 3.11

* Thu Mar 24 2022 Dan Radez <dradez@redhat.com> - 8.6.0-6
- skipping a test for pytest 7 compatibility

* Thu Feb 10 2022 Dan Radez <dradez@redhat.com> - 8.6.0-5
- jaraco.text is packaged, removing provisions to skip it

* Fri Jan 28 2022 Miro Hrončok <mhroncok@redhat.com> - 8.6.0-4
- Provide python3dist(cheroot) = 8.6
- Provide python3.Xdist(cheroot) = 8.6

* Wed Jan 19 2022 Dan Radez <dradez@redhat.com> - 8.6.0-2
- BZ#2042509

* Wed Jan 19 2022 Dan Radez <dradez@redhat.com> - 8.6.0-2
- Attempting to enable tests
- had to manually disable a couple due to missing deps

* Tue Jan 04 2022 Dan Radez <dradez@redhat.com> - 8.6.0-1
- update to 8.6.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 8.5.2-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 19 2021 Dan Radez <dradez@redhat.com> - 8.5.2-1
- update to 8.5.2

* Sat Dec 12 2020 Dan Radez <dradez@redhat.com> - 8.5.1-1
- update to 8.5.1

* Mon Dec 07 2020 Ken Dreyer <kdreyer@redhat.com> 8.5.0-1
- Update to 8.5.0 (rhbz#1868629)

* Tue Aug 04 2020 Fabien Boucher <fboucher@redhat.com> - 8.4.2-1
- update to 8.4.2

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 03 2020 Matthias Runge <mrunge@redhat.com> - 8.2.1-3
- skip test and rebuild to fix fail to install for cherrypy

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 8.2.1-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 18 2019 Dan Radez <dradez@redhat.com> - 8.2.1-1
- update to 8.2.1

* Thu Oct 17 2019 Dan Radez <dradez@redhat.com> - 8.2.0-1
- update to 8.2.0

* Fri Oct 11 2019 Dan Radez <dradez@redhat.com> - 8.1.0-1
- update to 8.1.0

* Fri Sep 27 2019 Dan Radez <dradez@redhat.com> - 7.0.0-2
- fixing dep naming issues

* Thu Sep 26 2019 Dan Radez <dradez@redhat.com> - 7.0.0-1
- update to 7.0.0

* Tue Sep 24 2019 Dan Radez <dradez@redhat.com> - 6.5.8-1
- update to 6.5.8

* Wed Aug 21 2019 Miro Hrončok <mhroncok@redhat.com> - 6.5.6-2
- Rebuilt for Python 3.8

* Mon Aug 19 2019 Dan Radez <dradez@redhat.com> - 6.5.6-1
- update to 6.5.6

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 6.5.5-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 30 2019 Dan Radez <dradez@redhat.com> - 6.5.5-1
- update to 6.5.5
- disable docs build, new dep sphinx-tabs was introduced.

* Tue Apr 09 2019 Dan Radez <dradez@redhat.com> - 6.5.4-2
- enabling docs

* Wed May 02 2018 Dan Radez <dradez@redhat.com> - 6.5.4-1
- Initial package.
