Summary:        A Rust-VMM based cloud hypervisor from Intel
Name:           cloud-hypervisor
Version:        22.0
Release:        3%{?dist}
License:        ASL 2.0 or BSD
URL:            https://github.com/cloud-hypervisor/cloud-hypervisor
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-cargo-%{release}.tar.gz
Source2:        %{name}-%{version}-vendor-%{release}.tar.gz
Patch0:         CVE-2023-28448.patch
Patch1:         CVE-2023-2650.patch
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
tar xf %{SOURCE1} --no-same-owner
%patch0 -p1
%setup -q
%patch1 -p1
tar xf %{SOURCE2} -C ../ --no-same-owner

%build
CARGO_HOME=$(pwd)/../.cargo cargo build --release --offline

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
%{_libdir}/cloud-hypervisor
%exclude %{_libdir}/debug

%changelog
* Tue Jul 04 2023 Suresh Thelkar <sthelkar@microsoft.com> - 22.0-3
- Patch CVE-2023-0465 and CVE-2023-2650

* Wed Apr 05 2023 Henry Beberman <henry.beberman@microsoft.com> - 22.0-2
- Patch CVE-2023-28448 in vendored versionize crate

* Wed Mar 09 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 22.0-1
- Updating to version 22.0 to build with 'rust' 1.59.0.

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
