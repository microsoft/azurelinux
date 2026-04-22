# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           userspace-rcu
Version:        0.15.3
Release: 3%{?dist}
Summary:        RCU (read-copy-update) implementation in user-space
License:        LGPL-2.1-or-later
URL:            https://liburcu.org

Source0:        https://lttng.org/files/urcu/%{name}-%{version}.tar.bz2
Source1:        https://lttng.org/files/urcu/%{name}-%{version}.tar.bz2.asc
# gpg2 --export --export-options export-minimal 2A0B4ED915F2D3FA45F5B16217280A9781186ACF > gpgkey-2A0B4ED915F2D3FA45F5B16217280A9781186ACF.gpg
Source2:        gpgkey-2A0B4ED915F2D3FA45F5B16217280A9781186ACF.gpg
Patch0:         regtest-without-bench.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  multilib-rpm-config
BuildRequires:  pkgconfig

%description
This data synchronization library provides read-side access which scales
linearly with the number of cores. It does so by allowing multiples copies
of a given data structure to live at the same time, and by monitoring
the data structure accesses to detect grace periods after which memory
reclamation is possible.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package contains libraries and header files for developing applications
that use %{name}


%prep
%autosetup -p1

%build
# Reinitialize libtool with the fedora version to remove Rpath
autoreconf -vif -W all,error

%configure --disable-static --enable-compiler-atomic-builtins
V=1 make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
find %{buildroot} -type f -name "*.la" -delete
rm %{buildroot}/%{_docdir}/%{name}/LICENSE.md
# Replace arch-dependent header file with arch-independent stub (when needed).
%multilib_fix_c_header --file %{_includedir}/urcu/config.h
%multilib_fix_c_header --file %{_includedir}/urcu/arch.h
%multilib_fix_c_header --file %{_includedir}/urcu/uatomic.h

%check
make check
make regtest

%ldconfig_scriptlets


%files
%license LICENSE.md lgpl-relicensing.md
%doc ChangeLog README.md
%{_libdir}/liburcu-bp.so.8*
%{_libdir}/liburcu-cds.so.8*
%{_libdir}/liburcu-common.so.8*
%{_libdir}/liburcu-mb.so.8*
%{_libdir}/liburcu-memb.so.8*
%{_libdir}/liburcu-qsbr.so.8*
%{_libdir}/liburcu.so.8*

%files devel
%doc %{_pkgdocdir}/examples
%{_includedir}/*
%{_libdir}/liburcu-bp.so
%{_libdir}/liburcu-cds.so
%{_libdir}/liburcu-common.so
%{_libdir}/liburcu-mb.so
%{_libdir}/liburcu-memb.so
%{_libdir}/liburcu-qsbr.so
%{_libdir}/liburcu.so
%{_libdir}/pkgconfig/liburcu*.pc
%{_docdir}/%{name}/cds-api.md
%{_docdir}/%{name}/rcu-api.md
%{_docdir}/%{name}/solaris-build.md
%{_docdir}/%{name}/uatomic-api.md


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue May 20 2025 Michael Jeanson <mjeanson@efficios.com> - 0.15.3-1
- New upstream release

* Tue Apr 15 2025 Michael Jeanson <mjeanson@efficios.com> - 0.15.2-1
- New upstream release

* Tue Feb 18 2025 Michael Jeanson <mjeanson@efficios.com> - 0.15.1-1
- New upstream release

* Thu Jan 16 2025 Michael Jeanson <mjeanson@efficios.com> - 0.15.0-1
- New upstream release
- The 'signal' flavour of liburcu was removed upstream
- Enable compiler atomics

* Tue Sep 03 2024 Kienan Stewart <kstewart@efficios.com> - 0.14.1-1
- New upstream release

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon May 08 2023 Michael Jeanson <mjeanson@efficios.com> - 0.14.0-2
- migrated to SPDX license

* Thu Apr 27 2023 Michael Jeanson <mjeanson@efficios.com> - 0.14.0-1
- New upstream release

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Oct 28 2022 Michael Jeanson <mjeanson@efficios.com> - 0.13.2-1
- New upstream release

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Michael Jeanson <mjeanson@efficios.com> - 0.13.0-2
- New upstream release
- Bump SONAME to 8

* Thu Feb 18 2021 Michael Jeanson <mjeanson@efficios.com> - 0.12.2-1
- New upstream release

* Wed Feb 17 2021 Michael Jeanson <mjeanson@efficios.com> - 0.12.1-4
- Fix conflicts in userspace-rcu-devel multilib packages (#1886615)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Apr 22 2020 Michael Jeanson <mjeanson@efficios.com> - 0.12.1-1
- New upstream release

* Tue Apr 14 2020 Michael Jeanson <mjeanson@efficios.com> - 0.12.0-1
- New upstream release

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 03 2019 Michael Jeanson <mjeanson@efficios.com> - 0.11.1-1
- New upstream release

* Fri May 03 2019 Michael Jeanson <mjeanson@efficios.com> - 0.10.2-1
- New upstream release

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 10 2018 Peter Robinson <pbrobinson@fedoraproject.org> 0.10.1-3
- Use %%license, spec cleanups

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Michael Jeanson <mjeanson@efficios.com> - 0.10.1-1
- New upstream release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 22 2017 Michael Jeanson <mjeanson@efficios.com> - 0.10.0-1
- New upstream release

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 30 2016 Michael Jeanson <mjeanson@efficios.com> - 0.9.3-1
- New upstream release

* Wed Jun 22 2016 Michael Jeanson <mjeanson@efficios.com> - 0.9.2-2
- Re-add rpath removing

* Tue Jun 21 2016 Michael Jeanson <mjeanson@efficios.com> - 0.9.2-1
- New upstream release
- Dropped aarch64 patch merged upstream

* Sun May 15 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 0.8.6-4
- Fix %%doc usage (#1001239)

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 26 2015 Scott Tsai <scottt.tw@gmail.com> - 0.8.6-1
- New upstream release

* Sun Nov 02 2014 Suchakra Sharma <suchakra@fedoraproject.org> - 0.8.5-1
- New upstream release

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 0.8.1-3
- Use upstream patch for aarch64 (includes ppc64le too)

* Thu May 22 2014 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 0.8.1-2
- Added AArch64 support

* Mon Feb 10 2014 Yannick Brosseau <yannick.brosseau@gmail.com> 0.8.1-1
- New upstream release

* Sat Jan 18 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.9-1
- Update to 0.7.9

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 05 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 0.7.7-1
- New upstream version

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 0.7.6-1
- New upstream version

* Tue Oct 23 2012 Yannick Brosseau <yannick.brosseau@gmail.com> - 0.7.5-1
- New upstream version 

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Yannick Brosseau <yannick.brosseau@gmail.com> - 0.7.3-1
- New upstream version (#828716)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 26 2010 Jan "Yenya" Kasprzak <kas@fi.muni.cz> 0.4.1-1
- new upstream version.

* Tue Oct 20 2009 Jan "Yenya" Kasprzak <kas@fi.muni.cz> 0.2.4-1
- Initial revision.
