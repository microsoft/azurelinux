
# rpmbuild options:
#   --with | --without fabric
#   --with | --without ndctl

# do not terminate build if files in the $RPM_BUILD_ROOT
# directory are not found in %%files (without fabric case)
%define _unpackaged_files_terminate_build 0

%define min_libfabric_ver 1.4.2
%define min_ndctl_ver 60.1
%define upstreamversion 2.0.1

# Debug variants of the libraries should be filtered out of the provides.
%global __provides_exclude_from ^%{_libdir}/pmdk_debug/.*\\.so.*$

%bcond_without fabric

# by default build with ndctl, unless explicitly disabled
%bcond_without ndctl

# by default build without pmemcheck, unless explicitly enabled
# pmemcheck is not packaged by Fedora
%bcond_with pmemcheck

Summary:        Persistent Memory Development Kit (formerly NVML)
Name:           nvml
Version:        2.0.1
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://pmem.io/pmdk
Source0:        https://github.com/pmem/pmdk/releases/download/%{upstreamversion}/pmdk-%{upstreamversion}.tar.gz
#Patch0:         0001-test-py-add-require_free_space.patch
#Patch1:         0002-test-Fix-obj_zones-for-ppc64le.patch
#Patch2:         0003-test-build-obj_defrag_advanced-with-some-optimizatio.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libunwind-devel
BuildRequires:  make
BuildRequires:  man
BuildRequires:  pkg-config
BuildRequires:  python3

%if %{with ndctl}
BuildRequires:  daxctl-devel >= %{min_ndctl_ver}
BuildRequires:  ndctl-devel >= %{min_ndctl_ver}
%endif

%if %{with fabric}
BuildRequires:  libfabric-devel >= %{min_libfabric_ver}
%endif

%if %{with_check}
BuildRequires:  bc
BuildRequires:  gdb
BuildRequires:  glibc-devel
BuildRequires:  valgrind
%endif

# By design, PMDK does not support any 32-bit architecture.
# Due to dependency on some inline assembly, PMDK can be compiled only
# on these architectures:
# - x86_64
# - ppc64le (experimental)
# - aarch64 (unmaintained, supporting hardware doesn't exist?)
#
# Other 64-bit architectures could also be supported, if only there is
# a request for that, and if somebody provides the arch-specific
# implementation of the low-level routines for flushing to persistent
# memory.

# https://bugzilla.redhat.com/show_bug.cgi?id=1340634
# https://bugzilla.redhat.com/show_bug.cgi?id=1340635
# https://bugzilla.redhat.com/show_bug.cgi?id=1340637
ExclusiveArch:  x86_64 ppc64le

%description
The Persistent Memory Development Kit is a collection of libraries for
using memory-mapped persistence, optimized specifically for persistent memory.

%package -n libpmem
Summary:        Low-level persistent memory support library

%description -n libpmem
The libpmem provides low level persistent memory support. In particular,
support for the persistent memory instructions for flushing changes
to pmem is provided.

%package -n libpmem-devel
Summary:        Development files for the low-level persistent memory library
Requires:       libpmem = %{version}-%{release}

%description -n libpmem-devel
The libpmem provides low level persistent memory support. In particular,
support for the persistent memory instructions for flushing changes
to pmem is provided.

This library is provided for software which tracks every store to
pmem and needs to flush those changes to durability. Most developers
will find higher level libraries like libpmemobj to be much more
convenient.

%package -n libpmem-debug
Summary:        Debug variant of the low-level persistent memory library
Requires:       libpmem = %{version}-%{release}

%description -n libpmem-debug
The libpmem provides low level persistent memory support. In particular,
support for the persistent memory instructions for flushing changes
to pmem is provided.

This sub-package contains debug variant of the library, providing
run-time assertions and trace points. The typical way to access the
debug version is to set the environment variable LD_LIBRARY_PATH to
%{_libdir}/pmdk_debug.

%package -n libpmemblk-devel
Summary:        Development files for the Persistent Memory Resident Array of Blocks library
Requires:       libpmem-devel = %{version}-%{release}
Requires:       libpmemblk = %{version}-%{release}

%description -n libpmemblk-devel
The libpmemblk implements a pmem-resident array of blocks, all the same
size, where a block is updated atomically with respect to power
failure or program interruption (no torn blocks).

For example, a program keeping a cache of fixed-size objects in pmem
might find this library useful. This library is provided for cases
requiring large arrays of objects at least 512 bytes each. Most
developers will find higher level libraries like libpmemobj to be
more generally useful.

%package -n libpmemblk
Summary:        Persistent Memory Resident Array of Blocks library
Requires:       libpmem >= %{version}-%{release}

