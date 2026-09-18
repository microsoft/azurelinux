# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global _generatorsdir %{_prefix}/lib/systemd/system-generators

Name:    vsftpd
Version: 3.0.5
Release: 14%{?dist}
Summary: Very Secure Ftp Daemon

# OpenSSL link exception
License:  GPL-2.0-only WITH vsftpd-openssl-exception
URL:      https://security.appspot.com/vsftpd.html
Source0:  https://security.appspot.com/downloads/%{name}-%{version}.tar.gz
Source1:  vsftpd.xinetd
Source2:  vsftpd.pam
Source3:  vsftpd.ftpusers
Source4:  vsftpd.user_list
Source6:  vsftpd_conf_migrate.sh
Source7:  vsftpd.service
Source8:  vsftpd@.service
Source9:  vsftpd.target
Source10: vsftpd-generator
Source11: vsftpd-tmpfiles.conf

BuildRequires: make
BuildRequires: pam-devel
BuildRequires: libcap-devel
BuildRequires: openssl-devel
BuildRequires: systemd
BuildRequires: git
BuildRequires: gcc

Requires: logrotate

Patch1:  0001-Don-t-use-the-provided-script-to-locate-libraries.patch
Patch2:  0002-Enable-build-with-SSL.patch
Patch3:  0003-Enable-build-with-TCP-Wrapper.patch
Patch4:  0004-Use-etc-vsftpd-dir-for-config-files-instead-of-etc.patch
Patch5:  0005-Use-hostname-when-calling-PAM-authentication-module.patch
Patch6:  0006-Close-stdin-out-err-before-listening-for-incoming-co.patch
Patch7:  0007-Make-filename-filters-smarter.patch
Patch8:  0008-Write-denied-logins-into-the-log.patch
Patch9:  0009-Trim-whitespaces-when-reading-configuration.patch
Patch10: 0010-Improve-daemonizing.patch
Patch11: 0011-Fix-listing-with-more-than-one-star.patch
Patch12: 0012-Replace-syscall-__NR_clone-.-with-clone.patch
Patch13: 0013-Extend-man-pages-with-systemd-info.patch
Patch14: 0014-Add-support-for-square-brackets-in-ls.patch
Patch15: 0015-Listen-on-IPv6-by-default.patch
Patch16: 0016-Increase-VSFTP_AS_LIMIT-from-200UL-to-400UL.patch
Patch17: 0017-Fix-an-issue-with-timestamps-during-DST.patch
Patch18: 0018-Change-the-default-log-file-in-configuration.patch
Patch19: 0019-Introduce-reverse_lookup_enable-option.patch
Patch20: 0020-Use-unsigned-int-for-uid-and-gid-representation.patch
Patch21: 0021-Introduce-support-for-DHE-based-cipher-suites.patch
Patch22: 0022-Introduce-support-for-EDDHE-based-cipher-suites.patch
Patch23: 0023-Add-documentation-for-isolate_-options.-Correct-defa.patch
Patch24: 0024-Introduce-new-return-value-450.patch
Patch25: 0025-Improve-local_max_rate-option.patch
Patch26: 0026-Prevent-hanging-in-SIGCHLD-handler.patch
Patch27: 0027-Delete-files-when-upload-fails.patch
Patch28: 0028-Fix-man-page-rendering.patch
Patch29: 0029-Fix-segfault-in-config-file-parser.patch
Patch30: 0030-Fix-logging-into-syslog-when-enabled-in-config.patch
Patch31: 0031-Fix-question-mark-wildcard-withing-a-file-name.patch
Patch32: 0032-Propagate-errors-from-nfs-with-quota-to-client.patch
Patch34: 0034-Turn-off-seccomp-sandbox-because-it-is-too-strict.patch
Patch36: 0036-Redefine-VSFTP_COMMAND_FD-to-1.patch
Patch37: 0037-Document-the-relationship-of-text_userdb_names-and-c.patch
Patch38: 0038-Document-allow_writeable_chroot-in-the-man-page.patch
Patch39: 0039-Improve-documentation-of-ASCII-mode-in-the-man-page.patch
Patch40: 0040-Use-system-wide-crypto-policy.patch
Patch41: 0041-Document-the-new-default-for-ssl_ciphers-in-the-man-.patch
Patch42: 0042-When-handling-FEAT-command-check-ssl_tlsv1_1-and-ssl.patch
Patch44: 0044-Disable-anonymous_enable-in-default-config-file.patch
Patch45: 0045-Expand-explanation-of-ascii_-options-behaviour-in-ma.patch
Patch46: 0046-vsftpd.conf-Refer-to-the-man-page-regarding-the-asci.patch
Patch47: 0047-Disable-tcp_wrappers-support.patch
Patch48: 0048-Fix-default-value-of-strict_ssl_read_eof-in-man-page.patch
Patch49: 0049-Add-new-filename-generation-algorithm-for-STOU-comma.patch
Patch50: 0050-Don-t-link-with-libnsl.patch
Patch51: 0051-Improve-documentation-of-better_stou-in-the-man-page.patch
Patch52: 0052-Fix-rDNS-with-IPv6.patch
Patch53: 0053-Always-do-chdir-after-chroot.patch
Patch54: 0054-vsf_sysutil_rcvtimeo-Check-return-value-of-setsockop.patch
Patch55: 0055-vsf_sysutil_get_tz-Check-the-return-value-of-syscall.patch
Patch56: 0056-Log-die-calls-to-syslog.patch
Patch57: 0057-Improve-error-message-when-max-number-of-bind-attemp.patch
Patch58: 0058-Make-the-max-number-of-bind-retries-tunable.patch
Patch59: 0059-Fix-SEGFAULT-when-running-in-a-container-as-PID-1.patch
Patch61: 0001-Move-closing-standard-FDs-after-listen.patch
Patch62: 0002-Prevent-recursion-in-bug.patch
Patch63: 0001-Set-s_uwtmp_inserted-only-after-record-insertion-rem.patch
Patch64: 0002-Repeat-pututxline-if-it-fails-with-EINTR.patch
Patch65: 0001-Repeat-pututxline-until-it-succeeds-if-it-fails-with.patch
Patch67: 0001-Fix-timestamp-handling-in-MDTM.patch
Patch68: 0002-Drop-an-unused-global-variable.patch
Patch69: 0001-Remove-a-hint-about-the-ftp_home_dir-SELinux-boolean.patch
Patch70: fix-str_open.patch
Patch71: vsftpd-3.0.5-enable_wc_logs-replace_unprintable_with_hex.patch
Patch72: vsftpd-3.0.5-replace-old-network-addr-functions.patch
Patch73: vsftpd-3.0.5-replace-deprecated-openssl-functions.patch
Patch74: vsftpd-3.0.5-add-option-for-tlsv1.3-ciphersuites.patch
Patch75: vsftpd-3.0.5-use-old-tlsv-options.patch
Patch76: 0076-Correct-the-definition-of-setup_bio_callbacks-in-ssl.patch

