# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?python_enable_dependency_generator}

%global pypi_name urlgrabber
%global majorver 4
%global minorver 1
%global patchver 0
%global dashversion %{majorver}-%{minorver}-%{patchver}

# Tests require internet access
%bcond_with check

Name:           python-%{pypi_name}
Version:        %{majorver}.%{minorver}.%{patchver}
Release: 25%{?dist}
Summary:        A high-level cross-protocol url-grabber

# Automatically converted from old format: LGPLv2+ - review is highly recommended.
License:        LicenseRef-Callaway-LGPLv2+
URL:            http://urlgrabber.baseurl.org/
# Not uploaded there yet...
#Source0:        https://files.pythonhosted.org/packages/source/u/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
#Source0:        http://urlgrabber.baseurl.org/download/urlgrabber-%{version}.tar.gz
Source0:        https://github.com/rpm-software-management/urlgrabber/releases/download/urlgrabber-%{dashversion}/urlgrabber-%{version}.tar.gz

BuildArch:      noarch

%global _description\
A high-level cross-protocol url-grabber for python supporting HTTP, FTP\
and file locations.  Features include keepalive, byte ranges, throttling,\
authentication, proxies and more.

%description %{_description}

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python3dist(setuptools)
%if %{with check}
BuildRequires:  python3dist(pycurl)
BuildRequires:  python3dist(six)
%endif

%description -n python%{python3_pkgversion}-%{pypi_name} %{_description}

This package provides the Python 3 version.

%prep
%autosetup -n %{pypi_name}-%{version} -p1

