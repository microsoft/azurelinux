## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 9;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python-impacket
Summary:        Collection of Python classes providing access to network packets
Version:        0.12.0

License:        Apache-1.1 AND Zlib
URL:            https://github.com/fortra/impacket
# was           https://github.com/SecureAuthCorp/impacket
# was           https://github.com/CoreSecurity/impacket

# During re-add of the python2-impacket we found about dependency to ldapdomaindump
# feature can be avoided by option --no-dump to ntlmrelay.py
# https://bugzilla.redhat.com/show_bug.cgi?id=1672052#c8
# Also exclude stuff from examples, recommended manually
%global __requires_exclude ldapdomaindump|flask|httplib2

%global         sum             Collection of Python classes providing access to network packets

%global         common_desc     %{expand:
Impacket is a collection of Python classes focused on providing access to
network packets. Impacket allows Python developers to craft and decode network
packets in simple and consistent manner. It is highly effective when used in
conjunction with a packet capture utility or package such as Pcapy. Packets
can be constructed from scratch, as well as parsed from raw data. Furthermore,
the object oriented API makes it simple to work with deep protocol hierarchies.}

# weak dependencies not needed for the core python impacket library
# used by example scripts
# dsinternals and ldapdomaindump
# - used by ntlmrelayx.py example - feature can be avoided by option --no-dump
# https://bugzilla.redhat.com/show_bug.cgi?id=1672052#c8
# Also exclude stuff from examples, recommended manually
%global __requires_exclude ldapdomaindump|flask|httplib2|dsinternals

%global         gituser         fortra
%global         gitname         impacket
%global         commit          5af85c240076444d631d5f504e294daff065796b
%global         gitdate         20230731
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

# By defualt build with python3
# To disable python3 subpackage do: rpmbuild --rebuild python-impacket.*.src.rpm --without python3
%bcond_without  python3

%global         pkgver          %(echo %{version} | sed 's/\\./_/g')

# By default build from the release tarball
# to build from git snapshot use rpmbuild --rebuild python-impacket.*.src.rpm --without release
%bcond_without  release

%if %{with release}
Release:        %autorelease
Source0:        https://github.com/%{gituser}/%{gitname}/releases/download/%{gitname}_%{pkgver}/%{gitname}-%{version}.tar.gz
%else
Release:        %autorelease -s %{gitdate}git%{shortcommit}
Source0:        https://github.com/%{gituser}/%{gitname}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
%endif

# https://github.com/fortra/impacket/pull/1689
# remove unnecessary shebang
Patch0:         python-impacket-0.12.0-cleanup.patch

# relax the strict requirement for version ==24.0.0
Patch1:         python-impacket-0.12.0-pyopenssl.patch

BuildArch:      noarch

BuildRequires:  sed
BuildRequires:  grep

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

%description
%{common_desc}


#===== the python3 package definition
%package -n python%{python3_pkgversion}-%{gitname}
Summary:        %{sum}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{gitname}}
Provides:       impacket = %{version}-%{release}

# Used by many
Requires:       python%{python3_pkgversion}-pycryptodomex

# Used by /usr/bin/psexec.py
Requires:       python%{python3_pkgversion}-pyasn1

# Used by /usr/bin/ntlmrelayx.py
Requires:       python%{python3_pkgversion}-pyOpenSSL
Requires:       python%{python3_pkgversion}-ldap3

%if 0%{?fedora} || 0%{?rhel} >= 8
# Used by /usr/bin/nsplit.py
Recommends:     python%{python3_pkgversion}-pcapy
# Used by impacket/examples/ntlmrelayx/servers/socksserver.py
Recommends:     python%{python3_pkgversion}-httplib2
Recommends:     python%{python3_pkgversion}-flask
%else
# python3 package for pcapy currently missing in EPEL7
# Used by /usr/bin/nsplit.py
%global __requires_exclude pcapy|ldapdomaindump|flask|httplib2
# Requires:       python%%{python3_pkgversion}-pcapy
# Used by impacket/examples/ntlmrelayx/servers/socksserver.py
Requires:       python%{python3_pkgversion}-httplib2
Requires:       python%{python3_pkgversion}-flask
%endif


%description -n python%{python3_pkgversion}-%{gitname}
Python3 package of %{name}. %{common_desc}


#===== Preparation
%prep
%if %{with release}
# Build from git release version
%autosetup -p 1 -n %{gitname}-%{version}

