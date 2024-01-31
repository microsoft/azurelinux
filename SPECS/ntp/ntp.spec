Summary:        Network Time Protocol reference implementation
Name:           ntp
Version:        4.2.8p17
Release:        1%{?dist}
License:        BSD AND GPLv2+ AND LGPLv2+ AND MIT AND OpenLDAP AND Public Domain
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/NetworkingPrograms
URL:            https://www.ntp.org/
Source0:        https://www.eecis.udel.edu/~ntp/ntp_spool/ntp4/ntp-4.2/%{name}-%{version}.tar.gz
#https://github.com/darkhelmet/ntpstat
Source1:        ntpstat-master.zip
Source2:        ntp.sysconfig
Source3:        ntp.step-tickers
Source4:        ntpdate.wrapper
Source5:        ntpdate.sysconfig
Source6:        ntpdate.service
Source7:        ntpd.service
Source8:        LICENSE.PTR
Patch0:         ntp-gcc11.patch

BuildRequires:  gcc >= 11.2.0
BuildRequires:  glibc >= 2.34
BuildRequires:  libcap-devel
BuildRequires:  openssl-devel
BuildRequires:  systemd
BuildRequires:  unzip
BuildRequires:  which

Requires:       libcap >= 2.24
Requires:       openssl
Requires:       systemd
Requires(pre):  %{_sbindir}/groupadd
Requires(pre):  %{_sbindir}/useradd

Provides:       ntpdate = %{version}-%{release}

%description
The ntp package contains a client and server to keep the time
synchronized between various computers over a network. This
package is the official reference implementation of the
NTP protocol.

%package        perl
Summary:        Perl scripts for ntp
Group:          Utilities

Requires:       ntp = %{version}-%{release}
Requires:       perl >= 5
Requires:       perl-IO-Socket-SSL
Requires:       perl-Net-SSLeay

%description    perl
Perl scripts for ntp.

%package -n ntpstat
Summary:        Utilities
Group:          Utilities

%description -n ntpstat
ntpstat is a utility which reports the synchronisation
state of the NTP daemon running on the local machine.

%prep
%setup -q -a 1
%patch0 -p1

%build

sh configure \
    CFLAGS="%{optflags}" \
    CXXFLAGS="%{optflags}" \
    --disable-silent-rules \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --sysconfdir=%{_sysconfdir} \
    --with-binsubdir=sbin \
    --enable-linuxcaps
make %{?_smp_mflags}
make -C ntpstat-master CFLAGS="$CFLAGS"

%install

cp %{SOURCE8} .

