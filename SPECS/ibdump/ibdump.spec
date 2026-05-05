%bcond_with mlnx_libs
%if %{with mlnx_libs}
%define libs_exp_arg LIBS_EXP=yes
%else
%define libs_exp_arg %{nil}
%endif

%bcond_with mstflint
%if %{with mstflint}
%define mstflint_arg WITH_MSTFLINT=yes
%else
%define mstflint_arg %{nil}
%endif

%if %{undefined make_build}
%global make_build %{__make} %{?_smp_mflags}
%endif

%define make_opts %{libs_exp_arg} PREFIX=%{_prefix} WITHOUT_FW_TOOLS=yes

%if 0%{?_ver:1}
%define ver 6.0.0
%else
%define ver 6.0.0
%endif

%if 0%{?_rel:1}
%define rel 2
%else
%define rel 1
%endif

Summary: Mellanox InfiniBand sniffing application
Name: ibdump 
Version: 6.0.0
Release:        1%{?dist}
License: BSD2+GPL2
Vendor:          Microsoft Corporation
Distribution:    Azure Linux
Group: System Environment/Base
BuildRoot:       /var/tmp/%{name}-%{version}-build
# DOCA OFED feature sources come from the following MLNX_OFED_SRC tgz.
# This archive contains the SRPMs for each feature and each SRPM includes the source tarball and the SPEC file.
# https://linux.mellanox.com/public/repo/doca/3.2.2/SOURCES/mlnx_ofed/OFED-internal-25.10-2.4.1.tgz
Source0:         %{_distro_sources_url}/ibdump-6.0.0-3.2.2.tar.gz
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: libibverbs-devel
ExclusiveArch: i386 i486 i586 i686 x86_64 ppc64 ppc64le aarch64
Url: https://github.com/Mellanox/ibdump

%description
InfiniBand sniffer for MellanoX Technologies LTD. ConnectX HCAs

%prep
%setup -n %{name}-%{version}

%build
%make_build %{make_opts}

%install
rm -rf $RPM_BUILD_ROOT
%{make_install} %{make_opts}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/ibdump
%{_bindir}/vpi_tcpdump

%changelog
* Thu Apr 17 2026 Azure Linux Team - 6.0.0-1
- Initial Azure Linux import from NVIDIA (license: BSD2+GPL2)
- License verified
