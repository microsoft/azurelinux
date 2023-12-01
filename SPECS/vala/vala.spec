%define majver %(echo %{version} | cut -d. -f 1-2)
Summary:        Compiler for the Vala programming language
Name:           vala
Version:        0.54.6
Release:        1%{?dist}
License:        LGPL
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://wiki.gnome.org/Projects/Vala
Source0:        http://download.gnome.org/sources/vala/%{majver}/vala-%{version}.tar.xz
BuildRequires:  glib-devel
BuildRequires:  glibc-devel
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  gobject-introspection-devel
BuildRequires:  libxslt
BuildRequires:  graphviz-devel

%description
Vala is a programming language using modern high level abstractions without imposing additional
runtime requirements and without using a different ABI compared to applications and libraries
written in C.

%package devel
Summary:        Static libraries and headers for Vala.
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
%{summary}

%package tools
Summary:        Tools for creating projects and bindings for Vala.
Group:          Development/Languages
Requires:       %{name} = %{version}-%{release}

%description tools
%{summary}

%package        doc
Summary:        Documentation for %{name}
License:        LGPLv2+
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
	
%description    doc
Vala is a new programming language that aims to bring modern programming
language features to GNOME developers without imposing any additional
runtime requirements and without using a different ABI compared to
applications and libraries written in C.
	
This package contains documentation in a devhelp HTML book.

%package -n valadoc
Summary:        Vala documentation generator
Requires:       %{name}%{?_isa} = %{version}-%{release}
	
%description -n valadoc
Valadoc is a documentation generator for generating API documentation from Vala
source code.

	
%package -n     valadoc-devel
Summary:        Development files for valadoc
Requires:       valadoc%{?_isa} = %{version}-%{release}
	
%description -n valadoc-devel
Valadoc is a documentation generator for generating API documentation from Vala
source code.
	
The valadoc-devel package contains libraries and header files for
developing applications that use valadoc.

%prep
%setup -q

%build
%configure --enable-vapigen
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete -print

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%dir %{_datadir}/vala-%{majver}
%doc AUTHORS THANKS
%{_datadir}/vala-%{majver}/*
%{_libdir}/libvala-*.so.*
%{_bindir}/vala
%{_bindir}/vala-%{majver}
%{_bindir}/vala-gen-introspect
%{_bindir}/vala-gen-introspect-%{majver}
%{_bindir}/valac
%{_bindir}/valac-%{majver}
%{_bindir}/vapigen*
%{_libdir}/pkgconfig/libvala-*.pc
%{_libdir}/pkgconfig/vapigen-%{majver}.pc
%{_libdir}/pkgconfig/vapigen.pc
%{_libdir}/vala-*
%{_mandir}/man1/vala-gen-introspect*
%{_mandir}/man1/valac*
%{_mandir}/man1/vapigen*
%{_datadir}/aclocal/vala.m4
%{_datadir}/aclocal/vapigen.m4
%{_datadir}/vala/

%files devel
%defattr(-,root,root)
%dir %{_includedir}/vala-*/
%doc ChangeLog NEWS README
%{_datadir}/aclocal/vala.m4
%{_datadir}/aclocal/vapigen.m4
%{_datadir}/vala/Makefile.vapigen
%{_includedir}/vala-*/*.h
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
%{_libdir}/vala-*
%{_mandir}/man1/vala-gen-introspect*
%{_mandir}/man1/valac*
%{_mandir}/man1/vapigen*

%files doc
%doc %{_datadir}/devhelp/books/vala-%{majver}

%files -n valadoc
%{_bindir}/valadoc
%{_bindir}/valadoc-%{majver}
%{_libdir}/libvaladoc-%{majver}.so.0*
%{_libdir}/valadoc-%{majver}/
%{_datadir}/valadoc-%{majver}/
%{_mandir}/man1/valadoc-%{majver}.1*
%{_mandir}/man1/valadoc.1*

%files -n valadoc-devel	
%{_includedir}/valadoc-%{majver}/
%{_libdir}/libvaladoc-%{majver}.so
%{_libdir}/pkgconfig/valadoc-%{majver}.pc

%changelog
* Mon Jan 24 2022 Henry Li <lihl@microsoft.com> - 0.54.6-1
- Upgrade to version 0.54.6
- Add bison, flex, gobject-introspection-devel, libxslt and graphviz-devel as BR
- Add subpackages vala-doc, valadoc and valadoc-devel
- Remove /usr/bin/vapicheck* since the files no longer exist
- Remove duplicate %license COPYING from main package  
- License Verified

* Fri Sep 10 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.34.6-4
- Remove libtool archive files from final packaging

* Tue Mar 16 2021 Henry Li <lihl@microsoft.com> - 0.34.6-3
- Add necessary files to vala package

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 0.34.6-2
-   Added %%license line automatically

*	Mon Apr 06 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.34.6-1
-	Original version for CBL-Mariner.
