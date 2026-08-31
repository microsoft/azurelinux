# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary:        User configurable send-only Mail Transfer Agent
Summary(de):    Benutzerkonfigurierbarer nur versendender Mail Transfer Agent (MTA)
Name:           esmtp
Version:        1.2
Release:        30%{?dist}
Source:         http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source1:        esmtp-0.4.1-mutt
# esmtp system config file configuring procmail as mda, for the local-delivery
# sub-package
Source2:        esmtprc-mda
Url:            http://esmtp.sourceforge.net/
# no license in files. Some come from fetchmail, another from libesmtp
# esmtp-wrapper is GPLv2+
# Automatically converted from old format: GPL+ and GPLv2+ - review is highly recommended.
License:        GPL-1.0-or-later AND GPL-2.0-or-later

Requires(post):  %{_sbindir}/alternatives
Requires(preun): %{_sbindir}/alternatives
BuildRequires:   libesmtp-devel, gcc
BuildRequires: make
# for esmtp-wrapper
Requires:       coreutils, liblockfile
Patch0:	esmtp-1.2-cron-fix.patch
Patch1: 0001-Deliver-mail-to-user-localhost-locally-using-a-MDA.patch
# esmtp doesn't listen on port 25, so it cannot provide server(smtp).
# This implies that any program requiring a program that sends mail
# on port 25 should rely on another package than esmtp to fulfill the
# dependency.
#Provides:       server(smtp)

%if "%{_sbindir}" == "%{_bindir}"
# Compat symlinks for Requires in other packages.
# We rely on filesystem to create the symlinks for us.
Requires: filesystem(unmerged-sbin-symlinks)
Provides: /usr/sbin/sendmail
%endif

%description
ESMTP is a user configurable relay-only Mail Transfer Agent (MTA) with a
sendmail-compatible syntax. It's based on libESMTP supporting the AUTH
(including the CRAM-MD5 and NTLM SASL mechanisms) and the StartTLS SMTP
extensions.

%description -l de
ESMTP ist ein benutzerkonfigurierbarer nur versendender Mail Transfer
Agent (MTA) mit einem Sendmail-kompatiblen Syntax. Es basiert auf
libESMTP und unterstützt AUTH (mit CRAM-MD5 und NTLM SASL) und StartTLS
SMTP.

%package local-delivery
Summary:        Configuration for esmtp allowing for local delivery
Requires:       %{name} = %{version}-%{release}
Requires:       procmail
Provides:       mail(local)

%description local-delivery
This packages contains the system ESMTP configuration file with local
delivery through an external mail delivery agent configured.

%prep
%setup -q
%patch -P0 -p1 -b .cron-fix
%patch -P1 -p1 -b .localhost
cp -p %{SOURCE1} mutt-esmtp
for file in esmtp.1 esmtprc.5; do
   iconv -f ISO8859-1 -t UTF8 < $file > $file.new && touch -r $file $file.new && mv -f $file.new $file
done

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL='install -p'
mkdir -p %{buildroot}%{_sysconfdir}
install -p -m0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/esmtprc
install -p -m0755 esmtp-wrapper %{buildroot}%{_bindir}

# setup dummy files for alternatives
rm -f %{buildroot}%{_bindir}/mailq
touch %{buildroot}%{_bindir}/mailq
rm -f %{buildroot}%{_libdir}/sendmail
mkdir -p %{buildroot}%{_prefix}/lib
touch %{buildroot}%{_prefix}/lib/sendmail
rm -f %{buildroot}%{_sbindir}/sendmail
touch %{buildroot}%{_sbindir}/sendmail
rm -f %{buildroot}%{_mandir}/man1/sendmail.1*
touch %{buildroot}%{_mandir}/man1/mailq.1.gz
mkdir -p %{buildroot}%{_mandir}/man8/
touch %{buildroot}%{_mandir}/man8/sendmail.8.gz

# remove newaliases because they are unusable
rm -f %{buildroot}%{_bindir}/newaliases %{buildroot}%{_mandir}/man1/newaliases.1*

%post
# newaliases is fake, so don't install the links.
%{_sbindir}/alternatives --install %{_sbindir}/sendmail mta %{_bindir}/esmtp-wrapper 30 \
  --slave %{_prefix}/lib/sendmail mta-sendmail %{_bindir}/esmtp-wrapper \
  --slave %{_mandir}/man8/sendmail.8.gz mta-sendmailman %{_mandir}/man1/esmtp.1.gz \
  --slave %{_bindir}/mailq mta-mailq %{_bindir}/esmtp-wrapper \
  --slave %{_mandir}/man1/mailq.1.gz mta-mailqman %{_mandir}/man1/esmtp.1.gz

%preun
if [ "$1" = 0 ]; then
   %{_sbindir}/alternatives --remove mta %{_bindir}/esmtp-wrapper
fi

