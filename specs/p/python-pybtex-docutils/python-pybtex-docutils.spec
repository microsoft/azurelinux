# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python-pybtex-docutils
Version:        1.0.3
Release: 11%{?dist}
Summary:        Docutils backend for pybtex

# The content is MIT.  Other licenses are due to files copied in by Sphinx.
# _static/_sphinx_javascript_frameworks_compat.js: BSD-2-Clause
# _static/basic.css: BSD-2-Clause
# _static/classic.css: BSD-2-Clause
# _static/doctools.js: BSD-2-Clause
# _static/documentation_options.js: BSD-2-Clause
# _static/file.png: BSD-2-Clause
# _static/jquery*.js: MIT
# _static/language_data.js: BSD-2-Clause
# _static/minus.png: BSD-2-Clause
# _static/plus.png: BSD-2-Clause
# _static/searchtools.js: BSD-2-Clause
# _static/sidebar.js: BSD-2-Clause
# _static/underscore*.js: MIT
# genindex.html: BSD-2-Clause
# search.html: BSD-2-Clause
# searchindex.js: BSD-2-Clause
License:        MIT AND BSD-2-Clause
URL:            https://pybtex-docutils.readthedocs.io/
VCS:            git:https://github.com/mcmtroffaes/pybtex-docutils.git
Source:         %pypi_source pybtex-docutils

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  python3-devel
BuildRequires:  python3-docs
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist sphinx}

%global common_desc %{expand:
This package contains a docutils backend for pybtex, a BibTeX-compatible
bibliography processor written in Python.  Bibliographic references in
BibTeX format (or any other format supported by pybtex) can be inserted
into python documentation to be rendered by docutils.}

%description %common_desc

%package -n python3-pybtex-docutils
Summary:        Docutils backend for pybtex
Provides:       bundled(js-jquery)
Provides:       bundled(js-underscore)

%description -n python3-pybtex-docutils %common_desc

%prep
%autosetup -n pybtex-docutils-%{version}

%conf
# Update the sphinx theme name
sed -i "s/'default'/'classic'/" doc/conf.py

# Use local objects.inv for intersphinx
sed -i "s|\('http://docs\.python\.org/', \)None|\1'%{_docdir}/python3-docs/html/objects.inv'|" doc/conf.py

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel
PYTHONPATH=$PWD/src make -C doc html
rst2html --no-datestamp README.rst README.html

%install
%pyproject_install
%pyproject_save_files -l pybtex_docutils

%check
%pytest -v test

%files -n python3-pybtex-docutils -f %{pyproject_files}
%doc README.html doc/_build/html/*

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.0.3-10
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.0.3-9
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.0.3-7
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.0.3-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Aug 22 2023 Jerry James <loganjerry@gmail.com> - 1.0.3-1
- Version 1.0.3

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 1.0.2-5
- Rebuilt for Python 3.12

* Thu Feb 23 2023 Jerry James <loganjerry@gmail.com> - 1.0.2-4
- Dynamically generate BuildRequires
- Drop unneeded -test patch

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 13 2022 Jerry James <loganjerry@gmail.com> - 1.0.2-3
- Convert License tag to SPDX

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.0.2-2
- Rebuilt for Python 3.11

* Wed May 25 2022 Jerry James <loganjerry@gmail.com> - 1.0.2-1
- Version 1.0.2
- Add -test patch so the tests keep working with docutils 0.17

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 29 2021 Jerry James <loganjerry@gmail.com> - 1.0.1-1
- Version 1.0.1

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.0.0-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 15 2021 Jerry James <loganjerry@gmail.com> - 1.0.0-1
- Version 1.0.0
- Drop upstream patches

* Tue Aug 11 2020 Miro Hrončok <mhroncok@redhat.com> - 0.2.2-6
- Fix build with tox 3.19 (by not using it without tox config)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 25 2020 Miro Hrončok <mhroncok@redhat.com> - 0.2.2-4
- Rebuilt for Python 3.9

* Wed Apr 22 2020 Jerry James <loganjerry@gmail.com> - 0.2.2-3
- Add upstream patches to switch from nose to pytest

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 16 2019 Jerry James <loganjerry@gmail.com> - 0.2.2-1
- New upstream version

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.2.1-15
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sun Aug 18 2019 Miro Hrončok <mhroncok@redhat.com> - 0.2.1-14
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov 01 2018 Miro Hrončok <mhroncok@redhat.com> - 0.2.1-11
- Subpackage python2-pybtex-docutils has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.2.1-9
- Rebuilt for Python 3.7

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.2.1-8
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.2.1-4
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Mar  2 2016 Jerry James <loganjerry@gmail.com> - 0.2.1-2
- Expand package description
- Fix sphinx and noseutils invocations for python 3
- Do not convert license file to HTML

* Thu Feb 25 2016 Jerry James <loganjerry@gmail.com> - 0.2.1-1
- Initial RPM
