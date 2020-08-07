Summary:	Programs for generating Makefiles
Name:		automake
Version:	1.16.1
Release:        3%{?dist}
License:	GPLv2+
URL:		http://www.gnu.org/software/automake/
Group:		System Environment/Base
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:	http://ftp.gnu.org/gnu/automake/%{name}-%{version}.tar.xz
%define sha1 automake=1012bc79956013d53da0890f8493388a6cb20831
BuildRequires:	autoconf
BuildArch:      noarch

%description
Contains programs for generating Makefiles for use with Autoconf.
%prep
%setup -q
%build
sed -i 's:/\\\${:/\\\$\\{:' bin/automake.in
./configure \
	--prefix=%{_prefix} \
	--docdir=%{_defaultdocdir}/%{name}-%{version} \
	--disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_infodir}

%check
sed -i "s:./configure:LEXLIB=/usr/lib/libfl.a &:" t/lex-{clean,depend}-cxx.sh
sed -i "s|test ! -s stderr||g" t/distcheck-no-prefix-or-srcdir-override.sh
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_datarootdir}/aclocal/README
%{_datarootdir}/%{name}-1.16/*
%{_datarootdir}/aclocal-1.16/*
%{_defaultdocdir}/%{name}-%{version}/*
%{_mandir}/*/*
%changelog
* Sat May 09 00:21:00 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.16.1-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.16.1-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Thu Sep 06 2018 Anish Swaminathan <anishs@vmware.com> 1.16.1-1
-   Update version to 1.16.1
*	Tue Jan 02 2018 Alexey Makhalov <amakhalov@vmware.com> 1.15.1-1
-	Version update
*	Fri Aug 04 2017 Danut Moraru <dmoraru@vmware.com> 1.15-4
-	Disable check that fails test case
*	Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.15-3
-	Fix arch
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.15-2
-	GA - Bump release of all rpms
*	Thu Jul 23 2015 Divya Thaluru <dthaluru@vmware.com> 1.15-1
-	Updated to version 1.15
*	Wed Jun 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.14.1-2
-	Adding autoconf package to build time requires packages
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.14.1-1
-	Initial build. First version
