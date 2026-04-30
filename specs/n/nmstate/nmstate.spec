## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define srcname nmstate
%define libname libnmstate

Name:           nmstate
Version:        2.2.57
Release:        %autorelease
Summary:        Declarative network manager API
License:        Apache-2.0 AND LGPL-2.1-or-later
URL:            https://github.com/%{srcname}/%{srcname}
Source0:        %{url}/releases/download/v%{version}/%{srcname}-%{version}.tar.gz
Source1:        %{url}/releases/download/v%{version}/%{srcname}-%{version}.tar.gz.asc
Source2:        https://nmstate.io/nmstate.gpg
Source3:        %{url}/releases/download/v%{version}/%{srcname}-vendor-%{version}.tar.xz
# Force nmstate-libs upgrade along with nmstate rpm when installed
# https://issues.redhat.com/browse/RHEL-52890
Requires:       (nmstate-libs%{?_isa} = %{version}-%{release} if nmstate-libs)
BuildRequires:  python3-devel
BuildRequires:  gnupg2
BuildRequires:  systemd-devel
BuildRequires:  systemd-rpm-macros
%if 0%{?rhel}
BuildRequires:  rust-toolset
%else
BuildRequires:  rust-packaging
BuildRequires:  (crate(clap/cargo) >= 3.1 with crate(clap/cargo) < 4.0)
BuildRequires:  (crate(clap/default) >= 3.1 with crate(clap/default) < 4.0)
BuildRequires:  (crate(time/std) >= 0.3 with crate(time/std) < 0.4)
BuildRequires:  (crate(time/formatting) >= 0.3 with crate(time/formatting) < 0.4)
BuildRequires:  (crate(time/parsing) >= 0.3 with crate(time/parsing) < 0.4)
BuildRequires:  (crate(env_logger/default) >= 0.11 with crate(env_logger/default) < 0.12)
BuildRequires:  (crate(libc/default) >= 0.2 with crate(libc/default) < 0.3)
BuildRequires:  (crate(log/default) >= 0.4 with crate(log/default) < 0.5)
BuildRequires:  (crate(nispor/default) >= 1.2.27 with crate(nispor/default) < 2.0)
BuildRequires:  (crate(serde/default) >= 1.0 with crate(serde/default) < 2.0)
BuildRequires:  (crate(serde/derive) >= 1.0 with crate(serde/derive) < 2.0)
BuildRequires:  (crate(serde_json/default) >= 1.0 with crate(serde_json/default) < 2.0)
BuildRequires:  (crate(serde_yaml/default) >= 0.9 with crate(serde_yaml/default) < 1.0)
BuildRequires:  (crate(uuid/v4) >= 1.1 with crate(uuid/v4) < 2.0)
BuildRequires:  (crate(uuid/v5) >= 1.1 with crate(uuid/v5) < 2.0)
BuildRequires:  (crate(zbus/default) >= 5.1 with crate(zbus/default) < 6.0)
BuildRequires:  (crate(zvariant/default) >= 5.1 with crate(zvariant/default) < 6.0)
BuildRequires:  (crate(nix/default) >= 0.30 with crate(nix/default) < 0.31)
BuildRequires:  (crate(toml/default) >= 0.9 with crate(toml/default) < 1.0)
BuildRequires:  (crate(tokio/default) >= 1.3 with crate(tokio/default) < 2.0)
BuildRequires:  (crate(tokio/net) >= 1.3 with crate(tokio/net) < 2.0)
BuildRequires:  (crate(tokio/rt) >= 1.3 with crate(tokio/rt) < 2.0)
BuildRequires:  (crate(tokio/signal) >= 1.3 with crate(tokio/signal) < 2.0)
BuildRequires:  (crate(tokio/time) >= 1.3 with crate(tokio/time) < 2.0)
BuildRequires:  (crate(once_cell/default) >= 1.12 with crate(once_cell/default) < 2.0)
%endif

%generate_buildrequires
pushd rust/src/python >/dev/null
%pyproject_buildrequires
popd >/dev/null

%description
Nmstate is a library with an accompanying command line tool that manages host
networking settings in a declarative manner and aimed to satisfy enterprise
needs to manage host networking through a northbound declarative API and multi
provider support on the southbound.


%package libs
Summary:        C binding of nmstate
# Use Recommends for NetworkManager because only access to NM DBus is required,
# but NM could be running on a different host
Recommends:     NetworkManager
# Avoid automatically generated profiles
Recommends:     NetworkManager-config-server
License:        Apache-2.0

%description libs
C binding of nmstate.

%package devel
Summary:        Development files for nmstate
Group:          Development/Libraries
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
License:        Apache-2.0

%description devel
Development files of nmstate C binding.

%package static
Summary:        Static development files for nmstate
Group:          Development/Libraries
License:        Apache-2.0
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static C library bindings for nmstate.

%package -n python3-%{libname}
Summary:        nmstate Python 3 API library
# Use Recommends for NetworkManager because only access to NM DBus is required,
# but NM could be running on a different host
Recommends:     NetworkManager
# Avoid automatically generated profiles
Recommends:     NetworkManager-config-server
Recommends:     (nmstate-plugin-ovsdb if openvswitch)
# Use Suggests for NetworkManager-ovs and NetworkManager-team since it is only
# required for OVS and team support
Suggests:       NetworkManager-ovs
Suggests:       NetworkManager-team
Provides:       nmstate-plugin-ovsdb = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Obsoletes:      nmstate-plugin-ovsdb < 2.0-1
License:        Apache-2.0

