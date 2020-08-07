Summary:        A Rust-VMM based cloud hypervisor from Intel
Name:           cloud-hypervisor
Version:        0.6.0
Release:        5%{?dist}
License:        ASL 2.0 or BSD
URL:            https://github.com/cloud-hypervisor/cloud-hypervisor
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner
#Source0:       %{url}/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-cargo.tar.gz
ExclusiveArch:  x86_64

BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  binutils
BuildRequires:  rust
BuildRequires:  git

%description
A Rust-VMM based cloud hypervisor from Intel.

%prep
# Setup .cargo directory
mkdir -p $HOME
pushd $HOME
tar xf %{SOURCE1} --no-same-owner
popd
%setup -q

%build
cargo build --release

%install
install -d %{buildroot}%{_bindir}
install -D -m755 target/release/ch-remote %{buildroot}%{_bindir}
install -D -m755 target/release/cloud-hypervisor %{buildroot}%{_bindir}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_libdir}/cloud-hypervisor
install -D -m755 target/release/vhost_user_blk %{buildroot}%{_libdir}/cloud-hypervisor
install -D -m755 target/release/vhost_user_fs %{buildroot}%{_libdir}/cloud-hypervisor
install -D -m755 target/release/vhost_user_net %{buildroot}%{_libdir}/cloud-hypervisor

%files
%defattr(-,root,root)
%license LICENSE-APACHE
%{_bindir}/*
%{_libdir}/cloud-hypervisor
%exclude %{_libdir}/debug

%changelog
*   Sat May 09 00:21:14 PST 2020 Nick Samson <nisamson@microsoft.com> - 0.6.0-5
-   Added %%license line automatically
*   Thu May 07 2020 Nicolas Guibourge <mrgirgin@microsoft.com> 0.6.0-4
-   Fix docker based build issue
*   Mon May 04 2020 Emre Girgin <mrgirgin@microsoft.com> 0.6.0-3
-   Replace BuildArch with ExclusiveArch
*   Fri Apr 24 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.6.0-3
-   License verified.
-   Fixed Source0 tag.
*   Tue Apr 21 2020 Andrew Phelps <anphel@microsoft.com> 0.6.0-2
-   Support building offline with prepopulated .cargo directory.
*   Thu Feb 13 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> 0.6.0-1
-   Original version for CBL-Mariner.