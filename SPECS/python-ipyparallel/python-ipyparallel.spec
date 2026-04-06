# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		python-ipyparallel
Version:	9.0.2
Release:	2%{?dist}
Summary:	Interactive Parallel Computing with IPython

License:	BSD-3-Clause
URL:		https://github.com/ipython/ipyparallel
Source0:	%pypi_source ipyparallel
BuildArch:	noarch

%description
IPython Parallel (ipyparallel) is a Python package and collection of
CLI scripts for controlling clusters of IPython processes, built on
the Jupyter protocol.

%package -n python3-ipyparallel
Summary:	Interactive Parallel Computing with IPython
%py_provides	python3-ipyparallel
Requires:	python-jupyter-filesystem >= 4.7.0-5
Obsoletes:	python-ipyparallel-doc <= 8.7.0

%description -n python3-ipyparallel
IPython Parallel (ipyparallel) is a Python package and collection of
CLI scripts for controlling clusters of IPython processes, built on
the Jupyter protocol.

%package -n python3-ipyparallel+test
Summary:	Tests for python3-ipyparallel
%py_provides	python3-ipyparallel+test
%py_provides	python3-ipyparallel-tests
Obsoletes:	python3-ipyparallel-tests < 8.4.1-3
Requires:	python3-ipyparallel = %{version}-%{release}

%description -n python3-ipyparallel+test
This package contains the tests of python3-ipyparallel.

%prep
%setup -q -n ipyparallel-%{version}

rm ipyparallel/labextension/schemas/ipyparallel-labextension/package.json.orig

%generate_buildrequires
%pyproject_buildrequires -x test

%build
%pyproject_wheel

%install
%pyproject_install

for f in apps/iploggerapp.py cluster/app.py controller/app.py \
	 controller/heartmonitor.py engine/app.py ; do
  sed '/\/usr\/bin\/env/d' -i %{buildroot}%{python3_sitelib}/ipyparallel/${f}
  chmod -x %{buildroot}%{python3_sitelib}/ipyparallel/${f}
done

# Fix wrong install directory for configuraton files
mv %{buildroot}%{_prefix}%{_sysconfdir} %{buildroot}%{_sysconfdir}

%check
%pytest -v --color=no