%description -n python3-%{libname}
This package contains the Python 3 library for Nmstate.

%if ! 0%{?rhel}
%package -n rust-%{name}-devel
Summary:        Rust crate of nmstate
BuildArch:      noarch
License:        Apache-2.0

%description -n rust-%{name}-devel
This package contains library source intended for building other packages
which use "%{name}" crate.

%package -n rust-%{name}+default-devel
Summary:        Rust crate of nmstate with default feature
BuildArch:      noarch
License:        Apache-2.0

%description -n rust-%{name}+default-devel
This package contains library source intended for building other packages
which use "%{name}" crate with default feature.

%package -n rust-%{name}+gen_conf-devel
Summary:        Rust crate of nmstate with default feature
BuildArch:      noarch
License:        Apache-2.0

%description -n rust-%{name}+gen_conf-devel
This package contains library source intended for building other packages
which use "%{name}" crate with gen_conf feature.

%package -n rust-%{name}+query_apply-devel
Summary:        Rust crate of nmstate with query_apply feature
BuildArch:      noarch
License:        Apache-2.0
# https://bugzilla.redhat.com/show_bug.cgi?id=2161128
Requires:  (crate(nispor/default) >= 1.2.17 with crate(nispor/default) < 2.0)
Requires:  (crate(nix/default) >= 0.26 with crate(nix/default) < 0.27)
Requires:  (crate(zbus/default) >= 5.1 with crate(zbus/default) < 6.0)

%description -n rust-%{name}+query_apply-devel
This package contains library source intended for building other packages
which use "%{name}" crate with query_apply feature.

%package -n rust-%{name}+gen_revert-devel
Summary:        Rust crate of nmstate with gen_revert feature
BuildArch:      noarch
License:        Apache-2.0

%description -n rust-%{name}+gen_revert-devel
This package contains library source intended for building other packages
which use "%{name}" crate with gen_revert feature.
%endif

%prep
gpg2 --import --import-options import-export,import-minimal \
    %{SOURCE2} > ./gpgkey-mantainers.gpg
gpgv2 --keyring ./gpgkey-mantainers.gpg %{SOURCE1} %{SOURCE0}

%autosetup -n %{name}-%{version_no_tilde} -p1 %{?rhel:-a3}

pushd rust
%if 0%{?rhel}
mv ../vendor ./
%cargo_prep -v vendor
%else
%cargo_prep
%endif
popd

%build
pushd rust
%cargo_build
%cargo_license_summary
%{cargo_license} > ../LICENSE.dependencies
%if 0%{?rhel}
%cargo_vendor_manifest
%endif
popd

pushd rust/src/python
%pyproject_wheel
popd

%install
env SKIP_PYTHON_INSTALL=1 \
    PREFIX=%{_prefix} \
    LIBDIR=%{_libdir} \
    SYSCONFDIR=%{_sysconfdir} \
    %make_install

pushd rust/src/python
%pyproject_install
popd

%if ! 0%{?rhel}
pushd rust/src/lib
# Fedora cargo2rpm has problem when working with worksace dependency
#   https://pagure.io/fedora-rust/cargo2rpm/issue/13
# we use `cargo package` to generate the expanded Cargo.toml which
# is also the one used in crates.io
cargo package --frozen --no-verify --target-dir %{_tmppath}
tar xf %{_tmppath}/package/nmstate-%{version}.crate \
  nmstate-%{version}/Cargo.toml
mv nmstate-%{version}/Cargo.toml ./Cargo.toml
# Remove worksapce Cargo.toml
rm ../../Cargo.toml
%cargo_install
popd
%endif

%files
%doc README.md
%license LICENSE.dependencies
%if 0%{?rhel}
%license rust/cargo-vendor.txt
%endif
%doc examples/
%{_mandir}/man8/nmstatectl.8*
%{_mandir}/man8/nmstate-autoconf.8*
%{_mandir}/man8/nmstate.service.8*
%{_bindir}/nmstatectl
%{_bindir}/nmstate-autoconf
%{_unitdir}/nmstate.service
%dir %{_sysconfdir}/%{name}
%{_sysconfdir}/%{name}/README

%files libs
%{_libdir}/libnmstate.so.*

%files devel
%{_libdir}/libnmstate.so
%{_includedir}/nmstate.h
%{_libdir}/pkgconfig/nmstate.pc

%files -n python3-%{libname}
%license LICENSE
%{python3_sitelib}/%{libname}
%{python3_sitelib}/%{srcname}-*.dist-info/

%files static
%{_libdir}/libnmstate.a

%if ! 0%{?rhel}
%files -n rust-%{name}-devel
%license LICENSE
%{cargo_registry}/%{name}-%{version}/

%files -n rust-%{name}+default-devel
%ghost %{cargo_registry}/%{name}-%{version}/Cargo.toml

%files -n rust-%{name}+gen_conf-devel
%ghost %{cargo_registry}/%{name}-%{version}/Cargo.toml

