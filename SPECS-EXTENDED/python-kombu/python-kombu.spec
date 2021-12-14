%{!?python3_pkgversion: %global python3_pkgversion 3}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?__python3: %global __python3 /usr/bin/python3}
%{!?py3_build: %define py3_build CFLAGS="%{optflags}" %{__python3} setup.py build}
%{!?py3_install: %define py3_install %{__python3} setup.py install --skip-build --root %{buildroot}}

%bcond_without python3
%bcond_with tests
%bcond_with python2

%global srcname kombu

Summary:        An AMQP Messaging Framework for Python
Name:           python-%{srcname}
Version:        5.0.2
Release:        3%{?dist}
# utils/functional.py contains a header that says Python
License:        BSD and Python
URL:            http://kombu.readthedocs.org/
#Source0:       https://github.com/celery/kombu/archive/v%{version}/%{srcname}-%{version}.tar.gz
Source0:        https://github.com/celery/kombu/archive/v%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch

%description
AMQP is the Advanced Message Queuing Protocol, an open standard protocol
for message orientation, queuing, routing, reliability and security.

One of the most popular implementations of AMQP is RabbitMQ.

The aim of Kombu is to make messaging in Python as easy as possible by
providing an idiomatic high-level interface for the AMQP protocol, and
also provide proven and tested solutions to common messaging problems.

%if %{with python2}
%package -n python2-%{srcname}
Summary:        %{summary}
Requires:       python2-amqp >= 2.5.2
Requires:       python2-vine

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools

%if %{with tests}
# test requirements
BuildRequires:  python2-pytest
BuildRequires:  python2-pytest-cov
BuildRequires:  python2-vine
BuildRequires:  python2-case
BuildRequires:  python2-pytz

BuildRequires:  python2-nose

BuildRequires:  python2-nose-cover3
BuildRequires:  python2-coverage
BuildRequires:  python2-mock
BuildRequires:  python2-simplejson
BuildRequires:  python2-pyyaml
BuildRequires:  python2-msgpack
BuildRequires:  python2-amqp
# No longer packaged
#BuildRequires:  python2-pymongo
%endif

# For documentation
#BuildRequires:  python2-pymongo python2-sphinx
#This causes tests error, needs fixing upstream. Incompatible with python > 2.7
#BuildRequires:  python2-couchdb
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
AMQP is the Advanced Message Queuing Protocol, an open standard protocol
for message orientation, queuing, routing, reliability and security.

One of the most popular implementations of AMQP is RabbitMQ.

The aim of Kombu is to make messaging in Python as easy as possible by
providing an idiomatic high-level interface for the AMQP protocol, and
also provide proven and tested solutions to common messaging problems.
%endif

%if %{with python3}
%package -n python3-%{srcname}
Summary:        %{summary}
Requires:       python3-amqp >= 5.0.1
Requires:       python3-vine

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with tests}
BuildRequires:  python3-mock
BuildRequires:  python3-nose-cover3
BuildRequires:  python3-coverage
BuildRequires:  python3-amqp >= 5.0.1
BuildRequires:  python3-pymongo
BuildRequires:  python3-nose
BuildRequires:  python3-vine
BuildRequires:  python3-case
BuildRequires:  python3-pytz
BuildRequires:  python3-sqlalchemy
BuildRequires:  python3-boto3
BuildRequires:  python3-pytest
%endif
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
AMQP is the Advanced Message Queuing Protocol, an open standard protocol
for message orientation, queuing, routing, reliability and security.

One of the most popular implementations of AMQP is RabbitMQ.

The aim of Kombu is to make messaging in Python as easy as possible by
providing an idiomatic high-level interface for the AMQP protocol, and
also provide proven and tested solutions to common messaging problems.
%endif

%prep
%autosetup -n %{srcname}-%{version}

%build
%{?with_python2:%py2_build}
%{?with_python3:%py3_build}

%install
%{?with_python3:%py3_install}
%{?with_python2:%py2_install}

%check
%if %{with tests}
# python3-pyro is outdated and FTI in Fedora, ignore pyro tests
py.test-3 --ignore=t/unit/transport/test_pyro.py
%endif

%if %{with python2}
%files -n python2-%{srcname}
%doc AUTHORS FAQ READ* THANKS TODO examples/
%license LICENSE
%{python2_sitelib}/%{srcname}
%{python2_sitelib}/%{srcname}*.egg-info
%endif

