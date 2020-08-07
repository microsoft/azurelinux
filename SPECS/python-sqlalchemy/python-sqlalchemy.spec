%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        The Python SQL Toolkit and Object Relational Mapper
Name:           python-sqlalchemy
Version:        1.3.2
Release:        2%{?dist}
Url:            https://www.sqlalchemy.org
License:        MIT
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://files.pythonhosted.org/packages/source/S/SQLAlchemy/SQLAlchemy-%{version}.tar.gz
BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
Requires:       python2
Requires:       python2-libs

%description
SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL. SQLAlchemy provides a full suite of well known enterprise-level persistence patterns, designed for efficient and high-performing database access, adapted into a simple and Pythonic domain language.


%prep
%setup -q -n SQLAlchemy-%{version}

%build
python2 setup.py build

%check
easy_install apipkg
easy_install py
easy_install mock
export PYTHONPATH=$PYTHONPATH:%{_builddir}/SQLAlchemy-%{version}/.eggs/pytest-3.0.3-py2.7.egg
python2 setup.py test

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root)
%license LICENSE
%{python2_sitelib}/*

%changelog
* Sat May 09 00:21:09 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.3.2-2
- Added %%license line automatically

* Thu Mar 19 2020 Paul Monson <paulmon@microsoft.com> 1.3.2-1
- Update to 1.3.2. Fix Source0 URL. License verified.
* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.2.11-3
- Initial CBL-Mariner import from Photon (license: Apache2).
* Thu Jan 10 2019 Alexey Makhalov <amakhalov@vmware.com> 1.2.11-2
- Added BuildRequires python2-devel
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.2.11-1
- Update to version 1.2.11
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.1.7-2
- Use python2 explicitly
* Thu Mar 30 2017 Siju Maliakkal <smaliakal@vmware.com> 1.1.7-1
- Updating package version to latest
* Fri Nov 18 2016 Alexey Makhalov <amakhalov@vmware.com> 1.0.15-2
- Remove noarch
* Tue Sep 6 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0.15-1
- Initial packaging for Photon
