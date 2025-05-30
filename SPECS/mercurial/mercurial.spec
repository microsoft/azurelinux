Summary:        A free, distributed source control management tool.
Name:           mercurial
Version:        6.5.1
Release:        1%{?dist}
License:        GPLv2+
URL:            https://www.mercurial-scm.org
Group:          System Environment/Security
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        https://www.mercurial-scm.org/release/%{name}-%{version}.tar.gz
BuildRequires:  python3-devel
%if 0%{?with_check}
BuildRequires:  check
BuildRequires:  python3-setuptools
BuildRequires:  unzip
BuildRequires:  which
%endif

Requires:       python3

%description
Mercurial is a distributed source control management tool similar to Git and Bazaar.
Mercurial is written in Python and is used by projects such as Mozilla and Vim.

%prep
%setup -q

%build
make %{?_smp_mflags} build

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
mkdir -p %{buildroot}/%{_bindir}
python3 setup.py install --skip-build --root %{buildroot}

cat >> %{buildroot}/.hgrc << "EOF"
[ui]
username = "$(id -u)"
EOF

%check
sed -i '1087,1088d' tests/test-obsolete.t
sed -i '54,56d' tests/test-clonebundles.t
sed -i '54i\ \ abort:\ stream:\ not\ a\ Mercurial\ bundle' tests/test-clonebundles.t
pushd tests
python3 run-tests.py -t 360
popd

%post -p /sbin/ldconfig

%postun
/sbin/ldconfig

# tries to set zsh_completions_dir or fallback to default value. Used in %files section
%define zsh_completions_dir %(pkg-config --variable=completionsdir zsh 2>/dev/null || echo '%{_datadir}/zsh/site-functions')

%files
%defattr(-,root,root)
%license COPYING
/usr/share/bash-completion/completions/hg
%{zsh_completions_dir}/_hg
/.hgrc
%{_bindir}/hg
%{python3_sitelib}/*

%changelog
* Tue Feb 06 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.5.1-1
- Auto-upgrade to 6.5.1 - 3.0 package upgrade

* Tue Mar 28 2022 Olivia Crain <oliviacrain@microsoft.com> - 6.0.3-2
- Remove unwanted check-time dependency on python-setuptools (replace with py3 version)

*   Wed Feb 23 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 6.0.3-1
-   Upgrading to latest version 6.0.3
-   Switching from python2 to python3.

*   Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.4-3
-   Removing the explicit %%clean stage.

*   Tue Jan 26 2021 Andrew Phelps <anphel@microsoft.com> 5.4-2
-   Fix check tests
*   Tue May 19 2020 Andrew Phelps <anphel@microsoft.com> 5.4-1
-   Update to version 5.4.
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 4.8.2-2
-   Added %%license line automatically
*   Tue Mar 17 2020 Henry Beberman <henry.beberman@microsoft.com> 4.8.2-1
-   Update to 4.8.2. Removed fixed CVE-2018-17983 patch. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 4.7.1-4
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon May 06 2019 Keerthana K <keerthanak@vmware.com> 4.7.1-3
-   Fix CVE-2018-17983
*   Thu Oct 25 2018 Sujay G <gsujay@vmware.com> 4.7.1-2
-   Disable zstd
*   Mon Sep 10 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.7.1-1
-   Update to version 4.7.1
*   Tue Oct 17 2017 Xiaolin Li <xiaolinl@vmware.com> 4.3.3-1
-   Update verion to 4.3.3 for CVE-2017-1000115, CVE-2017-1000116.
*   Fri Aug 11 2017 Rongrong Qiu <rqiu@vmware.com> 4.1-4
-   update error info in make check for bug 1900338
*   Fri Jun 16 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.1-3
-   Use python2 explicitly while building
*   Tue Jun 13 2017 Xiaolin Li <xiaolinl@vmware.com> 4.1-2
-   Apply CVE-2017-9462 patch
*   Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 4.1-1
-   Update package version
*   Mon Jan 22 2017 Xiaolin Li <xiaolinl@vmware.com> 3.7.1-6
-   Install with setup.py.
*   Tue Nov 22 2016 Xiaolin Li <xiaolinl@vmware.com> 3.7.1-5
-   Apply patches for CVE-2016-3068, CVE-2016-3069, CVE-2016-3105
*   Fri Oct 07 2016 ChangLee <changlee@vmware.com> 3.7.1-4
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.7.1-3
-   GA - Bump release of all rpms
*   Wed May 04 2016 Anish Swaminathan <anishs@vmware.com> 3.7.1-2
-   Edit postun script.
*   Thu Feb 25 2016 Kumar Kaushik <kaushikk@vmware.com> 3.7.1-1
-   Updating Version.
*   Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> 3.1.2-4
-   Edit post script.
*   Mon Nov 16 2015 Sharath George <sharathg@vmware.com> 3.1.2-3
-   Change path to /var/opt.
*   Tue Jun 30 2015 Alexey Makhalov <amakhalov@vmware.com> 3.1.2-2
-   /etc/profile.d permission fix
*   Mon Oct 13 2014 Divya Thaluru <dthaluru@vmware.com> 3.1.2-1
-   Initial build.  First version
