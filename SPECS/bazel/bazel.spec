%define _enable_debug_package 0
%global debug_package %{nil}
%define __os_install_post %{_libdir}/rpm/brp-compress %{nil}
Summary:        Correct, reproducible, and fast builds for everyone.
Name:           bazel
Version:        4.2.1
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://bazel.io/
Source0:        https://github.com/bazelbuild/%{name}/releases/download/%{version}/%{name}-%{version}-dist.zip
Patch0:         fix-bazel-version-check.patch
BuildRequires:  libstdc++
BuildRequires:  libstdc++-devel
#BuildRequires:  openjdk8
BuildRequires:  openjdk-11-hotspot
BuildRequires:  python3
BuildRequires:  unzip
BuildRequires:  zip
#Requires:       openjdk8
Requires:       openjdk-11-hotspot

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
* Mon Nov 29 2021 Andrew Phelps <anphel@microsoft.com> - 4.2.1-1
- Update to version 4.2.1

* Tue Sep 14 2021 Henry Li <lihl@microsoft.com> - 4.1.0-1
- Upgrade to version 4.1.0
- Remove jni-build-error patch

* Tue Jul 13 2021 Henry Li <lihl@microsoft.com> - 2.2.0-2
- Apply patch to resolve jni build error on aarch64

* Wed Jun 09 2021 Henry Li <lihl@microsoft.com> - 2.2.0-1
- Original version for CBL-Mariner
- License Verified