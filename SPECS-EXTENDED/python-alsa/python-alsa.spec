Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%define		baseversion 1.2.14

Summary:	Python binding for the ALSA library
Name:		python-alsa
Version:	%{baseversion}
Release:	4%{?dist}
License:	LGPL-2.1-or-later
Source0:	https://www.alsa-project.org/files/pub/pyalsa/pyalsa-%{version}.tar.bz2
Source1:  %{name}-LICENSE.txt
URL:		http://www.alsa-project.org/
BuildRequires:	alsa-lib-devel >= %{version}
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
BuildRequires:  python3-pytest
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:	gcc

# Filter private shared library provides
%global __provides_exclude_from ^(%{python2_sitearch}|%{python3_sitearch})/.*\\.so$

%global _description \
Python bindings for the ALSA library.

%description %_description

%package -n python3-alsa
Summary: %summary
%{?python_provide:%python_provide python3-alsa}

%description -n python3-alsa %_description

%prep
%autosetup -n pyalsa-%{version} -p 1
mv %{SOURCE1} ./LICENSE.txt

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel
	
%install
%pyproject_install
%pyproject_save_files '*'

%check
%pyproject_check_import

%files -n python3-alsa -f %{pyproject_files}
%license LICENSE.txt

%changelog
* Fri Sep 26 2025 Sumit Jena <v-sumitjena@microsoft.com> - 1.2.14-1
- Upgrade to version 1.2.14
- Added check section.

* Wed Dec 18 2024 Sumit Jena <v-sumitjena@microsoft.com> - 1.2.12-4
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 11 2024 Python Maint <python-maint@redhat.com> - 1.2.12-2
- Rebuilt for Python 3.13

* Tue Jun 11 2024 Jaroslav Kysela <perex@perex.cz> - 1.2.12-1
- Updated to 1.2.12

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.2.7-10
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.2.7-6
- Rebuilt for Python 3.12

* Wed Mar 08 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.2.7-5
- migrated to SPDX license

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.2.7-2
- Rebuilt for Python 3.11

* Tue May 31 2022 Jaroslav Kysela <perex@perex.cz> - 1.2.7-1
- Updated to 1.2.6

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 06 2021 Jaroslav Kysela <perex@perex.cz> - 1.2.6-1
- Updated to 1.2.6

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.1.6-16
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 10 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.1.6-14
- Patch for Python 3.10.

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.1.6-12
- BR python3-setuptools

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.1.6-11
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.6-9
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.6-8
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 09 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.6-5
- Subpackage python2-alsa has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Wed Jul 25 2018 Gwyn Ciesla <limburgher@gmail.com> - 1.1.6-4
- BR fix.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1.6-2
- Rebuilt for Python 3.7

* Tue Apr 03 2018 Jaroslav Kysela <perex@perex.cz> - 1.1.6-1
- Updated to 1.1.6
- Added python3-alsa package

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.29-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Feb 07 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.0.29-10
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.0.29-9
- Python 2 binary package renamed to python2-alsa
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.29-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.29-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.0.29-6
- Rebuild due to bug in RPM (RHBZ #1468476)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.29-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.29-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 26 2015 Jaroslav Kysela <perex@perex.cz> - 1.0.29-1
- Updated to 1.0.29

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.26-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Sep  6 2012 Jaroslav Kysela <jkysela@redhat.com> - 1.0.26-1
- Updated to 1.0.26

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 27 2012 Jon Ciesla <limburgher@gmail.com> - 1.0.25-1
- New upstream.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Mar 29 2011 Robin Lee <cheeselee@fedoraproject.org> - 1.0.24-1
- Update to 1.0.24 (#674260)
- Filter private shared library provides
- Clean up unused definitions

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.22-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.0.22-1.1
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Jan 25 2010 Andy Shevchenko <andy@smile.org.ua> - 1.0.22-1
- update to release 1.0.22 (should fix bug #558229)

* Sat Sep 05 2009 Andy Shevchenko <andy@smile.org.ua> - 1.0.21-1
- update to release 1.0.21

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.20-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 11 2009 Andy Shevchenko <andy@smile.org.ua> - 1.0.20-1
- update to release 1.0.20

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.17-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0.17-2
- Rebuild for Python 2.6

* Fri Jul 25 2008 Andy Shevchenko <andy@smile.org.ua> - 1.0.17-1
- update to release 1.0.17

* Sun May 04 2008 Andy Shevchenko <andy@smile.org.ua> - 1.0.16-1
- update to release 1.0.16

* Wed Feb 20 2008 Jesse Keating <jkeating@redhat.com> - 1.0.15-3
- Rebuild for GCC 4.3

* Fri Jan 04 2008 Andy Shevchenko <andy@smile.org.ua> 1.0.15-2
- include egg-info to the files: catched from rawhide mass rebuild
  (http://sunsite.mff.cuni.cz/rawhide20071220-gcc43/fails-even-with-41/python-alsa-1.0.15-1.fc8.log)

* Wed Oct 17 2007 Andy Shevchenko <andy@smile.org.ua> 1.0.15-1
- update to relase 1.0.15

* Sun Oct 14 2007 Andy Shevchenko <andy@smile.org.ua> 1.0.15-0.4.rc2
- require at least ALSA 1.0.15

* Fri Oct 12 2007 Andy Shevchenko <andy@smile.org.ua> 1.0.15-0.3.rc2
- don't put executable files to the documentation

* Thu Oct 11 2007 Andy Shevchenko <andy@smile.org.ua> 1.0.15-0.2.rc2
- prepare to include to the Fedora
  (https://bugzilla.redhat.com/show_bug.cgi?id=327351)

* Wed Oct 10 2007 Andy Shevchenko <andy@smile.org.ua> 1.0.15-0.1.rc2
- initial build
