Vendor:         Microsoft Corporation
Distribution:   Mariner
%define		baseversion 1.1.6

Summary:	Python binding for the ALSA library
Name:		python-alsa
Version:	%{baseversion}
Release:	12%{?dist}
License:	LGPLv2+
Source0:	ftp://ftp.alsa-project.org/pub/pyalsa/pyalsa-%{version}.tar.bz2
Source1:  %{name}-LICENSE.txt
URL:		http://www.alsa-project.org/
BuildRequires:	alsa-lib-devel >= %{version}
BuildRequires:	python3-devel
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
%autosetup -n pyalsa-%{version}
mv %{SOURCE1} ./LICENSE.txt

%build
%py3_build
	
%install
%py3_install

%files -n python3-alsa
%license LICENSE.txt
%{python3_sitearch}/*

%changelog
* Fri Dec 10 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.1.6-12
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.6-11
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
