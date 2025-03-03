%global modname rpmfluff

Name:          python-%{modname}
Version:       0.6.5
Release:       4%{?dist}
Summary:       Lightweight way of building RPMs, and sabotaging them

License:       GPL-2.0-or-later
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:           https://pagure.io/rpmfluff
Source0:       https://pagure.io/releases/%{modname}/%{modname}-%{version}.tar.xz#/%{name}-%{version}.tar.xz

BuildArch:     noarch

%global _description \
rpmfluff provides a python library for building RPM packages, and\
sabotaging them so they are broken in controlled ways.\
\
It is intended for use when validating package analysis tools such as RPM lint.\
It can also be used to construct test cases for package management software\
such as RPM, YUM, and DNF.

%description %{_description}

%package -n python3-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{modname}}
BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  python3-rpm
BuildRequires:  python3-setuptools
Requires:       rpm-build
Requires:       createrepo_c

%description -n python3-%{modname} %{_description}

Python 3 version.

%prep
%autosetup -n %{modname}-%{version}

%build
%py3_build

%install
%py3_install

%check
python3 -m unittest %{modname}.test

%files -n python3-%{modname}
%license LICENSE
%doc README.md
%{python3_sitelib}/*

%changelog
* Fri Dec 20 2024 Akhila Guruju <v-guakhila@microsoft.com> - 0.6.5-4
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.6.5-2
- Rebuilt for Python 3.13

* Fri May 31 2024 Jan Hutar <jhutar@redhat.com> - 0.6.4-1
- dshea: Explicitly disable debuginfo when not requested

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 17 2023 Jan Hutar <jhutar@redhat.com> - 0.6.3-1
- gotmax23: remove usage of deprecated rpm.fi

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.6.2-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Oct 18 2022 Jan Hutar <jhutar@redhat.com> - 0.6.2-1
- Change deprecated distutils to setuptools

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.6.1-6
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 0.6.1-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 12 2020 Jan Hutar <jhutar@redhat.com> - 0.6.1-1
- jhutar: Expose two more items

* Fri Aug 07 2020 Jan Hutar <jhutar@redhat.com> - 0.6-1
- jhutar: Workaround for https://github.com/rpm-software-management/rpm/issues/1301
- msuchy: Do not write %clean by default
- msuchy: Make build directory in /tmp
- msuchy: Call buildArchs as named argument
- msuchy: Do not clean install
- msuchy: BuildRoot is ignored by rpm
- msuchy: Remove artefacts after the test
- msuchy: Fix various pylint warnings
- msuchy: Break down package into several modules
- msuchy: Remove dead code
- msuchy: Apply 2to3 script
- msuchy: Mention DNF in description
- msuchy: Move rpmfluff.py to rpmfluff/__init__.py
- dcantrell: Only write the License tag if it is set
- jhutar: Sanitize values we use to construct file paths
- tbaeder: Read compiler from CC environment variable
- dcantrell: Allow setting a different spec file basename than the package name

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.7.1-8
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 0.5.7.1-6
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.5.7.1-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 0.5.7.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat May 11 2019 Jan Hutar <jhutar@redhat.com> - 0.5.7.1-1
- Fixed tests to run in F31 with rpm-4.14.2.1-7.fc31

* Fri May 10 2019 Jan Hutar <jhutar@redhat.com> - 0.5.7-1
- Remove python 2 subpackage
- ksrot: RPM now returns all string data as surrogate-escaped utf-8 strings
- bcl: Tests fixes
- bcl: pylint warnings
- Better version of the check as advised by pmatilai

* Thu Jan 31 2019 Jan Hutar <jhutar@redhat.com> - 0.5.6-1
- dshea: Add a add_manpage function
- dshea: Sanitize the base directory name
- dshea: Support subpackage scriptlets
- dshea: Allow file directives to be added to symlinks
- dshea: Use valid images for the test PNG and GIF data

* Fri Jan 04 2019 Miro Hrončok <mhroncok@redhat.com> - 0.5.5-2
- Subpackage python2-rpmfluff has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sun Jul 22 2018 Jan Hutar <jhutar@redhat.com> - 0.5.5-1
- Fixing tests to be able to build in Fedora 29

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 17 2018 Miro Hrončok <mhroncok@redhat.com> - 0.5.4-3
- Rebuilt for Python 3.7

* Wed Feb 14 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.5.4-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Tue Feb 13 2018 Jan Hutar <jhutar@redhat.com> - 0.5.4-1
- Fixes RHBZ#1544361

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 28 2017 Jan Hutar <jhutar@redhat.com> - 0.5.3-1
- Support mixing noarch and archful packages in a yum repo build by Dan Callaghan <dcallagh@redhat.com>

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.5.2-2
- Rebuild for Python 3.6

* Thu Sep 29 2016 Jan Hutar <jhutar@redhat.com> - 0.5.2-1
- Lots of fixes by Dan Callaghan <dcallagh@redhat.com>

* Fri Jul 22 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.5.1-1
- Fix Requires for createrepo_c in py3 subpkg
- Fix crash on python2 due to non-existing shutil.which()

* Fri Jul 22 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.5-1
- Make package following guidelines
- Replace usage of obsolete createrepo_c with createrepo

* Thu Aug 20 2015 Jan Hutar <jhutar@redhat.com> - 0.4.2-1
- John Dulaney implemented weak dependencies

* Thu Jul 09 2015 Jan Hutar <jhutar@redhat.com> - 0.4-1
- David Shea did a lots of work to support Python 3
- RHEL5 (i.e. Python 2.4) support dropped

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 30 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 0.3-13
- Replace pyhton-setuptools-devel BR with python-setuptools

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 30 2010 David Malcolm <dmalcolm@redhat.com> - 0.3-6
- rebuild for python 2.7

* Fri Feb 12 2010 Jan Hutar <jhutar@redhat.com> - 0.3-5
- Now version is in the separate file

* Tue Jan 26 2010 Jan Hutar <jhutar@redhat.com> - 0.3-4
- Fix for deprecated popen2 module

* Thu Jan 7 2010 Jan Hutar <jhutar@redhat.com> - 0.3-3
- Moved to use EGGs for distribution

* Mon Dec 21 2009 Jan Hutar <jhutar@redhat.com> - 0.3-2
- Added separate LICENSE file

* Fri Dec 18 2009 Jan Hutar <jhutar@redhat.com> - 0.3-1
- New version, first attempt to get to Fedora

* Tue Jul 08 2008 Jan Hutar <jhutar@redhat.com> - 0.1-1
- Initial version
- spec-file based on python-html2text.spec
