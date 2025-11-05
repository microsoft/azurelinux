Name:		 mlnx-ethtool
Version:	 6.9
Release:	 4%{?dist}
Group:		 Utilities
Summary:	 Settings tool for Ethernet and other network devices
License:	 GPLv2
Vendor:          Microsoft Corporation
Distribution:    Azure Linux
URL:		 https://ftp.kernel.org/pub/software/network/ethtool/
Buildroot:	 /var/tmp/%{name}-%{version}-build
Source0:         https://linux.mellanox.com/public/repo/mlnx_ofed/24.10-0.7.0.0/SRPMS/mlnx-ethtool-6.9.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  libmnl-devel

%description
This utility allows querying and changing settings such as speed,
port, auto-negotiation, PCI locations and checksum offload on many
network devices, especially Ethernet devices.

%prep
%setup -q


%build
CFLAGS="${RPM_OPT_FLAGS}" ./configure --prefix=%{_prefix} --mandir=%{_mandir}
make


%install
make install DESTDIR=${RPM_BUILD_ROOT}


# --- Rename conflicting assets ---
# Binary: move from ethtool -> mlnx-ethtool
if [ -f "%{buildroot}%{_sbindir}/ethtool" ]; then
    mv "%{buildroot}%{_sbindir}/ethtool" \
       "%{buildroot}%{_sbindir}/mlnx-ethtool"
fi

# Manpage: normalize and rename to mlnx-ethtool.8.gz
# Upstream may install either gzipped or plain; handle both.
if ls "%{buildroot}%{_mandir}/man8/ethtool.8"* >/dev/null 2>&1; then
    if [ -f "%{buildroot}%{_mandir}/man8/ethtool.8" ]; then
        gzip -9 "%{buildroot}%{_mandir}/man8/ethtool.8"
    fi
    if [ -f "%{buildroot}%{_mandir}/man8/ethtool.8.gz" ]; then
        mv "%{buildroot}%{_mandir}/man8/ethtool.8.gz" \
           "%{buildroot}%{_mandir}/man8/mlnx-ethtool.8.gz"
    fi
fi

# Bash completion: install as a separate completion script for mlnx-ethtool
if [ -f "%{buildroot}%{_datadir}/bash-completion/completions/ethtool" ]; then
    mv "%{buildroot}%{_datadir}/bash-completion/completions/ethtool" \
       "%{buildroot}%{_datadir}/bash-completion/completions/mlnx-ethtool"
fi

# Helpful post-install info
install -d "%{buildroot}%{_sysconfdir}/profile.d"
cat > "%{buildroot}%{_sysconfdir}/profile.d/mlnx-ethtool.sh" <<'EOF'
# Mellanox/NVIDIA ethtool co-installation notice
# Invoke: /usr/sbin/mlnx-ethtool  (stock ethtool remains /usr/sbin/ethtool)
EOF
%post
cat <<'EOF'
Mellanox/NVIDIA ethtool installed as: /usr/sbin/mlnx-ethtool
Stock ethtool remains:               /usr/sbin/ethtool
Use 'man mlnx-ethtool' for the MLNX manpage.
EOF

%files
%defattr(-,root,root)
%{_sbindir}/mlnx-ethtool
%{_mandir}/man8/mlnx-ethtool.8.gz
%{_datadir}/bash-completion/completions/mlnx-ethtool
%config(noreplace) %{_sysconfdir}/profile.d/mlnx-ethtool.sh
%doc AUTHORS NEWS README
%license COPYING


%changelog
* Mon Oct 27 2025 Mayank Singh <mayansingh@microsoft.com> - 6.9-4
- Make mlnx-ethtool co-installable by renaming binary (mlnx-ethtool),
  manpage (mlnx-ethtool.8.gz), and bash-completion (mlnx-ethtool).
  Avoid owning files provided by stock ethtool to resolve RPM conflicts.

* Mon Sep 15 2025 Elaheh Dehghani <edehghani@microsoft.com> - 6.9-3
- Enable ARM64 build by removing ExclusiveArch
* Tue Dec  17 2024 Binu Jose Philip <bphilip@microsoft.com> - 6.9-2
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
