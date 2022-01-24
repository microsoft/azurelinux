# mod_ipv6calc related
%{!?_httpd_apxs:    %{expand: %%global _httpd_apxs    %%{_sbindir}/apxs}}
%{!?_httpd_moddir:  %{expand: %%global _httpd_moddir  %%{_libdir}/httpd/modules}}
%{!?_httpd_confdir: %{expand: %%global _httpd_confdir %%{_sysconfdir}/httpd/conf.d}}
# database support (deselectable)
%if "%{?_without_ip2location:0}%{?!_without_ip2location:1}" == "1"
%define enable_ip2location 1
%endif
%if "%{?_without_geoip:0}%{?!_without_geoip:1}" == "1"
%define enable_geoip 1
%endif
%if "%{?_without_dbip:0}%{?!_without_dbip:1}" == "1"
%define enable_dbip 1
%endif
%if "%{?_without_external:0}%{?!_without_external:1}" == "1"
%define enable_external 1
%endif
# database locations
%define ip2location_db	%{_datadir}/IP2Location
%define geoip_db	%{_datadir}/GeoIP
%define dbip_db		%{_datadir}/DBIP
%define external_db	%{_datadir}/%{name}/db
# Berkeley DB selector
%define require_db4 %(echo "%{dist}" | grep -E -q '^\.el(5|6)$' && echo 1 || echo 0)
# shared library support (deselectable)
%if "%{?_without_shared:0}%{?!_without_shared:1}" == "1"
%define enable_shared 1
%endif
Summary:        IPv6 address format change and calculation utility
Name:           ipv6calc
Version:        2.2.0
Release:        42%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://www.deepspace6.net/projects/%{name}.html
Source0:        ftp://ftp.bieringer.de/pub/linux/IPv6/ipv6calc/%{name}-%{version}.tar.gz
Patch0:         ipv6calc-2.2.0-patch-8c7eea58.diff
BuildRequires:  gcc
BuildRequires:  openssl-devel
BuildRequires:  perl
BuildRequires:  procps-ng
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
#Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
%if %{enable_shared}
Provides:       ipv6calc-libs = %{version}-%{release}
%else
Conflicts:      ipv6calc-libs
%endif

%if %{require_db4}
BuildRequires:  db4-devel
%else
BuildRequires:  libdb-devel
%endif

%description
ipv6calc is a small utility which formats and calculates IPv4/IPv6 addresses
in different ways.

Install this package, if you want to retrieve information about a particular
IPv4/IPv6/MAC address (-i ADDRESS) or make life easier in adding entries to
reverse IPv6 DNS zones (e.g. -a 2001:db8:1234::1/48).

In addition many format and type conversions are supported, see online help
and/or given URL for more.

Also this package contains additional programs
 - ipv6loganon: anonymize Apache web server logs
 - ipv6logconv: special Apache web server log converter
    (examples included for use with analog)
 - ipv6logstats: create statistics from list of IPv4/IPv6 addresses
    (examples included for use with gnu-plot)
 - mod_ipv6calc: Apache module for anonymization/information logging on-the-fly

Support for following databases
 - IP2Location	%{?enable_ip2location:ENABLED}%{?!enable_ip2location:DISABLED}
		default directory for downloaded db files: %{ip2location_db}
		(requires also external library on system)

 - GeoIP	%{?enable_geoip:ENABLED}%{?!enable_geoip:DISABLED}
		default directory for downloaded db files: %{geoip_db}
		(requires also external library on system)

 - GeoIP v2	%{?enable_mmdb:ENABLED}%{?!enable_mmdb:DISABLED}
		default directory for downloaded db files: %{geoip_db}
		(requires also external library on system)

 - db-ip.com	%{?enable_dbip:ENABLED}%{?!enable_dbip:DISABLED}
		(once generated database files are found on system)
		default directory for generated db files: %{dbip_db}

 - db-ip.com v2	%{?enable_mmdb:ENABLED}%{?!enable_mmdb:DISABLED}
		(once generated database files are found on system)
		default directory for generated db files: %{dbip_db}

 - External	%{?enable_external:ENABLED}%{?!enable_external:DISABLED}
		default directory for generated db files: %{external_db}

Built %{?enable_shared:WITH}%{?!enable_shared:WITHOUT} shared-library

