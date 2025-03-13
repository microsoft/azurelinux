%global gittag0 v1.14.0
# WORKAROUND to avoid breaking the build at the atrocious libtool shell scrip
# due to RPM environmental macros being lost for the subshells
%undefine _package_note_file

Name: 		memkind
Summary: 	User Extensible Heap Manager
Version: 	1.14.0
Release: 	10%{?dist}
License: 	BSD-3-Clause
URL: 		http://memkind.github.io/memkind
Vendor:         Microsoft Corporation
Distribution:   Azure Linux

BuildRequires: 	make
BuildRequires:	patch
BuildRequires: 	automake
BuildRequires:	libtool
BuildRequires:	numactl-devel
BuildRequires:	systemd
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	daxctl-devel
# memkind has been discontinued and archived upstream. See Bugzilla 2296288.
# We are deprecating it now, to flag any potential user of its future removal.
Provides: 	deprecated()

Source0: 	https://github.com/%{name}/%{name}/archive/%{gittag0}/%{name}-%{version}.tar.gz

# unbreak the atrocious autotools Makefile.am construction for
# libmemkind archive creation target
Patch0: 	Makefile.am.patch

%description
The memkind library is an user extensible heap manager built on top of
jemalloc which enables control of memory characteristics and a
partitioning of the heap between kinds of memory.  The kinds of memory
are defined by operating system memory policies that have been applied
to virtual address ranges. Memory characteristics supported by
memkind without user extension include control of NUMA and page size
features. The jemalloc non-standard interface has been extended to
enable specialized arenas to make requests for virtual memory from the
operating system through the memkind partition interface. Through the
other memkind interfaces the user can control and extend memory
partition features and allocate memory while selecting enabled
features. This software is being made available for early evaluation.
Feedback on design or implementation is greatly appreciated.

%package devel
Summary: 	Memkind User Extensible Heap Manager development lib and tools
Requires: 	%{name} = %{version}-%{release}
Provides: 	deprecated()

%description devel
Install header files and development aids to link memkind library 
into applications. The memkind library is an user extensible heap manager 
built on top of jemalloc which enables control of memory characteristics and
heap partitioning on different kinds of memory. This software is being made 
available for early evaluation. The memkind library should be considered 
pre-alpha: bugs may exist and the interfaces may be subject to change prior to 
alpha release. Feedback on design or implementation is greatly appreciated.

%prep
%autosetup -n %{name}-%{version}

%build
cd %{_builddir}/%{name}-%{version}
echo %{version} > %{_builddir}/%{name}-%{version}/VERSION
test -f configure || ./autogen.sh
%configure --enable-secure --enable-tls --prefix=%{_prefix} --libdir=%{_libdir} \
	   --includedir=%{_includedir} --sbindir=%{_sbindir} --bindir=%{_bindir} \
	   --mandir=%{_mandir} --docdir=%{_docdir}/%{name} \
	   CFLAGS="$RPM_OPT_FLAGS -std=gnu99" LDFLAGS="%{build_ldflags}"
%{__make} V=1

%install
cd %{_builddir}/%{name}-%{version}
make DESTDIR=%{buildroot} INSTALL='install -p' install
rm -f %{buildroot}/%{_libdir}/lib%{name}.{l,}a
rm -f %{buildroot}/%{_libdir}/libautohbw.{l,}a
rm -f %{buildroot}/%{_libdir}/libmemtier.{l,}a
rm -f %{buildroot}/%{_docdir}/%{name}/VERSION

%ldconfig_scriptlets

%files
%{_bindir}/memtier
%{_libdir}/lib%{name}.so.*
%{_libdir}/libautohbw.so.*
%{_libdir}/libmemtier.so.*
%{_bindir}/%{name}-hbw-nodes
%{_bindir}/%{name}-auto-dax-kmem-nodes
%{_mandir}/man1/%{name}*.1.*
%{_mandir}/man1/memtier.1.*
%{_mandir}/man7/autohbw.7.*
%{_mandir}/man7/memtier.7.*
%{_mandir}/man7/libmemtier.7.*
%dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/README
%license %{_docdir}/%{name}/COPYING

