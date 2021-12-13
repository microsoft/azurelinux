Vendor:         Microsoft Corporation
Distribution:   Mariner
%define api 1.0

Name:           dleyna-core
Version:        0.6.0
Release:        7%{?dist}
Summary:        Utilities for higher level dLeyna libraries

License:        LGPLv2
URL:            https://01.org/dleyna/
Source0:        https://01.org/sites/default/files/downloads/dleyna/%{name}-%{version}.tar_3.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmodule-2.0)
BuildRequires:  pkgconfig(gupnp-1.0)

%description
A set of utility functions that are used by the higher level dLeyna libraries
to communicate with DLNA devices. It provides APIs for logging, error, settings
and task management, and an IPC abstraction.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
autoreconf -f -i
%configure \
  --disable-silent-rules \
  --disable-static

make %{?_smp_mflags}


%install
make install INSTALL="%{__install} -p" DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -delete

%ldconfig_scriptlets


%files
%license COPYING
%doc AUTHORS
%doc ChangeLog
%doc README
%{_libdir}/libdleyna-core-%{api}.so.*

%files devel
%{_libdir}/libdleyna-core-%{api}.so
%{_libdir}/pkgconfig/%{name}-%{api}.pc

%dir %{_includedir}/dleyna-%{api}
%dir %{_includedir}/dleyna-%{api}/libdleyna
%{_includedir}/dleyna-%{api}/libdleyna/core


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.6.0-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Oct 05 2017 Debarshi Ray <rishi@fedoraproject.org> - 0.6.0-1
- Update to 0.6.0

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Sep 15 2016 Debarshi Ray <rishi@fedoraproject.org> - 0.5.0-4
- Don't schedule dleyna_task_processor_t->on_quit_cb more than once
  (RH #1251366)
- Remove all queues before dleyna_task_processor_t->on_quit_cb is run
  (RH #1205574, #1360209)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 06 2015 Debarshi Ray <rishi@fedoraproject.org> - 0.5.0-1
- Update to 0.5.0

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan 15 2014 Bastien Nocera <bnocera@redhat.com> - 0.4.0-1
- Update to 0.4.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 26 2013 Debarshi Ray <rishi@fedoraproject.org> - 0.1.0-1
- Initial spec.
