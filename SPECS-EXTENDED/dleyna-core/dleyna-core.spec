%define api 1.0
Summary:        Utilities for higher level dLeyna libraries
Name:           dleyna-core
Version:        0.6.0
Release:        15%{?dist}
License:        LGPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://01.org/dleyna/
Source0:        https://01.org/sites/default/files/downloads/dleyna/%{name}-%{version}.tar_3.gz
# Backported from upstream
Patch0:         port-to-gupnp-1.6.patch
Patch1:         dleyna-core-Don-t-remove-a-queue-more-than-once.patch
Patch2:         dleyna-core-Make-the-task-processor-more-robust.patch
Patch3:         port_gupnp_1.6_context_filter.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmodule-2.0)
BuildRequires:  pkgconfig(gupnp-1.6)

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
%autosetup -p1

%build
autoreconf -f -i
%configure \
  --disable-silent-rules \
  --disable-static

%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

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
* Wed Feb 01 2023 Sumedh Sharma <sumsharma@microsoft.com> - 0.6.0-15
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- Port to gupnp api version 1.6
- License verified

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Aug 20 2021 Kalev Lember <klember@redhat.com> - 0.6.0-12
- Rebuilt for gupnp soname bump

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Dec 04 2020 Debarshi Ray <rishi@fedoraproject.org> - 0.6.0-9
- Don't remove a queue more than once (RH #1903139)
- Remove any pending task processing handlers when destroying a queue
  (RH #1890618)

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Mar 12 2020 Kalev Lember <klember@redhat.com> - 0.6.0-7
- Port to gupnp 1.2

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
