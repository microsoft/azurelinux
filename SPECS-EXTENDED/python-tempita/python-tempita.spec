Vendor:         Microsoft Corporation
Distribution:   Mariner

Name:           python-tempita
Version:        0.5.2
Release:        1%{?dist}
Summary:        A very small text templating language

License:        MIT
URL:            http://pythonpaste.org/tempita/
Source0:        https://pypi.python.org/packages/source/T/Tempita/Tempita-%{version}.tar.gz
Source1:        %{name}-LICENSE.txt
Patch0001:      0001-Fix-SyntaxError-multiple-exception-types-must-be-par.patch

BuildArch:      noarch

BuildRequires: python3-devel
BuildRequires: python3-setuptools

%global _description\
Tempita is a small templating language for text substitution.

%description %_description

%package -n python3-tempita
Summary:        A very small text templating language
%{?python_provide:%python_provide python3-tempita}
# Without one of these there's no aes implementation which means there's no way to
# have encrypted cookies.  This is a reduction in features over the python2 version.
# Currently there's no working python3 port for either:
# http://allmydata.org/trac/pycryptopp/ticket/35
# http://lists.dlitz.net/pipermail/pycrypto/2010q2/000253.html
#%if 0%{?fedora}
#Requires: python3-pycryptopp
#%else
#Requires: python3-crypto
#%endif

%description -n python3-tempita
Tempita is a small templating language for text substitution.


%prep
%autosetup -n Tempita-%{version} -p1
cp %{SOURCE1} ./LICENSE.txt


%build
# Mariner's version of 'python3-setuptools' removed support for the "use_2to3" option.
sed -i '/use_2to3/d' setup.py
%py3_build


%install
%py3_install


%files -n python3-tempita
%license LICENSE.txt
%{python3_sitelib}/tempita/
%{python3_sitelib}/*.egg-info/

%changelog
* Fri Feb 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.5.2-1
- Fixing build for updated version of "python3-setuptools".
- Updating to version 0.5.2 and applying a build patch from Fedora 36 (license: MIT).

* Fri Dec 10 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.5.1-28
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.5.1-27
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep 25 2019 Miro Hrončok <mhroncok@redhat.com> - 0.5.1-25
- Subpackage python2-tempita has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 0.5.1-24
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 17 2018 Miro Hrončok <mhroncok@redhat.com> - 0.5.1-20
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.5.1-19
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.5.1-17
- Python 2 binary package renamed to python2-tempita
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.5.1-14
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-13
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 28 2016 Dan Horák <dan[at]danny.cz> - 0.5.1-11
- spec cleanup

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-10
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 0.5.1-4
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 0.5.1-3
- remove rhel logic from with_python3 conditional

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 24 2012 Ricky Zhou <ricky@fedoraproject.org> - 0.5.1-1
- Update to 0.5.1.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 25 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.4-6
- rebuild with python3.2
  http://lists.fedoraproject.org/pipermail/devel/2010-August/141368.html

* Tue Aug  3 2010 Kyle VanderBeek <kylev@kylev.com> - 0.4-5
- Add python3-tempita subpackage.

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sat Jun 26 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.4-3
- Cosmetic fixes -- BR python-setuptools instead of python-setuptools-devel
- Conditionalize python_sitelib definition
- trailing slash for directory in %%files

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 20 2009 Ricky Zhou <ricky@fedoraproject.org> - 0.4-1
- Upstream released a new version.

* Tue Apr 14 2009 Ricky Zhou <ricky@fedoraproject.org> - 0.3-3
- Change define to global.
- Remove old >= 8 conditional.
- Remove unnecessary BuildRequires on python-devel.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 06 2008 Ricky Zhou <ricky@fedoraproject.org> - 0.3-1
- Upstream released a new version.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0-4
- Rebuild for Python 2.6

* Mon Jul 07 2008 Ricky Zhou <ricky@fedoraproject.org> - 0.2-2
- Add %%check section.

* Sat Jun 14 2008 Ricky Zhou <ricky@fedoraproject.org> - 0.2-1
- Initial RPM Package.
