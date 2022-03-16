Summary:        A Rust-VMM based cloud hypervisor from Intel
Name:           cloud-hypervisor
Version:        22.0
Release:        1%{?dist}
License:        ASL 2.0 or BSD
URL:            https://github.com/cloud-hypervisor/cloud-hypervisor
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:       %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Note: the %%{name}-%%{version}-cargo.tar.gz file contains a cache created by capturing the contents downloaded into $CARGO_HOME.
# To update the cache run:
#   [repo_root]/toolkit/scripts/build_cargo_cache.sh %%{name}-%%{version}.tar.gz
Source1:        %{name}-%{version}-cargo.tar.gz
BuildRequires:  binutils
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  glibc-devel
BuildRequires:  rust
ExclusiveArch:  x86_64

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

%files
%defattr(-,root,root)
%license LICENSE-APACHE
%{_bindir}/*
%exclude %{_libdir}/debug

%changelog
* Wed Mar 09 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 22.0-1
- Updating to version 22.0 to build with 'rust' 1.59.0.

* Tue Feb 08 2022 Henry Li <lihl@microsoft.com> - 21.0-1
- Update to version 21.0

* Wed Dec 01 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 19.0-1
- Updating to version 19.0 to use existing dependencies and build with the 1.56.1 version of 'rust'.

* Mon Apr 26 2021 Thomas Crain <thcrain@microsoft.com> - 0.6.0-7
- Bump release to rebuild with rust 1.47.0-3 (security update)

* Tue Apr 20 2021 Thomas Crain <thcrain@microsoft.com> - 0.6.0-6
- Bump release to rebuild with rust 1.47.0-2 (security update)

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.6.0-5
- Added %%license line automatically

* Thu May 07 2020 Nicolas Guibourge <mrgirgin@microsoft.com> - 0.6.0-4
- Fix docker based build issue

* Mon May 04 2020 Emre Girgin <mrgirgin@microsoft.com> - 0.6.0-3
- Replace BuildArch with ExclusiveArch

* Fri Apr 24 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.6.0-3
- License verified.
- Fixed Source0 tag.

* Tue Apr 21 2020 Andrew Phelps <anphel@microsoft.com> - 0.6.0-2
- Support building offline with prepopulated .cargo directory.

* Thu Feb 13 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 0.6.0-1
- Original version for CBL-Mariner.
