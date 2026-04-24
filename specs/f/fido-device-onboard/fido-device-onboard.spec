# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global dracutlibdir %{_prefix}/lib/dracut
%bcond_without check
%global combined_license Apache-2.0 AND (Apache-2.0 OR BSL-1.0) AND (Apache-2.0 OR ISC OR MIT) AND (Apache-2.0 OR MIT) AND ((Apache-2.0 OR MIT) AND BSD-3-Clause) AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND BSD-2-Clause AND BSD-3-Clause AND (CC0-1.0 OR Apache-2.0) AND (CC0-1.0 OR MIT-0 OR Apache-2.0) AND ISC AND MIT AND ((MIT OR Apache-2.0) AND Unicode-DFS-2016) AND (Apache-2.0 OR MIT OR Zlib) AND MPL-2.0 AND (Unlicense OR MIT)

Name:           fido-device-onboard
Version:        0.5.5
Release: 7%{?dist}
Summary:        A rust implementation of the FIDO Device Onboard Specification
License:        BSD-3-Clause

URL:            https://github.com/fdo-rs/fido-device-onboard-rs
Source0:        %{url}/archive/v%{version}/%{name}-rs-%{version}.tar.gz
Source1:        %{name}-rs-%{version}-vendor-patched.tar.xz
Patch1:         0001-use-released-aws-nitro-enclaves-cose-version.patch

# Because nobody cares
ExcludeArch: %{ix86}

%if 0%{?rhel}
BuildRequires:  rust-toolset
%else
BuildRequires:  rust-packaging
%endif
BuildRequires:  clang-devel
BuildRequires:  cryptsetup-devel
BuildRequires:  device-mapper-devel
BuildRequires:  golang
BuildRequires:  openssl-devel >= 3.0.1-12
BuildRequires:  systemd-rpm-macros
BuildRequires:  tpm2-tss-devel
BuildRequires:  sqlite-devel
BuildRequires:  libpq-devel

%description
%{summary}.

%prep

%if 0%{?rhel}
%autosetup -p1 -a1 -n %{name}-rs-%{version}
rm -f Cargo.lock
%if 0%{?rhel} >= 10
%cargo_prep -v vendor
%else
%cargo_prep -V 1
%endif
%endif

%if 0%{?fedora}
%autosetup -p1 -n %{name}-rs-%{version}
%cargo_prep
%generate_buildrequires
%cargo_generate_buildrequires -a
%endif

%build
%cargo_build \
-F openssl-kdf/deny_custom

%{?cargo_license_summary}
%{?cargo_license} > LICENSE.dependencies
%if 0%{?rhel} >= 10
%cargo_vendor_manifest
%endif

