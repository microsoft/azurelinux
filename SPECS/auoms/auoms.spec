%define      debug_package %{nil}

Summary:        Auditd plugin that forwards audit events to OMS Agent for Linux
Name:           auoms
Version:        2.2.5
Release:        1%{?dist}
License:        MIT
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
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner

BuildRequires:  unzip
BuildRequires:  cmake
BuildRequires:  wget
BuildRequires:  sudo
BuildRequires:  grep
BuildRequires:  sed
BuildRequires:  bash
BuildRequires:  bash-devel
BuildRequires:  audit-devel
BuildRequires:  boost-devel
BuildRequires:  python2
BuildRequires:  python2-devel

Requires:       audit
Requires:       sudo
Requires:       bash
Requires:       sed
Requires:       libstdc++
Requires:       perl
Requires:       glibc

%description
OMS Audit data collection daemon

%prep
tar xf %{SOURCE1} --no-same-owner --one-top-level=pal --strip-components 1
cp %{SOURCE2} ./
cp %{SOURCE3} ./
%setup
%patch0 -p1

%build
grep AUOMS_BUILDVERSION auoms.version | head -n 4 | cut -d'=' -f2 | tr '\n' '.' | sed 's/.$//' | sed 's/^/#define AUOMS_VERSION "/' > auoms_version.h
sed -i 's/$/"/' auoms_version.h
cp -R /usr/include/boost /usr/local/include/boost
mv /usr/include/boost /usr/include/boost148
cd build
./configure --enable-ulinux && make clean && make

%install
install -vdm 755 %{buildroot}%{_sysconfdir}/init.d
install -vdm 755 %{buildroot}%{_sysconfdir}/opt/microsoft/auoms
install -vdm 755 %{buildroot}%{_sysconfdir}/opt/microsoft/auoms/outconf.d
install -vdm 755 %{buildroot}%{_sysconfdir}/opt/microsoft/auoms/rules.d
install -vdm 755 %{buildroot}/opt/microsoft/auoms
install -vdm 755 %{buildroot}/opt/microsoft/auoms/bin
install -vdm 755 %{buildroot}/usr/share/selinux/packages/auoms
install -vdm 750 %{buildroot}/var/opt/microsoft/auoms/data
install -vdm 750 %{buildroot}/var/opt/microsoft/auoms/data/outputs

install -m 644 intermediate/selinux/*                           %{buildroot}/usr/share/selinux/packages/auoms
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

%clean
rm -rf $RPM_BUILD_ROOT

%pre
#!/bin/sh

if [ $1 -gt 1 ] ; then
    if [ -e /etc/audisp/plugins.d/auoms.conf ]; then
        echo "Pre: found etc/audisp/plugins.d/auoms.conf"
        if [ -e /etc/audisp/plugins.d/auoms.conf.auomssave ]; then
            rm /etc/audisp/plugins.d/auoms.conf.auomssave
        fi
        cp -p /etc/audisp/plugins.d/auoms.conf /etc/audisp/plugins.d/auoms.conf.auomssave
    fi
    if [ -e /etc/audit/plugins.d/auoms.conf ]; then
        echo "Pre: found etc/audit/plugins.d/auoms.conf"
        if [ -e /etc/audit/plugins.d/auoms.conf.auomssave ]; then
            rm /etc/audit/plugins.d/auoms.conf.auomssave
        fi
        cp -p /etc/audit/plugins.d/auoms.conf /etc/audit/plugins.d/auoms.conf.auomssave
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
    if [ -e /etc/audisp/plugins.d/auoms.conf.auomssave ]; then
        echo "Post: found /etc/audisp/plugins.d/auoms.conf"
        if [ -e /etc/audisp/plugins.d/auoms.conf ]; then
            rm /etc/audisp/plugins.d/auoms.conf
        fi
        cp -p /etc/audisp/plugins.d/auoms.conf.auomssave /etc/audisp/plugins.d/auoms.conf
    fi
    if [ -e /etc/audit/plugins.d/auoms.conf.auomssave ]; then
        echo "Post: found /etc/audit/plugins.d/auoms.conf"
        if [ -e /etc/audit/plugins.d/auoms.conf ]; then
            rm /etc/audit/plugins.d/auoms.conf
        fi
        cp -p /etc/audit/plugins.d/auoms.conf.auomssave /etc/audit/plugins.d/auoms.conf
    fi
    echo "Post: executing upgrade"
    /opt/microsoft/auoms/bin/auomsctl upgrade
fi
for dir in /usr/lib/systemd/system /lib/systemd/system; do
    if [ -e $dir ]; then
        install -m 644 ${SERVICEDIR}/auoms.service $dir
        systemctl enable auoms.service
        break
    fi
done
sudo /opt/microsoft/auoms/bin/auomsctl enable
rm -f /etc/audisp/plugins.d/auoms.conf.*
rm -f /etc/audit/plugins.d/auoms.conf.*

%postun
#!/bin/sh

if [ $1 -eq 0 ]; then
    rm -f /etc/audisp/plugins.d/auoms.conf*
    rm -f /etc/audit/plugins.d/auoms.conf*

    rm -rf -v /etc/opt/microsoft/auoms
    rm -rf -v /var/opt/microsoft/auoms
fi
for dir in /usr/lib/systemd/system /lib/systemd/system; do
    if [ -e ${dir}/auoms.service ]; then
        systemctl disable auoms.service
        rm -f ${dir}/auoms.service
        break
    fi
done

%files
%defattr(-,root,root)
/usr/share/selinux/packages/auoms
/usr/share/selinux/packages/auoms/*
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
/var/opt/microsoft/auoms
/var/opt/microsoft/auoms/data
/var/opt/microsoft/auoms/data/outputs

%changelog
* Thu Oct 22 2020 Andrew Phelps <anphel@microsoft.com> 2.2.5-1
- Initial CBL-Mariner version.
