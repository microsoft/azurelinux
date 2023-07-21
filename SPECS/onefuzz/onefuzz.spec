Summary:        A self-hosted Fuzzing-As-A-Service platform
Name:           onefuzz
Version:        8.5.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://github.com/microsoft/OneFuzz
Source0:        https://github.com/microsoft/onefuzz/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         git-version.patch
%define debug_package %{nil}
BuildRequires:  cargo >= 1.68
BuildRequires:  git
BuildRequires:  kernel-headers
BuildRequires:  libunwind-devel
BuildRequires:  openssl-devel
BuildRequires:  perl
BuildRequires:  rust >= 1.68
BuildRequires:  util-linux

%description
Project OneFuzz enables continuous developer-driven fuzzing to proactively
harden software prior to release. With a single command, which can be baked
into CICD, developers can launch fuzz jobs from a few virtual machines to
thousands of cores.

%prep
%setup -q
%patch0 -p1

%build
cd src/agent
ONEFUZZ_SET_VERSION=%{version} RUSTFLAGS="-llzma" cargo build --release

%install
cd src/agent
mkdir -p %{buildroot}%{_bindir}
install target/release/onefuzz-agent %{buildroot}%{_bindir}/
install target/release/onefuzz-task %{buildroot}%{_bindir}/

%check
cd src/agent
# Run all tests except test_get_machine_id as that requires a specific file to exist
ONEFUZZ_SET_VERSION=%{version} RUSTFLAGS="-llzma" cargo test --release -- --skip test_get_machine_id

%files
%license LICENSE
%{_bindir}/*

%changelog
* Fri Jul 21 2023 Chris Swindle <chrisswindle@microsoft.com> - 8.5.0-1
- Original version for CBL-Mariner
- License verified
