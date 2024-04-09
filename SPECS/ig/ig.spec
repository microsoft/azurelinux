Summary:        The eBPF tool and systems inspection framework for Kubernetes, containers and Linux hosts.
Name:           ig
Version:        0.25.0
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
make gadgets-unit-tests
ig_file=$(mktemp /tmp/ig-XXXXXX.out)
sudo ./bin/build/ig trace exec --host > $ig_file &
ig_pid=$!
sleep inf &
sleep_pid=$!
kill $ig_pid
kill $sleep_pid
grep -P "${sleep_pid}\s+\d+\s+sleep" $ig_file
rm $ig_file

%files
%license LICENSE
%license LICENSE-bpf.txt
%{_bindir}/ig

%changelog
* Tue Mar 14 2023 Francis Laniel <flaniel@linux.microsoft.com> - 0.25.0-1
- Original version for CBL-Mariner
- License Verified
