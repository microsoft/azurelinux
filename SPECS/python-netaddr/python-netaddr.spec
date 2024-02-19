Summary:        A pure Python network address representation and manipulation library
Name:           python-netaddr
Version:        1.2.1
Release:        1%{?dist}
License:        BSD-3-Clause
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://github.com/netaddr/netaddr
Source0:        https://github.com/netaddr/netaddr/archive/refs/tags/%{version}.tar.gz#/netaddr-%{version}.tar.gz

BuildArch:      noarch
	
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-wheel
BuildRequires:  python3-pip
BuildRequires:  pyproject-rpm-macros


%global desc A network address manipulation library for Python\
\
Provides support for:\
\
Layer 3 addresses\
\
 * IPv4 and IPv6 addresses, subnets, masks, prefixes\
 * iterating, slicing, sorting, summarizing and classifying IP networks\
 * dealing with various ranges formats (CIDR, arbitrary ranges and globs, nmap)\
 * set based operations (unions, intersections etc) over IP addresses and\
   subnets\
 * parsing a large variety of different formats and notations\
 * looking up IANA IP block information\
 * generating DNS reverse lookups\
 * supernetting and subnetting\
\
Layer 2 addresses\
\
 * representation and manipulation MAC addresses and EUI-64 identifiers\
 * looking up IEEE organisational information (OUI, IAB)\
 * generating derived IPv6 addresses
 
%global _description\
%{desc}
 
%description %_description

%package -n python3-netaddr
Summary: A pure Python network address representation and manipulation library
 
%description -n python3-netaddr
%{desc}
 
%package -n python3-netaddr-shell
Summary: An interactive shell environment for the netaddr library
Requires:  python3-netaddr = %{version}-%{release}
 
%description -n python3-netaddr-shell
An interactive shell environment for the netaddr library

%prep
%autosetup -n netaddr-%{version} -p1
	
# Make rpmlint happy, rip out python shebang lines from most python
# modules
#find netaddr -name "*.py" | \
#  xargs sed -i -e '1 {/^#!\//d}'

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files netaddr
	
%check
pip3 install iniconfig
%pytest
	
%files -n python3-netaddr -f %{pyproject_files}
%license COPYRIGHT.rst
%doc AUTHORS.rst CHANGELOG.rst README.rst THANKS.rst

%files -n python3-netaddr-shell
%{_bindir}/netaddr

%changelog
* Mon Feb 26 2024 Yash Panchal <yashpanchal@microsoft.com> - 1.2.1-1
- Upgrade to latest upstream version

* Mon Jan 24 2022 Thomas Crain <thcrain@microsoft.com> - 0.8.0-1
- Upgrade to latest upstream version

* Fri Dec 03 2021 Thomas Crain <thcrain@microsoft.com> - 0.7.19-10
- Replace easy_install usage with pip in %%check sections

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 0.7.19-9
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.7.19-8
- Added %%license line automatically

* Tue Apr 07 2020 Joe Schmitt <joschmit@microsoft.com> - 0.7.19-7
- Initial CBL-Mariner import from Photon (license: Apache2).
- Update URL.
- Update Source0 with valid URL.
- Remove sha1 macro.
- License verified.

* Mon Dec 03 2018 Tapas Kundu <tkundu@vmware.com> - 0.7.19-6
- Fixed make check.

* Tue Jul 25 2017 Divya Thaluru <dthaluru@vmware.com> - 0.7.19-5
- Fixed test command and added patch to fix test issues.

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.7.19-4
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> - 0.7.19-3
- Separate python2 and python3 bindings

* Mon Mar 27 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.7.19-2
- Added python3 package.

* Fri Feb 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> - 0.7.19-1
- Initial version of python-netaddr package for Photon.