%files
%doc AUTHORS COPYING NEWS README TODO sample.esmtprc mutt-esmtp
%{_bindir}/esmtp-wrapper
%ghost %{_sbindir}/sendmail
%ghost %{_bindir}/mailq
%ghost %{_prefix}/lib/sendmail
%{_bindir}/esmtp
%{_mandir}/man1/esmtp.1*
%{_mandir}/man5/esmtprc.5*
%ghost %{_mandir}/man8/sendmail.8.gz
%ghost %{_mandir}/man1/mailq.1.gz

%files local-delivery
%config(noreplace) %{_sysconfdir}/esmtprc

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Jan 12 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.2-28
- Rebuilt for the bin-sbin merge (2nd attempt)

* Wed Aug 07 2024 Miroslav Suchý <msuchy@redhat.com> - 1.2-27
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 09 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.2-25
- Rebuilt for the bin-sbin merge

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 19 2018 Ondřej Lysoněk <olysonek@redhat.com> - 1.2-11
- Add gcc to BuildRequires

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Oct 27 2017 Ondřej Lysoněk <olysonek@redhat.com> - 1.2-9
- Deliver mail to user@hostname locally only if hostname is 'localhost'
- Do not try to check if the hostname resolves to 127.0.0.1. That would be
- complicated and maybe not even the right thing to do.
- Resolves: rhbz#1491721

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Ondřej Lysoněk <olysonek@redhat.com> - 1.2-5
- Deliver mails to something@localhost locally
  Resolves: rhbz#1404768

* Wed Aug 03 2016 Ondřej Lysoněk <olysonek@redhat.com> - 1.2-4
- Fixed patch esmtp-1.2-cron-fix.patch from the last release
  This resolves some SELinux denials
  Resolves: rhbz#1303305

* Mon Jul 18 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 1.2-3
- Fixed some errors when running from the cron
  Resolves: rhbz#1303305

* Mon Feb 15 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 1.2-2
- Added explicit liblockfile requirement (required by esmtp-wrapper)

* Mon Feb 15 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 1.2-1
- New version
  Resolves: rhbz#1051667
- Removed spurious whitespaces
- Fixed bogus dates in changelog (best effort)
- Removed some obsoleted artifacts (like clean section)
- Ghosted files for alternatives and removed explicit provides
  Resolves: rhbz#570797

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.0-6
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 16 2009 Tomas Mraz <tmraz@redhat.com> 1.0-3
- rebuild with new openssl

* Mon Nov 24 2008 Patrice Dumas <pertusus@free.fr> 1.0-2
- update to 1.0
- add a subpackage with local delivery enabled and dependency on procmail

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.6.0-4
- Autorebuild for GCC 4.3

* Tue Dec 18 2007 Patrice Dumas <pertusus@free.fr> 0.6.0-3
- keep more timestamps
- add a Requires(preun) for alternatives

* Thu Dec 06 2007 Release Engineering <rel-eng at fedoraproject dot org> - 0.6.0-2
 - Rebuild for deps

* Wed Oct 10 2007 Patrice Dumas <pertusus@free.fr> 0.6.0-1
- update to 0.6.0

* Mon Sep 11 2006 Patrice Dumas <pertusus@free.fr> 0.5.1-13
- rebuild for FC6

* Thu Jun 22 2006 Patrice Dumas <pertusus@free.fr> 0.5.1-12
- provide an alternative for /usr/lib/sendmail even if %%_lib isn't lib
  fix 196277

* Thu Feb 16 2006 Patrice Dumas <pertusus@free.fr> 0.5.1-11
- rebuild for fc5

* Sun Jan  8 2006 Patrice Dumas <pertusus@free.fr> 0.5.1-10
- convert man pages to utf8 (Dmitry Butskoy report)

* Wed Nov 16 2005 Patrice Dumas <pertusus@free.fr> 0.5.1-9
- remove the workaround for libesmtp not requiring openssl (#166844 closed)

* Sun Nov 13 2005 Patrice Dumas <pertusus@free.fr> 0.5.1-8
- rebuild against new openssl

* Mon Aug 29 2005 Patrice Dumas <pertusus@free.fr> 0.5.1-7
- uncomment german translation

* Fri Aug 26 2005 Patrice Dumas <pertusus@free.fr> 0.5.1-6
- add temporarily a BuildRequires: openssl-devel to workaround missing
  Requires: of libesmtp-devel (#166844)

* Fri Aug 26 2005 Patrice Dumas <pertusus@free.fr> 0.5.1-5
- comment out german translation
- cleanups (thanks Aurelien Bompard)

* Fri Mar 12 2004 Patrice Dumas <pertusus@free.fr> 0.5.1-2
- Use alternatives

* Fri Mar 12 2004 Patrice Dumas <pertusus@free.fr> 0.5.1-1
- Use fedora-newrpmspec to update the spec file
- Package sendmail replacements

* Sat Nov 15 2003 Robert Scheck <esmtp@robert-scheck.de> 0.5.0-1
- Update to 0.5.0
- Added german description and summary

* Mon Oct 27 2003 Robert Scheck <esmtp@robert-scheck.de> 0.4.1-1
- Update to 0.4.1
- Initial Release for Red Hat Linux
