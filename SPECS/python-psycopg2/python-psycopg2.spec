%define _python_bytecompile_errors_terminate_build 0
Summary:        Python-PostgreSQL Database Adapter
Name:           python-psycopg2
Version:        2.7.5
Release:        8%{?dist}
Url:            https://pypi.python.org/pypi/psycopg2
License:        LGPLv3+ with exceptions
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://files.pythonhosted.org/packages/source/p/psycopg2/psycopg2-%{version}.tar.gz
Patch0:         psycopg2-py38.patch

%description
Psycopg is the most popular PostgreSQL database adapter for the Python programming language.

%package -n     python3-psycopg2
Summary:        Python-PostgreSQL Database Adapter
BuildRequires:  python3-devel
BuildRequires:  postgresql-devel >= 10.5
Requires:       python3
Requires:       postgresql >= 10.5

%description -n python3-psycopg2
Psycopg is the most popular PostgreSQL database adapter for the Python programming language.
Its main features are the complete implementation of the Python DB API 2.0 specification and
the thread safety (several threads can share the same connection).

%package doc
Summary:  Documentation for psycopg python PostgreSQL database adapter
Provides: python3-psycopg2-doc = %{version}-%{release}

%description doc
Documentation and example files for the psycopg python PostgreSQL
database adapter.

%prep
%autosetup -p1 -n psycopg2-%{version}

%build
%py3_build

%install
%py3_install

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
PYTHONPATH=%{buildroot}%{python3_sitelib} PATH=$PATH:%{buildroot}%{_bindir} sudo -u postgres python3 -c "from psycopg2 import tests; tests.unittest.main(defaultTest='tests.test_suite')" --verbose
su - postgres -c 'pg_ctl -D /home/postgres/data stop'
rm -r /home/postgres/data &>/dev/null ||:

%files -n python3-psycopg2
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*

%files doc
%license LICENSE
%doc doc

%changelog
* Fri Dec 03 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.7.5-8
- Fix build with Python 3.9 using upstream patch

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.7.5-7
- Add license to python3 package
- Remove python2 package
- Lint spec
- License verified

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
