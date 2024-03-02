%global srcname pip
%global _description %{expand:
A tool for installing and managing Python packages}

Summary:        A tool for installing and managing Python packages
Name:           python-pip
Version:        24.0
Release:        1%{?dist}
License:        MIT AND Python-2.0.1 AND Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND ISC AND LGPL-2.1-only AND MPL-2.0 AND (Apache-2.0 OR BSD-2-Clause)
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Tools
URL:            https://pip.pypa.io/
Source0:        https://github.com/pypa/pip/archive/%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

%description    %{_description}

%package -n python3-pip
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-wheel

%description -n python3-pip %{_description}

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build_wheel

%install
pip3 install --no-cache-dir --no-index --ignore-installed --root %{buildroot} \
    --no-user --find-links dist pip

%files -n python3-pip
%defattr(-,root,root,755)
%{_bindir}/pip*
%{python3_sitelib}/pip*

%changelog
* Tue Feb 13 2024 Andrew Phelps anphel@microsoft.com - 24.0-1
- License verified
- Original version for CBL-Mariner
