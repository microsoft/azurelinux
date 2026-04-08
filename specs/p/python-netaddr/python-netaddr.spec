# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond docs %{undefined rhel}

Name:           python-netaddr
Version:        1.3.0
Release:        10%{?dist}
Summary:        A pure Python network address representation and manipulation library

License:        BSD-3-Clause
URL:            https://github.com/netaddr/netaddr
Source0:        https://pypi.python.org/packages/source/n/netaddr/netaddr-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pytest

%if %{with docs}
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx-issues
BuildRequires:  python3-furo
%endif

%global desc A network address manipulation library for Python\
\
Provides support for:\
\
Layer 3 addresses\
\
 * IPv4 and IPv6 addresses, subnets, masks, prefixes\
 * iterating, slicing, sorting, summarizing and classifying IP networks\
 * dealing with various ranges formats (CIDR, arbitrary ranges and globs, nmap)\
 * set based operations (unions, intersections etc) over IP addresses and\
   subnets\
 * parsing a large variety of different formats and notations\
 * looking up IANA IP block information\
 * generating DNS reverse lookups\
 * supernetting and subnetting\
\
Layer 2 addresses\
\
 * representation and manipulation MAC addresses and EUI-64 identifiers\
 * looking up IEEE organisational information (OUI, IAB)\
 * generating derived IPv6 addresses

%global _description\
%{desc}

%description %_description

%package -n python3-netaddr
Summary: A pure Python network address representation and manipulation library

%description -n python3-netaddr
%{desc}

%package -n python3-netaddr-shell
Summary: An interactive shell environment for the netaddr library
Requires:  python3-netaddr = %{version}-%{release}

%description -n python3-netaddr-shell
An interactive shell environment for the netaddr library

%prep
%autosetup -n netaddr-%{version} -p1

# Make rpmlint happy, rip out python shebang lines from most python
# modules
find netaddr -name "*.py" | \
  xargs sed -i -e '1 {/^#!\//d}'

%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel

#docs
%if %{with docs}
pushd docs
PYTHONPATH='../' sphinx-build-%{python3_version} -b html -d build/doctrees source python3/html
rm -f python3/html/.buildinfo
popd
%endif


%install
%pyproject_install
%pyproject_save_files netaddr

%check
%pytest

%files -n python3-netaddr -f %{pyproject_files}
%license COPYRIGHT.rst
%doc AUTHORS.rst CHANGELOG.rst README.rst THANKS.rst
%if %{with docs}
%doc docs/python3/html
%endif

%files -n python3-netaddr-shell
%{_bindir}/netaddr

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.3.0-10
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.3.0-9
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 04 2025 Python Maint <python-maint@redhat.com> - 1.3.0-7
- Rebuilt for Python 3.14

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.3.0-6
- Bootstrap for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 1.3.0-3
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.3.0-2
- Bootstrap for Python 3.13

