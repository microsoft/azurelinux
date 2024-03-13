Summary:        Package for Mariner to meet Azure Security Baseline 
Name:           asc
Version:        3.0
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Base
URL:            https://aka.ms/mariner
Obsoletes:      filesystem-asc

%description
Package for Mariner to meet Azure Security Baseline by adding multiple config files in /etc/modprobe.d

%prep

%build

%install
install -vdm 755 %{buildroot}/etc/modprobe.d

# Security patch for CCE-14118-4, msid: 6.6
# Disable the installation and use of file systems that are not required (squashfs)
cat > %{buildroot}/etc/modprobe.d/squashfs.conf <<- "EOF"
# Begin /etc/modprobe.d/squashfs.conf

install squashfs /bin/true

# End /etc/modprobe.d/squashfs.conf
EOF

# Security patch for msid: 1.1.21.1
# Ensure mounting of USB storage devices is disabled
cat > %{buildroot}/etc/modprobe.d/usb-storage.conf <<- "EOF"
# Begin /etc/modprobe.d/usb-storage.conf

install usb-storage /bin/true

# End /etc/modprobe.d/usb-storage.conf
EOF

# Security patch for msid: 6.1
# Disable the installation and use of file systems that are not required (cramfs)
cat > %{buildroot}/etc/modprobe.d/cramfs.conf <<- "EOF"
# Begin /etc/modprobe.d/cramfs.conf

install cramfs /bin/true

# End /etc/modprobe.d/cramfs.conf
EOF

# Security patch for msid: 6.2
# Disable the installation and use of file systems that are not required (freevxfs)
cat > %{buildroot}/etc/modprobe.d/freevxfs.conf <<- "EOF"
# Begin /etc/modprobe.d/freevxfs.conf

install freevxfs /bin/true

# End /etc/modprobe.d/freevxfs.conf
EOF

# Security patch for msid: 6.3
# Disable the installation and use of file systems that are not required (hfs)
cat > %{buildroot}/etc/modprobe.d/hfs.conf <<- "EOF"
# Begin /etc/modprobe.d/hfs.conf

install hfs /bin/true

# End /etc/modprobe.d/hfs.conf
EOF

# Security patch for msid: 6.4
# Disable the installation and use of file systems that are not required (hfsplus)
cat > %{buildroot}/etc/modprobe.d/hfsplus.conf <<- "EOF"
# Begin /etc/modprobe.d/hfsplus.conf

install hfsplus /bin/true

# End /etc/modprobe.d/hfsplus.conf
EOF

# Security patch for msid: 6.5
# Disable the installation and use of file systems that are not required (jffs2)
cat > %{buildroot}/etc/modprobe.d/jffs2.conf <<- "EOF"
# Begin /etc/modprobe.d/jffs2.conf

install jffs2 /bin/true

# End /etc/modprobe.d/jffs2.conf
EOF

# Security patch for msid: 54
# Ensure DCCP is disabled
cat > %{buildroot}/etc/modprobe.d/dccp.conf <<- "EOF"
# Begin /etc/modprobe.d/dccp.conf

install dccp /bin/true

# End /etc/modprobe.d/dccp.conf
EOF

# Security patch for msid: 55
# Ensure SCTP is disabled
cat > %{buildroot}/etc/modprobe.d/sctp.conf <<- "EOF"
# Begin /etc/modprobe.d/sctp.conf

install sctp /bin/true

# End /etc/modprobe.d/sctp.conf
EOF

# Security patch for msid: 56
# Disable support for RDS
cat > %{buildroot}/etc/modprobe.d/rds.conf <<- "EOF"
# Begin /etc/modprobe.d/rds.conf

install rds /bin/true

# End /etc/modprobe.d/rds.conf
EOF

# Security patch for msid: 57
# Ensure TIPC is disabled
cat > %{buildroot}/etc/modprobe.d/tipc.conf <<- "EOF"
# Begin /etc/modprobe.d/tipc.conf

install tipc /bin/true

# End /etc/modprobe.d/tipc.conf
EOF


%files
%defattr(-,root,root,0755)
%config(noreplace) /etc/modprobe.d/squashfs.conf
%config(noreplace) /etc/modprobe.d/usb-storage.conf
%config(noreplace) /etc/modprobe.d/cramfs.conf
%config(noreplace) /etc/modprobe.d/freevxfs.conf
%config(noreplace) /etc/modprobe.d/hfs.conf
%config(noreplace) /etc/modprobe.d/hfsplus.conf
%config(noreplace) /etc/modprobe.d/jffs2.conf
%config(noreplace) /etc/modprobe.d/dccp.conf
%config(noreplace) /etc/modprobe.d/sctp.conf
%config(noreplace) /etc/modprobe.d/rds.conf
%config(noreplace) /etc/modprobe.d/tipc.conf


%changelog
* Mon Mar 04 2024 Dan Streetman <ddstreet@microsoft.com> - 3.0-2
- move filesystem-asc stuff into asc

* Tue Feb 27 2024 Muhammad Falak <mwani@microsoft.com> - 3.0-1
- Bump version to 3.0 for AzureLiux 3.0

* Tue Aug 16 2022 Minghe Ren <mingheren@microsoft.com> - 1.0-1
- Initial CBL-Mariner import from Azure (license: MIT)
- License verified
