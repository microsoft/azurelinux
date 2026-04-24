# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global libseat_sover   1
%global _hardened_build 1

%bcond_without  server

Name:           seatd
Version:        0.9.2
Release: 3%{?dist}
Summary:        Minimal seat management daemon

License:        MIT
URL:            https://sr.ht/~kennylevinsen/seatd/
Source0:        https://git.sr.ht/~kennylevinsen/seatd/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        seatd.sysusers

BuildRequires:  gcc
BuildRequires:  meson >= 0.60.0

BuildRequires:  pkgconfig(libsystemd)
%if %{with server}
BuildRequires:  pkgconfig(scdoc)
BuildRequires:  systemd-rpm-macros
%endif


%description
A seat management daemon, that does everything it needs to do.
Nothing more, nothing less. Depends only on libc.


%package -n     libseat
Summary:        Universal seat management library

%description -n libseat
A seat management library allowing applications to use whatever seat
management is available.

Supports:
 * seatd
 * (e)logind
 * embedded seatd for standalone operation

Each backend can be compile-time included and is runtime auto-detected or
manually selected with the LIBSEAT_BACKEND environment variable.

Which backend is in use is transparent to the application, providing a
simple common interface.


%package -n     libseat-devel
Summary:        Development files for libseat
Requires:       libseat%{?_isa} = %{version}-%{release}

%description -n libseat-devel
The libseat-devel package contains libraries and header files for
developing applications that use libseat.


%prep
%autosetup


%build
%meson \
    -Dlibseat-logind=systemd \
    -Dserver=%[%{with server}?"enabled":"disabled"]
%meson_build


%install
%meson_install

%if %{with server}
install -D -m 0644 -pv contrib/systemd/%{name}.service \
    %{buildroot}%{_unitdir}/%{name}.service
install -D -m 0644 -pv %{SOURCE1} \
    %{buildroot}%{_sysusersdir}/%{name}.conf
%endif


%check
%meson_test


%if %{with server}
%pre
%sysusers_create_compat %{SOURCE1}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
# TODO: seatd-launch should run with elevated privileges, i.e. SUID or CAP_SETUID
%{_bindir}/%{name}-launch
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}-launch.1*
%{_sysusersdir}/%{name}.conf
%{_unitdir}/%{name}.service
%endif

%files -n libseat
%license LICENSE
%doc README.md
%{_libdir}/libseat.so.%{libseat_sover}

%files -n libseat-devel
%{_includedir}/libseat.h
%{_libdir}/libseat.so
%{_libdir}/pkgconfig/libseat.pc


%changelog
* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Jan 07 2026 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.9.2-1
- Update to 0.9.2 (#2427130)

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Oct 30 2024 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.9.1-1
- Update to 0.9.1 (rhbz#2322864)

* Tue Oct 22 2024 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.9.0-1
- Update to 0.9.0

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.8.0-1
- Update to 0.8.0 (#2223943)

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 30 2023 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.7.0-4
- Build seatd server

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 23 2022 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.7.0-1
- Update to 0.7.0 (#2089517)

* Mon Feb 21 2022 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.6.4-1
- Update to 0.6.4 (#2056723)

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Oct 19 2021 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.6.3-1
- Update to 0.6.3 (#2015692)

* Fri Sep 17 2021 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.6.2-1
- Update to 0.6.2
- Server: create `seat` group for controlling seatd access

* Sat Sep 11 2021 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.6.0-1
- Update to 0.6.0
- Enable libseat-seatd backend in the default build

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Apr 14 2021 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.5.0-1
- Initial import (#1949358)
