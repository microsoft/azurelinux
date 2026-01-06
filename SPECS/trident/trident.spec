# This spec file is used for both the Trident repo builds and as the
# basis for the azurelinux build. For the Trident repo builds, `rpm_ver`
# is defined, dictating the build version. If `rpm_ver` is undefined,
# the spec defines the azurelinux distro build (using source and vendor
# tarballs, etc)

%global selinuxtype targeted

Summary:        Declarative, security-first OS lifecycle agent designed primarily for Azure Linux
Name:           trident
%if %{undefined rpm_ver}
Version:        0.20.0
Release:        1%{?dist}
%else
Version:        %{rpm_ver}
Release:        %{rpm_rel}%{?dist}
%endif
License:        MIT
Vendor:         Microsoft Corporation
Group:          Applications/System
Distribution:   Azure Linux

%if %{undefined rpm_ver}
URL:            https://github.com/microsoft/trident/
Source0:        https://github.com/microsoft/trident/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# Note: the %%{name}-%%{version}-cargo.tar.gz file contains a cache created by capturing the contents downloaded into $CARGO_HOME.
# To update the cache and config.toml run:
#   tar -xf %%{name}-%%{version}.tar.gz
#   cd %%{name}-%%{version}
#   cargo vendor > config.toml
#   tar -czf %%{name}-%%{version}-cargo.tar.gz vendor/
#
Source1:        %{name}-%{version}-cargo.tar.gz

BuildRequires:  cargo >= 1.85.0
Requires:       azurelinux-image-tools-osmodifier
%else
Source2:        osmodifier
%endif

BuildRequires:  rust >= 1.85.0
BuildRequires:  openssl-devel
BuildRequires:  systemd-units

Requires:       e2fsprogs
Requires:       util-linux
Requires:       dosfstools
Requires:       efibootmgr
Requires:       lsof
Requires:       systemd >= 255
Requires:       systemd-udev
Requires:       (%{name}-selinux if selinux-policy-%{selinuxtype})

# Optional dependencies for various optional features

# For network configuration (os.network, managementOs.network)
Suggests:       netplan        
# For RAID support (storage.raid)
Suggests:       mdadm          
# For encryption support (storage.encryption)
Suggests:       tpm2-tools     
Suggests:       cryptsetup
# For integrity support (storage.verity)     
Suggests:       veritysetup
# For mounting NTFS filesystems
Suggests:       ntfs-3g
# For creating NTFS filesystems
Suggests:       ntfsprogs


%description
Trident. This package provides the Trident tool
and its dependencies for managing the lifecycle of Azure Linux hosts.

%files
%{_bindir}/%{name}
%dir /etc/%{name}
%{_bindir}/osmodifier

# ------------------------------------------------------------------------------

%package provisioning
Summary:        Trident files for the provisioning OS
Requires:       %{name}

%description provisioning
Trident files for the provisioning OS

%files provisioning
%{_unitdir}/%{name}-network.service

%post provisioning
%systemd_post %{name}-network.service

%preun provisioning
%systemd_preun %{name}-network.service

%postun provisioning
%systemd_postun_with_restart %{name}-network.service

# ------------------------------------------------------------------------------

%package service
Summary:        Trident files for SystemD update and commit services
Requires:       %{name}
Conflicts:      %{name}-install-service

%description service
Trident files for SystemD update and commit services

%files service
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}-update.service

%post service
%systemd_post %{name}.service
%systemd_post %{name}-update.service

%preun service
%systemd_preun %{name}.service
%systemd_preun %{name}-update.service

%postun service
%systemd_postun_with_restart %{name}.service
%systemd_postun_with_restart %{name}-update.service

# ------------------------------------------------------------------------------

%package install-service
Summary:        Trident files for SystemD install service
Requires:       %{name}
Conflicts:      %{name}-service

%description install-service
Trident files for SystemD install service

%files install-service
%{_unitdir}/%{name}-install.service

%post install-service
%systemd_post %{name}-install.service

%preun install-service
%systemd_preun %{name}-install.service

%postun install-service
%systemd_postun_with_restart %{name}-install.service

# ------------------------------------------------------------------------------

%package update-poll
Summary:        Trident files for SystemD service
Requires:       %{name}
Requires:       %{name}-service

%description update-poll
SystemD timer for update polling with Harpoon.

%files update-poll
%{_unitdir}/%{name}-update.timer

