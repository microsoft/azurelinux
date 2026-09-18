# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		ssmtp
Version:	2.64
Release:	40%{?dist}
Summary:	Extremely simple MTA to get mail off the system to a Mailhub
License:	GPL-2.0-or-later
URL:		http://packages.debian.org/stable/mail/ssmtp
Source0:	ftp://ftp.debian.org/debian/pool/main/s/%{name}/%{name}_%{version}.orig.tar.bz2
Source1:	mailq.8
Source2:	newaliases.8
# http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=340803
# replaces RSA's md5 with a GPL compatible implementation
Patch1:		%{name}-md5auth-non-rsa.patch

#bug fixing patches
Patch2:		%{name}-garbage_writes.patch
Patch8:		%{name}-authpass.patch

#enhancements
#enhancement not present in Debian
Patch10:	%{name}-aliases.patch
# add X-Originating-IP field
#http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=557741
Patch11:	%{name}-remote-addr.patch
Patch12:	%{name}-validate-TLS-server-cert.patch

#fixes for Fedora PATHs
Patch21:	%{name}-defaultvalues.patch

Patch22:	ssmtp-configure-c99.patch
Patch23: ssmtp-c99.patch
Patch24:	ssmtp-c23.patch

#hack around wrong requires for mutt and mdadm
%if 0%{?rhel}
Provides:	MTA smtpdaemon
%endif
%if 0%{?fedora} < 8
Provides:	MTA smtpdaemon
%endif
Requires(post):	%{_sbindir}/alternatives
Requires(preun):	%{_sbindir}/alternatives
BuildRequires: make
BuildRequires:  gcc
BuildRequires:	openssl-devel

%if "%{_sbindir}" == "%{_bindir}"
# Compat symlinks for Requires in other packages.
# We rely on filesystem to create the symlinks for us.
Requires: filesystem(unmerged-sbin-symlinks)
Provides: /usr/sbin/sendmail
%endif


%description
A secure, effective and simple way of getting mail off a system to your mail
hub. It contains no suid-binaries or other dangerous things - no mail spool
to poke around in, and no daemons running in the background. Mail is simply
forwarded to the configured mailhost. Extremely easy configuration.

WARNING: the above is all it does; it does not receive mail, expand aliases
or manage a queue. That belongs on a mail hub with a system administrator.


%prep
%setup -q
%patch -P1 -p1 -b .gplmd5
%patch -P2 -p1 -b .garbage
%patch -P8 -p1 -b .authpass
%patch -P10 -p1 -b .aliases
%patch -P11 -p1 -b .remote-ip
%patch -P12 -p1 -b .tls

%patch -P21 -p1 -b .saneconf

%patch -P22 -p1 -b .configure-c99
%patch -P 23 -p1
%patch -P24 -p1 -b .c23

%build
%configure --enable-ssl --enable-md5auth --enable-inet6
make %{?_smp_mflags}

%install 
rm -rf %{buildroot}
install -p -D -m 2750 %{name} %{buildroot}%{_sbindir}/%{name}
#install -p -D -m 755 generate_config_alt %{buildroot}%{_bindir}/generate_config_alt
mkdir -p %{buildroot}%{_bindir}/
install -p -D -m 644 revaliases %{buildroot}%{_sysconfdir}/ssmtp/revaliases
install -p -m 640 ssmtp.conf %{buildroot}%{_sysconfdir}/ssmtp/ssmtp.conf
install -p -D -m 644 ssmtp.8 %{buildroot}%{_mandir}/man8/ssmtp.8
install -m 644 %{SOURCE1} %{buildroot}%{_mandir}/man8/mailq.ssmtp.8
install -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man8/newaliases.ssmtp.8
install -p -D -m 644 ssmtp.conf.5 %{buildroot}%{_mandir}/man5/ssmtp.conf.5
ln -s --relative %{_sbindir}/%{name} %{buildroot}%{_sbindir}/sendmail.ssmtp
ln -s --relative %{_sbindir}/%{name} %{buildroot}%{_bindir}/newaliases.ssmtp
ln -s --relative %{_sbindir}/%{name} %{buildroot}%{_bindir}/mailq.ssmtp
touch %{buildroot}%{_sbindir}/sendmail
touch %{buildroot}%{_bindir}/mailq
touch %{buildroot}%{_bindir}/newaliases
touch %{buildroot}%{_mandir}/man8/mailq.8.gz
touch %{buildroot}%{_mandir}/man8/newaliases.8.gz
touch %{buildroot}%{_mandir}/man8/sendmail.8.gz

