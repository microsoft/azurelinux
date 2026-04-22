# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global upname bottleneck

%bcond docs %[!0%{?rhel}]

Name:		python-Bottleneck
Version:	1.6.0
Release: 2%{?dist}
Summary:	Collection of fast NumPy array functions written in Cython

License:	BSD-2-Clause
URL:		https://pypi.org/project/Bottleneck/
Source0:	%pypi_source %{upname}
# https://github.com/pydata/bottleneck/pull/432
Patch0001:	0001-Fix-doc-build-with-Sphinx-6.patch

BuildRequires:	gcc
BuildRequires:	python3-devel
BuildRequires:	python3-pytest

BuildSystem:	pyproject
BuildOption(install):	-l bottleneck
%if %{with docs}
BuildOption(generate_buildrequires):	-x doc
%endif

# See https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:	%{ix86}

%description
%{name} is a collection of fast NumPy array functions
written in Cython.


%if %{with docs}
%package doc
Summary:	Documentation files for %{name}

BuildArch:	noarch

%description doc
This package contains the HTML-docs for %{name}.
%endif


%package -n python3-Bottleneck
Summary:	Collection of fast NumPy array functions written in Cython

%description -n python3-Bottleneck
python3-Bottleneck is a collection of fast NumPy array functions
written in Cython.


%prep
%autosetup -n %{upname}-%{version} -p 1

# Remove the contributors extensions which can't work because we don't
# have a repo anyway.
sed -i /contributors/d doc/source/conf.py

%if %{with docs}
%install -a
# Build the autodocs.
export PYTHONPATH="%{buildroot}%{python3_sitearch}"
export READTHEDOCS=1
sphinx-build -b html doc/source doc/html

# Clean unneeded stuff from docs.
rm -rf doc/html/{.buildinfo,.doctrees,.nojekyll}
%endif


%check
cd build/lib.linux-*
%pytest bottleneck
cd -


%if %{with docs}
%files doc
%license LICENSE
%doc README* RELEASE* doc/html
%endif


%files -n python3-Bottleneck -f %{pyproject_files}
%doc README* RELEASE*


%changelog
* Tue Oct 07 2025 Björn Esser <besser82@fedoraproject.org> - 1.6.0-1
- Update to 1.6.0

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.5.0-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Tue Aug 26 2025 Jerry James <loganjerry@gmail.com> - 1.5.0-1
- Version 1.5.0
- Stop building for 32-bit x86
- Update the License field to BSD-2-Clause
- Use the pyproject declarative buildsystem
- Do not build documentation for RHEL

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.4.2-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.4.2-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec 17 2024 Orion Poplawski <orion@nwra.com> - 1.4.2-1
- Update to 1.4.2

* Tue Dec 17 2024 Orion Poplawski <orion@nwra.com> - 1.3.7-9
- Rebuild with numpy 2.0

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 1.3.7-8
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 1.3.7-6
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 28 2023 Python Maint <python-maint@redhat.com> - 1.3.7-2
- Rebuilt for Python 3.12

* Tue Apr 04 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 1.3.7-1
- Update to 1.3.7
Fixes: rhbz#2056294
Fixes: rhbz#2137289

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 15 2022 Python Maint <python-maint@redhat.com> - 1.3.2-4
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 17 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.3.2-1
- Update to latest version (#1768152)

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.2.1-18
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 25 2020 Miro Hrončok <mhroncok@redhat.com> - 1.2.1-15
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct  4 2019 Orion Poplawski <orion@nwra.com> - 1.2.1-13
- Fix URL

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2.1-12
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2.1-11
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 28 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2.1-9
- Subpackage python2-Bottleneck has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.2.1-6
- Rebuilt for Python 3.7
- Use numpydoc from our package to fix FTBFS (#1594555)

* Fri Feb 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.2.1-5
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 16 2017 Björn Esser <besser82@fedoraproject.org> - 1.2.1-1
- Updated to new upstream release (rhbz#1451146)

* Sun Apr 09 2017 Björn Esser <besser82@fedoraproject.org> - 1.2.0-1
- Updated to new upstream release (rhbz#1105817)
- Updated spec-file to recent guidelines

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-10
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-9
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Nov 15 2015 Thomas Spura <tomspur@fedoraproject.org> - 0.6.0-7
- Use new python macros and add python2 subpackage

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed Aug 21 2013 Björn Esser <bjoern.esser@gmail.com> - 0.6.0-1
- Initial rpm release (#999563)
