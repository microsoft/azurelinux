Summary:       Intltool
Name:          intltool
Version:       0.51.0
Release:       7%{?dist}
License:       GPLv2+
URL:           https://freedesktop.org/wiki/Software/intltool/
Source0:       https://launchpad.net/%{name}/trunk/%{version}/+download/%{name}-%{version}.tar.gz
Group:         Development/Tools
Vendor:        Microsoft Corporation
Distribution:  Mariner
Requires:      perl-XML-Parser
BuildRequires: perl-XML-Parser
BuildArch:     noarch

%description
The Intltool is an internationalization tool used for extracting translatable strings from source files.
%prep
%setup -q
%build
./configure --prefix=%{_prefix}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -v -Dm644 doc/I18N-HOWTO %{buildroot}/%{_docdir}/%{name}-%{version}/I18N-HOWTO

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%license COPYING
%{_docdir}/%{name}-%{version}/I18N-HOWTO
%{_bindir}/*
%{_datadir}/aclocal/intltool.m4
%{_datadir}/intltool/*
%{_mandir}/man8/*

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.51.0-7
- Added %%license line automatically

*   Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 0.51.0-6
-   Renaming XML-Parser to perl-XML-Parser
*   Wed Apr 08 2020 Joe Schmitt <joschmit@microsoft.com> 0.51.0-5
-   Update Source0 with valid URL.
-   Remove sha1 macro.
-   License verified.
-   Fix changelog styling.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.51.0-4
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.51.0-3
-   Fix arch
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.51.0-2
-   GA - Bump release of all rpms
*   Thu Feb 25 2016 Anish Swaminathan <anishs@vmware.com>  0.51.0-1
-   Upgrade to 0.51.0
*   Thu Oct 23 2014 Divya Thaluru <dthaluru@vmware.com> 0.50.2-1
-   Initial version
