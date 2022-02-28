Vendor:         Microsoft Corporation
Distribution:   Mariner
%bcond_without python3

%global github_owner    gabrielfalcao
%global github_name     HTTPretty
%global srcname         httpretty
# define these only if actually building from a GH snapshot not a release tarball
#global github_commit   70af1f8cf925ef50cb5e72212fb0aa46e1451dc3
#global shortcommit     %%(c=%%{github_commit}; echo ${c:0:7})
#global github_date     20161011


%global run_tests 1

Name:           python-httpretty
Version:        0.9.7
# If github_date is defined, assume a post-release snapshot
Release:        4%{?dist}
Summary:        HTTP request mock tool for Python

License:        MIT
URL:            https://github.com/%{github_owner}/%{github_name}
Source0:        %{pypi_source}
# Alternative for building from a github snapshot
#Source0:        https://github.com/%%{github_owner}/%%{github_name}/archive/%%{github_commit}/%%{github_name}-%%{shortcommit}.tar.gz

# Avoid unnecessary remote access requirement (note: test only actually
# does a remote connection after PR #313)
Patch1:         python-httpretty-fakesock_getpeercert_noconnect.patch

BuildArch:      noarch

%global _description\
Once upon a time a python developer wanted to use a RESTful API, everything was\
fine but until the day he needed to test the code that hits the RESTful API:\
what if the API server is down? What if its content has changed?\
\
Don't worry, HTTPretty is here for you.

%description %_description

%if %{with python2}
%package -n python2-httpretty
Summary: %summary
Requires:       python%{?fedora:2}-six

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
# For tests
BuildRequires:  python%{?fedora:2}-httplib2
BuildRequires:  python%{?fedora:2}-mock
BuildRequires:  python%{?fedora:2}-nose
BuildRequires:  python%{?fedora:2}-requests
BuildRequires:  python%{?fedora:2}-sure
BuildRequires:  python%{?fedora:2}-urllib3
BuildRequires:  python%{?fedora:2}-tornado
%if 0%{?epel} == 6
# Need unittest2 to get the 'skip' decorator
BuildRequires:  python-unittest2
%endif
%{?python_provide:%python_provide python2-httpretty}

%description -n python2-httpretty %_description
%endif

%if %{with python3}
%package -n python3-httpretty
Summary:        HTTP request mock tool for Python 3
Requires:       python%{python3_pkgversion}-six

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
# For tests
BuildRequires:  python%{python3_pkgversion}-httplib2
BuildRequires:  python%{python3_pkgversion}-mock
BuildRequires:  python%{python3_pkgversion}-nose
BuildRequires:  python%{python3_pkgversion}-requests
BuildRequires:  python%{python3_pkgversion}-sure
BuildRequires:  python%{python3_pkgversion}-urllib3
BuildRequires:  python%{python3_pkgversion}-tornado

%description -n python3-httpretty
Once upon a time a python developer wanted to use a RESTful API, everything was
fine but until the day he needed to test the code that hits the RESTful API:
what if the API server is down? What if its content has changed?

Don't worry, HTTPretty is here for you.
%endif

%prep
%autosetup -n httpretty-%{version} -p1

# Alternative for building from commit tarball
#autosetup -n %%{github_name}-%%{github_commit} -p1

# nose plugins we don't have yet
sed -i 's/^with-randomly = 1$//' setup.cfg
sed -i 's/^rednose = 1$//' setup.cfg

%build
%if %{with python2}
# setup.py contains non-ASCII characters; in Koji build environment
# default encoding is ASCII and this will choke, so set a UTF-8 locale
LANG=C.UTF-8 %py2_build
%endif

%if %{with_python3}
%py3_build
%endif

%install
%if %{with python2}
LANG=C.UTF-8 %py2_install
%endif

%if %{with_python3}
%py3_install
%endif


%check
%if %{run_tests}

%if %{with python2}
LANG=C.UTF-8 %{__python2} -m nose -v
%endif

%if %{with_python3}
%{__python3} -m nose -v
%endif

%endif


%if %{with python2}
%files -n python2-httpretty
%doc README.rst
%license COPYING
%{python2_sitelib}/httpretty
%{python2_sitelib}/httpretty-%{version}-py2.?.egg-info
%endif

%if %{with_python3}
%files -n python3-httpretty
%doc README.rst
%license COPYING
%{python3_sitelib}/httpretty
%{python3_sitelib}/httpretty-%{version}-py3.?.egg-info
%endif


%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.9.7-4
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Feb 04 2021 Joe Schmitt <joschmit@microsoft.com> - 0.9.7-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove Fedora version check for python version

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 08 2020 Charalampos Stratakis <cstratak@redhat.com> - 0.9.7-1
- Update to 0.9.7 (rhbz#1759992)

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.6-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.6-3
- Rebuilt for Python 3.8

* Tue Aug 06 2019 Jiri Popelka <jpopelka@redhat.com> - 0.9.6-2
- Escape macro in comment

* Tue Jul 30 2019 Jiri Popelka <jpopelka@redhat.com> - 0.9.6-1
- Update to 0.9.6
- Disable python2 subpackage on F30+

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.9.5-4
- Drop explicit locale setting for python3, use C.UTF-8 for python2
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 0.9.5-2
- Rebuilt for Python 3.7

* Wed Jun 06 2018 Miro Hrončok <mhroncok@redhat.com> - 0.9.5-1
- Update to 0.9.5, fix for Python 3.7 (#1580060)

* Sat May 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.9.4-1
- Update to 0.9.4 (#1572888)

* Wed Feb 21 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.8.14-8.20161011git70af1f8
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.14-7.20161011git70af1f8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 0.8.14-6.20161011git70af1f8
- Cleanup spec file conditionals

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.8.14-5.20161011git70af1f8
- Python 2 binary package renamed to python2-httpretty
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.14-4.20161011git70af1f8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.14-3.20161011git70af1f8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Adam Williamson <awilliam@redhat.com> - 0.8.14-2.20161011git70af1f8
- Backport PR #317 (call reset from setUp / tearDown) - thanks gholms

* Fri Jan 06 2017 Adam Williamson <awilliam@redhat.com> - 0.8.14-1.20161011git70af1f8
- Update to current git master (as a 0.8.14 post-release snapshot)
- Backport PR #313 (fix with recent OpenSSL, requests and urllib3)
- Backport PR #314 (fix a test with Python 3)
- Backport PR #315 (fix some issues with urllib 1.10, as found in RHEL 6)
- Avoid an unnecessary remote roundtrip in one of the tests
- Replace dependency 'un-pinning' patch with some sed commands in the spec
- Replace ASCII patch by running setup.py with a UTF-8 LANG
- Enable the tests, with necessary buildrequires

* Tue Dec 13 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.8.3-8
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-7
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 02 2015 Jamie Lennox <jamielennox@redhat.com> - 0.8.3-3
- Added conditional __python2 macros for building on RHEL 6.

* Tue Feb 24 2015 Jamie Lennox <jamielennox@redhat.com> - 0.8.3-2
- Added with_python3 build flags to enable building on EPEL.

* Mon Jul 28 2014 Jamie Lennox <jamielennox@redhat.com> - 0.8.3-1
- Updated to new version.
- Removed check, there are simply too many problems upstream.

* Mon Mar 10 2014 Jamie Lennox <jamielennox@redhat.com> - 0.8.0-1
- Initial package.

