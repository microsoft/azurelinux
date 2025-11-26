%global srcname markdown
%global pkgname markdown
Summary:        Markdown implementation in Python
Name:           python-%{pkgname}
Version:        3.9
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://python-markdown.github.io/
# Cannot use %{version} as URL uses 3.9.0 while Version tag is 3.9
Source0:        https://github.com/Python-Markdown/markdown/releases/download/3.9.0/markdown-3.9.tar.gz#/python-%{srcname}-%{version}.tar.gz
BuildArch:      noarch

%description
This is a Python implementation of John Grubers Markdown. It is
almost completely compliant with the reference implementation, though
there are a few very minor differences.

%package -n python%{python3_pkgversion}-%{pkgname}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pkgname}}
Summary:        Markdown implementation in Python
BuildRequires:  PyYAML
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-importlib-metadata
BuildRequires:  python%{python3_pkgversion}-pip
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-tidy
BuildRequires:  python%{python3_pkgversion}-wheel
BuildRequires:  python%{python3_pkgversion}-zipp
Requires:       python%{python3_pkgversion}-importlib-metadata

%description -n python%{python3_pkgversion}-%{pkgname}
This is a Python implementation of John Gruber's Markdown. It is
almost completely compliant with the reference implementation, though
there are a few known issues.

%prep
%autosetup -p1 -n %{srcname}-%{version}

# fix pyproject.toml to comply with PEP 621
sed -i '/license-files/d' pyproject.toml
sed -i 's/^license = "BSD-3-Clause"/license = {text = "BSD-3-Clause"}/' pyproject.toml

%build
%pyproject_wheel

%install
%pyproject_install

# process license file
PYTHONPATH=%{buildroot}%{python3_sitelib} \
  %{buildroot}%{_bindir}/markdown_py \
  LICENSE.md > LICENSE.html

%check
%{__python3} -m unittest discover -v


