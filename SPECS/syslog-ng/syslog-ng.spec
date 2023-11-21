Summary:        Next generation system logger facilty
Name:           syslog-ng
Version:        3.33.2
Release:        5%{?dist}
License:        BSD AND GPLv2+ AND LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Daemons
URL:            https://syslog-ng.org/
Source0:        https://github.com/balabit/%{name}/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
Source1:        60-syslog-ng-journald.conf
Source2:        syslog-ng.service
Patch0:         CVE-2022-38725.patch
BuildRequires:  glib-devel
BuildRequires:  json-c-devel
BuildRequires:  json-glib-devel
BuildRequires:  python3-devel
BuildRequires:  systemd-devel
%if %{with_check}
BuildRequires:  curl-devel
BuildRequires:  python3-pip
%endif
Requires:       glib
Requires:       json-c
Requires:       json-glib
Requires:       systemd
Obsoletes:      eventlog

Provides: syslog

%description
 The syslog-ng application is a flexible and highly scalable
 system logging tool. It is often used to manage log messages and implement
 centralized logging, where the aim is to collect the log messages of several
 devices to a single, central log server.

%package -n     python3-syslog-ng
Summary:        python3-syslog-ng
Requires:       python3
Requires:       python3-libs

%description -n python3-syslog-ng
Python 3 version.

%package        devel
Summary:        Header and development files for syslog-ng
Requires:       %{name} = %{version}-%{release}

%description    devel
 syslog-ng-devel package contains header files, pkfconfig files, and libraries
 needed to build applications using syslog-ng APIs.

%prep
%autosetup -p1
rm -rf ../p3dir
cp -a . ../p3dir

