Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:             xdp-tools
Version:          1.4.1
Release:          1%{?dist}
Summary:          Utilities and example programs for use with XDP
%global _soversion 1.4.0

License:          GPL-2.0-only
URL:              https://github.com/xdp-project/%{name}
Source0:          https://github.com/xdp-project/%{name}/releases/download/v%{version}/xdp-tools-%{version}.tar.gz

%global azl 3
# /bin/strip causes errors during install
BuildRequires:    libbpf-devel
BuildRequires:    elfutils-libelf-devel
BuildRequires:    zlib-devel
BuildRequires:    libpcap-devel
BuildRequires:    clang >= 10.0.0
BuildRequires:    llvm >= 10.0.0
BuildRequires:    make
BuildRequires:    gcc
BuildRequires:    pkgconfig
BuildRequires:    m4
# Azlinux does not have emacs. Docs will not be built.
%if !%{azl}
BuildRequires:    emacs-nox
%endif
# Azlinux does not have wireshark, required for tests. Tests will not be run.
%if !%{azl}
BuildRequires:    wireshark-cli
%endif

%ifnarch i686
BuildRequires:    bpftool
%endif

# Always keep xdp-tools and libxdp packages in sync
Requires:         libxdp = %{version}-%{release}

# find-debuginfo produces empty debugsourcefiles.list
# disable the debug package to avoid rpmbuild error'ing out because of this
%global debug_package %{nil}
%global _hardened_build 1
%if %{azl}
%global __strip /bin/true
%endif

%description
Utilities and example programs for use with XDP

%package -n libxdp
Summary:          XDP helper library
License:          LGPL-2.1-only OR BSD-2-Clause
Requires:         kernel-headers

%package -n libxdp-devel
Summary:          Development files for libxdp
License:          LGPL-2.1-only OR BSD-2-Clause
Requires:         kernel-headers
Requires:         libxdp = %{version}-%{release}

%package -n libxdp-static
Summary:          Static library files for libxdp
License:          LGPL-2.1-only OR BSD-2-Clause
Requires:         kernel-headers
Requires:         libxdp-devel = %{version}-%{release}

%description -n libxdp
The libxdp package contains the libxdp library for managing XDP programs,
used by the %{name} package

%description -n libxdp-devel
The libxdp-devel package contains headers used for building XDP programs using
libxdp.

%description -n libxdp-static
The libxdp-static package contains the static library version of libxdp.

%prep
%autosetup -p1 -n %{name}-%{version}


%build
export CFLAGS='%{build_cflags}'
export LDFLAGS='%{build_ldflags}'
export LIBDIR='%{_libdir}'
export RUNDIR='%{_rundir}'
export CLANG=%{_bindir}/clang
export LLC=%{_bindir}/llc
export PRODUCTION=1
export DYNAMIC_LIBXDP=1
export FORCE_SYSTEM_LIBBPF=1
# AzLinux does not build emacs. Docs will not be available
%if %{azl}
export FORCE_EMACS=0
%else
export FORCE_EMACS=1
%endif
./configure
make %{?_smp_mflags} V=1

%install
export DESTDIR='%{buildroot}'
export SBINDIR='%{_sbindir}'
export LIBDIR='%{_libdir}'
export RUNDIR='%{_rundir}'
export MANDIR='%{_mandir}'
export DATADIR='%{_datadir}'
export HDRDIR='%{_includedir}/xdp'
make install V=1

