%global rel 1.2510122
%global version 3.13.12
%global pkgname sharp
%global prefix /opt/mellanox/sharp
%global __check_files %{nil}
%global _libdir %{prefix}/lib
%{!?configure_opts: %global configure_opts %{nil}}
%global  debug_package %{nil}
%bcond_with valgrind

# Remove the filedigest algorithm since it is old definition 
# and new algorithms are used by default
#global _binary_filedigest_algorithm 1
#global _source_filedigest_algorithm 1

%global lt_release @LT_RELEASE@
%global lt_version @LT_CURRENT@.@LT_REVISION@.@LT_AGE@

%bcond_with    cuda
%bcond_with    gdrcopy

Name: %{pkgname}
Summary: Scalable Hierarchical Aggregation Protocol
Version: %{version}
Release:        1%{?dist}

License: Proprietary
Group: Applications
# DOCA OFED feature sources come from the following MLNX_OFED_SRC tgz.
# This archive contains the SRPMs for each feature and each SRPM includes the source tarball and the SPEC file.
# https://linux.mellanox.com/public/repo/doca/3.2.2/SOURCES/mlnx_ofed/OFED-internal-25.10-2.4.1.tgz
Source0:         %{_distro_sources_url}/sharp-3.13.12.tar.gz
Requires: libibverbs
%if 0%{?suse_version} < 1100
BuildRequires: gcc-c++ libibverbs-devel binutils
%else
BuildRequires: gcc-c++ libibverbs-devel binutils-devel
%endif
%if %{with valgrind}
BuildRequires: valgrind-devel
%endif
%if %{with gdrcopy}
BuildRequires: gdrcopy
%endif

BuildRoot:       /var/tmp/%{name}-%{version}-build
URL: http://www.mellanox.com
Prefix: %{prefix}
Packager: sharp
Vendor:          Microsoft Corporation


%description
SHArP is a switch collectives library

%prep
rm -rf $RPM_BUILD_ROOT

%setup -q

%build
%define _with_arg()   %{expand:%%{?with_%{1}:--with-%{2}}%%{!?with_%{1}:--without-%{2}}}
%define _enable_arg() %{expand:%%{?with_%{1}:--enable-%{2}}%%{!?with_%{1}:--disable-%{2}}}
./contrib/configure-release \
                     %_with_arg cuda cuda \
                     %_with_arg gdrcopy gdrcopy \
                     %{configure_opts}
make %{?_smp_mflags}

%install

rm -rf "$RPM_BUILD_ROOT"

# Strip out some dependencies
cat > find-requires.sh <<'EOF'
exec %{__find_requires} "$@" | egrep -v '^perl'
EOF
chmod +x find-requires.sh
%global _use_internal_dependency_generator 0
%global __find_requires %{_builddir}/%{buildsubdir}/find-requires.sh

make DESTDIR="$RPM_BUILD_ROOT" install
mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d/
echo %{_libdir} > $RPM_BUILD_ROOT/etc/ld.so.conf.d/sharp.conf
mkdir -p $RPM_BUILD_ROOT/usr/lib64/pkgconfig
cp sharp.pc $RPM_BUILD_ROOT/usr/lib64/pkgconfig

%clean
# We may be in the directory that we're about to remove, so cd out of
# there before we remove it
cd /tmp

# Remove installed driver after rpm build finished
chmod -R o+w $RPM_BUILD_DIR/%{name}-%{version}
rm -rf $RPM_BUILD_DIR/%{name}-%{version}

test "x$RPM_BUILD_ROOT" != "x" && rm -rf $RPM_BUILD_ROOT


%files
%defattr(-, root, root)
%{prefix}
/etc/ld.so.conf.d/sharp.conf
/usr/lib64/pkgconfig/sharp.pc
%if %{with cuda}
%exclude %{_libdir}/libsharp_coll_cuda*
%endif
%if %{with gdrcopy}
%exclude %{_libdir}/libsharp_coll_gdrcopy*
%endif


# sharp-cuda
%if %{with cuda}
%package cuda
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: SHARP CUDA support

%description cuda
Provide CUDA (NVIDIA GPU) support for HCOLL. Enables passing GPU memory pointers
to HCOLL collective routine

%files cuda
%{_libdir}/libsharp_coll_cuda*
%if %{with gdrcopy}
%{_libdir}/libsharp_coll_gdrcopy*
%endif
%endif


# Your application file list goes here
# %{prefix}/lib/lib*.so*
#%doc COPYRIGHT ChangeLog README AUTHORS NEWS
#%doc doc/*

# If you install a library
%post
/sbin/ldconfig || exit 1

%preun
# Remove sharp_am daemon only in case of rpm removal/uninstallation (preserve in case of rpm upgrade)
if [ $1 == 0 ]; then
	%{prefix}/sbin/sharp_daemons_setup.sh -r -d sharp_am &> /dev/null || true
fi

# If you install a library
%postun
/sbin/ldconfig
exit 0


%changelog
* Thu Apr 17 2026 Azure Linux Team - 3.13.12-1
- Initial Azure Linux import from NVIDIA (license: Proprietary)
- License verified
