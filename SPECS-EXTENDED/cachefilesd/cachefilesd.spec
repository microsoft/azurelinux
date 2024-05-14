Vendor:         Microsoft Corporation
Distribution:   Azure Linux

Name:		cachefilesd
Version:	0.10.10
Release:	9%{?dist}
Summary:	CacheFiles user-space management daemon
License:	GPLv2+
URL:		https://people.redhat.com/~dhowells/fscache/
Source0:	https://people.redhat.com/dhowells/fscache/cachefilesd-%{version}.tar.bz2
Source1:	%{name}-LICENSE.txt

BuildRequires:  gcc
BuildRequires: systemd-units
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires: selinux-policy-base >= 3.7.19-5

%define _hardened_build 1

%description
The cachefilesd daemon manages the caching files and directory that are that
are used by network file systems such a AFS and NFS to do persistent caching to
the local disk.

%global docdir %{_docdir}/cachefilesd

%prep
%setup -q
cp %{SOURCE1} ./LICENSE.txt

%build
make all \
	ETCDIR=%{_sysconfdir} \
	SBINDIR=%{_sbindir} \
	MANDIR=%{_mandir} \
	CFLAGS="-Wall -Werror $RPM_OPT_FLAGS $RPM_LD_FLAGS $ARCH_OPT_FLAGS"

%install
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_mandir}/{man5,man8}
mkdir -p %{buildroot}%{_localstatedir}/cache/fscache
make DESTDIR=%{buildroot} install \
	ETCDIR=%{_sysconfdir} \
	SBINDIR=%{_sbindir} \
	MANDIR=%{_mandir} \
	CFLAGS="-Wall $RPM_OPT_FLAGS -Werror"

install -m 644 cachefilesd.conf %{buildroot}%{_sysconfdir}
install -m 644 cachefilesd.service %{buildroot}%{_unitdir}/cachefilesd.service

%post
%systemd_post cachefilesd.service

%preun
%systemd_preun cachefilesd.service

%postun
%systemd_postun_with_restart cachefilesd.service

%files
%license LICENSE.txt
%doc README
%doc howto.txt
%doc selinux/move-cache.txt
%doc selinux/*.fc
%doc selinux/*.if
%doc selinux/*.te
%config(noreplace) %{_sysconfdir}/cachefilesd.conf
%{_sbindir}/*
%{_unitdir}/*
%{_mandir}/*/*
%{_localstatedir}/cache/fscache

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.10.10-9
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 7 2017 David Howells <dhowells@redhat.com> 0.10.10-1
- Stop using readdir_r [RH BZ 1423289].

* Wed Feb 17 2016 David Howells <dhowells@redhat.com> 0.10.9-1
- Fix name of directory in Makefile-generated tarball.

* Wed Feb 17 2016 David Howells <dhowells@redhat.com> 0.10.8-1
- Use systemd interaction macros in specfile installation sections [RH BZ 850053].
- Fix the service file to use /usr/sbin/ rather than /sbin/.
- Turn on RELRO and PIE build hardening in RPM builds.

* Wed Feb 3 2016 David Howells <dhowells@redhat.com> 0.10.7-1
- Call setgroups() before calling setuid() (caught by rpmlint).

* Wed Feb 3 2016 David Howells <dhowells@redhat.com> 0.10.6-1
- Note the correct licence.
- Handle malformed kernel status correctly.
- Permit culling to be disabled on the command line with the -N flag.
- Suspend culling when cache space is short and cache objects are pinned.

* Tue Dec 6 2011 David Howells <dhowells@redhat.com> 0.10.5-1
- Fix systemd service data according to review comments [RH BZ 754811].

* Tue Dec 6 2011 Dan Horák <dan[at]danny.cz>
- use Fedora CFLAGS in build (fixes build on s390)

* Wed Nov 30 2011 David Howells <dhowells@redhat.com> 0.10.4-1
- Fix packaging of systemd service file [RH BZ 754811].
- Fix rpmlint complaints.

* Tue Nov 22 2011 David Howells <dhowells@redhat.com> 0.10.3-1
- Move to native systemd management [RH BZ 754811].

* Fri Jul 15 2011 David Howells <dhowells@redhat.com> 0.10.2-1
- Downgrade all the culling messages to debug level [RH BZ 660347].

