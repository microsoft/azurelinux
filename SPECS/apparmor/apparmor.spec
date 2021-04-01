%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Name:           apparmor
Version:        2.13
Release:        12%{?dist}
Summary:        AppArmor is an effective and easy-to-use Linux application security system.
License:        GNU LGPL v2.1
URL:            https://launchpad.net/apparmor
Source0:        https://launchpad.net/apparmor/2.13/2.13.0/+download/%{name}-%{version}.tar.gz
Patch0:         apparmor-set-profiles-complain-mode.patch
Patch1:         apparmor-service-start-fix.patch
Patch2:         apparmor-fix-make-check.patch
Patch3:         apparmor-update-severity-db.patch
# CVE-2016-1585 has no upstream fix as of 2020/09/28
Patch100:       CVE-2016-1585.nopatch
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Productivity/Security
BuildRequires:  python3
BuildRequires:  perl
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  swig
BuildRequires:  make
BuildRequires:  gawk
BuildRequires:  which
BuildRequires:  libstdc++
BuildRequires:  libstdc++-devel
BuildRequires:  gcc
BuildRequires:  libgcc
BuildRequires:  libgcc-devel
BuildRequires:  glibc
BuildRequires:  glibc-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  httpd
BuildRequires:  httpd-devel
BuildRequires:  httpd-tools
BuildRequires:  apr
BuildRequires:  apr-util-devel
BuildRequires:  pam
BuildRequires:  pam-devel
BuildRequires:  dejagnu
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  python3-setuptools, python3-xml

%description
AppArmor is a file and network mandatory access control
mechanism. AppArmor confines processes to the resources allowed by the
systems administrator and can constrain the scope of potential security
vulnerabilities.

%package -n libapparmor
Summary:    Utility library for AppArmor
License:    GNU LGPL v2.1
Group:      Development/Libraries/C and C++

%description -n libapparmor
This package contains the AppArmor library.

%package -n libapparmor-devel
Summary:    Development headers and libraries for libapparmor
License:    GNU LGPL v2.1
Group:      Development/Libraries/C and C++
Requires:   libapparmor = %{version}-%{release}

%description -n libapparmor-devel
This package contains development files for libapparmor.

%package -n apache2-mod_apparmor
Summary:    AppArmor module for apache2
License:    GNU LGPL v2.1
Group:      Productivity/Security

%description -n apache2-mod_apparmor
This provides the Apache module needed to declare various differing
confinement policies when running virtual hosts in the webserver
by using the changehat abilities exposed through libapparmor.

%package profiles
Summary:    AppArmor profiles that are loaded into the apparmor kernel module
License:    GNU LGPL v2.1
Group:      Productivity/Security
Requires:   apparmor-parser = %{version}-%{release}
Requires:   apparmor-abstractions = %{version}-%{release}

%description profiles
This package contains the basic AppArmor profiles.

%package parser
Summary:    AppArmor userlevel parser utility
License:    GNU LGPL v2.1
Group:      Productivity/Security
Requires:   libapparmor = %{version}-%{release}
Requires:   systemd

%description parser
The AppArmor Parser is a userlevel program that is used to load in
program profiles to the AppArmor Security kernel module.
This package is part of a suite of tools that used to be named
SubDomain.

%package abstractions
Summary:    AppArmor abstractions and directory structure
License:    GNU LGPL v2.1
Group:      Productivity/Security
Requires:   apparmor-parser = %{version}-%{release}

%description abstractions
AppArmor abstractions (common parts used in various profiles) and
the /etc/apparmor.d/ directory structure.

%package -n pam_apparmor
Summary:    PAM module for AppArmor change_hat
License:    GNU LGPL v2.1
Group:      Productivity/Security
Requires:   pam
Requires:   pam-devel

%description -n pam_apparmor
The pam_apparmor module provides the means for any PAM applications
that call pam_open_session() to automatically perform an AppArmor
change_hat operation in order to switch to a user-specific security
policy.

%package utils
Summary:    AppArmor User-Level Utilities Useful for Creating AppArmor Profiles
License:    GNU LGPL v2.1
Group:      Productivity/Security
Requires:   libapparmor = %{version}-%{release}
Requires:   audit
Requires:   apparmor-abstractions = %{version}-%{release}

%description utils
This package contains programs to help create and manage AppArmor
profiles.

%package -n python3-apparmor
Summary:    Python 3 interface for libapparmor functions
License:    GNU LGPL v2.1
Group:      Development/Libraries/Python
Requires:   libapparmor = %{version}-%{release}
Requires:   python3

