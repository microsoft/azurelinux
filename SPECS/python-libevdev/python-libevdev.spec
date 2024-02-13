%global srcname libevdev

Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           python-%{srcname}
Version:        0.11
Release:        1%{?dist}
Summary:        Python bindings for the Linux input handling subsystem in userspace

License:        MIT
URL:            https://python-%{srcname}.readthedocs.io/en/latest/
Source0:        https://gitlab.freedesktop.org/%{srcname}/%{name}/-/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  glib-devel
BuildRequires:  libevdev-devel
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools


%global _description \
This package python-libevdev is a wrapper around the libevdev C library, with \
a pythonic API. libevdev makes it easy to read and parse events from an input \
device, such as create a virtual input device and make it send events, duplicate \
an existing device, and modify the event stream Linux.


%description %{_description}


%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}
%description -n python3-%{srcname} %{_description}


#------------------------------------------------------------------------------
%global debug_package %{nil}
%prep
%autosetup

#------------------------------------------------------------------------------
%build
%py3_build

#------------------------------------------------------------------------------
%install
%py3_install

#------------------------------------------------------------------------------
%files -n python3-%{srcname}
%defattr(-,root,root,-)
%license COPYING
%doc README.md
%{python3_sitelib}/*
%{python3_sitearch}/%{srcname}-%{version}-py%{python3_version}.egg-info/

#------------------------------------------------------------------------------
%changelog
* Wed Feb 07 2024 Ameya Usgaonkar <ausgaonkar@microsoft.com> - 0.11-1
- Original version for CBL-Mariner
- License verified
