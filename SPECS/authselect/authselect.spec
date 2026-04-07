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

# Do not terminate build if language files are empty.
%define _empty_manifest_terminate_build 0

Name:           authselect
Version:        1.6.2
Release:        %autorelease
Summary:        Configures authentication and identity sources from supported profiles
URL:            https://github.com/authselect/authselect

License:        GPL-3.0-or-later
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

%global makedir %{_builddir}/%{name}-%{version}

# Disable NIS profile on RHEL
%if 0%{?rhel}
%global with_nis_profile 0
%else
%global with_nis_profile 1
%endif

# Set the default profile
%{?fedora:%global default_profile local with-silent-lastlog}
%{?rhel:%global default_profile local}

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  findutils
BuildRequires:  libtool
BuildRequires:  m4
BuildRequires:  gcc
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(popt)
BuildRequires:  gettext-devel
BuildRequires:  po4a
BuildRequires:  %{_bindir}/a2x
BuildRequires:  libcmocka-devel >= 1.0.0
BuildRequires:  libselinux-devel
BuildRequires:  systemd-devel
BuildRequires:  systemd-rpm-macros
Requires: authselect-libs%{?_isa} = %{version}-%{release}

# RHEL does not have meta flag yet
%if 0%{?rhel} <= 10
Suggests: sssd
Suggests: samba-winbind
Suggests: fprintd-pam
Suggests: oddjob-mkhomedir
%else
Suggests(meta): sssd
Suggests(meta): samba-winbind
Suggests(meta): fprintd-pam
Suggests(meta): oddjob-mkhomedir
%endif

# Properly obsolete removed authselect-compat package.
Obsoletes: authselect-compat < 1.3

%description
Authselect is designed to be a replacement for authconfig but it takes
a different approach to configure the system. Instead of letting
the administrator build the PAM stack with a tool (which may potentially
end up with a broken configuration), it would ship several tested stacks
(profiles) that solve a use-case and are well tested and supported.
At the same time, some obsolete features of authconfig are not
supported by authselect.

%package libs
Summary: Utility library used by the authselect tool
# Required by scriptlets
Requires: coreutils
Requires: sed
Suggests: systemd

%description libs
Common library files for authselect. This package is used by the authselect
command line tool and any other potential front-ends.

%package devel
Summary: Development libraries and headers for authselect
Requires: authselect-libs%{?_isa} = %{version}-%{release}

%description devel
System header files and development libraries for authselect. Useful if
you develop a front-end for the authselect library.

%prep
%setup -q

for p in %patches ; do
    %__patch -p1 -i $p
done

%build
autoreconf -if
%configure \
%if %{with_nis_profile}
    --with-nis-profile \
%endif
    %{nil}
%make_build

%check
%make_build check

%install
%make_install

# Find translations
%find_lang %{name}
%find_lang %{name} %{name}.8.lang --with-man
%find_lang %{name}-migration %{name}-migration.7.lang --with-man
%find_lang %{name}-profiles %{name}-profiles.5.lang --with-man

# We want this file to contain only manual page translations
%__sed -i '/LC_MESSAGES/d' %{name}.8.lang

# Remove .la and .a files created by libtool
find $RPM_BUILD_ROOT -name "*.la" -exec %__rm -f {} \;
find $RPM_BUILD_ROOT -name "*.a" -exec %__rm -f {} \;

%ldconfig_scriptlets libs

