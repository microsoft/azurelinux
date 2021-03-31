Summary:        Cyrus Simple Authentication Service Layer (SASL) library
Name:           cyrus-sasl
Version:        2.1.27
Release:        4%{?dist}
License:        BSD with advertising
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://www.cyrusimap.org/sasl/
Source0:        https://github.com/cyrusimap/%{name}/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
Patch0:         CVE-2019-19906.patch
# CVE-2020-8032 only applies to the packaging of openSUSE's version of cyrus-sasl
# https://bugzilla.suse.com/show_bug.cgi?id=1180669
Patch1:         CVE-2020-8032.nopatch
BuildRequires:  e2fsprogs-devel
BuildRequires:  krb5-devel >= 1.12
BuildRequires:  openssl-devel
BuildRequires:  pam-devel
BuildRequires:  systemd
Requires:       krb5 >= 1.12
Requires:       openssl
Requires:       pam
Requires:       systemd

%description
The Cyrus SASL package contains a Simple Authentication and Security
Layer, a method for adding authentication support to
connection-based protocols. To use SASL, a protocol includes a command
for identifying and authenticating a user to a server and for
optionally negotiating protection of subsequent protocol interactions.
If its use is negotiated, a security layer is inserted between the
protocol and the connection.

%prep
%autosetup -p1

%build
autoreconf -fi
%configure \
    CFLAGS="%{optflags} -fPIC" \
    CXXFLAGS="%{optflags}" \
    --with-plugindir=%{_libdir}/sasl2 \
    --without-dblib \
    --with-saslauthd=/run/saslauthd \
    --without-authdaemond \
    --disable-macos-framework \
    --disable-sample \
    --disable-digest \
    --disable-otp \
    --disable-plain \
    --disable-anon \
    --enable-srp \
    --enable-gss_mutexes \
    --disable-static \
    --enable-shared \
    --enable-fast-install \
    --enable-krb4

make

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete -print
install -D -m644 COPYING %{buildroot}%{_datadir}/licenses/%{name}/LICENSE
%{_fixperms} %{buildroot}/*

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
cat << EOF >> %{buildroot}/%{_sysconfdir}/sysconfig/saslauthd
# Directory in which to place saslauthd's listening socket, pid file, and so
# on.  This directory must already exist.
SOCKETDIR=/run/saslauthd

# Mechanism to use when checking passwords.  Run "saslauthd -v" to get a list
# of which mechanism your installation was compiled with the ablity to use.
MECH=pam

# Additional flags to pass to saslauthd on the command line.  See saslauthd(8)
# for the list of accepted flags.
FLAGS=
EOF

mkdir -p %{buildroot}/lib/systemd/system
cat << EOF >> %{buildroot}/lib/systemd/system/saslauthd.service
[Unit]
Description=SASL authentication daemon.

[Service]
Type=forking
PIDFile=/run/saslauthd/saslauthd.pid
EnvironmentFile=%{_sysconfdir}/sysconfig/saslauthd
ExecStart=%{_sbindir}/saslauthd -m \$SOCKETDIR -a \$MECH \$FLAGS
RuntimeDirectory=saslauthd

[Install]
WantedBy=multi-user.target
EOF

install -vdm755 %{buildroot}%{_libdir}/systemd/system-preset
echo "disable saslauthd.service" > %{buildroot}%{_libdir}/systemd/system-preset/50-saslauthd.preset

%check
make %{?_smp_mflags} check

%post
%{_sbindir}/ldconfig
%systemd_post saslauthd.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart saslauthd.service

%preun
%systemd_preun saslauthd.service

%files
%defattr(-,root,root)
%license COPYING
%{_sysconfdir}/sysconfig/saslauthd
/lib/systemd/system/saslauthd.service
%{_libdir}/systemd/system-preset/50-saslauthd.preset
%{_includedir}/*
%{_libdir}/*.so*
%{_libdir}/pkgconfig/*
%{_libdir}/sasl2/*
%{_sbindir}/*
%{_mandir}/man3/*
%{_datadir}/licenses/%{name}/LICENSE
%{_mandir}/man8/saslauthd.8.gz

%changelog
* Fri Mar 05 2021 Thomas Crain <thcrain@microsoft.com> - 2.1.27-5
- Add nopatch for CVE-2020-8032
- Lint spec

* Thu May 28 2020 Andrew Phelps <anphel@microsoft.com> - 2.1.27-4
- Add patch to fix CVE-2019-19906

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.1.27-3
- Added %%license line automatically

* Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> - 2.1.27-2
- Renaming Linux-PAM to pam

* Wed Mar 25 2020 Nicolas Ontiveros <niontive@microsoft.com> - 2.1.27-1
- Update version to 2.1.27. License verified. URL and Source0 updated.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.1.26-15
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Nov 21 2017 Anish Swaminathan <anishs@vmware.com> - 2.1.26-14
- Update patch for memory leak fix

* Tue Oct 10 2017 Anish Swaminathan <anishs@vmware.com> - 2.1.26-13
- Add patch for memory leak fix

* Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com> - 2.1.26-12
- Disabled saslauthd service by default

* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> - 2.1.26-11
- BuildRequires Linux-PAM-devel

* Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> - 2.1.26-10
- Required krb5-devel.

* Wed Oct 05 2016 ChangLee <changlee@vmware.com> - 2.1.26-9
- Modified %check

* Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com> - 2.1.26-8
- Fixed logic to restart the active services after upgrade

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.1.26-7
- GA - Bump release of all rpms

* Tue May 3 2016 Divya Thaluru <dthaluru@vmware.com> - 2.1.26-6
- Fixing spec file to handle rpm upgrade scenario correctly

* Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com> - 2.1.26-5
- Add systemd to Requires and BuildRequires.

* Wed Nov 11 2015 Xiaolin Li <xiaolinl@vmware.com> - 2.1.26-4
- Add saslauthd service to systemd.

* Tue Sep 01 2015 Vinay Kulkarni <kulkarniv@vmware.com> - 2.1.26-3
- Enable CRAM.

* Thu Jul 16 2015 Divya Thaluru <dthaluru@vmware.com> - 2.1.26-2
- Disabling parallel threads in make

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> - 2.1.26-1
- Initial build. First version