%post
%{_sbindir}/alternatives  --install %{_sbindir}/sendmail mta %{_sbindir}/sendmail.ssmtp 30 \
	--slave %{_bindir}/mailq mta-mailq %{_bindir}/mailq.ssmtp \
	--slave %{_bindir}/newaliases mta-newaliases %{_bindir}/newaliases.ssmtp \
	--slave %{_mandir}/man1/mailq.1.gz mta-mailqman %{_mandir}/man8/mailq.ssmtp.8.gz \
	--slave %{_mandir}/man1/newaliases.1.gz mta-newaliasesman %{_mandir}/man8/newaliases.ssmtp.8.gz \
	--slave %{_mandir}/man8/sendmail.8.gz mta-sendmailman %{_mandir}/man8/ssmtp.8.gz 


%preun
#only remove in case of erase (but not at upgrade)
if [ $1 -eq 0 ] ; then
	%{_sbindir}/alternatives --remove mta %{_sbindir}/sendmail.ssmtp
fi
exit 0

%postun
if [ "$1" -ge "1" ]; then
	if [ "`readlink %{_sysconfdir}/alternatives/mta`" == "%{_sbindir}/sendmail.ssmtp" ]; then
		%{_sbindir}/alternatives --set mta %{_sbindir}/sendmail.ssmtp
	fi
fi

