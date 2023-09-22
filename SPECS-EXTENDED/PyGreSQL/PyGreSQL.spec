Vendor:         Microsoft Corporation
Distribution:   Mariner
%global srcname	PyGreSQL

Name:		%{srcname}
Version:	5.2.2
Release:	3%{?dist}
Summary:	Python client library for PostgreSQL

URL:		http://www.pygresql.org/
License:	PostgreSQL

Source0:	https://github.com/PyGreSQL/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:	libpq-devel
BuildRequires:	python3-devel

# For testsuite
%if %{with_check}
# Missing test dependencies:
# BuildRequires:	postgresql-test-rpm-macros
%endif

%global _description\
PostgreSQL is an advanced Object-Relational database management system.\
The PyGreSQL package provides a module for developers to use when writing\
Python code for accessing a PostgreSQL database.

%description %_description

%package -n python3-pygresql
Summary:	%summary
%{?python_provide:%python_provide python3-pygresql}
# Remove before F30
Provides: python3-PyGreSQL = %{version}-%{release}
Provides: python3-PyGreSQL%{?_isa} = %{version}-%{release}
Obsoletes: python3-PyGreSQL < %{version}-%{release}

%description -n python3-pygresql


%prep
%autosetup -n %{srcname}-%{version} -p1

# PyGreSQL releases have execute bits on all files
find -type f -exec chmod 644 {} +


%build
%py3_build


%install
%py3_install


