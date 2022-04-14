Vendor:         Microsoft Corporation
Distribution:   Mariner
%global srcname waitress

%global _docdir_fmt %{name}

Name:           python-%{srcname}
Version:        1.4.3
Release:        2%{?dist}
Summary:        Waitress WSGI server

License:        ZPLv2.1
URL:            https://github.com/Pylons/%{srcname}
Source0:        v%{version}-nodocs.tar.gz
# Upstream ships non free docs files.
# We do not even want them in our src.rpms
# So we remove them before uploading.
#
# Download the upstream tarball and invoke this script while in the
# tarball's directory:
# ./generate-tarball.sh 1.0
#
Source1: generate-tarball.sh

BuildArch:      noarch

# No docs as we don't have packaged pylons theme for sphinx

%global _description \
Waitress is meant to be a production-quality pure-Python WSGI server with\
very acceptable performance. It has no dependencies except ones which live\
in the Python standard library. It runs on CPython on Unix and Windows under\
Python 2.6+ and Python 3.3+. It is also known to run on PyPy 1.6.0+ on UNIX.\
It supports HTTP/1.0 and HTTP/1.1.

%description %{_description}

%package -n python3-%{srcname}
Summary:        Waitress WSGI server
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-nose
BuildRequires:  python3-coverage

%description -n python3-%{srcname} %{_description}

Python 3 version.

%prep
%autosetup -n %{srcname}-%{version}-nodocs

%build
%py3_build

%install
%py3_install

#check
# disable checks for now as they fail trying to lookup localhost in koji.
#

%files -n python3-%{srcname}
%license COPYRIGHT.txt LICENSE.txt
%doc README.rst CHANGES.txt
%{_bindir}/waitress-serve
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}-*.egg-info/

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4.3-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Feb 07 2020 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 1.4.3-1
- Update to 1.4.3 Fixes bug #1785591

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 20 2020 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 1.4.2-1
- Update to 1.4.2 Fixes bugs #1785591 #1789807 #1789809 #1789810 #1791415
  #1791416 #1791417 #1791420 #1791421 #1791422 #1791423

* Thu Jan 16 2020 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 1.4.1-1
- Update to 1.4.1 Fixes bug #1785591

* Wed Dec 25 2019 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 1.4.0-1
- Update to 1.4.0 Fixes bug #1785591

* Sun Oct 06 2019 Kevin Fenzi <kevin@scrye.com> - 1.3.1-1
- Update to 1.3.1. Fixes bug #1747075

* Mon Sep 09 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2.1-5
- Subpackage python2-waitress has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2.1-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jun 29 2019 Kevin Fenzi <kevin@scrye.com> - 1.2.1-2
- Remove non free docs from src.rpm and provide script to do so before upload. 
- Fixes bug #1684335

* Tue Feb 05 2019 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 1.2.1-1
- Update to 1.2.1 (#1667466)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 17 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-3
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Nov 11 2017 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 1.1.0-1
- Update to 1.1.0 (#1504455)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 18 2017 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 1.0.2-1
- Update to 1.0.2. Fixes bug #1419297

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.0.1-2
- Rebuild for Python 3.6

* Tue Oct 25 2016 Kevin Fenzi <kevin@scrye.com> - 1.0.1-1
- Update to 1.0.1. Fixes bug #1387885

* Sat Sep 03 2016 Kevin Fenzi <kevin@scrye.com> - 1.0.0-1
- Update to 1.0.0. Fixes bug #1372330

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jun 29 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.9.0-3
- Modernize spec to comply with new packaging guidelines

* Thu May 26 2016 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 0.9.0-2
- Fixed Source0 to point to new PyPi predictable URL format

* Thu May 5 2016 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 0.9.0-1
- Update to 0.9.0
- Fixed 2 warnings from fedpkg lint

* Sun Apr 10 2016 Kevin Fenzi <kevin@scrye.com> - 0.9.0b1-1
- Update to 0.9.0b1. Fixes bug #1325661

* Mon Mar 21 2016 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 0.9.0b0-1
- New (beta) version

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.10-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Sep 16 2015 Ralph Bean <rbean@redhat.com> - 0.8.10-1
- new version

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 27 2015 Ralph Bean <rbean@redhat.com> - 0.8.9-5
- Conditionalize the python3 subpackage.

* Mon Jul 14 2014 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 0.8.9-4
- Fix comment in description section about versioned directory for docs
- Use __python2 macro instead of __python

* Sat Jun 14 2014 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 0.8.9-3
- Run the tests with nose to avoid unclosed socket errors

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 25 2014 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 0.8.9-1
- Update to upstream

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Dec 22 2013 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 0.8.8-1
- Update to upstream

* Sun Dec 8 2013 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 0.8.5-3
- Remove python3 dependency on the python-waitress python2 package

* Wed Aug 7 2013 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 0.8.5-2
- Update description to use the new Fedora 20 _pkgdocdir macro, which
  is also defined for backwards cmompatibility

* Wed Jul 31 2013 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 0.8.5-1
- Update to upstream

* Sat Jul 6 2013 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 0.8.4-1
- Update to upstream
- Added waitress-serve as a binary executable in /usr/bin

* Sun May 12 2013 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 0.8.3-1
- Update to upstream

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 28 2012 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 0.8.2-3
- Use version macro in the Source0 to avoid duplicates
* Sat Nov 24 2012 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 0.8.2-2
- Point to the local docs directory in the description for the documentation
- Remove py3dir before copying the files to it in the prep phase
- Remove -O1 in the build phase as it is not used anymore in the Fedora
  Packaging guidelines
- Remove files rpmlint doesn't like
* Mon Nov 19 2012 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com> - 0.8.2-1
- New package.
