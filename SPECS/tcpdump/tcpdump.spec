Summary:        Packet Analyzer
Name:           tcpdump
Version:        4.99.4
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Networking
URL:            https://www.tcpdump.org
Source0:        https://www.tcpdump.org/release/%{name}-%{version}.tar.gz
BuildRequires:  libpcap-devel
Requires:       libpcap

%description
Tcpdump is a common packet analyzer that runs under the command line.
It allows the user to display TCP/IP and other packets being
transmitted or received over a network to which the computer is attached.

%prep
%autosetup -p1

%build
%configure
make %{?_smp_mflags}

%install
# make install installs to /usr/bin in 4.99.1
# so specify install to sbin instead
mkdir -p %{buildroot}/%{_sbindir}
mkdir -p %{buildroot}/%{_mandir}/man1

chmod 755 %{buildroot}/%{_sbindir}
chmod 755 %{buildroot}/%{_mandir}/man1

install -m755 tcpdump %{buildroot}%{_sbindir}/tcpdump
ln -sf tcpdump %{buildroot}%{_sbindir}/tcpdump.%{version}
install -m755 tcpdump.1 %{buildroot}%{_mandir}/man1/tcpdump.1

find %{buildroot} -type f -name "*.la" -delete -print

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%license LICENSE
%{_sbindir}/*
%{_mandir}/man1/*

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.99.4-1
- Auto-upgrade to 4.99.4 - Azure Linux 3.0 - package upgrades

* Tue Feb 08 2022 Rachel Menge <rachelmenge@microsoft.com> - 4.99.1-1
- Update to 4.99.1

* Fri Nov 13 2020 Thomas Crain <thcrain@microsoft.com> - 4.9.3-3
- Patch CVE-2020-8037
- Lint to Mariner style

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 4.9.3-2
- Added %%license line automatically

* Tue Apr 21 2020 Emre Girgin <mrgirgin@microsoft.co> - 4.9.3-1
- Upgrade to 4.9.3 to resolve 28 CVEs.
- Fixed CVE-2020-10103.
- Fixed CVE-2020-10105.
- Update Source0 and URL.
- License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 4.9.2-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Mar 14 2019 Michelle Wang <michellew@vmware.com> - 4.9.2-2
- Add patch CVE-2018-19519

* Fri Sep 15 2017 Dheeraj Shetty <dheerajs@vmware.com> - 4.9.2-1
- Updating version to 4.9.2

* Thu Sep 07 2017 Dheeraj Shetty <dheerajs@vmware.com> - 4.9.1-2
- Fix for CVE-2017-11541 CVE-2017-11542 and CVE-2017-11543

* Thu Aug 03 2017 Dheeraj Shetty <dheerajs@vmware.com> - 4.9.1-1
- Updating version to 4.9.1

* Thu Feb 02 2017 Dheeraj Shetty <dheerajs@vmware.com> - 4.9.0-1
- Adding latest version to handle following CVEs
- CVE-2016-7922, CVE-2016-7923, CVE-2016-7924, CVE-2016-7925,
- CVE-2016-7926, CVE-2016-7927, CVE-2016-7928, CVE-2016-7929,
- CVE-2016-7930, CVE-2016-7931, CVE-2016-7932, CVE-2016-7933,
- CVE-2016-7934, CVE-2016-7935, CVE-2016-7936, CVE-2016-7937,
- CVE-2016-7938, CVE-2016-7939, CVE-2016-7940, CVE-2016-7973,
- CVE-2016-7974, CVE-2016-7975, CVE-2016-7983, CVE-2016-7984,
- CVE-2016-7985, CVE-2016-7986, CVE-2016-7992, CVE-2016-7993,
- CVE-2016-8574, CVE-2016-8575, CVE-2017-5202, CVE-2017-5203,
- CVE-2017-5204, CVE-2017-5205, CVE-2017-5341, CVE-2017-5342,
- CVE-2017-5482, CVE-2017-5483, CVE-2017-5484, CVE-2017-5485,
- CVE-2017-5486

* Tue Oct 04 2016 ChangLee <changlee@vmware.com> - 4.7.4-3
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 4.7.4-2
- GA - Bump release of all rpms

* Wed Jan 20 2016 Anish Swaminathan <anishs@vmware.com> - 4.7.4-1
- Upgrade version.

* Mon Apr 6  2015 Mahmoud Bassiouny <mbassiouny@vmware.com> - 4.7.3-1
- Updating version to 4.7.3
