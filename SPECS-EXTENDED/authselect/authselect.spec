# Do not terminate build if language files are empty.
%define _empty_manifest_terminate_build 0

Name:           authselect
Version:        1.2.1
Release:        2%{?dist}
Summary:        Configures authentication and identity sources from supported profiles
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/authselect/authselect

License:        GPLv3+
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%if 0%{?rhel}
Source1:        translations.tar.gz
%endif

%global makedir %{_builddir}/%{name}-%{version}

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
Requires: authselect-libs%{?_isa} = %{version}-%{release}
Suggests: sssd
Suggests: samba-winbind
Suggests: fprintd-pam
Suggests: oddjob-mkhomedir

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
Requires: findutils
Requires: gawk
Requires: grep
Requires: sed
Requires: systemd
Requires: pam >= 1.3.1-23

%description libs
Common library files for authselect. This package is used by the authselect
command line tool and any other potential front-ends.

%package compat
Summary: Tool to provide minimum backwards compatibility with authconfig
Obsoletes: authconfig < 7.0.1-6
Provides: authconfig
BuildRequires: python3-devel
Requires: authselect%{?_isa} = %{version}-%{release}
Recommends: oddjob-mkhomedir
Suggests: sssd
Suggests: realmd
Suggests: samba-winbind
# Required by scriptlets
Requires: sed

%description compat
This package will replace %{_sbindir}/authconfig with a tool that will
translate some of the authconfig calls into authselect calls. It provides
only minimum backward compatibility and users are encouraged to migrate
to authselect completely.

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

# Install RHEL translations
# It is not possible to use wildcards here so we need to use 'find'
%if 0%{?rhel}
find "%{makedir}/po" "%{makedir}/src/man/po" -name "*.po" -delete
%__rm "%{makedir}/po/LINGUAS"
%setup -T -D -a 1
%endif

%build
autoreconf -if
%configure --with-pythonbin="%{__python3}"
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
%dir %{_localstatedir}/lib/authselect
%ghost %attr(0755,root,root) %{_localstatedir}/lib/authselect/backups/
%ghost %attr(0644,root,root) %{_localstatedir}/lib/authselect/dconf-db
%ghost %attr(0644,root,root) %{_localstatedir}/lib/authselect/dconf-locks
%ghost %attr(0644,root,root) %{_localstatedir}/lib/authselect/fingerprint-auth
%ghost %attr(0644,root,root) %{_localstatedir}/lib/authselect/nsswitch.conf
%ghost %attr(0644,root,root) %{_localstatedir}/lib/authselect/password-auth
%ghost %attr(0644,root,root) %{_localstatedir}/lib/authselect/postlogin
%ghost %attr(0644,root,root) %{_localstatedir}/lib/authselect/smartcard-auth
%ghost %attr(0644,root,root) %{_localstatedir}/lib/authselect/system-auth
%ghost %attr(0644,root,root) %{_localstatedir}/lib/authselect/user-nsswitch-created
%dir %{_datadir}/authselect
%dir %{_datadir}/authselect/vendor
%dir %{_datadir}/authselect/default
%dir %{_datadir}/authselect/default/minimal/
%dir %{_datadir}/authselect/default/nis/
%dir %{_datadir}/authselect/default/sssd/
%dir %{_datadir}/authselect/default/winbind/
%{_datadir}/authselect/default/minimal/nsswitch.conf
%{_datadir}/authselect/default/minimal/password-auth
%{_datadir}/authselect/default/minimal/postlogin
%{_datadir}/authselect/default/minimal/README
%{_datadir}/authselect/default/minimal/REQUIREMENTS
%{_datadir}/authselect/default/minimal/system-auth
%{_datadir}/authselect/default/nis/dconf-db
%{_datadir}/authselect/default/nis/dconf-locks
%{_datadir}/authselect/default/nis/fingerprint-auth
%{_datadir}/authselect/default/nis/nsswitch.conf
%{_datadir}/authselect/default/nis/password-auth
%{_datadir}/authselect/default/nis/postlogin
%{_datadir}/authselect/default/nis/README
%{_datadir}/authselect/default/nis/REQUIREMENTS
%{_datadir}/authselect/default/nis/system-auth
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
%{_datadir}/authselect/default/winbind/system-auth
%{_libdir}/libauthselect.so.*
%{_mandir}/man5/authselect-profiles.5*
%{_datadir}/doc/authselect/COPYING
%{_datadir}/doc/authselect/README.md
%license COPYING
%doc README.md