%if %{with python3}
%files -n python3-%{srcname}
%doc AUTHORS FAQ READ* THANKS TODO examples/
%license LICENSE
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{srcname}*.egg-info
%endif

%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 5.0.2-3
- Remove epoch

* Wed Dec 09 2020 Steve Laughman <steve.laughman@microsoft.com> - 1:5.0.2-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT)
- Disable tests by default

* Tue Sep 29 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 1:5.0.2-1
- kombu 5.0.2

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.6.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 25 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 1:4.6.11-1
- kombu 4.6.11

* Wed Jun 03 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 1:4.6.10-1
- kombu 4.6.10

* Mon Jun 01 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 1:4.6.9-1
- kombu 4.6.9

* Mon Jun 01 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 1:4.6.6-5
- Enable testsuite as python-vine is now packaged

* Mon May 25 2020 Miro Hrončok <mhroncok@redhat.com> - 1:4.6.6-4
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.6.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 03 2019 Matthias Runge <mrunge@redhat.com> -4.6.6-2
- use importlib.metadata from the standard library in python

* Tue Dec 03 2019 Yatin Karel <ykarel@redhat.com> - 4.6.6-1
- Update to 4.6.6

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1:4.6.4-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Tue Aug 20 2019 Miro Hrončok <mhroncok@redhat.com> - 1:4.6.4-3
- Use standard library importlib.metadata on Python 3.8

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1:4.6.4-2
- Rebuilt for Python 3.8

