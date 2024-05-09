Summary:        Key table files, console fonts, and keyboard utilities
Name:           kbd
Version:        2.2.0
Release:        2%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Applications/System
URL:            https://ftp.altlinux.org/pub/people/legion/kbd
Source0:        https://ftp.altlinux.org/pub/people/legion/kbd/%{name}-%{version}.tar.xz
Patch0:         kbd-2.0.4-backspace-1.patch

BuildRequires:  check >= 0.9.4

Conflicts:      toybox

Provides:       %{name}-misc = %{version}-%{release}

%description
The Kbd package contains key-table files, console fonts, and keyboard utilities.

%prep
%autosetup -p1
sed -i 's/\(RESIZECONS_PROGS=\)yes/\1no/g' configure
sed -i 's/resizecons.8 //'  docs/man/man8/Makefile.in
# /bin/ld: libfont.a(kdmapop.o):/usr/src/mariner/BUILD/kbd-2.0.4/src/version.h:8: multiple definition of `progname';
# mapscrn-mapscrn.o:/usr/src/mariner/BUILD/kbd-2.0.4/src/version.h:8: first defined here


%build
PKG_CONFIG_PATH=/tools/lib/pkgconfig \
%configure --disable-vlock --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}%{_defaultdocdir}/%{name}-%{version}
cp -R -v docs/doc/* %{buildroot}%{_defaultdocdir}/%{name}-%{version}
rm -f %{buildroot}%{_defaultdocdir}/%{name}-%{version}/kbd.FAQ*
%find_lang %{name}

%check
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_defaultdocdir}/%{name}-%{version}/*
%{_datarootdir}/consolefonts/*
%{_datarootdir}/consoletrans/*
%{_datarootdir}/keymaps/*
%{_datarootdir}/unimaps/*
%{_mandir}/*/*

%changelog
* Thu Feb 15 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.2.0-2
- Updated patch application macros.

* Fri Oct 22 2021 Andrew Phelps <anphel@microsoft.com> - 2.2.0-1
- Update to version 2.2.0
- License verified

* Fri Sep 24 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.4-6
- Adding 'Provides' for 'kbm-misc'.
- Removing 'sha1' macro.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.0.4-5
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.0.4-4
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Oct 2 2018 Michelle Wang <michellew@vmware.com> - 2.0.4-3
- Add conflict toybox.

* Mon Sep 11 2017 Anish Swaminathan <anishs@vmware.com> - 2.0.4-2
- Remove FAQs from main package.

* Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> - 2.0.4-1
- Updated to version 2.0.4.

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.0.3-2
- GA - Bump release of all rpms.

* Wed Jan 13 2016 Xiaolin Li <xiaolinl@vmware.com> - 2.0.3-1
- Updated to version 2.0.3.

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> - 2.0.1-1
- Initial build First version.
