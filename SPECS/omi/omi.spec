%define      debug_package %{nil}

Name:          omi
Version:       1.6.6
Release:       1%{?dist}
Summary:       Open Management Infrastructure
Group:         Productivity/Security
License:       MIT
Vendor:        Microsoft Corporation
Distribution:  Mariner
URL:           https://github.com/microsoft/omi
#Source0: https://github.com/microsoft/%{name}/archive/v%{version}-0.tar.gz
Source0:       %{name}-%{version}.tar.gz
Patch0:        buildtool.patch
BuildRequires: pam-devel
BuildRequires: sudo
BuildRequires: unzip
BuildRequires: which
BuildRequires: krb5-devel
BuildRequires: e2fsprogs-devel


%description
Open Management Infrastructure (OMI) is an open source project to 
further the development of a production quality implementation of 
the DMTF CIM/WBEM standards.


%prep
%setup -n %{name}-%{version}-0
%patch0 -p1


%build
cd Unix
chmod 7777 *
./configure --enable-microsoft
make

%install
cd Unix
make install

install -vdm 755 %{buildroot}/opt/omi
install -vdm 775 %{buildroot}/opt/omi/lib
install -vdm 755 %{buildroot}/usr/include/micxx
install -vdm 755 %{buildroot}/usr/include/omiclient
install -vdm 755 %{buildroot}/usr/include/pal
install -vdm 755 %{buildroot}/usr/include/nits
install -vdm 755 %{buildroot}/usr/include/nits/base
install -vdm 755 %{buildroot}/usr/include/linux

install -m 755 output/lib/libmicxx.so %{buildroot}/opt/omi/lib/
install -m 755 output/lib/libomiclient.so %{buildroot}/opt/omi/lib/
install -m 755 output/lib/libmi.so %{buildroot}/opt/omi/lib/
install -m 755 output/lib/libomiidentify.so %{buildroot}/opt/omi/lib/

install -m 644 micxx/* %{buildroot}/usr/include/micxx
install -m 644 omiclient/client.h %{buildroot}/usr/include/omiclient
install -m 644 omiclient/*.h output/include/config.h common/*.h %{buildroot}/usr/include/
install -m 644 pal/*.h %{buildroot}/usr/include/pal
install -m 644 nits/base/nits.h %{buildroot}/usr/include/nits/base
install -m 644 common/linux/sal.h %{buildroot}/usr/include/linux/

sudo sed -i -e 's/\"..\/..\/common\/linux\/sal.h"/<linux\/sal.h>/g' %{buildroot}/usr/include/pal/palcommon.h


%files
%defattr(-,root,root)
/opt/omi/lib/libmicxx.so
/opt/omi/lib/libomiclient.so
/opt/omi/lib/libmi.so
/opt/omi/lib/libomiidentify.so
/usr/include/micxx/*
/usr/include/omiclient/client.h
/usr/include/*
/usr/include/pal/*.h
/usr/include/nits/base/nits.h
/usr/include/linux/sal.h


%changelog
* Thu Oct 22 2020 Nick Samson <nick.samson@microsoft.com> 1.6.6-1
- Updated source and version
* Mon Sep 28 2020 Henry Li <lihl@microsoft.com>   1.0.8-1
- Add runtime required rpm
