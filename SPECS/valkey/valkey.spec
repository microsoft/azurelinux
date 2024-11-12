Summary:        advanced key-value store
Name:           valkey
Version:        8.0.1
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Applications/Databases
URL:            https://valkey.io/
Source0:        https://github.com/valkey-io/valkey/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         valkey-conf.patch
Patch1:         disable-mem-defrag-tests.patch
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  systemd
BuildRequires:  tcl
BuildRequires:  tcl-devel
BuildRequires:  which
Requires:       systemd
Requires(pre):  %{_sbindir}/groupadd
Requires(pre):  %{_sbindir}/useradd

%description
A flexible distributed key-value datastore that supports both caching and beyond caching workloads.

%prep
%autosetup -p1

%build
make BUILD_TLS=yes %{?_smp_mflags}

%install
install -vdm 755 %{buildroot}
make PREFIX=%{buildroot}%{_prefix} install
install -D -m 0640 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}.conf
mkdir -p %{buildroot}%{_sharedstatedir}/valkey
mkdir -p %{buildroot}%{_var}/log
mkdir -p %{buildroot}%{_var}/opt/%{name}/log
ln -sfv %{_var}/opt/%{name}/log %{buildroot}%{_var}/log/%{name}
mkdir -p %{buildroot}/usr/lib/systemd/system
cat << EOF >>  %{buildroot}/usr/lib/systemd/system/valkey.service
[Unit]
Description=Valkey in-memory key-value datastore
After=network.target

[Service]
ExecStart=%{_bindir}/valkey-server %{_sysconfdir}/valkey.conf --daemonize no
ExecStop=%{_bindir}/valkey-cli shutdown
User=valkey
Group=valkey

[Install]
WantedBy=multi-user.target
EOF

%check
make check

%pre
getent group %{name} &> /dev/null || \
groupadd -r %{name} &> /dev/null
getent passwd %{name} &> /dev/null || \
useradd -r -g %{name} -d %{_sharedstatedir}/valkey -s /sbin/nologin \
-c 'Valkey Datastore Server' %{name} &> /dev/null
exit 0

%post
/sbin/ldconfig
%systemd_post  valkey.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart valkey.service

%files
%defattr(-,root,root)
%license COPYING
%dir %attr(0750, valkey, valkey) %{_sharedstatedir}/valkey
%dir %attr(0750, valkey, valkey) %{_var}/opt/%{name}/log
%attr(0750, valkey, valkey) %{_var}/log/%{name}
%{_bindir}/*
%{_libdir}/systemd/*
%config(noreplace) %attr(0640, %{name}, %{name}) %{_sysconfdir}/valkey.conf

%changelog
* Mon Nov 04 2024 Sean Dougherty <sdougherty@microsoft.com> - 8.0.1-1
- Version bump to address CVE-2024-31449 CVE-2024-31228 and CVE-2024-31227.

* Tue Oct 29 2024 Rohit Rawat <rohitrawat@microsoft.com> - 8.0.0-2
- Add patch to remove flaky mem defrag test.

* Mon Sep 30 2024 Rohit Rawat <rohitrawat@microsoft.com> - 8.0.0-1
- Original version for CBL-Mariner.
- License Verified.
