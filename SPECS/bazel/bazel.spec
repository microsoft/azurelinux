%define _enable_debug_package 0
%global debug_package %{nil}
%define __os_install_post %{_libdir}/rpm/brp-compress %{nil}
Summary:        Correct, reproducible, and fast builds for everyone.
Name:           bazel
Version:        2.2.0
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://bazel.io/
Source0:        https://github.com/bazelbuild/%{name}/releases/download/%{version}/%{name}-%{version}-dist.zip
Patch0:         fix-bazel-version-check.patch
BuildRequires:  libstdc++
BuildRequires:  libstdc++-devel
BuildRequires:  openjdk8
BuildRequires:  python3
BuildRequires:  unzip
BuildRequires:  zip
Requires:       openjdk8

%description
A fast, scalable, multi-language and extensible build system.

%prep
%autosetup -p1 -c -n %{name}-%{version}

%build
ln -s %{_bindir}/python3 %{_bindir}/python

EXTRA_BAZEL_ARGS="--host_javabase=@local_jdk//:jdk" ./compile.sh

%install
mkdir -p %{buildroot}/%{_bindir}
cp output/bazel %{buildroot}/%{_bindir}/bazel-real
cp ./scripts/packages/bazel.sh %{buildroot}/%{_bindir}/bazel

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/bazel
%attr(0755,root,root) %{_bindir}/bazel-real

%changelog
* Wed Jun 09 2021 Henry Li <lihl@microsoft.com> - 2.2.0-1
- Original version for CBL-Mariner