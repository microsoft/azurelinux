%bcond_with python2

Name:           python-cheetah
Version:        3.2.4
Release:        4%{?dist}
Summary:        Template engine and code generator

License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://cheetahtemplate.org/
Source:         https://github.com/CheetahTemplate3/cheetah3/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  gcc

%global _description\
Cheetah is an open source template engine and code generation tool,\
written in Python. It can be used standalone or combined with other\
tools and frameworks. Web development is its principal use, but\
Cheetah is very flexible and is also being used to generate C++ code,\
Java, SQL, form emails and even Python code.

%description %{_description}

%if %{with python2}
%package -n python2-cheetah
Summary: %summary
%{?python_provide:%python_provide python2-cheetah}

BuildRequires: python2-devel
BuildRequires: python2-setuptools


BuildRequires: python2-pygments

%description -n python2-cheetah %_description

%endif

%package -n python3-cheetah
Summary: %summary
%{?python_provide:%python_provide python3-cheetah}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-markdown
BuildRequires: python3-pygments

%description -n python3-cheetah %_description


%prep
%autosetup -p1 -n cheetah3-%{version}

# remove unnecessary shebang lines to silence rpmlint
%{__sed} -i -e '/^#!/,1d' Cheetah/Tests/*.py \
    Cheetah/CheetahWrapper.py Cheetah/DirectiveAnalyzer.py \
    Cheetah/Filters.py Cheetah/NameMapper.py Cheetah/Servlet.py \
    Cheetah/Templates/SkeletonPage.py Cheetah/Tools/SiteHierarchy.py \
    Cheetah/Version.py

%build
%if %{with python2}
%py2_build
%endif

%py3_build

%install
%if %{with python2}
%py2_install

EGG_INFO=(%{buildroot}/%{python2_sitearch}/Cheetah*.egg-info)
cp -r $EGG_INFO ${EGG_INFO//Cheetah3/Cheetah}
sed -i "s/Name: Cheetah3/Name: Cheetah/" ${EGG_INFO//Cheetah3/Cheetah}/PKG-INFO
rm %{buildroot}%{_bindir}/*
%endif

%py3_install


%check
export PATH="%{buildroot}/%{_bindir}:$PATH"
export PYTHONPATH="%{buildroot}/%{python3_sitearch}"
%{buildroot}/%{_bindir}/cheetah test

%if %{with python2}
%files -n python2-cheetah
%license LICENSE
%doc ANNOUNCE.rst README.rst TODO BUGS

%{python2_sitearch}/Cheetah
%{python2_sitearch}/Cheetah*.egg-info
%endif

%files -n python3-cheetah
%license LICENSE
%doc ANNOUNCE.rst README.rst TODO BUGS

%{_bindir}/cheetah*

%{python3_sitearch}/Cheetah
%{python3_sitearch}/Cheetah*.egg-info

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.2.4-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 18 2019 Patrik Novotný <panovotn@redhat.com> - 3.2.4-2
- Remove python2 package

* Mon Nov 18 2019 Patrik Novotný <panovotn@redhat.com> - 3.2.4-1
- Rebase to upstream release 3.2.4

* Tue Sep 17 2019 Nicolas Chauvet <kwizart@gmail.com> - 3.2.3-2
- Keep python2 despite python2-markdown is missing

* Tue Sep 17 2019 Nicolas Chauvet <kwizart@gmail.com> - 3.2.3-1
- Update to 3.2.3
- Don't own python_sitearch - rhbz#1672098

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.1.0-9
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 mskalick@redhat.com - 3.1.0-5
- Remove python2 tests - was calling python3 subprocesses internally

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.1.0-4
- Rebuilt for Python 3.7

* Tue Jun 12 2018 Lumír Balhar <lbalhar@redhat.com> - 3.1.0-3
- Fixed python2 conditions
- Removed usage of %%{py3dir}

* Wed Mar 28 2018 Marek Skalický <mskalick@redhat.com> - 3.1.0-2
- Use python3 shebang in binary files

* Tue Mar 20 2018 Marek Skalický <mskalick@redhat.com> - 3.1.0-1
- Rebase to latest upstream release

* Tue Feb 27 2018 Marek Skalický <mskalick@redhat.com> - 3.0.0-20
- Add missing BuildRequires: gcc/gcc-c++

* Thu Feb 22 2018 Marek Skalický <mskalick@redhat.com> - 3.0.0-19
- Add Cheetah egg-info for backward compatibility

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.4.4-17
- Python 2 binary package renamed to python2-cheetah
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.4-13
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 31 2014 Tom Callaway <spot@fedoraproject.org> - 2.4.4-9
- fix license handling

* Mon Jul 21 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 2.4.4-8
- Since we're leaving out the dep on markdown in the rpm requirements we need
  to leave it out of egginfo as well otherwise pkg_resources using code breaks

* Thu Jun 19 2014 Matthew Miller <mattdm@fedoraproject.org> - 2.4.4-7
- remove python-markdown and python-pygments hard dependencies

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Mike Bonnet <mikeb@redhat.com> - 2.4.4-1
- update to the 2.4.4 release

* Mon Oct 18 2010 Mike Bonnet <mikeb@redhat.com> - 2.4.3-1
- update to the 2.4.3 release

* Mon Oct 18 2010 Mike Bonnet <mikeb@redhat.com> - 2.4.2.1-3
- Fix compatibility with Python 2.7

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon May 24 2010 Mike Bonnet <mikeb@redhat.com> - 2.4.2.1-1
- update to the 2.4.2.1 release

* Thu Jan 14 2010 Mike Bonnet <mikeb@redhat.com> - 2.4.1-3
- remove unnecessary shebang lines to silence rpmlint

* Fri Jan  8 2010 Mike Bonnet <mikeb@redhat.com> - 2.4.1-2
- fix Source url

* Mon Jan  4 2010 Mike Bonnet <mikeb@redhat.com> - 2.4.1-1
- update to the 2.4.1 release

* Tue Oct 20 2009 Mike Bonnet <mikeb@redhat.com> - 2.2.2-2
- backport significant improvements to utf-8/unicode handling from upstream

* Mon Sep 14 2009 Mike Bonnet <mikeb@redhat.com> - 2.2.2-1
- update to the 2.2.2 release
- add dependency on python-markdown for consistency with the egg-info

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun  5 2009 Mike Bonnet <mikeb@redhat.com> - 2.2.1-1
- update to the 2.2.1 release

* Mon May 18 2009 Mike Bonnet <mikeb@redhat.com> - 2.2.0-1
- update to the 2.2.0 release
- remove unneeded importHook() patch, it has been included upstream

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 1 2008 Toshio Kuratomi <toshio@fedoraproject.org> - 2.0.1-4
- Fix cheetah enough that it will pass its unittests on python-2.6.  This has
  actually been broken since py-2.5 and this fix is only a workaround.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0.1-3
- Rebuild for Python 2.6

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.0.1-2
- Autorebuild for GCC 4.3

* Tue Dec  4 2007 Mike Bonnet <mikeb@redhat.com> - 2.0.1-1
- update to the 2.0.1 release

* Mon Oct 15 2007 Mike Bonnet <mikeb@redhat.com> - 2.0-1
- update to the 2.0 release

* Tue Aug 21 2007 Mike Bonnet <mikeb@redhat.com> - 2.0-0.7.rc8
- rebuild for F8

* Thu May  3 2007 Mike Bonnet <mikeb@redhat.com> - 2.0-0.6.rc8
- bump release for rebuild

* Mon Apr 23 2007 Mike Bonnet <mikeb@redhat.com> - 2.0-0.5.rc8
- update to 2.0rc8

* Mon Jan  8 2007 Mike Bonnet <mikeb@redhat.com> - 2.0-0.4.rc7
- use setuptools and install setuptools metadata

* Sun Dec 10 2006 Mike Bonnet <mikeb@redhat.com> - 2.0-0.3.rc7
- rebuild against python 2.5
- remove obsolete python-abi Requires:

* Mon Sep 11 2006 Mike Bonnet <mikeb@redhat.com> - 2.0-0.2.rc7
- un-%%ghost .pyo files

* Thu Jul 13 2006 Mike Bonnet <mikeb@redhat.com> - 2.0-0.1.rc7
- update to 2.0rc7
- change %%release format to conform to Extras packaging guidelines

* Sun May 21 2006 Mike Bonnet <mikeb@redhat.com> - 2.0-0.rc6.0
- update to 2.0rc6
- run the included test suite after install

* Thu Feb 16 2006 Mike Bonnet <mikeb@redhat.com> - 1.0-2
- Rebuild for Fedora Extras 5

* Wed Dec  7 2005 Mike Bonnet <mikeb@redhat.com> - 1.0-1
- Initial version
