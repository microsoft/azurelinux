Summary:        Enables uid & gid authentication across a host cluster
Name:           munge
Version:        0.5.15
Release:        1%{?dist}
# The libs and devel package is GPLv3+ and LGPLv3+ where as the main package is GPLv3 only.
License:        GPLv3+ AND LGPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://dun.github.io/munge/
Source0:        https://github.com/dun/munge/releases/download/munge-%{version}/munge-%{version}.tar.xz
Source1:        create-munge-key
Source2:        munge.logrotate
BuildRequires:  bzip2-devel
BuildRequires:  gcc
BuildRequires:  openssl-devel
BuildRequires:  systemd-units
BuildRequires:  zlib-devel
Requires:       logrotate
Requires:       munge-libs = %{version}-%{release}
Requires(post): systemd
Requires(postun): systemd
Requires(pre):  shadow-utils
Requires(preun): systemd

%description
MUNGE (MUNGE Uid 'N' Gid Emporium) is an authentication service for creating
and validating credentials. It is designed to be highly scalable for use
in an HPC cluster environment.
It allows a process to authenticate the UID and GID of another local or
remote process within a group of hosts having common users and groups.
These hosts form a security realm that is defined by a shared cryptographic
key. Clients within this security realm can create and validate credentials
without the use of root privileges, reserved ports, or platform-specific
methods.

%package devel
Summary:        Development files for uid * gid authentication across a host cluster
Requires:       munge-libs%{?_isa} = %{version}-%{release}

%description devel
Header files for developing using MUNGE.

%package libs
Summary:        Runtime libs for uid * gid authentication across a host cluster

%description libs
Runtime libraries for using MUNGE.

%prep
%setup -q
cp -p %{SOURCE1} create-munge-key
cp -p %{SOURCE2} munge.logrotate

%build
%configure  --disable-static --with-crypto-lib=openssl
echo "d /run/munge 0755 munge munge -" > src/etc/munge.tmpfiles.conf.in
# Get rid of some rpaths for /usr/sbin
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build


%install

%make_install

# Install extra files.
install -p -m 755 create-munge-key %{buildroot}/%{_sbindir}/create-munge-key
install -p -D -m 644 munge.logrotate %{buildroot}/%{_sysconfdir}/logrotate.d/munge

# Not installed by make
install -p -D -m 0644 src/etc/munge.tmpfiles.conf  %{buildroot}%{_tmpfilesdir}/%{name}.conf

# rm unneeded files.
rm %{buildroot}/%{_sysconfdir}/sysconfig/munge

# Exclude .la files
rm %{buildroot}/%{_libdir}/libmunge.la


# Fix a few permissions
chmod 700 %{buildroot}%{_sharedstatedir}/munge %{buildroot}%{_var}/log/munge
chmod 700 %{buildroot}%{_sysconfdir}/munge

# Create and empty key file and pid file to be marked as a ghost file below.
# i.e it is not actually included in the rpm, only the record
# of it is.
mkdir -p  %{buildroot}%{_var}/run/munge/
touch %{buildroot}%{_var}/run/munge/munged.pid
mv %{buildroot}%{_var}/run %{buildroot}

%postun
%systemd_postun_with_restart munge.service

%preun
%systemd_preun munge.service

%pre
getent group munge >/dev/null || groupadd -r munge
getent passwd munge >/dev/null || \
useradd -r -g munge -d /run/munge -s %{_sbindir}/nologin \
  -c "Runs Uid 'N' Gid Emporium" munge
exit 0

%post
%systemd_post munge.service

%ldconfig_scriptlets   libs

%files
%{_bindir}/munge
%{_bindir}/remunge
%{_bindir}/unmunge
%{_sbindir}/munged
%{_sbindir}/create-munge-key
%{_sbindir}/mungekey
%{_mandir}/man1/munge.1.gz
%{_mandir}/man1/remunge.1.gz
%{_mandir}/man1/unmunge.1.gz
%{_mandir}/man7/munge.7.gz
%{_mandir}/man8/munged.8.gz
%{_mandir}/man8/mungekey.8.gz
%{_unitdir}/munge.service

%attr(0700,munge,munge) %dir %{_var}/log/munge
%attr(0700,munge,munge) %dir %{_sharedstatedir}/munge
%attr(0700,munge,munge) %dir %{_sysconfdir}/munge
%attr(0755,munge,munge) %dir /run/munge/
%attr(0644,munge,munge) %ghost /run/munge/munged.pid

%config(noreplace) %{_tmpfilesdir}/munge.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/munge

%license COPYING COPYING.LESSER
%doc AUTHORS
%doc JARGON NEWS QUICKSTART README
%doc doc

%files libs
%{_libdir}/libmunge.so.2
%{_libdir}/libmunge.so.2.0.0

%files devel
%{_includedir}/munge.h
%{_libdir}/libmunge.so
%{_libdir}/pkgconfig/munge.pc
%{_mandir}/man3/munge.3.gz
%{_mandir}/man3/munge_ctx.3.gz
%{_mandir}/man3/munge_ctx_copy.3.gz
%{_mandir}/man3/munge_ctx_create.3.gz
%{_mandir}/man3/munge_ctx_destroy.3.gz
%{_mandir}/man3/munge_ctx_get.3.gz
%{_mandir}/man3/munge_ctx_set.3.gz
%{_mandir}/man3/munge_ctx_strerror.3.gz
%{_mandir}/man3/munge_decode.3.gz
%{_mandir}/man3/munge_encode.3.gz
%{_mandir}/man3/munge_enum.3.gz
%{_mandir}/man3/munge_enum_int_to_str.3.gz
%{_mandir}/man3/munge_enum_is_valid.3.gz
%{_mandir}/man3/munge_enum_str_to_int.3.gz
%{_mandir}/man3/munge_strerror.3.gz

