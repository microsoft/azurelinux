Summary:        The eBPF tool and systems inspection framework for Kubernetes, containers and Linux hosts.
Name:           ig
Version:        0.26.0
Release:        1%{?dist}
License:        Apache 2.0 and GPL 2.0 for eBPF code
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Tools/Container
URL:            https://github.com/inspektor-gadget/inspektor-gadget
Source0:        https://github.com/inspektor-gadget/inspektor-gadget/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-govendor-v1.tar.gz
BuildRequires:  golang


%description
Inspektor Gadget is a collection of tools (or gadgets) to debug and inspect Kubernetes resources and applications. It manages the packaging, deployment and execution of eBPF programs in a Kubernetes cluster, including many based on BCC tools, as well as some developed specifically for use in Inspektor Gadget. It automatically maps low-level kernel primitives to high-level Kubernetes resources, making it easier and quicker to find the relevant information.

This package contains ig, the local CLI flavor of Inspektor Gadget.

%prep
%autosetup -n inspektor-gadget-%{version}
%setup -q -n inspektor-gadget-%{version} -T -D -a 1

%build
CGO_ENABLED=0 go build \
		-ldflags "-X github.com/inspektor-gadget/inspektor-gadget/cmd/common.version=v%{version} \
			-X github.com/inspektor-gadget/inspektor-gadget/cmd/common/image.builderImage=ghcr.io/inspektor-gadget/ebpf-builder:v%{version} \
			-extldflags '-static'" \
		-tags "netgo" \
		-o ./bin/build/ig ./cmd/ig

%install
mkdir -p "%{buildroot}/%{_bindir}"
install -D -m0755 bin/build/ig %{buildroot}/%{_bindir}

%check
set -e
set -o pipefail

# Inspektor Gadget provides unit tests but they rely on several components which
# are not present in the chroot used to build and test the package, among
# others:
# * runc: https://github.com/inspektor-gadget/inspektor-gadget/blob/3c8d1455525b/pkg/container-hook/tracer.go#L302
# * dockerd: https://github.com/inspektor-gadget/inspektor-gadget/blob/3c8d1455525b/pkg/container-utils/testutils/docker.go#L67
# Even if we recreate a proper testing environment, we will still have problems
# as, for example, the path tested will be inside the chroot while ig reports
# the full path from host point of view.
# For all these reasons, we will skip the unit tests and rather run a small
# integration test.
# Moreover, Inspektor Gadget CI covers Azure Linux extensively:
# https://github.com/inspektor-gadget/inspektor-gadget/pull/1186/commits/066bf618d158
if [ -d /sys/kernel/debug/tracing ]; then
	sleep inf &
	sleep_pid=$!
	./bin/build/ig snapshot process --host | grep -qP "sleep\s+${sleep_pid}"
	kill $sleep_pid
else
	echo "Skipping ig check as prerequisites are not satisfied in the chroot"
fi

%files
%license LICENSE
%license LICENSE-bpf.txt
%{_bindir}/ig

%changelog
* Tue Mar 12 2024 Francis Laniel <flaniel@linux.microsoft.com> - 0.26.0-1
- Bump to version 0.26.0

* Tue Mar 14 2023 Francis Laniel <flaniel@linux.microsoft.com> - 0.25.0-2
- Fix %check.

* Tue Feb 14 2023 Francis Laniel <flaniel@linux.microsoft.com> - 0.25.0-1
- Original version for Azure Linux
- License Verified
