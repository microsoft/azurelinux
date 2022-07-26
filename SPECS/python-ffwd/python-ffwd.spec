Name:           python-ffwd-client
Version:        0.0.2
Release:        1%{?dist}
Summary:        Flexible metric forwarding agent(ffwd) client for python
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/udoprog/ffwd-client-python
Source0:        https://github.com/udoprog/ffwd-client-python/archive/refs/tags/%{version}.tar.gz#/ffwd-client-python-%{version}.tar.gz
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
%endif
BuildArch:      noarch

%description
Flexible metric forwarding agent (FFWD) client for python.

%prep
%autosetup -n ffwd-client-python-%{version} -p1

%build
%py3_build

%install
%py3_install

%check
%{python3} -m pip install atomicwrites attrs pluggy pygments six more-itertools
%{python3} -m pytest -v tests

%files
%doc README.md
%license LICENSE
%{_bindir}/ffwd-send
%{python3_sitelib}/*

%changelog
* Thu Jun 23 2022 Sumedh Sharma <sumsharma@microsoft.com> - 0.0.2-1
- Original version for CBL-Mariner (license: MIT)
- Adding as run dependency (Requires) for package cassandra medusa.
- License verified