* Fri Jun 18 2010 David Howells <dhowells@redhat.com>
- Fix the initscript to have the appropriate parseable description and exit codes.

* Wed Apr 28 2010 David Howells <dhowells@redhat.com>
- Fix the Requires line on selinux-policy-base to be >=, not =.

* Fri Apr 23 2010 David Howells <dhowells@redhat.com> 0.10.1-1
- The SELinux policies for cachefilesd now live in the selinux-policy RPM, so
  the cachefilesd-selinux RPM is now redundant.
- Move the default cache dir to /var/cache/fscache.
- Make the initscript do a restorecon when starting the cache to make sure the
  labels are correct.
- Fix a wildchar that should be a literal dot in the SELinux policy.

* Thu Feb 25 2010 David Howells <dhowells@redhat.com> 0.10-1
- Fix the SELinux policies for cachefilesd.
- Compress the installed policy files.

* Tue Feb 23 2010 David Howells <dhowells@redhat.com>
- Must include sys/stat.h to use stat() and co. [RH BZ 565135].
- Remove tail comments from functions.

* Thu Aug 9 2007 David Howells <dhowells@redhat.com> 0.9-1
- The cachefiles module no longer accepts directory fds on cull and inuse
  commands, but rather uses current working directory.

* Mon Jul 2 2007 David Howells <dhowells@redhat.com> 0.8-16
- Use stat64/fstatat64 to avoid EOVERFLOW errors from the kernel on large files.

* Tue Nov 14 2006 David Howells <dhowells@redhat.com> 0.8-15
- Made cachefilesd ask the kernel whether cullable objects are in use and omit
  them from the cull table if they are.
- Made the size of cachefilesd's culling tables configurable.
- Updated the manual pages.

* Mon Nov 13 2006 David Howells <dhowells@redhat.com> 0.8-14
- Documented SELinux interaction.

* Fri Nov 10 2006 David Howells <dhowells@redhat.com> 0.8-11
- Include SELinux policy for cachefilesd.

* Thu Oct 19 2006 Steve Dickson <steved@redhat.com> 0.7-3
- Fixed typo that was causing the howto.txt not to be installed.

* Tue Oct 17 2006 David Howells <dhowells@redhat.com> 0.8-1
- Use /dev/cachefiles if it present in preference to /proc/fs/cachefiles.
- Use poll rather than SIGURG on /dev/cachefilesd.

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 0.7-2
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Fri Sep 22 2006 Steve Dickson <steved@redhat.com> 0.7-1
- updated to 0.7 which adds the howto.txt

* Wed Aug 30 2006 Steve Dickson <steved@redhat.com> 0.6-1
- Fixed memory corruption problem
- Added the fcull/fstop/frun options

* Fri Aug 11 2006 Steve Dickson <steved@redhat.com> 0.5-1
- Upgraded to 0.5 which fixed initial scan problem when
  started on an empty cache (bz 202184)

* Tue Aug  8 2006 Steve Dickson <steved@redhat.com> 0.4-3
- Updated init.d script to look for cachefilesd in /sbin
- Added postun and preun rules so cachefilesd is stopped
  and started when the rpm is updated or removed.

* Tue Aug  8 2006 Jesse Keating <jkeating@redhat.com> 0.4-2
- require /sbin/chkconfig not /usr/bin/chkconfig

* Tue Aug  1 2006 David Howells <dhowells@redhat.com> 0.4-1
- Discard use of autotools

* Tue Aug  1 2006 Steve Dickson <steved@redhat.com> 0.3-3
- Added URL to source file

* Fri Jul 28 2006 Steve Dickson <steved@redhat.com> 0.3-2
- Added post and preun rules
- Changed init.d script to up right before portmapper.

* Fri Jun  9 2006 Steve Dickson <steved@redhat.com> 0.3-1
- Incorporated David Howells manual page updates

* Thu Jun  8 2006 Steve Dickson <steved@redhat.com> 0.2-1
- Made the daemon 64-bit application.
- Changed the syslog logging to log the daemon's PID
- Changed OS error logging to log errno number as well the string

* Sat Apr 22 2006 Steve Dickson <steved@redhat.com> 0.1-1
- Initial commit
