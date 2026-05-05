%{!?configure_options: %global configure_options %{nil}}
%{!?use_rel: %global use_rel 1.2510122}

%{!?make_build: %global make_build %{__make} %{?_smp_mflags} %{?mflags} V=1}

Name: dpcp
Version: 1.1.55
Release:        1%{?dist}
Summary: Direct Packet Control Plane (DPCP) is a library to use DevX
%if 0%{?rhl}%{?fedora} == 0
Group: System Environment/Libraries
%endif

License: BSD-3-Clause
Vendor:          Microsoft Corporation
Distribution:    Azure Linux
Url: https://github.com/Mellanox/%{name}
# DOCA OFED feature sources come from the following MLNX_OFED_SRC tgz.
# This archive contains the SRPMs for each feature and each SRPM includes the source tarball and the SPEC file.
# https://linux.mellanox.com/public/repo/doca/3.2.2/SOURCES/mlnx_ofed/OFED-internal-25.10-2.4.1.tgz
Source0:         %{_distro_sources_url}/dpcp-1.1.55.tar.gz
Source1: %{name}-%{version}.tar.gz

%if 0%{?rhl}%{?fedora} == 0
BuildRoot:       /var/tmp/%{name}-%{version}-build
%endif

# project currently supports only the following architectures
ExclusiveArch: x86_64 ppc64le ppc64 aarch64

BuildRequires: pkgconfig
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: gcc-c++
BuildRequires: rdma-core-devel

%description
Direct Packet Control Plane (DPCP) provides an unified flexible
interface for programming IB devices using DevX.

%prep
%setup -q

%build
if [ ! -e configure ] && [ -e autogen.sh ]; then
    PRJ_RELEASE=%{use_rel} ./autogen.sh
fi

%configure \
           %{?configure_options}
%{make_build}

%install
%if 0%{?rhl}%{?fedora} == 0
[ "${RPM_BUILD_ROOT}" != "/" -a -d ${RPM_BUILD_ROOT} ] && rm -rf ${RPM_BUILD_ROOT}
%endif

%{make_build} DESTDIR=%{buildroot} install

find $RPM_BUILD_ROOT%{_libdir} -name '*.la' -delete
find $RPM_BUILD_ROOT%{_libdir} -name '*.a' -delete

%clean
%if 0%{?rhl}%{?fedora} == 0
[ "${RPM_BUILD_ROOT}" != "/" -a -d ${RPM_BUILD_ROOT} ] && rm -rf ${RPM_BUILD_ROOT}
%endif

%files
%{_libdir}/lib%{name}.so*
%{_includedir}/mellanox/dpcp.h
%doc README.md
%if 0%{?rhel} >= 7 || 0%{?fedora} >= 24 || 0%{?suse_version} >= 1500
%license LICENSE
%endif

%changelog
* Thu Apr 17 2026 Azure Linux Team - 1.1.55-1
- Initial Azure Linux import from NVIDIA (license: BSD-3-Clause)
- License verified
