%define _enable_debug_package 0
%global debug_package %{nil}
%define __os_install_post %{_libdir}/rpm/brp-compress %{nil}
Summary:        Correct, reproducible, and fast builds for everyone.
Name:           bazel
Version:        7.0.0
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://bazel.io/
Source0:        https://github.com/bazelbuild/%{name}/releases/download/%{version}/%{name}-%{version}-dist.zip
Patch0:         fix-bazel-version-check.patch
BuildRequires:  build-essential
BuildRequires:  libstdc++
BuildRequires:  libstdc++-devel
BuildRequires:  msopenjdk-11
BuildRequires:  python3
BuildRequires:  unzip
BuildRequires:  zip
Requires:       msopenjdk-11

%description
A fast, scalable, multi-language and extensible build system.

%prep
%autosetup -p1 -c -n %{name}-%{version}
# Modify source to "#include <limits>" which resolves gcc11 errors:
# graphcycles.cc:451:26: error: 'numeric_limits' is not a member of 'std'"
sed -i 's/#include <string.h>/#include <string.h>\n#include <limits>/g' third_party/ijar/common.h
sed -i 's/<limits.h>/<limits>\n#include <climits>/g' src/main/cpp/util/numbers.cc
# abseil-cpp source contains graphcycles.cc in "derived/distdir/df3ea785d8c30a9503321a3d35ee7d35808f190d.tar.gz"
# since graphcycles.cc fails to compile on gcc11 and already includes <utility>, force inclusion of <limits>
sed -i 's/#include <utility>/#include <utility>\n#include <limits>/g' /usr/include/c++/11.2.0/array

%build
export JAVA_HOME=$(find %{_libdir}/jvm -name "msopenjdk*")
ln -s %{_bindir}/python3 %{_bindir}/python

EXTRA_BAZEL_ARGS="--tool_java_runtime_version=local_jdk --remote_download_minimal" ./compile.sh

%install
mkdir -p %{buildroot}/%{_bindir}
cp output/bazel %{buildroot}/%{_bindir}/bazel-real
cp ./scripts/packages/bazel.sh %{buildroot}/%{_bindir}/bazel

%files
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/bazel
%attr(0755,root,root) %{_bindir}/bazel-real

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 7.0.0-1
- Auto-upgrade to 7.0.0 - Azure Linux 3.0 - package upgrades

* Fri Dec 09 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.3.2-1
- Auto-upgrade to 5.3.2 - CVE-2022-3474

* Fri Dec 02 2022 Riken Maharjan <rmaharjan@microsoft.com> - 5.3.0-1
- Upgrade to 5.3.0

* Mon Oct 31 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.2.3-1
- Upgrade to 4.2.3

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.2.1-2
- Removing the explicit %%clean stage.

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