%description -n libpmemblk
The libpmemblk implements a pmem-resident array of blocks, all the same
size, where a block is updated atomically with respect to power
failure or program interruption (no torn blocks).

%package -n libpmemblk-debug
Summary:        Debug variant of the Persistent Memory Resident Array of Blocks library
Requires:       libpmemblk = %{version}-%{release}

%description -n libpmemblk-debug
The libpmemblk implements a pmem-resident array of blocks, all the same
size, where a block is updated atomically with respect to power
failure or program interruption (no torn blocks).

This sub-package contains debug variant of the library, providing
run-time assertions and trace points. The typical way to access the
debug version is to set the environment variable LD_LIBRARY_PATH to
%{_libdir}/pmdk_debug.

%package -n libpmemlog
Summary:        Persistent Memory Resident Log File library
Requires:       libpmem >= %{version}-%{release}

%description -n libpmemlog
The libpmemlog library provides a pmem-resident log file. This is
useful for programs like databases that append frequently to a log
file.

%package -n libpmemlog-devel
Summary:        Development files for the Persistent Memory Resident Log File library
Requires:       libpmem-devel = %{version}-%{release}
Requires:       libpmemlog = %{version}-%{release}

%description -n libpmemlog-devel
The libpmemlog library provides a pmem-resident log file. This
library is provided for cases requiring an append-mostly file to
record variable length entries. Most developers will find higher
level libraries like libpmemobj to be more generally useful.

%package -n libpmemlog-debug
Summary:        Debug variant of the Persistent Memory Resident Log File library
Requires:       libpmemlog = %{version}-%{release}

%description -n libpmemlog-debug
The libpmemlog library provides a pmem-resident log file. This
library is provided for cases requiring an append-mostly file to
record variable length entries. Most developers will find higher
level libraries like libpmemobj to be more generally useful.

This sub-package contains debug variant of the library, providing
run-time assertions and trace points. The typical way to access the
debug version is to set the environment variable LD_LIBRARY_PATH to
%{_libdir}/pmdk_debug.

%package -n libpmemobj
Summary:        Persistent Memory Transactional Object Store library
Requires:       libpmem >= %{version}-%{release}

%description -n libpmemobj
The libpmemobj library provides a transactional object store,
providing memory allocation, transactions, and general facilities for
persistent memory programming.

%package -n libpmemobj-devel
Summary:        Development files for the Persistent Memory Transactional Object Store library
Requires:       libpmem-devel = %{version}-%{release}
Requires:       libpmemobj = %{version}-%{release}

%description -n libpmemobj-devel
The libpmemobj library provides a transactional object store,
providing memory allocation, transactions, and general facilities for
persistent memory programming. Developers new to persistent memory
probably want to start with this library.

%package -n libpmemobj-debug
Summary:        Debug variant of the Persistent Memory Transactional Object Store library
Requires:       libpmemobj = %{version}-%{release}

%description -n libpmemobj-debug
The libpmemobj library provides a transactional object store,
providing memory allocation, transactions, and general facilities for
persistent memory programming. Developers new to persistent memory
probably want to start with this library.

This sub-package contains debug variant of the library, providing
run-time assertions and trace points. The typical way to access the
debug version is to set the environment variable LD_LIBRARY_PATH to
%{_libdir}/pmdk_debug.

%package -n libpmempool
Summary:        Persistent Memory pool management library
Requires:       libpmem >= %{version}-%{release}

%description -n libpmempool
The libpmempool library provides a set of utilities for off-line
administration, analysis, diagnostics and repair of persistent memory
pools created by libpmemlog, libpmemblk and libpmemobj libraries.

%package -n libpmempool-devel
Summary:        Development files for Persistent Memory pool management library
Requires:       libpmem-devel = %{version}-%{release}
Requires:       libpmempool = %{version}-%{release}

%description -n libpmempool-devel
The libpmempool library provides a set of utilities for off-line
administration, analysis, diagnostics and repair of persistent memory
pools created by libpmemlog, libpmemblk and libpmemobj libraries.

%package -n libpmempool-debug
Summary:        Debug variant of the Persistent Memory pool management library
Requires:       libpmempool = %{version}-%{release}

%description -n libpmempool-debug
The libpmempool library provides a set of utilities for off-line
administration, analysis, diagnostics and repair of persistent memory
pools created by libpmemlog, libpmemblk and libpmemobj libraries.

This sub-package contains debug variant of the library, providing
run-time assertions and trace points. The typical way to access the
debug version is to set the environment variable LD_LIBRARY_PATH to
%{_libdir}/pmdk_debug.

