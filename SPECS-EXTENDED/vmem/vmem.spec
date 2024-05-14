
# rpmbuild options:
#   --define _testconfig <path to custom testconfig.sh>

%define upstreamversion 1.8

Name:		vmem
Version:	%{upstreamversion}
Release:	2%{?dist}
Summary:	Volatile Memory Development Kit
License:	BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:		https://pmem.io/vmem

Source0:	https://github.com/pmem/vmem/archive/%{upstreamversion}.tar.gz#/%{name}-%{version}.tar.gz


BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	glibc-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	man
BuildRequires:	pkgconfig

# for tests
BuildRequires:	gdb
BuildRequires:	bc
BuildRequires:	libunwind-devel

# Debug variants of the libraries should be filtered out of the provides.
%global __provides_exclude_from ^%{_libdir}/vmem_debug/.*\\.so.*$

# By design, no 32-bit architectures are supported.  As for 64-bit archs,
# there's generally no reason porting couldn't be done, but someone would
# need to do the work.  Outside of x86_64, aarch64 works -- but no one did
# any serious testing.
#
# Bugs reported for the PMDK project that VMEM originally comes from:

# https://bugzilla.redhat.com/show_bug.cgi?id=1340634
# https://bugzilla.redhat.com/show_bug.cgi?id=1340635
# https://bugzilla.redhat.com/show_bug.cgi?id=1340636
# https://bugzilla.redhat.com/show_bug.cgi?id=1340637

ExclusiveArch: x86_64

%description
vmem and vmmalloc are libraries for using persistent memory as volatile
heap for malloc-like allocations.


%package -n libvmem
Summary: Volatile Memory allocation library
%description -n libvmem
The libvmem library turns a pool of persistent memory into a volatile
memory pool, similar to the system heap but kept separate and with
its own malloc-style API.

%files -n libvmem
%{_libdir}/libvmem.so.*
%license LICENSE
%doc ChangeLog README.md


%package -n libvmem-devel
Summary: Development files for the Volatile Memory allocation library
Requires: libvmem = %{version}-%{release}
%description -n libvmem-devel
The libvmem library turns a pool of persistent memory into a volatile
memory pool, similar to the system heap but kept separate and with
its own malloc-style API.

This sub-package contains libraries and header files for developing
applications that want to make use of libvmem.

%files -n libvmem-devel
%{_libdir}/libvmem.so
%{_libdir}/pkgconfig/libvmem.pc
%{_includedir}/libvmem.h
%{_mandir}/man7/libvmem.7.gz
%{_mandir}/man3/vmem_*.3.gz
%license LICENSE
%doc ChangeLog README.md


%package -n libvmem-debug
Summary: Debug variant of the Volatile Memory allocation library
Requires: libvmem = %{version}-%{release}
%description -n libvmem-debug
The libvmem library turns a pool of persistent memory into a volatile
memory pool, similar to the system heap but kept separate and with
its own malloc-style API.

This sub-package contains debug variant of the library, providing
run-time assertions and trace points. The typical way to access the
debug version is to set the environment variable LD_LIBRARY_PATH to
/usr/lib64/vmem_debug.

%files -n libvmem-debug
%dir %{_libdir}/vmem_debug
%{_libdir}/vmem_debug/libvmem.so
%{_libdir}/vmem_debug/libvmem.so.*
%license LICENSE
%doc ChangeLog README.md


%package -n libvmmalloc
Summary: Dynamic to Persistent Memory allocation translation library
%description -n libvmmalloc
The libvmmalloc library transparently converts all the dynamic memory
allocations into persistent memory allocations. This allows the use
of persistent memory as volatile memory without modifying the target
application.

The typical usage of libvmmalloc is to load it via the LD_PRELOAD
environment variable.

%files -n libvmmalloc
%{_libdir}/libvmmalloc.so.*
%license LICENSE
%doc ChangeLog README.md


%package -n libvmmalloc-devel
Summary: Development files for the Dynamic-to-Persistent allocation library
Requires: libvmmalloc = %{version}-%{release}
%description -n libvmmalloc-devel
The libvmmalloc library transparently converts all the dynamic memory
allocations into persistent memory allocations. This allows the use
of persistent memory as volatile memory without modifying the target
application.

This sub-package contains libraries and header files for developing
applications that want to specifically make use of libvmmalloc.

%files -n libvmmalloc-devel
%{_libdir}/libvmmalloc.so
%{_libdir}/pkgconfig/libvmmalloc.pc
%{_includedir}/libvmmalloc.h
%{_mandir}/man7/libvmmalloc.7.gz
%license LICENSE
%doc ChangeLog README.md


%package -n libvmmalloc-debug
Summary: Debug variant of the Dynamic-to-Persistent allocation library
Requires: libvmmalloc = %{version}-%{release}
%description -n libvmmalloc-debug
The libvmmalloc library transparently converts all the dynamic memory
allocations into persistent memory allocations. This allows the use
of persistent memory as volatile memory without modifying the target
application.

This sub-package contains debug variant of the library, providing
run-time assertions and trace points. The typical way to access the
debug version is to set the environment variable LD_LIBRARY_PATH to
/usr/lib64/vmem_debug.

%files -n libvmmalloc-debug
%dir %{_libdir}/vmem_debug
%{_libdir}/vmem_debug/libvmmalloc.so
%{_libdir}/vmem_debug/libvmmalloc.so.*
%license LICENSE
%doc ChangeLog README.md


%prep
%setup -q -n vmem-%{upstreamversion}


%build
# For debug build default flags may be overriden to disable compiler
# optimizations.
CFLAGS="%{optflags}" \
LDFLAGS="%{?__global_ldflags}" \
make %{?_smp_mflags} NORPATH=1


# Override LIB_AR with empty string to skip installation of static libraries
%install
make install DESTDIR=%{buildroot} \
	LIB_AR= \
	prefix=%{_prefix} \
	libdir=%{_libdir} \
	includedir=%{_includedir} \
	mandir=%{_mandir} \
	bindir=%{_bindir} \
	sysconfdir=%{_sysconfdir} \
	docdir=%{_docdir}



%check
%if 0%{?_skip_check} == 1
	echo "Check skipped"
%else
	%if %{defined _testconfig}
		cp %{_testconfig} src/test/testconfig.sh
	%else
		echo "TEST_DIR=/tmp" > src/test/testconfig.sh
		echo 'TEST_BUILD="debug nondebug"' >> src/test/testconfig.sh
	%endif
	make check
%endif

%ldconfig_scriptlets   -n libvmem
%ldconfig_scriptlets   -n libvmmalloc

%if 0%{?__debug_package} == 0
%debug_package
%endif


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.8-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Feb 11 2020 Adam Borowski <kilobyte@angband.pl> - 1.8-1
- Upstream release 1.8
- Re-add libunwind-devel to BReqs.

* Fri Jan 24 2020 Adam Borowski <kilobyte@angband.pl> - 1.8~rc1-1
- Initial RPM release
