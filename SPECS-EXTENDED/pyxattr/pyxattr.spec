Name:           pyxattr
Summary:        Extended attributes library wrapper for Python
Version:        0.7.1
Release:        4%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://pyxattr.k1024.org/
Source0:        %{URL}/downloads/%{name}-%{version}.tar.gz
Source1:        %{URL}/downloads/%{name}-%{version}.tar.gz.asc
Source2:        https://k1024.org/files/key.asc

BuildRequires:  gcc
BuildRequires:  libattr-devel
BuildRequires:  python3-devel
BuildRequires:  gnupg2
BuildRequires:  %{py3_dist pytest}

%global _description %{expand:
Python extension module wrapper for libattr. It allows to query, list,
add and remove extended attributes from files and directories.}

%description %_description

%package -n python3-%{name}
Summary: %{summary}
%{?python_provide:%python_provide python3-%{name}}

%description -n python3-%{name} %_description

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup

%build
%py3_build

%install
%py3_install

%check
# selinux in koji produces unexpected xattrs for tests
export TEST_IGNORE_XATTRS=security.selinux
# the module is just a C extension => need to add the installed destination to
# PYTHONPATH, otherwise it won't be found
export PYTHONPATH=%{buildroot}%{python3_sitearch}:$PYTHONPATH
python3 -m pytest test

%files -n python3-%{name}
%{python3_sitearch}/xattr.cpython-??*
%{python3_sitearch}/*egg-info
%license COPYING
%doc NEWS README.md

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.7.1-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 03 2019 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.7.1-2
- Backport RPM specification improvements from sister project pylibacl

* Tue Nov 26 2019 Dan Čermák <dan.cermak@cgc-instruments.com> - 0.7.1-1
- Update to 0.7.1
- Drop python2 subpackage
- Add gpg signature check

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jul 14 2019 Dan Čermák <dan.cermak@cgc-instruments.com> - 0.6.1-1
- Bump version to 0.6.1
- Simplify spec file

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 24 2018 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.5.6-2
- Backport patch from 0.6.1 to fix issues with missing ENOATTR in libatttr 2.4.48
  in Fedora 28/29 (#1603242, related to #1601482) - 0.5.6-1 was broken also in F28

* Thu Jul 19 2018 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.5.6-1
- Upgrade to 0.5.6 (transitional step before 0.6.x for Fedora <29)
- Drop Py_ssize_t patch applied upstream
- Update download URL

* Thu Jul 12 2018 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.5.3-18
- Add gcc to BuildRequires - https://fedoraproject.org/wiki/Changes/Remove_GCC_from_BuildRoot

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 0.5.3-17
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.5.3-15
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Tue Dec 26 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.5.3-14
- Also add Provides for the old name without %%_isa

* Sun Aug 13 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.5.3-13
- Python 2 binary package renamed to python2-pyxattr
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.5.3-9
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-8
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 14 2015 Robert Kuska <rkuska@redhat.com> - 0.5.3-6
- Rebuilt for Python3.5 rebuild
- Change pattern for listed so file to reflect new naming in py35

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Aug  7 2014 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.5.3-3
- add Mark Hamzy's patch to fix issue with PPC builds (bug 1127310)

* Mon Aug  4 2014 Tom Callaway <spot@fedoraproject.org> - 0.5.3-2
- fix license handling

* Sat Jun 28 2014 Miro Hrončok <mhroncok@redhat.com> - 0.5.3-1
- Updated to 0.5.3
- Updated the website
- Updated download URL to PyPI
- Removed useless Require of python >= 2.2
- Use %%{pythonX_sitearch} macros
- Removed BuildRoot definition, %%clean section and rm -rf at the beginning of %%install
- Introduced Python 3 subpackage
- Introduced %%check and run the test suite

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.5.1-1
- updated to 0.5.1
- fix bugs found with cpychecker (bug 809974)

* Mon Feb 27 2012 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.5.0-5
- remove prodive/obsolete of python-xattr (bug 781838)
- fix problem with mixed use of tabs and spaces

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Dec 27 2009 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.5.0-1
- updated to 0.5.0
- added support for unicode filenames (bug 479417)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 6 2008 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.4.0-2
- added python-setuptools in BuildRequires which is needed in build process
since version 0.4.0 (thanks to Kevin Fenzi)

* Fri Dec 5 2008 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.4.0-1
- updated to 0.4.0
- License Tag adjusted to current licensing LGPLv2+
- modified Python Eggs support due to its usage in source distribution 

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.2.2-4
- Rebuild for Python 2.6

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.2.2-3
- Autorebuild for GCC 4.3

* Tue Jan 15 2008 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.2.2-2
- added compatibility with Python Eggs forced in F9 

* Mon Aug 27 2007 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.2.2-1
- upgraded to 0.2.2

* Sun Aug 26 2007 Kevin Fenzi <kevin@tummy.com> - 0.2.1-5
 - Updated License tag

* Wed Apr 25 2007 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.2.1-4
 - added Provides/Obsoletes tags

* Sat Apr 21 2007 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.2.1-3
 - removed redundant after name change "exclude" tag
 - comments cleanup

* Wed Apr 18 2007 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.2.1-2
 - applied suggestions from Kevin Fenzi
 - name changed from python-xattr to pyxattr
 - corrected path to the source file

* Thu Apr 5 2007 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.2.1-1
 - updated to 0.2.1
 - added python-devel in BuildRequires
 - added more doc files
 - added Provides section
 - modified to Fedora Extras requirements

* Sun Sep 11 2005 Dag Wieers <dag@wieers.com> - 0.2-1 - +/
- Initial package. (using DAR)