%files -n rust-%{name}+query_apply-devel
%ghost %{cargo_registry}/%{name}-%{version}/Cargo.toml

%files -n rust-%{name}+gen_revert-devel
%ghost %{cargo_registry}/%{name}-%{version}/Cargo.toml
%endif

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 2.2.57-2
- test: add initial lock files

* Tue Dec 09 2025 Gris Ge <fge@redhat.com> - 2.2.57-1
- Merge branch 'rawhide' into f43

* Wed Nov 12 2025 Packit <hello@packit.dev> - 2.2.55-1
- Update to 2.2.55 upstream release
- Resolves: rhbz#2414345

* Mon Oct 20 2025 Packit <hello@packit.dev> - 2.2.54-1
- Update to 2.2.54 upstream release
- Resolves: rhbz#2405107

* Tue Sep 30 2025 Gris Ge <fge@redhat.com> - 2.2.52-2
- Merge remote-tracking branch 'origin/rawhide' into f43

* Thu Sep 18 2025 Gris Ge <fge@redhat.com> - 2.2.52-1
- Merge branch 'rawhide' into f43

* Wed Aug 27 2025 Packit <hello@packit.dev> - 2.2.50-1
- Update to 2.2.50 upstream release
- Resolves: rhbz#2391026

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.2.49-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Aug 01 2025 Packit <hello@packit.dev> - 2.2.49-1
- Update to 2.2.49 upstream release
- Resolves: rhbz#2385933

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.48-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 24 2025 Íñigo Huguet <ihuguet@riseup.net> - 2.2.48-2
- python: use pyproject macros

* Fri Jul 11 2025 Gris Ge <fge@redhat.com> - 2.2.48-1
- Upgrade to 2.2.48

* Fri Jul 11 2025 Gris Ge <fge@redhat.com> - 2.2.47-2
- test: Include error message

* Thu Jul 10 2025 Packit <hello@packit.dev> - 2.2.47-1
- Update to 2.2.47 upstream release
- Resolves: rhbz#2379363

* Mon Jun 23 2025 Packit <hello@packit.dev> - 2.2.46-1
- Update to 2.2.46 upstream release

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 2.2.45-2
- Rebuilt for Python 3.14

* Wed May 28 2025 Packit <hello@packit.dev> - 2.2.45-1
- Update to 2.2.45 upstream release
- Resolves: rhbz#2368875

* Thu Apr 17 2025 Packit <hello@packit.dev> - 2.2.44-1
- Update to 2.2.44 upstream release
- Resolves: rhbz#2354855

* Tue Apr 08 2025 Gris Ge <fge@redhat.com> - 2.2.43-2
- Add notes for bundle update with nispor and rust-netlink

* Wed Apr 02 2025 Gris Ge <fge@redhat.com> - 2.2.43-1
- Upgrade to 2.2.43

* Wed Mar 05 2025 Gris Ge <fge@redhat.com> - 2.2.42-1
- Upgrade to 2.2.42

* Mon Feb 24 2025 Gris Ge <fge@redhat.com> - 2.2.41-2
- Fix rust-nmstate-query_apply-devel dependency

* Mon Feb 24 2025 Gris Ge <fge@redhat.com> - 2.2.41-1
- Upgrade 2.2.41

* Fri Jan 24 2025 Packit <hello@packit.dev> - 2.2.40-1
- Update to 2.2.40 upstream release
- Resolves: rhbz#2341922

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.39-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Nov 29 2024 Gris Ge <fge@redhat.com> - 2.2.39-2
- Upgrade nmstate-libs along with nmstate rpm when installed

* Wed Nov 20 2024 Packit <hello@packit.dev> - 2.2.39-1
- Update to 2.2.39 upstream release
- Resolves: rhbz#2313710

* Sat Aug 24 2024 Gris Ge <fge@redhat.com> - 2.2.35-1
- Upgrade to 2.2.35

* Thu Aug 01 2024 Packit <hello@packit.dev> - 2.2.34-1
- Update to 2.2.34 upstream release
- Resolves: rhbz#2302393

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jun 13 2024 Gris Ge <fge@redhat.com> - 2.2.33-1
- Upgrade to 2.2.33

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.2.26-5
- Rebuilt for Python 3.13

* Mon Mar 25 2024 Gris Ge <fge@redhat.com> - 2.2.26-4
- Fix cargo vendor license file

* Thu Mar 21 2024 Gris Ge <fge@redhat.com> - 2.2.26-3
- patchelf is not required anymore

* Thu Mar 21 2024 Gris Ge <fge@redhat.com> - 2.2.26-2
- Fix ELN build by moving vendor folder to rust folder

* Mon Mar 18 2024 Gris Ge <fge@redhat.com> - 2.2.26-1
- Upgrade to 2.2.26

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 15 2023 Gris Ge <fge@redhat.com> - 2.2.21-1
- Upgrade to 2.2.21

* Wed Sep 06 2023 Gris Ge <fge@redhat.com> - 2.2.15-2
- Use SPDX license for sub-packages

* Fri Aug 25 2023 Packit <hello@packit.dev> - 2.2.15-1
- [packit] 2.2.15 upstream release

