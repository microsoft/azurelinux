%define pkgname pywbem

Summary:        Python WBEM client interface and related utilities
Name:           python-%{pkgname}
Version:        1.0.1
Release:        6%{?dist}
License:        LGPLv2.1
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/pywbem/pywbem
Source0:        https://github.com/%{pkgname}/%{pkgname}/archive/%{version}.tar.gz#/%{pkgname}-%{version}.tar.gz
BuildArch:      noarch

%description
A Python library for making CIM (Common Information Model) operations over HTTP\
using the WBEM CIM-XML protocol. It is based on the idea that a good WBEM\
client should be easy to use and not necessarily require a large amount of\
programming knowledge. It is suitable for a large range of tasks from simply\
poking around to writing web and GUI applications.\
\
WBEM, or Web Based Enterprise Management is a manageability protocol, like\
SNMP, standardized by the Distributed Management Task Force (DMTF) available\
at http://www.dmtf.org/standards/wbem.\
\
It also provides a Python provider interface, and is the fastest and\
easiest way to write providers on the planet.

%package -n python3-%{pkgname}
Summary:        Python3 WBEM Client and Provider Interface
BuildRequires:  python3-PyYAML
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-pip
BuildRequires:  python3-ply
BuildRequires:  python3-setuptools
Requires:       python3
Requires:       python3-PyYAML
Requires:       python3-nocasedict
Requires:       python3-ply
Requires:       python3-requests
Requires:       python3-xml
Requires:       python3-yamlloader
AutoReqProv:    no
Provides:       python3dist(pywbem) = %{version}-%{release}
Provides:       python3.7dist(pyweb) = %{version}-%{release}
BuildArch:      noarch

%description -n python3-%{pkgname}
A WBEM client allows issuing operations to a WBEM server, using the CIM
operations over HTTP (CIM-XML) protocol defined in the DMTF standards DSP0200
and DSP0201. The CIM/WBEM infrastructure is used for a wide variety of systems
management tasks supported by systems running WBEM servers. See WBEM Standards
for more information about WBEM.

%prep
%setup -q -n %{pkgname}-%{version}

%build
PBR_VERSION="%{version}" CFLAGS="%{build_cflags}" python3 setup.py build

%install
env PYTHONPATH=%{buildroot}/%{python3_sitelib} \
    PBR_VERSION="%{version}" \
    python3 setup.py install -O1 --skip-build --root %{buildroot} --prefix=%{_prefix}
