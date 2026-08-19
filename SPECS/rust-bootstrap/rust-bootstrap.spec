Summary:        Prebuilt stage0 bootstrap toolchain used to build rust
Name:           rust-bootstrap
Version:        1.95.0
Release:        1%{?dist}
License:        (ASL 2.0 OR MIT) AND BSD AND CC-BY-3.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages
URL:            https://www.rust-lang.org/
BuildArch:      noarch

# Notes:
#  - These are the official upstream prebuilt cargo/rustc/rust-std tarballs
#    consumed by rust.spec to bootstrap-compile a new toolchain from source.
#  - When bumping "stage0_version"/"release_date" in rust.spec, bump the same
#    values here (Version and %{release_date}) and rebuild this package first.
%define release_date 2026-04-16

Source0:        https://static.rust-lang.org/dist/%{release_date}/cargo-%{version}-x86_64-unknown-linux-gnu.tar.xz
Source1:        https://static.rust-lang.org/dist/%{release_date}/rustc-%{version}-x86_64-unknown-linux-gnu.tar.xz
Source2:        https://static.rust-lang.org/dist/%{release_date}/rust-std-%{version}-x86_64-unknown-linux-gnu.tar.xz
Source3:        https://static.rust-lang.org/dist/%{release_date}/cargo-%{version}-aarch64-unknown-linux-gnu.tar.xz
Source4:        https://static.rust-lang.org/dist/%{release_date}/rustc-%{version}-aarch64-unknown-linux-gnu.tar.xz
Source5:        https://static.rust-lang.org/dist/%{release_date}/rust-std-%{version}-aarch64-unknown-linux-gnu.tar.xz

%description
Prebuilt cargo/rustc/rust-std stage0 tarballs (x86_64 and aarch64) consumed
by the rust package to bootstrap-compile a new toolchain. Not intended for
direct/standalone use.

%prep
# Nothing to unpack, sources are installed as-is.

%build
# Nothing to build, sources are installed as-is.

%install
mkdir -p %{buildroot}%{_datadir}/rust-bootstrap/%{version}
cp %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} \
    %{buildroot}%{_datadir}/rust-bootstrap/%{version}/

%files
%{_datadir}/rust-bootstrap/%{version}/

%changelog
* Wed Aug 19 2026 Kavya Sree Kaitepalli <kkaitepalli@microsoft.com> - 1.95.0-1
- Original version. Split out of rust.spec to keep its SRPM small.