Available rpmbuild rebuild options:
  --without ip2location
  --without geoip
  --without dbip
  --without mmdb (which disables GeoIP v2 and db-ip.com v2)
  --without external
  --without shared
  --without mod_ipv6calc

%package ipv6calcweb
Summary:        IP address information web utility
BuildRequires:  perl(Digest::MD5)
Requires:       httpd
Requires:       ipv6calc
Requires:       perl(Digest::MD5)

%description ipv6calcweb
ipv6calcweb contains a CGI program and a configuration file for
displaying information of IP addresses on a web page using ipv6calc.

Check/adjust %{_sysconfdir}/httpd/conf.d/ipv6calcweb.conf
Default restricts access to localhost

%prep
%setup -q

%patch0 -p1

%configure \
	%{?enable_ip2location:--enable-ip2location} \
	%{?enable_ip2location:--with-ip2location-dynamic --with-ip2location-headers-fallback} \
	--with-ip2location-db=%{ip2location_db} \
	%{?enable_geoip:--enable-geoip} \
	%{?enable_geoip:--with-geoip-dynamic --with-geoip-headers-fallback} \
	--with-geoip-db=%{geoip_db} \
	%{?enable_dbip:--enable-dbip} \
	--with-dbip-db=%{dbip_db} \
	%{?enable_mmdb:--enable-mmdb --with-mmdb-dynamic} \
	%{?enable_external:--enable-external} \
	--with-external-db=%{external_db} \
	%{?enable_shared:--enable-shared} \
	%{?enable_mod_ipv6calc:--enable-mod_ipv6calc}


%build
make clean
make %{?_smp_mflags} COPTS="%{optflags}"


%install
make install DESTDIR=%{buildroot}

## Install examples and helper files
install -d -p %{buildroot}%{_docdir}/%{name}-%{version}/

## examples
install -d %{buildroot}%{_datadir}/%{name}/examples/

