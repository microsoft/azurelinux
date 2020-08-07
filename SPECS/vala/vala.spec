%define majver %(echo %version | cut -d. -f 1-2)

Summary:        Compiler for the Vala programming language
Name:           vala
Version:        0.34.6
Release:        2%{?dist}
URL:            https://wiki.gnome.org/Projects/Vala
Group:          Development/Languages
License:        LGPL
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        http://download.gnome.org/sources/vala/%{majver}/vala-%{version}.tar.xz

BuildRequires: glib-devel
BuildRequires: glibc-devel

%description
Vala is a programming language using modern high level abstractions without imposing additional
runtime requirements and without using a different ABI compared to applications and libraries
written in C.

%package devel
Group:         Development/Libraries
Summary:       Static libraries and headers for Vala.
Requires:      %{name} = %{version}-%{release}

%description devel
%{summary}

%package tools
Group:         Development/Languages
Summary:       Tools for creating projects and bindings for Vala.
Requires:      %{name} = %{version}-%{release}

%description tools
%{summary}

%prep
%setup -q

%build
%configure --enable-vapigen
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%dir %{_datadir}/vala-%{majver}
%doc AUTHORS COPYING THANKS
%{_datadir}/vala-%{majver}/*
%{_libdir}/libvala-*.so.*

%files devel
%defattr(-,root,root)
%dir %{_includedir}/vala-*/
%doc ChangeLog NEWS README
%{_datadir}/aclocal/vala.m4
%{_datadir}/aclocal/vapigen.m4
%{_datadir}/vala/Makefile.vapigen
%{_includedir}/vala-*/*.h
%{_libdir}/libvala-*.la
%{_libdir}/libvala-*.so
%{_libdir}/pkgconfig/libvala-*.pc
%{_libdir}/pkgconfig/vapigen-%{majver}.pc
%{_libdir}/pkgconfig/vapigen.pc

%files tools
%defattr(-,root,root)
%{_bindir}/vala
%{_bindir}/vala-%{majver}
%{_bindir}/vala-gen-introspect
%{_bindir}/vala-gen-introspect-%{majver}
%{_bindir}/valac
%{_bindir}/valac-%{majver}
%{_bindir}/vapigen*
%{_bindir}/vapicheck*
%{_libdir}/vala-*
%{_mandir}/man1/vala-gen-introspect*
%{_mandir}/man1/valac*
%{_mandir}/man1/vapigen*

%changelog
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 0.34.6-2
-   Added %%license line automatically

*	Mon Apr 06 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.34.6-1
-	Original version for CBL-Mariner.