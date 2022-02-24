Vendor:         Microsoft Corporation
Distribution:    Mariner
Summary:	Real-time file compressor
Name:		lzop
Version:	1.04
Release:	5%{?dist}
License:	GPLv2+
URL:		https://www.lzop.org/
Source:		https://www.lzop.org/download/%{name}-%{version}.tar.gz
BuildRequires:	gcc
BuildRequires:	lzo-devel

%description
lzop is a compression utility which is designed to be a companion to gzip.
It is based on the LZO data compression library and its main advantages over
gzip are much higher compression and decompression speed at the cost of some
compression ratio. The lzop compression utility was designed with the goals
of reliability, speed, portability and with reasonable drop-in compatibility
to gzip.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
%make_install INSTALL='install -p' install
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS NEWS README THANKS
%{_bindir}/%{name}
%{_mandir}/man?/%{name}.*

%changelog
* Thu Feb 24 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.04-5
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.04-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Kamil Dudka <kdudka@redhat.com> - 1.04-1
- update to 1.04

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.03-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.03-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 19 2018 Kamil Dudka <kdudka@redhat.com> - 1.03-20
- add explicit BR for the gcc compiler
- use https:// in URL and Source

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.03-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.03-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.03-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.03-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Mar 08 2016 Robert Scheck <robert@fedoraproject.org> - 1.03-15
- Added patch from openSUSE to fix building using GCC 6 (#1307760)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.03-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 29 2015 Robert Scheck <robert@fedoraproject.org> - 1.03-13
- Added patch by Khem Raj to use static inlines as the external
  inline definition has changed with GCC 5 (to fix ppc64 builds)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 28 2012 Kamil Dudka <kdudka@redhat.com> - 1.03-7
- revert specfile changes that cause problems to Robert Scheck

* Tue Aug 28 2012 Kamil Dudka <kdudka@redhat.com> - 1.03-6
- fix specfile issues reported by the fedora-review script

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 31 2010 Robert Scheck <robert@fedoraproject.org> 1.03-2
- Minor spec file cleanups and updated %%description

* Tue Dec 07 2010 Kamil Dudka <kdudka@redhat.com> - 1.03-1
- update to 1.03

* Wed Mar 03 2010 Kamil Dudka <kdudka@redhat.com> - 1.02-0.9.rc1
- license changed to GPLv2+
- added -q option to %%setup

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.02-0.8.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Robert Scheck <robert@fedoraproject.org> 1.02-0.7.rc1
- Rebuild against gcc 4.4 and rpm 4.6

* Tue Sep 18 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 1.02-0.6.rc1
- gcc 4.3 rebuild

* Tue Sep 18 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 1.02-0.5.rc1
- License fix

* Sat Sep 02 2006  Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 1.02-0.4.rc1
- FE6 Rebuild

* Sun Jul 30 2006 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 1.02-0.3.rc1
- use new alphatag convention
- build with lzop 2 at last

* Mon Feb 13 2006 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 1.02-0.2
- rebuilt for new gcc4.1 snapshot and glibc changes
- build with lzop 1 since lzop 2 hasn't been merged yet

* Thu Jan 19 2006 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 1.02-0.1
- update to 1.02rc1
- build with lzop 2

* Wed Jan 18 2006 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 1.01-4
- gcc 4.1 build time

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com>
- 1.01-3
- rebuild on all arches

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Tue Apr 20 2004 Nicolas Mailhot <Nicolas.Mailhot at laPoste.net>
- 0:1.01-0.fdr.1
- Fedorization

* Tue Mar 09 2004 Dag Wieers <dag@wieers.com>
- 1.01-1
- Initial package. (using DAR)