%build
%configure \
    CFLAGS="%{optflags}" \
    CXXFLAGS="%{optflags}" \
    --disable-silent-rules \
    --sysconfdir=%{_sysconfdir}/syslog-ng \
    --enable-systemd \
    --with-systemdsystemunitdir=%{_libdir}/systemd/system \
    --enable-json=yes \
    --with-jsonc=system \
    --disable-java \
    --disable-redis \
    --with-python=3 \
    PYTHON=/bin/python3 \
    PKG_CONFIG_PATH=%{_prefix}/local/lib/pkgconfig/
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name "*.la" -exec rm -f {} \;
rm %{buildroot}/%{_libdir}/systemd/system/syslog-ng@.service
rm -rf %{buildroot}/%{_infodir}
install -vd %{buildroot}%{_sysconfdir}/systemd/journald.conf.d/
install -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/systemd/journald.conf.d/
install -p -m 644 %{SOURCE2} %{buildroot}%{_libdir}/systemd/system/
%{_fixperms} %{buildroot}/*
sed -i 's/eventlog//g'  %{buildroot}%{_libdir}/pkgconfig/syslog-ng.pc

install -vdm755 %{buildroot}%{_libdir}/systemd/system-preset
echo "disable syslog-ng.service" > %{buildroot}%{_libdir}/systemd/system-preset/50-syslog-ng.preset

%check
pip3 install unittest2 nose ply pep8
make %{?_smp_mflags} ENABLE_TESTING=1 check

%post
if [ $1 -eq 1 ] ; then
  mkdir -p %{_prefix}%{_var}/
fi
%systemd_post syslog-ng.service

%preun
%systemd_preun syslog-ng.service

%postun
%systemd_postun_with_restart syslog-ng.service

%files
%defattr(-,root,root)
%license COPYING GPL.txt LGPL.txt
%config(noreplace) %{_sysconfdir}/syslog-ng/syslog-ng.conf
%config(noreplace) %{_sysconfdir}/syslog-ng/scl.conf
%{_sysconfdir}/systemd/journald.conf.d/*
%{_libdir}/systemd/system/syslog-ng.service
%{_libdir}/systemd/system-preset/50-syslog-ng.preset
%{_bindir}/*
%{_sbindir}/syslog-ng
%{_sbindir}/syslog-ng-ctl
%{_sbindir}/syslog-ng-debun
%{_libdir}/libsyslog-ng-*.so.*
%{_libdir}/libevtlog-*.so.*
%{_libdir}/libloggen_helper*
%{_libdir}/libloggen_plugin*
%{_libdir}/libsecret-storage*
%{_libdir}/%{name}/loggen/*
%{_libdir}/syslog-ng/lib*.so
%{_mandir}/man1/dqtool.1.gz
%{_mandir}/man1/loggen.1.gz
%{_mandir}/man1/pdbtool.1.gz
%{_mandir}/man1/persist-tool.1.gz
%{_mandir}/man1/slogencrypt.1.gz
%{_mandir}/man1/slogkey.1.gz
%{_mandir}/man1/slogverify.1.gz
%{_mandir}/man1/syslog-ng-ctl.1.gz
%{_mandir}/man1/syslog-ng-debun.1.gz
%{_mandir}/man5/syslog-ng.conf.5.gz
%{_mandir}/man7/secure-logging.7.gz
%{_mandir}/man8/syslog-ng.8.gz
%{_datadir}/syslog-ng/*

%files -n python3-syslog-ng
%defattr(-,root,root,-)
%{_libdir}/syslog-ng/python/*

%files devel
%defattr(-,root,root)
%{_includedir}/syslog-ng/*
%{_libdir}/libsyslog-ng.so
%{_libdir}/libevtlog.so
%{_libdir}/libsyslog-ng-native-connector.a
%{_libdir}/pkgconfig/*

%changelog
* Fri Oct 13 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 3.33.2-5
- Patched CVE-2022-38725

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 3.33.2-4
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Mon Jan 31 2022 Thomas Crain <thcrain@microsoft.com> - 3.33.2-3
- Remove python2 subpackage

* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.33.2-2
- Added "Provides: syslog".

* Fri Jan 14 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 3.33.2-1
- Update to version 3.33.2.

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.23.1-4
- Removing the explicit %%clean stage.

* Fri Dec 03 2021 Thomas Crain <thcrain@microsoft.com> - 3.23.1-3
- Replace easy_install usage with pip in %%check sections

* Tue Oct 13 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 3.23.1-2
- Added the %%license macro.
- License verified.

* Wed Mar 18 2020 Henry Beberman <henry.beberman@microsoft.com> 3.23.1-1
- Update to 3.23.1. License fixed.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.17.2-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Oct 10 2018 Ankit Jain <ankitja@vmware.com> 3.17.2-1
- Update to version 3.17.2

* Mon Sep 11 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.11.1-3
- Obsolete eventlog.

* Mon Sep 04 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.11.1-2
- Use old service file.

* Fri Aug 18 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.11.1-1
- Update to version 3.11.1

* Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com>  3.9.1-3
- Disabled syslog-ng service by default

* Thu May 18 2017 Xiaolin Li <xiaolinl@vmware.com> 3.9.1-2
- Move python2 requires to python2 subpackage and added python3 binding.

* Tue Apr 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.9.1-1
- Update to version 3.9.1

* Tue Oct 04 2016 ChangLee <changlee@vmware.com> 3.6.4-6
- Modified %check

* Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com>  3.6.4-5
- Fixed logic to restart the active services after upgrade

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.6.4-4
- GA - Bump release of all rpms

* Wed May 4 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com>  3.6.4-3
- Fix for upgrade issues

* Wed Feb 17 2016 Anish Swaminathan <anishs@vmware.com>  3.6.4-2
- Add journald conf file.

* Wed Jan 20 2016 Anish Swaminathan <anishs@vmware.com> 3.6.4-1
- Upgrade version.

* Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  3.6.2-5
- Change config file attributes.

* Wed Dec 09 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 3.6.2-4
- Moving files from devel rpm to the main package.

* Wed Aug 05 2015 Kumar Kaushik <kaushikk@vmware.com> 3.6.2-3
- Adding preun section.

* Sat Jul 18 2015 Vinay Kulkarni <kulkarniv@vmware.com> 3.6.2-2
- Split headers and unshared libs over to devel package.

* Thu Jun 4 2015 Vinay Kulkarni <kulkarniv@vmware.com> 3.6.2-1
- Add syslog-ng support to photon.