%files libs -f %{name}.lang -f %{name}-profiles.5.lang
%dir %{_sysconfdir}/authselect
%dir %{_sysconfdir}/authselect/custom
%ghost %attr(0644,root,root) %{_sysconfdir}/authselect/authselect.conf
%ghost %attr(0644,root,root) %{_sysconfdir}/authselect/dconf-db
%ghost %attr(0644,root,root) %{_sysconfdir}/authselect/dconf-locks
%ghost %attr(0644,root,root) %{_sysconfdir}/authselect/fingerprint-auth
%ghost %attr(0644,root,root) %{_sysconfdir}/authselect/nsswitch.conf
%ghost %attr(0644,root,root) %{_sysconfdir}/authselect/password-auth
%ghost %attr(0644,root,root) %{_sysconfdir}/authselect/postlogin
%ghost %attr(0644,root,root) %{_sysconfdir}/authselect/smartcard-auth
%ghost %attr(0644,root,root) %{_sysconfdir}/authselect/system-auth
%ghost %attr(0644,root,root) %{_sysconfdir}/nsswitch.conf
%ghost %attr(0644,root,root) %{_sysconfdir}/pam.d/fingerprint-auth
%ghost %attr(0644,root,root) %{_sysconfdir}/pam.d/password-auth
%ghost %attr(0644,root,root) %{_sysconfdir}/pam.d/postlogin
%ghost %attr(0644,root,root) %{_sysconfdir}/pam.d/smartcard-auth
%ghost %attr(0644,root,root) %{_sysconfdir}/pam.d/system-auth
%dir %{_localstatedir}/lib/authselect
%ghost %attr(0755,root,root) %{_localstatedir}/lib/authselect/backups/
%dir %{_datadir}/authselect
%dir %{_datadir}/authselect/vendor
%dir %{_datadir}/authselect/default
%dir %{_datadir}/authselect/default/local/
%dir %{_datadir}/authselect/default/sssd/
%dir %{_datadir}/authselect/default/winbind/
%verify(not md5 size mtime) %{_datadir}/authselect/checksum
%{_datadir}/authselect/default/local/dconf-db
%{_datadir}/authselect/default/local/dconf-locks
%{_datadir}/authselect/default/local/fingerprint-auth
%{_datadir}/authselect/default/local/nsswitch.conf
%{_datadir}/authselect/default/local/password-auth
%{_datadir}/authselect/default/local/postlogin
%{_datadir}/authselect/default/local/README
%{_datadir}/authselect/default/local/REQUIREMENTS
%{_datadir}/authselect/default/local/smartcard-auth
%{_datadir}/authselect/default/local/system-auth
%{_datadir}/authselect/default/sssd/dconf-db
%{_datadir}/authselect/default/sssd/dconf-locks
%{_datadir}/authselect/default/sssd/fingerprint-auth
%{_datadir}/authselect/default/sssd/nsswitch.conf
%{_datadir}/authselect/default/sssd/password-auth
%{_datadir}/authselect/default/sssd/postlogin
%{_datadir}/authselect/default/sssd/README
%{_datadir}/authselect/default/sssd/REQUIREMENTS
%{_datadir}/authselect/default/sssd/smartcard-auth
%{_datadir}/authselect/default/sssd/system-auth
%{_datadir}/authselect/default/winbind/dconf-db
%{_datadir}/authselect/default/winbind/dconf-locks
%{_datadir}/authselect/default/winbind/fingerprint-auth
%{_datadir}/authselect/default/winbind/nsswitch.conf
%{_datadir}/authselect/default/winbind/password-auth
%{_datadir}/authselect/default/winbind/postlogin
%{_datadir}/authselect/default/winbind/README
%{_datadir}/authselect/default/winbind/REQUIREMENTS
%{_datadir}/authselect/default/winbind/smartcard-auth
%{_datadir}/authselect/default/winbind/system-auth
%if %{with_nis_profile}
%dir %{_datadir}/authselect/default/nis/
%{_datadir}/authselect/default/nis/dconf-db
%{_datadir}/authselect/default/nis/dconf-locks
%{_datadir}/authselect/default/nis/fingerprint-auth
%{_datadir}/authselect/default/nis/nsswitch.conf
%{_datadir}/authselect/default/nis/password-auth
%{_datadir}/authselect/default/nis/postlogin
%{_datadir}/authselect/default/nis/README
%{_datadir}/authselect/default/nis/REQUIREMENTS
%{_datadir}/authselect/default/nis/smartcard-auth
%{_datadir}/authselect/default/nis/system-auth
%endif
%{_libdir}/libauthselect.so.*
%{_mandir}/man5/authselect-profiles.5*
%dir %{_datadir}/doc/authselect
%{_datadir}/doc/authselect/COPYING
%{_datadir}/doc/authselect/README.md
%{_unitdir}/authselect-apply-changes.service
%license COPYING
%doc README.md

