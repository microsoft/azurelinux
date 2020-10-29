Summary:	Library for accessing X.509 and CMS data structure.
Name:		libksba
Version:	1.3.5
Release:        4%{?dist}
License:	GPLv3+
URL:		https://www.gnupg.org/(fr)/download/index.html#libksba
Group:		Security/Libraries.
Source0:        https://www.gnupg.org/ftp/gcrypt/%{name}/%{name}-%{version}.tar.bz2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Provides:       %{name}-devel = %{version}-%{release}
BuildRequires:  libgpg-error-devel >= 1.2

%description
Libksba is a library to make the tasks of working with X.509 certificates,
CMS data and related objects more easy. It provides a highlevel interface
to the implemented protocols and presents the data in a consistent way.

%prep
%setup -q

%build
%configure --disable-static \
           --prefix=%{_prefix}
make

%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete

%check
make %{?_smp_mflags} -k check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/ksba-config
%{_libdir}/*.so*
%{_includedir}/*
%{_datadir}/aclocal/ksba.m4
%{_datadir}/info/ksba.info.gz
%exclude %{_datadir}/info/dir

%changelog
*   Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> 1.3.5-4
-   Provide libksba-devel for base package
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.3.5-3
-   Added %%license line automatically
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.3.5-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*	Tue	Apr 11 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.3.5-1
-	Udpated to version 1.3.5
*   Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 1.3.4-2
-   BuildRequired libgpg-error-devel.
*   Wed Jul 27 2016 Kumar Kaushik <kaushikk@vmware.com> 1.3.4-1
-   Initial Build.
