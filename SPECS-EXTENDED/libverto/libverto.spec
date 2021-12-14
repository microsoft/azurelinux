%global homepage https://github.com/latchset/libverto

Name:           libverto
Version:        0.3.0
Release:        10%{?dist}
Summary:        Main loop abstraction library

License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            %{homepage}
Source0:        %{homepage}/releases/download/%{version}/%{name}-%{version}.tar.gz

Patch0: Work-around-libev-not-being-c89-compliant.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool

BuildRequires:  glib2-devel
BuildRequires:  libevent-devel
# BuildRequires:  libtevent-devel
%if !0%{?rhel}
BuildRequires:  libev-devel
%endif

BuildRequires:  git

Obsoletes:      libverto-tevent < 0.3.0-2
Obsoletes:      libverto-tevent-devel < 0.3.0-2

%description
libverto provides a way for libraries to expose asynchronous interfaces
without having to choose a particular event loop, offloading this
decision to the end application which consumes the library.

If you are packaging an application, not library, based on libverto,
you should depend either on a specific implementation module or you
can depend on the virtual provides 'libverto-module-base'. This will
ensure that you have at least one module installed that provides io,
timeout and signal functionality. Currently glib is the only module
that does not provide these three because it lacks signal. However,
glib will support signal in the future.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        glib
Summary:        glib module for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    glib
Module for %{name} which provides integration with glib.

This package does NOT yet provide %{name}-module-base.

%package        glib-devel
Summary:        Development files for %{name}-glib
Requires:       %{name}-glib%{?_isa} = %{version}-%{release}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description    glib-devel
The %{name}-glib-devel package contains libraries and header files for
developing applications that use %{name}-glib.

%package        libevent
Summary:        libevent module for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       %{name}-module-base = %{version}-%{release}

%description    libevent
Module for %{name} which provides integration with libevent.

%package        libevent-devel
Summary:        Development files for %{name}-libevent
Requires:       %{name}-libevent%{?_isa} = %{version}-%{release}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description    libevent-devel
The %{name}-libevent-devel package contains libraries and header files for
developing applications that use %{name}-libevent.

# %package        tevent
# Summary:        tevent module for %{name}
# Requires:       %{name}%{?_isa} = %{version}-%{release}
# Provides:       %{name}-module-base = %{version}-%{release}

# %description    tevent
# Module for %{name} which provides integration with tevent.

# This package provides %{name}-module-base since it supports io, timeout
# and signal.

# %package        tevent-devel
# Summary:        Development files for %{name}-tevent
# Requires:       %{name}-tevent%{?_isa} = %{version}-%{release}
# Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

# %description    tevent-devel
# The %{name}-tevent-devel package contains libraries and header files for
# developing applications that use %{name}-tevent.

%if !0%{?rhel}
%package        libev
Summary:        libev module for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       %{name}-module-base = %{version}-%{release}

%description    libev
Module for %{name} which provides integration with libev.

This package provides %{name}-module-base since it supports io, timeout
and signal.

%package        libev-devel
Summary:        Development files for %{name}-libev
Requires:       %{name}-libev%{?_isa} = %{version}-%{release}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description    libev-devel
The %{name}-libev-devel package contains libraries and header files for
developing applications that use %{name}-libev.

This package provides %{name}-module-base since it supports io, timeout
and signal.
%endif

%prep
%autosetup -S git

%build
autoreconf -fiv
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%ldconfig_scriptlets
%ldconfig_scriptlets glib
%ldconfig_scriptlets libevent
#ldconfig_scriptlets tevent
%if !0%{?rhel}
%ldconfig_scriptlets libev
%endif

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/%{name}.so.*

%files devel
%{_includedir}/verto.h
%{_includedir}/verto-module.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%files glib
%{_libdir}/%{name}-glib.so.*

%files glib-devel
%{_includedir}/verto-glib.h
%{_libdir}/%{name}-glib.so
%{_libdir}/pkgconfig/%{name}-glib.pc

%files libevent
%{_libdir}/%{name}-libevent.so.*

%files libevent-devel
%{_includedir}/verto-libevent.h
%{_libdir}/%{name}-libevent.so
%{_libdir}/pkgconfig/%{name}-libevent.pc

# %files tevent
# %{_libdir}/%{name}-tevent.so.*

# %files tevent-devel
# %{_includedir}/verto-tevent.h
# %{_libdir}/%{name}-tevent.so
# %{_libdir}/pkgconfig/%{name}-tevent.pc

%if !0%{?rhel}
%files libev
%{_libdir}/%{name}-libev.so.*

%files libev-devel
%{_includedir}/verto-libev.h
%{_libdir}/%{name}-libev.so
%{_libdir}/pkgconfig/%{name}-libev.pc
%endif

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.3.0-10
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 19 2018 Robbie Harwood <rharwood@redhat.com> - 0.3.0-5
- Rebuild due to libevent soname bump

* Wed Feb 07 2018 Kalev Lember <klember@redhat.com> - 0.3.0-4
- Obsolete removed tevent and tevent-devel subpackages

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.3.0-3
- Switch to %%ldconfig_scriptlets

* Wed Jan 31 2018 Robbie Harwood <rharwood@redhat.com> - 0.3.0-2
- Stop providing the tevent backend
- https://bugzilla.samba.org/show_bug.cgi?id=12987

* Tue Sep 05 2017 Robbie Harwood <rharwood@redhat.com> - 0.3.0-1
- New upstream release (0.3.0)

* Mon Aug 07 2017 Robbie Harwood <rharwood@redhat.com> - 0.2.6-11
- Fix memleak in vfree()
- Misc spec file fixes

* Thu Aug 03 2017 Robbie Harwood <rharwood@redhat.com> - 0.2.6-10
- Fix all compile warnings

* Tue Aug 01 2017 Robbie Harwood <rharwood@redhat.com> - 0.2.6-9
- Update upstream URLs (no functional changes)
- Move to autosetup

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> - 0.2.6-3
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 12 2014 Nathaniel McCallum <npmccallum@redhat.com> - 0.2.6-1
- Update to 0.2.6

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 25 2012 Nathaniel McCallum <npmccallum@redhat.com> - 0.2.5-1
- Update to 0.2.5
- Drop libverto-0.2.4-fix-libev.patch

* Tue Aug 07 2012 Nathaniel McCallum <npmccallum@redhat.com> - 0.2.4-4
- Don't build libev on RHEL

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 13 2012 Nathaniel McCallum <npmccallum@redhat.com> - 0.2.4-2
- Added libverto-0.2.4-fix-libev.patch

* Thu Feb 09 2012 Nathaniel McCallum <npmccallum@redhat.com> - 0.2.4-1
- Update to 0.2.4 release

* Wed Feb 08 2012 Nathaniel McCallum <npmccallum@redhat.com> - 0.2.3-1
- Update to 0.2.3 release

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 11 2011 Nathaniel McCallum <npmccallum@redhat.com> - 0.2.2-1
- Update to 0.2.2 release
- Add ChangeLog documentation

* Fri Nov 11 2011 Nathaniel McCallum <npmccallum@redhat.com> - 0.2.1-2
- Fix Requires to have proper ISA dependencies

* Thu Nov 10 2011 Nathaniel McCallum <npmccallum@redhat.com> - 0.2.1-1
- Update to 0.2.1

* Mon Aug 15 2011 Nathaniel McCallum <npmccallum@redhat.com> - 0.1-1
- Initial release