make DESTDIR=%{buildroot} install
install -v -m755    -d %{buildroot}%{_docdir}/%{name}-%{version}
cp -v -R html/*     %{buildroot}%{_docdir}/%{name}-%{version}/
install -vdm 755 %{buildroot}%{_sysconfdir}

mkdir -p %{buildroot}%{_sharedstatedir}/ntp/drift
mkdir -p %{buildroot}%{_sysconfdir}/ntp
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
cp %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/ntp
pushd ntpstat-master
install -m 755 ntpstat %{buildroot}/%{_bindir}
install -m 644 ntpstat.1 %{buildroot}/%{_mandir}/man8/ntpstat.8
popd

cat > %{buildroot}%{_sysconfdir}/ntp.conf <<- "EOF"
tinker panic 0
restrict default kod nomodify notrap nopeer noquery
restrict 127.0.0.1
restrict -6 ::1
driftfile %{_sharedstatedir}/ntp/drift/ntp.drift
EOF

install -D -m644 COPYRIGHT %{buildroot}%{_datadir}/licenses/%{name}/LICENSE
rm -rf %{buildroot}%{_sysconfdir}/rc.d/*

%{_fixperms} %{buildroot}/*
mkdir -p %{buildroot}%{_unitdir}
install -p -m644 %{SOURCE7} %{buildroot}%{_unitdir}/ntpd.service

install -vdm755 %{buildroot}%{_libdir}/systemd/system-preset
echo "disable ntpd.service" > %{buildroot}%{_libdir}/systemd/system-preset/50-ntpd.preset

# No vendor pool created for CBL-Mariner yet.
sed -e 's|VENDORZONE\.||' \
	< %{SOURCE3} > %{buildroot}%{_sysconfdir}/ntp/step-tickers
touch -r %{SOURCE3} %{buildroot}%{_sysconfdir}/ntp/step-tickers

install -p -m755 %{SOURCE4} %{buildroot}%{_libexecdir}/ntpdate-wrapper
install -p -m750 %{SOURCE5} %{buildroot}%{_sysconfdir}/sysconfig/ntpdate
install -p -m644 %{SOURCE6} %{buildroot}%{_unitdir}/ntpdate.service

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%pre
if ! getent group ntp >/dev/null; then
    groupadd -g 87 ntp
fi
if ! getent passwd ntp >/dev/null; then
    useradd -c "Network Time Protocol" -d %{_sharedstatedir}/ntp -u 87 -g ntp -s /bin/false ntp
fi

%post
%{_sbindir}/ldconfig
%systemd_post ntpd.service
%systemd_post ntpdate.service

%preun
%systemd_preun ntpd.service
%systemd_preun ntpdate.service

%postun
%systemd_postun_with_restart ntpd.service
%systemd_postun ntpdate.service

%files
%defattr(-,root,root)
%license COPYRIGHT LICENSE.PTR
%dir %{_sharedstatedir}/ntp/drift
%attr(0755, ntp, ntp) %{_sharedstatedir}/ntp/drift
%attr(0750, root, root) %config(noreplace) %{_sysconfdir}/ntp.conf
%attr(0750, root, root) %config(noreplace) %{_sysconfdir}/sysconfig/ntp
%attr(0750, root, root) %config(noreplace) %{_sysconfdir}/sysconfig/ntpdate
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/ntp/step-tickers
%{_unitdir}/ntpd.service
%{_unitdir}/ntpdate.service
%{_libdir}/systemd/system-preset/50-ntpd.preset
%{_libexecdir}/ntpdate-wrapper
%{_bindir}/ntpd
%{_bindir}/ntpdate
%{_bindir}/ntpdc
%{_bindir}/ntp-keygen
%{_bindir}/ntpq
%{_bindir}/ntptime
%{_bindir}/sntp
%{_bindir}/tickadj
%{_docdir}/%{name}-%{version}/*
%{_docdir}/ntp/*
%{_docdir}/sntp/*
%{_datadir}/licenses/ntp/LICENSE
%{_mandir}/man1/ntpd.1.gz
%{_mandir}/man1/ntpdc.1.gz
%{_mandir}/man1/ntp-keygen.1.gz
%{_mandir}/man1/ntpq.1.gz
%{_mandir}/man1/sntp.1.gz
%{_mandir}/man5/*

%files perl
%{_bindir}/calc_tickadj
%{_bindir}/ntptrace
%{_bindir}/ntp-wait
%{_bindir}/update-leap
%{_datadir}/ntp/lib/NTP/Util.pm
%{_mandir}/man1/calc_tickadj.1.gz
%{_mandir}/man1/ntptrace.1.gz
%{_mandir}/man1/ntp-wait.1.gz
%{_mandir}/man1/update-leap.1.gz

%files -n ntpstat
%defattr(-,root,root)
%{_bindir}/ntpstat
%{_mandir}/man8/ntpstat.8*

%changelog
* Wed Jan 31 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.2.8p17-1
- Auto-upgrade to 4.2.8p17 - 3.0 - Upgrade

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.2.8p15-3
- Removing the explicit %%clean stage.

* Wed Nov 17 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.2.8p15-2
- License verified.
- Added "LICENSE.PTR" to clarify licensing.

* Wed Nov 10 2021 Nicolas Guibourge <nicolasg@microsoft.com> - 4.2.8p15-1
- Upgrade to version 4.2.8p15.

* Fri Sep 24 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.2.8p13-4
- Adding 'Provides' for 'ntpdate' using Fedora 32 spec (license: MIT) as guidance.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 4.2.8p13-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 4.2.8p13-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Jul 16 2019 Srinidhi Rao <srinidhir@vmware.com> - 4.2.8p13-1
- Upgrade to version 4.2.8p13
- Ported fix to created drift directory owning ntp user.

* Fri Aug 24 2018 Srinidhi Rao <srinidhir@vmware.com> - 4.2.8p12-1
- Upgrade version to 4.2.8p12.

* Mon Mar 05 2018 Xiaolin Li <xiaolinl@vmware.com> - 4.2.8p11-1
- Upgrade version to 4.2.8p11 and move perl scripts to perl subpackage.

* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.2.8p10-4
- Remove shadow from requires and use explicit tools for post actions

* Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com> - 4.2.8p10-3
- Disabled ntpd service by default

* Mon Apr 10 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 4.2.8p10-2
- add noquery to conf

* Wed Apr 05 2017 Anish Swaminathan <anishs@vmware.com> - 4.2.8p10-1
- Upgrade version to 4.2.8p10 - fix for CVE-2017-6458, CVE-2017-6460

* Tue Jan 24 2017 Xiaolin Li <xiaolinl@vmware.com> - 4.2.8p9-1
- Updated to version 4.2.8p9.

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 4.2.8p6-4
- GA - Bump release of all rpms

* Thu May 12 2016 Divya Thaluru <dthaluru@vmware.com> - 4.2.8p6-3
- Adding ntp sysconfig file

* Wed May 04 2016 Anish Swaminathan <anishs@vmware.com> - 4.2.8p6-2
- Edit scriptlets.

* Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> - 4.2.8p6-1
- Upgrade version

* Thu Jan 7 2016 Xiaolin Li <xiaolinl@vmware.com> - 4.2.8p3-4
- Add ntpstat package.

* Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com> - 4.2.8p3-3
- Add systemd to Requires and BuildRequires.

* Fri Oct 30 2015 Xiaolin Li <xiaolinl@vmware.com> - 4.2.8p3-2
- Add ntpd to systemd service.

* Fri Oct 10 2014 Divya Thaluru <dthaluru@vmware.com> - 4.2.8p3-1
- Updating to version 4.2.8p3

* Fri Oct 10 2014 Divya Thaluru <dthaluru@vmware.com> - 4.2.6p5-1
- Initial build.  First version