%files -n python%{python3_pkgversion}-%{pkgname}
# temporarily skip packaging docs - see also
# https://github.com/Python-Markdown/markdown/issues/621
#doc python3/build/docs/*
%license LICENSE.*
%{python3_sitelib}/*
%{_bindir}/markdown_py

%changelog
* Tue Oct 07 2025 Sudipta Pandit <sudpandit@microsoft.com> - 3.9-1
- Upgrade to version 3.9

* Tue Apr 29 2025 Riken Maharjan <rmaharjan@microsoft.com> -  3.5.2-2
- Use proper ptest command to run the test.

* Fri Feb 16 2024 Andrew Phelps <anphel@microsoft.com> - 3.5.2-1
- Upgrade to version 3.5.2
- Add BR for python3-pip and python3-wheel
- Remove unneeded python2 conflicts

* Wed Nov 30 2022 Riken Maharjan <rmaharjan@microsoft.com> - 3.2.2-4
- Move to Core.
- License verified.

* Mon Dec 14 2020 Ruying <v-ruyche@microsoft.com> - 3.2.2-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Make python3-importlib-metadata requirements default.
- Add python3-zipp as a build requirement.

* Sat May 16 2020 Thomas Moschny <thomas.moschny@gmx.de> - 3.2.2-2
- Update BRs.

* Sat May 16 2020 Thomas Moschny <thomas.moschny@gmx.de> - 3.2.2-1
- Update to 3.2.2.

* Sat Feb 22 2020 Thomas Moschny <thomas.moschny@gmx.de> - 3.2.1-1
- Update to 3.2.1.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.1.1-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 3.1.1-5
- Rebuilt for Python 3.8

* Tue Aug 13 2019 Thomas Moschny <thomas.moschny@gmx.de> - 3.1.1-4
- Drop versioned binaries.

* Tue Aug 13 2019 Gwyn Ciesla <gwync@protonmail.com> - 3.1.1-3
- Drop Python 2.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat May 25 2019 Thomas Moschny <thomas.moschny@gmx.de> - 3.1.1-1
- Update to 3.1.1.

* Fri May 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.1-2
- Move /usr/bin/markdown_py to python3-markdown (#1705777)

* Tue Mar 26 2019 Thomas Moschny <thomas.moschny@gmx.de> - 3.1-1
- Update to 3.1.

* Mon Mar 25 2019 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.1-1
- Update to 3.0.1.
- Simplify spec file.
- CLI tool uses Python3 now.
- Update BRs.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 17 2018 Miro Hrončok <mhroncok@redhat.com> - 2.6.11-3
- Rebuilt for Python 3.7

* Sun Jun  3 2018 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.11-2
- Try to fix a FTBFS with Python 3.7 (rhbz#1583678).

* Sun Feb 11 2018 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.11-1
- Update to 2.6.11.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 30 2017 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.9-2
- Fix BRs.

* Wed Aug 30 2017 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.9-1
- Update to 2.6.9.
- Allow building a python3 subpackage on EPEL7+.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 29 2017 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.8-1
- Update to 2.6.8.

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.6.7-2
- Rebuild for Python 3.6

* Sat Sep 24 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.7-1
- Update to 2.6.7.
- Update Source0 URL.

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.6-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Apr  5 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.6-1
- Update to 2.6.6.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Nov 29 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.5-1
- Update to 2.6.5.

* Sat Nov 21 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.4-1
- Update to 2.6.4.
- Follow updated Python packaging guidelines.

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 22 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.2-1
- Update to 2.6.2.

* Sat Mar 14 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.1-2
- Add license file.

* Sat Mar 14 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.6.1-1
- Update to 2.6.1.
- Apply updated Python packaging guidelines.

* Sun Feb 22 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.6-1
- Update to 2.6.
- Update the upstream URL.

* Sun Nov 23 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.5.2-1
- Update to 2.5.2.

* Thu Oct  2 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.5.1-1
- Update to 2.5.1.

* Thu Sep 25 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.5-1
- Update to 2.5.
- Add BR on PyYAML.

* Wed Jun  4 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.4.1-1
- Update to 2.4.1.

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue Apr 15 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.4-1
- Update to 2.4.
- Update Python3 conditional.
- Fix wrong line endings.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 19 2013 Thomas Moschny <thomas.moschny@gmx.dee> - 2.3.1-2
- Move python3 runtime dependency to python3 subpackage (rhbz#986376).

* Mon Apr  8 2013 Thomas Moschny <thomas.moschny@gmx.de> - 2.3.1-1
- Update to 2.3.1.

* Mon Mar 18 2013 Thomas Moschny <thomas.moschny@gmx.de> - 2.3-1
- Update to 2.3.
- Spec file cleanups.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 23 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.1-1
- Update to 2.2.1.

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 2.2.0-3
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jul 14 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.0-1
- Update to 2.2.0.
- Update url.
- Add patch from upstream git for failing test.

* Wed Feb  8 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.1-1
- Update to 2.1.1.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 17 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.0-1
- Update to 2.1.0.
- Fix rhel conditional.
- Binary has been renamed.
- Build python3 subpackage.
- Include documentation in HTML instead of Markdown format.
- Run tests.

* Wed Sep 07 2011 Jesse Keating <jkeating@redhat.com> - 2.0.3-4
- Set a version in the rhel macro

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Oct  8 2009 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.3-1
- Update to 2.0.3.

* Thu Aug 27 2009 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.1-3
- Add requirement on python-elementtree, which was a separate package
  before Python 2.5.
- Re-add changelog entries accidentally removed earlier.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 11 2009 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.1-1
- Update to 2.0.1.
- Upstream stripped .py of the cmdline script.

* Sat Apr 25 2009 Thomas Moschny <thomas.moschny@gmx.de> - 2.0-1
- Update to 2.0.
- Adjusted source URL.
- License changed to BSD only.
- Upstream now provides a script to run markdown from the cmdline.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.7-2
- Rebuild for Python 2.6

* Mon Aug  4 2008 Thomas Moschny <thomas.moschny@gmx.de> - 1.7-1
- New package.
