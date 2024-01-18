Summary:        A general purpose TCP-IP emulator
Name:           libslirp
Version:        4.7.0
Release:        1%{?dist}
License:        BSD AND MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://gitlab.freedesktop.org/slirp/libslirp
Source0:        %{url}/-/archive/v%{version}/%{name}-v%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  glib-devel
BuildRequires:  meson

%description
A general purpose TCP-IP emulator used by virtual machine hypervisors
to provide virtual networking services.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -n %{name}-v%{version}

%build
%meson
%meson_build

%install
%meson_install

# %%check
# There is no test suite available for libslirp as of 4.6.1

%files
%license COPYRIGHT
%doc README.md CHANGELOG.md
%{_libdir}/%{name}.so.0*

%files devel
%dir %{_includedir}/slirp/
%{_includedir}/slirp/*
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/slirp.pc

%changelog
* Thu Jan 18 2024 Sindhu Karri <lakarri@microsoft.com> - 4.7.0-1
- Upgrade slirp to 4.7.0
- Updated source URL to a generic URL that allows autoupgrades in the future

* Wed Sep 22 2021 Thomas Crain <thcrain@microsoft.com> - 4.6.1-3
- Initial CBL-Mariner import from Fedora 35 (license: MIT)
- Lint spec
- License verified

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 18 2021 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.6.1-1
- new version

* Mon Jun 14 2021 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.6.0-1
- new version

* Wed May 19 2021 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.5.0-1
- new version

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec  2 18:19:30 +04 2020 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.4.0-1
- new version

* Fri Nov 27 20:10:28 +04 2020 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.3.1-3
- Fix CVE-2020-29129 CVE-2020-29130 out-of-bounds access while processing ARP/NCSI packets
  rhbz#1902232

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 08 2020 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.3.1-1
- New v4.3.1 release

* Thu Apr 23 2020 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.3.0-1
- New v4.3.0 release

* Mon Apr 20 2020 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.2.0-2
- CVE-2020-1983 fix

* Tue Mar 17 2020 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.2.0-1
- New v4.2.0 release

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 03 2019 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.1.0-1
- New v4.1.0 release

* Fri Aug  2 2019 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.0.0-3
- Fix CVE-2019-14378, rhbz#1735654

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 22 2019 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.0.0-1
- Initial package, rhbz#1712980
