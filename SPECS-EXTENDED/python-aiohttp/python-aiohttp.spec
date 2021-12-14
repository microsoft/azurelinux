Vendor:         Microsoft Corporation
Distribution:   Mariner
%global srcname aiohttp
%global debug_package %{nil}

Name:           python-%{srcname}
Version:        3.6.2
Release:        3%{?dist}
Summary:        Python HTTP client/server for asyncio

License:        ASL 2.0
URL:            https://github.com/aio-libs/aiohttp
Source0:        %{url}/archive/v%{version}/%{srcname}-%{version}.tar.gz
# Unbundle http-parser
Patch0:         unbundle-http-parser.patch

BuildRequires:  gcc
BuildRequires:  http-parser-devel

%description
Python HTTP client/server for asyncio which supports both the client and the
server side of the HTTP protocol, client and server websocket, and webservers
with middlewares and pluggable routing.

%package -n python3-%{srcname}
Summary:        %{summary}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-Cython

Recommends:     python%{python3_version}dist(aiodns)
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
Python HTTP client/server for asyncio which supports both the client and the
server side of the HTTP protocol, client and server websocket, and webservers
with middlewares and pluggable routing.

%prep
%autosetup -p 1 -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-%{srcname}
%doc CHANGES.rst CONTRIBUTING.rst CONTRIBUTORS.txt HISTORY.rst README.rst
%license LICENSE.txt
%{python3_sitearch}/%{srcname}-*.egg-info/
%{python3_sitearch}/%{srcname}/

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.6.2-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 25 2019 Fabian Affolter <mail@fabian-affolter.ch> - 3.6.2-1
- Update to new upstream version 3.6.2

* Sat Sep 21 2019 Fabian Affolter <mail@fabian-affolter.ch> - 3.6.1-1
- Update to new upstream version 3.6.1

* Wed Sep 18 2019 Fabian Affolter <mail@fabian-affolter.ch> - 3.6.0-1
- Update to new upstream version 3.6.0

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.5.4-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jun 01 2019 Fabian Affolter <mail@fabian-affolter.ch> - 3.5.4-3
- Remove dep generator

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jan 12 2019 Fabian Affolter <mail@fabian-affolter.ch> - 3.5.4-1
- Update to new upstream version 3.5.4

* Fri Jan 11 2019 Fabian Affolter <mail@fabian-affolter.ch> - 3.5.3-1
- Update to new upstream version 3.5.3

* Thu Jan 10 2019 Fabian Affolter <mail@fabian-affolter.ch> - 3.5.2-1
- Update to new upstream version 3.5.2

* Wed Dec 26 2018 Fabian Affolter <mail@fabian-affolter.ch> - 3.5.1-1
- Update to new upstream version 3.5.1

