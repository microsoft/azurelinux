%define      debug_package %{nil}
Summary:        Auditd plugin that forwards audit events to OMS Agent for Linux
Name:           auoms
Version:        2.2.5
Release:        7%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://github.com/microsoft/OMS-Auditd-Plugin
#Source0:       https://github.com/microsoft/OMS-Auditd-Plugin/archive/v2.2.5-0.tar.gz
Source0:        %{name}-%{version}.tar.gz
#Source1:       https://github.com/microsoft/pal/archive/v1.6.6-0.tar.gz
Source1:        pal-1.6.6-0.tar.gz
#Source2:       https://github.com/msgpack/msgpack-c/archive/cpp-2.0.0.zip
Source2:        msgpack-c-cpp-2.0.0.zip
#Source3:       https://github.com/Tencent/rapidjson/archive/v1.0.2.tar.gz
Source3:        rapidjson-1.0.2.tar.gz
Patch0:         auoms.patch
BuildRequires:  audit-devel
BuildRequires:  bash
BuildRequires:  bash-devel
BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  grep
BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  sed
BuildRequires:  sudo
BuildRequires:  unzip
BuildRequires:  wget
Requires:       audit
Requires:       bash
Requires:       chkconfig
Requires:       glibc
Requires:       initscripts
Requires:       libstdc++
Requires:       perl
Requires:       procps-ng
Requires:       sed
Requires:       sudo

%description
OMS Audit data collection daemon

%prep
tar xf %{SOURCE1} --no-same-owner --one-top-level=pal --strip-components 1
cp %{SOURCE2} ./
cp %{SOURCE3} ./
%setup -q -n OMS-Auditd-Plugin-2.2.5-0
%patch0 -p1
# Fix gcc11 compilation errors
sed -i 's#throw#throw;//throw#g' TranslateSyscall.cpp
sed -i 's/#include <cstring>/#include <string>\n#include <cstring>/g' AuditRules.h
sed -i 's#throw#throw;//throw#g' AuditRules.h

%build
grep AUOMS_BUILDVERSION auoms.version | head -n 4 | cut -d'=' -f2 | tr '\n' '.' | sed 's/.$//' | sed 's/^/#define AUOMS_VERSION "/' > auoms_version.h
sed -i 's/$/"/' auoms_version.h
cp -R %{_includedir}/boost /usr/local/include/boost
mv %{_includedir}/boost /usr/include/boost148
cd build
./configure --enable-ulinux && make clean && make

%install
install -vdm 755 %{buildroot}%{_sysconfdir}/init.d
install -vdm 755 %{buildroot}%{_sysconfdir}/opt/microsoft/auoms
install -vdm 755 %{buildroot}%{_sysconfdir}/opt/microsoft/auoms/outconf.d
install -vdm 755 %{buildroot}%{_sysconfdir}/opt/microsoft/auoms/rules.d
install -vdm 755 %{buildroot}/opt/microsoft/auoms
install -vdm 755 %{buildroot}/opt/microsoft/auoms/bin
install -vdm 755 %{buildroot}%{_datadir}/selinux/packages/auoms
install -vdm 750 %{buildroot}%{_var}/opt/microsoft/auoms/data
install -vdm 750 %{buildroot}%{_var}/opt/microsoft/auoms/data/outputs