%package -n pmempool
Summary:        Utilities for Persistent Memory
Requires:       libpmem >= %{version}-%{release}
Requires:       libpmemblk >= %{version}-%{release}
Requires:       libpmemlog >= %{version}-%{release}
Requires:       libpmemobj >= %{version}-%{release}
Requires:       libpmempool >= %{version}-%{release}
Obsoletes:      nvml-tools < %{version}-%{release}

%description -n pmempool
The pmempool is a standalone utility for management and off-line analysis
of Persistent Memory pools created by PMDK libraries. It provides a set
of utilities for administration and diagnostics of Persistent Memory pools.
The pmempool may be useful for troubleshooting by system administrators
and users of the applications based on PMDK libraries.

%if %{with fabric}
%package -n librpmem
Summary:        Remote Access to Persistent Memory library
Requires:       libfabric >= %{min_libfabric_ver}
Requires:       openssh-clients

%description -n librpmem
The librpmem library provides low-level support for remote access
to persistent memory utilizing RDMA-capable NICs. It can be used
to replicate persistent memory regions over RDMA protocol.

%package -n librpmem-devel
Summary:        Development files for the Remote Access to Persistent Memory library
Requires:       librpmem = %{version}-%{release}

%description -n librpmem-devel
The librpmem library provides low-level support for remote access
to persistent memory utilizing RDMA-capable NICs. It can be used
to replicate persistent memory regions over RDMA protocol.

This sub-package contains libraries and header files for developing
applications that want to specifically make use of librpmem.

%package -n librpmem-debug
Summary:        Debug variant of the Remote Access to Persistent Memory library
Requires:       librpmem = %{version}-%{release}

%description -n librpmem-debug
The librpmem library provides low-level support for remote access
to persistent memory utilizing RDMA-capable NICs. It can be used
to replicate persistent memory regions over RDMA protocol.

This sub-package contains debug variant of the library, providing
run-time assertions and trace points. The typical way to access the
debug version is to set the environment variable LD_LIBRARY_PATH to
%{_libdir}/pmdk_debug.

%package -n rpmemd
Summary:        Target node process executed by librpmem
Requires:       libfabric >= %{min_libfabric_ver}

%description -n rpmemd
The rpmemd process is executed on a target node by librpmem library
and facilitates access to persistent memory over RDMA.

# _with_fabric
%endif

%if %{with ndctl}
%package -n daxio
Summary:        Perform I/O on Device DAX devices or zero a Device DAX device
Requires:       libpmem >= %{version}-%{release}

%description -n daxio
The daxio utility performs I/O on Device DAX devices or zero
a Device DAX device.  Since the standard I/O APIs (read/write) cannot be used
with Device DAX, data transfer is performed on a memory-mapped device.
The daxio may be used to dump Device DAX data to a file, restore data from
a backup copy, move/copy data to another device or to erase data from
a device.

# _with_ndctl
%endif

%if %{with pmemcheck}
%package -n pmreorder
Summary:        Consistency Checker for Persistent Memory
Requires:       python3

%description -n pmreorder
The pmreorder tool is a collection of python scripts designed to parse
and replay operations logged by pmemcheck - a persistent memory checking tool.
Pmreorder performs the store reordering between persistent memory barriers -
a sequence of flush-fence operations. It uses a consistency checking routine
provided in the command line options to check whether files are in a consistent state.

# _with_pmemcheck
%endif

%prep
%autosetup -p1 -n pmdk-%{upstreamversion}

%build
%make_build NORPATH=1

# Override LIB_AR with empty string to skip installation of static libraries
%install
%make_install \
	LIB_AR= \
	prefix=%{_prefix} \
	libdir=%{_libdir} \
	includedir=%{_includedir} \
	mandir=%{_mandir} \
	bindir=%{_bindir} \
	sysconfdir=%{_sysconfdir} \
	docdir=%{_docdir}
mkdir -p %{buildroot}%{_datadir}/pmdk
cp utils/pmdk.magic %{buildroot}%{_datadir}/pmdk/

%check
cat << EOF > src/test/testconfig.sh
PMEM_FS_DIR=/tmp
PMEM_FS_DIR_FORCE_PMEM=1
TEST_BUILD="debug nondebug"
TM=1
EOF

cat << EOF > src/test/testconfig.py
config = {
  'pmem_fs_dir': '/tmp',
  'fs_dir_force_pmem': 1,
  'build': ['debug', 'release'],
  'tm': 1,
  'test_type': 'check',
  'fs': 'all',
  'unittest_log_level': 1,
  'keep_going': False,
  'timeout': '3m',
  'dump_lines': 30,
  'force_enable': None,
  'device_dax_path': [],
}
EOF

