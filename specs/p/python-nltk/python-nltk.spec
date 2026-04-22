# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global mod_name nltk
Name:           python-nltk
Epoch:          1
Version:        3.9.1
Release: 7%{?dist}
Summary:        Natural Language Toolkit

# The entire source code is ASL 2.0 except nltk/stem/porter.py is
# GPLv2+ with exceptions
# Automatically converted from old format: ASL 2.0 and GPLv2+ with exceptions - review is highly recommended.
License:        Apache-2.0 AND LicenseRef-Callaway-GPLv2+-with-exceptions
URL:            http://www.nltk.org/
Source0:        https://github.com/nltk/nltk/archive/%{version}.tar.gz#/%{mod_name}-%{version}.tar.gz
BuildArch:      noarch

# https://github.com/nltk/nltk/pull/3309
Patch1: fix-import-WordNetLemmatizer.patch

%global _description\
NLTK is a Python package that simplifies the construction of programs\
that process natural language; and defines standard interfaces between\
the different components of an NLP system.  It was designed primarily\
to help teach graduate and undergraduate students about computational\
linguistics; but it is also useful as a framework for implementing\
research projects.

%description %_description

%package -n python3-%{mod_name}
Summary:        Natural Language Toolkit (Python 3)
BuildRequires:  python3-devel

%description -n python3-%{mod_name}
NLTK is a Python package that simplifies the construction of programs
that process natural language; and defines standard interfaces between
the different components of an NLP system.  It was designed primarily
to help teach graduate and undergraduate students about computational
linguistics; but it is also useful as a framework for implementing
research projects.

This package provides the Python 3 build of NLTK.

%prep
%autosetup -p1 -n %{mod_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l %{mod_name}


%check
# skip tests since it requires nltk-data and a few utilities not available in
# Fedora
#%%{__python3} %%{mod_name}/test/runtests.py


%files -n python3-%{mod_name} -f %{pyproject_files}
%{_bindir}/%{mod_name}
%doc AUTHORS.md CONTRIBUTING.md ChangeLog README.md


%changelog
* Mon Dec 08 2025 Romain Geissler <romain.geissler@amadeus.com> - 1:3.9.1-6
- Migrate to pyproject macros (rhbz#2377930)

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1:3.9.1-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1:3.9.1-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1:3.9.1-2
- Rebuilt for Python 3.14

* Tue Mar 11 2025 Romain Geissler <romain.geissler@amadeus.com> - 1:3.9.1-1
- Update to 3.9.1 (#2303929)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.8.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 1:3.8.1-8
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.8.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1:3.8.1-6
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1:3.8.1-2
- Rebuilt for Python 3.12

* Fri Mar 31 2023 FeRD (Frank Dana) <ferdnyc@gmail.com> - 1:3.8.1-1
- New upstream release

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.6.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1:3.6.2-4
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul  7 2021 José Matos <jamatos@fedoraproject.org> - 1:3.6.2-1
- update to 3.6.2

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1:3.4.5-6
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.4.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.4.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1:3.4.5-3
- Rebuilt for Python 3.9

* Thu Mar 19 2020 José Matos <jamatos@fedoraproject.org> - 1:3.4.5-2
- Remove /usr/bin/env python from script's headers

* Sun Mar  8 2020 Robin Lee <cheeselee@fedoraproject.org> - 1:3.4.5-1
- Updated to 3.4.5 (RHBZ#1771376, CVE-2019-14751)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1:3.0.3-18
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1:3.0.3-17
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jul 20 2019 Miro Hrončok <mhroncok@redhat.com> - 1:3.0.3-15
- Subpackage python2-nltk has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1:3.0.3-12
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 26 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1:3.0.3-10
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:3.0.3-9
- Python 2 binary package renamed to python2-nltk
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1:3.0.3-6
- Rebuild for Python 3.6

* Mon Sep 26 2016 Dominik Mierzejewski <rpm@greysector.net> - 1:3.0.3-5
- rebuilt for matplotlib-2.0.0

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.3-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Nov 12 2015 Kalev Lember <klember@redhat.com> - 1:3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Jul 03 2015 Parag Nemade <pnemade AT fedoraproject DOT org> - 1:3.0.3-1
- Update to 3.0.3

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Oct 24 2014 Robin Lee <cheeselee@fedoraproject.org> - 1:3.0.0-1
- Update to 3.0.0, build a python3 subpackage
- Drop the included distribute_setup.py
- License specified from 'ASL 2.0' to 'ASL 2.0 and GPLv2+ with exceptions'

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug  8 2013 Robin Lee <cheeselee@fedoraproject.org> - 1:2.0.4-5
- Update distribute_setup.py to work with setuptools >= 0.7

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 12 2012 Robin Lee <cheeselee@fedoraproject.org> - 1:2.0.4-2
- BuildRequires:  python-setuptools

* Wed Dec 12 2012 Robin Lee <cheeselee@fedoraproject.org> - 1:2.0.4-1
- Update to 2.0.4

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0.1-0.6.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0.1-0.5.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Apr 12 2011 Robin Lee <cheeselee@fedoraproject.org> - 1:2.0.1-0.4.rc1
- Update to 2.0.1rc1
- Requires tkinter

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0-0.4.b9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 30 2010 Robin Lee <robinlee.sysu@gmail.com> - 1:2.0-0.3.b9
- update to 2.0b9

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1:2.0-0.2.b8
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon May 17 2010 Robin Lee <robinlee.sysu@gmail.com> - 1:2.0-0.1.b8
- Updated to 2.0b8
- License switched upstream to ASL 2.0 since 2.0b4
- Remove specifications for obsolete Fedora versions
- Remove python_sitelib definition
- URL and Source0 URL revised
- BuildRoot tag removed
- BR: tkinter removed, PyYAML added
- Requires: tkinter removed
- nltk-0.9.2-use-sys-yaml.patch removed
- All redundant commands in 'install' section removed
- nltk_contrib entry in 'file' section was removed since it will include no
  file. Upstream split off a new tarball for nltk-contrib.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1:0.9.2-2
- Rebuild for Python 2.6

* Mon Apr  7 2008 Michel Salim <salimma@fedoraproject.org> - 1:0.9.2-1
- Update to 0.9.2

* Sat Feb 23 2008 Michel Salim <michel.sylvan@gmail.com> - 1:0.9-2
- Use system PyYAML (bug #432329)

* Sun Jan 20 2008 Michel Salim <michel.sylvan@gmail.com> - 1:0.9-1
- Update to final 0.9
- Add Epoch to clear upgrade path from (old) 1.4.4

* Sat Sep 22 2007 Michel Salim <michel.sylvan@gmail.com> - 0.9-0.2.b2
- BR on tkinter, it is now needed at build time

* Fri Sep 21 2007 Michel Salim <michel.sylvan@gmail.com> - 0.9-0.1.b2
- Updated to 0.9b2
- Renamed back to python-nltk

* Mon Dec 18 2006 Michel Salim <michel.salim@gmail.com> - 0.6.6-2
- Rebuild for development branch

* Mon Oct 30 2006 Michel Salim <michel.salim@gmail.com> - 0.6.6-1
- Initial package
