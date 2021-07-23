Summary:        A package to provide cockpit for mariner
Name:           cockpit
Version:        248
Release:        1%{?dist}
License:        MIT
URL:            https://github.com/cockpit-project/cockpit
Vendor:         Microsoft
Distribution:   Mariner
Source0:        https://github.com/cockpit-project/cockpit/releases/download/248/cockpit-248.tar.xz

BuildRequires: gcc
BuildRequires: glib-devel
BuildRequires: json-glib-devel
BuildRequires: polkit-devel
BuildRequires: pam-devel

BuildRequires: autoconf automake
BuildRequires: make
BuildRequires: gettext >= 0.19.7
BuildRequires: libssh-devel >= 0.8.5
BuildRequires: openssl-devel
BuildRequires: gnutls-devel >= 3.4.3
BuildRequires: zlib-devel
BuildRequires: krb5-devel >= 1.11
# BuildRequires: libxslt-devel
# BuildRequires: glib-networking
BuildRequires: sed
BuildRequires: systemd-devel >= 235
BuildRequires:  e2fsprogs-devel
BuildRequires:  which

%define _unpackaged_files_terminate_build 0

%description
cockpit for mariner

%prep
%setup -q
mkdir -p %{buildroot}/etc/pam.d

%build
./configure --sysconfdir=/etc --prefix=/usr --disable-pcp --disable-doc
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
cat > %{buildroot}/etc/pam.d/cockpit << EOF
    #%PAM-1.0 
    # this MUST be first in the "auth" stack as it sets PAM_USER 
    # user_unknown is definitive, so die instead of ignore to avoid subsequent modules mess up the error code 
    -auth      [success=done new_authtok_reqd=done user_unknown=die default=ignore]   pam_cockpit_cert.so 
    auth       substack     system-auth 
    auth       optional     pam_ssh_add.so 
    account    required     pam_nologin.so 
    account    include      system-account 
    password   include      system-password 
    session    required     pam_loginuid.so 
    session    optional     pam_keyinit.so force revoke 
    session    optional     pam_ssh_add.so 
    session    include      system-session 
EOF
chmod -R go+rx %{buildroot}/usr/share/cockpit
chmod o+rx %{buildroot}/etc/cockpit

%check
make check

%files
# %defattr(-,root,root)
%license COPYING
%license COPYING.node
/usr/share/cockpit
/etc/cockpit
/etc/pam.d/cockpit
/usr/share/metainfo/*cockpit*.xml
/usr/share/polkit-1/actions/org.cockpit-project.cockpit-bridge.policy
/usr/share/pixmaps/cockpit*.png
/usr/lib/tmpfiles.d/cockpit-tempfiles.conf
/lib/systemd/system/cockpit*.socket
/lib/systemd/system/cockpit*.service
/lib/systemd/system/system-cockpithttps.slice
/etc/issue.d/cockpit.issue
/etc/motd.d/cockpit
/usr/bin/cockpit-bridge
/usr/lib/security/pam_cockpit_cert.so
/usr/lib/security/pam_ssh_add.so
/usr/libexec/cockpit-*
/usr/sbin/remotectl

%changelog
* Fri July 23 2021 Shane Guan <shaneguan@microsoft.com> 248-1
- Initial version of cockpit package

