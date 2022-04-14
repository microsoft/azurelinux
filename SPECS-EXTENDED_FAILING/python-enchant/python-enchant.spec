Vendor:         Microsoft Corporation
Distribution:   Mariner
# Work around a problem with libenchant versioning
# (python-enchant-1.3.1 failed to work with enchant-1.4.2-2.fc10)
%global enchant_dep enchant >= 1.5.0
%global srcname enchant

Name:           python-enchant
Version:        2.0.0
Release:        12%{?dist}
Summary:        Python bindings for Enchant spellchecking library

License:        LGPLv2+
URL:            http://packages.python.org/pyenchant/
Source0:        https://files.pythonhosted.org/packages/source/p/py%{srcname}/py%{srcname}-%{version}.tar.gz#/python-py%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  enchant-devel

%description
PyEnchant is a spellchecking library for Python, based on the Enchant
library by Dom Lachowicz.


%package -n python3-%{srcname}
Summary:        Python 3 bindings for Enchant spellchecking library

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
# For running tests
BuildRequires:  python3-nose

Requires:       %{enchant_dep}

%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
PyEnchant is a spellchecking library for Python 3, based on the Enchant
library by Dom Lachowicz.

%prep
%setup -q -n py%{srcname}-%{version}
# Remove bundled egg-info
rm -rf py%{srcname}.egg-info

find . -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'

%build
%py3_build

%install
%py3_install

# Directories used in windows build
rm -rf $RPM_BUILD_ROOT/%{python3_sitelib}/%{srcname}/lib
rm -rf $RPM_BUILD_ROOT/%{python3_sitelib}/%{srcname}/share


%check
pushd $RPM_BUILD_ROOT/%{python3_sitelib}
# There is no dictionary for language C, need to use en_US
nosetests-3
popd


%files -n python3-%{srcname}
%doc README.txt TODO.txt
%license LICENSE.txt
%dir %{python3_sitelib}/%{srcname}
%dir %{python3_sitelib}/%{srcname}/__pycache__
%dir %{python3_sitelib}/%{srcname}/checker
%dir %{python3_sitelib}/%{srcname}/checker/__pycache__
%dir %{python3_sitelib}/%{srcname}/tokenize
%dir %{python3_sitelib}/%{srcname}/tokenize/__pycache__
%{python3_sitelib}/%{srcname}/*.py
%{python3_sitelib}/%{srcname}/__pycache__/*.py[co]
%{python3_sitelib}/%{srcname}/checker/*.py
%{python3_sitelib}/%{srcname}/checker/__pycache__/*.py[co]
%{python3_sitelib}/%{srcname}/tokenize/*.py
%{python3_sitelib}/%{srcname}/tokenize/__pycache__/*.py[co]
%{python3_sitelib}/py%{srcname}-%{version}-py?.?.egg-info


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.0-12
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Sep 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.0.0-10
- Subpackage python2-enchant has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 2.0.0-9
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.0.0-6
- Drop explicit locale setting for python3, use C.UTF-8 for python2
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 17 2018 Miro Hrončok <mhroncok@redhat.com> - 2.0.0-4
- Rebuilt for Python 3.7

* Thu Mar 15 2018 Charalampos Stratakis <cstratak@redhat.com> - 2.0.0-3
- Conditionalize the python2 subpackage

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 11 2017 Charalampos Stratakis <cstratak@redhat.com> - 2.0.0-1
- Update to 2.0.0

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Charalampos Stratakis <cstratak@redhat.com> - 1.6.10-1
- Update to 1.6.10

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.6.8-2
- Rebuild for Python 3.6

* Tue Nov 22 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.6.8-1
- Update to 1.6.8

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.6-8
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Feb 10 2016 David Shea <dshea@redhat.com> - 1.6.6-7
- Fix TypeError at shutdown

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 31 2015 Ville Skyttä <ville.skytta@iki.fi> - 1.6.6-5
- Add dependency on enchant to python3 subpackage

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.6-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Nov 10 2015 Ville Skyttä <ville.skytta@iki.fi> - 1.6.6-3
- Rebuild for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 26 2015 Radek Novacek <rnovacek@redhat.com> 1.6.6-1
- Update to 1.6.6
- Enable python3 tests in the check section

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.5-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 1.6.5-13
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue Aug 06 2013 Radek Novacek <rnovacek@redhat.com> 1.6.5-12
- Disable distribute setup

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 01 2012 Radek Novacek <rnovacek@redhat.com> 1.6.5-9
- Enable tests in %%check

* Wed Oct 31 2012 Radek Novacek <rnovacek@redhat.com> 1.6.5-8
- Fix upstream url and source url

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 1.6.5-7
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 12 2011 Radek Novacek <rnovacek@redhat.com> 1.6.5-4
- Release bump to ensure upgrade path from F16

* Mon Oct 10 2011 David Malcolm <dmalcolm@redhat.com> - 1.6.5-3
- add python3 subpackage

* Fri Sep 23 2011 Radek Novacek <rnovacek@redhat.com> 1.6.5-2
- Obsolete old arch-specific version

* Fri Sep 23 2011 Radek Novacek <rnovacek@redhat.com> 1.6.5-1
- Update to version 1.6.5
- Change architecture to noarch
- Change python_sitearch to python_sitelib
- Changelog in no longer in source tarball
- Remove nonpacked files

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Feb  1 2010 Stepan Kasal <skasal@redhat.com> - 1.3.1-6
- add a require to work around a problem with libenchant versioning

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.3.1-3
- Rebuild for Python 2.6

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3.1-2
- Autorebuild for GCC 4.3

* Tue Dec 11 2007 Roozbeh Pournader <roozbeh@farsiweb.info> - 1.3.1-1
- Update to 1.3.1
- Change license tag to LGPLv2+

* Sat Jan 13 2007 Roozbeh Pournader <roozbeh@farsiweb.info> - 1.3.0-1
- Update to 1.3.0
- Add ChangeLog and TODO.txt as documentation

* Sat Dec 09 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 1.2.0-2
- Rebuild for Python 2.5

* Tue Nov  7 2006 José Matos <jamatos[AT]fc.up.pt> - 1.2.0-1
- New upstream release

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 1.1.5-5
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 20 2006 José Matos <jamatos[AT]fc.up.pt> - 1.1.5-4
- Rebuild for FC-6.
- Unghost .pyo files.

* Tue Feb 14 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 1.1.5-3
- Rebuild for Fedora Extras 5

* Tue Feb 07 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 1.1.5-2
- Rebuild

* Sat Feb 04 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 1.1.5-1
- Update to 1.1.5

* Wed Feb 01 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 1.1.3-3
- Use %%{python_sitearch} instead of %%{python_sitelib} (for x86_64)

* Wed Feb 01 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 1.1.3-2
- Remove %%{enchant_dir} macro
- Add %%dir for architecture-specific directory
- Add "Provides:" for PyEnchant
- Remove "Requires:" on enchant (Brian Pepple)

* Mon Jan 09 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 1.1.3-1
- Initial packaging
