Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# Copyright 2011, Red Hat
%global oname configshell-fb

Name:           python-configshell
License:        Apache-2.0
Summary:        A framework to implement simple but nice CLIs
Epoch:          1
Version:        1.1.30
Release:        9%{?dist}
URL:            https://github.com/open-iscsi/configshell-fb
Source:         %{url}/archive/v%{version}/%{oname}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel python3-setuptools

%global _description\
A framework to implement simple but nice configuration-oriented\
command-line interfaces.

%description %_description

%package -n python3-configshell
Summary:        A framework to implement simple but nice CLIs
Requires:       python3-pyparsing python3-urwid
%{?python_provide:%python_provide python3-configshell}

%description -n python3-configshell %_description

%prep
%setup -q -n %{oname}-%{version}

sed -r -i "s/'pyparsing.*'/'pyparsing'/" setup.py

%build
%py3_build

%install
%py3_install

%files -n python3-configshell
%{python3_sitelib}/configshell*
%doc COPYING README.md

%changelog
* Wed Dec 18 2024 Sumit Jena <v-sumitjena@microsoft.com> - 1.1.30-9
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.30-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1:1.1.30-7
- Rebuilt for Python 3.13

* Mon Feb 12 2024 Maurizio Lombardi <mlombard@redhat.com> - 1:1.1.30-6
- Migrated to SPDX License

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.30-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.30-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1:1.1.30-2
- Rebuilt for Python 3.12

* Tue Jun 06 2023 Maurizio Lombardi <mlombard@redhat.com> - 1:1.1.30-1
- Rebase to version v1.1.30

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.29-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Aug 03 2022 Vojtech Trefny <vtrefny@redhat.com> - 1:1.1.29-9
- Python 3.11: replace getargspec() with getfullargspec()

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.29-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:1.1.29-7
- Rebuilt for pyparsing-3.0.9

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1:1.1.29-5
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1:1.1.29-2
- Rebuilt for Python 3.10

* Mon May 17 2021 Maurizio Lombardi <mlombard@redhat.com> - 1:1.1.29-1
- Update to version 1.1.29

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 18 2020 Matt Coleman <matt@datto.com> - 1:1.1.28-1
- New upstream version

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1:1.1.fb25-9
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.fb25-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1:1.1.fb25-7
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1:1.1.fb25-6
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.fb25-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.fb25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Oct 11 2018 Miro Hrončok <mhroncok@redhat.com> - 1:1.1.fb25-3
- Python2 binary package has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Wed Oct 10 2018 Andy Grover <agrover@redhat.com> - 1:1.1.fb25-2
- Fix URL to point to open-iscsi org

* Wed Oct 10 2018 Andy Grover <agrover@redhat.com> - 1:1.1.fb25-1
- New upstream release
- Update URL so spectool -g works

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.fb24-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1:1.1.fb24-4
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.fb24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 29 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1:1.1.fb24-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Jan 26 2018 Andy Grover <agrover@redhat.com> - 1:1.1.fb24-1
- New upstream release
- Remove patch configshell-fix-term.patch

* Fri Dec 01 2017 Troy Dawson <tdawson@redhat.com> - 1:1.1.fb23-5
- Update spec file conditionals

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:1.1.fb23-4
- Python 2 binary package renamed to python2-configshell
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.fb23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 23 2017 Andy Grover <agrover@redhat.com> - 1:1.1.fb23-2
- Add patch configshell-fix-term.patch

* Wed Mar 1 2017 Andy Grover <agrover@redhat.com> - 1:1.1.fb23-1
- New upstream release

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.fb20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1:1.1.fb20-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.fb20-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Apr 7 2016 Andy Grover <agrover@redhat.com> - 1:1.1.fb20-1
- New upstream release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.fb19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 1 2015 Andy Grover <agrover@redhat.com> - 1:1.1.fb19-1
- New upstream release

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.fb18-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Oct 27 2015 Andy Grover <agrover@redhat.com> - 1:1.1.fb18-2
- Rebuild

