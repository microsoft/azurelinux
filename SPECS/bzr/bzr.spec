%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        A version control system
Name:           bzr
Version:        2.7.0
Release:        5%{?dist}
License:        GPLv2+
URL:            http://www.bazaar-vcs.org/
Group:          System Environment/Security
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://launchpad.net/bzr/2.7/2.7.0/+download/bzr-2.7.0.tar.gz
Patch0:         CVE-2017-14176.patch
BuildRequires:  python2-devel

%description
Bazaar is a version control system that helps you track project history over time and to collaborate easily with others. Whether you're a single developer, a co-located team or a community of developers scattered across the world, Bazaar scales and adapts to meet your needs. Part of the GNU Project, Bazaar is free software sponsored by Canonical. For a closer look, see ten reasons to switch to Bazaar.

%prep
%setup -q
%patch0 -p1

%build
python2 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot} --install-data=/usr/share
%{find_lang} bzr

%check
python2 setup.py check

%files -f bzr.lang
%defattr(-,root,root)
%license COPYING.txt
%{python2_sitelib}/*
%{_bindir}/bzr
%{_mandir}/man1/*

%changelog
* Thu May 21 2020 Emre Girgin <mrgirgin@microsoft.com> 2.7.0-5
- Fix CVE-2017-14176.
* Sat May 09 00:21:00 PST 2020 Nick Samson <nisamson@microsoft.com> - 2.7.0-4
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.7.0-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> 2.7.0-2
-   Added BuildRequires python2-devel
*   Thu Jun 22 2017 Xiaolin Li <xiaolinl@vmware.com> 2.7.0-1
-   Initial build. First version
