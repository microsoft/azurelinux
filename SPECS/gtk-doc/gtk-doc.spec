%global debug_package %{nil}

Summary:        Program to generate documenation
Name:           gtk-doc
Version:        1.29
Release:        6%{?dist}
License:        GPLv2+ and GFDL
URL:            https://www.gtk.org/
Source0:        https://ftp.gnome.org/pub/gnome/sources/%{name}/%{version}/%{name}-%{version}.tar.xz
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner

Requires:       libxslt
Requires:       docbook-dtd-xml
Requires:       docbook-style-xsl
Requires:       python3

BuildRequires:  docbook-dtd-xml >= 4.5
BuildRequires:  docbook-style-xsl >= 1.78.1
BuildRequires:  itstool >= 2.0.2
BuildRequires:  libxslt >= 1.1.28
BuildRequires:  cmake
BuildRequires:  check
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Provides:       perl(gtkdoc-common.pl)

BuildArch:      noarch

%description
The GTK-Doc package contains a code documenter. This is useful for extracting
specially formatted comments from the code to create API documentation.
%prep
%setup -q
%build
%configure --disable-silent-rules CFLAGS="%{build_cflags}"
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} sysconfdir=%{_sysconfdir} datadir=%{_datadir} install

%check
cd tests && make check-TESTS

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
/usr/share/*
%{_libdir}/cmake/

%changelog
* Sat May 09 00:20:38 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.29-6
- Added %%license line automatically

* Tue May 05 2020 Emre Girgin <mrgirgin@microsoft.com> 1.29-5
- Renaming docbook-xsl to docbook-style-xsl
* Tue May 05 2020 Emre Girgin <mrgirgin@microsoft.com> 1.29-4
- Renaming docbook-xml to docbook-dtd-xml
* Wed Mar 25 2020 Paul Monson <paulmon@microsoft.com> 1.29-3
- Fix URL. Fix Source0 URL. License verified.
* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.29-2
- Initial CBL-Mariner import from Photon (license: Apache2).
* Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com>  1.29-1
- Upgrade to 1.29
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.25-2
- Fix arch
* Fri Mar 24 2017 Dheeraj Shetty <dheerajs@vmware.com>  1.25-1
- Upgrade to 1.25
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.24-3
- GA - Bump release of all rpms
* Thu Feb 25 2016 Anish Swaminathan <anishs@vmware.com>  1.24-1
- Upgrade to 1.24
* Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 1.21.1-2
- Updated group.
* Mon Nov 24 2014 Divya Thaluru <dthaluru@vmware.com> 1.21-1
- Initial build. First version
