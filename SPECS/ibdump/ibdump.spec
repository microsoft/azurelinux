# https://linux.mellanox.com/public/repo/doca/3.3.0/SOURCES/mlnx_ofed/OFED-internal-26.01-1.0.0.0.tgz
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

%define make_opts %{libs_exp_arg} PREFIX=%{_prefix}

Summary: Mellanox InfiniBand sniffing application
Name: ibdump
Version: 6.0.0
Release: 1%{?dist}
License: BSD2+GPL2
Group: System Environment/Base
Vendor: Microsoft Corporation
Distribution: Azure Linux
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}
Source0: %{_distro_sources_url}/%{name}-%{version}_doca-3.3.0.tar.gz
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
%make_build %{make_opts} WITHOUT_FW_TOOLS=yes

%install
rm -rf $RPM_BUILD_ROOT
%{make_install} %{make_opts} WITHOUT_FW_TOOLS=yes

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/ibdump
%{_bindir}/vpi_tcpdump

%changelog
* Mon May 11 2026 Azure Linux Team - 6.0.0-1
- Initial Azure Linux import from NVIDIA (license: BSD)
- License verified
- Upgrade to DOCA 3.3.0 (OFED 26.01-1.0.0.0)
