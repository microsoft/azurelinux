Summary:        ALSA Utilities.
Name:           alsa-utils
Version:        1.2.6
Release:        2%{?dist}
License:        GPLv2+
URL:            https://alsa-project.org
Group:          Applications/Internet
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://www.alsa-project.org/files/pub/utils/%{name}-%{version}.tar.bz2
Patch0:         ens1371.patch
BuildRequires:  alsa-lib-devel >= %{version}
BuildRequires:  ncurses-devel
Requires:       kernel-drivers-sound ncurses
Requires:       alsa-lib ncurses >= %{version}
%description
The ALSA Utilities package contains various utilities which are useful
for controlling your sound card.

%prep
%setup -q
%patch0 -p1

%build
%configure --disable-alsaconf --disable-xmlto
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
install -d -m 755 $RPM_BUILD_ROOT/var/lib/alsa

%post
alsactl init
alsactl -L store

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_libdir}/*
%exclude %{_libdir}/debug/
/lib/*
%{_sbindir}/*
%{_datadir}/*
%{_localstatedir}/*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.2.6-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Tue Jan 4 2022 Nicolas Guibourge <nicolasg@microsoft.com> 1.2.6-1
- Update to version 1.2.6
- License verified
* Fri May 29 2020 Andrew Phelps <anphel@microsoft.com> 1.2.2-1
- Update to version 1.2.2 to fix CVE-2009-0035
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.1.9-3
- Added %%license line automatically
* Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> 1.1.9-2
- Renaming linux to kernel
* Thu Mar 19 2020 Emre Girgin <mrgirgin@microsoft.com> 1.1.9-1
- Update version to 1.1.9. Correct license info.
* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.1.7-2
- Initial CBL-Mariner import from Photon (license: Apache2).
* Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.1.7-1
- initial version, moved from Vivace
