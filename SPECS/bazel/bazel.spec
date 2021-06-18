# they warn against fetching source ... but it's so convenient :-\

%define _disable_source_fetch 0

Name:           bazel
Version:        2.2.0
Release:        2%{?dist}
Summary:        Correct, reproducible, and fast builds for everyone.
License:        Apache License 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://bazel.io/
Source0:        https://github.com/bazelbuild/%{name}/releases/download/%{version}/%{name}-%{version}-dist.zip

BuildRequires:  openjdk8
BuildRequires:  zlib-devel
BuildRequires:  bash-completion-devel
BuildRequires:  findutils
BuildRequires:  libstdc++ libstdc++-devel
BuildRequires:  which
BuildRequires:  unzip
BuildRequires:  zip
BuildRequires:  python3

Requires:       openjdk8

%define bashcompdir %(pkg-config --variable=completionsdir bash-completion 2>/dev/null)
%global debug_package %{nil}
%define __os_install_post %{nil}

%description
Correct, reproducible, and fast builds for everyone.

%prep
%setup -q -c -n bazel-%{version}

%build
# thanks to @aehlig for this tip: https://github.com/bazelbuild/bazel/issues/8665#issuecomment-503575270
find . -type f -regextype posix-extended -iregex '.*(sh|txt|py|_stub|stub_.*|bazel|get_workspace_status|protobuf_support|_so)' -exec %{__sed} -i -e '1s|^#!/usr/bin/env python$|#!/usr/bin/env python3|' "{}" \;
export EXTRA_BAZEL_ARGS="${EXTRA_BAZEL_ARGS} --python_path=/usr/bin/python3"

# horrible of horribles, just to have `python` in the PATH
# https://github.com/bazelbuild/bazel/issues/8665
%{__mkdir_p} ./bin-hack
%{__ln_s} /usr/bin/python3 ./bin-hack/python
export PATH=$(pwd)/bin-hack:$PATH

%ifarch aarch64
export EXTRA_BAZEL_ARGS="${EXTRA_BAZEL_ARGS} --nokeep_state_after_build --notrack_incremental_state --nokeep_state_after_build"
%else
%endif

%ifarch s390x
# increase heap size to addess s390x build failures
export BAZEL_JAVAC_OPTS="-J-Xmx4g -J-Xms512m"
%else
%endif

# loose epoch from their release date
export SOURCE_DATE_EPOCH="$(date -d $(head -1 CHANGELOG.md | %{__grep} -Eo '\b[[:digit:]]{4}-[[:digit:]]{2}-[[:digit:]]{2}\b' ) +%s)"
export EMBED_LABEL="%{version}"

# for debugging's sake
which g++
g++ --version

export TMPDIR=%{_tmppath}
export CC=gcc
export CXX=g++
export EXTRA_BAZEL_ARGS="${EXTRA_BAZEL_ARGS} --sandbox_debug --host_javabase=@local_jdk//:jdk --verbose_failures"
env ./compile.sh
env ./output/bazel shutdown

%install
%{__mkdir_p} %{buildroot}/%{_bindir}
%{__mkdir_p} %{buildroot}/%{bashcompdir}
%{__cp} output/bazel %{buildroot}/%{_bindir}/bazel-real
%{__cp} ./scripts/packages/bazel.sh %{buildroot}/%{_bindir}/bazel

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/bazel
%attr(0755,root,root) %{_bindir}/bazel-real


%changelog
* Wed Jun 09 2021 Henry Li <lihl@microsoft.com>   2.2.0-2
- Remove distro condition checks that do not apply for CBL-Mariner

* Thu Jul 16 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com>   2.2.0-1
- Initial version Mariner