%files
%doc COPYING INSTALL README TLS CHANGELOG_OLD ChangeLog COPYRIGHT 
%{_mandir}/man5/*
%{_mandir}/man8/*
%attr(2755, root, mail) %{_sbindir}/%{name}

%ghost %{_sbindir}/sendmail
%ghost %{_bindir}/mailq
%ghost %{_bindir}/newaliases
%ghost %{_mandir}/man8/mailq.8.gz 
%ghost %{_mandir}/man8/newaliases.8.gz
%ghost %{_mandir}/man8/sendmail.8.gz

%{_sbindir}/sendmail.ssmtp
%{_bindir}/newaliases.ssmtp
%{_bindir}/mailq.ssmtp
%attr(2750, root, mail) %dir %{_sysconfdir}/ssmtp/
%config(noreplace) %{_sysconfdir}/ssmtp/revaliases
%attr(640, root, mail) %config(noreplace) %{_sysconfdir}/ssmtp/ssmtp.conf


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.64-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri May 23 2025 Dominik Mierzejewski <dominik@greysector.net> - 2.64-39
- C23 compatibility fix (resolves rhbz#2341386)

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.64-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.64-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri May 17 2024 Davide Cavalca <dcavalca@fedoraproject.org> - 2.64-36
- Add compat sbin Provides
- Convert license tag to SPDX

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.64-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 05 2024 Florian Weimer <fweimer@redhat.com> - 2.64-34
- C compatibility fixes

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.64-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.64-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec  2 2022 Florian Weimer <fweimer@redhat.com> - 2.64-31
- Port configure script to C99

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.64-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.64-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 2.64-28
- Rebuilt with OpenSSL 3.0.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.64-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.64-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.64-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.64-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.64-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.64-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.64-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.64-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.64-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.64-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.64-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.64-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.64-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Oct 13 2014 Manuel "lonely wolf" Wolfshant <wolfy@fedoraproject.org> - 2.64-14
- Fix spurious permissions for config file ( #1060515)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.64-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.64-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Jan 18 2014 Manuel "lonely wolf" Wolfshant <wolfy@fedoraproject.org> - 2.64-11
- uncomment TLS_CA in the config file

* Wed Sep 26 2013 Manuel "lonely wolf" Wolfshant <wolfy@fedoraproject.org> - 2.64-10
- Force loading of the CA bundle via the config file; should fix #1004998

* Wed Aug 20 2013 Manuel "lonely wolf" Wolfshant <wolfy@fedoraproject.org> - 2.64-9
- replace TLS patch with a corrected one. thanks Till Maas for the fix

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.64-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 5 2013 Manuel "lonely wolf" Wolfshant <wolfy@fedoraproject.org> - 2.64-7
- remove world readable permissions of the config file (#962988)
- revive the authpass patch (#970123)
- revive improved default config settings which were lost during rebase (#895708)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.64-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Oct 13 2012  Manuel "lonely wolf" Wolfshant <wolfy@fedoraproject.org> - 2.64-5
- Optional separation of TLS client key and certificate files
- Add patch enabling verification of TLS server (  #864894 )

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.64-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul 1 2012 Manuel "lonely wolf" Wolfshant <wolfy@fedoraproject.org> - 2.64-3
- Make the alternatives symlinks compatible with other MTAs
- Adjust the man page for newaliases

* Sun Jul 1 2012 Manuel "lonely wolf" Wolfshant <wolfy@fedoraproject.org> - 2.64-2
- Fix incorrect symlink in alternatives

* Sat Jun 30 2012 Manuel "lonely wolf" Wolfshant <wolfy@fedoraproject.org> - 2.64-1
- New upstream version ( long awaited in Fedora... )

* Sat Jun 30 2012 Manuel "lonely wolf" Wolfshant <wolfy@fedoraproject.org> - 2.61-18
- Apply patch to fix addition of garbage at end of attachments
- Close #830733

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.61-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.61-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 27 2010 Manuel "lonely wolf" Wolfshant <wolfy@fedoraproject.org> - 2.61-15
- fix regression created by the patch for standardise() -- Buffer overflow

* Tue Apr 20 2010 Manuel "lonely wolf" Wolfshant <wolfy@fedoraproject.org> 2.61-14
- use Fedora's default TLS cert path (close #553734)
- add Debian's patch for "send-mail: standardise() -- Buffer overflow"
  (close #582236)

* Mon Mar 08 2010 Manuel "lonely wolf" Wolfshant <wolfy@fedoraproject.org> 2.61-13
- Use %%ghost instead of explicit-provides according to Packaging Guidelines for
  Alternatives.
- close #570799

* Tue Feb 16 2010 Manuel "lonely wolf" Wolfshant <wolfy@fedoraproject.org> 2.61-12
- fix FTBFS due to ImplicitDSOLinking
- close #564967

* Wed Aug 26 2009 Tomas Mraz <tmraz@redhat.com> 2.61-11.10
- rebuild for new openssl

* Wed Feb 17 2009 Manuel "lonely wolf" Wolfshant <wolfy@nobugconsulting.ro> 2.61-11.9
- add Provides for mailq; this should make ssmtp dissapear from the "bad" list
  from https://fedoraproject.org/wiki/PackagingDrafts/UsingAlternatives

* Fri Jan 16 2009 Manuel "lonely wolf" Wolfshant <wolfy@nobugconsulting.ro> 2.61-11.8.1
- rebuild for newer openssl

* Fri Dec 26 2008 Manuel "lonely wolf" Wolfshant <wolfy@nobugconsulting.ro> 2.61-11.8
- integrate patch adding support for aliases; initial version received from Tako 
  Schotanus <tako@codejive.org>, who adapted it from "eatnumber1"
- README and the man page now reflect that aliases are expanded and used

* Wed Nov 26 2008 Manuel "lonely wolf" Wolfshant <wolfy@nobugconsulting.ro> 2.61-11.7
- integrate patch from Andreas Dilger, fixes https://bugzilla.redhat.com/show_bug.cgi?id=430608

* Fri Sep 12 2008 Manuel "lonely wolf" Wolfshant <wolfy@nobugconsulting.ro> 2.61-11.6.1
- use conditionals to consolidate specs for Fedora and EPEL

* Thu Sep 11 2008 Manuel "lonely wolf" Wolfshant <wolfy@nobugconsulting.ro> 2.61-11.6
- patch to fix CVE-2008-3962 (courtesy https://bugs.gentoo.org/127592)
- cleanup of other patches, make build with fuzz=0

* Sat Aug 02 2008 Manuel "lonely wolf" Wolfshant <wolfy@nobugconsulting.ro> 2.61-11.5.4
- work around rpmbuild more strict syntax checker

* Tue Feb 12 2008 Manuel "lonely wolf" Wolfshant <wolfy@nobugconsulting.ro> 2.61-11.5.3
- rebuilt for gcc 4.3.0

* Wed Dec 5 2007 lonely wolf <wolfy@nobugconsulting.ro> 2.61-11.5.2
- rebuilt for newer openssl
- fix usage of disttag for compatibility with mock + el3

* Wed Oct 24 2007 lonely wolf <wolfy@nobugconsulting.ro> 2.61-11.5.1
- adds back /usr/sbin/sendmail provides, rpmbuild by default does not add it

* Wed Oct 24 2007 lonely wolf <wolfy@nobugconsulting.ro> 2.61-11.5
- fixes https://bugzilla.redhat.com/show_bug.cgi?id=235594 by removing MTA
  and smtpdaemon provides, as the packages which required those were fixed

* Tue Oct 16 2007 lonely wolf <wolfy@nobugconsulting.ro> 2.61-11.4
- includes patch from http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=340803
  replacing md5 from RSA with a version released under GPLv2+
- fix URL for upstream

* Fri Aug 22 2007 lonely wolf <wolfy@nobugconsulting.ro> 2.61-11.3.1
- rebuilt

* Fri Aug 10 2007 lonely wolf <wolfy@nobugconsulting.ro> 2.61-11.3
- fix release tag, previous one did not match the changelog

* Fri Aug 3 2007 lonely wolf <wolfy@nobugconsulting.ro> 2.61-11.2
- license clarification

* Sun Dec 10 2006 lonely wolf <wolfy@nobugconsulting.ro> 2.61-11.1
- fix double %%changelog entry

* Fri Dec 08 2006 lonely wolf <wolfy@nobugconsulting.ro> 2.61-11
- fix security leak (http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=369542 )
- include more patches from debian (report an error in treating Bcc: addresses and if the SSL certificate does not match )

* Tue Nov 28 2006 lonely wolf <wolfy@nobugconsulting.ro> 2.61-10
- fix silly typo in changelog

* Tue Nov 28 2006 lonely wolf <wolfy@nobugconsulting.ro> 2.61-9
- included Ville Skyttä's patch for saner default values in ssmtp.conf (https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=217270)

* Mon Oct 10 2006 lonely wolf <wolfy@pcnet.ro> 2.61-8
- enabled IPv6 (just added this option to %%configure, the capability was already there)
- removed yet another man page from %%Provides
- cosmetic fixes - consistent use of macros
- added a missing Require
- I have also included a [commented] URL to the current patch (v9) provided by Debian. Because starting with version 8 the patch modifies the SSL libraries used. I will include this modification once I can perform more tests. 

* Mon Oct 10 2006 lonely wolf <wolfy@pcnet.ro> 2.61-7
- removed man pages and stubs from %%Provides

* Fri Sep 22 2006 lonely wolf <wolfy@pcnet.ro> 2.61-6
- cosmetic fixes

* Tue Apr 11 2006 lonely wolf <wolfy@pcnet.ro> 2.61-5
- cleaner hack for RHEL 3
- added back Provides: smtpdaemon
- correct typo in Provides
 
* Tue Apr 11 2006 lonely wolf <wolfy@pcnet.ro> 2.61-4
- hack for RHEL 3 which has krb5.h in a different place
 
* Mon Apr 10 2006 lonely wolf <wolfy@pcnet.ro> 2.61-3
- removed Requires: openssl
- removed Provides: smtpdaemon
- cleaning of %%files
- correct typos in version numbers in changelog
- disabled "alternatives --auto mta" in postrun macro, pending more tests

* Sat Apr 8 2006 lonely wolf <wolfy@pcnet.ro> 2.61-2
- fix spec file: consistent use of buildroot macro, no double "ssmtp" in files' name, switch back the name of the main patch to the one used by Debian
- removed the generate_config_alt script; it is ugly, buggy and completely replaces the default provided configuration file, including the comments (which are useful)
- add openssl to requires and openssl-devel to buildrequires
- fix pre/post install scriptlets (upgrade would have removed the files from the alternatives system)
- remove two unneeded files from the alternatives call; man sendmail will default to the page provided by ssmtp

* Thu Apr 6 2006 lonely wolf <wolfy@pcnet.ro> 2.61-1
- Initial rpm version, based on Debian sources & patch
- Includes patch from Mandrake to lower the default system UIDs from 1000 to 500
- Includes generate_config_alt, a small script to generate a customized ssmtp.conf (thus overriding the default one); beware that this script will completely replace the default ssmtp.conf.
- Customized to play nice in the alternatives environment
