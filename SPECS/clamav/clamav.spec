%{!?python2_sitelib: %global python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Open source antivirus engine
Name:           clamav
Version:        0.103.0
Release:        1%{?dist}
License:        ASL 2.0 and BSD and bzip2-1.0.4 and GPLv2 and LGPLv2+ and MIT and Public Domain and UnRar
Group:          System Environment/Security
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.clamav.net
Source0:        %{url}/downloads/production/%{name}-%{version}.tar.gz

BuildRequires:  libtool
BuildRequires:  zlib-devel
# Workaround for coreutils missing requirement flex 
BuildRequires:  flex-devel
# Required to produce systemd files
BuildRequires:  systemd-devel
BuildRequires:  openssl-devel
Requires:       zlib
Requires:       openssl

%description
ClamAV® is an open source (GPL) anti-virus engine used in a variety of situations
including email scanning, web scanning, and end point security. It provides a number
of utilities including a flexible and scalable multi-threaded daemon, a command
line scanner and an advanced tool for automatic database updates.

%prep
%setup -q

%build
%configure

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%check
make %{?_smp_mflags} check

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING COPYING.bzip2 COPYING.file COPYING.getopt COPYING.LGPL COPYING.llvm COPYING.lzma COPYING.pcre COPYING.regex COPYING.unrar COPYING.YARA COPYING.zlib
%{_bindir}/*
%{_sysconfdir}/*.sample
%{_includedir}/*.h
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
/lib/systemd/*
%{_sbindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*


%changelog
* Tue Oct 27 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.103.0-1
- Updating to 0.103.0 to fix: CVE-2019-12625, CVE-2019-15961.
* Mon Oct 19 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.101.2-3
- License verified.
- Added %%license macro.
- Switching to using the %%configure macro.
- Extended package's summary and description.
* Wed Oct 02 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.101.2-2
- Fix vendor and distribution. Add systemd files to the list.
* Thu Jul 25 2019 Chad Zawistowski <chzawist@microsoft.com> 0.101.2-1
- Initial CBL-Mariner import from Azure.