%description
vsftpd is a Very Secure FTP daemon. It was written completely from
scratch.

%prep
%autosetup -S git
cp %{SOURCE1} .

%build

%ifarch s390x sparcv9 sparc64
%make_build CFLAGS="$RPM_OPT_FLAGS -fPIE -pipe -Wextra -Werror" \
%else
%make_build CFLAGS="$RPM_OPT_FLAGS -fpie -pipe -Wextra -Werror" \
%endif
        LINK="-pie -lssl $RPM_LD_FLAGS" %{?_smp_mflags}

%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/{vsftpd,pam.d,logrotate.d}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man{5,8}
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
mkdir -p $RPM_BUILD_ROOT%{_generatorsdir}
install -m 755 vsftpd  $RPM_BUILD_ROOT%{_bindir}/vsftpd
install -m 600 vsftpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/vsftpd/vsftpd.conf
install -m 644 vsftpd.conf.5 $RPM_BUILD_ROOT/%{_mandir}/man5/
install -m 644 vsftpd.8 $RPM_BUILD_ROOT/%{_mandir}/man8/
install -m 644 RedHat/vsftpd.log $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/vsftpd
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/vsftpd
install -m 600 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/vsftpd/ftpusers
install -m 600 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/vsftpd/user_list
install -m 744 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/vsftpd/vsftpd_conf_migrate.sh
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_unitdir}
install -m 644 %{SOURCE8} $RPM_BUILD_ROOT%{_unitdir}
install -m 644 %{SOURCE9} $RPM_BUILD_ROOT%{_unitdir}
install -m 755 %{SOURCE10} $RPM_BUILD_ROOT%{_generatorsdir}
install -Dpm 644 %{SOURCE11} $RPM_BUILD_ROOT%{_tmpfilesdir}/vsftpd.conf
                            
mkdir -p $RPM_BUILD_ROOT/%{_var}/ftp/pub

%post
%systemd_post vsftpd.service

%preun
%systemd_preun vsftpd.service
%systemd_preun vsftpd.target

%postun
%systemd_postun_with_restart vsftpd.service 

