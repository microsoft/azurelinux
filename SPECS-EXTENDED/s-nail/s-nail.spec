Name:           s-nail
Version:        14.9.25
Release:        1%{?dist}
Summary:        Environment for sending and receiving mail, providing functionality of POSIX mailx

# Everything is ISC except parts coming from the original Heirloom mailx which are BSD
License:        ISC AND BSD-4-Clause-UC AND BSD-3-Clause AND HPND-sell-variant
URL:            https://www.sdaoden.eu/code.html#s-nail
Source0:        https://www.sdaoden.eu/downloads/%{name}-%{version}.tar.xz
Source1:        https://www.sdaoden.eu/downloads/%{name}-%{version}.tar.xz.asc
# https://ftp.sdaoden.eu/steffen.asc
Source2:        steffen.asc

# https://bugzilla.redhat.com/show_bug.cgi?id=2171723
Patch0:		s-nail-makeflags.patch
Patch1:		s-nail-14.9.25-test-sha256.patch

BuildRequires:  make
BuildRequires:  gnupg2
BuildRequires:  gcc
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  krb5-devel
BuildRequires:  libidn2-devel
BuildRequires:  ncurses-devel

Requires(pre):  %{_sbindir}/update-alternatives

Provides:       mailx = %{version}-%{release}
Obsoletes:      mailx < 12.6

# For backwards compatibility
Provides: /bin/mail
Provides: /bin/mailx


%description
S-nail provides a simple and friendly environment for sending
and receiving mail. It is intended to provide the functionality
of the POSIX mailx(1) command, but is MIME capable and optionally offers
extensions for line editing, S/MIME, SMTP and POP3, among others.
S-nail divides incoming mail into its constituent messages and allows
the user to deal with them in any order. It offers many commands
and internal variables for manipulating messages and sending mail.
It provides the user simple editing capabilities to ease the composition
of outgoing messages, and increasingly powerful and reliable
non-interactive scripting capabilities.


%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'

%autosetup -p1

cat <<EOF >>nail.rc

# Fedora-specific defaults
set bsdcompat
set noemptystart
set prompt='& '
EOF


%build
%make_build \
    CFLAGS="%{build_cflags}" \
    LDFLAGS="%{build_ldflags}" \
    OPT_AUTOCC=no \
    OPT_DEBUG=yes \
    OPT_NOMEMDBG=yes \
    OPT_DOTLOCK=no \
    VAL_PREFIX=%{_prefix} \
    VAL_SYSCONFDIR=%{_sysconfdir} \
    VAL_MAIL=%{_localstatedir}/mail \
    config

%make_build build


%install
%make_install

# s-nail binary is installed with 0555 permissions, fix that
chmod 0755 %{buildroot}%{_bindir}/%{name}

# compatibility symlinks
for f in Mail mail mailx nail; do
    ln -s %{_bindir}/%{name} %{buildroot}%{_bindir}/$f
    ln -s %{_mandir}/man1/%{name}.1 %{buildroot}%{_mandir}/man1/$f.1
done


%check
%if %{defined rhel}
# SHA-1 is disabled as insecure by RHEL default policies, but used in tests
export OPENSSL_ENABLE_SHA1_SIGNATURES=yes
%endif
make test


%pre
%{_sbindir}/update-alternatives --remove-all mailx >/dev/null 2>&1 || :


%files
%license COPYING
%doc README
%{_bindir}/Mail
%{_bindir}/mail
%{_bindir}/nail
%{_bindir}/mailx
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.rc
%{_mandir}/man1/Mail.1*
%{_mandir}/man1/mail.1*
%{_mandir}/man1/nail.1*
%{_mandir}/man1/mailx.1*
%{_mandir}/man1/%{name}.1*


%changelog
* Thu Aug 01 2024 Tomas Korbar <tkorbar@redhat.com> - 14.9.25-1
- Rebase to 14.9.25
- Resolves: rhbz#2301265
- Resolves: rhbz#2295570

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 14.9.24-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 04 2024 Tomas Korbar <tkorbar@redhat.com> - 14.9.24-10
- Remove RSA-MD from License tag

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 14.9.24-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 11 2023 Nikola Forró <nforro@redhat.com> - 14.9.24-8
- Replace and obsolete mailx

* Wed Nov 01 2023 Tomas Korbar <tkorbar@redhat.com> - 14.9.24-7
- Add licenses to fully conform to SPDX

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 14.9.24-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Apr 21 2023 Tomas Korbar <tkorbar@redhat.com> - 14.9.24-5
- Fix s-nail installation without docs
- Resolves: rhbz#2188620

* Thu Apr 13 2023 Tomas Korbar <tkorbar@redhat.com> - 14.9.24-4
- Fix s-nail makeflags
- Resolves: rhbz#2171723

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 14.9.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 14.9.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Mar 27 2022 Nikola Forró <nforro@redhat.com> - 14.9.24-1
- New upstream release 14.9.24
  resolves: #2068768

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 14.9.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Nov 12 2021 Nikola Forró <nforro@redhat.com> - 14.9.23-1
- New upstream release 14.9.23
  resolves: #2022552

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 14.9.22-6
- Rebuilt with OpenSSL 3.0.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 14.9.22-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 07 2021 Nikola Forró <nforro@redhat.com> - 14.9.22-4
- Provide /bin/mail{,x} for backwards compatibility

* Wed Apr 14 2021 Nikola Forró <nforro@redhat.com> - 14.9.22-3
- Remove globs in %%files

* Tue Mar 16 2021 Nikola Forró <nforro@redhat.com> - 14.9.22-2
- Fix alternatives
  related: #1897928

* Wed Feb 24 2021 Nikola Forró <nforro@redhat.com> - 14.9.22-1
- New upstream release 14.9.22
  resolves: #1932122

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 14.9.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Nikola Forró <nforro@redhat.com> - 14.9.21-1
- New upstream release 14.9.21
  resolves: #1919030

* Mon Dec 14 2020 Nikola Forró <nforro@redhat.com> - 14.9.20-1
- New upstream release 14.9.20
  resolves: #1907112

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 14.9.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Apr 27 2020 Nikola Forró <nforro@redhat.com> - 14.9.19-1
- New upstream release 14.9.19
- Adjust default configuration to be closer to Heirloom mailx
- Provide alternativized binaries and man pages
  resolves: #1827969

* Thu Apr 23 2020 Nikola Forró <nforro@redhat.com> - 14.9.18-1
- Update to the latest upstream release

* Thu Apr 09 2020 Nikola Forró <nforro@redhat.com> - 14.9.17-1
- Initial package
