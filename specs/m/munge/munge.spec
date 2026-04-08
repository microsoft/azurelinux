## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_without check

Name:           munge
Version:        0.5.18
Release:        %autorelease
Summary:        Enables uid & gid authentication across a host cluster

# The libs and devel package is GPLv3+ and LGPLv3+ where as the main package is GPLv3 only.
License:        GPL-3.0-or-later AND LGPL-3.0-or-later
URL:            https://dun.github.io/munge/
Source0:        https://github.com/dun/munge/releases/download/munge-%{version}/munge-%{version}.tar.xz
Source1:        https://github.com/dun/munge/releases/download/%{name}-%{version}/%{name}-%{version}.tar.xz.asc
Source2:        https://github.com/dun.gpg
Source3:        munge.sysusers
Source4:        README.md

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  git-core
BuildRequires:  gnupg2
BuildRequires:  systemd-rpm-macros
BuildRequires:  zlib-devel bzip2-devel openssl-devel
Requires:       munge-libs = %{version}-%{release}
Requires:       logrotate

%if %{with check}
BuildRequires:  procps-ng
BuildRequires:  util-linux
%endif


%{?systemd_requires}

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
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -N -S git
cp "%{SOURCE4}"  README-Fedora.md

%autopatch

%build
%configure  --disable-static --with-crypto-lib=openssl --runstatedir="%{_rundir}" --with-systemdunitdir="%{_unitdir}"  --with-sysconfigdir="%{_sysconfdir}/sysconfig/" --with-logrotateddir="%{_sysconfdir}/logrotate.d/"
# Get rid of some rpaths for /usr/sbin
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build


%install
%make_install

# Install extra files.
install -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysusersdir}/munge.conf

# rm unneeded files.
# Exclude .la files
rm %{buildroot}/%{_libdir}/libmunge.la


# Fix a few permissions
chmod 700 %{buildroot}%{_var}/lib/munge %{buildroot}%{_var}/log/munge
chmod 700 %{buildroot}%{_sysconfdir}/munge

# Create and empty key file and pid file to be marked as a ghost file below.
# i.e it is not actually included in the rpm, only the record
# of it is.
mkdir -p %{buildroot}%{_rundir}/munge
touch %{buildroot}%{_rundir}/munge/munged.pid

%check
%if %{with check}
%make_build check \
    LD_LIBRARY_PATH=%{buildroot}%{_libdir} \
    root=/tmp/munge-$$ VERBOSE=t verbose=t
%endif



%preun
%systemd_preun munge.service

%post
%systemd_post munge.service

%postun
%systemd_postun_with_restart munge.service

%ldconfig_scriptlets   libs

%files
%{_bindir}/munge
%{_bindir}/remunge
%{_bindir}/unmunge
%{_sbindir}/munged
%{_sbindir}/mungekey
%{_mandir}/man1/munge.1.gz
%{_mandir}/man1/remunge.1.gz
%{_mandir}/man1/unmunge.1.gz
%{_mandir}/man7/munge.7.gz
%{_mandir}/man8/munged.8.gz
%{_mandir}/man8/mungekey.8.gz
%{_unitdir}/munge.service

%attr(0700,munge,munge) %dir  %{_var}/log/munge
%attr(0700,munge,munge) %dir  %{_var}/lib/munge
%attr(0700,munge,munge) %dir %{_sysconfdir}/munge
%attr(0755,munge,munge) %ghost %dir  /run/munge/
%attr(0644,munge,munge) %ghost /run/munge/munged.pid

%{_sysusersdir}/munge.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/munge
%config(noreplace) %{_sysconfdir}/sysconfig/munge

%license COPYING COPYING.LESSER
%doc README-Fedora.md
%doc AUTHORS
%doc JARGON NEWS QUICKSTART README
%doc doc

%files libs
%{_libdir}/libmunge.so.2
%{_libdir}/libmunge.so.2.*

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
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 0.5.18-2
- Latest state for munge

* Fri Feb 13 2026 Michal Schmidt <mschmidt@redhat.com> - 0.5.18-1
- Update to 0.5.18

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.16-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Feb 11 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.5.16-5
- Drop call to %%sysusers_create_compat

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Mar 24 2024 Sandro <devel@penguinpee.nl> - 0.5.16-2
- Add Packit config

* Sun Mar 24 2024 Sandro <devel@penguinpee.nl> - 0.5.16-1
- Update to 0.5.16 (RHBZ#2269782)

* Tue Feb 06 2024 Izabela Bakollari <ibakolla@redhat.com> - 0.5.15-8
- migrated to SPDX license

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Aug 19 2022 Debarshi Ray <debarshir@gnome.org> - 0.5.15-3
- Remove redundant Requires(pre)

* Mon Jul 25 2022 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 0.5.15-2
- fix: correct failing test

* Mon Jul 25 2022 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 0.5.15-1
- feat: update to 0.5.15 (fixes rhbz#2100309)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.14-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 0.5.14-6
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Apr 30 2021 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.5.14-4
- Correct readme
- Include patches to fix build on s390x
- https://bugzilla.redhat.com/show_bug.cgi?id=1923337
- Include additional sources

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.5.14-3
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Nov 18 2020 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.5.14-1
- remove tmpfiles.d
- make %%_rundir,
- improve readme
- Mark /run/munge as ghost also

* Tue Nov 17 2020 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.5.14-1
- Update to latest release
- Remove unneeded files
- Update Readme.
- Enable gpgverify
- Enable tests

* Tue Sep 29 2020 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.5.13-10
- Fix spec + build

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Feb 10 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.5.13-8
- Provide a sysusers.d file to get user() and group() provides
  (see https://fedoraproject.org/wiki/Changes/Adopting_sysusers.d_format).

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

## END: Generated by rpmautospec
