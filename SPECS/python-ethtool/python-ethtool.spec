Vendor:         Microsoft Corporation
Distribution:   Mariner
# The tests fail in mock
%bcond_with tests

# Created by pyp2rpm-3.2.2
%global pypi_name ethtool

Name:           python-%{pypi_name}
Version:        0.15
Release:        1%{?dist}
Summary:        Python module to interface with %{pypi_name}

License:        GPLv2
URL:            https://github.com/fedora-python/python-ethtool
Source0:        https://github.com/fedora-python/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

BuildRequires:  libnl3-devel
BuildRequires:  asciidoc

%description
Python bindings for the ethtool kernel interface, that allows querying and
changing of Ethernet card settings, such as speed, port, auto-negotiation, and
PCI locations.

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
Python 3 bindings for the ethtool kernel interface, that allows querying and
changing of Ethernet card settings, such as speed, port, auto-negotiation, and
PCI locations.


%prep
%autosetup
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info


%build
%py3_build

a2x -d manpage -f manpage man/pethtool.8.asciidoc
a2x -d manpage -f manpage man/pifconfig.8.asciidoc

%install
%py3_install
mkdir -p %{buildroot}%{_sbindir}
mv %{buildroot}{%{_bindir},%{_sbindir}}/pifconfig
mv %{buildroot}{%{_bindir},%{_sbindir}}/pethtool

mkdir -p %{buildroot}%{_mandir}/man8/
cp -p man/*.8 %{buildroot}%{_mandir}/man8/


%if %{with tests}
%check
export PYTHONPATH=%{buildroot}%{python3_sitearch}
%{__python3} tests/parse_ifconfig.py -v
%{__python3}  -m unittest discover -v
%endif


%files -n python3-%{pypi_name}
%doc README.rst CHANGES.rst
%license COPYING
%{_sbindir}/pifconfig
%{_sbindir}/pethtool
%doc %{_mandir}/man8/*
%{python3_sitearch}/%{pypi_name}.cpython-%{python3_version_nodots}*.so
%{python3_sitearch}/%{pypi_name}-%{version}-py%{python3_version}.egg-info/

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.15-1
- Auto-upgrade to 0.15 - Azure Linux 3.0 - package upgrades

* Fri Jan 28 2022 Thomas Crain <thcrain@microsoft.com> - 0.14-9
- Fix source name collision with ethtool package
- Use github source tarball instead of pypi
* Thu Jan 27 2022 Cameron Baird <cameronbaird@microsoft.com> - 0.14-8
- Move to SPECS
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.14-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Sep 17 2019 Miro Hrončok <mhroncok@redhat.com> - 0.14-5
- Drop python2-ethtool

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.14-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Sep 13 2018 Miro Hrončok <mhroncok@redhat.com> - 0.14-1
- Update to 0.14

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.13-5
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 13 2017 Miro Hrončok <mhroncok@redhat.com> - 0.13-1
- Updated to 0.13
- Added python3 and python2 subpackages
- Add --with tests
- Modernize spec
- Remove merged patch
- Update upstream URL

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-7
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jun 22 2015 Yaakov Selkowitz <yselkowi@redhat.com> - 0.11-5
- Fix compile on F23

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 8 2014 David Sommerseth <davids@redhat.com> - 0.11-1
- Updated to the lastest python-ethtool-0.11 release, which
  incorporates all these additional patches and improves
  libnl3 connection error checking.

* Mon Apr 7 2014 David Sommerseth <davids@redhat.com> - 0.10-6
- Removed the never close netlink patch
- Added a patch which will ensure it will open a valid socket in open_netlink()

* Wed Apr 2 2014 David Sommerseth <davids@redhat.com> - 0.10-5
- Update patch 8 - to also never close the netlink socket

* Wed Apr 2 2014 David Sommerseth <davids@redhat.com> - 0.10-4
- Added patch 8 - to see of FD_CLOEXEC impacts vdsm

* Tue Apr 1 2014 David Sommerseth <davids@redhat.com> - 0.10-3
- Added patch 6 and 7, to improve error handling.  Will be removed when released upstream

* Thu Mar 20 2014 David Sommerseth <davids@redhat.com> - 0.10-2
- Added patch 1, 2, 4 and 5; they have not appeared in an upstream release yet

* Thu Jan 09 2014 David Sommerseth <davids@redhat.com> - 0.10-1
- Updated to v0.10

* Wed Dec 11 2013 David Sommerseth <davids@redhat.com> - 0.9-2
- Forced rebuild with new tarball. Had pushed up old version.

* Tue Dec 10 2013 David Sommerseth <davids@redhat.com> - 0.9-1
- Rebased against upstream 0.9

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Feb 19 2013 David Malcolm <dmalcolm@redhat.com> - 0.8-1
- 0.8

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Apr 13 2011 David Sommerseth <davids@redhat.com> - 0.7-2
- Fixed missing man page packaging

* Mon Apr 11 2011 David Sommerseth <davids@redhat.com> - 0.7-1
- Fixed several memory leaks (commit aa2c20e697af, abc7f912f66d)
- Improved error checking towards NULL values(commit 4e928d62a8e3)
- Fixed typo in pethtool --help (commit 710766dc722)
- Only open a NETLINK connection when needed (commit 508ffffbb3c)
- Added man page for pifconfig and pethtool (commit 9f0d17aa532, rhbz#638475)
- Force NETLINK socket to close on fork() using FD_CLOEXEC (commit 1680cbeb40e)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 David Sommerseth <dazo@users.sourceforge.net> - 0.6-1
- Don't segfault if we don't receive any address from rtnl_link_get_addr()
- Remove errornous file from MANIFEST
- Added ethtool.version string constant
- Avoid duplicating IPv6 address information
- import sys module in setup.py (Miroslav Suchy)

* Mon Aug  9 2010 David Sommerseth <davids@redhat.com> - 0.5-1
- Fixed double free issue (commit c52ed2cbdc5b851ebc7b)

* Wed Apr 28 2010 David Sommerseth <davids@redhat.com> - 0.4-1
- David Sommerseth is now taking over the maintenance of python-ethtool
- New URLs for upstream source code
- Added new API: ethtool.get_interfaces_info() - returns list of etherinfo objects
- Added support retrieving for IPv6 address, using etherinfo::get_ipv6_addresses()

* Fri Sep  5 2008 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.3-2
- Rewrote build and install sections as part of the fedora review process
  BZ #459549

* Tue Aug 26 2008 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.3-1
- Add get_flags method from the first python-ethtool contributor, yay
- Add pifconfig command, that mimics the ifconfig tool using the
  bindings available

* Wed Aug 20 2008 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.2-1
- Expand description and summary fields, as part of the fedora
  review process.

* Tue Jun 10 2008 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.1-3
- add dist to the release tag

* Tue Dec 18 2007 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.1-2
- First build into MRG repo

* Tue Dec 18 2007 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.1-1
- Get ethtool code from rhpl 0.212