* Mon Aug 21 2023 Gris Ge <fge@redhat.com> - 2.2.14-2
- Use SPDX license

* Thu Jul 27 2023 Packit <hello@packit.dev> - 2.2.14-1
- [packit] 2.2.14 upstream release

* Fri Jul 21 2023 Gris Ge <fge@redhat.com> - 2.2.13-1
- Upgrade 2.2.13

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.2.12-3
- Rebuilt for Python 3.12

* Mon Jun 05 2023 Gris Ge <fge@redhat.com> - 2.2.12-2
- New gpg public key and remove unused patches

* Thu Jun 01 2023 Packit <hello@packit.dev> - 2.2.12-1
- [packit] 2.2.12 upstream release

* Tue May 30 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 2.2.10-5
- Use vendored deps for RHEL builds

* Wed May 03 2023 Fabio Valentini <decathorpe@gmail.com> - 2.2.10-4
- Rebuild for tokio crate >= v1.24.2 (RUSTSEC-2023-0005)

* Tue Apr 25 2023 Gris Ge <fge@redhat.com> - 2.2.10-3
- Fix error when DHCP on with auto address on STP enabled bridge

* Sun Apr 23 2023 Gris Ge <fge@redhat.com> - 2.2.10-2
- Auto build once patch from cathay4t merged got dist-git

* Sun Apr 23 2023 Gris Ge <fge@redhat.com> - 2.2.10-1
- Upgrade to 2.2.10

* Thu Mar 23 2023 Gris Ge <fge@redhat.com> - 2.2.9-1
- Upgrade to 2.2.9

* Wed Mar 22 2023 Gris Ge <fge@redhat.com> - 2.2.8-2
- Enable packit

* Sun Mar 12 2023 Gris Ge <fge@redhat.com> - 2.2.8-1
- Upgrade to 2.2.8

* Sun Feb 05 2023 Fabio Valentini <decathorpe@gmail.com> - 2.2.5-3
- Rebuild for fixed frame pointer compiler flags in Rust RPM macros

* Sun Feb 05 2023 Fabio Valentini <decathorpe@gmail.com> - 2.2.5-2
- Fix botched rpmautospec conversion

* Thu Jan 26 2023 Fernando Fernandez Mancera <ffmancera@riseup.net> - 2.2.5-1
- Upgrade to 2.2.5

* Fri Jan 20 2023 Fernando Fernandez Mancera <ffmancera@riseup.net> - 2.2.4-1
- Upgrade to 2.2.4

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023 Gris Ge <fge@redhat.com> - 2.2.3-2
- cargo: Use explicit dependency line for rust-nmstate+query_apply-devel

* Mon Jan 09 2023 Gris Ge <fge@redhat.com> - 2.2.3-1
- Upgrade to 2.2.3

* Sun Dec 18 2022 Gris Ge <fge@redhat.com> - 2.2.2-2
- Fix regression of VRF support

* Thu Dec 15 2022 Gris Ge <fge@redhat.com> - 2.2.2-1
- Upgrade to 2.2.2

* Mon Oct 31 2022 Gris Ge <fge@redhat.com> - 2.2.0-2
- Add feature sub package

* Mon Oct 17 2022 Gris Ge <fge@redhat.com> - 2.2.0-1
- Upgrade to 2.2.0

* Tue Aug 23 2022 Gris Ge <fge@redhat.com> - 2.1.4-2
- Add back the rust-crate sub-rpms

* Tue Aug 23 2022 Gris Ge <fge@redhat.com> - 2.1.4-1
- Upgrade to 2.1.4 and remove rust devel package

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 11 2022 Gris Ge <fge@redhat.com> - 2.1.2-1
- Upgrade to nmstate 2.1.2

* Wed Jun 29 2022 Gris Ge <fge@redhat.com> - 2.1.0-8
- WIP

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 2.1.0-7
- Rebuilt for Python 3.11

* Fri Apr 22 2022 Gris Ge <fge@redhat.com> - 2.1.0-6
- Upgrade to 2.1.0 release

* Tue Apr 19 2022 Gris Ge <fge@redhat.com> - 2.1.0-5
- Add license for -libs and -devel

* Tue Apr 19 2022 Gris Ge <fge@redhat.com> - 2.1.0-4
- The rust CLI does not require libs

* Tue Apr 19 2022 Gris Ge <fge@redhat.com> - 2.1.0-3
- Upgrade to 2.1.0.alpha2

* Wed Apr 13 2022 Gris Ge <fge@redhat.com> - 2.1.0-2
- Change the python binding to noarch

* Wed Apr 13 2022 Gris Ge <fge@redhat.com> - 2.1.0-1
- Upgrade to 2.1.0.alpha1

* Tue Feb 15 2022 Fernando Fernandez Mancera <ffmancera@riseup.net> - 2.0.0-1
- Upgrade to 2.0.0

* Tue Feb 01 2022 Fernando Fernandez Mancera <ffmancera@riseup.net> - 1.2.0-1
- Upgrade to 1.2.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Gris Ge <cnfourt@gmail.com> - 1.1.0-2
- Add varlink service back.

* Tue Jul 27 2021 Gris Ge <cnfourt@gmail.com> - 1.1.0-1
- Upgrade to 1.1.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.0.3-3
- Rebuilt for Python 3.10