%description -n python3-apparmor
This package provides the python3 interface to AppArmor. It is used for python
applications interfacing with AppArmor.

%package -n perl-apparmor
Summary:    AppArmor module for perl.
License:    GNU LGPL v2.1
Group:      Development/Libraries/Perl
Requires:   libapparmor = %{version}-%{release}

%description -n perl-apparmor
This package contains the AppArmor module for perl.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
export PYTHONPATH=/usr/lib/python3.7/site-packages
export PYTHON=/usr/bin/python3
export PYTHON_VERSION=3.7
export PYTHON_VERSIONS=python3
#Building libapparmor
cd ./libraries/libapparmor
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/lib/"
/sbin/ldconfig
sh ./autogen.sh
%configure \
 --with-perl \
 --with-python
make %{?_smp_mflags}
#Building Binutils
cd ../../binutils/
make %{?_smp_mflags}
#Building parser
cd ../parser
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/lib/"
export LIBRARY_PATH="$LIBRARY_PATH:/usr/lib"
echo $LD_LIBRARY_PATH
echo $LIBRARY_PATH
make %{?_smp_mflags}
#Building Utilities
cd ../utils
make %{?_smp_mflags}
#Building Apache mod_apparmor
cd ../changehat/mod_apparmor
make %{?_smp_mflags}
#Building PAM AppArmor
cd ../pam_apparmor
make %{?_smp_mflags}
#Building Profiles
cd ../../profiles
make %{?_smp_mflags}

%check
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 pyflakes
export PYTHONPATH=/usr/lib/python3.7/site-packages
export PYTHON=/usr/bin/python3
export PYTHON_VERSION=3.7
export PYTHON_VERSIONS=python3
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/lib/"
cd ./libraries/libapparmor
make check
cd ../../binutils/
make check
cd ../utils
make check

%install
export PYTHONPATH=/usr/lib/python3.7/site-packages
export PYTHON=/usr/bin/python3
export PYTHON_VERSION=3.7
export PYTHON_VERSIONS=python3
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/lib/"
cd libraries/libapparmor
make DESTDIR=%{buildroot} install
cd ../../binutils/
make DESTDIR=%{buildroot} install
cd ../parser
make DESTDIR=%{buildroot} install
cd ../utils
make DESTDIR=%{buildroot} install
cd ../changehat/mod_apparmor
make DESTDIR=%{buildroot} install
cd ../pam_apparmor
make DESTDIR=%{buildroot} install
cd ../../profiles
make DESTDIR=%{buildroot} install

%files -n libapparmor
%defattr(-,root,root)
%license LICENSE
%{_libdir}/libapparmor.so.*

%post -n libapparmor
/sbin/ldconfig

%postun -n libapparmor
/sbin/ldconfig

