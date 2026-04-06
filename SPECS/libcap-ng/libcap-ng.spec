# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global bpf_supported_arches aarch64 x86_64 ppc64le riscv64 s390x
Summary: Alternate posix capabilities library
Name: libcap-ng
Version: 0.9.1
Release: 1%{?dist}
License: LGPL-2.0-or-later
URL: https://github.com/stevegrubb/libcap-ng
Source0: %{name}-%{version}.tar.gz
BuildRequires: gcc make
BuildRequires: autoconf automake libtool
BuildRequires: kernel-headers >= 2.6.11 
BuildRequires: libattr-devel
%ifarch %{bpf_supported_arches}
# These next ones are needed by cap-audit
BuildRequires: clang
BuildRequires: bpftool libbpf-devel
BuildRequires: audit-libs-devel
%endif

%description
Libcap-ng is a library that makes using posix capabilities easier

%package devel
Summary: Header files for libcap-ng library
License: LGPL-2.0-or-later
Requires: kernel-headers >= 2.6.11
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
The libcap-ng-devel package contains the files needed for developing
applications that need to use the libcap-ng library.

%package python3
Summary: Python3 bindings for libcap-ng library
License: LGPL-2.0-or-later
BuildRequires: python3-devel swig python-unversioned-command
Requires: %{name}%{?_isa} = %{version}-%{release}

%description python3
The libcap-ng-python3 package contains the bindings so that libcap-ng
and can be used by python3 applications.

%package utils
Summary: Utilities for analyzing and setting file capabilities
License: GPL-2.0-or-later
Requires: %{name}%{?_isa} = %{version}-%{release}
%ifarch %{bpf_supported_arches}
Provides: %{name}-audit
Obsoletes: %{name}-audit < %{version}-%{release}
%endif

%description utils
The libcap-ng-utils package contains applications to analyze the
posix capabilities of all the program running on a system. It also
lets you set the file system based capabilities, and use cap-audit
to determine the necessary capabilities for a program.

%prep
%setup -q
touch NEWS
autoreconf -fv --install

%build
%configure --libdir=%{_libdir} \
%ifarch %{bpf_supported_arches}
	 --enable-cap-audit=yes \
%endif
	--with-python3

%make_build CFLAGS="%{optflags}"

%install
%make_install

# Remove a couple things so they don't get picked up
rm -f $RPM_BUILD_ROOT%{_libdir}/libcap-ng.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libcap-ng.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libdrop_ambient.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libdrop_ambient.a
rm -f $RPM_BUILD_ROOT%{_libdir}/python%{python3_version}/site-packages/_capng.a
rm -f $RPM_BUILD_ROOT%{_libdir}/python%{python3_version}/site-packages/_capng.la

%check
make check

%ldconfig_scriptlets

