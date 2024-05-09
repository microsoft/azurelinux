Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global gittag0 v1.10.0

Name: memkind
Summary: User Extensible Heap Manager
Version: 1.10.0
Release: 2%{?dist}
License: BSD
URL: https://memkind.github.io/memkind
BuildRequires: automake libtool numactl-devel systemd gcc gcc-c++

# x86_64 is the only arch memkind will build and work due to
# its current dependency on SSE4.2 CRC32 instruction which
# is used to compute thread local storage arena mappings
# with polynomial accumulations via GCC's intrinsic _mm_crc32_u64
# For further info check: 
# - /lib/gcc/<target>/<version>/include/smmintrin.h
# - https://gcc.gnu.org/bugzilla/show_bug.cgi?id=36095 
# - https://en.wikipedia.org/wiki/SSE4
ExclusiveArch: x86_64

Source0: https://github.com/%{name}/%{name}/archive/%{gittag0}/%{name}-%{version}.tar.gz

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
Summary: Memkind User Extensible Heap Manager development lib and tools
Requires: %{name} = %{version}-%{release}

%description devel
Install header files and development aids to link memkind library 
into applications. The memkind library is an user extensible heap manager 
built on top of jemalloc which enables control of memory characteristics and
heap partitioning on different kinds of memory. This software is being made 
available for early evaluation. The memkind library should be considered 
pre-alpha: bugs may exist and the interfaces may be subject to change prior to 
alpha release. Feedback on design or implementation is greatly appreciated.

%prep
%setup -q -a 0 -n %{name}-%{version}

%build
# It is required that we configure and build the jemalloc subdirectory
# before we configure and start building the top level memkind directory.
# To ensure the memkind build step is able to discover the output
# of the jemalloc build we must create an 'obj' directory, and build
# from within that directory.
cd %{_builddir}/%{name}-%{version}
echo %{version} > %{_builddir}/%{name}-%{version}/VERSION
./build.sh --prefix=%{_prefix} --includedir=%{_includedir} --libdir=%{_libdir} \
           --bindir=%{_bindir} --docdir=%{_docdir}/%{name} --mandir=%{_mandir} \
           --sbindir=%{_sbindir}

%install
cd %{_builddir}/%{name}-%{version}
make DESTDIR=%{buildroot} INSTALL='install -p' install
rm -f %{buildroot}/%{_libdir}/lib%{name}.{l,}a
rm -f %{buildroot}/%{_libdir}/libautohbw.{l,}a
rm -f %{buildroot}/%{_docdir}/%{name}/VERSION

%ldconfig_scriptlets

%files
%{_libdir}/lib%{name}.so.*
%{_libdir}/libautohbw.so.*
%{_bindir}/%{name}-hbw-nodes
%{_bindir}/%{name}-auto-dax-kmem-nodes
%{_mandir}/man1/%{name}*.1.*
%{_mandir}/man7/autohbw.7.*
%dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/README
%license %{_docdir}/%{name}/COPYING

%files devel
%{_includedir}/%{name}*.h
%{_includedir}/hbwmalloc.h
%{_includedir}/hbw_allocator.h
%{_includedir}/pmem_allocator.h
%{_libdir}/lib%{name}.so
%{_libdir}/libautohbw.so
%{_libdir}/pkgconfig/memkind.pc
%{_mandir}/man3/%{name}*.3.*
%{_mandir}/man3/hbwmalloc.3.*
%{_mandir}/man3/hbwallocator.3.*
%{_mandir}/man3/pmemallocator.3.*

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.10.0-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

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