# https://github.com/fortra/impacket/pull/1689
# 1) set library modules as non-executable as there is no main functionality and is meant to be used only via import
# impacket/examples/ldap_shell.py
# impacket/examples/smbclient.py
# 2) convert ends of lines from windows to unix (as rest of the project) for the file impacket/examples/mssqlshell.py
# 3) remove unnecessary shebang for impacket/examples/mssqlshell.py
chmod -x impacket/examples/ldap_shell.py impacket/examples/smbclient.py
sed -i -e 's/\r//g' impacket/examples/mssqlshell.py



%else
# Build from git commit
%autosetup -p 1 -n %{gitname}-%{commit}
%endif

# Clean-up

# Use explicit python3 shabeng instead of generic env python
%py3_shebang_fix impacket examples


# Rename split.py to splitpcap.py due to generic name colliding with DiderStevensSuite
# https://github.com/fortra/impacket/issues/1938
mv examples/split.py examples/splitpcap.py
sed -i -e "s%/split.py%/splitpcap.py%" impacket.egg-info/SOURCES.txt

# Drop useles dependency on future
# https://github.com/fortra/impacket/commit/d7b5e3 - will be fixed in 0.12.0
sed -i "s/'future',//" setup.py

#===== Build
%build
%py3_build


#===== Check
%check
PYTHONPATH=$BUILD_ROOT/usr/lib/python%{python3_version}/site-packages/ python3 -c \
    'import impacket.ImpactPacket ; impacket.ImpactPacket.IP().get_packet()'


#===== Install
%install
%py3_install

#now in license directory
rm -f %{buildroot}%{_defaultdocdir}/%{name}/LICENSE