%changelog
* Wed Jan 31 2024 Mitch Zhu <cblmargh@microsoft.com> - 0.5.15-1
- Upstream 0.5.15.

* Mon Feb 06 2023 Riken Maharjan <rmaharjan@microsoft.com> - 0.5.13-9
- Move from Extended to Core.
- License verified.

* Fri Apr 30 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.5.13-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Making binaries paths compatible with CBL-Mariner's paths.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 28 2019 Gerd Pokorra <gp@zimt.uni-siegen.de> - 0.5.13-6
- updating line in /usr/lib/tmpfiles.d/munge.conf: /var/run/munge → /run/munge
- add license tag
- add requires logrotate

* Wed Nov 27 2019 Gerd Pokorra <gp@zimt.uni-siegen.de> - 0.5.13-5
- built with OpenSSL (not libgcrypt)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 17 2018 Steve Traylen <steve.traylen@cern.ch> - 0.5.13-1
- Escape macros in %%changelog

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.5.12-9
- Escape macros in %%changelog

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 19 2017 Steve Traylen <steve.traylen@cern.ch> - 0.5.12-5
- Use libgcrypt rather than openssl.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Aug 15 2016 Steve Traylen <steve.traylen@cern.ch> - 0.5.12-3
- Correct Licesing strings.

* Mon Aug 15 2016 Steve Traylen <steve.traylen@cern.ch> - 0.5.12-2
- Include COPYING.LESSER also.
- Correct URL homepage

* Mon Aug 15 2016 Steve Traylen <steve.traylen@cern.ch> - 0.5.12-1
- Upstream 0.5.12
- License now GPLv3+ and also LGPLv3+ for libs.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 Nils Philippsen <nils@redhat.com>
- fix typo

* Fri Aug 30 2013 Steve Traylen <steve.traylen@cern.ch> - 0.5.11-1
- Upstream 0.5.11
- Use upstream's systemd files.
- Fix incorrect dates in changelogs.
- Fix systemd scriptlets #850219
- Use buildroot macro everywhere.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Feb 5 2012 Steve Traylen <steve.traylen@cern.ch> - 0.5.10-3
- Remove EPEL4 support since EOL.
- Change to systemd.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Feb 27 2011 Steve Traylen <steve.traylen@cern.ch> - 0.5.10-1
- Upstream to 0.5.10
- Add _isa tags to all build requires.
- Remove unused patch munge-correct-service-name.patch, upstream fixed.
- Update and add check-key-exists.patch back.
- Revert back to default CFLAGS. _GNU_SOURCE not needed any more.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 7 2010 Steve Traylen <steve.traylen@cern.ch> - 0.5.9-4
- Upsteam is now hosted on google.
- Mark /var/run/munge as a %%ghost file. #656631

* Sat Mar 27 2010 Steve Traylen <steve.traylen@cern.ch> - 0.5.9-3
- Release Bump

* Fri Mar 26 2010 Steve Traylen <steve.traylen@cern.ch> - 0.5.9-2
- Remove initd-pass-rpmlint.patch, has been applied upstream.
- Remove remove-GPL_LICENSED-cpp.patch, has been applied upstream.

* Fri Mar 26 2010 Steve Traylen <steve.traylen@cern.ch> - 0.5.9-1
- New upstream 0.5.9

* Wed Oct 21 2009 Steve Traylen <steve.traylen@cern.ch> - 0.5.8-8
- Requirment on munge removed from munge-libs.
- Explicit exact requirment on munge-libs for munge and munge-devel
  added.

* Wed Oct 21 2009 Steve Traylen <steve.traylen@cern.ch> - 0.5.8-7
- rhbz#530128 Move runtime libs to a new -libs package.
  ldconfig moved to new -libs package as a result.

* Sat Sep 26 2009 Steve Traylen <steve.traylen@cern.ch> - 0.5.8-6
- Patch for rhbz #525732 - Loads /etc/sysconfig/munge 
  correctly.
- Mark pid file as ghost file on oses that support that.
- Permisions on pid directory to 755

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.5.8-5
- rebuilt with new openssl

* Wed Jul 22 2009 Steve Traylen <steve.traylen@cern.ch> - 0.5.8-4
- Expand defattr with 4th argument for default directory perms.
- Explict attr for non 0644 files and 0755 directories.

* Wed Jul 22 2009 Steve Traylen <steve.traylen@cern.ch> - 0.5.8-3
- Append -DGNU_SOURCE to default CFLAGS.

* Wed Jul 22 2009 Steve Traylen <steve.traylen@cern.ch> - 0.5.8-2
- Correct License to GPLv2+
- Move man3 pages to the devel package.
- Remove +x bit from create-munge-key source.
- Preserve timestamps when installing files.
- ldconfig not needed on -devel package.
- Do a condrestart when upgrading.
- Remove redundant files from docs.
- chmod /var/lib/munge /var/log/munge and /etc/munge to 700.
- Apply patch to not error when GPL_LICENSED is not set.
- Patch service script to print error on if munge.key not present
  on start only and with a better error. 
- Remove dont-exit-form-lib.patch. munge is expecting munge to
  do this.
- Remove libgcrypt-devel from BuildRequires, uses openssl by
  default anyway.
- Mark the munge.key as a ghost file.

* Fri Jun 12 2009 Steve Traylen <steve@traylen.net> - 0.5.8-1
- First Build