install -m 644 intermediate/selinux/*                           %{buildroot}%{_datadir}/selinux/packages/auoms
install -m 555 installer/auoms.init                             %{buildroot}%{_sysconfdir}/init.d/auoms
install -m 644 installer/conf/auoms.conf                        %{buildroot}%{_sysconfdir}/opt/microsoft/auoms
install -m 644 installer/conf/auomscollect.conf                 %{buildroot}%{_sysconfdir}/opt/microsoft/auoms
install -m 644 installer/conf/example_output.conf               %{buildroot}%{_sysconfdir}/opt/microsoft/auoms
install -m 444 ./LICENSE                                        %{buildroot}/opt/microsoft/auoms
install -m 444 ./THIRD_PARTY_IP_NOTICE                          %{buildroot}/opt/microsoft/auoms
install -m 444 installer/auoms.service                          %{buildroot}/opt/microsoft/auoms
install -m 755 intermediate/builddir/release/bin/auomscollect   %{buildroot}/opt/microsoft/auoms/bin
install -m 755 intermediate/builddir/release/bin/auoms          %{buildroot}/opt/microsoft/auoms/bin
install -m 755 intermediate/builddir/release/bin/auomsctl       %{buildroot}/opt/microsoft/auoms/bin

%pre
#!/bin/sh

if [ $1 -gt 1 ] ; then
    if [ -e %{_sysconfdir}/audisp/plugins.d/auoms.conf ]; then
        echo "Pre: found etc/audisp/plugins.d/auoms.conf"
        if [ -e %{_sysconfdir}/audisp/plugins.d/auoms.conf.auomssave ]; then
            rm %{_sysconfdir}/audisp/plugins.d/auoms.conf.auomssave
        fi
        cp -p %{_sysconfdir}/audisp/plugins.d/auoms.conf %{_sysconfdir}/audisp/plugins.d/auoms.conf.auomssave
    fi
    if [ -e %{_sysconfdir}/audit/plugins.d/auoms.conf ]; then
        echo "Pre: found etc/audit/plugins.d/auoms.conf"
        if [ -e %{_sysconfdir}/audit/plugins.d/auoms.conf.auomssave ]; then
            rm %{_sysconfdir}/audit/plugins.d/auoms.conf.auomssave
        fi
        cp -p %{_sysconfdir}/audit/plugins.d/auoms.conf %{_sysconfdir}/audit/plugins.d/auoms.conf.auomssave
    fi
fi

%preun
#!/bin/sh

if [ $1 -eq 0 ]; then
    /opt/microsoft/auoms/bin/auomsctl disable
fi

%post
#!/bin/sh

SERVICEDIR=/opt/microsoft/auoms

if [ $1 -gt 1 ] ; then
    if [ -e %{_sysconfdir}/audisp/plugins.d/auoms.conf.auomssave ]; then
        echo "Post: found %{_sysconfdir}/audisp/plugins.d/auoms.conf"
        if [ -e %{_sysconfdir}/audisp/plugins.d/auoms.conf ]; then
            rm %{_sysconfdir}/audisp/plugins.d/auoms.conf
        fi
        cp -p %{_sysconfdir}/audisp/plugins.d/auoms.conf.auomssave %{_sysconfdir}/audisp/plugins.d/auoms.conf
    fi
    if [ -e %{_sysconfdir}/audit/plugins.d/auoms.conf.auomssave ]; then
        echo "Post: found %{_sysconfdir}/audit/plugins.d/auoms.conf"
        if [ -e %{_sysconfdir}/audit/plugins.d/auoms.conf ]; then
            rm %{_sysconfdir}/audit/plugins.d/auoms.conf
        fi
        cp -p %{_sysconfdir}/audit/plugins.d/auoms.conf.auomssave %{_sysconfdir}/audit/plugins.d/auoms.conf
    fi
    echo "Post: executing upgrade"
    /opt/microsoft/auoms/bin/auomsctl upgrade
fi
for dir in %{_libdir}/systemd/system /lib/systemd/system; do
    if [ -e $dir ]; then
        install -m 644 ${SERVICEDIR}/auoms.service $dir
        systemctl enable auoms.service
        break
    fi
done
sudo /opt/microsoft/auoms/bin/auomsctl enable
rm -f %{_sysconfdir}/audisp/plugins.d/auoms.conf.*
rm -f %{_sysconfdir}/audit/plugins.d/auoms.conf.*

%postun
#!/bin/sh

if [ $1 -eq 0 ]; then
    rm -f %{_sysconfdir}/audisp/plugins.d/auoms.conf*
    rm -f %{_sysconfdir}/audit/plugins.d/auoms.conf*

    rm -rf -v %{_sysconfdir}/opt/microsoft/auoms
    rm -rf -v %{_var}/opt/microsoft/auoms
fi
for dir in %{_libdir}/systemd/system /lib/systemd/system; do
    if [ -e ${dir}/auoms.service ]; then
        systemctl disable auoms.service
        rm -f ${dir}/auoms.service
        break
    fi
done

%files
%defattr(-,root,root)
%{_datadir}/selinux/packages/auoms
%{_datadir}/selinux/packages/auoms/*
%{_sysconfdir}/init.d/auoms
%{_sysconfdir}/opt/microsoft/auoms
%{_sysconfdir}/opt/microsoft/auoms/auoms.conf
%{_sysconfdir}/opt/microsoft/auoms/auomscollect.conf
%{_sysconfdir}/opt/microsoft/auoms/example_output.conf
%{_sysconfdir}/opt/microsoft/auoms/outconf.d
%{_sysconfdir}/opt/microsoft/auoms/rules.d
/opt/microsoft/auoms
%license /opt/microsoft/auoms/LICENSE
%license /opt/microsoft/auoms/THIRD_PARTY_IP_NOTICE
/opt/microsoft/auoms/auoms.service
/opt/microsoft/auoms/bin
/opt/microsoft/auoms/bin/auomscollect
/opt/microsoft/auoms/bin/auoms
/opt/microsoft/auoms/bin/auomsctl
%{_var}/opt/microsoft/auoms
%{_var}/opt/microsoft/auoms/data
%{_var}/opt/microsoft/auoms/data/outputs

%changelog
* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.2.5-7
- Removing the explicit %%clean stage.

* Fri Nov 12 2021 Andrew Phelps <anphel@microsoft.com> - 2.2.5-6
- Fix gcc11 compilation issues
- License verified

* Mon Apr 26 2021 Thomas Crain <thcrain@microsoft.com> - 2.2.5-5
- Replace incorrect %%{_lib} usage with %%{_libdir}

* Wed Nov 11 2020 Daniel McIlvaney <damcilva@microsoft.com> - 2.2.5-4
- Add dependnecy on chkconfig to avoid ownership conflict with /etc/init.d directory
- Add dependency on procps-ng so auomsctl can use pgrep
- Add dependnecy on initscripts so auomsctl can use /usr/sbin/service

* Wed Nov 11 2020 Daniel McIlvaney <damcilva@microsoft.com> - 2.2.5-3
- Clean up spec file with feedback from linter

* Sat Oct 24 2020 Andrew Phelps <anphel@microsoft.com> 2.2.5-2
- Fix setup macro

* Thu Oct 22 2020 Andrew Phelps <anphel@microsoft.com> 2.2.5-1
- Original version for CBL-Mariner.
