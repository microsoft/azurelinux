Summary:        A shared library implementation of IPMI and the basic tools
Name:           OpenIPMI
Version:        2.0.32
Release:        1%{?dist}
License:        LGPLv2+ AND GPLv2+ OR BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://sourceforge.net/projects/openipmi/
Source0:        https://downloads.sourceforge.net/openipmi/OpenIPMI-2.0.32.tar.gz
Source1:        openipmi-helper
Source2:        ipmi.service
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  perl
BuildRequires:  popt-devel
BuildRequires:  python3-devel
BuildRequires:  swig
BuildRequires:  systemd
Requires:       systemd

%description
This package contains a shared library implementation of IPMI and the
basic tools used with OpenIPMI.

%package        devel
Summary:        Development files for OpenIPMI
Group:          Utilities
Requires:       OpenIPMI = %{version}
Requires:       ncurses-devel

%description devel
Contains additional files need for a developer to create applications
and/or middleware that depends on libOpenIPMI

%package        perl
Summary:        Perl interface for OpenIPMI
Group:          Utilities
Requires:       OpenIPMI = %{version}-%{release}
Requires:       perl >= 5

%description    perl
A Perl interface for OpenIPMI.

%package        python
Summary:        Python interface for OpenIPMI
Group:          Utilities
Requires:       OpenIPMI = %{version}-%{release}
Requires:       python3
Provides:       python3-openipmi = %{version}-%{release}

%description    python
A Python interface for OpenIPMI.

%package        ui
Summary:        User Interface (ui)
Group:          Utilities
Requires:       OpenIPMI = %{version}-%{release}

%description    ui
This package contains a user interface

%package        lanserv
Summary:        Emulates an IPMI network listener
Group:          Utilities
Requires:       OpenIPMI = %{version}-%{release}

%description    lanserv
This package contains a network IPMI listener.

%prep
%autosetup -p1
autoreconf -fiv

%build
# USERFIX: Things you might have to add to configure:
#  --with-tclcflags='-I /usr/include/tclN.M' --with-tcllibs=-ltclN.M
#    Obviously, replace N.M with the version of tcl on your system.
%configure                                  \
    --with-tcl=no                           \
    --disable-static                        \
    --with-tkinter=no                       \
    --docdir=%{_docdir}/%{name}-%{version}  \
    --with-perl=yes                         \
    --with-perlinstall=%{perl_vendorarch}   \
    --with-python=%python3                  \
    --with-pythoninstall=%{python3_sitearch}
make

%install
make DESTDIR=%{buildroot} install
install -d %{buildroot}%{_sysconfdir}/init.d
install -d %{buildroot}%{_sysconfdir}/sysconfig
install ipmi.init %{buildroot}%{_sysconfdir}/init.d/ipmi
install ipmi.sysconf %{buildroot}%{_sysconfdir}/sysconfig/ipmi
find %{buildroot} -type f -name "*.la" -delete -print
mkdir -p %{buildroot}/lib/systemd/system
mkdir -p %{buildroot}/%{_libexecdir}
cp %{SOURCE1} %{buildroot}/%{_libexecdir}/.
cp %{SOURCE2} %{buildroot}/lib/systemd/system/ipmi.service
chmod 755 %{buildroot}/%{_libexecdir}/openipmi-helper
install -vdm755 %{buildroot}%{_libdir}/systemd/system-preset
echo "disable ipmi.service" > %{buildroot}%{_libdir}/systemd/system-preset/50-ipmi.preset

#The build VM does not support ipmi.
#%%check
#make %{?_smp_mflags} check

%preun
%systemd_preun ipmi.service

%post
/sbin/ldconfig
%systemd_post ipmi.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart ipmi.service

%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/libOpenIPMIcmdlang.so.*
%{_libdir}/libOpenIPMIposix.so.*
%{_libdir}/libOpenIPMIpthread.so.*
%{_libdir}/libOpenIPMI.so.*
%{_libdir}/libOpenIPMIutils.so.*
%license COPYING COPYING.LIB
%doc FAQ INSTALL README README.Force
%license COPYING.BSD
%doc README.MotorolaMXP CONFIGURING_FOR_LAN
%exclude %{_sysconfdir}/init.d/ipmi
%config(noreplace) %{_sysconfdir}/sysconfig/ipmi
%{_libexecdir}/*
/lib/systemd/system/ipmi.service
%{_libdir}/systemd/system-preset/50-ipmi.preset

%files perl
%defattr(-,root,root)
%{perl_vendorarch}
%doc swig/OpenIPMI.i swig/perl/sample swig/perl/ipmi_powerctl

%files python
%defattr(-,root,root)
%{python3_sitelib}/*OpenIPMI.*
%{python3_sitelib}/__pycache__/*
%doc swig/OpenIPMI.i

%files devel
%defattr(-,root,root)
%{_includedir}/OpenIPMI
%{_libdir}/*.so
%{_libdir}/pkgconfig
%doc doc/IPMI.pdf

%files ui
%defattr(-,root,root)
%{_bindir}/ipmi_ui
%{_bindir}/ipmicmd
%{_bindir}/openipmicmd
%{_bindir}/openipmi_eventd
%{_bindir}/ipmish
%{_bindir}/openipmish
%{_bindir}/solterm
%{_bindir}/rmcp_ping
%{_libdir}/libOpenIPMIui.so.*
%{_mandir}/man1/ipmi_ui.1*
%{_mandir}/man1/openipmicmd.1*
%{_mandir}/man1/openipmish.1*
%{_mandir}/man1/openipmigui.1*
%{_mandir}/man1/solterm.1*
%{_mandir}/man1/openipmi_eventd.1.gz
%{_mandir}/man1/rmcp_ping.1*
%{_mandir}/man7/ipmi_cmdlang.7*
%{_mandir}/man7/openipmi_conparms.7*

%files lanserv
%defattr(-,root,root)
%{_bindir}/ipmilan
%{_bindir}/ipmi_sim
%{_bindir}/sdrcomp
%{_libdir}/libIPMIlanserv.so.*
%config(noreplace) %{_sysconfdir}/ipmi/ipmisim1.emu
%config(noreplace) %{_sysconfdir}/ipmi/lan.conf
%{_mandir}/man8/ipmilan.8*
%{_mandir}/man1/ipmi_sim.1.gz
%{_mandir}/man5/ipmi_lan.5.gz
%{_mandir}/man5/ipmi_sim_cmd.5.gz

%changelog
* Tue Feb 22 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 2.0.32-1
- Upgrading to version 2.0.32.

* Mon Jan 31 2022 Olivia Crain <oliviacrain@microsoft.com> - 2.0.25-7
- Use python3 instead of python2 in python subpackage
- Add Fedora patch to enable build with python >= 3.9
- License verified

* Tue Mar 02 2021 Henry Li <lihl@microsoft.com> - 2.0.25-6
- Provides python3-openipmi from OpenIPMI-python

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.0.25-5
- Added %%license line automatically

* Fri Apr 17 2020 Nicolas Ontiveros <niontive@microsoft.com> 2.0.25-4
- Rename openipmi to OpenIPMI.
- Remove sha1 macro.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.0.25-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> 2.0.25-2
- Added BuildRequires python2-devel

* Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.0.25-1
- Upgrade to 2.0.25

* Fri Sep 15 2017 Xiaolin Li <xiaolinl@vmware.com> 2.0.24-2
- openipmi-devel requires ncurses-devel

* Mon Sep 11 2017 Xiaolin Li <xiaolinl@vmware.com> 2.0.24-1
- Initial build.  First version