%files
%license COPYING.LIB
%{_libdir}/libcap-ng.so.*
%{_libdir}/libdrop_ambient.so.*
%attr(0644,root,root) %{_mandir}/man7/*

%files devel
%attr(0644,root,root) %{_mandir}/man3/*
%attr(0644,root,root) %{_includedir}/cap-ng.h
%{_libdir}/libcap-ng.so
%{_libdir}/libdrop_ambient.so
%attr(0644,root,root) %{_datadir}/aclocal/cap-ng.m4
%{_libdir}/pkgconfig/libcap-ng.pc

%files python3
%attr(755,root,root) %{python3_sitearch}/*

%files utils
%license COPYING
%attr(0755,root,root) %{_bindir}/filecap
%attr(0755,root,root) %{_bindir}/netcap
%attr(0755,root,root) %{_bindir}/pscap
%attr(0644,root,root) %{_mandir}/man8/filecap.8.gz
%attr(0644,root,root) %{_mandir}/man8/netcap.8.gz
%attr(0644,root,root) %{_mandir}/man8/pscap.8.gz
%ifarch %{bpf_supported_arches}
%attr(0755,root,root) %{_bindir}/cap-audit
%attr(0644,root,root) %{_mandir}/man8/cap-audit.8.gz
%endif

%changelog
* Tue Feb 17 2026 Steve Grubb <sgrubb@redhat.com> 0.9.1-1
- New upstream bugfix release

* Mon Jan 26 2026 Steve Grubb <sgrubb@redhat.com> 0.9-7
- Add Obsoletes libcap-ng-audit to remove old package

* Mon Jan 26 2026 Steve Grubb <sgrubb@redhat.com> 0.9-6
- Deprecate captest and move cap-audit into utils package

* Fri Jan 23 2026 Steve Grubb <sgrubb@redhat.com> 0.9-5
- Add s390x to libcap-ng-audit build arches

* Fri Jan 23 2026 Steve Grubb <sgrubb@redhat.com> 0.9-4
- Expand libcap-ng-audit to non-x86_64 arches

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Mon Jan 12 2026 Steve Grubb <sgrubb@redhat.com> 0.9-2
- Fix SPDX licence on audit package

* Sun Jan 11 2026 Steve Grubb <sgrubb@redhat.com> 0.9-1
- New upstream feature release
- Make libcap-ng-audit exclusive to x86_64 for now

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.8.5-8
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.8.5-7
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.8.5-5
- Rebuilt for Python 3.14

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.8.5-2
- Rebuilt for Python 3.13

* Tue Apr 09 2024 Steve Grubb <sgrubb@redhat.com> 0.8.5-1
- New upstream bugfix release

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 04 2024 Steve Grubb <sgrubb@redhat.com> 0.8.4-2
- Remove python bindings global exception handler

* Wed Dec 20 2023 Steve Grubb <sgrubb@redhat.com> 0.8.4-1
- New upstream bugfix release
- Drop libcap-ng-0.8.3-apply-disable.patch since things should be fixed

* Mon Sep 04 2023 Steve Grubb <sgrubb@redhat.com> 0.8.3-8
- Add function annotations to warn on unused results
- SPDX Migration

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> 0.8.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.8.3-6
- Rebuilt for Python 3.12

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 20 2022 Steve Grubb <sgrubb@redhat.com> 0.8.3-4
- BuildRequires python-setuptools
- SPDX Migration

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.8.3-2
- Rebuilt for Python 3.11

* Tue Mar 29 2022 Steve Grubb <sgrubb@redhat.com> 0.8.3-1
- New upstream bugfix release

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 22 2021 Steve Grubb <sgrubb@redhat.com> 0.8.2-8
- Update apply-disable patch

* Wed Sep 22 2021 Steve Grubb <sgrubb@redhat.com> 0.8.2-7
- Drop .la and .a libraries

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.8.2-5
- Rebuilt for Python 3.10

* Tue Feb 02 2021 Steve Grubb <sgrubb@redhat.com> 0.8.2-4
- Adjust syslog warning for bad use of capng_apply

* Sat Jan 30 2021 Steve Grubb <sgrubb@redhat.com> 0.8.2-3
- Add syslog warning for bad use of capng_apply

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 09 2020 Steve Grubb <sgrubb@redhat.com> 0.8.2-1
- New upstream bugfix release

* Fri Nov 20 2020 Steve Grubb <sgrubb@redhat.com> 0.8.1-2
- Add temporary patch disabling bounding set error codes

* Wed Nov 18 2020 Steve Grubb <sgrubb@redhat.com> 0.8.1-1
- New upstream bugfix release

* Tue Sep 08 2020 Steve Grubb <sgrubb@redhat.com> 0.8-1
- New upstream feature release

* Sun Aug 23 2020 Steve Grubb <sgrubb@redhat.com> 0.7.11-1
- New upstream release

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.7.10-3
- Rebuilt for Python 3.9

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 01 2019 Steve Grubb <sgrubb@redhat.com> 0.7.10-1
- New upstream release

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.7.9-9
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Mar  8 2019 Joe Orton <jorton@redhat.com> - 0.7.9-7
- fix crash on dlclose due to atfork handler (#1680481)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 16 2018 Steve Grubb <sgrubb@redhat.com> 0.7.9-5
- Remove python2 bindings (#1634889)

* Thu Aug 09 2018 Steve Grubb <sgrubb@redhat.com> 0.7.9-4
- Fix bug where filecap may not show capabilities

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.7.9-2
- Rebuilt for Python 3.7

* Wed Feb 07 2018 Steve Grubb <sgrubb@redhat.com> 0.7.9-1
- New upstream bugfix release

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.8-9
- Switch to %%ldconfig_scriptlets

* Fri Jan 05 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.7.8-8
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.7.8-7
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.7.8-6
- Python 2 binary package renamed to python2-libcap-ng
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.7.8-2
- Rebuild for Python 3.6

* Sun Jul 24 2016 Steve Grubb <sgrubb@redhat.com> 0.7.8-1
- New upstream bugfix release

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.7-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Feb 03 2016 Steve Grubb <sgrubb@redhat.com> 0.7.7-4
- use python site arch macros (#1303610)

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.7-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 13 2015 Steve Grubb <sgrubb@redhat.com> 0.7.7-1
- New upstream bugfix release

* Fri May 08 2015 Steve Grubb <sgrubb@redhat.com> 0.7.6-1
- New upstream release adding python3 support

* Thu May 07 2015 Steve Grubb <sgrubb@redhat.com> 0.7.5-1
- New upstream release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 17 2014 Tom Callaway <spot@fedoraproject.org> - 0.7.4-6
- fix license handling

* Mon Jun 23 2014 Kyle McMartin <kyle@redhat.com> 0.7.4-5
- Clamp CAP_LAST_CAP at /proc/sys/kernel/cap_last_cap's value in the
  Python bindings test if possible, otherwise use the value from
  <linux/capability.h> since the kernel now has 37 capabilities upstream,
  but our builders are not that up to date.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 07 2014 Steve Grubb <sgrubb@redhat.com> 0.7.4-3
- Add PR_SET_NO_NEW_PRIVS call back to capng_lock

* Wed Apr 30 2014 Steve Grubb <sgrubb@redhat.com> 0.7.4-2
- Remove PR_SET_NO_NEW_PRIVS call in capng_lock

* Thu Apr 24 2014 Steve Grubb <sgrubb@redhat.com> 0.7.4-1
- New upstream release

* Thu Nov 14 2013 Steve Grubb <sgrubb@redhat.com> 0.7.3-6
- Rebuild to pickup current CAP_LAST_CAP

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 02 2013 Karsten Hopp <karsten@redhat.com> 0.7.3-4
- bump release and rebuild to fix dependencies on PPC

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 19 2012 Steve Grubb <sgrubb@redhat.com> 0.7.3-2
- Remove useless code in pscap causing EBADFD

* Fri Nov 09 2012 Steve Grubb <sgrubb@redhat.com> 0.7.3-1
- New upstream release

* Wed Oct 24 2012 Steve Grubb <sgrubb@redhat.com> 0.7.1-1
- New upstream release

* Tue Jul 24 2012 Steve Grubb <sgrubb@redhat.com> 0.7-1
- New upstream release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 24 2011 Steve Grubb <sgrubb@redhat.com> 0.6.6-1
- New upstream release

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 03 2010 Steve Grubb <sgrubb@redhat.com> 0.6.5-1
- New upstream release fixing 2.6.36 kernel header issue

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jun 17 2010 Steve Grubb <sgrubb@redhat.com> 0.6.4-3
- Only open regular files in filecap

* Mon May 24 2010 Steve Grubb <sgrubb@redhat.com> 0.6.4-2
- In utils subpackage added a requires statement.

* Thu May 06 2010 Steve Grubb <sgrubb@redhat.com> 0.6.4-1
- New upstream release fixing multi-threading issue

* Wed Apr 28 2010 Steve Grubb <sgrubb@redhat.com> 0.6.3-2
- filecap shows full capabilities if a file has any

* Thu Mar 11 2010 Steve Grubb <sgrubb@redhat.com> 0.6.3-1
- New upstream release

* Tue Feb 16 2010 Steve Grubb <sgrubb@redhat.com> 0.6.2-4
- Use global macro and require pkgconfig for devel subpackage

* Fri Oct 09 2009 Steve Grubb <sgrubb@redhat.com> 0.6.2-3
- Apply patch to retain setpcap only if clearing bounding set

* Sat Oct 03 2009 Steve Grubb <sgrubb@redhat.com> 0.6.2-2
- Apply patch correcting pscap and netcap acct detection

* Mon Sep 28 2009 Steve Grubb <sgrubb@redhat.com> 0.6.2-1
- New upstream release

* Sun Jul 26 2009 Steve Grubb <sgrubb@redhat.com> 0.6.1-1
- New upstream release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 29 2009 Steve Grubb <sgrubb@redhat.com> 0.6-1
- New upstream release

* Sun Jun 21 2009 Steve Grubb <sgrubb@redhat.com> 0.5.1-1
- New upstream release

* Fri Jun 19 2009 Steve Grubb <sgrubb@redhat.com> 0.5-1
- New upstream release

* Fri Jun 12 2009 Steve Grubb <sgrubb@redhat.com> 0.4.2-1
- New upstream release

* Fri Jun 12 2009 Steve Grubb <sgrubb@redhat.com> 0.4.1-1
- Initial build.

