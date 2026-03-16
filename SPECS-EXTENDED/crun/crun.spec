%global krun_opts %{nil}
%global wasmedge_opts %{nil}
%global yajl_opts %{nil}

%if %{defined copr_username}
%define copr_build 1
%endif

# krun and wasm support not yet provided in azurelinux
%global yajl_opts --enable-embedded-yajl

Summary:       OCI runtime written in C
Name:          crun
Version:       1.24
Release:       3%{?dist}
Vendor:        Microsoft Corporation
Distribution:  Azure Linux
URL:           https://github.com/containers/%{name}
Source0:       %{url}/releases/download/%{version}/%{name}-%{version}.tar.gz
License:       GPL-2.0-only
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc
BuildRequires: git-core
BuildRequires: gperf
BuildRequires: libcap-devel

%if %{defined krun_support}
BuildRequires: libkrun-devel
%endif

BuildRequires: systemd-devel

%if %{defined system_yajl}
BuildRequires: yajl-devel
%endif

BuildRequires: libseccomp-devel
BuildRequires: python3-libmount
BuildRequires: libtool
BuildRequires: protobuf-c-devel
BuildRequires: criu-devel >= 3.17.1-2
Recommends:    criu >= 3.17.1
Recommends:    criu-libs

%if %{defined wasmedge_support}
BuildRequires: wasmedge-devel
%endif

BuildRequires: python
BuildRequires: glibc-static >= 2.38-18%{?dist}
Provides:      oci-runtime

%description
%{name} is a OCI runtime

%if %{defined krun_support}
%package       krun
Summary:       %{name} with libkrun support
Requires:      libkrun
Requires:      %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:      krun = %{?epoch:%{epoch}:}%{version}-%{release}

%description krun
krun is a symlink to the %{name} binary, with libkrun as an additional dependency.
%endif

%if %{defined wasm_support}
%package wasm
Summary:       %{name} with wasm support
Requires:      %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
# wasm packages are not present on RHEL yet and are currently a PITA to test
# Best to only include wasmedge as weak dep on rhel
%if %{defined fedora}
Requires:      wasm-library
%endif
Recommends:    wasmedge

%description   wasm
%{name}-wasm is a symlink to the %{name} binary, with wasm as an additional dependency.
%endif

%prep
%autosetup -p1 -n %{name}-%{version}

%build
./autogen.sh
./configure --disable-silent-rules %{krun_opts} %{wasmedge_opts} %{yajl_opts}
%make_build

%install
%make_install prefix=%{_prefix}
rm -rf %{buildroot}%{_prefix}/lib*

# Placeholder check to silence rpmlint
%check

%files
%license COPYING
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz

%if %{defined krun_support}
%files krun
%license COPYING
%{_bindir}/krun
%{_mandir}/man1/krun.1.gz
%endif

%if %{defined wasm_support}
%files wasm
%license COPYING
%{_bindir}/%{name}-wasm
%endif

%changelog
* Thu Jan 22 2026 Kanishk Bansal <kanbansal@microsoft.com> - 1.24-3
- Bump to rebuild with updated glibc

* Mon Jan 19 2026 Kanishk Bansal <kanbansal@microsoft.com> - 1.24-2
- Bump to rebuild with updated glibc

* Fri Nov 07 2025 Sandeep Karambelkar <skarambelkar@microsoft.com> - 1.24-1
- Initial Azure Linux import from Fedora 42 (license: MIT).
- Modified for building in azurelinux
- License verified

* Thu Jul 31 2025 Packit <hello@packit.dev> - 1.23.1-1
- Update to 1.23.1 upstream release

* Thu Jul 24 2025 Packit <hello@packit.dev> - 1.23-1
- Update to 1.23 upstream release

* Fri Jun 27 2025 Packit <hello@packit.dev> - 1.22-1
- Update to 1.22 upstream release

* Fri Mar 28 2025 Packit <hello@packit.dev> - 1.21-1
- Update to 1.21 upstream release

* Mon Feb 10 2025 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.20-2
- fix gating config

* Wed Feb 05 2025 Packit <hello@packit.dev> - 1.20-1
- Update to 1.20 upstream release

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 15 2025 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.19.1-3
- TMT: use prepare conditionals

* Thu Dec 26 2024 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.19.1-2
- TMT: sync tests from upstream

* Tue Dec 17 2024 Packit <hello@packit.dev> - 1.19.1-1
- Update to 1.19.1 upstream release

* Fri Dec 06 2024 Packit <hello@packit.dev> - 1.19-1
- Update to 1.19 upstream release

* Thu Oct 31 2024 Packit <hello@packit.dev> - 1.18.2-1
- Update to 1.18.2 upstream release

* Wed Oct 30 2024 Packit <hello@packit.dev> - 1.18.1-1
- Update to 1.18.1 upstream release

* Tue Oct 22 2024 Packit <hello@packit.dev> - 1.18-1
- Update to 1.18 upstream release

* Mon Oct 21 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1.17-3
- Use embedded yajl in RHEL builds

* Thu Sep 26 2024 David Abdurachmanov <davidlt@rivosinc.com> - 1.17-2
- Disable criu support on riscv64

* Tue Sep 10 2024 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.17-1
- bump to 1.17

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu May 02 2024 Packit <hello@packit.dev> - 1.15-1
- Update to 1.15 upstream release

* Wed Mar 27 2024 Lokesh Mandvekar <lsm5@redhat.com> - 1.14.4-5
- wasmedge should stay enabled for official fedora

* Wed Mar 27 2024 Lokesh Mandvekar <lsm5@redhat.com> - 1.14.4-4
- remove eln macro

* Tue Mar 05 2024 Giuseppe Scrivano <gscrivan@redhat.com> - 1.14.4-3
- Revert "Add riscv64 support."
