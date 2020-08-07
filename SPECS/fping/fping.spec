Summary:       Utility to send ICMP echo probes to network hosts
Name:          fping
Version:       4.2
Release:       2%{?dist}
License:       BSD with advertising
Group:         Productivity/Networking/Diagnostic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:           https://www.fping.org/
Source0:       https://fping.org/dist/%{name}-%{version}.tar.gz
BuildRequires: autoconf
BuildRequires: automake

%description
fping is a ping like program which uses the Internet Control Message Protocol
(ICMP) echo request to determine if a target host is responding.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
ln -sf fping %{buildroot}%{_sbindir}/fping6
rm -rf %{buildroot}%{_infodir}

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%license COPYING
%{_sbindir}/fping
%{_sbindir}/fping6
%doc CHANGELOG.md COPYING
%doc %{_mandir}/man8/fping.8*

%changelog
* Sat May 09 00:20:36 PST 2020 Nick Samson <nisamson@microsoft.com> - 4.2-2
- Added %%license line automatically

*   Mon Mar 16 2020 Henry Beberman <henry.beberman@microsoft.com> 4.2-1
-   Updated to 4.2. Updated License.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 4.1-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
* Wed Jan 23 2019 Dweep Advani <dadvani@vmware.com> 4.1-1
- Added fping package to Photon 2.0
