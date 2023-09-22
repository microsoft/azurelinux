Summary:        AppArmor is an effective and easy-to-use Linux application security system.
Name:           apparmor
Version:        3.0.4
Release:        2%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Productivity/Security
URL:            https://launchpad.net/apparmor
Source0:        https://launchpad.net/apparmor/3.0/3.0.4/+download/%{name}-%{version}.tar.gz
Patch1:         apparmor-service-start-fix.patch
# CVE-2016-1585 has no upstream fix as of 2020/09/28
Patch100:       CVE-2016-1585.nopatch
BuildRequires:  apr
BuildRequires:  apr-util-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  curl-devel
BuildRequires:  dejagnu
BuildRequires:  gawk
BuildRequires:  gcc
BuildRequires:  glibc
BuildRequires:  glibc-devel
BuildRequires:  httpd
BuildRequires:  httpd-devel
BuildRequires:  httpd-tools
BuildRequires:  libgcc
BuildRequires:  libgcc-devel
BuildRequires:  libstdc++
BuildRequires:  libstdc++-devel
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  pam
BuildRequires:  pam-devel
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Pod::Checker)
BuildRequires:  perl(Pod::Html)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  swig
BuildRequires:  systemd-rpm-macros
BuildRequires:  which
%if %{with_check}
BuildRequires:  python3-pip
BuildRequires:  python3-psutil
BuildRequires:  python3-dbus
%endif

%description
AppArmor is a file and network mandatory access control
mechanism. AppArmor confines processes to the resources allowed by the
systems administrator and can constrain the scope of potential security
vulnerabilities.

%package -n libapparmor
Summary:        Utility library for AppArmor
License:        LGPLv2
Group:          Development/Libraries/C and C++

%description -n libapparmor
This package contains the AppArmor library.

%package -n libapparmor-devel
Summary:        Development headers and libraries for libapparmor
License:        LGPLv2
Group:          Development/Libraries/C and C++
Requires:       libapparmor = %{version}-%{release}

%description -n libapparmor-devel
This package contains development files for libapparmor.

%package -n apache2-mod_apparmor
Summary:        AppArmor module for apache2
Group:          Productivity/Security

%description -n apache2-mod_apparmor
This provides the Apache module needed to declare various differing
confinement policies when running virtual hosts in the webserver
by using the changehat abilities exposed through libapparmor.

%package profiles
Summary:        AppArmor profiles that are loaded into the apparmor kernel module
Group:          Productivity/Security
Requires:       apparmor-abstractions = %{version}-%{release}
Requires:       apparmor-parser = %{version}-%{release}

%description profiles
This package contains the basic AppArmor profiles.

%package parser
Summary:        AppArmor userlevel parser utility
Group:          Productivity/Security
Requires:       libapparmor = %{version}-%{release}
Requires:       systemd

%description parser
The AppArmor Parser is a userlevel program that is used to load in
program profiles to the AppArmor Security kernel module.
This package is part of a suite of tools that used to be named
SubDomain.

%package abstractions
Summary:        AppArmor abstractions and directory structure
Group:          Productivity/Security
Requires:       apparmor-parser = %{version}-%{release}

%description abstractions
AppArmor abstractions (common parts used in various profiles) and
the %{_sysconfdir}/apparmor.d/ directory structure.

%package -n pam_apparmor
Summary:        PAM module for AppArmor change_hat
Group:          Productivity/Security
Requires:       pam
Requires:       pam-devel

%description -n pam_apparmor
The pam_apparmor module provides the means for any PAM applications
that call pam_open_session() to automatically perform an AppArmor
change_hat operation in order to switch to a user-specific security
policy.

%package utils
Summary:        AppArmor User-Level Utilities Useful for Creating AppArmor Profiles
Group:          Productivity/Security
Requires:       apparmor-abstractions = %{version}-%{release}
Requires:       audit
Requires:       libapparmor = %{version}-%{release}

%description utils
This package contains programs to help create and manage AppArmor
profiles.

%package -n python3-apparmor
Summary:        Python 3 interface for libapparmor functions
Group:          Development/Libraries/Python
Requires:       libapparmor = %{version}-%{release}
Requires:       python3

%description -n python3-apparmor
This package provides the python3 interface to AppArmor. It is used for python
applications interfacing with AppArmor.

%package -n perl-apparmor
Summary:        AppArmor module for perl.
Group:          Development/Libraries/Perl
Requires:       libapparmor = %{version}-%{release}

%description -n perl-apparmor
This package contains the AppArmor module for perl.

%prep
%autosetup -p1

%build
export PYTHONPATH=%{python3_sitelib}
export PYTHON=%{python3}
export PYTHON_VERSION=%{python3_version}
export PYTHON_VERSIONS=python3
#Building libapparmor
cd ./libraries/libapparmor
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:%{_libdir}/"
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
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:%{_libdir}/"
export LIBRARY_PATH="$LIBRARY_PATH:%{_libdir}"
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
pip3 install pyflakes
pip3 install notify2
export PYTHONPATH=%{python3_sitelib}
export PYTHON=%{python3}
export PYTHON_VERSION=%{python3_version}
export PYTHON_VERSIONS=python3
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:%{_libdir}/"
cd ./libraries/libapparmor
make check
cd ../../binutils/
make check
cd ../utils
make check PYFLAKES=/usr/bin/pyflakes

%install
export PYTHONPATH=%{python3_sitelib}
export PYTHON=%{python3}
export PYTHON_VERSION=%{python3_version}
export PYTHON_VERSIONS=python3
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:%{_libdir}/"
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
%license LICENSE libraries/libapparmor/COPYING.LGPL
%{_libdir}/libapparmor.so.*

%post -n libapparmor -p /sbin/ldconfig
%postun -n libapparmor -p /sbin/ldconfig

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
%{_mandir}/man2/aa_change_hat.2.gz
%{_mandir}/man2/aa_find_mountpoint.2.gz
%{_mandir}/man2/aa_getcon.2.gz
%{_mandir}/man2/aa_query_label.2.gz
%{_mandir}/man3/aa_features.3.gz
%{_mandir}/man3/aa_kernel_interface.3.gz
%{_mandir}/man3/aa_policy_cache.3.gz
%{_mandir}/man3/aa_splitcon.3.gz

%files -n apache2-mod_apparmor
%defattr(-,root,root)
%{_libdir}/httpd/modules/mod_apparmor.so
%{_mandir}/man8/mod_apparmor.8.gz

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
%attr(644,root,root) %{_unitdir}/apparmor.service
%dir %{_sysconfdir}/apparmor
%dir %{_sysconfdir}/apparmor.d
%config(noreplace) %{_sysconfdir}/apparmor/parser.conf
%{_localstatedir}/lib/apparmor
%{_mandir}/man5/apparmor.d.5.gz
%{_mandir}/man5/apparmor.vim.5.gz
%{_mandir}/man7/apparmor.7.gz
%{_mandir}/man8/apparmor_parser.8.gz
%{_mandir}/man1/aa-enabled.1.gz
%{_mandir}/man1/aa-exec.1.gz
%{_mandir}/man2/aa_stack_profile.2.gz

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
%dir %{_sysconfdir}/apparmor.d/abi
%config(noreplace) %{_sysconfdir}/apparmor.d/abi/*
%config(noreplace) %{_sysconfdir}/apparmor.d/*
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
%{_sbindir}/aa-*
%{_sbindir}/apparmor_status
%{_bindir}/aa-easyprof
%{_bindir}/aa-features-abi
%{_datadir}/apparmor/easyprof/
%dir %{_datadir}/apparmor
%{_datadir}/apparmor/apparmor.vim
%{_mandir}/man1/aa-features-abi.1.gz
%{_mandir}/man2/aa_change_profile.2.gz
%{_mandir}/man5/logprof.conf.5.gz
%{_mandir}/man7/apparmor_xattrs.7.gz
%{_mandir}/man8/aa-*.gz
%{_mandir}/man8/apparmor_status.8.gz

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
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 3.0.4-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Mar 09 2022 Andrew Phelps <anphel@microsoft.com> - 3.04-1
- Upgrade to version 3.04

* Wed Jan 19 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 2.13-17
- Add perl Pod-Checker Pod-Html and ExtUtils-MakeMaker to build requires.

* Fri Dec 03 2021 Thomas Crain <thcrain@microsoft.com> - 2.13-16
- Remove hardcoded python3 variables in favor of macros to enable build with Python 3.9
- Add upstream patch to fix autoconf macro for python3 >= 3.8
- License verified

* Wed Sep 29 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.13-15
- Added missing BR on "systemd-rpm-macros".

* Fri Apr 02 2021 Thomas Crain <thcrain@microsoft.com> - 2.13-14
- Merge the following releases from 1.0 to dev branch
- anphel@microsoft.com, 2.13-12: Add patch to severity.db to fix tests.

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 2.13-13
- Replace incorrect %%{_lib} usage with %%{_libdir}

* Tue Nov 03 2020 Ruying Chen <v-ruyche@microsoft.com> - 2.13-12
- Systemd supports merged /usr. Update with corresponding file locations and macros.

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
