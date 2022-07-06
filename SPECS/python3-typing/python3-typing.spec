Name:           python3-typing
Version:        3.7.4.3
Release:        2%{?dist}
Summary:        Type Hints for Python
License:        PSF
Group:          Development/Tools
Url:            https://docs.python.org/3/library/typing.html
Vendor:         Mariner
Distribution:   Microsoft Corporation
Source0:        https://github.com/python/typing/archive/refs/tags/%{version}.tar.gz#/typing-%{version}.tar.gz
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs
BuildArch:      noarch

%description
Typing defines a standard notation for Python function and variable type annotations.
The notation can be used for documenting code in a concise,standard format,
and it has been designed to also be used by static and runtime type checkers, static analyzers, IDEs and other tools.

%prep
%autosetup -n typing-%{version}

%build
%py3_build

%install
%py3_install

%clean
rm -rf %{buildroot}

%check
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python3_sitelib} \
    python3 python3/test_typing.py

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Thu Jun 2022 Sumedh Sharma <sumsharma@microsoft.com> - 3.7.4.3-2
-   Initial CBL-Mariner import from PhotonOs (License: PSF)
-   Adding as build dependency for apache-libcloud needed by cassandra-medusa
-   License Verified 
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 3.7.4.3-1
-   Automatic Version Bump
*   Mon Jun 15 2020 Tapas Kundu <tkundu@vmware.com> 3.6.6-2
-   Mass removal python2
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 3.6.6-1
-   Update to version 3.6.6
*   Fri Jul 14 2017 Kumar Kaushik <kaushikk@vmware.com> 3.6.1-3
-   Adding python3 version.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.6.1-2
-   Use python2 explicitly
*   Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.6.1-1
-   Initial
