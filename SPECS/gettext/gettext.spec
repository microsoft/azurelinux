Summary:        Utilities for internationalization and localization
Name:           gettext
Version:        0.21
Release:        2%{?dist}
License:        GPLv3
URL:            https://www.gnu.org/software/gettext
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://ftp.gnu.org/gnu/gettext/%{name}-%{version}.tar.xz
Provides:       %{name}-devel = %{version}-%{release}

%description
These allow programs to be compiled with NLS
(Native Language Support), enabling them to output
messages in the user's native language.

%package common-devel
Summary: Common development files for %{name}
# autopoint archive
License: GPLv3+
BuildArch: noarch

%description common-devel
This package contains common architecture independent gettext development files.

%package libs
Summary: Libraries for %{name}
# libasprintf is LGPLv2+
# libgettextpo is GPLv3+
License: LGPLv2+ and GPLv3+

%description libs
This package contains libraries used internationalization support.

%prep
%setup -q

%build
export CFLAGS=" %{build_cflags} -Wno-error=format-security "
./configure \
	--prefix=%{_prefix} \
	--docdir=%{_defaultdocdir}/%{name}-%{version} \
	--disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}/usr/share/doc/gettext-%{version}/examples
rm -rf %{buildroot}%{_infodir}
%find_lang %{name} --all-name

%check
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig

%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_includedir}/*
%{_libdir}/gettext/*
%{_libdir}/*.so.*
%{_libdir}/*.so
%{_libdir}/*.a
%{_datarootdir}/aclocal/*
%{_datadir}/*
%{_defaultdocdir}/%{name}-%{version}/*
%{_datarootdir}/%{name}/*
%{_mandir}/*

%files common-devel
%{_datadir}/%{name}/archive.*.tar.xz

%files libs
%{_libdir}/libasprintf.so.0*
%{_libdir}/libgettextpo.so.0*
%{_libdir}/libgettextlib-0.*.so
%{_libdir}/libgettextsrc-0.*.so

%changelog
* Mon Sep 20 2021 Muhammad Falak <mwani@microsoft.com> 0.21-2
- Export subpackage `common-devel` & `libs`

* Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> 0.21-1
- Update to version 0.21.
- Update URL and Source0 to use https.
- Provide gettext-devel

* Thu Jun 11 2020 Henry Beberman <henry.beberman@microsoft.com> - 0.19.8.1-3
- Disable -Wno-error=format-security to build with hardened cflags

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 0.19.8.1-2
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 19.8.1-1
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 14 2018 Keerthana K <keerthanak@vmware.com> 0.19.8.1-1
- Update to version 0.19.8.1

* Wed Apr 05 2017 Danut Moraru <dmoraru@vmware.com> 0.19.8-1
- Upgrade to 0.19.8

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.19.5.1-2
- GA - Bump release of all rpms

* Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 0.19.5.1-1
- Updated to version 0.19.5.1

* Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 0.18.3.2-2
- Handled locale files with macro find_lang

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 0.18.3.2-1
- Initial build. First version