* Thu Sep 06 2018 Fabian Affolter <mail@fabian-affolter.ch> - 3.4.4-1
- Update to new upstream version 3.4.4 (rhbz#1625634)

* Wed Sep 05 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.4.3-1
- Update to 3.4.3

* Sun Sep 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.4.2-1
- Update to 3.4.2

* Mon Aug 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.4.0-4
- Unbundle http-parser (rhbz#1622508)

* Mon Aug 27 2018 Fabian Affolter <mail@fabian-affolter.ch> - 3.4.0-3
- Fix rhbz#1622310

* Sat Aug 25 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.4.0-2
- Recommend aiodns

* Sat Aug 25 2018 Fabian Affolter <mail@fabian-affolter.ch> - 3.4.0-1
- Update to new upstream version 3.4.0 (rhbz#1622288)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.3.2-2
- Rebuilt for Python 3.7

* Tue Jun 12 2018 Fabian Affolter <mail@fabian-affolter.ch> - 3.3.2-1
- Update to new upstream version 3.3.2

* Wed Jun 06 2018 Fabian Affolter <mail@fabian-affolter.ch> - 3.3.1-1
- Update to new upstream version 3.3.1

* Fri Jun 01 2018 Fabian Affolter <mail@fabian-affolter.ch> - 3.3.0-1
- Update to new upstream version 3.3.0 (rhbz#1585170)

* Thu May 10 2018 Fabian Affolter <mail@fabian-affolter.ch> - 3.2.1-1
- Update to new upstream version 3.2.1 (rhbz#1576796)

* Mon May 07 2018 Fabian Affolter <mail@fabian-affolter.ch> - 3.2.0-1
- Update to new upstream version 3.2.0 (rhbz#1575435)

* Sat Apr 14 2018 Fabian Affolter <mail@fabian-affolter.ch> - 3.1.3-1
- Update to new upstream version 3.1.3 (rhbz#1567093)

* Fri Apr 06 2018 Fabian Affolter <mail@fabian-affolter.ch> - 3.1.2-1
- Update to new upstream version 3.1.2

* Tue Mar 27 2018 Fabian Affolter <mail@fabian-affolter.ch> - 3.1.1-1
- Update to new upstream version 3.1.1

* Fri Mar 23 2018 Fabian Affolter <mail@fabian-affolter.ch> - 3.1.0-1
- Update to new upstream version 3.1.0

* Thu Mar 15 2018 Fabian Affolter <mail@fabian-affolter.ch> - 3.0.9-1
- Update to new upstream version 3.0.9 (rhbz#1556612)

* Tue Mar 13 2018 Fabian Affolter <mail@fabian-affolter.ch> - 3.0.8-1
- Update to new upstream version 3.0.8

* Fri Mar 09 2018 Fabian Affolter <mail@fabian-affolter.ch> - 3.0.7-1
- Update to new upstream version 3.0.7 (rhbz#1548601)

* Tue Mar 06 2018 Fabian Affolter <mail@fabian-affolter.ch> - 3.0.6-1
- Update to new upstream version 3.0.6 (rhbz#1548601)

* Wed Feb 28 2018 Fabian Affolter <mail@fabian-affolter.ch> - 3.0.5-1
- Update to new upstream version 3.0.5 (rhbz#1548601)

* Mon Feb 12 2018 Fabian Affolter <mail@fabian-affolter.ch> - 3.0.1-1
- Update to new upstream version 3.0.1

* Mon Feb 12 2018 Fabian Affolter <mail@fabian-affolter.ch> - 3.0.0-1
- Update to new upstream version 3.0.0 (rhbz#1544413)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Fabian Affolter <mail@fabian-affolter.ch> - 2.3.10-1
- Update to new upstream version 2.3.10 (rhbz#1541369)

* Fri Jan 19 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.3.9-2
- Enable usage of dependency generator

* Wed Jan 17 2018 Igor Gnatenko <ignatenko@redhat.com> - 2.3.9-1
- Update to 2.3.9

* Mon Jan 15 2018 Fabian Affolter <mail@fabian-affolter.ch> - 2.3.8-1
- Update to new upstream version 2.3.8

* Wed Dec 27 2017 Fabian Affolter <mail@fabian-affolter.ch> - 2.3.7-1
- Update to new upstream version 2.3.7 (rhbz#1529275)

* Mon Dec 04 2017 Fabian Affolter <mail@fabian-affolter.ch> - 2.3.6-1
- Update to new upstream version 2.3.6

* Fri Dec 01 2017 Fabian Affolter <mail@fabian-affolter.ch> - 2.3.5-1
- Update to new upstream version 2.3.5

* Fri Nov 17 2017 Fabian Affolter <mail@fabian-affolter.ch> - 2.3.3-1
- Update to new upstream version 2.3.3 (rhbz#1514434)

* Thu Nov 02 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.3.2-1
- Update to 2.3.2

* Fri Oct 20 2017 Fabian Affolter <mail@fabian-affolter.ch> - 2.3.1-1
- Update to new upstream version 2.3.1 (rhbz#1504339)

* Wed Oct 18 2017 Fabian Affolter <mail@fabian-affolter.ch> - 2.3.0-1
- Update to new upstream version 2.3.0

* Fri Aug 04 2017 Fabian Affolter <mail@fabian-affolter.ch> - 2.2.5-1
- Update to new upstream version 2.2.5

* Thu Aug 03 2017 Fabian Affolter <mail@fabian-affolter.ch> - 2.2.4-1
- Update to new upstream version 2.2.4

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 06 2017 Fabian Affolter <mail@fabian-affolter.ch> - 2.2.3-1
- Update to new upstream version 2.2.3 (rhbz#1467742)

* Mon Jul 03 2017 Fabian Affolter <mail@fabian-affolter.ch> - 2.2.2-1
- Update to new upstream version 2.2.2 

* Mon Jul 03 2017 Fabian Affolter <mail@fabian-affolter.ch> - 2.2.1-1
- Update to new upstream version 2.2.1 (rhbz#1467114)

* Tue Jun 20 2017 Fabian Affolter <mail@fabian-affolter.ch> - 2.2.0-1
- Update to new upstream version 2.2.0 (rhbz#1463234)

* Sat May 27 2017 Fabian Affolter <mail@fabian-affolter.ch> - 2.1.0-1
- Update URL
- Update to new upstream version 2.1.0 (rhbz#1456063)

* Fri Apr 14 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.7-1
- Update to 2.0.7

* Fri Apr 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.6-1
- Update to 2.0.6

* Thu Mar 30 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.5-1
- Update to 2.0.5

* Tue Mar 28 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.0.4-1
- Update to 2.0.4

* Sat Mar 25 2017 Fabian Affolter <mail@fabian-affolter.ch> - 2.0.3-1
- Update to new upstream version 2.0.3 (rhbz#1435844)

* Thu Mar 23 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.0.2-3
- Specify proper yarl version

* Thu Mar 23 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.0.2-2
- Fix requires

* Thu Mar 23 2017 Fabian Affolter <mail@fabian-affolter.ch> - 2.0.2-1
- Update to new upstream version 2.0.2 (rhbz#1432690)

* Wed Mar 15 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.3.4-1
- Update to 1.3.4

* Mon Feb 20 2017 Fabian Affolter <mail@fabian-affolter.ch> - 1.3.3-1
- Update to new upstream version 1.3.3 (rhbz#1423053)

* Thu Feb 09 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.3-1
- Update to 1.3

* Sun Jan 22 2017 Fabian Affolter <mail@fabian-affolter.ch> - 1.2-1
- Update to new upstream version 1.2
- Add new requirement
- Add real description

* Sun Jan 01 2017 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.0.5-3
- Add missing dependency on async-timeout (RHBZ #1391287)

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.0.5-2
- Rebuild for Python 3.6

* Mon Oct 31 2016 Fabian Affolter <mail@fabian-affolter.ch> - 1.0.5-1
- Update to new upstream version 1.0.5

* Tue Aug 30 2016 Fabian Affolter <mail@fabian-affolter.ch> - 0.22.5-1
- Update to new upstream version 0.22.5

* Wed Aug 10 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.21.6-4
- Move requires under real subpackage

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21.6-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Jun 23 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.21.6-2
- Add missing Requires: python3-multidict (RHBZ #1349576)

* Thu May 12 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.21.6-1
- Update to 0.21.6

* Tue Mar 22 2016 Fabian Affolter <mail@fabian-affolter.ch> - 0.21.5-1
- Update to new upstream version 0.21.5

* Sat Mar 05 2016 Fabian Affolter <mail@fabian-affolter.ch> - 0.21.2-1
- Update to new upstream version 0.21.2

* Sun Feb 14 2016 Fabian Affolter <mail@fabian-affolter.ch> - 0.21.1-1
- Add requirements (rhbz#1300186)
- Update to new upstream version 0.21.1

* Thu Feb 04 2016 Fabian Affolter <mail@fabian-affolter.ch> - 0.21.0-1
- Update to new upstream version 0.21.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 27 2015 Fabian Affolter <mail@fabian-affolter.ch> - 0.19.0-1
- Update py3
- Update to new upstream version 0.19.0

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.4-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Oct 16 2015 Fabian Affolter <mail@fabian-affolter.ch> - 0.17.4-1
- Update to new upstream version 0.17.4

* Sat Aug 01 2015 Fabian Affolter <mail@fabian-affolter.ch> - 0.16.6-2
- Fix license

* Sat Aug 01 2015 Fabian Affolter <mail@fabian-affolter.ch> - 0.16.6-1
- Update to lastest upstream release 0.16.6 (rhbz#1231670)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 15 2015 Fabian Affolter <mail@fabian-affolter.ch> - 0.16.5-1
- Update to lastest upstream release 0.16.5 (rhbz#1231670)

* Wed Nov 26 2014 Fabian Affolter <mail@fabian-affolter.ch> - 0.10.2-1
- Update to lastest upstream release 0.10.2

* Wed Oct 08 2014 Fabian Affolter <mail@fabian-affolter.ch> - 0.9.1-2
- Build only a py3 package

* Wed Feb 26 2014 Fabian Affolter <mail@fabian-affolter.ch> - 0.9.1-1
- Initial package for Fedora
