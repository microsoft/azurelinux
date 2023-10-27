Name:           traceroute
Summary:        Traces the route taken by packets over an IPv4/IPv6 network
Version:        2.1.3
Release:        1%{?dist}
License:        GPLv2+
Group:          Applications/Internet
Url:            http://traceroute.sourceforge.net
Source0:        http://downloads.sourceforge.net/project/traceroute/traceroute/traceroute-%{version}/traceroute-%{version}.tar.gz
Vendor:         Microsoft Corporation
Distribution:   Mariner


%description
The traceroute utility displays the route used by IP packets on their
way to a specified network (or Internet) host.

%prep
%setup -q


%build
make %{?_smp_mflags} CFLAGS="%{optflags}" LDFLAGS=""

%install
rm -rf %{buildroot}

install -d %{buildroot}/bin
install -m755 traceroute/traceroute %{buildroot}/bin
pushd %{buildroot}/bin
popd

install -d %{buildroot}%{_bindir}
install -m755 wrappers/tcptraceroute %{buildroot}%{_bindir}

install -d %{buildroot}%{_mandir}/man8
install -p -m644 traceroute/traceroute.8 $RPM_BUILD_ROOT%{_mandir}/man8
pushd %{buildroot}%{_mandir}/man8
ln -s traceroute.8 tcptraceroute.8
popd

%files
%defattr(-,root,root,-)
%license COPYING
%doc COPYING README TODO CREDITS
/bin/*
%{_bindir}/*
%{_mandir}/*/*


%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.1.3-1
- Auto-upgrade to 2.1.3 - Azure Linux 3.0 - package upgrades

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.1.0-7
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.1.0-6
- Removing the explicit %%clean stage.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.1.0-5
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.1.0-4
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Nov 30 2018 Ashwin H <ashwinh@vmware.com> 2.1.0-3
-   Remove traceroute6 softlink as iputils provides traceroute6
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.0-2
-   Ensure non empty debuginfo
*   Tue Mar 28 2017 Xiaolin Li <xiaolinl@vmware.com> 2.1.0-1
-   Updated to version 2.1.0.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.22-2
-   GA - Bump release of all rpms
*   Fri Feb 26 2016 Anish Swaminathan <anishs@vmware.com>  2.0.22-1
-   Initial version