%post update-poll
%systemd_post %{name}-update.timer

%preun update-poll
%systemd_preun %{name}-update.timer

%postun update-poll
%systemd_postun_with_restart %{name}-update.timer

# ------------------------------------------------------------------------------

%package selinux
Summary:             Trident SELinux policy
BuildArch:           noarch
Requires:            selinux-policy-%{selinuxtype}
Requires(post):      selinux-policy-%{selinuxtype}
BuildRequires:       selinux-policy-devel
%{?selinux_requires}

%description selinux
Custom SELinux policy module

%files selinux
%{_datadir}/selinux/packages/%{selinuxtype}/%{name}.pp.bz2
%{_datadir}/selinux/devel/include/distributed/%{name}.if
%ghost %verify(not md5 size mode mtime) %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{name}

# SELinux contexts are saved so that only affected files can be
# relabeled after the policy module installation
%pre selinux
%selinux_relabel_pre -s %{selinuxtype}

%post selinux
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{name}.pp.bz2

%postun selinux
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{name}
fi

%posttrans selinux
%selinux_relabel_post -s %{selinuxtype}

# ------------------------------------------------------------------------------

%package static-pcrlock-files
Summary:        Statically defined .pcrlock files
Requires:       %{name}

%description static-pcrlock-files
Statically defined .pcrlock files for PCR-based encryption. This is a workaround needed because AZL
3.0 fails to provide these files inside the same package as the systemd-pcrlock binary; this should
be removed once the fix is merged in AZL 4.0.

%files static-pcrlock-files
%{_sharedstatedir}/pcrlock.d

# ------------------------------------------------------------------------------

%if %{undefined rpm_ver}
%prep
%autosetup -n %{name}-%{version} -p1

# Do vendor expansion here manually by
# calling `tar x` and setting up
# .cargo/config to use it.
tar fx %{SOURCE1}
mkdir -p .cargo

cat >.cargo/config << EOF
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF
%endif

%build
export TRIDENT_VERSION="%{trident_version}"
cargo build --release

mkdir selinux
cp -p packaging/selinux-policy-trident/trident.fc selinux/
cp -p packaging/selinux-policy-trident/trident.if selinux/
cp -p packaging/selinux-policy-trident/trident.te selinux/

make -f %{_datadir}/selinux/devel/Makefile %{name}.pp
bzip2 -9 %{name}.pp

%check
test "$(./target/release/trident --version)" = "trident %{trident_version}"

%install
%if %{undefined rpm_ver}
install -D -m 755 osmodifier %{buildroot}%{_bindir}/osmodifier
%else
install -D -m 755 %{SOURCE2} %{buildroot}%{_bindir}/osmodifier
%endif
install -D -m 755 target/release/%{name} %{buildroot}/%{_bindir}/%{name}

# Copy Trident SELinux policy module to /usr/share/selinux/packages
install -D -m 0644 %{name}.pp.bz2 %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype}/%{name}.pp.bz2
install -D -p -m 0644 selinux/%{name}.if %{buildroot}%{_datadir}/selinux/devel/include/distributed/%{name}.if

mkdir -p %{buildroot}%{_unitdir}
install -D -m 644 packaging/systemd/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 packaging/systemd/%{name}-install.service %{buildroot}%{_unitdir}/%{name}-install.service
install -D -m 644 packaging/systemd/%{name}-update.service %{buildroot}%{_unitdir}/%{name}-update.service
install -D -m 644 packaging/systemd/%{name}-network.service %{buildroot}%{_unitdir}/%{name}-network.service
install -D -m 644 packaging/systemd/%{name}-update.timer %{buildroot}%{_unitdir}/%{name}-update.timer

mkdir -p %{buildroot}/etc/%{name}

# Copy statically defined .pcrlock files into /var/lib/pcrlock.d
pcrlockroot="%{buildroot}%{_sharedstatedir}/pcrlock.d"
mkdir -p "$pcrlockroot"
(
  cd packaging/static-pcrlock-files
  find . -type f -print0 | while IFS= read -r -d '' f; do
      mkdir -p "$pcrlockroot/$(dirname "$f")"
      install -m 644 "$f" "$pcrlockroot/$f"
  done
)

%changelog
* Mon Jan 5 2026 Brian Fjeldstad <bfjelds@microsoft.com> 0.20.0-1
- Original version for Azure Linux (license: MIT).
- License verified.