%files -n python3-ipyparallel
%license COPYING.md
%doc README.md
%{python3_sitelib}/ipyparallel-*.*-info
%dir %{python3_sitelib}/ipyparallel
%{python3_sitelib}/ipyparallel/*.py
%{python3_sitelib}/ipyparallel/__pycache__
%{python3_sitelib}/ipyparallel/apps
%{python3_sitelib}/ipyparallel/client
%{python3_sitelib}/ipyparallel/cluster
%{python3_sitelib}/ipyparallel/controller
%{python3_sitelib}/ipyparallel/engine
%{python3_sitelib}/ipyparallel/labextension
%{python3_sitelib}/ipyparallel/nbextension
%{python3_sitelib}/ipyparallel/serialize
%{_bindir}/ipcluster
%{_bindir}/ipcontroller
%{_bindir}/ipengine
%{_datadir}/jupyter/labextensions/ipyparallel-labextension
%{_datadir}/jupyter/nbextensions/ipyparallel
%config(noreplace) %{_sysconfdir}/jupyter/jupyter_notebook_config.d/ipyparallel.json
%config(noreplace) %{_sysconfdir}/jupyter/jupyter_server_config.d/ipyparallel.json
%config(noreplace) %{_sysconfdir}/jupyter/nbconfig/tree.d/ipyparallel.json

%files -n python3-ipyparallel+test
%ghost %{python3_sitelib}/ipyparallel-*.*-info
%{python3_sitelib}/ipyparallel/tests

%changelog
* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Oct 10 2025 Mattias Ellert  <mattias.ellert@physics.uu.se> - 9.0.2-1
- Update to 9.0.2

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 9.0.1-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 9.0.1-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 31 2025 Mattias Ellert <mattias.ellert@physics.uu.se> - 9.0.1-4
- Generate build requires instead of hardcoding them

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 05 2025 Python Maint <python-maint@redhat.com> - 9.0.1-2
- Rebuilt for Python 3.14

* Mon Mar 03 2025 Mattias Ellert <mattias.ellert@physics.uu.se> - 9.0.1-1
- Update to 9.0.1
- Drop patches (accepted upstream)

* Wed Feb 19 2025 Mattias Ellert <mattias.ellert@physics.uu.se> - 9.0.0-5
- Do not fail test when there are no public IP addresses

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec 10 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 9.0.0-3
- Drop spurious dependency on python3-zmq-tests

* Mon Dec 09 2024 Mattias Ellert <mattias.ellert@physics.uu.se> - 9.0.0-2
- Disable MongoDB tests

* Thu Nov 07 2024 Mattias Ellert <mattias.ellert@physics.uu.se> - 9.0.0-1
- Update to 9.0.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 8.8.0-3
- Rebuilt for Python 3.13

* Sun Jun 09 2024 Mattias Ellert <mattias.ellert@physics.uu.se> - 8.8.0-2
- Ignore deprecation warnings from datetime.strptime()

* Sat Apr 06 2024 Mattias Ellert <mattias.ellert@physics.uu.se> - 8.8.0-1
- Update to 8.8.0

* Tue Mar 05 2024 Mattias Ellert <mattias.ellert@physics.uu.se> - 8.7.0-1
- Update to 8.7.0
- Drop patches (accepted upstream)
- Drop documentation package (build dependency myst-nb not available)

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 03 2023 Python Maint <python-maint@redhat.com> - 8.6.1-3
- Rebuilt for Python 3.12

* Sat Apr 15 2023 Mattias Ellert <mattias.ellert@physics.uu.se> - 8.6.1-2
- Fix AttributeError in tests

* Fri Apr 14 2023 Mattias Ellert <mattias.ellert@physics.uu.se> - 8.6.1-1
- Update to 8.6.1

* Thu Mar 30 2023 Mattias Ellert <mattias.ellert@physics.uu.se> - 8.5.1-1
- Update to 8.5.1
- Use source from PyPI

* Sat Mar 18 2023 Mattias Ellert <mattias.ellert@physics.uu.se> - 8.5.0-1
- Update to 8.5.0
- Drop patches (accepted upstream)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 03 2022 Mattias Ellert <mattias.ellert@physics.uu.se> - 8.4.1-3
- Rename tests subpackage to fix auto provides
- Ignore deprecation warnings from jupyter-core

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jun 26 2022 Mattias Ellert <mattias.ellert@physics.uu.se> - 8.4.1-1
- Update to 8.4.1
- Drop python 3.11 patch (accepted upstream)
- Use the pyproject rpm macros

* Thu Jun 23 2022 Miro Hrončok <mhroncok@redhat.com> - 8.2.1-3
- Build with pydata-sphinx-theme again

* Mon Jun 20 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 8.2.1-2
- Add patch for Python 3.11 compatibility

* Tue Apr 05 2022 Mattias Ellert <mattias.ellert@physics.uu.se> - 8.2.1-1
- Update to 8.2.1

* Mon Feb 07 2022 Mattias Ellert <mattias.ellert@physics.uu.se> - 8.2.0-1
- Update to 8.2.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 23 2021 Mattias Ellert <mattias.ellert@physics.uu.se> - 8.1.0-1
- Update to 8.1.0

* Mon Nov 15 2021 Mattias Ellert <mattias.ellert@physics.uu.se> - 8.0.0-1
- Update to 8.0.0

* Sun Oct 03 2021 Mattias Ellert <mattias.ellert@physics.uu.se> - 7.1.0-1
- Update to 7.1.0

* Tue Sep 14 2021 Mattias Ellert <mattias.ellert@physics.uu.se> - 7.0.1-1
- Update to 7.0.1

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 6.3.0-7
- Rebuilt for Python 3.10

* Thu May 06 2021 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.3.0-6
- Ignore deprecation warnings

* Tue Apr 13 2021 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.3.0-5
- Disable the test_px_blocking and test_px_nonblocking tests on Fedora 35+
- Remove obsolete scriptlet for removing old style config

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 6.3.0-2
- Rebuilt for Python 3.9

* Wed May 06 2020 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.3.0-1
- Update to 6.3.0
- Drop patches (accepted upstream, or previously backported)

* Mon Apr 20 2020 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.2.5-1
- Update to 6.2.5
- Remove Python 2 parts from the spec file (Fedora 29 is EOL)
- Drop patches (accepted upstream, or previously backported)
- Prevent KeyError when handling heart failures of already shut down engines
- Print more helpful errors from pytest.warns(None)
- Fix client test for python 3.8

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 01 2019 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.2.4-4
- Compatibility with ipykernel 5.1.2 (backport from upstream)

* Mon Aug 12 2019 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.2.4-3
- Compatibility fixes for Python 3.7, 3.8 (backport from upstream)
- Use unittest.mock if available
- Adapt to Python 3.8 with PEP 570
- Disable the test_abort test (occasional random failures)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 13 2019 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.2.4-1
- Update to 6.2.4
- Avoid python3-mock dependency

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 13 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.2.3-2
- Don't build Python 2 packages for Fedora >= 30

* Mon Oct 22 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.2.3-1
- Update to 6.2.3

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.2.2-1
- Update to 6.2.2

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 6.2.1-2
- Rebuilt for Python 3.7

* Mon Jun 11 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.2.1-1
- Update to 6.2.1
- This version uses the possibility to split the configuration files into
  smaller files in .d directories introduced in Jupyter notebook 5.3.0
- Drop scriptlets for handling the old configuration
- Add scriptlet to remove old configuration when updating from earlier versions
- Enable the test_wait_for_send test again (the test suite now tries it three
  times before failing)

* Mon Jun 11 2018 Miro Hrončok <mhroncok@redhat.com> - 6.1.1-2
- Don't own /usr/share/jupyter/nbextensions,
  require python-jupyter-filesystem instead (#1589420)

* Wed Feb 07 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.1.1-1
- Update to 6.1.1

* Tue Feb 06 2018 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.1.0-1
- Update to 6.1.0
- Drop patch python-ipyparallel-pr254.patch (previously backported)
- Only provide one documentation package
- Disable the test_wait_for_send test (occasional random failures)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu May 18 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.0.2-2
- Put tests in a separate subpackage

* Sun Apr 30 2017 Mattias Ellert <mattias.ellert@physics.uu.se> - 6.0.2-1
- Initial packaging
