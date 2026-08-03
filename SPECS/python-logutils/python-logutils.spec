%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

%bcond_without check
%define pkgname logutils

Summary:        A set of handlers for the Python standard library’s logging package
Name:           python-%{pkgname}
Version:        0.3.5
Release:        2%{?dist}
License:        BSD
Url:            https://logutils.readthedocs.io/
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        https://pypi.io/packages/source/l/%{pkgname}/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch

%global _description %{expand:
The logutils package provides a set of handlers for the Python standard library’s logging package.

Some of these handlers are out-of-scope for the standard library, and so they are packaged here.
Others are updated versions which have appeared in recent Python releases, but are usable with 
older versions of Python, and so are packaged here..}

%description %_description

%package -n python3-%{pkgname}
Summary:        A lean and fast WSGI object-dispatching web framework

BuildRequires:  python3-devel
BuildRequires:  python3-xml
BuildRequires:  python3-setuptools
Requires:       python3
Requires:       python3-libs


%description -n python3-%{pkgname}  %_description

%prep
%setup -q -n %{pkgname}-%{version}
# Fix Python 3.12 compat: assertEquals removed, and tests need explicit log level
sed -i 's/self\.assertEquals/self.assertEqual/g' tests/test_dictconfig.py
sed -i '/l\.addHandler(h)/a\        l.setLevel(logging.WARNING)' tests/test_adapter.py tests/test_testing.py
sed -i '/l\.addHandler(qh)/i\        l.setLevel(logging.WARNING)' tests/test_queue.py

%build
python3 setup.py build

%install
python3 setup.py install --root=%{buildroot}

%if %{with check}
%check
# Patch fixes Python 3.12 compat: assertEquals -> assertEqual, explicit logger level
python3 setup.py test
%endif

%files -n python3-%{pkgname}
%license LICENSE.txt
%doc README.rst doc/
%{python3_sitelib}/*

%changelog
* Wed Jun 17 2026 Kshitiz Godara <kgodara@microsoft.com> - 0.3.5-2
- Patch tests for Python 3.12 compatibility: replace assertEquals with
  assertEqual and add explicit logger.setLevel(WARNING) where required.

* Fri Aug 21 2020 Thomas Crain <thcrain@microsoft.com> 1.4.0-1
- Original version for CBL-Mariner
- License verified
