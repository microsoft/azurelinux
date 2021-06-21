%define  debug_package %{nil}

Summary:        Software Update for Embedded Systems
Name:           swupdate
Version:        2019.11
Release:        5%{?dist}
License:        GPLv2+
URL:            https://sbabic.github.io/swupdate/
Group:          System Environment/Base
Vendor:         Microsoft Corporation
Distribution:   Mariner
#Source0:       https://github.com/sbabic/swupdate/archive/%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Source1:        .config

BuildRequires:  curl-devel
BuildRequires:  json-c-devel
BuildRequires:  libconfig
BuildRequires:  systemd-devel
BuildRequires:  libarchive-devel
BuildRequires:  zeromq-devel
Requires:       curl
Requires:       json-c
Requires:       libconfig
Requires:       systemd
Requires:       libarchive
Requires:       zeromq

%description
SWUpdate is a Linux Update agent with the goal to provide an efficient and safe way to update an embedded system.
SWUpdate supports local and remote updates, multiple update strategies.

%package tools
Summary: swupdate tools
Group: System Environment/Base

%description tools
Supporter tools for SWUpdate

%package devel
Summary: Development Libraries for swupdate
Group: Development/Libraries
Requires: swupdate = %{version}-%{release}

%description devel
This package contains symbolic links, header files,
and related items necessary for software development.

%prep
%setup -q
cp %{SOURCE1} .

%build
# Configure accordingly.
make %{?_smp_mflags}

%install
make install    DESTDIR=$RPM_BUILD_ROOT \
                HAVE_LUA=n

%pre
# swupdate - preinst
#!/bin/sh
if true && [ -z "$D" -a -f "/etc/init.d/swupdate" ]; then
    /etc/init.d/swupdate stop || :
fi
if true && type update-rc.d >/dev/null 2>/dev/null; then
    if [ -n "$D" ]; then
        OPT="-f -r $D"
    else
        OPT="-f"
    fi
    update-rc.d $OPT swupdate remove
fi


%post
# swupdate - postinst
#!/bin/sh
if true && type update-rc.d >/dev/null 2>/dev/null; then
    if [ -n "$D" ]; then
        OPT="-r $D"
    else
        OPT="-s"
    fi
    update-rc.d $OPT swupdate defaults 70
fi


%preun
# swupdate - prerm
#!/bin/sh
if [ "$1" = "0" ] ; then
if true && [ -z "$D" -a -x "/etc/init.d/swupdate" ]; then
    /etc/init.d/swupdate stop || :
fi
fi

%postun
# swupdate - postrm
#!/bin/sh
if [ "$1" = "0" ] ; then
if true && type update-rc.d >/dev/null 2>/dev/null; then
    if [ -n "$D" ]; then
        OPT="-f -r $D"
    else
        OPT="-f"
    fi
    update-rc.d $OPT swupdate remove
fi
fi

%files
%defattr(-,-,-,-)
%license Licenses
%dir "/usr"
%dir "/usr/bin"
"/usr/bin/swupdate"

%files tools
%defattr(-,-,-,-)
%dir "/usr"
%dir "/usr/bin"
"/usr/bin/swupdate-client"
"/usr/bin/swupdate-progress"
"/usr/bin/swupdate-sendtohawkbit"
"/usr/bin/swupdate-hawkbitcfg"
"/usr/bin/swupdate-sysrestart"


%files devel
%defattr(-,-,-,-)
%dir "/usr"
%dir "/usr/include"
"/usr/include/progress_ipc.h"
"/usr/include/network_ipc.h"
"/usr/include/swupdate_status.h"
%dir "/usr/lib"
"/usr/lib/libswupdate.a"


%changelog
*   Tue Jun 09 2020 Daniel McIlvaney <damcilva@microsoft.com> 2019.11-5
-   Use Grub on aarch64 systems to abstract firmware (no longer require U-Boot)

*   Thu May 28 2020 Emre Girgin <mrgirgin@microsoft.com> 2019.11-4
-   Remove the ifarch clause around Patch0 to unify the SRPM files accross architectures.

*   Sat May 09 00:20:47 PST 2020 Nick Samson <nisamson@microsoft.com> - 2019.11-3
-   Added %%license line automatically

*   Thu Apr 23 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 2019.11-2
-   License verified.
-   Fixed 'Source0' tag.

*   Fri Dec 27 2019 Emre Girgin <mrgirgin@microsoft.com> 2019.11-1
-   Original version for CBL-Mariner.
