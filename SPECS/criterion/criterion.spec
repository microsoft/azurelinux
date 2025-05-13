Name:           criterion
Version:        2.4.2
Release:        1%{?dist}
Summary:        A cross-platform C and C++ testing framework

License:        MIT
URL:            https://github.com/Snaipe/Criterion
Source0:        https://github.com/Snaipe/Criterion/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://github.com/scottt/debugbreak/archive/v1.0.tar.gz#/debugbreak-1.0.tar.gz
Source2:        https://github.com/attractivechaos/klib/archive/5c1451caa1ee476624d00eed71810532c89b82d1.tar.gz#/klib-5c1451c.tar.gz
Source3:        https://github.com/nanopb/nanopb/archive/refs/tags/nanopb-0.4.6.tar.gz#/nanopb-0.4.6.tar.gz
Source4:        https://github.com/Snaipe/BoxFort/archive/refs/tags/v0.1.4.tar.gz#/boxfort-0.1.4.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  libffi-devel
BuildRequires:  libffi
BuildRequires:  glibc-devel
BuildRequires:  ninja-build
BuildRequires:  nanomsg-devel
BuildRequires:  nanomsg
BuildRequires:  git
BuildRequires:  libgit2-devel
BuildRequires:  cmake
BuildRequires:  make
# bdep for nanodp
BuildRequires:  protobuf-compiler
# checkdep
# BuildRequires:  cram

%description
Criterion is a cross-platform C and C++ testing framework, which aims to bring 
cutting-edge features to the table while keeping the framework lightweight.

%prep
%setup -q -n Criterion-%{version}
# Extract and move debugbreak source

rm -rf dependencies/debugbreak
rm -rf dependencies/klib

mkdir -p dependencies/debugbreak
tar -xzf %{SOURCE1} -C dependencies/debugbreak --strip-components=1
cp -r dependencies/debugbreak subprojects
cp subprojects/packagefiles/debugbreak/meson.build subprojects/debugbreak/
# Extract and move klib source
mkdir -p dependencies/klib
tar -xzf %{SOURCE2} -C dependencies/klib --strip-components=1
cp -r dependencies/klib subprojects
cp subprojects/packagefiles/klib/meson.build subprojects/klib/

# Extract and move nanopb source
mkdir -p dependencies/nanopb
tar -xzf %{SOURCE3} -C dependencies/nanopb --strip-components=1
cp -r dependencies/nanopb subprojects

# Extract and move boxfort source
mkdir -p dependencies/boxfort
tar -xzf %{SOURCE4} -C dependencies/boxfort --strip-components=1
cp -r dependencies/boxfort subprojects



%build
%meson 
%meson_build

%install
%meson_install

%check
%meson_test

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%doc README.md
%{_libdir}/libcriterion.so*
%{_libdir}/libcriterion.a
%{_exec_prefix}/lib64/libprotobuf_nanopb_static.a
%{_libdir}/pkgconfig/criterion.pc
%{_datadir}/locale/de/LC_MESSAGES/criterion.mo
%{_datadir}/locale/fr/LC_MESSAGES/criterion.mo
%{_includedir}/criterion/

%changelog
* Mon Apr 21 2025 Riken Maharjan <rmaharjan@microsoft.com> - 2.4.2-1
- Initial package for Azure Linux 3.0