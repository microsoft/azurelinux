%global __requires_exclude perl\\(.*\\)
Summary:        Net-SNMP is a suite of applications used to implement SNMP v1, SNMP v2c and SNMP v3 using both IPv4 and IPv6.
Name:           net-snmp
Version:        5.9
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Productivity/Networking/Other
URL:            http://net-snmp.sourceforge.net/
Source0:        http://sourceforge.net/projects/%{name}/files/%{name}/%{version}/%{name}-%{version}.tar.gz
Source1:        snmpd.service
Source2:        snmptrapd.service

BuildRequires:  openssl-devel
BuildRequires:  perl
BuildRequires:  systemd

%if %{with_check}
BuildRequires:  net-tools
%endif

Requires:       perl
Requires:       systemd

%description
 Net-SNMP is a suite of applications used to implement SNMP v1, SNMP v2c and SNMP v3 using both IPv4 and IPv6.

%package devel
Summary:    The includes and static libraries from the Net-SNMP package.
Group:      Development/Libraries

Requires:   net-snmp = %{version}

%description devel
The net-snmp-devel package contains headers and libraries for building SNMP applications.

%prep
%autosetup

%build
%configure \
                --host=ia64-linux \
                --build=i686 \
                --target=ia64-linux \
                --sbindir=/sbin \
                --with-sys-location="unknown" \
                --with-logfile=%{_var}/log/net-snmpd.log \
                --with-persistent-directory=%{_sharedstatedir}/net-snmp \
                --with-sys-contact="root@localhost" \
                --with-defaults \
                --with-systemd \
                --disable-static \
                --with-x=no \
                --enable-as-needed
make

%install
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}/lib/systemd/system
install -m 0644 %{SOURCE1} %{buildroot}/lib/systemd/system/snmpd.service
install -m 0644 %{SOURCE2} %{buildroot}/lib/systemd/system/snmptrapd.service

%check
make %{?_smp_mflags} test

%post
/sbin/ldconfig
%systemd_post snmpd.service
%systemd_post snmptrapd.service

%preun
%systemd_preun snmpd.service
%systemd_preun snmptrapd.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart snmpd.service
%systemd_postun_with_restart snmptrapd.service

%clean
rm -rf %{buildroot}/*


%files
%license COPYING
%doc NEWS README ChangeLog
%defattr(-,root,root)
/lib/systemd/system/snmpd.service
/lib/systemd/system/snmptrapd.service
%{_bindir}
%{_libdir}/*.so.*
/sbin/*

%files devel
%defattr(-,root,root)
%{_datadir}
%{_includedir}
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/perl5
%{_libdir}/pkgconfig/*.pc
%exclude %{_lib}/perl5/*/*/perllocal.pod

%changelog
* Tue Nov 10 2020 Andrew Phelps <anphel@microsoft.com> - 5.9-2
- Fix check test by adding net-tools build requirement.

* Fri Oct 30 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.9-1
- Updating to 5.9 to fix CVE-2019-20892. A patch couldn't be applied without backporting.
- Switching to %%autosetup.
- License verified.
- Removed %%sha1 macro.
- Updating whitespaces to fix issues reported by the linter.

* Sat May 09 00:20:48 PST 2020 Nick Samson <nisamson@microsoft.com> - 5.8-4
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 5.8-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> - 5.8-2
- Using %configure and changing for perl upgrade

* Wed Sep 19 2018 Keerthana K <keerthanak@vmware.com> - 5.8-1
- Update to version 5.8

* Tue Jul 31 2018 Ajay Kaher <akaher@vmware.com> - 5.7.3-9
- Excluded perllocal.pod for aarch64

* Mon Apr 16 2018 Xiaolin Li <xiaolinl@vmware.com> - 5.7.3-8
- Apply patch for CVE-2018-1000116

* Mon Jul 24 2017 Dheeraj Shetty <dheerajs@vmware.com> - 5.7.3-7
- Make service file a different source

* Tue Apr 04 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 5.7.3-6
- Patch to remove U64 typedef

* Tue Oct 04 2016 ChangLee <changLee@vmware.com> - 5.7.3-5
- Modified %check

* Thu May 26 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 5.7.3-4
- Excluded the perllocal.pod log.

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 5.7.3-3
- GA - Bump release of all rpms

* Wed May 04 2016 Nick Shi <nshi@vmware.com> - 5.7.3-2
- Add snmpd and snmptrapd to systemd service.

* Mon Nov 30 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 5.7.3-1
- Initial build.  First version