* Mon Apr 19 2021 Fernando Fernandez Mancera <ffmancera@riseup.net> - 1.0.3-2
- Fix installation nmstate-varlink.service

* Thu Apr 15 2021 Fernando Fernandez Mancera <ffmancera@riseup.net> - 1.0.3-1
- Upgrade to 1.0.3

* Sun Feb 21 2021 Fernando Fernandez Mancera <ffmancera@riseup.net> - 1.0.2-1
- Upgrade to 1.0.2

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 18 2021 Fernando Fernandez Mancera <ffmancera@riseup.net> - 1.0.1-1
- Upgrade to 1.0.1

* Tue Dec 08 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 1.0.0-1
- Upgrade to 1.0.0

* Thu Oct 22 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.4.1-1
- Upgrade to 0.4.1

* Mon Oct 12 2020 Gris Ge <cnfourt@gmail.com> - 0.4.0-2
- Fix the ELN build by put ovs stuff as soft requirement.

* Sun Sep 20 2020 Gris Ge <cnfourt@gmail.com> - 0.4.0-1
- Upgrade to 0.4.0

* Mon Aug 31 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.3.5-1
- Update to 0.3.5

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 25 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.3.4-1
- Update to 0.3.4

* Thu Jul 02 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.3.3-1
- Update to 0.3.3

* Mon Jun 15 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.3.2-1
- Update to 0.3.2

* Tue Jun 09 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.3.1-1
- Update to 0.3.1

* Tue May 26 2020 Miro Hrončok <miro@hroncok.cz> - 0.3.0-5
- Rebuilt for Python 3.9

* Fri May 08 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.3.0-4
- Fix missing source

* Fri May 08 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.3.0-3
- Fix signature verification

* Fri May 08 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.3.0-2
- Update signature verification

* Fri May 08 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.3.0-1
- Update to 0.3.0

* Tue Apr 21 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.2.10-1
- Update to 0.2.10

* Thu Mar 26 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.2.9-1
- Update to 0.2.9

* Fri Mar 13 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.2.8-1
- Update to 0.2.8

* Wed Mar 04 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.2.7-1
- Update to 0.2.7

* Mon Feb 24 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.2.6-1
- Update to 0.2.6

* Wed Feb 19 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.2.5-1
- Update to 0.2.5

* Wed Feb 12 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.2.4-1
- Update to 0.2.4

* Wed Feb 05 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.2.3-1
- Update to 0.2.3

* Tue Feb 04 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.2.2-1
- Update to 0.2.2

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 13 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.2.1-2
- Fix changelog

* Mon Jan 13 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.2.1-1
- Update to 0.2.1

* Mon Dec 09 2019 Till Maas <opensource@till.name> - 0.2.0-3
- Use ascii-armored keyring

* Tue Dec 03 2019 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.2.0-2
- Fix changelog

* Tue Dec 03 2019 Fernando Fernandez Mancera <ferferna@redhat.com> - 0.2.0-1
- Update to 0.2.0

* Tue Dec 03 2019 Till Maas <opensource@till.name> - 0.1.1-2
- sources: restore GPG key

* Mon Dec 02 2019 Till Maas <opensource@till.name> - 0.1.1-1
- Update to 0.1.1 and sync spec file

* Thu Oct 03 2019 Miro Hrončok <miro@hroncok.cz> - 0.0.8-3
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <miro@hroncok.cz> - 0.0.8-2
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Gris Ge <fge@redhat.com> - 0.0.8-1
- Upgrade to 0.0.8.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 14 2019 Gris Ge <fge@redhat.com> - 0.0.7-2
- Workaround broken dbus-python packaging:
  https://bugzilla.redhat.com/show_bug.cgi?id=1654774

* Fri Jun 14 2019 Gris Ge <fge@redhat.com> - 0.0.7-1
- Upgrade to 0.0.7

* Sun May 05 2019 Gris Ge <fge@redhat.com> - 0.0.6-1
- Upgrade to 0.0.6

* Fri Apr 12 2019 Gris Ge <fge@redhat.com> - 0.0.5-3
- Add missing runtime requirement: python3-dbus

* Wed Mar 20 2019 Gris Ge <fge@redhat.com> - 0.0.5-2
- Enable Fedora CI

* Tue Mar 12 2019 Gris Ge <fge@redhat.com> - 0.0.5-1
- Upgrade to 0.0.5

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 Till Maas <opensource@till.name> - 0.0.4-2
- Sync with upstream spec

* Thu Jan 24 2019 Gris Ge <fge@redhat.com> - 0.0.4-1
- Upgrade to 0.0.4.

* Mon Jan 21 2019 Gris Ge <fge@redhat.com> - 0.0.3-3
- Add missing runtime dependency for nmstatectl.

* Wed Jan 02 2019 Gris Ge <fge@redhat.com> - 0.0.3-2
- Add source file PGP verification.

* Thu Dec 20 2018 Gris Ge <fge@redhat.com> - 0.0.3-1
- Upgrade to 0.0.3.

