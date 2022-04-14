Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           gupnp-igd
Version:        0.2.5
Release:        9%{?dist}
Summary:        Library to handle UPnP IGD port mapping

License:        LGPLv2+
URL:            https://wiki.gnome.org/Projects/GUPnP
Source0:        https://download.gnome.org/sources/%{name}/0.2/%{name}-%{version}.tar.xz

BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  gupnp-devel

Provides: %{name}-python = %{version}-%{release}
Provides: %{name}-python%{?_isa} = %{version}-%{release}
Obsoletes: %{name}-python < %{version}-%{release}
Provides: %{name}-python2 = %{version}-%{release}
Provides: %{name}-python2%{?_isa} = %{version}-%{release}
Obsoletes: %{name}-python2 < %{version}-%{release}

%description
%{name} is a library to handle UPnP IGD port mapping.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure --disable-static --disable-python --enable-introspection=yes
# quite rpmlint error about unused-direct-shlib-dependency
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
LDFLAGS="$RPM_LD_FLAGS -lgobject-2.0" make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%ldconfig_scriptlets


%files
%license COPYING
%doc README
%{_libdir}/*.so.*
%{_libdir}/girepository-1.0/GUPnPIgd-1.0.typelib


%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}-1.0*.pc
%{_datadir}/gtk-doc/html/%{name}/
%{_datadir}/gir-1.0/GUPnPIgd-1.0.gir


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.2.5-9
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 16 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.2.5-4
- Remove python2-gupnp-igd requires from -devel

* Thu Jun 07 2018 Bastien Nocera <bnocera@redhat.com> - 0.2.5-3
+ gupnp-igd-0.2.5-3
- Remove python2-gupnp-igd sub-package, nothing uses it in Fedora
  and gobject-introspection supports both Python2 and Python3

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 21 2017 Kalev Lember <klember@redhat.com> - 0.2.5-1
- Update to 0.2.5
- Update inter-package dependencies after python2-gupnp-igd rename
- Tighten deps with the _isa macro
- Update source URLs
- Use license macro for COPYING

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.2.4-7
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.2.4-6
- Python 2 binary package renamed to python2-gupnp-igd
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jun 22 2016 Richard Hughes <rhughes@redhat.com> - 0.2.4-1
- Update to 0.2.4

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.2.3-3
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Feb  7 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.2.3-1
- Update to 0.2.3
- Enable gobject-introspection

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 27 2013 Brian Pepple <bpepple@fedoraproject.org> - 0.2.2-1
- Update to 0.2.2.
- Drop define attribute. No longer needed.
- Update url and source url.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan 16 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.2.1-1
- Update to 0.2.1.
- Drop gcc patch. Fixed upstream.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Peter Robinson <pbrobinson@gmail.com> - 0.1.7-6
- Bump for new gupnp

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 26 2010 Peter Robinson <pbrobinson@gmail.com> - 0.1.7-4
- Add patch to fix FTBFS # 631415

* Thu Dec 23 2010 Dan Horák <dan[at]danny.cz> - 0.1.7-3
- workaround make 3.82 issue in python/Makefile

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sat May 22 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.1.7-1
- Update to 0.1.7.

* Sat Jan 30 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.1.6-1
- Update to 0.1.6.

* Sun Dec  6 2009 Peter Robinson <pbrobinson@gmail.com> - 0.1.5-1
- Update to 0.1.5.

* Mon Nov 16 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.1.4-1
- Update to 0.1.4.

* Thu Sep 17 2009 Bastien Nocera <bnocera@redhat.com> 0.1.3-3
- Rebuild for new gupnp

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.1.3-1
- Update to 0.1.3.

* Sat May 16 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.1.2-1
- Update to 0.1.2.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 18 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.1.1-2
- Quite rpmlint error about unused-direct-shlib-dependency.

* Wed Dec 31 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.1.1-1
- Initial Fedora spec.

