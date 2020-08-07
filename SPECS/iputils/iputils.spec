Summary:          Programs for basic networking
Name:             iputils
Version:          20180629
Release:          4%{?dist}
License:          BSD-3 and GPLv2+ and Rdisc
URL:              https://github.com/iputils/iputils
Group:            Applications/Communications
Vendor:           Microsoft Corporation
Distribution:     Mariner
#Source0:         https://github.com/iputils/iputils/archive/s20180629.tar.gz
Source0:          %{name}-s%{version}.tar.gz
BuildRequires:    libcap-devel libgcrypt-devel
Requires:         libcap
Requires:         libgcrypt
Obsoletes:        inetutils

%description
The Iputils package contains programs for basic networking.
%prep
%setup -q -n %{name}-s%{version}

%build
make %{?_smp_mflags} USE_IDN=no USE_GCRYPT=yes
(
cd ninfod
./configure --prefix=%{_prefix}
make %{?_smp_mflags}
)
#make html
#make man

%install
rm -fr %{buildroot}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}/%{_unitdir}

install -c clockdiff %{buildroot}%{_sbindir}/
install -cp arping %{buildroot}%{_sbindir}/
install -cp ping %{buildroot}%{_bindir}/
install -cp rdisc %{buildroot}%{_sbindir}/
install -cp tracepath %{buildroot}%{_bindir}/
install -cp traceroute6 %{buildroot}%{_bindir}/
install -cp ninfod/ninfod %{buildroot}%{_sbindir}/

ln -sf ../bin/tracepath %{buildroot}%{_sbindir}
ln -sf ../bin/traceroute6 %{buildroot}%{_sbindir}

iconv -f ISO88591 -t UTF8 RELNOTES.old -o RELNOTES.tmp
touch -r RELNOTES.old RELNOTES.tmp
mv -f RELNOTES.tmp RELNOTES.old

%files
%defattr(-,root,root)
%license LICENSE
%doc RELNOTES.old
%{_sbindir}/rdisc
%{_sbindir}/ninfod
%{_sbindir}/tracepath
%{_sbindir}/traceroute6
%{_bindir}/tracepath
%{_bindir}/traceroute6
%caps(cap_net_raw=p) %{_sbindir}/clockdiff
%caps(cap_net_raw=p) %{_sbindir}/arping
%caps(cap_net_raw=p cap_net_admin=p) %{_bindir}/ping

%changelog
* Sat May 09 00:21:37 PST 2020 Nick Samson <nisamson@microsoft.com> - 20180629-4
- Added %%license line automatically

*   Mon Apr 13 2020 Jon Slobodzian <joslobo@microsoft.com> 20180629-3
-   Verified license. Removed sha1. Fixed commented out URL. Fixed formatting.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 20180629-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Thu Sep 06 2018 Ankit Jain <ankitja@vmware.com> 20180629-1
-   Updated to version 20180629
*   Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> 20151218-4
-   Remove openssl and gnutls deps
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 20151218-3
-   GA - Bump release of all rpms
*   Thu Apr 07 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 20151218-2
-   Fixing permissions for binaries
*   Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 20151218-1
-   Updated to version 2.4.18
*   Tue Oct 20 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 20121221-1
-   Initial build.    First version