# ipv6logconv
install -d %{buildroot}%{_datadir}/%{name}/examples/ipv6logconv
for file in examples/analog/*.{cfg,txt,tab,sh}; do
	install $file %{buildroot}%{_datadir}/%{name}/examples/ipv6logconv/
done

# ipv6loganon
install -d %{buildroot}%{_datadir}/%{name}/examples/ipv6loganon
for file in ipv6loganon/README; do
	install $file %{buildroot}%{_datadir}/%{name}/examples/ipv6loganon/
done

# ipv6logstats
install -d %{buildroot}%{_datadir}/%{name}/examples/ipv6logstats
for file in ipv6logstats/README ipv6logstats/example_* ipv6logstats/collect_ipv6logstats.pl; do
	install $file %{buildroot}%{_datadir}/%{name}/examples/ipv6logstats/
done


# db directory
install -d %{buildroot}%{external_db}

# selinux
install -d %{buildroot}%{_datadir}/%{name}/selinux


# ipv6calcweb
install -d %{buildroot}%{_sysconfdir}/httpd/conf.d
install -d %{buildroot}%{_localstatedir}/www/cgi-bin

install ipv6calcweb/ipv6calcweb.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/
install -m 755 ipv6calcweb/ipv6calcweb.cgi  %{buildroot}%{_localstatedir}/www/cgi-bin/
install -m 644 ipv6calcweb/ipv6calcweb-databases-in-var.te  %{buildroot}%{_datadir}/%{name}/selinux/

%check
%ifnarch ppc64
	make test
%endif


%files
%license COPYING LICENSE
%doc ChangeLog README README.* CREDITS TODO USAGE doc/ipv6calc.lyx doc/ipv6calc.sgml doc/ipv6calc.html doc/ipv6calc.xml

%defattr(644,root,root,755)

# binaries
%attr(755,-,-) %{_bindir}/*

# man pages
%{_mandir}/man8/*

# tools
%attr(755,-,-) %{_datadir}/%{name}/tools/*

# selinux
%attr(644,-,-) %{_datadir}/%{name}/selinux/*

# shared library
%{?enable_shared:%attr(755,-,-) %{_libdir}/libipv6calc*}

# database directory
%{external_db}

# examples
%attr(755,-,-) %{_datadir}/%{name}/examples/*/*.pl
%attr(755,-,-) %{_datadir}/%{name}/examples/*/*.sh
%{_datadir}/%{name}/examples/ipv6loganon/
%{_datadir}/%{name}/examples/ipv6logconv/
%{_datadir}/%{name}/examples/ipv6logstats/

%files ipv6calcweb
%license COPYING LICENSE
%doc ipv6calcweb/README ipv6calcweb/USAGE

%defattr(644,root,root,755)

%attr(755,-,-) %{_localstatedir}/www/cgi-bin/ipv6calcweb.cgi
%config(noreplace) %{_sysconfdir}/httpd/conf.d/ipv6calcweb.conf

%post
%{_sbindir}/ldconfig

%postun
%{_sbindir}/ldconfig

%changelog
* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.2.0-42
- Removing the explicit %%clean stage.

* Wed Oct 21 2020 Henry Beberman <henry.beberman@microsoft.com> - 2.2.0-41
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- License verified.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 24 2020 Peter Bieringer <pb@bieringer.de> - 2.2.0-39
- add patch for BZ#1793903

* Sat Oct 12 2019 Peter Bieringer <pb@bieringer.de> - 2.2.0-38
- new release 2.2.0

* Sat Sep 07 2019 Peter Bieringer <pb@bieringer.de> - 2.1.1-36
- new release 2.1.1

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.1.0-34
- Perl 5.30 rebuild

* Fri Apr 05 2019 Peter Bieringer <pb@bieringer.de> - 2.1.0-33
- new release 2.1.0

* Tue Feb 05 2019 Peter Bieringer <pb@bieringer.de> - 2.0.0-32
- new release 2.0.0
- subpackage ipv6calcweb: remove dependency Perl(Proc::ProcessTable)
- add dependency libmaxminddb-devel

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jan 26 2019 Peter Bieringer <pb@bieringer.de> - 1.1.0-29
- new release 1.1.0
- subpackage ipv6calcweb: add dependency Perl(Proc::ProcessTable)
- fix bug in lib/libipv6addr.c

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.0.0-26
- Perl 5.28 rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Peter Bieringer <pb@bieringer.de> - 1.0.0-24
- fix compiler warnings introduced with gcc8 and also code (BZ#1541367)

* Mon Sep 18 2017 Peter Bieringer <pb@bieringer.de> - 1.0.0-23
- mod_ipv6calc: fix missing link flags

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun 23 2017 Peter Bieringer <pb@bieringer.de> - 1.0.0-20
- new release 1.0.0

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.99.2-19
- Perl 5.26 rebuild

* Sun Apr 16 2017 Peter Bieringer <pb@bieringer.de>
- add missing build requirement procps-ng

* Sun Feb 12 2017 Peter Bieringer <pb@bieringer.de>
- add ipv6calc-0.99.2-2017-02-12.patch to fix broken build

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 28 2016 Peter Bieringer <pb@bieringer.de> - 0.99.2-17
- new release 0.99.2
- add support for git commit hash

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.99.1-16
- Perl 5.24 rebuild

* Thu Feb 04 2016 Peter Bieringer <pb@bieringer.de> - 0.99.1-15
- minor fixes to make fedpkg lint happy

* Wed Feb 03 2016 Peter Bieringer <pb@bieringer.de> - 0.99.1-14
- conditionally set compiler option -Wno-unused-const-variable

* Sat Sep 05 2015 Peter Bieringer <pb@bieringer.de> - 0.99.1-13
- new release 0.99.1 (introduces new subpackage mod_ipv6calc)

* Sat Jul 25 2015 Peter Bieringer <pb@bieringer.de>
- Replace ipv6calc.{lyx,sgml,html,xml} by dedicated file.suffix

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.99.0-11
- Perl 5.22 rebuild

* Sat May 02 2015 Peter Bieringer <pb@bieringer.de> - 0.99.0-10
- new release 0.99.0

* Mon Mar 02 2015 Peter Bieringer <pb@bieringer.de> - 0.98.0-10
- new (fixed) upstream 0.98.0 tar.gz

* Sun Mar 01 2015 Peter Bieringer <pb@bieringer.de> - 0.98.0-9
- remove not necessary x-bits for some files by proper definition in files section

* Fri Feb 20 2015 Peter Bieringer <pb@bieringer.de> - 0.98.0-8
- new release 0.98.0

* Wed Feb 18 2015 Peter Bieringer <pb@bieringer.de>
- add support for conditional builds

* Sat Oct 25 2014 Peter Bieringer <pb@bieringer.de>
- add /usr/share/ipv6calc/db directory

* Sat Oct 11 2014 Peter Bieringer <pb@bieringer.de>
- add additional requirements for ipv6calc-ipv6calcweb
- enable db-ip.com & external database support

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.97.4-7
- Perl 5.20 rebuild

* Tue Aug 19 2014 Peter Bieringer <pb@bieringer.de> - 0.97.4-7
- new package for EPEL6/EPEL7

* Sun Aug 17 2014 Peter Bieringer <pb@bieringer.de>
- add missing requirement for ipv6calc-ipv6calcweb

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 02 2014 Peter Bieringer <pb@bieringer.de> - 0.97.4-5
- new release 0.97.4

* Thu Jul 31 2014 Peter Bieringer <pb@bieringer.de>
- include also tools into main package
- remove UTF-8 conversion, fixed in upstream now

* Tue Jul 29 2014 Peter Bieringer <pb@bieringer.de>
- introduce subpackage ipv6calcweb (align with upstream)
- enable fallback option for IP2Location
- build with dynamic load of GeoIP and IP2Location support

* Thu Jul 17 2014 Peter Bieringer <pb@bieringer.de>
- replace DESTDIR=$RPM_BUILD_ROOT with macro, define BuildRoot

* Wed Jul 16 2014 Peter Bieringer <pb@bieringer.de>
- change requirements from krb5-libs/devel to openssl(-libs)/-devel

* Tue Jul 15 2014 Peter Bieringer <pb@bieringer.de> - 0.97.3-3
- align package description with upstream

* Mon Jul 14 2014 Peter Bieringer <pb@bieringer.de> - 0.97.3-2
- new release 0.97.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Marcela Mašláňová <mmaslano@redhat.com> - 0.97.2-2
- new release 0.97.2

* Wed May 21 2014 Marcela Mašláňová <mmaslano@redhat.com> - 0.97.1-1
- new release 0.97.1

* Mon May 19 2014 Marcela Mašláňová <mmaslano@redhat.com> - 0.97.0-1
- new release 0.97

* Fri Feb 14 2014 Marcela Mašláňová <mmaslano@redhat.com> - 0.96.0-1
- new release 0.96

* Mon Dec  2 2013 Marcela Mašláňová <mmaslano@redhat.com> - 0.95.0-1
- new release #1033041

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.94.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 0.94.1-2
- Perl 5.18 rebuild

* Tue May 14 2013 Marcela Mašláňová <mmaslano@redhat.com> - 0.94.1-1
- update to 0.94.1

* Mon Feb 18 2013 Marcela Mašláňová <mmaslano@redhat.com> - 0.93.1-6
- fix days in changelog

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.93.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Aug  2 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.93.1-4
- 804317 on ppc64 tests never fully worked, conditionalized

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.93.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.93.1-2
- Perl 5.16 rebuild

* Mon Feb  6 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.93.1-1
- minor update

* Sun Jan 22 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.93.0-1
- update to 0.93 release
- add Perl requirements for cgi

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.92.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 10 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.92.0-1
- update to 0.92 release

* Fri May 27 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.90.0-1
- update to 0.90 release

* Fri May  6 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.82.1-1
- update to 0.82.1 release

* Wed Mar 30 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.82.0-1
- update to 0.82.0 release

* Mon Feb 28 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.81.0-1
- update to the new upstream version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.80.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan  4 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.80.0-1
- update to the latest version

* Mon Mar 01 2010 Marcela Mašláňová <mmaslano@redhat.com> - 0.73.0-1
- update to the latest version

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.72.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 01 2009 Marcela Mašláňová <mmaslano@redhat.com> - 0.72.1-1
- update to the latest version
- change installonly to standart DESTDIR

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.71.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.71.0-3
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.71.0-2
- Autorebuild for GCC 4.3

* Mon Aug 20 2007 Marcela Maslanova <mmaslano@redhat.com> - 0.71.0-1
- new version from upstream

* Tue Feb 27 2007 Marcela Maslanova <mmaslano@redhat.com> - 0.61-2
- package merge review
- rhbz#225910

* Fri Sep 01 2006 Marcela Maslanova <mmaslano@redhat.com> - 0.61-1
- upgrade to 0.61-1 - from upstream

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.60.1-1.1
- rebuild

* Tue Jul 11 2006 Radek Vokál <rvokal@redhat.com> 0.60.1-1
- upgrade to 0.60.1 - fix for big endian archs

* Sun Jun 25 2006 Radek Vokál <rvokal@redhat.com> 0.60.0-1
- upgrade to 0.60.0

* Wed Feb 22 2006 Radek Vokál <rvokal@redhat.com> 0.51-1
- upgrade to 0.51

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.50-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.50-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Sep 16 2005 Radek Vokal <rvokal@redhat.com> 0.50-1
- due to several other off-by-one bugs upgrade to 0.50

* Thu Sep 15 2005 Radek Vokal <rvokal@redhat.com> 0.49-2
- smash stack fix in ipv6calc_copy
- increase len of tmpstr

* Thu Sep 15 2005 Radek Vokal <rvokal@redhat.com> 0.49-1
- upgrade to 0.49

* Tue Apr 19 2005 Radek Vokal <rvokal@redhat.com> 0.48-5
- using CVS tarball, patch clean-up

* Sun Apr 17 2005 Robert Scheck <redhat@linuxnetz.de> 
- lots of spec file cleanups (#155164)

* Wed Apr 13 2005 Florian La Roche <laroche@redhat.com>
- remove empty scripts

* Fri Mar 04 2005 Radek Vokal <rvokal@redhat.com> 0.48-3
- gcc4 rebuilt

* Mon Nov 1 2004 Radek Vokal <rvokal@redhat.com> 0.48-2
- spec file cleanup
- md5 patch for makefile

* Sat Oct 30 2004 Peter Bieringer <pb@bieringer.de> 
- remove openssl(-devel) from requirements, no longer needed

* Tue Oct 26 2004 Radek Vokal <rvokal@redhat.com> 0.47-4
- spec file cleanup, typo patch

* Mon Oct 18 2004 Radek Vokal <rvokal@redhat.com> 0.47-3
- initial build for Fedora Core

* Sat Nov 22 2003 Peter Bieringer <pb@bieringer.de>
- adjustments

* Fri Nov 21 2003 Peter Bieringer <pb@bieringer.de>
- add ipv6logstats
- add man pages
- add configure options

* Mon Nov 11 2002 Peter Bieringer <pb@bieringer.de>
- change IPv6 address in description

* Sat Apr 20 2002 Peter Bieringer <pb@bieringer.de>
- Change URL

* Sun Apr 07 2002 Peter Bieringer <pb@bieringer.de>
- add more analog example files

* Fri Apr 05 2002 Peter Bieringer <pb@bieringer.de>
- remove BuildRequires extension, not needed for normal build

* Sun Mar 24 2002 Peter Bieringer <pb@bieringer.de>
- extend BuildRequires for perl /usr/bin/aggregate wget

* Mon Mar 18 2002 Peter Bieringer <pb@bieringer.de>
- add ipv6calcweb.cgi

* Sat Mar 16 2002 Peter Bieringer <pb@bieringer.de>
- add ipv6logconv, analog examples

* Mon Mar 11 2002 Peter Bieringer <pb@bieringer.de>
- Add perl to buildrequire and openssl to require

* Mon Jan 21 2002 Peter Bieringer <pb@bieringer.de>
- Add LICENSE + COPYING file

* Thu Dec 27 2001 Peter Bieringer <pb@bieringer.de>
- Add comment header
- Add call to configure on build

* Tue Dec 18 2001 Peter Bieringer <pb@bieringer.de>
- Replace hardwired version number with autoconf/configure variable

* Wed Apr 25 2001 Peter Bieringer <pb@bieringer.de>
- Fix permissions of doc files

* Thu Mar 15 2001 Peter Bieringer <pb@bieringer.de>
- Add doc directory also to files to make sure the directory will be removed on update or deinstall
- change install permissions for entries in doc directory
- change "make install" to "make installonly" (make test should be only executed once)

* Wed Mar 14 2001 Peter Bieringer <pb@bieringer.de>
- Add "make clean" and "make test" on build

* Tue Mar 13 2001 Peter Bieringer <pb@bieringer.de>
- add CREDITS and TODO for install

* Sat Mar 10 2001 Peter Bieringer <pb@bieringer.de>
- enable "URL"

* Sun Mar 04 2001 Peter Bieringer <pb@bieringer.de>
- change install location to /bin

* Tue Feb 27 2001 Peter Bieringer <pb@bieringer.de>
- review for new release, now named "ipv6calc"
- review install section for RedHat 7.0.91

* Sun Feb 25 2001 Peter Bieringer <pb@bieringer.de>
- initial build