rm -rf %{buildroot}%{_bindir}/*.bat

%files -n python3-%{pkgname}
%license LICENSE.txt
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/pywbem
%{python3_sitelib}/pywbem_mock
%{_bindir}/mof_compiler
%doc README.rst

%changelog
* Fri Apr 29 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.1-6
- License verified.

* Wed Apr 27 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.1-5
- Updating source URL.

* Fri Aug 13 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.0.1-4
- Remove python2

* Tue Jan 05 2021 Ruying Chen <v-ruyche@microsoft.com> - 1.0.1-3
- Disable auto dependency generator.

* Fri Aug 21 2020 Olivia Crain <oliviacrain@microsoft.com> - 1.0.1-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT)

* Mon Aug 10 2020 Gris Ge <fge@redhat.com> - 1.0.1-1
- Upgrade to 1.0.1

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.14.6-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 17 2019 Tony Asleson <tasleson@redhat.com> - 0.14.6-1
- Upgrade to 0.14.6

* Mon Sep 23 2019 Gris Ge <fge@redhat.com> - 0.14.4-1
- Upgrade to 0.14.4

* Fri Sep 13 2019 Gris Ge <fge@redhat.com> - 0.14.3-5
- Fix pywbemcli ModuleNotFoundError: RHBZ #1743784

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.14.3-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jul 13 2019 Gris Ge <fge@redhat.com> - 0.14.3-2
- Fix the conflict with sblim-wbemcli: RHBZ #1724104

* Sat Jul 13 2019 Gris Ge <fge@redhat.com> - 0.14.3-1
- Upgrade to 0.14.3 and removed python2 stuff

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 11 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.12.6-2
- Enable python dependency generator

* Wed Dec 26 2018 Gris Ge <fge@redhat.com> - 0.12.6-1
- Upgrade to 0.12.6

* Tue Jul 24 2018 Gris Ge <fge@redhat.com> - 0.12.4-1
- Upgrade to 0.12.4

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 0.12.3-5
- Rebuilt for Python 3.7

* Tue Jun 26 2018 Gris Ge <fge@redhat.com> - 0.12.3-4
- iAdd missing dependency -- python3-devel

* Tue Jun 26 2018 Gris Ge <fge@redhat.com> - 0.12.3-3
- Rebuild again with --target=f29-python.

* Thu Jun 21 2018 Gris Ge <fge@redhat.com> - 0.12.3-2
- Rebuilt for Python 3.7

* Tue May 22 2018 Gris Ge <fge@redhat.com> - 0.12.3-1
- Upgrade to 0.12.3

* Fri May 18 2018 Gris Ge <fge@redhat.com> - 0.12.2-3
- Fix build failure on F28- where python2 is enabled.
  Use %license macro.

* Fri May 18 2018 Gris Ge <fge@redhat.com> - 0.12.2-2
- Remove python2 for F29+. Add missing python3-pbr runtime requirement.

* Fri May 04 2018 Gris Ge <fge@redhat.com> - 0.12.2-1
- Upgrade to 0.12.2.

* Wed Feb 14 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.11.0-6
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 04 2018 Lumír Balhar <lbalhar@redhat.com> - 0.11.0-4
- Fix directory ownership

* Thu Oct 19 2017 Gris Ge <fge@redhat.com> - 0.11.0-3
- Fedora 25 does not have python2-pip, use python-pip instead.

* Thu Oct 19 2017 Gris Ge <fge@redhat.com> - 0.11.0-2
- Add missing runtime dependency python2-ply and python3-ply

* Wed Oct 11 2017 Gris Ge <fge@redhat.com> - 0.11.0-1
- Upgrade to 0.11.0

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.10.0-3
- Python 2 binary package renamed to python2-pywbem
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Feb 23 2017 Gris Ge <fge@redhat.com> - 0.10.0-1
- Upgrade to 0.10.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 22 2016 Miro Hrončok <mhroncok@redhat.com> - 0.9.1-2
- Rebuild for Python 3.6

* Thu Dec 08 2016 Gris Ge <fge@redhat.com> 0.9.1-1
- Upgrade to 0.9.1

* Wed Oct 19 2016 Gris Ge <fge@redhat.com> 0.9.0-3
- Add missing runtime dependency python3-six and python-six

* Tue Sep 27 2016 Gris Ge <fge@redhat.com> 0.9.0-2
- Add missing runtime dependency python3-PyYAML and PyYAML.

* Wed Sep 14 2016 Gris Ge <fge@redhat.com> - 0.9.0-1
- Upgrade to 0.9.0 and add python3 pacakge -- python3-pywbem.

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-30.20131121svn626
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-29.20131121svn626
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-28.20131121svn626
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 30 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 0.7.0-27.svn
- Replace python-setuptools-devel BR with python-setuptools

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-26.20131121svn626
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 24 2014 Michal Minar <miminar@redhat.com> 0.7.0-25.20131121svn656
- Fixed local authentication under root.

* Thu Jan 23 2014 Michal Minar <miminar@redhat.com> 0.7.0-24.20131121svn656
- Added support for non-ascii strings.

* Fri Jan 03 2014 Michal Minar <miminar@redhat.com> 0.7.0-23.20131121svn656
- Skip hostname check when no verification is desired.

* Fri Dec 27 2013 Michal Minar <miminar@redhat.com> 0.7.0-22.20131121svn656
- Work around M2Crypto's inability to handle unicode strings.

* Wed Dec 18 2013 Michal Minar <miminar@redhat.com> 0.7.0-21.20131121svn656
- Adjusted default certificates paths searched for cert validation.

* Tue Dec 17 2013 Michal Minar <miminar@redhat.com> 0.7.0-20.20131121svn656
- Tweaked the ssl_verify_host patch.

* Mon Dec 16 2013 Michal Minar <miminar@redhat.com> 0.7.0-18.20131121svn656
- Fixes TOCTOU vulnerability in certificate validation.
- Resolves: rhbz#1026891

* Thu Nov 21 2013 Jan Safranek <jsafrane@redhat.com> 0.7.0-17.20131121svn626
- Added '-d' option to /usr/bin/mofcomp to just check mof files and their
  includes.

* Tue Aug 27 2013 Jan Safranek <jsafrane@redhat.com> 0.7.0-16.20130827svn625
- Fixed parsing of IPv6 addresses.

* Fri Aug 09 2013 Michal Minar <miminar@redhat.com> 0.7.0-15.20130723svn623
- Fixed certificate verification issue.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-14.20130723svn623
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013  <jsafrane@redhat.com> 0.7.0-13.20130702svn623
- Added subpackage with Twisted module to reduce dependencies of the main package.

* Tue Jul 23 2013  <jsafrane@redhat.com> 0.7.0-12.20130702svn623
- Fixed checking of CIMVERSION in CIM-XML.

* Tue Jul  2 2013 Jan Safranek <jsafrane@redhat.com> 0.7.0-11.20130702svn622
- New upstream version.
- Method parameters are now case-insensitive.

* Fri May 24 2013 Tomas Bzatek <tbzatek@redhat.com> 0.7.0-10.20130411svn619
- Fix module imports in /usr/bin/mofcomp

* Thu Apr 11 2013 Jan Safranek <jsafrane@redhat.com> 0.7.0-9.20130411svn619
- New upstream version.
- Removed debug 'print' statements.

* Mon Jan 28 2013 Michal Minar <miminar@redhat.com> 0.7.0-8.20130128svn613
- New upstream version.
- Added post-release snapshot version info.
- Removed obsoleted BuildRoot,

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jan 01 2010 David Nalley <david@gnsa.us> 0.7.0-3
- refined requires for epel compat

* Sun Jun 28 2009 David Nalley <david@gnsa.us> 0.7.0-2
- Added some verbiage regarding what WBEM is and expanding WBEM and CIM acronyms
- Added python-twisted as a dependency

* Thu Jun 25 2009 David Nalley <david@gnsa.us> 0.7.0-1
- Initial packaging