%files compat
%{_sbindir}/authconfig
%{python3_sitelib}/authselect/

%files devel
%{_includedir}/authselect.h
%{_libdir}/libauthselect.so
%{_libdir}/pkgconfig/authselect.pc

%files  -f %{name}.8.lang  -f %{name}-migration.7.lang
%{_bindir}/authselect
%{_mandir}/man8/authselect.8*
%{_mandir}/man7/authselect-migration.7*
%{_sysconfdir}/bash_completion.d/authselect-completion.sh

%global validfile %{_localstatedir}/lib/rpm-state/%{name}.config-valid

%pre libs
%__rm -f %{validfile}
if [ $1 -gt 1 ] ; then
    # Remember if the current configuration is valid
    %{_bindir}/authselect check &> /dev/null
    if [ $? -eq 0 ]; then
        touch %{validfile}
    fi
fi

exit 0

%posttrans libs
# Copy nsswitch.conf to user-nsswitch.conf if it was not yet created
if [ ! -f %{_localstatedir}/lib/authselect/user-nsswitch-created ]; then
    %__cp -n %{_sysconfdir}/nsswitch.conf %{_sysconfdir}/authselect/user-nsswitch.conf &> /dev/null
    touch %{_localstatedir}/lib/authselect/user-nsswitch-created &> /dev/null

    # If we are upgrading from older version, we want to remove these comments.
    %__sed -i '/^# Generated by authselect on .*$/{$!{
      N;N # Read also next two lines
      /# Generated by authselect on .*\n# Do not modify this file manually.\n/d
    }}' %{_sysconfdir}/authselect/user-nsswitch.conf &> /dev/null
fi

# If the configuration is valid and we are upgrading from older version
# we need to create these files since they were added in 1.0.
if [ -f %{validfile} ]; then
    FILES="nsswitch.conf system-auth password-auth fingerprint-auth \
           smartcard-auth postlogin dconf-db dconf-locks"

    for FILE in $FILES ; do
        %__cp -n %{_sysconfdir}/authselect/$FILE \
               %{_localstatedir}/lib/authselect/$FILE &> /dev/null
    done

    %__rm -f %{validfile}
fi

# Apply any changes to profiles (validates configuration first internally)
%{_bindir}/authselect apply-changes &> /dev/null

# Enable with-sudo feature if sssd-sudo responder is enabled. RHBZ#1582111
CURRENT=`%{_bindir}/authselect current --raw 2> /dev/null`
if [ $? -eq 0 ]; then
    PROFILE=`echo $CURRENT | %__awk '{print $1;}'`

    if [ $PROFILE == "sssd" ] ; then
        if %__grep -E "services[[:blank:]]*=[[:blank:]]*.*sudo" /etc/sssd/sssd.conf &> /dev/null ; then
            %{_bindir}/authselect enable-feature with-sudo &> /dev/null
        elif systemctl is-active sssd-sudo.service sssd-sudo.socket --quiet || systemctl is-enabled sssd-sudo.socket --quiet ; then
            %{_bindir}/authselect enable-feature with-sudo &> /dev/null
        fi
    fi
fi

exit 0

%posttrans compat
# Fix for RHBZ#1618865
# Remove invalid lines from pwquality.conf generated by authconfig compat tool
# - previous version could write some options without value, which is invalid
# - we delete all options without value from existing file
%__sed -i -E '/^\w+=$/d' %{_sysconfdir}/security/pwquality.conf.d/10-authconfig-pwquality.conf &> /dev/null
exit 0

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.1-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