make pycheck
make check

%ldconfig_scriptlets   -n libpmem
%ldconfig_scriptlets   -n libpmemblk
%ldconfig_scriptlets   -n libpmemlog
%ldconfig_scriptlets   -n libpmemobj
%ldconfig_scriptlets   -n libpmempool

%if %{with fabric}
%ldconfig_scriptlets   -n librpmem
%endif

%files -n libpmem
%dir %{_datadir}/pmdk
%{_libdir}/libpmem.so.*
%{_datadir}/pmdk/pmdk.magic
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md

%files -n libpmem-devel
%{_libdir}/libpmem.so
%{_libdir}/pkgconfig/libpmem.pc
%{_includedir}/libpmem.h
%{_mandir}/man7/libpmem.7.gz
%{_mandir}/man3/pmem_*.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md

%files -n libpmem-debug
%dir %{_libdir}/pmdk_debug
%{_libdir}/pmdk_debug/libpmem.so
%{_libdir}/pmdk_debug/libpmem.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md

%files -n libpmemblk
%{_libdir}/libpmemblk.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md

%files -n libpmemblk-devel
%{_libdir}/libpmemblk.so
%{_libdir}/pkgconfig/libpmemblk.pc
%{_includedir}/libpmemblk.h
%{_mandir}/man7/libpmemblk.7.gz
%{_mandir}/man5/poolset.5.gz
%{_mandir}/man3/pmemblk_*.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md

%files -n libpmemblk-debug
%dir %{_libdir}/pmdk_debug
%{_libdir}/pmdk_debug/libpmemblk.so
%{_libdir}/pmdk_debug/libpmemblk.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md

%files -n libpmemlog
%{_libdir}/libpmemlog.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md

%files -n libpmemlog-devel
%{_libdir}/libpmemlog.so
%{_libdir}/pkgconfig/libpmemlog.pc
%{_includedir}/libpmemlog.h
%{_mandir}/man7/libpmemlog.7.gz
%{_mandir}/man5/poolset.5.gz
%{_mandir}/man3/pmemlog_*.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md

%files -n libpmemlog-debug
%dir %{_libdir}/pmdk_debug
%{_libdir}/pmdk_debug/libpmemlog.so
%{_libdir}/pmdk_debug/libpmemlog.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md

%files -n libpmemobj
%{_libdir}/libpmemobj.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md