%build
%py3_build
sed -e "s|/usr/bin/python|%{__python3}|" -i scripts/*

%install
%py3_install
rm -rf %{buildroot}%{_docdir}/urlgrabber-%{version}

%if %{with check}
%check
export PYTHONPATH=$PWD
export URLGRABBER_EXT_DOWN="%{buildroot}%{_libexecdir}/urlgrabber-ext-down"
%{__python3} test/runtests.py
%endif

%files -n python%{python3_pkgversion}-%{pypi_name}
%license LICENSE
%doc ChangeLog README TODO
%{_bindir}/urlgrabber
%{_libexecdir}/urlgrabber-ext-down
%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info/

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 4.1.0-24
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 4.1.0-23
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 4.1.0-21
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 4.1.0-19
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 4.1.0-17
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 4.1.0-13
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 4.1.0-10
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.1.0-7
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 4.1.0-4
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Nov 17 2019 Neal Gompa <ngompa13@gmail.com> - 4.1.0-2
- Reduce build dependencies when tests are not enabled
- Add EL8 compatibility

* Tue Oct 08 2019 Neal Gompa <ngompa13@gmail.com> - 4.1.0-1
- Update to 4.1.0

* Tue Sep 24 2019 Miro Hrončok <mhroncok@redhat.com> - 4.0.0-6
- Subpackage python2-urlgrabber has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 4.0.0-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 21 2019 Michal Domonkos <mdomonko@redhat.com> - 4.0.0-3
- Fix mirror parsing regression (rhbz#1710576)
- python3: fix urlgrabber-ext-down to pass correct options to pycurl
- Fix failing unit test covering the retry_no_cache option

* Sun May 12 2019 Pavel Raiskup <praiskup@redhat.com> - 4.0.0-2
- python3 compat work-around to fix mock (rhbz#1707657, rhbz#1688173)

* Mon Feb 25 2019 Neal Gompa <ngompa13@gmail.com> - 4.0.0-1
- Update to 4.0.0
- Add Python 3 subpackage and have binaries as Python 3
- Rework and clean up spec file

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 3.10.1-15
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.10.1-13
- Python 2 binary package renamed to python2-urlgrabber
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 9 2016 Orion Poplawski <orion@cora.nwra.com> - 3.10.1-10
- Modernize spec

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.1-9
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Oct 03 2014 Valentina Mukhamedzhanova <vmukhame@redhat.com> - 3.10.1-6
- Revert porting to Python 3.

* Tue Sep 09 2014 Tomas Radej <tradej@redhat.com> - 3.10.1-5
- Really fixed UTF behaviour

* Tue Sep 02 2014 Tomas Radej <tradej@redhat.com> - 3.10.1-4
- Fixed UTF behaviour (bz #1135632)

* Fri Aug 29 2014 Valentina Mukhamedzhanova <vmukhame@redhat.com> - 3.10.1-3
- Don't set speed=0 on a new mirror that 404'd. BZ 1051554
- Support both Python 2 and 3. BZ 985288

* Sun Aug  3 2014 Tom Callaway <spot@fedoraproject.org> - 3.10.1-2
- fix license handling

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.1-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Dec 18 2013 Zdenek Pavlas <zpavlas@redhat.com> - 3.10.1-0
- Update to latest HEAD.
- Decrease the default_speed value. BZ 1043177
- Added client-side range support. BZ 435076

* Mon Dec  9 2013 Zdenek Pavlas <zpavlas@redhat.com> - 3.10-1
- Process mirror retries before other queued requests.
- Tell curl to return immediately on ctrl-c. BZ 1017491

* Wed Oct  9 2013 Zdenek Pavlas <zpavlas@redhat.com> - 3.10-0
- Update to latest HEAD.
- clamp timestamps from the future.  BZ 894630, 1013733
- Fix the condition to enter single-connection mode. BZ 853432
- Fix unit tests

* Fri Sep 27 2013 Zdenek Pavlas <zpavlas@redhat.com> - 3.9.1-32
- Update to latest HEAD.
- Switch to max_connections=1 after refused connect. BZ 853432
- Never display negative downloading speed. BZ 1001767

* Thu Aug 29 2013 Zdenek Pavlas <zpavlas@redhat.com> - 3.9.1-31
- Update to latest HEAD.
- add ftp_disable_epsv option. BZ 849177
- Spelling fixes.
- docs: throttling is per-connection, suggest max_connections=1. BZ 998263
- More robust "Content-Length" parsing. BZ 1000841

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.1-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 18 2013 Zdenek Pavlas <zpavlas@redhat.com> - 3.9.1-29
- Update to latest HEAD.
- Fix parsing of FTP 213 responses
- Switch to max_connections=1 after timing out.  BZ 853432
- max_connections=0 should imply the default limit.

* Fri May 17 2013 Zdenek Pavlas <zpavlas@redhat.com> - 3.9.1-28
- Update to latest HEAD.
- Add the "minrate" option. BZ 964298
- Workaround progress "!!!" end for file:// repos.
- add URLGrabError.code to the external downloader API
- Disable GSSNEGOTIATE to work around a curl bug.  BZ 960163

* Wed Mar 27 2013 Zdenek Pavlas <zpavlas@redhat.com> - 3.9.1-26
- Update to latest HEAD.
- Handle HTTP 200 response to range requests correctly.  BZ 919076
- Reset curl_obj to clear CURLOPT_RANGE from previous requests.  BZ 923951

* Thu Mar  7 2013 Zdeněk Pavlas <zpavlas@redhat.com> - 3.9.1-25
- Update to latest HEAD.
- fix some test cases that were failing.  BZ 918658
- exit(1) or /bin/urlgrabber failures.  BZ 918613
- clamp timestamps from the future.  BZ 894630
- enable GSSNEGOTIATE if implemented correctly.
- make error messages more verbose.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan  7 2013 Zdeněk Pavlas <zpavlas@redhat.com> - 3.9.1-23
- Update to latest HEAD.
- Handle checkfunc unicode exceptions. BZ 672117

* Thu Dec  6 2012 Zdeněk Pavlas <zpavlas@redhat.com> - 3.9.1-22
- Update to latest HEAD.
- Improve URLGRABBER_DEBUG, add max_connections.  BZ 853432

* Thu Nov  1 2012 Zdeněk Pavlas <zpavlas@redhat.com> - 3.9.1-21
- Update to latest HEAD.
- Get rid of "HTTP 200 OK" errors.  BZ 871835.

* Tue Sep  4 2012 Zdeněk Pavlas <zpavlas@redhat.com> - 3.9.1-20
- Update to latest HEAD.
- Fixed BZ 851178, 854075.

* Mon Aug 27 2012 Zdeněk Pavlas <zpavlas@redhat.com> - 3.9.1-19
- timedhosts: defer 1st update until a 1MB+ download.  BZ 851178

* Wed Aug 22 2012 Zdeněk Pavlas <zpavlas@redhat.com> - 3.9.1-18
- Update to latest HEAD, lots of enhancements.

* Wed Aug 10 2012 Zdeněk Pavlas <zpavlas@redhat.com> - 3.9.1-17
- Fix a bug in progress display code. BZ 847105.

* Wed Aug  8 2012 Zdeněk Pavlas <zpavlas@redhat.com> - 3.9.1-16
- Update to latest head.
- Improved multi-file progress, small bugfixes.

* Fri Jul 20 2012 Zdeněk Pavlas <zpavlas@redhat.com> - 3.9.1-15
- Update to latest head, misc bugfixes: BZ 832028, 831904, 831291.
- Disable Kerberos auth.  BZ 769254
- copy_local bugfix. BZ 837018
- send 'tries' counter to mirror failure callback

* Mon May 21 2012 Zdeněk Pavlas <zpavlas@redhat.com> - 3.9.1-14
- timedhosts: sanity check on dl_time

* Fri May 18 2012 Zdeněk Pavlas <zpavlas@redhat.com> - 3.9.1-13
- fix file:// profiling.  BZ 822632.

* Mon May 14 2012 Zdeněk Pavlas <zpavlas@redhat.com> - 3.9.1-12
- Update to latest HEAD
- Merge multi-downloader patches

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Sep  3 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.9.1-9
- new update to latest head with a number of patches collected from 
  older bug reports.

* Mon Aug 30 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.9.1-8
- update to latest head patches

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 3.9.1-7
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Apr 13 2010 James Antill <james@fedoraproject.org> 3.9.1-6
- Update to upstream HEAD.
- LOWSPEEDLIMIT and hdrs

* Fri Feb 19 2010 Seth Vidal <skvidal at fedoraproject.org> - 3.9.1-5
- add patch to allow reset_curl_obj() to close and reload the cached curl obj

* Thu Nov 12 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.9.1-4
- reset header values when we redirect and make sure debug output will work

* Wed Nov 11 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.9.1-3
- fixing a bunch of redirect and max size bugs

* Fri Sep 25 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.9.1-2
- stupid patch

* Fri Sep 25 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.9.1-1
- 3.9.1

* Tue Aug 18 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.9.0-8
- ssl options, http POST string type fixes

* Mon Aug 10 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.9.0-6
- reget fixes, tmpfiles no longer made for urlopen() calls.

* Wed Aug  5 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.9.0-5
- apply complete patch to head fixes: timeouts, regets, improves exception raising

* Tue Aug  4 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.9.0-4
- timeout patch for https://bugzilla.redhat.com/show_bug.cgi?id=515497


* Thu Jul 30 2009 Seth Vidal <skvidal at fedoraproject.org> - 3.9.0-1
- new version - curl-based

* Wed Apr  8 2009 James Antill <james@fedoraproject.org> 3.0.0-15
- Fix progress bars for serial consoles.
- Make C-c behaviour a little nicer.

* Fri Mar 13 2009 Seth Vidal <skvidal at fedoraproject.org>
- kill deprecation warning from importing md5 if anyone uses keepalive

* Mon Mar  9 2009 Seth Vidal <skvidal at fedoraproject.org>
- apply patch for urlgrabber to properly check file:// urls with the checkfunc

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Nov 28 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> 3.0.0-11
- Rebuild for Python 2.6

* Wed Oct 14 2008 James Antill <james@fedoraproject.org> 3.0.0-10
- Have the progress bar have a small bar, for a virtual size doubling.

* Thu Jul 10 2008 James Antill <james@fedoraproject.org> 3.0.0-9
- Make urlgrabber usable if openssl is broken
- Relates: bug#454179

* Sun Jun 15 2008 James Antill <james@fedoraproject.org> 3.0.0-9
- Don't count partial downloads toward the total

* Sat May 18 2008 James Antill <james@fedoraproject.org> 3.0.0-8
- Tweak progress output so it's hopefully less confusing
- Add dynamic resizing ability to progress bar
- Resolves: bug#437197

* Fri May  2 2008 James Antill <james@fedoraproject.org> 3.0.0-7
- Fix reget's against servers that don't allow Range requests, also tweaks
- reget == check_timestamp, if anyone/thing uses that.
- Resolves: bug#435156
- Fix minor typo in progress for single instance.

* Mon Apr  7 2008 James Antill <james@fedoraproject.org> 3.0.0-6
- Fix the ftp byterange port problem:
- Resolves: bug#419241
- Fixup the progress UI:
-   add function for total progress
-   add total progress percentagee current download line
-   add rate to current download line
-   use dead space when finished downloading
-   don't confuse download rate on regets.

* Sat Mar 15 2008 Robert Scheck <robert@fedoraproject.org> 3.0.0-5
- Make sure, that *.egg-info is catched up during build

* Mon Dec  3 2007 Jeremy Katz <katzj@redhat.com> - 3.0.0-4
- Ensure fds are closed on exceptions (markmc, #404211)

* Wed Oct 10 2007 Jeremy Katz <katzj@redhat.com> - 3.0.0-3
- fix type checking of strings to also include unicode strings; fixes 
  regets from yum (#235618)

* Mon Aug 27 2007 Jeremy Katz <katzj@redhat.com> - 3.0.0-2
- fixes for package review (#226347)

* Thu May 31 2007 Jeremy Katz <katzj@redhat.com> - 3.0.0-1
- update to 3.0.0

* Wed Dec  6 2006 Jeremy Katz <katzj@redhat.com> - 2.9.9-5
- rebuild for python 2.5

* Wed Dec  6 2006 Jeremy Katz <katzj@redhat.com> - 2.9.9-4
- fix keepalive (#218268) 

* Sat Nov 11 2006 Florian La Roche <laroche@redhat.com>
- add version/release to "Provides: urlgrabber"

* Mon Jul 17 2006 James Bowes <jbowes@redhat.com> - 2.9.9-2
- Add support for byte ranges and keepalive over HTTPS

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.9.9-1.1
- rebuild

* Tue May 16 2006 Jeremy Katz <katzj@redhat.com> - 2.9.9-1
- update to 2.9.9

* Tue Mar 14 2006 Jeremy Katz <katzj@redhat.com> - 2.9.8-2
- catch read errors so they trigger the failure callback.  helps catch bad cds

* Wed Feb 22 2006 Jeremy Katz <katzj@redhat.com> - 2.9.8-1
- update to new version fixing progress bars in yum on regets

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Sep 21 2005 Jeremy Katz <katzj@redhat.com> - 2.9.6-4
- don't use --record and list files by hand so that we don't miss 
  directories (#158480)

* Wed Sep 14 2005 Jeremy Katz <katzj@redhat.com> - 2.9.6-3
- add directory to file list (#168261)

* Fri Jun 03 2005 Phil Knirsch <pknirsch@redhat.com> 2.9.6-2
- Fixed the reget method to actually work correctly (skip completely transfered
  files, etc)

* Tue Mar  8 2005 Jeremy Katz <katzj@redhat.com> - 2.9.6-1
- update to 2.9.6

* Mon Mar  7 2005 Jeremy Katz <katzj@redhat.com> - 2.9.5-1
- import into dist
- make the description less of a book

* Mon Mar  7 2005 Seth Vidal <skvidal@phy.duke.edu> 2.9.5-0
- 2.9.5

* Thu Feb 24 2005 Seth Vidal <skvidal@phy.duke.edu> 2.9.3-0
- first package for fc3
- named python-urlgrabber for naming guideline compliance
