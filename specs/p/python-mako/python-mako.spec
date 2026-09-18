# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:    python-mako
Version: 1.2.3
Release: 13%{?dist}
Summary: Mako template library for Python

# Mostly MIT, but _ast_util.py is Python-2.0.1 licensed
# examples/bench/basic.py is BSD-3-Clause
License: MIT AND Python-2.0.1 AND BSD-3-Clause
URL:     https://www.makotemplates.org/
Source0: https://github.com/sqlalchemy/mako/archive/rel_%(echo %{version} | sed "s/\./_/g").tar.gz

BuildArch:     noarch
BuildRequires: python3-devel
BuildRequires: python3-pytest
BuildRequires: python3-setuptools
BuildRequires: python3-markupsafe

%global _description\
Mako is a template library written in Python. It provides a familiar, non-XML\
syntax which compiles into Python modules for maximum performance. Mako's\
syntax and API borrows from the best ideas of many others, including Django\
templates, Cheetah, Myghty, and Genshi. Conceptually, Mako is an embedded\
Python (i.e. Python Server Page) language, which refines the familiar ideas of\
componentized layout and inheritance to produce one of the most straightforward\
and flexible models available, while also maintaining close ties to Python\
calling and scoping semantics.

%description %_description


%package -n python3-mako
Summary: %{summary}

# Beaker is the preferred caching backend, but is not strictly necessary
Recommends: python3-beaker

Obsoletes: python2-mako < 1.1.0-3
Obsoletes: python-mako-doc < 1.1.4-6

%{?python_provide:%python_provide python3-mako}

%description -n python3-mako %_description

This package contains the mako module built for use with python3.



%prep
%autosetup -p1 -n mako-rel_%(echo %{version} | sed "s/\./_/g")

# the package ends up installed as %%{version}.dev0 otherwise:
sed -i '/tag_build = dev/d' setup.cfg


%build
%py3_build


%install
%py3_install

mv %{buildroot}/%{_bindir}/mako-render %{buildroot}/%{_bindir}/mako-render-%{python3_version}
ln -s ./mako-render-%{python3_version} %{buildroot}/%{_bindir}/mako-render-3
ln -s ./mako-render-%{python3_version} %{buildroot}/%{_bindir}/mako-render


%check
pytest-3


%files -n python3-mako
%license LICENSE
%doc CHANGES README.rst examples
%{_bindir}/mako-render
%{_bindir}/mako-render-3
%{_bindir}/mako-render-%{python3_version}
%{python3_sitelib}/mako/
%{python3_sitelib}/Mako-*.egg-info/


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.2.3-13
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.2.3-12
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.2.3-10
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.2.3-7
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.2.3-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Oct 27 2022 David King <amigadave@amigadave.com> - 1.2.3-1
- Update to 1.2.3 (#1996163)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.1.4-8
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Oct 29 2021 Miro Hrončok <mhroncok@redhat.com> - 1.1.4-6
- Don't build the package as 1.1.4.dev0
- Remove the empty python-mako-doc package

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 1.1.4-4
- Rebuilt for Python 3.10

* Mon Mar 29 2021 David King <amigadave@amigadave.com> - 1.1.4-3
- Remove unnecessary python3-mock BuildRequires

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 14 19:55:31 CET 2021 Petr Viktorin <pviktori@redhat.com> - 1.1.4-1
- Update to version 1.1.4
- Avoids test warnings on Python 3.10
  Fixes: https://bugzilla.redhat.com/show_bug.cgi?id=1907474

* Fri Jun 26 2020 Charalampos Stratakis <cstratak@redhat.com> - 1.1.3-1
- Update to 1.1.3 (#1808872)

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 1.1.1-2
- Rebuilt for Python 3.9

* Mon Feb 10 2020 Miro Hrončok <mhroncok@redhat.com> - 1.1.1-1
- Update to 1.1.1 (#1787962) (#1793184)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 07 2020 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.1.0-4
- Fix FTBFS with pytest-5 by dropping a BR on python-nose (mako does not use nose).

* Fri Nov 15 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-3
- Subpackage python2-mako has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Fri Oct 11 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-2
- Rename the Python-versioned executables not to start with "python"
- Make mako-render Python 3 on Fedora 32+

* Tue Sep 03 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0 (#1725969).
- https://docs.makotemplates.org/en/latest/changelog.html#change-1.1.0

* Sun Aug 18 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.12-4
- Rebuilt for Python 3.8

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.12-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 05 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.0.12-1
- Update to 1.0.12 (#1708706).
- https://docs.makotemplates.org/en/latest/changelog.html#change-1.0.12

* Wed Apr 17 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.9-1
- Update to 1.0.9 (#1698191, #1700055)

* Wed Mar 20 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.8-1
- Update to 1.0.8 (#1470902, #1690902)

* Wed Mar 20 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.7-1
- Update to 1.0.7 (#1470902)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 1.0.6-10
- Rebuilt for Python 3.7

* Wed Mar 28 2018 Petr Viktorin <pviktori@redhat.com> - 1.0.6-9
- Make python-beaker an optional dependency
- Add missing python_provide for python3-mako
- Conditionalize the Python 2 subpackage
- Modernize the specfile

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.0.6-8
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild
