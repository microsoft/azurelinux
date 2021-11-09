Summary:        Trusted pre-kernel module and tools.
Name:           tboot
Version:        1.9.12
Release:        2%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://sourceforge.net/projects/tboot/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:        create-drtm-policy.sh
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  trousers-devel
Requires:       libtspi
ExclusiveArch:  x86_64

%description
Trusted Boot (tboot) is an open source, pre- kernel/VMM module that uses
Intel(R) Trusted Execution Technology (Intel(R) TXT) to perform a measured
and verified launch of an OS kernel/VMM.

%prep
%setup -q

%build
CFLAGS="%{optflags} -Wno-error=implicit-fallthrough= "
export CFLAGS
make debug=y %{?_smp_mflags}

%install
make debug=y DISTDIR=$RPM_BUILD_ROOT install
mkdir -p %{buildroot}%{_bindir}
install -m 755 %{SOURCE1} %{buildroot}%{_bindir}/create-drtm-policy.sh


%files
%doc README COPYING docs/* lcptools/Linux_LCP_Tools_User_Manual.pdf
%config %{_sysconfdir}/grub.d/20_linux_tboot
%config %{_sysconfdir}/grub.d/20_linux_xen_tboot
%{_bindir}/create-drtm-policy.sh
%{_sbindir}/acminfo
%{_sbindir}/lcp_readpol
%{_sbindir}/lcp_writepol
%{_sbindir}/lcp2_crtpol
%{_sbindir}/lcp2_crtpolelt
%{_sbindir}/lcp2_crtpollist
%{_sbindir}/lcp2_mlehash
%{_sbindir}/parse_err
%{_sbindir}/tb_polgen
%{_sbindir}/tpmnv_defindex
%{_sbindir}/tpmnv_getcap
%{_sbindir}/tpmnv_lock
%{_sbindir}/tpmnv_relindex
%{_sbindir}/txt-stat
%{_mandir}/man8/acminfo.8.gz
%{_mandir}/man8/lcp_crtpconf.8.gz
%{_mandir}/man8/lcp_crtpol.8.gz
%{_mandir}/man8/lcp_crtpol2.8.gz
%{_mandir}/man8/lcp_crtpolelt.8.gz
%{_mandir}/man8/lcp_crtpollist.8.gz
%{_mandir}/man8/lcp_mlehash.8.gz
%{_mandir}/man8/lcp_readpol.8.gz
%{_mandir}/man8/lcp_writepol.8.gz
%{_mandir}/man8/tb_polgen.8.gz
%{_mandir}/man8/txt-stat.8.gz
/boot/tboot.gz
/boot/tboot-syms


%changelog
* Thu Nov 04 2021 Henry Li <lihl@microsoft.com> 1.9.12-2
- Add mandatory grub configuration files/tooling that are missing
- Add script to create DRTM launch policy

*   Tue May 11 2021 Andrew Phelps <anphel@microsoft.com> 1.9.12-1
-   Update to version 1.9.12 for binutils 2.36.1 compatibility
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.9.7-7
-   Added %%license line automatically
*   Mon May 04 2020 Emre Girgin <mrgirgin@microsoft.com> 1.9.7-6
-   Replace BuildArch with ExclusiveArch
*   Tue Mar 24 2020 Henry Beberman <henry.beberman@microsoft.com> 1.9.7-5
-   Add patch to fix compat with GCC9. Source0 URL updated. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.9.7-4
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Dec 14 2018 Ankit Jain <ankitja@vmware.com> 1.9.7-3
-   Resolved conflict while installing the package
*   Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 1.9.7-2
-   Adding BuildArch
*   Fri Sep 07 2018 Michelle Wang <michellew@vmware.com> 1.9.7-1
-   Update to version 1.9.7.
*   Tue Aug 07 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.9.6-1
-   Update to version 1.9.6 to get it to build with gcc 7.3
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.5-2
-   Ensure non empty debuginfo
*   Thu Mar 2 2017 Alexey Makhalov <amakhalov@vmware.com> 1.9.5-1
-   Initial build. First version
