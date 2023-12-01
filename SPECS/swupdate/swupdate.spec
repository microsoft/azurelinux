Summary:        Software Update for Embedded Systems
Name:           swupdate
Version:        2021.04
Release:        1%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://sbabic.github.io/swupdate/
Source0:        https://github.com/sbabic/swupdate/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        .config
BuildRequires:  curl-devel
BuildRequires:  json-c-devel
BuildRequires:  libarchive-devel
BuildRequires:  libconfig-devel
BuildRequires:  systemd-devel
BuildRequires:  zeromq-devel
Requires:       curl
Requires:       json-c
Requires:       libarchive
Requires:       libconfig
Requires:       systemd
Requires:       zeromq

%description
SWUpdate is a Linux Update agent with the goal to provide an efficient and safe way to update an embedded system.
SWUpdate supports local and remote updates, multiple update strategies.

%package        tools
Summary:        swupdate tools
Group:          System Environment/Base

%description    tools
Supporter tools for SWUpdate

%package        devel
Summary:        Development Libraries for swupdate
Group:          Development/Libraries
Requires:       swupdate = %{version}-%{release}

%description devel
This package contains symbolic links, header files,
and related items necessary for software development.

%prep
%setup -q
cp %{SOURCE1} .

%build
# Configure accordingly.
make %{?_smp_mflags} SKIP_STRIP=y

%install
make install    DESTDIR=%{buildroot} \
                SKIP_STRIP=y            \
                HAVE_LUA=n

%pre
# swupdate - preinst
#!/bin/sh
if true && [ -z "$D" -a -f "%{_sysconfdir}/init.d/swupdate" ]; then
    %{_sysconfdir}/init.d/swupdate stop || :
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
if true && [ -z "$D" -a -x "%{_sysconfdir}/init.d/swupdate" ]; then
    %{_sysconfdir}/init.d/swupdate stop || :
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
%license LICENSES
%dir "%{_prefix}"
%dir "%{_bindir}"
"%{_bindir}/swupdate"

%files tools
%defattr(-,-,-,-)
%dir "%{_prefix}"
%dir "%{_bindir}"
"%{_bindir}/swupdate-client"
"%{_bindir}/swupdate-progress"
"%{_bindir}/swupdate-sendtohawkbit"
"%{_bindir}/swupdate-hawkbitcfg"
"%{_bindir}/swupdate-sysrestart"

%files devel
%defattr(-,-,-,-)
%dir "%{_prefix}"
%dir "%{_includedir}"
"%{_includedir}/progress_ipc.h"
"%{_includedir}/network_ipc.h"
"%{_includedir}/swupdate_status.h"
%dir "%{_libdir}"
%{_libdir}/libswupdate.so
%{_libdir}/libswupdate.so.*

%changelog
* Tue Jan 18 2022 Daniel McIlvaney <damcilva@microsoft.com> - 2021.04-1
- Update to version 2021.04.

* Tue Jun 29 2021 Olivia Crain <oliviacrain@microsoft.com> - 2019.11-7
- Use libconfig-devel at build-time, instead of libconfig

* Fri Sep 25 2020 Emre Girgin <mrgirgin@microsoft.com> - 2019.11-6
- Disable debug symbol stripping in .config, and create the debuginfo package.

* Tue Jun 09 2020 Daniel McIlvaney <damcilva@microsoft.com> - 2019.11-5
- Use Grub on aarch64 systems to abstract firmware (no longer require U-Boot)

* Thu May 28 2020 Emre Girgin <mrgirgin@microsoft.com> - 2019.11-4
- Remove the ifarch clause around Patch0 to unify the SRPM files accross architectures.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2019.11-3
- Added %%license line automatically

* Thu Apr 23 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 2019.11-2
- License verified.
- Fixed 'Source0' tag.

* Fri Dec 27 2019 Emre Girgin <mrgirgin@microsoft.com> - 2019.11-1
- Original version for CBL-Mariner.