%files -n python3-pygresql
%license docs/copyright.rst
%doc docs/*.rst
%{python3_sitearch}/*.so
%{python3_sitearch}/*.py
%{python3_sitearch}/__pycache__/*.py{c,o}
%{python3_sitearch}/*.egg-info


%check
%postgresql_tests_run

cat > LOCAL_PyGreSQL.py <<EOF
dbname = '${PGTESTS_DATABASES##*:}'
# Per https://mail.vex.net/mailman/private.cgi/pygresql/2017-July/003446.html
# advice to leave 'dbhost' empty.
dbhost = ''
dbport = $PGPORT
EOF

%{__python3} setup.py test


%changelog
* Thu Aug 31 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.2.2-3
- Disabling missing test dependency.
- License verified.

* Sat Jul 24 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.2.2-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Disabling BR on 'postgresql-test-rpm-macros' for non-test builds.

* Thu Dec 10 2020 Ondrej Dubaj <odubaj@redhat.com> - 5.2.2-1
- rebase to the latest upstream version (rhbz#1906008)

* Thu Oct 01 2020 Ondrej Dubaj <odubaj@redhat.com> - 5.2.1-1
- rebase to the latest upstream version (rhbz#1882813)

* Wed Jul 15 2020 Patrik Novotný <panovotn@redhat.com> - 5.2-1
- Rebase to upstream release 5.2

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 5.1.2-2
- Rebuilt for Python 3.9

* Mon Apr 20 2020 Ondrej Dubaj <odubaj@redhat.com> - 5.1.2-1
- rebase to the latest upstream version (rhbz#1825598)

* Mon Mar 09 2020 Honza Horak <hhorak@redhat.com> - 5.1.1-1
- Update to 5.1.1
  Resolves: #1808328

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 30 2019 Miro Hrončok <mhroncok@redhat.com> - 5.1-5
- Subpackage python2-pygresql has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 5.1-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 5.1-3
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 29 2019 Ondrej Dubaj <odubaj@redhat.com> - 5.1-1
- rebase to the latest upstream version (rhbz#1711700)

* Tue Feb 12 2019 Pavel Raiskup <praiskup@redhat.com> - 5.0.6-3
- tests FTBFS - fix checks for PostgreSQL version again (rhbz#1674591)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 30 2018 Pavel Raiskup <praiskup@redhat.com> - 5.0.6-1
- rebase to the latest upstream version, per release notes:
  http://www.pygresql.org/contents/changelog.html

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 5.0.5-2
- Rebuilt for Python 3.7

* Thu May 03 2018 Pavel Raiskup <praiskup@redhat.com> - 5.0.5-1
- Rebase to upstream version 5.0.5 per online changelog:
  changelog http://www.pygresql.org/changelog.html

* Fri Apr 13 2018 Pavel Raiskup <praiskup@redhat.com> - 5.0.4-4
- test against postgresql-test-rpm-macros

* Thu Mar 15 2018 Pavel Raiskup <praiskup@redhat.com> - 5.0.4-3
- fix FTBFS after PostgreSQL upgrade to 10

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 02 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 5.0.4-2
- Python 2 binary package renamed to python2-pygresql
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3
- Python 3 binary package renamed to python3-pygresql

* Wed Aug 16 2017 Pavel Raiskup <praiskup@redhat.com> - 5.0.4-1
- Rebase to upstream version 5.0.4 per rhbz#1475595
  See changelog http://www.pygresql.org/changelog.html

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 17 2017 Pavel Raiskup <praiskup@redhat.com> - 5.0.3-4
- fix nasty undefined behavior (rhbz#1423108)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 5.0.3-2
- Rebuild for Python 3.6

* Mon Dec 12 2016 Pavel Raiskup <praiskup@redhat.com> - 5.0.3-1
- rhbz#1403519, rebase per upstream changelog
  http://www.pygresql.org/contents/changelog.html

* Wed Oct 05 2016 Pavel Raiskup <praiskup@redhat.com> - 5.0.2-2
- run tests through postgresql-setup 5.0, packaged in postgresql-devel

* Wed Sep 21 2016 Petr Kubat <pkubat@redhat.com> - 5.0.2-1
- Rebase to upstream version 5.0.2 per #1376292
  See changelog http://www.pygresql.org/changelog.html

* Mon Aug 29 2016 Petr Kubat <pkubat@redhat.com> - 5.0.1-1
- Rebase to upstream version 5.0.1 per #1370775
  See changelog http://www.pygresql.org/changelog.html

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Mar 21 2016 Pavel Raiskup <praiskup@redhat.com> - 5.0-3
- hardcode TZ=UTC

* Mon Mar 21 2016 Pavel Raiskup <praiskup@redhat.com> - 5.0-2
- use %%python_provide macro according to Python packaging guidelines
- allow disabling the testsuite by 'rpmbuild --define "runselftest 0"'

* Mon Mar 21 2016 Pavel Raiskup <praiskup@redhat.com> - 5.0-1
- rebase to 5.0
- provide python2-PyGreSQL and add python3-PyGreSQL
- enable testsuite
- cleanup obsoleted spec statements

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Pavel Raiskup <praiskup@redhat.com> - 4.2-1
- rebase (per rhbz#1301241)

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 12 2014 Jozef Mlich <jmlich@redhat.com> - 4.1.1-1
- Rebase to 4.1.1.
  See changelog http://www.pygresql.org/changelog.html
  Resolves: #1071940

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 17 2012 Tom Lane <tgl@redhat.com> 4.0-6
- Update tarball URL in specfile (no actual package change)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul  7 2011 Tom Lane <tgl@redhat.com> 4.0-3
- Add upstream patch for set_decimal bug
Resolves: #719093

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 29 2010 Tom Lane <tgl@redhat.com> 4.0-1
- Update to PyGreSQL 4.0
- Relabel license as PostgreSQL now that that's separately recognized by OSI.

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Nov 24 2009 Tom Lane <tgl@redhat.com> 3.8.1-2
- Fix License tag and permissions on example scripts under tutorial/,
  per discussion in package review request.
Related: #452321

* Fri Jun 20 2008 Tom Lane <tgl@redhat.com> 3.8.1-1
- Created package by stripping down postgresql specfile and adjusting
  to meet current packaging guidelines for python modules.