* Tue Jun 23 2015 Andy Grover <agrover@redhat.com> - 1:1.1.fb18-1
- New upstream release
- Add dependency on python-six instead of 2to3

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.fb17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 13 2015 Andy Grover <agrover@redhat.com> - 1:1.1.fb17-1
- New upstream release

* Tue Dec 2 2014 Andy Grover <agrover@redhat.com> - 1:1.1.fb16-1
- New upstream release

* Fri Nov 14 2014 Andy Grover <agrover@redhat.com> - 1:1.1.fb14-3
- Add python 3 dependencies to Python 3 package

* Thu Nov 13 2014 Andy Grover <agrover@redhat.com> - 1:1.1.fb14-2
- Add Python 3 subpackage

* Thu Aug 28 2014 Andy Grover <agrover@redhat.com> - 1:1.1.fb14-1
- New upstream release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.fb13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 25 2014 Andy Grover <agrover@redhat.com> - 1:1.1.fb13-1
- New upstream release

* Fri Mar 14 2014 Andy Grover <agrover@redhat.com> - 1:1.1.fb12-1
- New upstream release

* Mon Jan 6 2014 Andy Grover <agrover@redhat.com> - 1:1.1.fb11-1
- New upstream release

* Fri Nov 1 2013 Andy Grover <agrover@redhat.com> - 1:1.1.fb10-1
- New upstream release

* Thu Sep 12 2013 Andy Grover <agrover@redhat.com> - 1:1.1.fb9-1
- New upstream release
- Remove dependency on python-simpleparse in favor of pyparsing
- Remove BuildRequires

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.fb8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Andy Grover <agrover@redhat.com> - 1:1.1.fb8-1
- New upstream release
- License now Apache 2.0
- README.md instead of README

* Tue Feb 26 2013 Andy Grover <agrover@redhat.com> - 1:1.1.fb7-1
- New upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.fb6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 4 2013 Andy Grover <agrover@redhat.com> - 1:1.1.fb6-1
- New upstream release
- Update source URL

* Tue Jul 31 2012 Andy Grover <agrover@redhat.com> - 1:1.1.fb5-1
- New upstream release
- Update Source URL to proper tarball

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.fb4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 10 2012 Andy Grover <agrover@redhat.com> - 1:1.1.fb4-1
- New upstream release

* Wed Dec 14 2011 Andy Grover <agrover@redhat.com> - 1:1.1.fb3-1
- New upstream release

* Tue Dec 13 2011 Andy Grover <agrover@redhat.com> - 1:1.1.fb2-1
- New upstream release

* Tue Dec 6 2011 Andy Grover <agrover@redhat.com> - 1:1.1.fb1-1
- New upstream source and release
- Remove patches:
  * python-configshell-remove-epydoc-dep.patch
  * python-configshell-git-version.patch

* Mon Nov 21 2011 Andy Grover <agrover@redhat.com> - 1:1.1-2
- Properly update changelog
- Sync version with upstream, Epoch used
- Change Source URL to intermediate github repo

* Fri Sep 23 2011 Andy Grover <agrover@redhat.com> - 1.99.1.git987b63b-5
* Rebuild

* Thu Aug 25 2011 Andy Grover <agrover@redhat.com> - 1.99.1.git987b63b-4
- Add patch
  - python-configshell-remove-epydoc-dep.patch

* Wed Aug 17 2011 Andy Grover <agrover@redhat.com> - 1.99.1.git987b63b-3
- Address comments from spec review
  - drop examples/myshell from doc, it hasn't been updated for API change
  - Fully document procedure to generate source .tar.gz
  - Remove "." from summary
  - Remove commented-out spec todos and other cruft

* Mon Aug 1 2011 Andy Grover <agrover@redhat.com> - 1.99.1.git987b63b-2
- Update to latest git version
- Add urwid builddep

* Tue May 10 2011 Andy Grover <agrover@redhat.com> - 1.99.1.git987b63b-1
- Initial packaging
