Summary:        Network Presence Binding Daemon
Name:           tang
Version:        15
Release:        7%{?dist}
License:        GPL-3.0-or-later
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/latchset/%{name}
Source0:        https://github.com/latchset/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.xz
Source1:        tang.sysusers

BuildRequires:  asciidoc
BuildRequires:  coreutils
BuildRequires:  curl
BuildRequires:  gcc
BuildRequires:  git-core
BuildRequires:  grep
BuildRequires:  iproute
BuildRequires:  jose >= 8
BuildRequires:  libjose-devel >= 8
BuildRequires:  libjose-openssl-devel >= 8
BuildRequires:  libjose-zlib-devel >= 8
BuildRequires:  meson
BuildRequires:  llhttp-devel
BuildRequires:  pkgconfig
BuildRequires:  sed
BuildRequires:  socat
BuildRequires:  systemd
BuildRequires:  systemd-devel
BuildRequires:  systemd-rpm-macros

%{?systemd_ordering}
Requires:       coreutils
Requires:       jose >= 8
Requires:       llhttp
Requires:       grep
Requires:       sed
Requires(pre):  shadow-utils

%description
Tang is a small daemon for binding data to the presence of a third party.

%prep
%autosetup -S git

%build
%meson
%meson_build

%install
%meson_install
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/tang.conf
%{__mkdir_p} $RPM_BUILD_ROOT/%{_localstatedir}/db/%{name}

%check
%meson_test

%pre
%sysusers_create_compat %{SOURCE1}
exit 0

%post
%systemd_post %{name}d.socket

# Let's make sure any existing keys are readable only
# by the owner/group.
if [ -d /var/db/tang ]; then
    for k in /var/db/tang/*.jwk; do
        test -e "${k}" || continue
        chmod 0440 -- "${k}"
    done
    for k in /var/db/tang/.*.jwk; do
        test -e "${k}" || continue
        chmod 0440 -- "${k}"
    done
    chown tang:tang -R /var/db/tang
fi

%preun
%systemd_preun %{name}d.socket

%postun
%systemd_postun_with_restart %{name}d.socket

%files
%license COPYING
%attr(0700, %{name}, %{name}) %{_localstatedir}/db/%{name}
%{_unitdir}/%{name}d@.service
%{_unitdir}/%{name}d.socket
%{_libexecdir}/%{name}d-keygen
%{_libexecdir}/%{name}d-rotate-keys
%{_libexecdir}/%{name}d
%{_mandir}/man8/tang.8*
%{_bindir}/%{name}-show-keys
%{_mandir}/man1/tang-show-keys.1*
%{_mandir}/man1/tangd-rotate-keys.1.*
%{_sysusersdir}/tang.conf

%changelog
* Wed May 14 2025 Archana Shettigar <v-shettigara@microsoft.com> - 15-7
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu May 09 2024 Sergio Correia <scorreia@redhat.com> - 15-5
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
