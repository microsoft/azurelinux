%define         debug_package %{nil}
Summary:        Fluent Bit is a fast Log Processor and Forwarder
Name:           td-agent-bit
Version:        1.7.6
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://fluentbit.io/
Source0:        https://fluentbit.io/releases/1.7/fluent-bit-%{version}.tar.gz
BuildRequires:  build-essential
BuildRequires:  cmake
BuildRequires:  bison
BuildRequires:  systemd-devel
BuildRequires:  zlib-devel
BuildRequires:  openssl-devel
BuildRequires:  flex
BuildRequires:  flex-devel
Requires:       openssl
Requires:       flex
Requires:       zlib

%description
Fast Log Processor and Forwarder which allows you to collect any data like
metrics and logs from different sources, enrich them with filters and
send them to multiple destinations.

%prep
%setup -q -n fluent-bit-%{version}

%build
cd build
cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} \
      -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
      -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir} \
      -DFLB_TD=Yes \
      -DMBEDTLS_FATAL_WARNINGS=Off \
      ..
make %{?_smp_mflags}

%install
cd build
make install DESTDIR=%{buildroot}

# Move service file to systemd unit files path
mkdir -p %{buildroot}%{_libdir}/systemd/system
mv %{buildroot}/lib/systemd/system/%{name}.service %{buildroot}%{_libdir}/systemd/system/%{name}.service
rm -r %{buildroot}/lib

%preun
%systemd_preun td-agent-bit.service

%post
/sbin/ldconfig
%systemd_post td-agent-bit.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart td-agent-bit.service

%files
%defattr(-,root,root)
%doc README.md
%license LICENSE
%{_bindir}/td-agent-bit
%{_libdir}/systemd/system/%{name}.service
%{_libdir}/td-agent-bit/libfluent-bit.so
%config(noreplace) %{_sysconfdir}/td-agent-bit/td-agent-bit.conf
%config(noreplace) %{_sysconfdir}/td-agent-bit/plugins.conf
%config(noreplace) %{_sysconfdir}/td-agent-bit/parsers.conf

%changelog
* Mon May 17 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.7.6-1
- Original version for CBL-Mariner
- License verified
