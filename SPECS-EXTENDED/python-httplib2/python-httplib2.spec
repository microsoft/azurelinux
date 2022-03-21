Vendor:         Microsoft Corporation
Distribution:   Mariner
%global srcname httplib2

Name:           python-%{srcname}
Version:        0.18.1
Release:        5%{?dist}
Summary:        Comprehensive HTTP client library
License:        MIT
URL:            https://pypi.python.org/pypi/httplib2
Source:         https://github.com/httplib2/httplib2/archive/v%{version}/%{srcname}-%{version}.tar.gz
#
# Patch to use the Fedora ca certs instead of the bundled ones
#
Patch1:         python-%{srcname}.certfile.patch

BuildArch:      noarch

%global _description\
A comprehensive HTTP client library that supports many features left out of\
other HTTP libraries.

%description %{_description}

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-cov
BuildRequires:  python3-pytest-forked
BuildRequires:  python3-pytest-flake8
BuildRequires:  python3-pytest-randomly
BuildRequires:  python3-pytest-timeout
BuildRequires:  python3-pytest-xdist
BuildRequires:  python3-six
BuildRequires:  python3-mock

%description -n python3-%{srcname} %{_description}


%prep
# The implementation is different for each major Python version
# and we need to install from separate directories
%setup -qc
pushd %{srcname}-%{version}
%autopatch -p1

# Drop coverage
sed -i '/--cov/d' setup.cfg
popd

mv %{srcname}-%{version} python3
rm -r python3/python2
mv python3/LICENSE .


%build
pushd python3
%py3_build
popd


%install
pushd python3
%py3_install
popd


%check
pushd python3
PYTHONPATH=%{buildroot}%{python3_sitelib} pytest -k 'not test_unknown_server'
popd

%files -n python3-%{srcname}
%license LICENSE
%doc python3/README.md
%{python3_sitelib}/%{srcname}-*.egg-info/
%{python3_sitelib}/%{srcname}/

%changelog
* Thu Feb 24 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.18.1-5
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.18.1-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jun 11 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.18.1-3
- BR fixes.

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 0.18.1-2
- Rebuilt for Python 3.9

* Wed May 20 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.18.1-1
- 0.18.1

* Wed May 20 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.18.0-1
- 0.18.0

* Wed May 20 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.17.4-1
- 0.17.4

* Mon May 04 2020 Miro Hrončok <mhroncok@redhat.com> - 0.17.3-3
- Fix python2/python3 mishmash (#1830222)
- Run tests

* Wed Apr 22 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.17.3-2
- Cleanup spec

* Wed Apr 22 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.17.3-1
- 0.17.3

* Mon Apr 13 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.17.2-1
- 0.17.2

* Thu Apr 02 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.17.1-1
- 0.17.1

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 24 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.17.0-1
- 0.17.0

* Fri Jan 17 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.16.0-1
- 0.16.0

* Thu Dec 19 2019 Gwyn Ciesla <gwync@protonmail.com> - 0.15.0-1
- 0.15.0

* Wed Nov 06 2019 Gwyn Ciesla <gwync@protonmail.com> - 0.14.0-1
- 0.14.0

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.13.1-2
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Thu Aug 22 2019 Kevin Fenzi <kevin@scrye.com> - 0.13.1-1
- Update to 0.13.1. Fixes bug #1742362

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 0.13.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 30 2019 Kevin Fenzi <kevin@scrye.com> - 0.13.0-1
- Update to 0.13.0.

* Tue Apr 23 2019 Kevin Fenzi <kevin@scrye.com> - 0.12.3-1
- Update to 0.12.3.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 21 2018 Kevin Fenzi <kevin@scrye.com> - 0.11.3-5
- Fix files section on python2 subpackage.

* Fri Jul 20 2018 Kevin Fenzi <kevin@scrye.com> - 0.11.3-4
- Fix FTBFS bug #1605725

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 0.11.3-2
- Rebuilt for Python 3.7

* Sun Jun 10 2018 Kevin Fenzi <kevin@scrye.com> - 0.11.3-1
- Update to 0.11.3. Fixes bug #1559204

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 11 2017 Nick Bebout <nb@fedoraproject.org> - 0.10.3-2
- Fix BuildRequires to use python2-* instead of python-*

* Sun Sep 10 2017 Nick Bebout <nb@fedoraproject.org> - 0.10.3-1
- Update to 0.10.3

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.9.2-7
- Python 2 binary package renamed to python2-httplib2
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.9.2-4
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Dec 26 2015 Kevin Fenzi <kevin@scrye.com> - 0.9.2-1
- Update to 0.9.2

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Apr 12 2015 Kevin Fenzi <kevin@scrye.com> 0.9.1-1
- Update to 0.9.1 and drop upstreamed patches

* Fri Apr 03 2015 Kevin Fenzi <kevin@scrye.com> 0.9-6
- Add patch to fix http over proxy. Fixes bug #857514
- Add patch to fix CVE-2013-2037. Fixes bug #958640
- Add patch to fix binary headers in python3. Fixes bug #1205127

* Mon Jan 12 2015 Adam Williamson <awilliam@redhat.com> - 0.9-5
- certfile.patch: use /etc/pki/tls not /etc/ssl/certs, patch python3 too

* Mon Jun 30 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 0.9-4
- Replace python-setuptools-devel BR with python-setuptools

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri May 23 2014 Kevin Fenzi <kevin@scrye.com> 0.9-1
- Update to 0.9

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.7.7-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 02 2013 Ding-Yi Chen <dchen at redhat.com> - 0.7.7-1
- Upstream update to 0.7.7

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 0.7.4-7
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Jul 27 2012 Ding-Yi Chen <dchen at redhat.com> - 0.7.4-6
- Fixed Bug 840968 - SSL errors when the site certificate contains
  subjectAltName but DNS is not in it

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Ding-Yi Chen <dchen at redhat.com> - 0.7.4-4
- Unify the spec file between EPEL and Fedora.

* Thu Jun 21 2012 Ding-Yi Chen <dchen at redhat.com> - 0.7.4-3
- Applied patch suggested by richardfearn@gmail.com regarding issue 208
- Fixed: Bug 832344 - Certification validation fails due to multiple 'dns' entries in subjectAltName

* Fri Jun 01 2012 Ding-Yi Chen <dchen at redhat.com> - 0.7.4-2
- Upstream update for Fedora

* Thu May 03 2012 Ding-Yi Chen <dchen at redhat.com> - 0.7.4-1
- Upstream update to 0.7.4
- Applied patch suggested in issue 208

* Fri Feb 24 2012 Ding-Yi Chen <dchen at redhat.com> - 0.7.2-1
- Upstream update to 0.7.2
  Which may fixed http://code.google.com/p/httplib2/issues/detail?id=62
  Note this version uses fedora's cert file bundle instead of httplib2
  default.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 29 2011 Ding-Yi Chen <dchen at redhat.com>  - 0.4.0-5.el6
- Apply that address python-httplib2 (GoogleCode Hosted) issue 39
  http://code.google.com/p/httplib2/issues/detail?id=39

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 25 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.6.0-4
- rebuild with python3.2
  http://lists.fedoraproject.org/pipermail/devel/2010-August/141368.html

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Apr 20 2010 Tom "spot" Callaway <tcallawa@redhat.com>
- minor spec cleanups
- enable python3 support

* Fri Apr 02 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> - 0.6.0-1
- version upgrade (#566721)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.4.0-2
- Rebuild for Python 2.6

* Thu Dec 27 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> - 0.4.0-1
- initial version