%files devel
%{_includedir}/%{name}*.h
%{_includedir}/hbwmalloc.h
%{_includedir}/hbw_allocator.h
%{_includedir}/pmem_allocator.h
%{_includedir}/fixed_allocator.h
%{_libdir}/lib%{name}.so
%{_libdir}/libautohbw.so
%{_libdir}/libmemtier.so
%{_libdir}/pkgconfig/memkind.pc
%{_mandir}/man3/%{name}*.3.*
%{_mandir}/man3/hbwmalloc.3.*
%{_mandir}/man3/hbwallocator.3.*
%{_mandir}/man3/pmemallocator.3.*
%{_mandir}/man3/fixedallocator.3.*
%{_mandir}/man3/libmemtier.3.*

%changelog
* Wed Jan 15 2025 Akhila Guruju <v-guakhila@microsoft.com> - 1.14.0-10
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul  8 2024 Rafael Aquini <aquini@linux.com> - 1.14.0-8
- Mark memkind as deprecated following its upstream discontinuation notice
- Fix minor typo on memkind.spec changelog section

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov  8 2023 Rafael Aquini <aquini@linux.com> - 1.14.0-5
- SPDX migration

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jan 24 2023 Rafael Aquini <aquini@linux.com> - 1.14.0-3
- Fix build issues after https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jan 13 2023 Rafael Aquini <aquini@linux.com> - 1.14.0-1
- Update memkind source file to 1.14.0 upstream

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 28 2022 Rafael Aquini <aquini@linux.com> - 1.13.0-1
- Update memkind source file to 1.13.0 upstream

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Aug 23 2021 Rafael Aquini <aquini@linux.com> - 1.11.0-1
- Update memkind source file to 1.11.0 upstream

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct 15 2020 Rafael Aquini <aquini@linux.com> - 1.10.1-2
- Work around false positive warning with gcc-11

* Wed Oct 07 2020 Rafael Aquini <aquini@linux.com> - 1.10.1-1
- Update memkind source file to 1.10.1 upstream

* Wed Jul 29 2020 Jeff Law <law@redhat.com> - 1.10.0-3
- Avoid uninitialized variable in testsuite

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Feb 01 2020 Rafael Aquini <aquini@linux.com> - 1.10.0-1
- Update memkind source file to 1.10.0 upstream

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Dec 14 2019 Jeff Law <law@redhat.com> - 1.9.0-3
- Fix missing #include for gcc-10

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 10 2019 Rafael Aquini <aquini@linux.com> - 1.9.0-1
- Update memkind source file to 1.9.0 upstream

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 20 2018 Rafael Aquini <aquini@linux.com> - 1.7.0-3
- Rebuild to fix removal of GCC from buildroots (1604813)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 23 2018 Rafael Aquini <aquini@linux.com> - 1.7.0-1
- Update memkind source file to 1.7.0 upstream

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 27 2017 Rafael Aquini <aquini@linux.com> - 1.5.0-1
- Update memkind source file to 1.5.0 upstream

* Fri Feb 17 2017 Rafael Aquini <aquini@linux.com> - 1.4.0-1
- Update memkind source file to 1.4.0 upstream

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 16 2016 Rafael Aquini <aquini@linux.com> - 1.3.0-1
- Update memkind source file to 1.3.0 upstream

* Wed Jun 08 2016 Rafael Aquini <aquini@linux.com> - 1.1.0-1
- Update memkind source file to 1.1.0 upstream

* Thu Mar 17 2016 Rafael Aquini <aquini@linux.com> - 1.0.0-1
- Update memkind source file to 1.0.0 upstream

* Sun Feb 07 2016 Rafael Aquini <aquini@linux.com> - 0.3.0-5
- Fix rpmlint error dir-or-file-in-var-run for /var/run/memkind

* Sat Feb 06 2016 Rafael Aquini <aquini@linux.com> - 0.3.0-4
- Update upstream fixes for memkind-0.3.0
- Switch old init.d scripts for systemd unit service
- Fix fc24 build error

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 17 2015 Rafael Aquini <aquini@linux.com> - 0.3.0-2
- Minor clean-ups and adjustments required for the RPM

* Tue Nov 17 2015 Rafael Aquini <aquini@linux.com> - 0.3.0-1
- Update memkind source file to 0.3.0 upstream

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-4.20150525git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 25 2015 Rafael Aquini <aquini@linux.com> - 0.2.2-3.20150525git
- Get rid of obsolete m4 macros usage on autotool scripts

* Mon May 18 2015 Rafael Aquini <aquini@linux.com> - 0.2.2-2.20150525git
- Fix to BuildRequires and License Text Marker in spec file (1222709#c1)

* Mon May 18 2015 Rafael Aquini <aquini@linux.com> - 0.2.2-1.20150518git
- Initial RPM packaging for Fedora

