Summary:        The finger client
Name:           finger
Version:        0.17
Release:        4%{?dist}
License:        BSD with advertising
Group:          Applications/Internet
Vendor:         Microsoft Corporation
Distribution:   Mariner
# No official URL found.
Source0:        http://ftp.linux.org.uk/pub/linux/Networking/netkit/bsd-%{name}-%{version}.tar.gz
Source1:        finger.socket
Source2:        finger@.service
Source3:        LICENSE
Patch0:         bsd-finger-time.patch
Patch1:         fix-manpage-typo.patch

BuildRequires:  systemd

%description
Finger is a utility that allows users to see information about system users
(login name, home directory, name, and more) on local and remote systems.

%package server
License:           BSD
Summary:           A Server for Showing User Information
Group:             System Environment/Daemons

Requires:           finger
Requires:           systemd
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description server
The finger daemon implements a simple protocol based on RFC1196 that provides an
interface to the Name and Finger programs at several network sites. The program
is supposed to return a friendly human-oriented status report on either the
system at the moment or a person.

%prep
%setup -q -n bsd-finger-%{version}
%patch0 -p1
%patch1 -p1

%build
sed -i 's/install -s/install/' finger/Makefile
sed -i 's/install -s/install/' fingerd/Makefile
./configure \
   --prefix=%{_prefix}

make %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man{1,8}
mkdir -p %{buildroot}%{_sbindir}

mkdir -p %{buildroot}%{_unitdir}
install -m 644 %{SOURCE1} %{buildroot}%{_unitdir}
install -m 644 %{SOURCE2} %{buildroot}%{_unitdir}
install -m 644 %{SOURCE3} LICENSE
make INSTALLROOT=%{buildroot} MANDIR=/usr/share/man install

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post server
%systemd_post finger.socket

%preun server
%systemd_preun finger.socket

%postun server
%systemd_postun_with_restart finger.socket

%files
%license LICENSE
%attr(0755,root,root) %{_bindir}/finger
%{_mandir}/man1/finger.1*

%files server
%license LICENSE
%{_unitdir}/finger.socket
%{_unitdir}/finger@.service
%attr(0755,root,root) %{_sbindir}/in.fingerd
%{_mandir}/man8/in.fingerd.8*
%{_mandir}/man8/fingerd.8*

%changelog
*   Mon Apr 27 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.17-4
-   Fixed 'Source0' tag.
-   License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.17-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.17-2
-   Apply patch to generate debuginfo
*   Wed Dec 7 2016 Dheeraj Shetty <dheerajs@vmware.com> 0.17-1
-   initial version
