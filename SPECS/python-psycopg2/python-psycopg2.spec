%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%define _python_bytecompile_errors_terminate_build 0

Summary:        Python-PostgreSQL Database Adapter
Name:           python-psycopg2
Version:        2.7.5
Release:        6%{?dist}
Url:            https://pypi.python.org/pypi/psycopg2
License:        LGPL with exceptions or ZPL
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://files.pythonhosted.org/packages/source/p/psycopg2/psycopg2-%{version}.tar.gz
%define sha1    psycopg2=4f77e3efcf9a0970be5120352274315f7bd1c754

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  postgresql-devel >= 10.5
Requires:       python2
Requires:       python2-libs
Requires:       postgresql >= 10.5

%description
Psycopg is the most popular PostgreSQL database adapter for the Python programming language. Its main features are the complete implementation of the Python DB API 2.0 specification and the thread safety (several threads can share the same connection). It was designed for heavily multi-threaded applications that create and destroy lots of cursors and make a large number of concurrent “INSERT”s or “UPDATE”s.

Psycopg 2 is mostly implemented in C as a libpq wrapper, resulting in being both efficient and secure. It features client-side and server-side cursors, asynchronous communication and notifications, “COPY TO/COPY FROM” support. Many Python types are supported out-of-the-box and adapted to matching PostgreSQL data types; adaptation can be extended and customized thanks to a flexible objects adaptation system.

Psycopg 2 is both Unicode and Python 3 friendly.

%package -n     python3-psycopg2
Summary:        python-psycopg2
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  postgresql-devel >= 10.5
Requires:       python3
Requires:       python3-libs
Requires:       postgresql >= 10.5

%description -n python3-psycopg2
Python 3 version.

%package doc
Summary:  Documentation for psycopg python PostgreSQL database adapter
Provides: python2-%{srcname}-doc = %{version}-%{release}
Provides: python3-%{srcname}-doc = %{version}-%{release}

%description doc
Documentation and example files for the psycopg python PostgreSQL
database adapter.

%prep
%setup -q -n psycopg2-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd

%check
chmod 700 /etc/sudoers
echo 'Defaults env_keep += "PYTHONPATH"' >> /etc/sudoers
#start postgresql server and create a database named psycopg2_test
useradd -m postgres &>/dev/null
groupadd postgres &>/dev/null
rm -r /home/postgres/data &>/dev/null ||:
mkdir -p /home/postgres/data
chown postgres:postgres /home/postgres/data
chmod 700 /home/postgres/data
su - postgres -c 'initdb -D /home/postgres/data'
echo "client_encoding = 'UTF8'" >> /home/postgres/data/postgresql.conf
echo "unix_socket_directories = '/run/postgresql'" >> /home/postgres/data/postgresql.conf
mkdir -p /run/postgresql
chown -R postgres:postgres /run/postgresql
su - postgres -c 'pg_ctl -D /home/postgres/data -l logfile start'
sleep 3
su - postgres -c 'createdb psycopg2_test'
PYTHONPATH=%{buildroot}%{python2_sitelib} PATH=$PATH:%{buildroot}%{_bindir} sudo -u postgres python2 -c "from psycopg2 import tests; tests.unittest.main(defaultTest='tests.test_suite')" --verbose

pushd ../p3dir
PYTHONPATH=%{buildroot}%{python3_sitelib} PATH=$PATH:%{buildroot}%{_bindir} sudo -u postgres python3 -c "from psycopg2 import tests; tests.unittest.main(defaultTest='tests.test_suite')" --verbose
popd
su - postgres -c 'pg_ctl -D /home/postgres/data stop'
rm -r /home/postgres/data &>/dev/null ||:

%files
%defattr(-,root,root)
%license LICENSE
%{python2_sitelib}/*

%files -n python3-psycopg2
%defattr(-,root,root,-)
%{python3_sitelib}/*

%files doc
%license LICENSE
%doc doc

%changelog
* Tue Jul 13 2021 Muhammad Falak Wani <mwani@microsoft.com> - 2.7.5-6
- Extend using Fedora 32 spec (license: MIT)
- Enable subpackage python-psycopg2-doc

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 2.7.5-5
- Make python byte compilation errors non-fatal due to python2 errors.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.7.5-4
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.7.5-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 2.7.5-2
- Consuming postgresql 10.5 version

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2.7.5-1
- Update to version 2.7.5

* Wed Aug 09 2017 Xiaolin Li <xiaolinl@vmware.com> 2.7.1-3
- Fixed make check errors

* Thu Jul 6 2017 Divya Thaluru <dthaluru@vmware.com> 2.7.1-2
- Added build requires on postgresql-devel

* Wed Apr 26 2017 Xialin Li <xiaolinl@vmware.com> 2.7.1-1
- Initial packaging for Photon