%files devel
%{_includedir}/authselect.h
%{_libdir}/libauthselect.so
%{_libdir}/pkgconfig/authselect.pc

%files  -f %{name}.8.lang  -f %{name}-migration.7.lang
%{_bindir}/authselect
%{_mandir}/man8/authselect.8*
%{_mandir}/man7/authselect-migration.7*
%{_sysconfdir}/bash_completion.d/authselect-completion.sh

%post libs
%systemd_post authselect-apply-changes.service

%preun libs
%systemd_preun authselect-apply-changes.service

%postun libs
%systemd_postun authselect-apply-changes.service

%posttrans libs
# Keep nss-altfiles for all rpm-ostree based systems.
# See https://github.com/authselect/authselect/issues/48
if test -e /run/ostree-booted; then
    for PROFILE in `ls %{_datadir}/authselect/default`; do
        %{_bindir}/authselect create-profile $PROFILE --vendor --base-on $PROFILE --symlink-pam --symlink-dconf --symlink=REQUIREMENTS --symlink=README &> /dev/null
        %__sed -i -e 's/{if "with-altfiles":\([^}]\+\)}/\1/g' %{_datadir}/authselect/vendor/$PROFILE/nsswitch.conf &> /dev/null
    done
fi

# If this is a new installation select the default configuration.
if [ $1 == 1 ] ; then
    %{_bindir}/authselect select %{default_profile} --force --nobackup &> /dev/null
    exit 0
fi