* Mon Aug 19 2019 Fabian Affolter <mail@fabian-affolter.ch> - 1:4.6.4-1
- Update to latest upstream version 4.6.4 (rhbz#1742743)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1:4.6.3-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 02 2019 Nils Philippsen <nils@redhat.com> - 1:4.6.3-2
- Don't indiscriminately require Python 2 packages to fix FTBFS on Rawhide

* Sat Jun 15 2019 Fabian Affolter <mail@fabian-affolter.ch> - 1:4.6.3-1
- Update to latest upstream version 4.6.3 (rhbz#1717745)

* Fri Jun 14 2019 Fabian Affolter <mail@fabian-affolter.ch> - 1:4.6.2-1
- Update to latest upstream version 4.6.2 (rhbz#1717745)

* Sat Jun 08 2019 Fabian Affolter <mail@fabian-affolter.ch> - 1:4.6.1-2
- Update to latest upstream version 4.6.1 (rhbz#1717745)

* Thu May 30 2019 Fabian Affolter <mail@fabian-affolter.ch> - 1:4.6.0-1
- Update to latest upstream version 4.6.0

* Thu May 30 2019 Fabian Affolter <mail@fabian-affolter.ch> - 1:4.5.0-1
- Update to latest upstream version 4.5.0 (rhbz#1673119)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Neal Gompa <ngompa13@gmail.com> - 1:4.2.2-1
- Update to 4.2.2
- Fix summary for Python 2 subpackage
- Switch to bconds for controlling the build
- Add EPEL7 compatibility

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1:4.2.1-2
- Rebuilt for Python 3.7

* Mon Jun 04 2018 Matthias Runge <mrunge@redhat.com> - 1:4.2.1-1
- update to 4.2.1 (rhbz#1584452)

* Thu May 24 2018 Matthias Runge <mrunge@redhat.com> - 1:4.2.0-2
- drop anyjson dependency

* Wed May 23 2018 Matthias Runge <mrunge@redhat.com> - 1:4.2.0-1
- update to 4.2.0 (rhbz#1473462)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1:4.0.2-7
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Mar 24 2017 Matthias Runge <mrunge@redhat.com> - 1:4.0.2-5
- disable checks temporarily, until they are fixed

* Sun Feb 26 2017 Brian Bouterse <bmbouter@redhat.com> - 1:4.0.2-4
- Adds upstream patch for 699 preventing the Qpid transport from working with Celery 4

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 04 2017 Matthias Runge <mrunge@redhat.com> - 1:4.0.2-2
- add requires: python[23]-vine (rhbz#1409908)

* Tue Dec 27 2016 Matthias Runge <mrunge@redhat.com> - 1:4.0.2-1
- fixed FTBFS, upgraded to 4.0.2 (rhbz#1314754)

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1:4.0.0-8
- Rebuild for Python 3.6

* Wed Nov 16 2016 Fabian Affolter <mail@fabian-affolter.ch> - 1:4.0.0-1
- Update to latest upstream version 4.0.0 (rhbz#1314754)

* Fri Aug 05 2016 Brian Bouterse <bmbouter@redhat.com> - 1:3.0.33-7
- Adds additional patch for 577 which prevents leaking file descriptors in Qpid transport

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.33-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Apr 06 2016 Brian Bouterse <bmbouter@redhat.com> - 1:3.0.33-5
- Adds patch to fix upstream issue 577

* Tue Feb 23 2016 Brian Bouterse <bmbouter@redhat.com> - 1:3.0.33-4
- Adds patch to fix upstream issue 569
- Adds patch to fix upstream issue 571

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Brian Bouterse <bmbouter@redhat.com> - 1:3.0.33-2
- Adds patch to fix upstream issue 563 (rhbz#1300811)

* Wed Jan 20 2016 Brian Bouterse <bmbouter@redhat.com> - 1:3.0.33-1
- Update to latest upstream version 3.0.33 (rhbz#1297116)

* Tue Dec 22 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 1:3.0.32-1
- Upstream 3.0.32 (RHBZ#1289079)
- Fix python3 guards
- Bugfix for debug log flooding and redis transport

* Wed Dec 02 2015 Matthias Runge <mrunge@redhat.com> - 1:3.0.29-5
- add requires: python3-anyjson
- minor spec cleanup

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Nov  9 2015 Toshio Kuratomi <toshio@fedoraproject.org> - - 3.0.29-2
- Make it so the python3 subpackage doesn't drag in python2

* Wed Oct 28 2015 Fabian Affolter <mail@fabian-affolter.ch> - 1:3.0.29-1
- Update to latest upstream version 3.0.29 (rhbz#1275450)

* Thu Oct 15 2015 Fabian Affolter <mail@fabian-affolter.ch> - 1:3.0.28-1
- Update to latest upstream version 3.0.28 (rhbz#1270505)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild
- Update to latest upstream version 3.0.26 (rhbz#1214720)

* Fri Nov 21 2014 Fabian Affolter <mail@fabian-affolter.ch> - 1:3.0.24-1
- Update to latest upstream version 3.0.24 (rhbz#1166402)

* Thu Sep 18 2014 Fabian Affolter <mail@fabian-affolter.ch> - 1:3.0.23-1
- Update to latest upstream version 3.0.23 (rhbz#1142995)

* Sun Sep 14 2014 Fabian Affolter <mail@fabian-affolter.ch> - 1:3.0.22-1
- Update to latest upstream version 3.0.22 (rhbz#1118674)

* Tue Jul 15 2014 Rahul Sundaram <sundaram@fedoraproject.org> - 1:3.0.21-2
- reintroduce adjusted conditions for EPEL
- fix permission for a test script

* Sun Jul 13 2014 Rahul Sundaram <sundaram@fedoraproject.org> - 1:3.0.21-1
- update to 3.0.21
- drop conditionals in spec

* Thu Jul 03 2014 Fabian Affolter <mail@fabian-affolter.ch> - 1:3.0.20-1
- Update to latest upstream version 3.0.20 (rhbz#1114337)

* Mon Jun 23 2014 Fabian Affolter <mail@fabian-affolter.ch> - 1:3.0.19-1
- Update to latest upstream version 3.0.19 (rhbz#1095266)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1:3.0.15-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon May 05 2014 Matthias Runge <mrunge@redhat.com> - 3.0.15-2
- fix broken build
- have files listed only once

* Thu Apr 17 2014 Fabian Affolter <mail@fabian-affolter.ch> - 3.0.15-1
- Update to latest upstream version 3.0.15 (rhbz#1072265)

* Wed Mar 26 2014 Fabian Affolter <mail@fabian-affolter.ch> - 3.0.14-1
- update to 3.0.14 (rhbz#1072265)

* Wed Feb 26 2014 Matthias Runge <mrunge@redhat.com> - 3.0.12-1
- update to 3.0.12 (rhbz#1052424)

* Wed Jan 08 2014 Matthias Runge <mrunge@redhat.com> - 3.0.8-2
- Remove requirements patch, bump epoch to be upgradeable

* Wed Jan 08 2014 Matthias Runge <mrunge@redhat.com> - 3.0.8-1
- Update to 3.0.8 (rhbz#1037549)

* Fri Nov 22 2013 Matthias Runge <mrunge@redhat.com> - 3.0.6-1
- Update to 3.0.6 and enable tests for py3 as well

* Sun Nov 17 2013 Fabian Affolter <mail@fabian-affolter.ch> - 3.0.5-1
- Updated to latest upstream version 3.0.5 (rhbz#1024916)

* Sat Nov 16 2013 Fabian Affolter <mail@fabian-affolter.ch> - 3.0.4-1
- Update to latest upstream version 3.0.4 (rhbz#1024916)

* Fri Nov 15 2013 Fabian Affolter <mail@fabian-affolter.ch> - 3.0.3-1
- Update to latest upstream version 3.0.3 (rhbz#1024916)

* Sun Nov 03 2013 Fabian Affolter <mail@fabian-affolter.ch> - 3.0.2-1
- Updatd to latest upstream version 3.0.2 (rhbz#1024916)

* Mon Oct 28 2013 Fabian Affolter <mail@fabian-affolter.ch> - 3.0.1-1
- Update to latest upstream version 3.0.1 (rhbz#1019148)

* Mon Oct 14 2013 Matthias Runge <mrunge@redhat.com> - 2.5.15-2
- Enable tests for python2

* Mon Oct 14 2013 Matthias Runge <mrunge@redhat.com> - 2.5.15-1
- Update to 2.5.15 (rhbz#1016271)

* Sun Aug 25 2013 Fabian Affolter <mail@fabian-affolter.ch> - 2.5.14-1
- Update to latest upstream version 2.5.14 (rhbz#1000696)

* Wed Aug 21 2013 Matthias Runge <mrunge@redhat.com> - 2.5.13-1
- Update to latest upstream version 2.5.13 (rhbz#998104)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 29 2013 Fabian Affolter <mail@fabian-affolter.ch> - 2.5.12-1
- Update to latest upstream version 2.5.12

* Mon Jun 24 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 2.5.10-2
- Add requires on python-amqp/python3-amqp. resolves rhbz#974684
- Fix rpmlint warnings about macro in comments

* Sun Apr 21 2013 Fabian Affolter <mail@fabian-affolter.ch> - 2.5.10-1
- Update to latest upstream version 2.5.10

* Sat Mar 23 2013 Fabian Affolter <mail@fabian-affolter.ch> - 2.5.8-1
- Update to latest upstream version 2.5.8

* Sat Mar 09 2013 Fabian Affolter <mail@fabian-affolter.ch> - 2.5.7-1
- Update to latest upstream version 2.5.7

* Mon Feb 11 2013 Fabian Affolter <mail@fabian-affolter.ch> - 2.5.6-1
- Update to latest upstream version 2.5.6

* Sat Feb 09 2013 Fabian Affolter <mail@fabian-affolter.ch> - 2.5.5-1
- Update to latest upstream version 2.5.5

* Thu Dec 13 2012 Matthias Runge <mrunge@redhat.com> - 2.5.4-1
- Update to upstream version 2.5.4 (rhbz#886001)

* Tue Dec 04 2012 Matthias Runge <mrunge@redhat.com> - 2.5.3-1
- Update to latest upstream version 2.5.3

* Mon Nov 26 2012 Matthias Runge <mrunge@redhat.com> - 2.4.10-1
- Update to latest upstream version 2.4.10

* Tue Nov 06 2012 Matthias Runge <mrunge@redhat.com> - 2.4.8-1
- Update to new upstream version 2.4.8

* Thu Sep 20 2012 Matthias Runge <mrunge@redhat.com> - 2.4.7-1
- Update to new upstream version 2.4.7

* Sun Aug 26 2012 Matthias Runge <mrunge@matthias-runge.de> - 2.4.3-1
- Update to new upstream version 2.4.3

* Thu Aug 23 2012 Matthias Runge <mrunge@matthias-runge.de> - 2.4.0-1
- Update to new upstream version 2.4.0

* Fri Aug 03 2012 Matthias Runge <mrunge@matthias-runge.de> - 2.3.2-1
- Update to version 2.3.2
- Enable tests
- Require python2 and/or python3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 15 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 1.1.3-1
- Initial spec
- Derived from the one written by Fabian Affolter
- Spec patch from Lakshmi Narasimhan