* Wed Dec 19 2018 Gris Ge <fge@redhat.com> - 0.0.2-2
- Initial import (RHBZ#1654666)

* Thu Sep 18 2025 Gris Ge <fge@redhat.com> - 2.2.52-1
- Upgrade to 2.2.52

* Wed Aug 27 2025 Packit <hello@packit.dev> - 2.2.50-1
- Update to 2.2.50 upstream release
- Resolves: rhbz#2391026

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.2.52-1
- Rebuilt for Python 3.14.0rc3 bytecode

* Tue Dec 09 2025 Gris Ge <fge@redhat.com> - 2.2.57-1
- Upgrade to 2.2.57

* Wed Nov 12 2025 Packit <hello@packit.dev> - 2.2.55-1
- Update to 2.2.55 upstream release
- Resolves: rhbz#2414345

* Mon Oct 20 2025 Packit <hello@packit.dev> - 2.2.54-1
- Update to 2.2.54 upstream release
- Resolves: rhbz#2405107

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.2.52-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Thu Sep 18 2025 Gris Ge <fge@redhat.com> - 2.2.52-1
- Upgrade to 2.2.52

* Wed Aug 27 2025 Packit <hello@packit.dev> - 2.2.50-1
- Update to 2.2.50 upstream release
- Resolves: rhbz#2391026

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.2.49-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Aug 01 2025 Packit <hello@packit.dev> - 2.2.49-1
- Update to 2.2.49 upstream release
- Resolves: rhbz#2385933

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.48-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 24 2025 Íñigo Huguet <ihuguet@riseup.net> - 2.2.48-2
- python: use pyproject macros

* Fri Jul 11 2025 Gris Ge <fge@redhat.com> - 2.2.48-1
- Upgrade to 2.2.48

* Fri Jul 11 2025 Gris Ge <fge@redhat.com> - 2.2.47-2
- test: Include error message

* Thu Jul 10 2025 Packit <hello@packit.dev> - 2.2.47-1
- Update to 2.2.47 upstream release
- Resolves: rhbz#2379363

* Mon Jun 23 2025 Packit <hello@packit.dev> - 2.2.46-1
- Update to 2.2.46 upstream release

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 2.2.45-2
- Rebuilt for Python 3.14

* Wed May 28 2025 Packit <hello@packit.dev> - 2.2.45-1
- Update to 2.2.45 upstream release
- Resolves: rhbz#2368875

* Thu Apr 17 2025 Packit <hello@packit.dev> - 2.2.44-1
- Update to 2.2.44 upstream release
- Resolves: rhbz#2354855

* Tue Apr 08 2025 Gris Ge <fge@redhat.com> - 2.2.43-2
- Add notes for bundle update with nispor and rust-netlink

* Wed Apr 02 2025 Gris Ge <fge@redhat.com> - 2.2.43-1
- Upgrade to 2.2.43

* Wed Mar 05 2025 Gris Ge <fge@redhat.com> - 2.2.42-1
- Upgrade to 2.2.42

* Mon Feb 24 2025 Gris Ge <fge@redhat.com> - 2.2.41-2
- Fix rust-nmstate-query_apply-devel dependency

* Mon Feb 24 2025 Gris Ge <fge@redhat.com> - 2.2.41-1
- Upgrade 2.2.41

* Fri Jan 24 2025 Packit <hello@packit.dev> - 2.2.40-1
- Update to 2.2.40 upstream release
- Resolves: rhbz#2341922

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.39-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Nov 29 2024 Gris Ge <fge@redhat.com> - 2.2.39-2
- Upgrade nmstate-libs along with nmstate rpm when installed

* Wed Nov 20 2024 Packit <hello@packit.dev> - 2.2.39-1
- Update to 2.2.39 upstream release
- Resolves: rhbz#2313710

* Sat Aug 24 2024 Gris Ge <fge@redhat.com> - 2.2.35-1
- Upgrade to 2.2.35

* Thu Aug 01 2024 Packit <hello@packit.dev> - 2.2.34-1
- Update to 2.2.34 upstream release
- Resolves: rhbz#2302393

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jun 13 2024 Gris Ge <fge@redhat.com> - 2.2.33-1
- Upgrade to 2.2.33

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.2.26-5
- Rebuilt for Python 3.13

* Mon Mar 25 2024 Gris Ge <fge@redhat.com> - 2.2.26-4
- Fix cargo vendor license file

* Thu Mar 21 2024 Gris Ge <fge@redhat.com> - 2.2.26-3
- patchelf is not required anymore

* Thu Mar 21 2024 Gris Ge <fge@redhat.com> - 2.2.26-2
- Fix ELN build by moving vendor folder to rust folder

* Mon Mar 18 2024 Gris Ge <fge@redhat.com> - 2.2.26-1
- Upgrade to 2.2.26

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 15 2023 Gris Ge <fge@redhat.com> - 2.2.21-1
- Upgrade to 2.2.21

* Wed Sep 06 2023 Gris Ge <fge@redhat.com> - 2.2.15-2
- Use SPDX license for sub-packages

* Fri Aug 25 2023 Packit <hello@packit.dev> - 2.2.15-1
- [packit] 2.2.15 upstream release

* Mon Aug 21 2023 Gris Ge <fge@redhat.com> - 2.2.14-2
- Use SPDX license

* Thu Jul 27 2023 Packit <hello@packit.dev> - 2.2.14-1
- [packit] 2.2.14 upstream release

* Fri Jul 21 2023 Gris Ge <fge@redhat.com> - 2.2.13-1
- Upgrade 2.2.13

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.2.12-3
- Rebuilt for Python 3.12

* Mon Jun 05 2023 Gris Ge <fge@redhat.com> - 2.2.12-2
- New gpg public key and remove unused patches

* Thu Jun 01 2023 Packit <hello@packit.dev> - 2.2.12-1
- [packit] 2.2.12 upstream release

* Tue May 30 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 2.2.10-5
- Use vendored deps for RHEL builds

* Wed May 03 2023 Fabio Valentini <decathorpe@gmail.com> - 2.2.10-4
- Rebuild for tokio crate >= v1.24.2 (RUSTSEC-2023-0005)

* Tue Apr 25 2023 Gris Ge <fge@redhat.com> - 2.2.10-3
- Fix error when DHCP on with auto address on STP enabled bridge

* Sun Apr 23 2023 Gris Ge <fge@redhat.com> - 2.2.10-2
- Auto build once patch from cathay4t merged got dist-git

* Sun Apr 23 2023 Gris Ge <fge@redhat.com> - 2.2.10-1
- Upgrade to 2.2.10

* Thu Mar 23 2023 Gris Ge <fge@redhat.com> - 2.2.9-1
- Upgrade to 2.2.9

* Wed Mar 22 2023 Gris Ge <fge@redhat.com> - 2.2.8-2
- Enable packit

* Sun Mar 12 2023 Gris Ge <fge@redhat.com> - 2.2.8-1
- Upgrade to 2.2.8

* Sun Feb 05 2023 Fabio Valentini <decathorpe@gmail.com> - 2.2.5-3
- Rebuild for fixed frame pointer compiler flags in Rust RPM macros

* Sun Feb 05 2023 Fabio Valentini <decathorpe@gmail.com> - 2.2.5-2
- Fix botched rpmautospec conversion

* Thu Jan 26 2023 Fernando Fernandez Mancera <ffmancera@riseup.net> - 2.2.5-1
- Upgrade to 2.2.5

* Fri Jan 20 2023 Fernando Fernandez Mancera <ffmancera@riseup.net> - 2.2.4-1
- Upgrade to 2.2.4

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023 Gris Ge <fge@redhat.com> - 2.2.3-2
- cargo: Use explicit dependency line for rust-nmstate+query_apply-devel

* Mon Jan 09 2023 Gris Ge <fge@redhat.com> - 2.2.3-1
- Upgrade to 2.2.3

* Sun Dec 18 2022 Gris Ge <fge@redhat.com> - 2.2.2-2
- Fix regression of VRF support

* Thu Dec 15 2022 Gris Ge <fge@redhat.com> - 2.2.2-1
- Upgrade to 2.2.2

* Mon Oct 31 2022 Gris Ge <fge@redhat.com> - 2.2.0-2
- Add feature sub package

* Mon Oct 17 2022 Gris Ge <fge@redhat.com> - 2.2.0-1
- Upgrade to 2.2.0

* Tue Aug 23 2022 Gris Ge <fge@redhat.com> - 2.1.4-2
- Add back the rust-crate sub-rpms

* Tue Aug 23 2022 Gris Ge <fge@redhat.com> - 2.1.4-1
- Upgrade to 2.1.4 and remove rust devel package

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 11 2022 Gris Ge <fge@redhat.com> - 2.1.2-1
- Upgrade to nmstate 2.1.2

* Wed Jun 29 2022 Gris Ge <fge@redhat.com> - 2.1.0-8
- WIP

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 2.1.0-7
- Rebuilt for Python 3.11

* Fri Apr 22 2022 Gris Ge <fge@redhat.com> - 2.1.0-6
- Upgrade to 2.1.0 release

* Tue Apr 19 2022 Gris Ge <fge@redhat.com> - 2.1.0-5
- Add license for -libs and -devel

* Tue Apr 19 2022 Gris Ge <fge@redhat.com> - 2.1.0-4
- The rust CLI does not require libs

* Tue Apr 19 2022 Gris Ge <fge@redhat.com> - 2.1.0-3
- Upgrade to 2.1.0.alpha2

* Wed Apr 13 2022 Gris Ge <fge@redhat.com> - 2.1.0-2
- Change the python binding to noarch

* Wed Apr 13 2022 Gris Ge <fge@redhat.com> - 2.1.0-1
- Upgrade to 2.1.0.alpha1

* Tue Feb 15 2022 Fernando Fernandez Mancera <ffmancera@riseup.net> - 2.0.0-1
- Upgrade to 2.0.0

* Tue Feb 01 2022 Fernando Fernandez Mancera <ffmancera@riseup.net> - 1.2.0-1
- Upgrade to 1.2.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Gris Ge <cnfourt@gmail.com> - 1.1.0-2
- Add varlink service back.

* Tue Jul 27 2021 Gris Ge <cnfourt@gmail.com> - 1.1.0-1
- Upgrade to 1.1.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.0.3-3
- Rebuilt for Python 3.10

* Mon Apr 19 2021 Fernando Fernandez Mancera <ffmancera@riseup.net> - 1.0.3-2
- Fix installation nmstate-varlink.service

* Thu Apr 15 2021 Fernando Fernandez Mancera <ffmancera@riseup.net> - 1.0.3-1
- Upgrade to 1.0.3

* Sun Feb 21 2021 Fernando Fernandez Mancera <ffmancera@riseup.net> - 1.0.2-1
- Upgrade to 1.0.2

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 18 2021 Fernando Fernandez Mancera <ffmancera@riseup.net> - 1.0.1-1
- Upgrade to 1.0.1

* Tue Dec 08 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 1.0.0-1
- Upgrade to 1.0.0

* Thu Oct 22 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.4.1-1
- Upgrade to 0.4.1

* Mon Oct 12 2020 Gris Ge <cnfourt@gmail.com> - 0.4.0-2
- Fix the ELN build by put ovs stuff as soft requirement.

* Sun Sep 20 2020 Gris Ge <cnfourt@gmail.com> - 0.4.0-1
- Upgrade to 0.4.0

* Mon Aug 31 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.3.5-1
- Update to 0.3.5

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 25 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.3.4-1
- Update to 0.3.4

* Thu Jul 02 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.3.3-1
- Update to 0.3.3

* Mon Jun 15 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.3.2-1
- Update to 0.3.2

* Tue Jun 09 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.3.1-1
- Update to 0.3.1

* Tue May 26 2020 Miro Hrončok <miro@hroncok.cz> - 0.3.0-5
- Rebuilt for Python 3.9

* Fri May 08 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.3.0-4
- Fix missing source

* Fri May 08 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.3.0-3
- Fix signature verification

* Fri May 08 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.3.0-2
- Update signature verification

* Fri May 08 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.3.0-1
- Update to 0.3.0

* Tue Apr 21 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.2.10-1
- Update to 0.2.10

* Thu Mar 26 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.2.9-1
- Update to 0.2.9

* Fri Mar 13 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.2.8-1
- Update to 0.2.8

* Wed Mar 04 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.2.7-1
- Update to 0.2.7

* Mon Feb 24 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.2.6-1
- Update to 0.2.6

* Wed Feb 19 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.2.5-1
- Update to 0.2.5

* Wed Feb 12 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.2.4-1
- Update to 0.2.4

* Wed Feb 05 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.2.3-1
- Update to 0.2.3

* Tue Feb 04 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.2.2-1
- Update to 0.2.2

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 13 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.2.1-2
- Fix changelog

* Mon Jan 13 2020 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.2.1-1
- Update to 0.2.1

* Mon Dec 09 2019 Till Maas <opensource@till.name> - 0.2.0-3
- Use ascii-armored keyring

* Tue Dec 03 2019 Fernando Fernandez Mancera <ffmancera@riseup.net> - 0.2.0-2
- Fix changelog

* Tue Dec 03 2019 Fernando Fernandez Mancera <ferferna@redhat.com> - 0.2.0-1
- Update to 0.2.0

* Tue Dec 03 2019 Till Maas <opensource@till.name> - 0.1.1-2
- sources: restore GPG key

* Mon Dec 02 2019 Till Maas <opensource@till.name> - 0.1.1-1
- Update to 0.1.1 and sync spec file

* Thu Oct 03 2019 Miro Hrončok <miro@hroncok.cz> - 0.0.8-3
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <miro@hroncok.cz> - 0.0.8-2
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Gris Ge <fge@redhat.com> - 0.0.8-1
- Upgrade to 0.0.8.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 14 2019 Gris Ge <fge@redhat.com> - 0.0.7-2
- Workaround broken dbus-python packaging:
  https://bugzilla.redhat.com/show_bug.cgi?id=1654774

* Fri Jun 14 2019 Gris Ge <fge@redhat.com> - 0.0.7-1
- Upgrade to 0.0.7

* Sun May 05 2019 Gris Ge <fge@redhat.com> - 0.0.6-1
- Upgrade to 0.0.6

* Fri Apr 12 2019 Gris Ge <fge@redhat.com> - 0.0.5-3
- Add missing runtime requirement: python3-dbus

* Wed Mar 20 2019 Gris Ge <fge@redhat.com> - 0.0.5-2
- Enable Fedora CI

* Tue Mar 12 2019 Gris Ge <fge@redhat.com> - 0.0.5-1
- Upgrade to 0.0.5

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 Till Maas <opensource@till.name> - 0.0.4-2
- Sync with upstream spec

* Thu Jan 24 2019 Gris Ge <fge@redhat.com> - 0.0.4-1
- Upgrade to 0.0.4.

* Mon Jan 21 2019 Gris Ge <fge@redhat.com> - 0.0.3-3
- Add missing runtime dependency for nmstatectl.

* Wed Jan 02 2019 Gris Ge <fge@redhat.com> - 0.0.3-2
- Add source file PGP verification.

* Thu Dec 20 2018 Gris Ge <fge@redhat.com> - 0.0.3-1
- Upgrade to 0.0.3.

* Wed Dec 19 2018 Gris Ge <fge@redhat.com> - 0.0.2-1
- Initial import (RHBZ#1654666)
## END: Generated by rpmautospec