# Minimal profile was removed. Switch to local during upgrade.
%__sed -i '1 s/^minimal$/local/'  %{_sysconfdir}/authselect/authselect.conf
for file in  %{_sysconfdir}/authselect/custom/*/*; do
    link=`%{_bindir}/readlink "$file"`
    if [[ "$link" == %{_datadir}/authselect/default/minimal/* ]]; then
        target=`%{_bindir}/basename "$link"`
        %{_bindir}/ln -sfn "%{_datadir}/authselect/default/local/$target" "$file"
    fi
done

# We might have add vendor profiles, compute new profiles checksum
%{_bindir}/find "%{_datadir}/authselect" -mindepth 2 -type f \
    -printf "%%P\n" -exec %{_bindir}/sha256sum {} + | %{_bindir}/sha256sum \
    > "%{_datadir}/authselect/checksum"

# Apply any changes to profiles (validates configuration first internally)
%{_bindir}/authselect apply-changes &> /dev/null

exit 0

%preun
if [ $1 == 0 ] ; then
    # Remove authselect symbolic links so all authselect files can be
    # deleted safely. If this fail, the uninstallation must fail to avoid
    # breaking the system by removing PAM files. However, the command can
    # only fail if it can not write to the file system.
    %{_bindir}/authselect opt-out
fi

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 1.6.2-2
- Latest state for authselect

* Tue Sep 30 2025 Packit <hello@packit.dev> - 1.6.2-1
- Update to 1.6.2 upstream release

* Thu Jul 31 2025 Packit <hello@packit.dev> - 1.6.1-1
- Update to 1.6.1 upstream release

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Feb 05 2025 Packit <hello@packit.dev> - 1.5.1-1
- Update to version 1.5.1

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Oct 9 2024 Pavel Březina <pbrezina@redhat.com> - 1.5.0-8
- Temporary revert: myhostname is put right before dns module in nsswitch.conf hosts (rhbz#2291062)

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 28 2024 Pavel Březina <pbrezina@redhat.com> - 1.5.0-6
- Use Suggests(meta) to avoid circular dependencies (rhbz#2291235)

* Tue Feb 27 2024 Jonathan Lebon <jonathan@jlebon.com> - 1.5.0-5
- Fix altfiles rendering on OSTree variants

* Fri Feb 23 2024 Pavel Březina <pbrezina@redhat.com> - 1.5.0-4
- Add back with-files-access-provider
- Remove outdated scriptlets
- Group merging added to nsswitch.conf group in all profiles
- myhostname is put right before dns module in nsswitch.conf hosts (rhbz#2257197)
- Internal packaging changes

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 18 2024 Pavel Březina <pbrezina@redhat.com> - 1.5.0-1
- Rebase to 1.5.0
- "minimal" profile was removed and replaced with "local". (rhbz#2253180)
- "local" profile is now default (rhbz#2253180)

* Wed Sep 27 2023 Pavel Březina <pbrezina@redhat.com> - 1.4.3-1
- Rebase to 1.4.3

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 5 2022 Pavel Březina <pbrezina@redhat.com> - 1.4.2-1
- Rebase to 1.4.2

* Thu Dec 1 2022 Pavel Březina <pbrezina@redhat.com> - 1.4.1-1
- Rebase to 1.4.1

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 8 2022 Pavel Březina <pbrezina@redhat.com> - 1.4.0-2
- Fix issues with popt-1.19

* Thu May 5 2022 Pavel Březina <pbrezina@redhat.com> - 1.4.0-1
- Rebase to 1.3.0

* Thu Feb 10 2022 Pavel Březina <pbrezina@redhat.com> - 1.3.0-10
- Fix mdns support (#2052269)

* Thu Feb 3 2022 Pavel Březina <pbrezina@redhat.com> - 1.3.0-9
- Make authselect compatible with ostree (#2034360)
- Authselect now requires explicit opt-out if users don't want to use it (#2051545)

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 13 2022 Pavel Březina <pbrezina@redhat.com> - 1.3.0-7
- Remove unnecessary dependencies (#2039869)

* Thu Jan 13 2022 Pavel Březina <pbrezina@redhat.com> - 1.3.0-6
- Fix detection of ostree system (#2034360)

* Tue Dec 28 2021 Frantisek Zatloukal <fzatlouk@redhat.com> - 1.3.0-5
- Try to use io.open() in pre scriptlet instead of rpm.open() (rpm >= 4.17.0)

* Tue Dec 21 2021 Frantisek Zatloukal <fzatlouk@redhat.com> - 1.3.0-4
- Use lua for pre scriptlets to reduce dependencies

* Fri Dec 10 2021 Pavel Březina <pbrezina@redhat.com> - 1.3.0-3
- Update conflicting versions of glibc and pam

* Mon Dec 6 2021 Pavel Březina <pbrezina@redhat.com> - 1.3.0-1
- Rebase to 1.3.0
- Authselect configuration is now enforced (#2000936)

* Sat Aug 14 2021 Björn Esser <besser82@fedoraproject.org> - 1.2.4-2
- Add proper Obsoletes for removed authselect-compat package
  Fixes: rhbz#1993189

* Mon Aug 9 2021 Pavel Březina <pbrezina@redhat.com> - 1.2.4-1
- Rebase to 1.2.4

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 21 2021 Björn Esser <besser82@fedoraproject.org> - 1.2.3-3
- Backport support for yescrypt hash method

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.2.3-2
- Rebuilt for Python 3.10

* Wed Mar 31 2021 Pavel Březina <pbrezina@redhat.com> - 1.2.3-1
- Rebase to 1.2.3

* Tue Mar 09 2021 Benjamin Berg <bberg@redhat.com> - 1.2.2-4
- Add patch to make fingerprint-auth return non-failing pam_fprintd.so errors
  Resolves: #1935331

* Thu Mar 4 2021 Pavel Březina <pbrezina@redhat.com> - 1.2.2-3
- minimal: add dconf settings to explicitly disable fingerprint and smartcard authentication

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Nov 25 2020 Pavel Březina <pbrezina@redhat.com> - 1.2.2-1
- Rebase to 1.2.2
- Add nss-altfiles to profiles on Fedora Silverblue

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 22 2020 Pavel Březina <pbrezina@redhat.com> - 1.2.1-3
- Add resolved by default to nis and minimal profiles
- Fix parsing of multiple conditionals on the same line

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.2.1-2
- Rebuilt for Python 3.9

* Mon May 11 2020 Pavel Březina <pbrezina@redhat.com> - 1.2.1-1
- Rebase to 1.2.1

* Wed Mar 4 2020 Pavel Březina <pbrezina@redhat.com> - 1.2-1
- Rebase to 1.2

* Mon Feb 17 2020 Pavel Březina <pbrezina@redhat.com> - 1.1-7
- fix restoring non-authselect configuration from backup

* Wed Jan 29 2020 Pavel Březina <pbrezina@redhat.com> - 1.1-6
- cli: fix auto backup when --force is set

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1-3
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 13 2019 Pavel Březina <pbrezina@redhat.com> - 1.1-1
- Rebase to 1.1

* Tue Feb 26 2019 Pavel Březina <pbrezina@redhat.com> - 1.0.3-1
- Rebase to 1.0.3

* Tue Feb 26 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.2-4
- Use %ghost for files owned by authselect

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 3 2018 Pavel Březina <pbrezina@redhat.com> - 1.0.2-2
- Resolves rhbz#1655025 (invalid backup).

* Fri Nov 23 2018 Pavel Březina <pbrezina@redhat.com> - 1.0.2-1
- Rebase to 1.0.2

* Thu Sep 27 2018 Pavel Březina <pbrezina@redhat.com> - 1.0.1-2
- Require systemd instead of systemctl

* Thu Sep 27 2018 Pavel Březina <pbrezina@redhat.com> - 1.0.1-1
- Rebase to 1.0.1

* Fri Sep 14 2018 Pavel Březina <pbrezina@redhat.com> - 1.0-3
- Scriptlets should no produce any error messages (RHBZ #1622272)
- Provide fix for pwquality configuration (RHBZ #1618865)

* Thu Aug 30 2018 Adam Williamson <awilliam@redhat.com> - 1.0-2
- Backport PR #78 to fix broken pwquality config (RHBZ #1618865)

* Mon Aug 13 2018 Pavel Březina <pbrezina@redhat.com> - 1.0-1
- Rebase to 1.0

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.4-4
- Rebuilt for Python 3.7

* Mon May 14 2018 Pavel Březina <pbrezina@redhat.com> - 0.4-3
- Disable sssd as sudo rules source with sssd profile by default (RHBZ #1573403)

* Wed Apr 25 2018 Christian Heimes <cheimes@redhat.com> - 0.4-2
- Don't disable oddjobd.service (RHBZ #1571844)

* Mon Apr 9 2018 Pavel Březina <pbrezina@redhat.com> - 0.4-1
- rebasing to 0.4

* Tue Mar 6 2018 Pavel Březina <pbrezina@redhat.com> - 0.3.2-1
- rebasing to 0.3.2
- authselect-compat now only suggests packages, not recommends

* Mon Mar 5 2018 Pavel Březina <pbrezina@redhat.com> - 0.3.1-1
- rebasing to 0.3.1

* Tue Feb 20 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.3-3
- Provide authconfig

* Tue Feb 20 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.3-2
- Properly own all appropriate directories
- Remove unneeded %%defattr
- Remove deprecated Group tag
- Make Obsoletes versioned
- Remove unneeded ldconfig scriptlets

* Tue Feb 20 2018 Pavel Březina <pbrezina@redhat.com> - 0.3-1
- rebasing to 0.3
* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild
* Wed Jan 10 2018 Pavel Březina <pbrezina@redhat.com> - 0.2-2
- fix rpmlint errors
* Wed Jan 10 2018 Pavel Březina <pbrezina@redhat.com> - 0.2-1
- rebasing to 0.2
* Mon Jul 31 2017 Jakub Hrozek <jakub.hrozek@posteo.se> - 0.1-1
- initial packaging

## END: Generated by rpmautospec