%files
%{_sbindir}/xdp-filter
%{_sbindir}/xdp-loader
%{_sbindir}/xdpdump
%ifnarch i686
%{_sbindir}/xdp-bench
%{_sbindir}/xdp-monitor
%{_sbindir}/xdp-trafficgen
%endif
%{_mandir}/man8/*
%{_libdir}/bpf/xdpfilt_*.o
%{_libdir}/bpf/xdpdump_*.o
%{_datadir}/xdp-tools/
%license LICENSES/*

%files -n libxdp
%{_libdir}/libxdp.so.1
%{_libdir}/libxdp.so.%{_soversion}
%{_libdir}/bpf/xdp-dispatcher.o
%{_libdir}/bpf/xsk_def_xdp_prog*.o
%{_mandir}/man3/*
%license LICENSES/*

%files -n libxdp-static
%{_libdir}/libxdp.a

%files -n libxdp-devel
%{_includedir}/xdp/*.h
%{_libdir}/libxdp.so
%{_libdir}/pkgconfig/libxdp.pc

%changelog
* Mon Jan 29 2024 Kanika Nema <kanikanema@microsoft.com> 1.4.1-2
- Initial CBL-Mariner import from Fedora 40 (License: MIT)
- License Verified
- Azlinux specific changes to turn off tests and docs

* Fri Oct 20 2023 Toke Høiland-Jørgensen <toke@redhat.com> 1.4.1-1
- Upstream version bump

* Wed Aug 9 2023 Toke Høiland-Jørgensen <toke@redhat.com> 1.4.0-3
- Migrated to SPDX format for licenses

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 6 2023 Toke Høiland-Jørgensen <toke@redhat.com> 1.4.0-1
- Upstream version bump

* Thu Feb 23 2023 Toke Høiland-Jørgensen <toke@redhat.com> 1.3.1-1
- Upstream version bump

* Fri Feb 10 2023 Toke Høiland-Jørgensen <toke@redhat.com> 1.3.0-1
- Upstream version bump
- Add patch to enable building without bpftool on i686

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Dec 14 2022 Toke Høiland-Jørgensen <toke@redhat.com> 1.2.9-1
- Upstream version bump

* Thu Nov 03 2022 Jiri Olsa <jolsa@kernel.org> 1.2.8-2
- libbpf 1.0 build

* Sun Sep 18 2022 Toke Høiland-Jørgensen <toke@redhat.com> 1.2.8-1
- Upstream version bump

* Tue Aug 16 2022 Toke Høiland-Jørgensen <toke@redhat.com> 1.2.6-1
- Upstream version bump

* Mon Aug 8 2022 Toke Høiland-Jørgensen <toke@redhat.com> 1.2.5-1
- Upstream version bump

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Feb 17 2022 Toke Høiland-Jørgensen <toke@redhat.com> 1.2.3-1
- Upstream version bump

* Thu Jan 20 2022 Toke Høiland-Jørgensen <toke@redhat.com> 1.2.2-1
- Upstream version bump

* Thu Jan 13 2022 Toke Høiland-Jørgensen <toke@redhat.com> 1.2.1-1
- Upstream version bump

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 7 2021 Toke Høiland-Jørgensen <toke@redhat.com> 1.2.0-1
- Upstream version bump

* Wed Feb 3 2021 Toke Høiland-Jørgensen <toke@redhat.com> 1.1.1-1
- Upstream version bump

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 4 2021 Toke Høiland-Jørgensen <toke@redhat.com> 1.1.0-1
- Upstream version bump

* Thu Aug 20 2020 Toke Høiland-Jørgensen <toke@redhat.com> 1.0.1-1
- Upstream version bump

* Tue Aug 18 2020 Toke Høiland-Jørgensen <toke@redhat.com> 1.0.0-1
- Upstream version bump

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0~beta3-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 15 2020 Eelco Chaudron <echaudro@redhat.com> 1.0.0~beta3-0.1
- Upstream version bump

* Fri Jul 10 2020 Toke Høiland-Jørgensen <toke@redhat.com> 1.0.0~beta2-0.1
- Upstream version bump

* Mon Jun 15 2020 Toke Høiland-Jørgensen <toke@redhat.com> 1.0.0~beta1-0.1
- Upstream version bump

* Mon Apr 6 2020 Toke Høiland-Jørgensen <toke@redhat.com> 0.0.3-1
- Upstream update, add libxdp sub-packages

* Thu Nov 21 2019 Toke Høiland-Jørgensen <toke@redhat.com> 0.0.2-1
- Upstream update

* Fri Nov 8 2019 Toke Høiland-Jørgensen <toke@redhat.com> 0.0.1-1
- Initial release
