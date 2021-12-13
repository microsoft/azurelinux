%{!?python3_pkgversion: %global python3_pkgversion 3}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?__python3: %global __python3 /usr/bin/python3}
%{!?py3_build: %define py3_build CFLAGS="%{optflags}" %{__python3} setup.py build}
%{!?py3_install: %define py3_install %{__python3} setup.py install --skip-build --root %{buildroot}}

Summary:        Distributed Task Queue
Name:           python-celery
Version:        5.0.3
Release:        2%{?dist}
BuildArch:      noarch
License:        BSD
URL:            https://docs.celeryproject.org/en/stable/index.html
Source0:        https://github.com/celery/celery/archive/v%{version}/%{name}-%{version}.tar.gz
# Fix custom pytest markers for pytest
Source1:        pytest.ini

%description
An open source asynchronous task queue/job queue based on
distributed message passing. It is focused on real-time
operation, but supports scheduling as well.

The execution units, called tasks, are executed concurrently
on one or more worker nodes using multiprocessing, Eventlet
or gevent. Tasks can execute asynchronously (in the background)
or synchronously (wait until ready).

Celery is used in production systems to process millions of
tasks a day.

Celery is written in Python, but the protocol can be implemented
in any language. It can also operate with other languages using
web hooks.

The recommended message broker is RabbitMQ, but limited support
for Redis, Beanstalk, MongoDB, CouchDB and databases
(using SQLAlchemy or the Django ORM) is also available.

%package doc
Summary: Documentation for python-celery
License: CC-BY-SA

%description doc
Documentation for python-celery.

%package -n python3-celery
Summary:        Distributed Task Queue
Requires:       python3-amqp
Requires:       python3-billiard
Requires:       python3-kombu >= 5.0.2
Requires:       python3-pytz
Requires:       python3-setuptools
BuildRequires:  python3-amqp
BuildRequires:  python3-billiard
BuildRequires:  python3-case
BuildRequires:  python3-cryptography
BuildRequires:  python3-click
BuildRequires:  python3-devel
BuildRequires:  python3-dns
BuildRequires:  python3-dateutil
#BuildRequires:  python3-future
BuildRequires:  python3-kombu >= 5.0.2
BuildRequires:  python3-msgpack
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-timeout
BuildRequires:  python3-pytest-subtests
BuildRequires:  python3-pymongo
BuildRequires:  python3-pytz
BuildRequires:  python3-PyYAML
BuildRequires:  python3-redis
#BuildRequires:  python3-rpm-macros
BuildRequires:  python3-setuptools
BuildRequires:  python3-simplejson

%description -n python3-celery
%{desc}

%prep
%autosetup -n celery-%{version}

%build
%py3_build

#pushd docs
# missing python-sphinx_celery (for the moment)
#make %{?_smp_mflags} html
#popd

# fix custom celery markers in pytest
cp %{SOURCE1} .

%install
%py3_install
pushd %{buildroot}%{_bindir}
mv celery celery-%{python3_version}
ln -s celery-%{python3_version} celery-3
ln -s celery-3 celery
popd

%check
# python-moto is not packaged in Fedora, ignore S3 tests
# mongodb is not packaged in Fedora, ignore mongodb tests

# cache tests
export TEST_BROKER=redis://
export TEST_BACKEND=cache+pylibmc://
py.test-3 --ignore=t/unit/backends/test_s3.py --ignore=t/unit/backends/test_mongodb.py --ignore=t/distro/test_CI_reqs.py

# redis tests
export TEST_BROKER=redis://
export TEST_BACKEND=redis://
py.test-3 --ignore=t/unit/backends/test_s3.py --ignore=t/unit/backends/test_mongodb.py --ignore=t/distro/test_CI_reqs.py

# rabbitmq tests
export TEST_BROKER=pyamqp://
export TEST_BACKEND=rpc
py.test-3 --ignore=t/unit/backends/test_s3.py --ignore=t/unit/backends/test_mongodb.py --ignore=t/distro/test_CI_reqs.py

%files doc
%license LICENSE

%files -n python3-celery
%license LICENSE
%doc README.rst TODO CONTRIBUTORS.txt examples
%{_bindir}/celery
%{_bindir}/celery-3*
%{python3_sitelib}/celery-*.egg-info
%{python3_sitelib}/celery

%changelog
* Wed Dec 09 2020 Steve Laughman <steve.laughman@microsoft.com> - 5.0.3-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT)
* Sun Dec 06 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 5.0.3-1
- Celery 5.0.3
* Tue Nov 03 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 5.0.2-1
- Celery 5.0.2
* Mon Oct 19 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 5.0.1-1
- Celery 5.0.1
* Wed Sep 30 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 5.0.0-2
- Enable more tests
* Tue Sep 29 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 5.0.0-1
- Celery 5.0.0
* Mon Aug 03 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 4.4.7-1
- Celery 4.4.7
* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
* Thu Jun 25 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 4.4.6-1
- Celery 4.4.6
* Mon Jun 08 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 4.4.5-1
- Celery 4.4.5
* Mon Jun 01 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 4.4.4-1
- Celery 4.4.4
* Mon Jun 01 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 4.4.3-1
- Celery 4.4.3
- Run pytest during rpm build
* Mon May 25 2020 Miro Hrončok <mhroncok@redhat.com> - 4.3.0-6
- Rebuilt for Python 3.9
* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 4.3.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)
* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 4.3.0-3
- Rebuilt for Python 3.8
* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild
* Tue Jul 02 2019 Nils Philippsen <nils@redhat.com> - 4.3.0-1
- Update to 4.3.0
* Thu Jun 06 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 4.2.1-5
- Drop python2-celery, as nothing was using it and it fails to install (#1716370).
* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
* Mon Jan 28 2019 Neal Gompa <ngompa13@gmail.com> - 4.2.1-3
- Drop old, unused dependencies from Python 2 subpackage
* Mon Jan 28 2019 Neal Gompa <ngompa13@gmail.com> - 4.2.1-2
- Switch celery binary to Python 3 in F30+
- Switch to bconds for controlling the build
- Drop unused macro
* Wed Sep 19 2018 Randy Barlow <bowlofeggs@fedoraproject.org> - 4.2.1-1
- Update to 4.2.1 (#1602746).
- https://github.com/celery/celery/blob/v4.2.1/Changelog
- Correct documentation license to CC-BY-SA.
* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild
* Tue Jun 26 2018 Matthias Runge <mrunge@redhat.com> - 4.2.0-2
- rebuild for python 3.7
* Mon Jun 25 2018 Carl George <carl@george.computer> - 4.2.0-1
- Latest upstream
* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 4.1.1-2
- Rebuilt for Python 3.7
* Tue May 22 2018 Matthias Runge <mrunge@redhat.com> - 4.1.1-1
- update to 4.1.1 (rhbz#1474545)
* Sun Feb 11 2018 Iryna Shcherbina <ishcherb@redhat.com> - 4.0.2-6
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)
* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild