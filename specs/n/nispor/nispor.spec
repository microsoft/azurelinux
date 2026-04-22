## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 7;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# The check need root privilege hence disabled by default
%bcond_with check

Name:           nispor
Version:        1.2.27
Release:        %autorelease
Summary:        Unified interface for Linux network state querying
License:        Apache-2.0
URL:            https://github.com/nispor/nispor
Source:         https://github.com/nispor/nispor/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://github.com/nispor/nispor/releases/download/v%{version}/nispor-vendor-%{version}.tar.xz
BuildRequires:  make
BuildRequires:  pkg-config
BuildRequires:  python3-devel
BuildRequires:  systemd-devel
BuildRequires:  systemd-rpm-macros
%if 0%{?rhel}
BuildRequires:  rust-toolset
%else
BuildRequires:  rust-packaging
BuildRequires:  (crate(clap/cargo) >= 4.2.0 with crate(clap/cargo) < 5.0)
BuildRequires:  (crate(clap/default) >= 4.2.0 with crate(clap/default) < 5.0)
BuildRequires:  (crate(env_logger/default) >= 0.11 with crate(env_logger/default) < 0.12)
BuildRequires:  (crate(ethtool/default) >= 0.2.8 with crate(ethtool/default) < 0.3)
BuildRequires:  (crate(futures/default) >= 0.3 with crate(futures/default) < 0.4)
BuildRequires:  (crate(libc/default) >= 0.2.126 with crate(libc/default) < 0.3)
BuildRequires:  (crate(log/default) >= 0.4 with crate(log/default) < 0.5)
BuildRequires:  (crate(mptcp-pm/default) >= 0.1.4 with crate(mptcp-pm/default) < 0.2)
BuildRequires:  (crate(rtnetlink/default) >= 0.18.0 with crate(rtnetlink/default) < 0.19)
BuildRequires:  (crate(serde/default) >= 1.0 with crate(serde/default) < 2.0)
BuildRequires:  (crate(serde/derive) >= 1.0 with crate(serde/derive) < 2.0)
BuildRequires:  (crate(serde_json/default) >= 1.0 with crate(serde_json/default) < 2.0)
BuildRequires:  (crate(serde_yaml/default) >= 0.9 with crate(serde_yaml/default) < 0.10)
BuildRequires:  (crate(tokio/macros) >= 1.19 with crate(tokio/macros) < 2.0)
BuildRequires:  (crate(tokio/rt) >= 1.19 with crate(tokio/rt) < 2.0)
BuildRequires:  (crate(wl-nl80211/default) >= 0.3 with crate(wl-nl80211/default) < 0.4)
BuildRequires:  (crate(pretty_assertions/default) >= 1.2 with crate(pretty_assertions/default) < 2)
%endif

%description
Unified interface for Linux network state querying.

%if ! 0%{?rhel}
%package -n     rust-%{name}-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n rust-%{name}-devel

This package contains library source intended for building other packages
which use "%{name}" crate.

%package -n     rust-%{name}+default-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n rust-%{name}+default-devel

This package contains library source intended for building other packages
which use "%{name}" crate with default feature.
%endif

%package -n     python3-%{name}
Summary:        %{summary}
Requires:       nispor = %{?epoch:%{epoch}:}%{version}-%{release}
BuildArch:      noarch

%description -n python3-%{name}

This package contains python3 binding of %{name}.

%package        devel
Summary:        %{summary}
Requires:       nispor%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel

This package contains C binding of %{name}.

%prep
%autosetup -n %{name}-%{version_no_tilde} -p1 %{?rhel:-a1}

%if 0%{?rhel}
%cargo_prep -v vendor
%else
%cargo_prep
%endif

%generate_buildrequires
pushd src/python >/dev/null
%pyproject_buildrequires
popd >/dev/null

%build
%cargo_build
%cargo_license_summary
%{cargo_license} > LICENSE.dependencies
%if 0%{?rhel}
%cargo_vendor_manifest
%endif

pushd src/python
%pyproject_wheel
popd

%install
%if ! 0%{?rhel}
pushd src/lib
# The cargo_isntall does not support workspace:
#   https://pagure.io/fedora-rust/cargo2rpm/issue/5
cargo package --frozen --no-verify --target-dir %{_tmppath}
tar xf %{_tmppath}/package/nispor-%{version}.crate \
  nispor-%{version}/Cargo.toml
mv nispor-%{version}/Cargo.toml ./Cargo.toml
# Remove worksapce Cargo.toml
rm ../../Cargo.toml
%cargo_install
popd
%endif

env SKIP_PYTHON_INSTALL=1 PREFIX=%{_prefix} LIBDIR=%{_libdir} %make_install

pushd src/python
%pyproject_install
popd

%if %{with check}
%check
%cargo_test
%endif

%files
%doc AUTHORS CHANGELOG DEVEL.md README.md
%license LICENSE
%license LICENSE.dependencies
%if 0%{?rhel}
%license cargo-vendor.txt
%endif
%{_bindir}/npc
%{_libdir}/libnispor.so.*

%files -n       python3-%{name}
%license LICENSE
%{python3_sitelib}/nispor*

%files devel
%license LICENSE
%{_libdir}/libnispor.so
%{_includedir}/nispor.h
%{_libdir}/pkgconfig/nispor.pc

%if ! 0%{?rhel}
%files -n       rust-%{name}-devel
%license LICENSE
%{cargo_registry}/%{name}-%{version_no_tilde}/

%files -n       rust-%{name}+default-devel
%ghost %{cargo_registry}/%{name}-%{version_no_tilde}/Cargo.toml
%endif

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 1.2.27-7
- Latest state for nispor

* Thu Sep 18 2025 Gris Ge <fge@redhat.com> - 1.2.27-4
- Add missing dev-dependency

* Thu Sep 18 2025 Gris Ge <fge@redhat.com> - 1.2.27-3
- Use cargo package to generate Cargo.toml

* Thu Sep 18 2025 Gris Ge <fge@redhat.com> - 1.2.27-2
- Fix python and rust sub-package

* Thu Sep 18 2025 Gris Ge <fge@redhat.com> - 1.2.27-1
- Upgrade to 1.2.27

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.2.25-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 26 2025 Packit <hello@packit.dev> - 1.2.25-1
- Update to 1.2.25 upstream release
- Resolves: rhbz#2353166

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.2.24-3
- Rebuilt for Python 3.14

* Wed Apr 02 2025 Gris Ge <fge@redhat.com> - 1.2.24-2
- Fix env_logger dependency

* Wed Apr 02 2025 Gris Ge <fge@redhat.com> - 1.2.24-1
- Upgrade to 1.2.24

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 30 2024 Packit <hello@packit.dev> - 1.2.22-1
- Update to 1.2.22 upstream release
- Resolves: rhbz#2314601

* Fri Oct 18 2024 Gris Ge <fge@redhat.com> - 1.2.21-1
- Upgrade to 1.2.21

* Mon Apr 22 2024 Packit <hello@packit.dev> - 1.2.19-1
- Update to 1.2.19 upstream release
- Resolves: rhbz#2276399

* Tue Mar 19 2024 Packit <hello@packit.dev> - 1.2.18-1
- [packit] 1.2.18 upstream release
- Resolves rhbz#2262486

* Mon Mar 18 2024 Gris Ge <fge@redhat.com> - 1.2.17-1
- Upgrade to 1.2.17

* Fri Feb 02 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1.2.16-4
- Update Rust macro usage

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Dec 23 2023 Packit <hello@packit.dev> - 1.2.16-1
- [packit] 1.2.16 upstream release
- Resolves rhbz#2255700

* Fri Dec 15 2023 Gris Ge <fge@redhat.com> - 1.2.15-2
- Remove unused patch

* Fri Dec 15 2023 Gris Ge <fge@redhat.com> - 1.2.15-1
- Upgrade to 1.2.15

* Mon Sep 04 2023 Gris Ge <fge@redhat.com> - 1.2.12-4
- Enable packit

* Mon Aug 21 2023 Gris Ge <fge@redhat.com> - 1.2.12-3
- Use SPDX license

* Fri Jul 21 2023 Gris Ge <fge@redhat.com> - 1.2.12-2
- Fix build failure on incorrect Makefile version

* Fri Jul 21 2023 Gris Ge <fge@redhat.com> - 1.2.12-1
- Upgrade to 1.2.12

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.2.11-3
- Rebuilt for Python 3.12

* Wed May 24 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.2.11-2
- Use vendored dependencies for RHEL builds

* Wed May 10 2023 Gris Ge <fge@redhat.com> - 1.2.11-1
- Upgrade to 1.2.11

* Wed May 03 2023 Fabio Valentini <decathorpe@gmail.com> - 1.2.10-4
- Rebuild for tokio crate >= v1.24.2 (RUSTSEC-2023-0005)

* Sun Mar 12 2023 Gris Ge <fge@redhat.com> - 1.2.10-3
- Fix %%cargo_install failure

* Sun Mar 12 2023 Gris Ge <fge@redhat.com> - 1.2.10-2
- Fix dependent version of rust-rtnetlink

* Fri Mar 10 2023 Gris Ge <fge@redhat.com> - 1.2.10-1
- Upgrade to 1.2.10

* Sun Feb 05 2023 Fabio Valentini <decathorpe@gmail.com> - 1.2.9-4
- Rebuild for fixed frame pointer compiler flags in Rust RPM macros

* Sun Feb 05 2023 Fabio Valentini <decathorpe@gmail.com> - 1.2.9-3
- Fix botched rpmautospec conversion

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Dec 14 2022 Gris Ge <fge@redhat.com> - 1.2.9-1
- Upgrade to 1.2.9

* Mon Oct 17 2022 Gris Ge <fge@redhat.com> - 1.2.8-1
- Upgrade to 1.2.8

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 06 2022 Gris Ge <fge@redhat.com> - 1.2.7-1
- Upgrade to 1.2.7

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 1.2.5-2
- Rebuilt for Python 3.11

* Tue Apr 12 2022 Gris Ge <fge@redhat.com> - 1.2.5-1
- Upgrade to 1.2.5

* Tue Feb 01 2022 Fernando Fernandez Mancera <ffmancera@riseup.net> - 1.2.3-2
- Add python-setuptools as BuildRequires

* Tue Feb 01 2022 Fernando Fernandez Mancera <ffmancera@riseup.net> - 1.2.3-1
- Upgrade to 1.2.3

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Sep 10 2021 Fernando Fernandez Mancera <ffmancera@riseup.net> - 1.1.1-1
- Upgrade to 1.1.1

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.0.1-5
- Rebuilt for Python 3.10

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.0.1-4
- Rebuilt for updated systemd-rpm-macros

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 07 2021 Tom Stellard <tstellar@redhat.com> - 1.0.1-2
- Add BuildRequires: make

* Tue Nov 10 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 1.0.1-1
- Upgrade to 1.0.1

* Mon Nov 09 2020 Gris Ge <cnfourt@gmail.com> - 1.0.0-3
- Fix iface type of python bonding

* Mon Nov 09 2020 Gris Ge <cnfourt@gmail.com> - 1.0.0-2
- Fix build dependency

* Mon Nov 09 2020 Gris Ge <cnfourt@gmail.com> - 1.0.0-1
- Upgrade to 1.0.0

* Sat Oct 10 2020 Gris Ge <cnfourt@gmail.com> - 0.6.1-2
- Fix incorrect build requirements.

* Sat Oct 10 2020 Gris Ge <cnfourt@gmail.com> - 0.6.1-1
- Upgrade to 0.6.1

* Sun Sep 20 2020 Gris Ge <cnfourt@gmail.com> - 0.5.1-1
- Upgrade to 0.5.1

* Mon Sep 07 2020 Gris Ge <cnfourt@gmail.com> - 0.5.0-2
- Fix the python3-nispor requirement

* Mon Sep 07 2020 Gris Ge <cnfourt@gmail.com> - 0.5.0-1
- Upgrade to 0.5.0
## END: Generated by rpmautospec
