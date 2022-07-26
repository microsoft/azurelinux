%global srcname geomet
%global debug_package %{nil}
%global _description \
Convert GeoJSON to WKT/WKB (Well-Known Text/Binary), and vice versa.

Name:           python-%{srcname}
Version:        0.2.1
Release:        1%{?dist}
Summary:        GeoJSON <-> WKT/WKB conversion utilities
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://github.com/geomet
Source0:        https://github.com/geomet/geomet/archive/refs/tags/%{version}.tar.gz#/%{srcname}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  python3-pip
%endif

%description %{_description}

%package -n python3-%{srcname}
Summary:        %{summary}
Requires:       python3
Requires:       python3-click
Requires:       python3-six

%description -n python3-%{srcname} %{_description}

%prep
%autosetup -n geomet-%{version}

%build
%py3_build

%install
%py3_install
# Remove /usr/LICENSE file which is being copied during install_data
rm -f %{buildroot}/%{_exec_prefix}/LICENSE

%check
%{python3} -m pip install -r test-requirements.txt
%python3 setup.py test

%files -n python3-%{srcname}
%license LICENSE
%{_bindir}/geomet
%{python3_sitelib}/*

%changelog
*   Wed Jun 22 2022 Sumedh Sharma <sumsharma@microsoft.com> - 0.2.1-1
-   Initial CBL-Mariner import from Photon (license: Apache2).
-   Bumping version to 0.2.1
-   Adding as run dependency for python-cassandra-driver needed by cassandra-medusa.
-   License Verified.

*   Fri Jun 11 2021 Ankit Jain <ankitja@vmware.com> 0.1.2-1
-   Initial packaging for Photon