%files
%{_unitdir}/*
%{_generatorsdir}/*
%{_bindir}/vsftpd
%dir %{_sysconfdir}/vsftpd
%{_sysconfdir}/vsftpd/vsftpd_conf_migrate.sh
%config(noreplace) %{_sysconfdir}/vsftpd/ftpusers
%config(noreplace) %{_sysconfdir}/vsftpd/user_list
%config(noreplace) %{_sysconfdir}/vsftpd/vsftpd.conf
%config(noreplace) %{_sysconfdir}/pam.d/vsftpd
%config(noreplace) %{_sysconfdir}/logrotate.d/vsftpd
%doc FAQ INSTALL BUGS AUDIT Changelog LICENSE README README.security REWARD
%doc SPEED TODO BENCHMARKS COPYING SECURITY/ EXAMPLE/ TUNING SIZE vsftpd.xinetd
%{_mandir}/man5/vsftpd.conf.*
%{_mandir}/man8/vsftpd.*
%{_var}/ftp
%{_tmpfilesdir}/vsftpd.conf

%changelog
* Wed Jan 14 2026 Tomas Korbar <tkorbar@redhat.com> - 3.0.5-14
- Resolve CVE-2025-14242

* Thu Dec 18 2025 Fedor Vorobev <fvorobev@redhat.com> - 3.0.5-13
- Add a tmpfiles.d config. (image mode support)

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Apr 15 2025 Tomas Korbar <tkorbar@redhat.com> - 3.0.5-11
- Move executable to bindir

* Fri Jan 24 2025 Stepan Broz <sbroz@redhat.com> - 3.0.5-10
- Correct the definition of setup_bio_callbacks() in ssl.c

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Aug 19 2024 Tomas Korbar <tkorbar@redhat.com> - 3.0.5-8
- Fix FEAT command to list AUTH TLS when TLSv1.3 is enabled

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu May 04 2023 Richard Lescak <rlescak@redhat.com> - 3.0.5-4
- add option for TLSv1.3 ciphersuites
- SPDX migration

* Fri Feb 17 2023 Richard Lescak <rlescak@redhat.com> - 3.0.5-3
- make vsftpd compatible with Openssl 3.0+
- replace old network functions

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 28 2022 Richard Lescak <rlescak@redhat.com> 3.0.5-1
- rebase to version 3.0.5

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-51
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-50
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Oct 27 2021 Artem Egorenkov <aegorenk@redhat.com> - 3.0.3-49
- add option to disable TLSv1.3
- Resolves: rhbz#2017705

* Wed Oct 13 2021 Artem Egorenkov <aegorenk@redhat.com> - 3.0.3-48
- ALPACA fix backported from upstram 3.0.5 version
- Resolves: rhbz#1975648

* Wed Oct 13 2021 Artem Egorenkov <aegorenk@redhat.com> - 3.0.3-47
- Temporary pass -Wno-deprecated-declarations to gcc to ignore
  deprecated warnings to be able to build against OpenSSL-3.0
- Resolves: rhbz#1962603

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 3.0.3-46
- Rebuilt with OpenSSL 3.0.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Apr 8 2021 Artem Egorenkov <aegorenk@redhat.com> - 3.0.3-44
- Enable support for wide-character strings in logs
- Replace unprintables with HEX code, not question marks

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.0.3-43
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Nov 27 2020 Timm Bäder<tbaeder@redhat.com> - 3.0.3-41
- Fix str_open() so it doesn't warn when compiled with clang
- Pass $RPM_LD_FLAGS when linking

* Mon Nov 02 2020 Artem Egorenkov <aegorenk@redhat.com> - 3.0.3-40
- Unit files fixed "After=network-online.target"

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Mar 17 2020 Ondřej Lysoněk <olysonek@redhat.com> - 3.0.3-38
- Removed a hint about the ftp_home_dir SELinux boolean from the config file
- Resolves: rhbz#1623424

* Thu Feb 13 2020 Ondřej Lysoněk <olysonek@redhat.com> - 3.0.3-37
- Fix timestamp handling in MDTM
- Resolves: rhbz#1567855

* Fri Feb 07 2020 Ondřej Lysoněk <olysonek@redhat.com> - 3.0.3-36
- Fix build with gcc 10
- Resolves: rhbz#1800239

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Tom Stellard <tstellar@redhat.com> - 3.0.3-34
- Use make_build macro

* Thu Nov 28 2019 Ondřej Lysoněk <olysonek@redhat.com> - 3.0.3-33
- Finish up the fix to the problem with bad utmp entries when pututxline() fails
- Resolves: rhbz#1688852
- Resolves: rhbz#1737433

* Mon Aug 05 2019 Ondřej Lysoněk <olysonek@redhat.com> - 3.0.3-32
- Partially fix problem with bad utmp entries when pututxline() fails
- Resolves: rhbz#1688848

* Sat Aug 03 2019 Ondřej Lysoněk <olysonek@redhat.com> - 3.0.3-31
- Fix segfault when listen() returns an error
- Resolves: rhbz#1666380

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jul 25 2018 Ondřej Lysoněk <olysonek@redhat.com> - 3.0.3-28
- Rebuilt, switched to SHA512 source tarball hash

* Wed Jul 25 2018 Ondřej Lysoněk <olysonek@redhat.com> - 3.0.3-27
- Fix a segfault when running as PID 1

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Ondřej Lysoněk <olysonek@redhat.com> - 3.0.3-25
- Add config option log_die allowing to pass error messages to syslog
- Add config option bind_retries allowing to change the max number
- of attempts to find a listening port for the PASV/EPSV command
- Resolves: rhbz#1318198

* Fri Jun 01 2018 Ondřej Lysoněk <olysonek@redhat.com> - 3.0.3-24
- Fix filename expansion in vsftpd_conf_migrate.sh ... again

* Thu May 10 2018 Ondřej Lysoněk <olysonek@redhat.com> - 3.0.3-23
- Fix issues found by Coverity Scan

* Fri Apr 27 2018 Ondřej Lysoněk <olysonek@redhat.com> - 3.0.3-22
- Fix filename expansion in vsftpd_conf_migrate.sh

* Thu Apr 05 2018 Ondřej Lysoněk <olysonek@redhat.com> - 3.0.3-21
- Improve documentation of better_stou in the man page

* Mon Feb 19 2018 Ondřej Lysoněk <olysonek@redhat.com> - 3.0.3-20
- Add gcc to BuildRequires

* Tue Feb 06 2018 Ondřej Lysoněk <olysonek@redhat.com> - 3.0.3-19
- Don't link with libnsl

* Tue Feb 06 2018 Ondřej Lysoněk <olysonek@redhat.com> - 3.0.3-18
- Add a new config option 'better_stou', which can be used to enable
  a better algorithm for generating unique filenames for the STOU command.
- Resolves: rhbz#1479237

* Wed Jan 10 2018 Ondřej Lysoněk <olysonek@redhat.com> - 3.0.3-17
- Add BuildRequires: libnsl2-devel
- https://fedoraproject.org/wiki/Changes/NISIPv6

* Fri Jan 05 2018 Ondřej Lysoněk <olysonek@redhat.com> - 3.0.3-16
- Disable tcp_wrappers support
- Resolves: rhbz#1518796
- Fix default value of strict_ssl_read_eof in man page

* Tue Jan 02 2018 Ondřej Lysoněk <olysonek@redhat.com> - 3.0.3-15
- Expand the explanation of the ascii_* options behaviour

* Tue Jan 02 2018 Ondřej Lysoněk <olysonek@redhat.com> - 3.0.3-14
- Disable anonymous_enable in default config file
- Resolves: rhbz#1338637

* Thu Dec 21 2017 Ondřej Lysoněk <olysonek@redhat.com> - 3.0.3-13
- Document the new default for ssl_ciphers in the man page
- Related: rhbz#1483970
- When handling FEAT command, check ssl_tlsv1_1 and ssl_tlsv1_2
- Patch was written by Martin Sehnoutka
- Resolves: rhbz#1432054
- Disable TLSv1 and TLSv1.1 - enable only TLSv1.2 by default

* Thu Dec 21 2017 Ondřej Lysoněk <olysonek@redhat.com> - 3.0.3-12
- Use system wide crypto policy
- Resolves: rhbz#1483970

* Fri Nov 24 2017 Ondřej Lysoněk <olysonek@redhat.com> - 3.0.3-11
- Improve documentation of ASCII mode in the man page
- Resolves: rhbz#1139409

* Tue Oct 31 2017 Ondřej Lysoněk <olysonek@redhat.com> - 3.0.3-10
- Document allow_writeable_chroot in the man page
- Resolves: rhbz#1507143

* Thu Oct 26 2017 Ondřej Lysoněk <olysonek@redhat.com> - 3.0.3-9
- Document the relationship of text_userdb_names and chroot_local_user
- Resolves: rhbz#1439724

* Tue Sep 05 2017 Ondřej Lysoněk <olysonek@redhat.com> - 3.0.3-8
- Build against OpenSSL 1.1
- Redefine VSFTP_COMMAND_FD to 1 to get errors generated during
- startup picked up by systemd
- Resolves: rhbz#1443055

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 01 2016 Martin Sehnoutka <msehnout@redhat.com> - 3.0.3-4
- Use OpenSSL compat library on rawhide

* Thu Nov 17 2016 Martin Sehnoutka <msehnout@redhat.com> - 3.0.3-3
- Review patches
- Add TLSv1.{1,2} options
- Fix question mark wildcard within a file name
- Seccomp patch removed

* Fri Apr 08 2016 Martin Sehnoutka <msehnout@redhat.com> - 3.0.3-2
- Applied patches:
- Readd seccomp disabled by default
- vsftpd local_max_rate option doesn't work as expected
- The vsftpd hangs in a SIGCHLD handler when the pam_exec.so is used in pam.d 
- configuration
- The vsftpd doesn't remove failed upload when the delete_failed_uploads is 
- enabled and the network cable is unplagged
- man pages bug
- vsftpd segfaults in vsf_sysutil_strndup
- Fix logging when syslog is used

* Thu Mar 17 2016 Martin Sehnoutka <msehnout@redhat.com> - 3.0.3-1
- Update to 3.0.3 version

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Sep 16 2014 Jiri Skala <jskala@redhat.com> - 3.0.2-13
- added appropriate values to ssl_ciphers (dh and ecdh patches)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 04 2014 Jiri Skala <jskala@redhat.com> - 3.0.2-11
- fixed deny_file, hide_file options - updated sqb patch

* Wed Jun 18 2014 Jiri Skala <jskala@redhat.com> - 3.0.2-10
- improves DH cipher
- implements ECDH cipher
- adds isolate* options to man vsftpd.conf
- corrects max_clients, max_per_ip default values in man vsftd.conf
- adds return code 450 when a file is temporarily unavailable

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Jiri Skala <jskala@redhat.com> - 3.0.2-8
- adds reverse lookup option to vsftpd.conf
- changes types of uid and gid to uint
- removes spare patch pasv-addr
- implements DH cipher
- gets rid init scirpt subpackage

* Tue Sep 10 2013 Jiri Skala <jskala@redhat.com> - 3.0.2-7
- fixed #1005549 - vsftpd startup broken

* Wed Sep 04 2013 Jiri Skala <jskala@redhat.com> - 3.0.2-6
- fixes usage pasv_address option in combination with external IP
- updated man pages - multile instances using vsftpd.target

* Thu Aug 15 2013 Jiri Skala <jskala@redhat.com> - 3.0.2-5
- replaced systemd path by _unitdir macro
- fixes #7194344 - multiple instances (target, generator)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 25 2013 Jiri Skala <jskala@redhat.com> - 3.0.2-3
- fixes #913519 - login fails (increased AS_LIMIT)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Sep 19 2012 Jiri Skala <jskala@redhat.com> - 3.0.2-2
- update to latest upstream 3.0.2

* Mon Sep 17 2012 Jiri Skala <jskala@redhat.com> - 3.0.1-1
- update to latest upstream 3.0.1
- fixes #851441 - Introduce new systemd-rpm macros in vsftpd spec file
- fixes #845980 - vsftpd seccomp filter is too strict

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Jiri Skala <jskala@redhat.com> - 3.0.0-3
- changed default value of xferlog_file to /var/log/xferlog
- added rotating xferlog

* Thu Apr 26 2012 Jiri Skala <jskala@redhat.com> - 3.0.0-2
- corrected time zone handling - especially DST flag
- fixed default value of option 'listen'

* Tue Apr 10 2012 Jiri Skala <jskala@redhat.com> - 3.0.0-1
- updated to latest upstream 3.0.0

* Thu Feb 09 2012 Jiri Skala <jskala@redhat.com> - 2.3.5-3
- fixes #788812 - authentication failure on x86_64 when using nss_pgsql

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 19 2011 Jiri Skala <jskala@redhat.com> - 2.3.5-1
- updated to latest upstream 2.3.5

* Mon Nov 28 2011 Jiri Skala <jskala@redhat.com> - 2.3.4-7
- added patch from BZ#450853#c23

* Tue Nov 15 2011 Jiri Skala <jskala@redhat.com> - 2.3.4-6
- fixes #753365 - multiple issues with vsftpd's systemd unit
- removes exclusivity between listen and listen_ipv6 BZ#450853
- ls wildchars supports square brackets

* Wed Aug 03 2011 Jiri Skala <jskala@redhat.com> - 2.3.4-5
- fixes #719434 - Provide native systemd unit file
- moving SysV initscript into subpackage

* Mon Aug 01 2011 Jiri Skala <jskala@redhat.com> - 2.3.4-4
- rebuild for libcap

* Mon Jul 04 2011 Nils Philippsen <nils@redhat.com> - 2.3.4-3
- update upstream and source URL

* Wed Feb 16 2011 Jiri Skala <jskala@redhat.com> - 2.3.4-2
- fixes #717412 - Connection failures - patched by Takayuki Nagata

* Wed Feb 16 2011 Jiri Skala <jskala@redhat.com> - 2.3.4-1
- updated to latest upstream 2.3.4

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 20 2010 Jiri Skala <jskala@redhat.com> - 2.3.2-1
- fixes #625404 - vsftpd-2.3.1 is available
- joined patches (libs+dso, wildchar+greedy)

* Fri Aug 06 2010 Jiri Skala <jskala@redhat.com> - 2.2.2-8
- fixes #472880 - Configuration can cause confusion because of selinux labels

* Mon May 17 2010 Jiri Skala <jskala@redhat.com> - 2.2.2-7
- when listen_ipv6=YES sets socket option to listen IPv6 only

* Fri May 14 2010 Jiri Skala <jskala@redhat.com> - 2.2.2-6
- syscall(__NR_clone) replaced by clone() to fix incorrect order of params on s390 arch

* Wed Apr 07 2010 Jiri Skala <jskala@redhat.com> - 2.2.2-5
- corrected daemonize_plus patch - don't try kill parent when vsftpd isn't daemonized

* Tue Mar 16 2010 Jiri Skala <jskala@redhat.com> - 2.2.2-4
- fixes #544251 - /etc/rc.d/init.d/vsftpd does not start more than one daemon

* Mon Feb 15 2010 Jiri Skala <jskala@redhat.com> - 2.2.2-3
- fixes #565067 - FTBFS: ImplicitDSOLinking

* Thu Dec 17 2009 Jiri Skala <jskala@redhat.com> - 2.2.2-2
- corrected two patches due to fuzz 0

* Thu Dec 17 2009 Jiri Skala <jskala@redhat.com> - 2.2.2-1
- update to latest upstream

* Mon Nov 23 2009 Jiri Skala <jskala@rehat.com> - 2.2.0-6
- added lost default values of vsftpd.conf (rh patch)

* Wed Sep 16 2009 Tomas Mraz <tmraz@redhat.com> - 2.2.0-5
- use password-auth common PAM configuration instead of system-auth

* Mon Sep 14 2009 Jiri Skala <jskala@rehat.com> - 2.2.0-4
- modified init script to be LSB compliant

* Tue Sep 08 2009 Jiri Skala <jskala@rehat.com> - 2.2.0-3
- fixed bug messaged in RHEL-4 #479774 - Wildcard failures with vsftpd

* Thu Aug 27 2009 Tomas Mraz <tmraz@redhat.com> - 2.2.0-2
- rebuilt with new openssl

* Mon Aug 24 2009 Martin Nagy <mnagy@redhat.com> - 2.2.0-1
- update to latest upstream release 2.2.0

* Tue Aug 04 2009 Martin Nagy <mnagy@redhat.com> - 2.2.0-0.1.pre4
- update to latest upstream release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 02 2009 Jiri Skala <jskala@redhat.com> - 2.1.2-1
- updated to latest upstream version

* Thu May 21 2009 Jiri Skala <jskala@redhat.com> - 2.1.1-0.3
- fixed daemonize_plus patch
- fixed test in initscript [ -z "CONFS" ]

* Mon May 04 2009 Jiri Skala <jskala@redhat.com> - 2.1.1-0.2
- fixes daemonize patch

* Wed Apr 22 2009 Jiri Skala <jskala@redhat.com> - 2.1.0-3
- updated to latest upstream version
- improved daemonizing - init script gets correct return code if binding fails
- trim white spaces from option values
- fixed #483604 - vsftpd not honouring delay_failed_login when userlist active

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 24 2009 Martin Nagy <mnagy@redhat.com> - 2.1.0-1
- update to latest upstream release

* Fri Jan 23 2009 Martin Nagy <mnagy@redhat.com> - 2.1.0-0.3.pre4
- update to latest upstream release
- enable ptrace sandbox again
- don't mark vsftpd_conf_migrate.sh as a config file

* Fri Jan 16 2009 Martin Nagy <mnagy@redhat.com> - 2.1.0-0.2.pre3
- disable ptrace sandbox to fix build on i386

* Fri Jan 16 2009 Martin Nagy <mnagy@redhat.com> - 2.1.0-0.1.pre3
- update to latest upstream release
- cleanup the spec file
- drop patches fixed upstream:
    vsftpd-1.0.1-missingok.patch
    vsftpd-1.2.1-nonrootconf.patch
    vsftpd-2.0.1-tcp_wrappers.patch
    vsftpd-2.0.2-signal.patch
    vsftpd-2.0.3-daemonize_fds.patch
    vsftpd-2.0.5-correct_comments.patch
    vsftpd-2.0.5-pasv_dot.patch
    vsftpd-2.0.5-write_race.patch
    vsftpd-2.0.5-fix_unique.patch
    vsftpd-2.0.5-uname_size.patch
    vsftpd-2.0.5-bind_denied.patch
    vsftpd-2.0.5-pam_end.patch
    vsftpd-2.0.5-underscore_uname.patch
    vsftpd-2.0.6-listen.patch
- join all configuration patches into one:
    vsftpd-1.1.3-rh.patch
    vsftpd-1.2.1-conffile.patch
    vsftpd-2.0.1-dir.patch
    vsftpd-2.0.1-server_args.patch
    vsftpd-2.0.3-background.patch
    vsftpd-2.0.5-default_ipv6.patch
    vsftpd-2.0.5-add_ipv6_option.patch
    vsftpd-2.0.5-man.patch

* Mon Sep  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.0.7-1
- fix license tag
- update to 2.0.7

* Fri Jun 20 2008 Dennis Gilmore <dennis@ausil.us> - 2.0.6-5
- add sparc arches to -fPIE list

* Wed May 21 2008 Martin Nagy <mnagy@redhat.com> - 2.0.6-4
- fix a small memory leak (#397011)

* Mon Mar 31 2008 Martin Nagy <mnagy@redhat.com> - 2.0.6-3
- set option listen to default to YES

* Mon Feb 25 2008 Martin Nagy <mnagy@redhat.com> - 2.0.6-2
- fix init script (#431452)
- make the init script LSB compliant (#247093)

* Fri Feb 22 2008 Martin Nagy <mnagy@redhat.com> - 2.0.6-1
- rebase for new upstream version
- remove patches that were fixed in upstream: kickline, confspell, anon_umask

* Mon Feb 11 2008 Martin Nagy <mnagy@redhat.com> - 2.0.5-22
- rebuild for gcc-4.3

* Fri Nov 30 2007 Martin Nagy <mnagy@redhat.com> - 2.0.5-21
- Remove uniq_rename patch.
- Correct create/lock race condition, original patch by <mpoole@redhat.com>
  (#240550).
- Fix bad handling of unique files (#392231).
- Added userlist_log option.
- Allow usernames to begin with underscore or dot (#339911).
- Removed user_config patch.
- Fix nonrootconf patch (#400921).
- Increase maximum length of allowed username (#236326).
- Fix file listing issue with wildcard (#392181).
- Removed use_localtime patch (#243087).

* Thu Nov 08 2007 Martin Nagy <mnagy@redhat.com> - 2.0.5-20
- Correct calling of pam_end (#235843).

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.0.5-19
- Rebuild for selinux ppc32 issue.

* Tue Jul 10 2007 Maros Barabas <mbarabas@redhat.com> - 2.0.5-18
- Add comment for xferlog_std_format
- Resolves #218260

* Fri Jun 29 2007 Maros Barabas <mbarabas@redhat.com> - 2.0.5-17
- Fix pasv dot after pasv response (RFC 959 page 40)

* Wed Apr 04 2007 Maros Barabas <mbarabas@redhat.com> - 2.0.5-16
- Merge review: - fix using %%{_var}, %%{_sbindir} and 
                  %%{_sysconfigdir} macros for files and install
                - fix BuildRoot
                - dropped usermod, openssl & pam requirement

* Tue Mar 20 2007 Florian La Roche <laroche@redhat.com> - 2.0.5-15
- fix BuildPrereq

* Tue Jan 30 2007 Maros Barabas <mbarabas@redhat.com> - 2.0.5-14
- remove file upload permission problem 
- change name of patch vsfptd-2.0.3-user_config
- Resolves #190193

* Fri Jan 19 2007 Maros Barabas <mbarabas@redhat.com> - 2.0.5-13
- add lost patch: don't die when no user config file is present 
- Resolves #166986

* Thu Jan 18 2007 Radek Vokal <rvokal@redhat.com> - 2.0.5-12
- add dist tag
- add buildrequires tcp_wrappers-devel

* Wed Jan 17 2007 Maros Barabas <mbarabas@redhat.com> - 2.0.5-11
- add errno EACCES to not die by vsf_sysutil_bind
- Resolves #198677

* Thu Dec 14 2006 Maros Barabas <mbarabas@redhat.com> - 2.0.5-10
- correct man (5) pages
- Resolves: #216765
- correct calling function stat 
- Resolves: bz200763

* Mon Dec 04 2006 Maros Barabas <mbarabas@redhat.com> - 2.0.5-9
- change BuildRequires tcp_wrappers to tcp_wrappers-devel

* Mon Aug 28 2006 Maros Barabas <mbarabas@redhat.com> - 2.0.5-8
- added forgotten patch to make filename filter (#174764)

* Tue Aug 22 2006 Maros Barabas <mbarabas@redhat.com> - 2.0.5-7
- correct paths of configuration files on man pages

* Tue Aug 15 2006 Maros Barabas <mbarabas@redhat.com> - 2.0.5-6
- correct comments

* Tue Aug 08 2006 Maros Barabas <mbarabas@redhat.com> - 2.0.5-5
- option to change listening to IPv6 protocol

* Tue Aug 01 2006 Maros Barabas <mbarabas@redhat.com> - 2.0.5-4
- listen to IPv4 connections in default conf file

* Mon Jul 17 2006 Radek Vokal <rvokal@redhat.com> - 2.0.5-3
- listen to IPv6 connections in default conf file

* Thu Jul 13 2006 Radek Vokal <rvokal@redhat.com> - 2.0.5-2
- add keyinit instructions to the vsftpd PAM script (#198637)

* Wed Jul 12 2006 Radek Vokal <rvokal@redhat.com> - 2.0.5-1
- upgrade to 2.0.5
- IE should now show the login dialog again (#191147)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.0.4-1.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.0.4-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.0.4-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Jan 12 2006 Radek Vokal <rvokal@redhat.com> 2.0.4-1
- upgrade to 2.0.4
- vsftpd now lock files for simultanous up/downloads (#162511)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 09 2005 Radek Vokal <rvokal@redhat.com> 2.0.3-12
- rebuilt against new openssl
- close std file descriptors

* Tue Oct 04 2005 Radek Vokal <rvokal@redhat.com> 2.0.3-11
- use include instead of pam_stack in pam config

* Fri Sep 09 2005 Radek Vokal <rvokal@redhat.com> 2.0.3-10
- vsfptd.log as a default log file has to be rotated (#167359)
- vsftpd does dns reverse before passing hosts to pam_access.so (#159745)

* Wed Aug 31 2005 Radek Vokal <rvokal@redhat.com> 2.0.3-9
- don't die when no user config file is present (#166986)

* Tue Aug 09 2005 Radek Vokal <rvokal@redhat.com> 2.0.3-8
- removed additional cmd line for ftp (#165083)

* Thu Aug 04 2005 Radek Vokal <rvokal@redhat.com> 2.0.3-7
- daemonize with file descriptors (#164998)

* Thu Jun 30 2005 Radek Vokal <rvokal@redhat.com> 2.0.3-6
- start in background as default, init script changed (#158714)

* Mon Jun 27 2005 Radek Vokal <rvokal@redhat.com> 2.0.3-5
- fixed requires for 64bit libs

* Thu Jun 23 2005 Radek Vokal <rvokal@redhat.com> 2.0.3-4
- fixed requires for pam_loginuid

* Wed Jun 01 2005 Radek Vokal <rvokal@redhat.com> 2.0.3-3
- vsftpd update for new audit system (#159223)

* Fri May 27 2005 Radek Vokal <rvokal@redhat.com> 2.0.3-2
- timezone fix, patch from suse.de (#158779)

* Wed Mar 23 2005 Radek Vokal <rvokal@redhat.com> 2.0.3-1
- new release, fixes #106416 and #134541 

* Mon Mar 14 2005 Radek Vokal <rvokal@redhat.com> 2.0.3-pre2
- prerelease, fixes IPv6 issues

* Mon Mar 14 2005 Radek Vokal <rvokal@redhat.com> 2.0.2-1
- update to new release, several bug fixes

* Wed Mar 02 2005 Radek Vokal <rvokal@redhat.com> 2.0.1-10
- rebuilt against gcc4 and new openssl

* Mon Feb 07 2005 Radek Vokal <rvokal@redhat.com> 2.0.1-9
- don't allow to read non-root config files (#145548)

* Mon Jan 10 2005 Radek Vokal <rvokal@redhat.com> 2.0.1-8
- use localtime also in logs (#143687)

* Tue Dec 14 2004 Radek Vokal <rvokal@redhat.com> 2.0.1-7
- fixing directory in vsftpd.pam file (#142805)

* Thu Nov 11 2004 Radek Vokal <rvokal@redhat.com> 2.0.1-6
- vsftpd. files moved to /etc/vsftpd
- added vsftpd_conf_migrate.sh script for moving conf files

* Fri Oct 01 2004 Radek Vokal <rvokal@redhat.com> 2.0.1-5
- vsftpd under xinetd reads its config file (#134314)

* Thu Sep 16 2004 Radek Vokal <rvokal@redhat.com> 2.0.1-4
- spec file changed, ftp dir change commented (#130119)
- added doc files (#113056)

* Wed Sep 08 2004 Jan Kratochvil <project-vsftpd@jankratochvil.net>
- update for 2.0.1 for SSL

* Fri Aug 27 2004 Radek Vokal <rvokal@redhat.com> 2.0.1-2
- vsftpd.conf file changed, default IPv6 support

* Fri Aug 20 2004 Radek Vokal <rvokal@redhat.com> 2.0.1-1
- tcp_wrapper patch updated, signal patch updated
- upgrade to 2.0.1, fixes several bugs, RHEL and FC builds

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 19 2004 Bill Nottingham <notting@redhat.com> 1.2.1-6
- fix the logrotate config (#116253) 

* Mon May  3 2004 Bill Nottingham <notting@redhat.com> 1.2.1-5
- fix all references to vsftpd.conf to be /etc/vsftpd/vsftpd.conf,
  including in the binary (#121199, #104075)

* Thu Mar 25 2004 Bill Nottingham <notting@redhat.com> 1.2.1-4
- don't call malloc()/free() in signal handlers (#119136,
  <olivier.baudron@m4x.org>)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Nov 24 2003 Karsten Hopp <karsten@redhat.de> 1.2.1-1
- update to 1.2.1, which fixes #89765 and lot of other issues
- remove manpage patch, it isn't required anymore
- clean up init script
- don't use script to find libs to link with (lib64 issues)

* Sun Oct 12 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- allow compiling without tcp_wrappers support

* Mon Sep 15 2003 Bill Nottingham <notting@redhat.com> 1.2.0-4
- fix errant newline (#104443)

* Fri Aug  8 2003 Bill Nottingham <notting@redhat.com> 1.2.0-3
- tweak man page (#84584, #72798)
- buildprereqs for pie (#99336)
- free ride through the build system to fix (#101582)

* Thu Jun 26 2003 Bill Nottingham <notting@redhat.com> 1.2.0-2
- update to 1.2.0

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Apr 28 2003 Bill Nottingham <notting@redhat.com> 1.1.3-9
- fix tcp_wrappers usage (#89765, <dale@riyescott.com>)

* Fri Feb 28 2003 Nalin Dahyabhai <nalin@redhat.com> 1.1.3-8
- enable use of tcp_wrappers

* Tue Feb 11 2003 Bill Nottingham <notting@redhat.com> 1.1.3-7
- provide /var/ftp & /var/ftp/pub. obsolete anonftp.

* Mon Feb 10 2003 Bill Nottingham <notting@redhat.com> 1.1.3-6
- clean up comments in init script (#83962)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Dec 30 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- change to /etc/rc.d/init.d for better compatibility

* Mon Dec 16 2002 Bill Nottingham <notting@redhat.com> 1.1.3-3
- fix initscript perms
- fix typo in initscript (#76587)

* Fri Dec 13 2002 Bill Nottingham <notting@redhat.com> 1.1.3-2
- update to 1.1.3
- run standalone, don't run by default
- fix reqs
 
* Fri Nov 22 2002 Joe Orton <jorton@redhat.com> 1.1.0-3
- fix use with xinetd-ipv6; add flags=IPv4 in xinetd file (#78410)

* Tue Nov 12 2002 Nalin Dahyabhai <nalin@redhat.com> 1.0.1-9
- remove absolute paths from PAM configuration so that the right modules get
  used for whichever arch we're built for on multilib systems

* Thu Aug 15 2002 Elliot Lee <sopwith@redhat.com> 1.0.1-8
- -D_FILE_OFFSET_BITS=64
- smp make
- remove forced optflags=-g for lack of supporting documentation
 
* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Apr 10 2002 Bill Nottingham <notting@redhat.com> 1.0.1-5
- don't spit out ugly errors if anonftp isn't installed (#62987)
- fix horribly broken userlist setup (#62321)

* Thu Feb 28 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.0.1-4
- s/Copyright/License/
- add "missingok" to the logrotate script, so we don't get errors
  when nothing has happened

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Nov 28 2001 Bill Nottingham <notting@redhat.com>
- initial packaging for RHL, munge included specfile

* Thu Mar 22 2001 Seth Vidal <skvidal@phy.duke.edu>
- updated to 0.0.15
- added entry for vsftpd.8 man page
- added entry for vsftpd.log logrotate file
- added TUNING file to docs list

* Wed Mar 7 2001 Seth Vidal <skvidal@phy.duke.edu>
- Updated to 0.0.14
- made %%files entry for man page

* Wed Feb 21 2001 Seth Vidal <skvidal@phy.duke.edu>
- Updated to 0.0.13

* Mon Feb 12 2001 Seth Vidal <skvidal@phy.duke.edu>
- Updated to 0.0.12

* Wed Feb 7 2001 Seth Vidal <skvidal@phy.duke.edu>
- updated to 0.0.11

* Thu Feb 1 2001 Seth Vidal <skvidal@phy.duke.edu>
- Update to 0.0.10

* Thu Feb 1 2001 Seth Vidal <skvidal@phy.duke.edu>
- First RPM packaging
- Stolen items from wu-ftpd's pam setup
- Separated rh 7 and rh 6.X's packages
- Built for Rh6