%install
install -D -m 0755 -t %{buildroot}%{_libexecdir}/fdo target/release/fdo-client-linuxapp
install -D -m 0755 -t %{buildroot}%{_libexecdir}/fdo target/release/fdo-manufacturing-client
install -D -m 0755 -t %{buildroot}%{_libexecdir}/fdo target/release/fdo-manufacturing-server
install -D -m 0755 -t %{buildroot}%{_libexecdir}/fdo target/release/fdo-owner-onboarding-server
install -D -m 0755 -t %{buildroot}%{_libexecdir}/fdo target/release/fdo-rendezvous-server
install -D -m 0755 -t %{buildroot}%{_libexecdir}/fdo target/release/fdo-serviceinfo-api-server
install -D -m 0755 -t %{buildroot}%{_bindir} target/release/fdo-owner-tool
install -D -m 0755 -t %{buildroot}%{_bindir} target/release/fdo-admin-tool
install -D -m 0644 -t %{buildroot}%{_unitdir} examples/systemd/*
install -D -m 0644 -t %{buildroot}%{_docdir}/fdo examples/config/*
# db sql files
install -D -m 0644 -t %{buildroot}%{_docdir}/fdo/migrations/migrations_manufacturing_server_postgres  migrations/migrations_manufacturing_server_postgres/2023-10-03-152801_create_db/*
install -D -m 0644 -t %{buildroot}%{_docdir}/fdo/migrations/migrations_manufacturing_server_sqlite  migrations/migrations_manufacturing_server_sqlite/2023-10-03-152801_create_db/*
install -D -m 0644 -t %{buildroot}%{_docdir}/fdo/migrations/migrations_owner_onboarding_server_postgres  migrations/migrations_owner_onboarding_server_postgres/2023-10-03-152801_create_db/*
install -D -m 0644 -t %{buildroot}%{_docdir}/fdo/migrations/migrations_owner_onboarding_server_sqlite  migrations/migrations_owner_onboarding_server_sqlite/2023-10-03-152801_create_db/*
install -D -m 0644 -t %{buildroot}%{_docdir}/fdo/migrations/migrations_rendezvous_server_postgres  migrations/migrations_rendezvous_server_postgres/2023-10-03-152801_create_db/*
install -D -m 0644 -t %{buildroot}%{_docdir}/fdo/migrations/migrations_rendezvous_server_sqlite  migrations/migrations_rendezvous_server_sqlite/2023-10-03-152801_create_db/*
# duplicates as needed by AIO command so link them
mkdir -p %{buildroot}%{_bindir}
ln -sr %{buildroot}%{_bindir}/fdo-owner-tool  %{buildroot}%{_libexecdir}/fdo/fdo-owner-tool
ln -sr %{buildroot}%{_bindir}/fdo-admin-tool %{buildroot}%{_libexecdir}/fdo/fdo-admin-tool
# Create directories needed by the various services so we own them
mkdir -p %{buildroot}%{_sysconfdir}/fdo
mkdir -p %{buildroot}%{_sysconfdir}/fdo/keys
mkdir -p %{buildroot}%{_sysconfdir}/fdo/stores
mkdir -p %{buildroot}%{_sysconfdir}/fdo/stores/manufacturer_keys
mkdir -p %{buildroot}%{_sysconfdir}/fdo/stores/manufacturing_sessions
mkdir -p %{buildroot}%{_sysconfdir}/fdo/stores/owner_onboarding_sessions
mkdir -p %{buildroot}%{_sysconfdir}/fdo/stores/owner_vouchers
mkdir -p %{buildroot}%{_sysconfdir}/fdo/stores/rendezvous_registered
mkdir -p %{buildroot}%{_sysconfdir}/fdo/stores/rendezvous_sessions
mkdir -p %{buildroot}%{_sysconfdir}/fdo/stores/serviceinfo_api_devices
mkdir -p %{buildroot}%{_sysconfdir}/fdo/manufacturing-server.conf.d
mkdir -p %{buildroot}%{_sysconfdir}/fdo/owner-onboarding-server.conf.d
mkdir -p %{buildroot}%{_sysconfdir}/fdo/rendezvous-server.conf.d
mkdir -p %{buildroot}%{_sysconfdir}/fdo/serviceinfo-api-server.conf.d
mkdir -p %{buildroot}%{_localstatedir}/lib/fdo
# Dracut manufacturing service
install -D -m 0755 -t %{buildroot}%{dracutlibdir}/modules.d/52fdo dracut/52fdo/module-setup.sh
install -D -m 0755 -t %{buildroot}%{dracutlibdir}/modules.d/52fdo dracut/52fdo/manufacturing-client-generator
install -D -m 0755 -t %{buildroot}%{dracutlibdir}/modules.d/52fdo dracut/52fdo/manufacturing-client-service
install -D -m 0755 -t %{buildroot}%{dracutlibdir}/modules.d/52fdo dracut/52fdo/manufacturing-client.service

%package -n fdo-init
Summary: dracut module for device initialization
License: %combined_license
Requires: openssl-libs >= 3.0.1-12
Requires: dracut
%description -n fdo-init
%{summary}

%files -n fdo-init
%license LICENSE LICENSE.dependencies
%if 0%{?rhel} >= 10
%license cargo-vendor.txt
%endif
%{dracutlibdir}/modules.d/52fdo/
%{_libexecdir}/fdo/fdo-manufacturing-client

%package -n fdo-owner-onboarding-server
Summary: FDO Owner Onboarding Server implementation
License: %combined_license
Requires: openssl-libs >= 3.0.1-12
%description -n fdo-owner-onboarding-server
%{summary}

%files -n fdo-owner-onboarding-server
%license LICENSE LICENSE.dependencies
%if 0%{?rhel} >= 10
%license cargo-vendor.txt
%endif
%dir %{_sysconfdir}/fdo
%dir %{_sysconfdir}/fdo/keys
%dir %{_sysconfdir}/fdo/owner-onboarding-server.conf.d
%dir %{_sysconfdir}/fdo/serviceinfo-api-server.conf.d
%dir %{_sysconfdir}/fdo/stores
%dir %{_sysconfdir}/fdo/stores/owner_onboarding_sessions
%dir %{_sysconfdir}/fdo/stores/owner_vouchers
%dir %{_sysconfdir}/fdo/stores/serviceinfo_api_devices
%{_libexecdir}/fdo/fdo-owner-onboarding-server
%{_libexecdir}/fdo/fdo-serviceinfo-api-server
%dir %{_localstatedir}/lib/fdo
%dir %{_docdir}/fdo
%{_docdir}/fdo/device_specific_serviceinfo.yml
%{_docdir}/fdo/serviceinfo-api-server.yml
%{_docdir}/fdo/owner-onboarding-server.yml
%{_docdir}/fdo/migrations/migrations_owner_onboarding_server_postgres/*
%{_docdir}/fdo/migrations/migrations_owner_onboarding_server_sqlite/*
%{_unitdir}/fdo-serviceinfo-api-server.service
%{_unitdir}/fdo-owner-onboarding-server.service

%post -n fdo-owner-onboarding-server
%systemd_post fdo-owner-onboarding-server.service
%systemd_post fdo-serviceinfo-api-server.service

%preun -n fdo-owner-onboarding-server
%systemd_preun fdo-owner-onboarding-server.service
%systemd_post fdo-serviceinfo-api-server.service

%postun -n fdo-owner-onboarding-server
%systemd_postun_with_restart fdo-owner-onboarding-server.service
%systemd_postun_with_restart fdo-serviceinfo-api-server.service

%package -n fdo-rendezvous-server
Summary: FDO Rendezvous Server implementation
License: %combined_license
%description -n fdo-rendezvous-server
%{summary}

%files -n fdo-rendezvous-server
%license LICENSE LICENSE.dependencies
%if 0%{?rhel} >= 10
%license cargo-vendor.txt
%endif
%dir %{_sysconfdir}/fdo
%dir %{_sysconfdir}/fdo/keys
%dir %{_sysconfdir}/fdo/rendezvous-server.conf.d
%dir %{_sysconfdir}/fdo/stores
%dir %{_sysconfdir}/fdo/stores/rendezvous_registered
%dir %{_sysconfdir}/fdo/stores/rendezvous_sessions
%{_libexecdir}/fdo/fdo-rendezvous-server
%dir %{_localstatedir}/lib/fdo
%dir %{_docdir}/fdo
%{_docdir}/fdo/rendezvous-*.yml
%{_docdir}/fdo/migrations/migrations_rendezvous_server_postgres/*
%{_docdir}/fdo/migrations/migrations_rendezvous_server_sqlite/*
%{_unitdir}/fdo-rendezvous-server.service

%post -n fdo-rendezvous-server
%systemd_post fdo-rendezvous-server.service

%preun -n fdo-rendezvous-server
%systemd_preun fdo-rendezvous-server.service

%postun -n fdo-rendezvous-server
%systemd_postun_with_restart fdo-rendezvous-server.service

%package -n fdo-manufacturing-server
Summary: FDO Manufacturing Server implementation
License: %combined_license
Requires: openssl-libs >= 3.0.1-12
%description -n fdo-manufacturing-server
%{summary}

%files -n fdo-manufacturing-server
%license LICENSE LICENSE.dependencies
%if 0%{?rhel} >= 10
%license cargo-vendor.txt
%endif
%dir %{_sysconfdir}/fdo
%dir %{_sysconfdir}/fdo/keys
%dir %{_sysconfdir}/fdo/manufacturing-server.conf.d
%dir %{_sysconfdir}/fdo/stores
%dir %{_sysconfdir}/fdo/stores/manufacturer_keys
%dir %{_sysconfdir}/fdo/stores/manufacturing_sessions
%dir %{_sysconfdir}/fdo/stores/owner_vouchers
%{_libexecdir}/fdo/fdo-manufacturing-server
%dir %{_localstatedir}/lib/fdo
%dir %{_docdir}/fdo
%{_docdir}/fdo/manufacturing-server.yml
%{_docdir}/fdo/migrations/migrations_manufacturing_server_postgres/*
%{_docdir}/fdo/migrations/migrations_manufacturing_server_sqlite/*
%{_unitdir}/fdo-manufacturing-server.service

%post -n fdo-manufacturing-server
%systemd_post fdo-manufacturing-server.service

%preun -n fdo-manufacturing-server
%systemd_preun fdo-manufacturing-server.service

%postun -n fdo-manufacturing-server
%systemd_postun_with_restart fdo-manufacturing-server.service

%package -n fdo-client
Summary: FDO Client implementation
License: %combined_license
Requires: openssl-libs >= 3.0.1-12
Requires: clevis
Requires: clevis-luks
Requires: clevis-pin-tpm2
Requires: cryptsetup
%description -n fdo-client
%{summary}

%files -n fdo-client
%if 0%{?rhel} >= 10
%license cargo-vendor.txt
%endif
%license LICENSE LICENSE.dependencies
%{_libexecdir}/fdo/fdo-client-linuxapp
%{_unitdir}/fdo-client-linuxapp.service

%post -n fdo-client
%systemd_post fdo-client-linuxapp.service

%preun -n fdo-client
%systemd_preun fdo-client-linuxapp.service

%postun -n fdo-client
%systemd_postun_with_restart fdo-client-linuxapp.service

%package -n fdo-owner-cli
Summary: FDO Owner tools implementation
License: %combined_license
%description -n fdo-owner-cli
%{summary}

%files -n fdo-owner-cli
%if 0%{?rhel} >= 10
%license cargo-vendor.txt
%endif
%license LICENSE LICENSE.dependencies
%{_bindir}/fdo-owner-tool
%{_libexecdir}/fdo/fdo-owner-tool

%package -n fdo-admin-cli
Summary: FDO admin tools implementation
License: %combined_license
Requires: fdo-manufacturing-server = %{version}-%{release}
Requires: fdo-rendezvous-server = %{version}-%{release}
Requires: fdo-owner-onboarding-server = %{version}-%{release}
Requires: fdo-owner-cli = %{version}-%{release}
Requires: fdo-client = %{version}-%{release}
Requires: fdo-init = %{version}-%{release}
%description -n fdo-admin-cli
%{summary}

%files -n fdo-admin-cli
%if 0%{?rhel} >= 10
%license cargo-vendor.txt
%endif
%license LICENSE LICENSE.dependencies
%dir %{_sysconfdir}/fdo
%dir %{_sysconfdir}/fdo/keys
%{_bindir}/fdo-admin-tool
%{_libexecdir}/fdo/fdo-admin-tool
%{_unitdir}/fdo-aio.service

%post -n fdo-admin-cli
%systemd_post fdo-aio.service

%preun -n fdo-admin-cli
%systemd_preun fdo-aio.service

%postun -n fdo-admin-cli
%systemd_postun_with_restart fdo-aio.service

%changelog
* Mon Feb 02 2026 Maxwell G <maxwell@gtmx.me> - 0.5.5-6
- Rebuild for https://fedoraproject.org/wiki/Changes/golang1.26

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Oct 10 2025 Maxwell G <maxwell@gtmx.me> - 0.5.5-4
- Rebuild for golang 1.25.2

* Fri Aug 15 2025 Maxwell G <maxwell@gtmx.me> - 0.5.5-3
- Rebuild for golang-1.25.0

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed May 28 2025 Packit <hello@packit.dev> - 0.5.5-1
## What's Changed
 * chore: bump openssl from 0.10.70 to 0.10.72 by @dependabot in https://github.com/fdo-rs/fido-device-onboard-rs/pull/758
 * fix: replace default.target with initrd.target by @lbrabec in https://github.com/fdo-rs/fido-device-onboard-rs/pull/762
 * ci(mergify): upgrade configuration to current format by @mergify in https://github.com/fdo-rs/fido-device-onboard-rs/pull/766
 * chore: bump tokio from 1.36.0 to 1.45.1 by @dependabot in https://github.com/fdo-rs/fido-device-onboard-rs/pull/769
 * chore: bump actions/upload-artifact from 3 to 4 by @dependabot in https://github.com/fdo-rs/fido-device-onboard-rs/pull/593
 * chore: bump actions/checkout from 3 to 4 by @dependabot in https://github.com/fdo-rs/fido-device-onboard-rs/pull/551
 * chore: bump regex from 1.10.3 to 1.11.1 by @dependabot in https://github.com/fdo-rs/fido-device-onboard-rs/pull/752
 * chore: bump tss-esapi crate to 7.6 by @nullr0ute in https://github.com/fdo-rs/fido-device-onboard-rs/pull/772
 * chore: fix the container deps by @nullr0ute in https://github.com/fdo-rs/fido-device-onboard-rs/pull/775
 * chore: bump for 0.5.5 release by @pcdubs in https://github.com/fdo-rs/fido-device-onboard-rs/pull/771

## New Contributors
 * @lbrabec made their first contribution in https://github.com/fdo-rs/fido-device-onboard-rs/pull/762
 * @mergify made their first contribution in https://github.com/fdo-rs/fido-device-onboard-rs/pull/766

 **Full Changelog**: https://github.com/fdo-rs/fido-device-onboard-rs/compare/v0.5.4...v0.5.5
- Resolves: rhbz#2369025

* Fri Mar 28 2025 Packit <hello@packit.dev> - 0.5.4-1
## What's Changed
 * packit: drop centos propose downstream and jobs by @runcom in https://github.com/fdo-rs/fido-device-onboard-rs/pull/743
 * fix: packit: bring back pkg_tool centpkg by @runcom in https://github.com/fdo-rs/fido-device-onboard-rs/pull/744
 * Makefile tarball targets by @mmartinv in https://github.com/fdo-rs/fido-device-onboard-rs/pull/745
 * chore: describe how to release a new version by @mmartinv in https://github.com/fdo-rs/fido-device-onboard-rs/pull/746
 * chore: allow libcryptsetup-rs >= 0.11.2 by @mmartinv in https://github.com/fdo-rs/fido-device-onboard-rs/pull/739
 * chore: bump diesel from 2.2.3 to 2.2.7 by @dependabot in https://github.com/fdo-rs/fido-device-onboard-rs/pull/728
 * Update to latest version of aws-nitro-enclaves-cose by @mmartinv in https://github.com/fdo-rs/fido-device-onboard-rs/pull/724
 * chore: bump reqwest from 0.12.7 to 0.12.9 by @dependabot in https://github.com/fdo-rs/fido-device-onboard-rs/pull/751
 * chore: bump ring from 0.17.8 to 0.17.13 by @dependabot in https://github.com/fdo-rs/fido-device-onboard-rs/pull/754
 * chore: bump futures from 0.3.30 to 0.3.31 by @dependabot in https://github.com/fdo-rs/fido-device-onboard-rs/pull/753
 * chore: prepare 0.5.4 release by @nullr0ute in https://github.com/fdo-rs/fido-device-onboard-rs/pull/757


 **Full Changelog**: https://github.com/fdo-rs/fido-device-onboard-rs/compare/v0.5.3...v0.5.4

* Fri Feb 07 2025 Packit <hello@packit.dev> - 0.5.3-1
## What's Changed
 * chore: update CONTRIBUTING with additional deps by @miabbott in https://github.com/fdo-rs/fido-device-onboard-rs/pull/721
 * Fix the aws-nitro-enclaves patches and serveral problems reported by clippy by @mmartinv in https://github.com/fdo-rs/fido-device-onboard-rs/pull/722
 * New makefile targets by @mmartinv in https://github.com/fdo-rs/fido-device-onboard-rs/pull/725
 * Packit changes by @mmartinv in https://github.com/fdo-rs/fido-device-onboard-rs/pull/726
 * chore: bump openssl from 0.10.66 to 0.10.70 by @dependabot in https://github.com/fdo-rs/fido-device-onboard-rs/pull/733
 * chore: bump for 0.5.3 release by @mmartinv in https://github.com/fdo-rs/fido-device-onboard-rs/pull/738


 **Full Changelog**: https://github.com/fdo-rs/fido-device-onboard-rs/compare/v0.5.2...v0.5.3
- Resolves: rhbz#2336848

* Thu Feb 06 2025 Fabio Valentini <decathorpe@gmail.com> - 0.5.1-3
- Rebuild for openssl crate >= v0.10.70 (RUSTSEC-2025-0004)

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Nov 26 2024 Antonio Murdaca <amurdaca@redhat.com> - 0.5.1-1
## What's Changed
 * chore: update patch for new release by @nullr0ute in https://github.com/fdo-rs/fido-device-onboard-rs/pull/625
 * chore: fix require error with commitlint by @miabbott in https://github.com/fdo-rs/fido-device-onboard-rs/pull/636
 * fix(license): replace space with - in Apache 2.0 by @7flying in https://github.com/fdo-rs/fido-device-onboard-rs/pull/632
 * fix(data-formats): use serde_tuple serializer for error messages by @mmartinv in https://github.com/fdo-rs/fido-device-onboard-rs/pull/629
 * fix: cargo test for non-root users by @mmartinv in https://github.com/fdo-rs/fido-device-onboard-rs/pull/635
 * fix(get_current_user_name): remove trailing whitespaces. by @mmartinv in https://github.com/fdo-rs/fido-device-onboard-rs/pull/638
 * chore: bump mio from 0.8.10 to 0.8.11 by @dependabot in https://github.com/fdo-rs/fido-device-onboard-rs/pull/640
 * fix: vendored tarfile creation by @mmartinv in https://github.com/fdo-rs/fido-device-onboard-rs/pull/634
 * fix: static-mut-refs warning by @7flying in https://github.com/fdo-rs/fido-device-onboard-rs/pull/651
 * Enable CentOS 9 builds and add Testing Farm e2e tests by @mmartinv in https://github.com/fdo-rs/fido-device-onboard-rs/pull/650
 * Add an OV re-registration window option when using DB storage by @7flying in https://github.com/fdo-rs/fido-device-onboard-rs/pull/643
 * chore: bump pem from 2.0.1 to 3.0.3 by @dependabot in https://github.com/fdo-rs/fido-device-onboard-rs/pull/639
 * chore: bump h2 from 0.3.25 to 0.3.26 by @dependabot in https://github.com/fdo-rs/fido-device-onboard-rs/pull/659
 * feat: verify trusted manufacturers by @mmartinv in https://github.com/fdo-rs/fido-device-onboard-rs/pull/656
 * database enhancements by @runcom in https://github.com/fdo-rs/fido-device-onboard-rs/pull/666
 * chore: bump openssl to 0.10.66 by @7flying in https://github.com/fdo-rs/fido-device-onboard-rs/pull/664
 * chore(store): make the store OVs agnostic by @runcom in https://github.com/fdo-rs/fido-device-onboard-rs/pull/671
 * feat(manufacturing-server): implement an export OVs endpoint  by @runcom in https://github.com/fdo-rs/fido-device-onboard-rs/pull/673
 * fix(systemd-units): run before powering off the system by @mmartinv in https://github.com/fdo-rs/fido-device-onboard-rs/pull/676
 * fix(dracut): use isolate on error in the manufacturing-client service by @mmartinv in https://github.com/fdo-rs/fido-device-onboard-rs/pull/678
 * fix(systemd-generator): write configuration to '/run' by @mmartinv in https://github.com/fdo-rs/fido-device-onboard-rs/pull/677
 * fix(owner-tool): use the new API to export ovs by @runcom in https://github.com/fdo-rs/fido-device-onboard-rs/pull/675
 * chore: update diesel to 2.2.3 by @7flying in https://github.com/fdo-rs/fido-device-onboard-rs/pull/669
 * chore: bump reqwest from 0.11.27 to 0.12.7 by @dependabot in https://github.com/fdo-rs/fido-device-onboard-rs/pull/683
 * fix: use centos-stream-9 target instead of epel-9 by @mmartinv in https://github.com/fdo-rs/fido-device-onboard-rs/pull/687
 * enhance onboarding testing by @mmartinv in https://github.com/fdo-rs/fido-device-onboard-rs/pull/681
 * ci: add konflux test cases by @yih-redhat in https://github.com/fdo-rs/fido-device-onboard-rs/pull/688
 * fix(make-vendored-tarfile.sh): exclude idna tests with unicode points by @runcom in https://github.com/fdo-rs/fido-device-onboard-rs/pull/692
 * chore: bump for 0.5.1 by @runcom in https://github.com/fdo-rs/fido-device-onboard-rs/pull/693

## New Contributors
 * @miabbott made their first contribution in https://github.com/fdo-rs/fido-device-onboard-rs/pull/636
 * @yih-redhat made their first contribution in https://github.com/fdo-rs/fido-device-onboard-rs/pull/688

 **Full Changelog**: https://github.com/fdo-rs/fido-device-onboard-rs/compare/v0.5.0...v0.5.1
- Resolves: rhbz#2328690

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 20 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 0.5.0-1
- Update to 0.5.0

* Mon Feb 12 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 0.4.13-1
- Update to 0.4.13

* Sun Feb 11 2024 Maxwell G <maxwell@gtmx.me> - 0.4.12-10
- Rebuild for golang 1.22.0

* Sun Feb 04 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 0.4.12-9
- Update Rust macro usage

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 26 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 0.4.12-1
- Update to 0.4.12

* Mon Jul 03 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 0.4.11-1
- Update to 0.4.11

* Mon Jul 03 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 0.4.10-2
- Updates for eln/c9s building

* Fri Jun 23 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 0.4.10-1
- Update to 0.4.10

* Wed Jun 14 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 0.4.9-5
- More spec updates

* Wed Jun 14 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 0.4.9-4
- Add patch for libcryptsetup-rs 0.8 API changes

* Tue Jun 13 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 0.4.9-3
- Updates for licenses

* Tue May 30 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 0.4.9-2
- Review feedback
- Patch for libcryptsetup-rs 0.7

* Thu May 11 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 0.4.9-1
- Update to 0.4.9

* Mon Feb 20 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 0.4.7-3
- Fix services start

* Wed Feb 15 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 0.4.7-2
- Upstream fix for rhbz#2168089

* Wed Nov 30 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 0.4.7-1
- Update to 0.4.7
- Package updates and cleanup

* Tue Mar 29 2022 Antonio Murdaca <runcom@linux.com> - 0.4.5-1
- bump to 0.4.5

* Mon Feb 28 2022 Antonio Murdaca <runcom@linux.com> - 0.4.0-2
- fix runtime requirements to use openssl-libs and not -devel

* Thu Feb 24 2022 Antonio Murdaca <runcom@linux.com> - 0.4.0-1
- upgrade to 0.4.0

* Tue Feb 01 2022 Antonio Murdaca <runcom@linux.com> - 0.3.0-1
- bump to 0.3.0

* Tue Jan 11 2022 Antonio Murdaca <runcom@linux.com> - 0.2.0-2
- use patched vendor w/o win files and rename license

* Mon Dec 13 2021 Antonio Murdaca <runcom@linux.com> - 0.2.0-1
- import fido-device-onboard
