Summary:        TCP/IP stack auditing and much more
Name:           hping3
Version:        0.0.20051105
Release:        41%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://www.hping.org/
Source0:        https://src.fedoraproject.org/lookaside/pkgs/hping3/hping3-20051105.tar.gz/ca4ea4e34bcc2162aedf25df8b2d1747/hping3-20051105.tar.gz
Patch0:         hping3-include.patch
Patch1:         hping3-bytesex.patch
Patch2:         hping3-getifnamedebug.patch
Patch3:         hping3-cflags.patch
Patch4:         hping3-man.patch
Patch5:         hping3-20051105-typo.patch
Patch6:         hping3-common.patch
BuildRequires:  gcc
BuildRequires:  libpcap-devel
BuildRequires:  make
BuildRequires:  tcl-devel
Obsoletes:      hping2
Provides:       hping2

%description
hping3 is a network tool able to send custom TCP/IP packets and to
display target replies like ping do with ICMP replies. hping3 can handle
fragmentation, and almost arbitrary packet size and content, using the
command line interface.
Since version 3, hping implements scripting capabilties

%prep

%setup -q -n hping3-20051105
%patch0  -b .include
%patch1  -b .bytesex
%patch2 -p1 -b .getifnamedebug
%patch3  -b .cflags
%patch4  -b .man
%patch5 -p1
%patch6 -p1 -b .common

%build
%configure --force-libpcap
make %{?_smp_mflags}

%install

install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8}

install -m0755 hping3 %{buildroot}%{_sbindir}
install -m0644 docs/hping3.8 %{buildroot}%{_mandir}/man8

ln -sf hping3 %{buildroot}%{_sbindir}/hping
ln -sf hping3 %{buildroot}%{_sbindir}/hping2

%check
# no upstream tests available yet

%files
%license COPYING
%doc *BUGS CHANGES README TODO docs/AS-BACKDOOR docs/HPING2-HOWTO.txt
%doc docs/HPING2-IS-OPEN docs/MORE-FUN-WITH-IPID docs/SPOOFED_SCAN.txt
%doc docs/HPING3.txt
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*

%changelog
* Thu Sep 28 2023 Ameet Porwal <ameetporwal@microsoft.com> - 0.0.20051105-41
- Initial CBL-Mariner import from Fedora 38 (license: MIT).
- License verified

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.20051105-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.20051105-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.20051105-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.20051105-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.20051105-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Jeff Law <law@redhat.com> - 0.0.20051105-35
- Avoid multiple definitions of delaytable.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.20051105-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.20051105-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.20051105-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.20051105-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.20051105-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.20051105-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.20051105-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.20051105-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.20051105-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.20051105-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Sep 10 2014 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 0.0.20051105-24
- Handle AArch64

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.20051105-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.20051105-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 0.0.20051105-21
- Rebuilt for https://fedoraproject.org/wiki/Changes/f21tcl86

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.20051105-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.20051105-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jul 17 2012 Paul Wouters <pwouters@redhat.com> - 0.0.20051105-18
- Fix typo in output (tramitting -> transmitting), rhbz#781325

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.20051105-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.20051105-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.20051105-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 25 2009 Dan Horak <dan[at]danny.cz> - 0.0.20051105-14
- update the bytesex patch to include s390/s390x arch

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.20051105-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Nov 27 2008 Paul Wouters <paul@xelerance.com> - 0.0.20051105-12
- Fix for "sh" arch, see https://bugzilla.redhat.com/show_bug.cgi?id=471709

* Fri Nov  7 2008 Paul Wouters <paul@xelerance.com> - 0.0.20051105-11
- Fix for man page, see https://bugzilla.redhat.com/show_bug.cgi?id=456675

* Thu Jul 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.0.20051105-10
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.0.20051105-9
- Autorebuild for GCC 4.3

* Thu Jan  3 2008 Alex Lancaster <alexlan[AT]fedoraproject.org> - 0.0.20051105-8
- Rebuild against new Tcl 8.5

* Fri Feb 22 2007 Paul Wouters <paul@xelerance.com> 0.0.20051105-7
- Rebuild for new tcl 8.4 dependancy (it got rolled back)

* Fri Feb  2 2007 Paul Wouters <paul@xelerance.com> 0.0.20051105-6
- Rebuild for new tcl 8.5 dependancy

* Wed Nov 29 2006 Paul Wouters <paul@xelerance.com> 0.0.20051105-5
- Rebuild for new libpcap dependancy

* Thu Sep  7 2006 Paul Wouters <paul@xelerance.com> 0.0.20051105-4
- Rebuild requested for PT_GNU_HASH support from gcc

* Sun May 19 2006 Paul Wouters <paul@xelerance.com> 0.0.20051105-2
- Added Provides hping2 to fix upgrade path

* Sun May 07 2006 Paul Wouters <paul@xelerance.com> 0.0.20051105-1
- Initial Release based on hping2 package