#===== files for python3 package
%if %{with python3}
%files -n       python%{python3_pkgversion}-%{gitname}
%license        LICENSE
%doc            ChangeLog.md README.md
%{python3_sitelib}/%{gitname}/
%{python3_sitelib}/%{gitname}*.egg-info
%exclude %{_defaultdocdir}/%{gitname}
# %%exclude %%{_defaultdocdir}/%%{gitname}/testcases/*
%exclude %{_defaultdocdir}/%{gitname}/README.md
%{_bindir}/*.py
# with python3
%endif


%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 0.12.0-9
- Latest state for python-impacket

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.12.0-8
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.12.0-7
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.12.0-5
- Rebuilt for Python 3.14

* Wed Apr 02 2025 Michal Ambroz <rebus@seznam.cz> - 0.12.0-3
- bump to 0.12.0, relax the strict req to pyOpenSSL version

* Wed Apr 02 2025 Michal Ambroz <rebus@seznam.cz> - 0.12.0-2
- release strict requirement for pyopenssl==24.0.0

* Wed Apr 02 2025 Michal Ambroz <rebus@seznam.cz> - 0.12.0-1
- bump to 0.12.0

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.11.0-5
- Rebuilt for Python 3.13

* Tue Jan 23 2024 Michal Ambroz <rebus@seznam.cz> - 0.11.0-4
- remove the python version links (python2 support removed long time ago)

* Tue Jan 23 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 0.11.0-3
- Remove unavailable dsinternals dependency

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 01 2023 Michal Ambroz <rebus _AT seznam.cz> - 0.11.0-1
- bump to 0.11.0

* Wed Sep 20 2023 Lumír Balhar <lbalhar@redhat.com> - 0.10.0-5
- Remove dependency on future

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.10.0-3
- Rebuilt for Python 3.12

* Mon Jan 30 2023 Michal Ambroz <rebus _AT seznam.cz> - 0.10.0-3
- update the git user / URL

* Mon Jan 30 2023 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-2
- Rebuilt to change Python shebangs to /usr/bin/python3.6 on EPEL 8

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Oct 26 2022 Michal Ambroz <rebus _AT seznam.cz> - 0.10.0-1
- bump to 0.10.0
- version 0.10.0 is dropping support for python2.7

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.9.23-3
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Aug 26 2021 Fabian Affolter <mail@fabian-affolter.ch> - 0.9.23-1
- Update to latest upstream release 0.9.23 (closes rhbz#1969986)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.22-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.9.22-5
- Rebuilt for Python 3.10

* Fri May 21 2021 Michal Ambroz <rebus _AT seznam.cz> - 0.9.22-4
- remove the dependency to python-crypto

* Fri May 07 2021 Michal Ambroz <rebus _AT seznam.cz> - 0.9.22-3
- fix CVE-2021-31800 - #1957428, #1957427 during 0.9.22 lifecycle

* Sun May 02 2021 Michal Ambroz <rebus _AT seznam.cz> - 0.9.22-2
- fix dependencies for EPEL7 as of #1893859

* Wed Apr 14 2021 Michal Ambroz <rebus _AT seznam.cz> - 0.9.22-1
- Updated to new upstream release 0.9.22
- modernize specfile with bconds
- upstream patch for python39 compatibility (needed for FC34+)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.21-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.21-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.9.21-6
- Rebuilt for Python 3.9

* Tue Apr 28 2020 Michal Ambroz <rebus _AT seznam.cz> - 0.9.21-5
- fix dependency - pcapy renamed to python2-pcapy, python3-pcapy in fedora

* Tue Apr 28 2020 Michal Ambroz <rebus _AT seznam.cz> - 0.9.21-4
- cosmetics, remove comments with endif, macros with comments

* Thu Apr 02 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.9.21-3
- Updated to new upstream release 0.9.21

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Oct 12 2019 Michal Ambroz <rebus _AT seznam.cz> - 0.9.20-2
- patch the ldap3 dependencies to allow >=2.5.1 as we have already
  2.6 in Fedora 30 with updates. Dependency is used only for
  ntlmrelayx example and right now missing the ldapdump dependency
  anyway

* Sat Oct 12 2019 Michal Ambroz <rebus _AT seznam.cz> - 0.9.20-1
- bump to version 0.9.20
- generate python3 packages, preference goes to python3
- omit python2 for fc32+ rhel8+

* Tue Sep 17 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.19-2
- Only recommend packages needed for examples

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.19-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Apr 04 2019 Michal Ambroz <rebus _AT seznam.cz> - 0.9.19-1
- bump to version 0.9.19

* Tue Feb 05 2019 Michal Ambroz <rebus _AT seznam.cz> - 0.9.18-3
- conditional dependencies for EPEL7 - python-flask and pyOpenSSL

* Mon Feb 04 2019 Michal Ambroz <rebus _AT seznam.cz> - 0.9.18-2
- add missing dependencies for EPEL7 - python2-setuptools
- patch setup.py to remove python_version to meet RHEL7 setuptools version

* Mon Feb 04 2019 Michal Ambroz <rebus _AT seznam.cz> - 0.9.18-1
- bump to version 0.9.18

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.17-0.4.20180308gite0af5bb
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.17-0.3.20180308gite0af5bb
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 12 2018 Michal Ambroz <rebus _AT seznam.cz> - 0.9.17-0.2
- fix python runtime dependencies #1506227

* Sun Mar 11 2018 Michal Ambroz <rebus _AT seznam.cz> - 0.9.17-0.1
- bump to development version of 0.9.17 as there won't be any 0.9.16

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Sep 12 2016 Michal Ambroz <rebus _AT seznam.cz> - 0.9.15-4
- fix python provides for the python-impacket

* Wed Aug 24 2016 Michal Ambroz <rebus _AT seznam.cz> - 0.9.15-3
- python2/3 split package, disable python3 subpackage by default
- fix FTBFS

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.15-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Jul 14 2016 Fabian Affolter <mail@fabian-affolter.ch> - 0.9.15-1
- Update to latest upstream release (rhb#1307918)

* Tue Mar 01 2016 Michal Ambroz <rebus _AT seznam.cz> - 0.9.14-1
- Updated to new upstream release 0.9.14
- as Impacket upstream is not ready for python3 I propose to have the py3
  building ready, but disabled by default

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Nov 15 2015 Fabian Affolter <mail@fabian-affolter.ch> - 0.9.13-2
- Cleanup and py3

* Wed Jul 22 2015 Fabian Affolter <mail@fabian-affolter.ch> - 0.9.13-1
- Updated to new upstream release 0.9.13
- Fix FTBS (rhbz#1239842)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar 12 2015 Fabian Affolter <mail@fabian-affolter.ch> - 0.9.12-1
- Updated to new upstream release 0.9.12

* Sat Jun 28 2014 Fabian Affolter <mail@fabian-affolter.ch> - 0.9.11-2
- Move files out of /usr/bin
- Update licence (according to mailing list)

* Wed Feb 26 2014 Fabian Affolter <mail@fabian-affolter.ch> - 0.9.11-1
- Updated to new upstream release 0.9.11

* Sat Aug 10 2013 Fabian Affolter <mail@fabian-affolter.ch> - 0.9.10-1
- Updated to new upstream release 0.9.10

* Sat Nov 17 2012 Fabian Affolter <mail@fabian-affolter.ch> - 0.9.9.9-1
- Initial package


## END: Generated by rpmautospec