%files -n libapparmor-devel
%defattr(-,root,root)
%{_libdir}/libapparmor.a
%{_libdir}/libapparmor.la
%{_libdir}/libapparmor.so
%{_libdir}/pkgconfig/libapparmor.pc
%dir %{_includedir}/aalogparse
%dir %{_includedir}/sys
%{_includedir}/aalogparse/*
%{_includedir}/sys/*
%doc %{_mandir}/man2/aa_change_hat.2.gz
%doc %{_mandir}/man2/aa_find_mountpoint.2.gz
%doc %{_mandir}/man2/aa_getcon.2.gz
%doc %{_mandir}/man2/aa_query_label.2.gz
%doc %{_mandir}/man3/aa_features.3.gz
%doc %{_mandir}/man3/aa_kernel_interface.3.gz
%doc %{_mandir}/man3/aa_policy_cache.3.gz
%doc %{_mandir}/man3/aa_splitcon.3.gz

%files -n apache2-mod_apparmor
%defattr(-,root,root)
%{_libdir}/httpd/modules/mod_apparmor.so
%doc %{_mandir}/man8/mod_apparmor.8.gz

%files profiles
%defattr(-,root,root,755)
%dir %{_sysconfdir}/apparmor.d/apache2.d
%config(noreplace) %{_sysconfdir}/apparmor.d/apache2.d/phpsysinfo
%config(noreplace) %{_sysconfdir}/apparmor.d/bin.*
%config(noreplace) %{_sysconfdir}/apparmor.d/sbin.*
%config(noreplace) %{_sysconfdir}/apparmor.d/usr.*
%config(noreplace) %{_sysconfdir}/apparmor.d/local/*
%dir %{_datadir}/apparmor
%{_datadir}/apparmor/extra-profiles/*

%files parser
%defattr(755,root,root,755)
/sbin/apparmor_parser
/sbin/rcapparmor
/lib/apparmor/rc.apparmor.functions
/lib/apparmor/apparmor.systemd
%{_bindir}/aa-exec
%{_bindir}/aa-enabled
%attr(644,root,root) %{_prefix}%{_unitdir}/apparmor.service
%dir %{_sysconfdir}/apparmor
%dir %{_sysconfdir}/apparmor.d
%config(noreplace) %{_sysconfdir}/apparmor/parser.conf
%config(noreplace) %{_sysconfdir}/apparmor/subdomain.conf
%{_localstatedir}/lib/apparmor
%doc %{_mandir}/man5/apparmor.d.5.gz
%doc %{_mandir}/man5/apparmor.vim.5.gz
%doc %{_mandir}/man5/subdomain.conf.5.gz
%doc %{_mandir}/man7/apparmor.7.gz
%doc %{_mandir}/man8/apparmor_parser.8.gz
%doc %{_mandir}/man1/aa-enabled.1.gz
%doc %{_mandir}/man1/aa-exec.1.gz
%doc %{_mandir}/man2/aa_stack_profile.2.gz

%preun parser
%systemd_preun apparmor.service

%post parser
%systemd_post apparmor.service

%postun parser
%systemd_postun_with_restart apparmor.service

%files abstractions
%defattr(644,root,root,755)
%dir %{_sysconfdir}/apparmor.d/abstractions
%config(noreplace) %{_sysconfdir}/apparmor.d/abstractions/*
%dir %{_sysconfdir}/apparmor.d/disable
%dir %{_sysconfdir}/apparmor.d/local
%dir %{_sysconfdir}/apparmor.d/tunables
%config(noreplace) %{_sysconfdir}/apparmor.d/tunables/*
%exclude %{_datadir}/locale

%files utils
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/apparmor/easyprof.conf
%config(noreplace) %{_sysconfdir}/apparmor/logprof.conf
%config(noreplace) %{_sysconfdir}/apparmor/notify.conf
%config(noreplace) %{_sysconfdir}/apparmor/severity.db
/sbin/aa-teardown
%{_sbindir}/aa-*
%{_sbindir}/apparmor_status
%{_bindir}/aa-easyprof
%{_datadir}/apparmor/easyprof/
%dir %{_datadir}/apparmor
%{_datadir}/apparmor/apparmor.vim
%doc %{_mandir}/man2/aa_change_profile.2.gz
%doc %{_mandir}/man5/logprof.conf.5.gz
%doc %{_mandir}/man8/aa-*.gz
%doc %{_mandir}/man8/apparmor_status.8.gz

%files -n pam_apparmor
%defattr(-,root,root,755)
/lib/security/pam_apparmor.so

%files -n python3-apparmor
%defattr(-,root,root)
%{python3_sitelib}/*

%files -n perl-apparmor
%defattr(-,root,root)
%{perl_vendorarch}/auto/LibAppArmor/
%{perl_vendorarch}/LibAppArmor.pm
%exclude %{perl_archlib}/perllocal.pod

%changelog
*   Wed Mar 03 2021 Andrew Phelps <anphel@microsoft.com> 2.13-12
-   Add patch to severity.db to fix tests.
*   Mon Sep 28 2020 Daniel McIlvaney <damcilva@microsoft.com> 2.13-11
-   Nopatch CVE-2016-1585
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 2.13-10
-   Added %%license line automatically
*   Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> 2.13-9
-   Renaming Linux-PAM to pam
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.13-8
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Tue Mar 05 2019 Siju Maliakkal <smaliakkal@vmware.com> 2.13-7
-   Excluded conflicting perllocal.pod
*   Thu Dec 06 2018 Keerthana K <keerthanak@vmware.com> 2.13-6
-   Fixed make check failures.
*   Fri Oct 05 2018 Tapas Kundu <tkundu@vmware.com> 2.13-5
-   Updated using python 3.7 libs
*   Wed Oct 03 2018 Keerthana K <keerthanak@vmware.com> 2.13-4
-   Depcrecated ruby apparmor package.
-   Modified the perl and python path to generic.
*   Wed Sep 26 2018 Ajay Kaher <akaher@vmware.com> 2.13-3
-   Fix for aarch64
*   Thu Sep 20 2018 Keerthana K <keerthanak@vmware.com> 2.13-2
-   Updated the ruby packagefor latest version.
*   Thu Aug 30 2018 Keerthana K <keerthanak@vmware.com> 2.13-1
-   Initial Apparmor package for Photon.