%files -n libpmemobj-devel
%{_libdir}/libpmemobj.so
%{_libdir}/pkgconfig/libpmemobj.pc
%{_includedir}/libpmemobj.h
%dir %{_includedir}/libpmemobj
%{_includedir}/libpmemobj/*.h
%{_mandir}/man7/libpmemobj.7.gz
%{_mandir}/man5/poolset.5.gz
%{_mandir}/man3/pmemobj_*.3.gz
%{_mandir}/man3/pobj_*.3.gz
%{_mandir}/man3/oid_*.3.gz
%{_mandir}/man3/toid*.3.gz
%{_mandir}/man3/direct_*.3.gz
%{_mandir}/man3/d_r*.3.gz
%{_mandir}/man3/tx_*.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md

%files -n libpmemobj-debug
%dir %{_libdir}/pmdk_debug
%{_libdir}/pmdk_debug/libpmemobj.so
%{_libdir}/pmdk_debug/libpmemobj.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md

%files -n libpmempool
%{_libdir}/libpmempool.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md

%files -n libpmempool-devel
%{_libdir}/libpmempool.so
%{_libdir}/pkgconfig/libpmempool.pc
%{_includedir}/libpmempool.h
%{_mandir}/man7/libpmempool.7.gz
%{_mandir}/man5/poolset.5.gz
%{_mandir}/man3/pmempool_*.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md

%files -n libpmempool-debug
%dir %{_libdir}/pmdk_debug
%{_libdir}/pmdk_debug/libpmempool.so
%{_libdir}/pmdk_debug/libpmempool.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md

%files -n pmempool
%{_bindir}/pmempool
%{_mandir}/man1/pmempool.1.gz
%{_mandir}/man1/pmempool-*.1.gz
%config(noreplace) %{_sysconfdir}/bash_completion.d/pmempool
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md

%if %{with fabric}

%files -n librpmem
%{_libdir}/librpmem.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md

%files -n librpmem-devel
%{_libdir}/librpmem.so
%{_libdir}/pkgconfig/librpmem.pc
%{_includedir}/librpmem.h
%{_mandir}/man7/librpmem.7.gz
%{_mandir}/man3/rpmem_*.3.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md

%files -n librpmem-debug
%dir %{_libdir}/pmdk_debug
%{_libdir}/pmdk_debug/librpmem.so
%{_libdir}/pmdk_debug/librpmem.so.*
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md

%files -n rpmemd
%{_bindir}/rpmemd
%{_mandir}/man1/rpmemd.1.gz

# _with_fabric
%endif

%if %{with ndctl}

%files -n daxio
%{_bindir}/daxio
%{_mandir}/man1/daxio.1.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md

# _with_ndctl
%endif

%if %{with pmemcheck}

%files -n pmreorder
%{_bindir}/pmreorder
%{_datadir}/pmreorder/*.py
%{_mandir}/man1/pmreorder.1.gz
%license LICENSE
%doc ChangeLog CONTRIBUTING.md README.md

# _with_pmemcheck
%endif

%changelog
* Wed Jan 24 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0.1-1
- Auto-upgrade to 2.0.1 - 3.0 release

* Wed Dec 01 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.8-4
- License verified.
- Using 'make' macros instead of manually setting flags and paths.

* Wed Jan 13 2021 Joe Schmitt <joschmit@microsoft.com> - 1.8-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Build with fabric

* Wed Feb 26 2020 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.8-2
- Enable PPC64LE packages

* Wed Feb 12 2020 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.8-1
- Update to PMDK version 1.8. This release stops shipping
  libvmem & libvmmalloc. These libraries are now provided by vmem
  package.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 1 2019 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.7-1
- Update to PMDK version 1.7

* Fri Aug 30 2019 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.6.1-1
- Update to PMDK version 1.6.1

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 26 2019 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.6-1
- Update to PMDK version 1.6

* Mon Mar 18 2019 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.6-0.1.rc2
- Update to PMDK version 1.6-rc2

* Fri Mar 08 2019 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.5.1-1
- Update to PMDK version 1.5.1

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Dec 14 2018 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.5-2
- Remove Group: tag and add ownership information for libpmemobj headers
  directory.

* Tue Nov 6 2018 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.5-1
- Update to PMDK version 1.5
  libpmemobj C++ bindings moved to separate package (RHBZ #1647145)
  pmempool convert is now a thin wrapper around pmdk-convert (RHBZ #1647147)

* Fri Aug 17 2018 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.4.2-1
- Update to PMDK version 1.4.2 (RHBZ #1589406)

* Tue Aug 14 2018 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.4.2-0.2.rc1
- Revert package name change

* Tue Aug 14 2018 Marcin Ślusarz <marcin.slusarz@intel.com> - 1.4.2-0.1.rc1
- Update to PMDK version 1.4.2-rc1 (RHBZ #1589406)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 30 2018 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.4-3
- Revert package name change
- Re-enable check

* Thu Mar 29 2018 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.4-2
- Fix issues found by rpmlint

* Thu Mar 29 2018 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.4-1
- Rename NVML project to PMDK
- Update to PMDK version 1.4 (RHBZ #1480578, #1539562, #1539564)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 27 2018 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.3.1-1
- Update to NVML version 1.3.1 (RHBZ #1480578)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.3-1
- Update to NVML version 1.3 (RHBZ #1451741, RHBZ #1455216)
- Add librpmem and rpmemd sub-packages
- Force file system to appear as PMEM for make check

* Fri Jun 16 2017 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.2.3-2
- Update to NVML version 1.2.3 (RHBZ #1451741)

* Sat Apr 15 2017 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.2.2-1
- Update to NVML version 1.2.2 (RHBZ #1436820, RHBZ #1425038)

* Thu Mar 16 2017 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.2.1-1
- Update to NVML version 1.2.1 (RHBZ #1425038)

* Tue Feb 21 2017 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.2-3
- Fix compilation under gcc 7.0.x (RHBZ #1424004)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 30 2016 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.2-1
- Update to NVML version 1.2 (RHBZ #1383467)
- Add libpmemobj C++ bindings

* Thu Jul 14 2016 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.1-3
- Add missing package version requirements

* Mon Jul 11 2016 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.1-2
- Move debug variants of the libraries to -debug subpackages

* Sun Jun 26 2016 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.1-1
- NVML 1.1 release
- Update link to source tarball
- Add libpmempool subpackage
- Remove obsolete patches

* Wed Jun 01 2016 Dan Horák <dan[at]danny.cz> - 1.0-3
- switch to ExclusiveArch

* Sun May 29 2016 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.0-2
- Exclude PPC architecture
- Add bug numbers for excluded architectures

* Tue May 24 2016 Krzysztof Czurylo <krzysztof.czurylo@intel.com> - 1.0-1
- Initial RPM release
