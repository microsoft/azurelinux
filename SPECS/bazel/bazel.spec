Name:           bazel
Version:        2.2.0
Release:        1%{?dist}
Summary:        Correct, reproducible, and fast builds for everyone.
License:        Apache License 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://bazel.io/
Source0:        https://github.com/bazelbuild/%{name}/releases/download/%{version}/%{name}-%{version}-dist.zip
Patch0:         fix-bazel-version-check.patch

BuildRequires:  openjdk8
BuildRequires:  bash-completion-devel
BuildRequires:  libstdc++ 
BuildRequires:  libstdc++-devel
BuildRequires:  unzip
BuildRequires:  zip
BuildRequires:  python3

Requires:       openjdk8

%define _enable_debug_package 0
%global debug_package %{nil}
%define __os_install_post /usr/lib/rpm/brp-compress %{nil}

%description
a fast, scalable, multi-language and extensible build system.

%prep
%setup -q -c -n bazel-%{version}
%patch0 -p1

%build
ln -s /usr/bin/python3 /usr/bin/python

env EXTRA_BAZEL_ARGS="--host_javabase=@local_jdk//:jdk" bash ./compile.sh

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
- Original version for CBL-Mariner.