* Wed May 29 2024 John Eckersberg <jeckersb@redhat.com> - 1.3.0-1
- New upstream release 1.3.0 (rhbz#2283706)

* Tue Feb 20 2024 John Eckersberg <jeckersb@redhat.com> - 1.2.1-1
- New upstream release 1.2.1 (rhbz#2264686)
- Remove hard dependency on ipython in the shell subpackage
  (see https://github.com/netaddr/netaddr/commit/b75ea33b08c26cd8251a0d0cc1a8ee00d6a7e538)
- Fix outdated upstream URL

* Thu Feb 15 2024 John Eckersberg <jeckersb@redhat.com> - 1.1.0-1
- New upstream release 1.1.0 (rhbz#2264314)

* Tue Feb 13 2024 John Eckersberg <jeckersb@redhat.com> - 1.0.0-1
- New upstream release 1.0.0 (rhbz#2263598)
- Cleanup and modernize spec file a bit

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 04 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 0.10.1-2
- Conditionalize docs

* Wed Jan  3 2024 John Eckersberg <jeckersb@redhat.com> - 0.10.1-1
- New upstream release 0.10.1 (rhbz#2256342)
- Remove patch for Python 3.13 compatibility (merged upstream in 0.10.0)
- Add new depencency on furo
- Include missing THANKS file (https://github.com/netaddr/netaddr/pull/345)

* Thu Dec 14 2023 John Eckersberg <jeckersb@redhat.com> - 0.9.0-2
- Add patch for Python 3.13 compatibility (rhbz#2246093)

* Tue Sep 19 2023 John Eckersberg <jeckersb@redhat.com> - 0.9.0-1
- New upstream release 0.9.0 (rhbz#2239532)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 0.8.0-13
- Rebuilt for Python 3.12

* Thu Feb 23 2023 Orion Poplawski <orion@nwra.com> - 0.8.0-12
- Cleanup spec
- Use SPDX License tag

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.8.0-9
- Rebuilt for Python 3.11

* Fri May 13 2022 John Eckersberg <jeckersb@redhat.com> - 0.8.0-8
- Move netaddr shell into a separate subpackage (rhbz#2076031)

* Tue Apr 12 2022 John Eckersberg <jeckersb@redhat.com> - 0.8.0-7
- Add Recommends on python3-ipython (rhbz#2074313)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.8.0-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul  3 2020 John Eckersberg <jeckersb@redhat.com> - 0.8.0-1
- New upstream release 0.8.0 (rhbz#1853684)

* Fri Jun 19 2020 John Eckersberg <jeckersb@redhat.com> - 0.7.20-1
- New upstream release 0.7.20 (rhbz#1848782)
- Minor spec and rpmlint cleanups

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.7.19-22
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.19-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov  7 2019 John Eckersberg <eck@redhat.com> - 0.7.19-20
- Remove python2 subpackage from Fedora 32+ (rhbz#1769871)

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.7.19-19
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.7.19-18
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.19-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 22 2019 John Eckersberg <eck@redhat.com> - 0.7.19-16
- Move /usr/bin/netaddr to python3 and remove python2 version
  See https://fedoraproject.org/wiki/Changes/Python_means_Python3

* Mon Mar 11 2019 John Eckersberg <eck@redhat.com> - 0.7.19-15
- Remove BuildRequires on python2-sphinx
  See https://fedoraproject.org/wiki/Changes/Sphinx2

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.19-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 28 2018 John Eckersberg <eck@redhat.com> - 0.7.19-13
- Add python_provide for python3 subpackage per packaging guidelines (RHBZ#1654198)

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.7.19-12
- Drop explicit locale setting
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.19-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.7.19-10
- Rebuilt for Python 3.7

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.7.19-9
- Rebuilt for Python 3.7

* Thu Feb 22 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.7.19-8
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Mon Feb 19 2018 John Eckersberg <eck@redhat.com> - 0.7.19-7
- Fix shebang mangling for python3 (RHBZ#1546800)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.19-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 0.7.19-5
- Cleanup spec file conditionals

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.7.19-4
- Python 2 binary package renamed to python2-netaddr
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 17 2017 John Eckersberg <eck@redhat.com> - 0.7.19-1
- New upstream release 0.7.19 (RHBZ#1413231)

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.7.18-10
- Rebuild for Python 3.6

* Sun Nov 13 2016 Orion Poplawski <orion@cora.nwra.com> - 0.7.18-9
- Update description
- Fix netaddr shebang (bug #1394046)

* Thu Nov 10 2016 Orion Poplawski <orion@cora.nwra.com> - 0.7.18-8
- Use updated python macros
- Use %%license

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.18-7
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Mar  8 2016 John Eckersberg <eck@redhat.com> - 0.7.18-6
- Add provides for python2-netaddr (RHBZ#1282129)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Nov 22 2015 Robert Kuska <rkuska@redhat.com> - 0.7.18-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5
- Delete file which contains bundled pytest

* Wed Nov 11 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.18-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.18-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Sep  4 2015 John Eckersberg <eck@redhat.com> - 0.7.18-1
- New upstream release 0.7.18 (RHBZ#1259969)

* Tue Sep  1 2015 John Eckersberg <eck@redhat.com> - 0.7.17-1
- New upstream release 0.7.17

* Mon Jun 29 2015 John Eckersberg <eck@redhat.com> - 0.7.15-1
- New upstream release 0.7.15
- Add separate source for tests, see https://github.com/drkjam/netaddr/issues/102
- Add patch for broken assertion, see https://github.com/drkjam/netaddr/pull/103

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr  1 2015 John Eckersberg <eck@redhat.com> - 0.7.14-1
- New upstream release 0.7.14

* Wed Sep 17 2014 Haïkel Guémar <hguemar@fedoraproject.org> - 0.7.12-1
- Upstream 0.7.12
- Conditionalize python3 subpackages build on Fedora
- Few spec cleanups

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.7.11-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Apr 21 2014 John Eckersberg <jeckersb@redhat.com> - 0.7.11-1
- New upstream release 0.7.11
- Enabled Python 3 support (bz1070357)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon May 30 2011 Jakub Hrozek <jhrozek@redhat.com> - 0.7.5-3
- Do not traceback on invalid IPNetwork input (upstream issues #2, #6, #5, #8)
- Remove executable bit from documentation files to make rpmlint happy

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 05 2010 John Eckersberg <jeckersb@redhat.com> - 0.7.5-1
- New upstream release 0.7.5
- Updated summary and description to match upstream README
- Updated URL and source to reflect upstream move to github

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon May 17 2010 John Eckersberg <jeckersb@redhat.com> - 0.7.4-1
- New upstream release 0.7.4

* Wed Sep 30 2009 John Eckersberg <jeckersb@redhat.com> - 0.7.3-1
- New upstream release 0.7.3

* Fri Aug 21 2009 John Eckersberg <jeckersb@redhat.com> - 0.7.2-1
- New upstream release 0.7.2
- Updated Summary and Description with new values provided by upstream

* Mon Aug 17 2009 John Eckersberg <jeckersb@redhat.com> - 0.7.1-1
- New upstream release 0.7.1 fixes naming conflict with 'nash' by
  renaming the netaddr shell to 'netaddr'

* Wed Aug 12 2009 John Eckersberg <jeckersb@redhat.com> - 0.7-1
- Upstream release 0.7

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 John Eckersberg <jeckersb@redhat.com> - 0.6.3-2
- Minor tweaks to spec file aligning with latest Fedora packaging guidelines
- Enforce python 2.4 dependency as needed by netaddr >= 0.6.2
- Drop BR on python-setuptool as it is not imported in setup.py
- Drop BR on dos2unix use sed instead
- Align description with that of delivered PKG-INFO
- Rip out python shebangs
- Add %%check section to enable tests
- Thanks to Gareth Armstrong <gareth.armstrong@hp.com>

* Tue Jun 23 2009 John Eckersberg <jeckersb@redhat.com> - 0.6.3-1
- New upstream bugfix release

* Mon Apr 13 2009 John Eckersberg <jeckersb@redhat.com> - 0.6.2-1
- New upstream bugfix release

* Tue Apr 7 2009 John Eckersberg <jeckersb@redhat.com> - 0.6.1-1
- New upstream bugfix release

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 John Eckersberg <jeckersb@redhat.com> - 0.6-2
- Add BuildDepends on dos2unix to clean up some upstream sources

* Wed Feb 18 2009 John Eckersberg <jeckersb@redhat.com> - 0.6-1
- New upstream version

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.5.2-2
- Rebuild for Python 2.6

* Fri Oct 10 2008 John Eckersberg <jeckersb@redhat.com> - 0.5.2-1
- New upstream version, bug fixes for 0.5.1

* Tue Sep 23 2008 John Eckersberg <jeckersb@redhat.com> - 0.5.1-1
- New upstream version, bug fixes for 0.5

* Sun Sep 21 2008 John Eckersberg <jeckersb@redhat.com> - 0.5-1
- New upstream version

* Mon Aug 11 2008 John Eckersberg <jeckersb@redhat.com> - 0.4-1
- Initial packaging for Fedora

