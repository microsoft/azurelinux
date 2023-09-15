Summary:        Network Presence Binding Daemon
Name:           tang
Version:        14
Release:        1%{?dist}
License:        GPL-3.0-or-later
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/latchset/%{name}
Source0:        https://github.com/latchset/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        tang.sysusers
BuildRequires:  asciidoc
BuildRequires:  coreutils
BuildRequires:  curl
BuildRequires:  gcc
BuildRequires:  git-core
BuildRequires:  grep
BuildRequires:  http-parser-devel >= 2.7.1-3
BuildRequires:  iproute
BuildRequires:  jose >= 8
BuildRequires:  libjose-devel >= 8
BuildRequires:  libjose-openssl-devel >= 8
BuildRequires:  libjose-zlib-devel >= 8
BuildRequires:  meson
BuildRequires:  pkgconfig
BuildRequires:  sed
BuildRequires:  socat
BuildRequires:  systemd
BuildRequires:  systemd-devel
Requires:       coreutils
Requires:       grep
Requires:       jose >= 8
Requires:       sed
Requires(pre):  shadow-utils
%{?systemd_requires}

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
echo "User=%{name}" >> %{buildroot}/%{_unitdir}/%{name}d@.service
mkdir -p %{buildroot}/%{_localstatedir}/db/%{name}

%check
%meson_test

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d %{_localstatedir}/cache/%{name} -s %{_sbindir}/nologin \
    -c "Tang Network Presence Daemon user" %{name}
exit 0

%post
%systemd_post %{name}d.socket

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
* Tue Sep 05 2023 Muhammad Falak R Wani <mwani@microsoft.com> - 14-1
- Upgrade version to address CVE-2023-1672
- Lint spec
- License verified

* Fri Apr 30 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 7-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Making binaries paths compatible with CBL-Mariner's paths.

* Tue Dec 1 2020 Sergio Correia <scorreia@redhat.com> - 7-6
- Move build system to meson
  Upstream commits (fed9020, 590de27)
- Move key handling to tang itself
  Upstream commits (6090505, c71df1d, 7119454)

* Tue Feb 25 2020 Sergio Correia <scorreia@redhat.com> - 7-5
- Rebuilt after http-parser update

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Aug 10 2018 Nathaniel McCallum <npmccallum@redhat.com> - 7-1
- New upstream release
- Retire tang-nagios package (now separate upstream)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 14 2017 Nathaniel McCallum <npmccallum@redhat.com> - 6-1
- New upstream release

* Wed Jun 14 2017 Nathaniel McCallum <npmccallum@redhat.com> - 5-2
- Fix incorrect dependencies

* Wed Jun 14 2017 Nathaniel McCallum <npmccallum@redhat.com> - 5-1
- New upstream release

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 14 2016 Nathaniel McCallum <npmccallum@redhat.com> - 4-2
- Fix a race condition in one of the tests

* Thu Nov 10 2016 Nathaniel McCallum <npmccallum@redhat.com> - 4-1
- New upstream release
- Add nagios subpackage

* Wed Oct 26 2016 Nathaniel McCallum <npmccallum@redhat.com> - 3-1
- New upstream release

* Wed Oct 19 2016 Nathaniel McCallum <npmccallum@redhat.com> - 2-1
- New upstream release

* Tue Aug 23 2016 Nathaniel McCallum <npmccallum@redhat.com> - 1-1
- First release
