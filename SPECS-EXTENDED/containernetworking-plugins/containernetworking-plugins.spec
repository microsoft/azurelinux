Vendor:         Microsoft Corporation
Distribution:   Mariner
%global with_devel 1
%global with_bundled 1
%global with_check 0
%global with_unit_test 1


%global with_debug 1




%if 0%{?with_debug}
%global _find_debuginfo_dwz_opts %{nil}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%if ! 0%{?gobuild:1}
%define gobuild(o:) GO111MODULE=off go build -buildmode pie -compiler gc -tags="rpm_crashtraceback ${BUILDTAGS:-}" -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -extldflags '-Wl,-z,relro -Wl,-z,now -specs=/usr/lib/rpm/mariner/default-hardened-ld '" -a -v -x %{?**};
%endif

%global provider github
%global provider_tld com
%global project containernetworking
%global repo plugins
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path %{provider_prefix}
%global git0 https://%{import_path}
%global commit0 f5c3d1b1bab6ee72a32702c22ebb0f008580ef2d
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

# Used for comparing with latest upstream tag
# to decide whether to autobuild (non-rawhide only)
%define built_tag v0.9.0
%define built_tag_strip %(b=%{built_tag}; echo ${b:1})
%define download_url %{git0}/archive/%{built_tag}.tar.gz

Name: %{project}-%{repo}
Version: 0.9.0
Release: 2%{?dist}
Summary: Libraries for writing CNI plugin
License: ASL 2.0
URL: %{git0}
Source0: %{download_url}#/%{name}-%{version}.tar.gz
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires: golang
BuildRequires: git
BuildRequires: go-md2man

%if ! 0%{?with_bundled}
BuildRequires: go-bindata
BuildRequires: golang(github.com/vishvananda/netlink)
BuildRequires: golang(github.com/coreos/go-systemd/activation)
BuildRequires: golang(github.com/d2g/dhcp4)
BuildRequires: golang(github.com/d2g/dhcp4client)
BuildRequires: golang(github.com/vishvananda/netlink)
BuildRequires: golang(golang.org/x/sys/unix)
BuildRequires: golang(github.com/coreos/go-iptables/iptables)
%endif

Obsoletes: %{project}-cni < 0.7.1-2
Provides: %{project}-cni = %{version}-%{release}
Provides: kubernetes-cni

%description
The CNI (Container Network Interface) project consists of a specification
and libraries for writing plugins to configure network interfaces in Linux
containers, along with a number of supported plugins. CNI concerns itself
only with network connectivity of containers and removing allocated resources
when the container is deleted.

%if 0%{?with_devel}
%package devel
Summary: %{summary}
BuildArch: noarch

%if 0%{?with_check} && ! 0%{?with_bundled}
BuildRequires: golang(github.com/coreos/go-iptables/iptables)
BuildRequires: golang(github.com/vishvananda/netlink)
BuildRequires: golang(golang.org/x/sys/unix)
%endif

Requires: golang(github.com/coreos/go-iptables/iptables)
Requires: golang(github.com/vishvananda/netlink)
Requires: golang(golang.org/x/sys/unix)

Provides: golang(%{import_path}/libcni) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/invoke) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/invoke/fakes) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/ip) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/ipam) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/ns) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/skel) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/testutils) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/types) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/types/020) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/types/current) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/utils) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/utils/hwaddr) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/utils/sysctl) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/version) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/version/legacy_examples) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/version/testhelpers) = %{version}-%{release}
Provides: golang(%{import_path}/plugins/ipam/host-local/backend) = %{version}-%{release}
Provides: golang(%{import_path}/plugins/ipam/host-local/backend/allocator) = %{version}-%{release}
Provides: golang(%{import_path}/plugins/ipam/host-local/backend/disk) = %{version}-%{release}
Provides: golang(%{import_path}/plugins/ipam/host-local/backend/testing) = %{version}-%{release}
Provides: golang(%{import_path}/plugins/test/noop/debug) = %{version}-%{release}

%description devel
This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%package unit-test-devel
Summary: Unit tests for %{name} package
%if 0%{?with_check}
%endif

Requires: %{name}-devel = %{version}-%{release}

%if 0%{?with_check} && ! 0%{?with_bundled}
BuildRequires: golang(github.com/d2g/dhcp4)
BuildRequires: golang(github.com/onsi/ginkgo)
BuildRequires: golang(github.com/onsi/ginkgo/config)
BuildRequires: golang(github.com/onsi/ginkgo/extensions/table)
BuildRequires: golang(github.com/onsi/gomega)
BuildRequires: golang(github.com/onsi/gomega/gbytes)
BuildRequires: golang(github.com/onsi/gomega/gexec)
BuildRequires: golang(github.com/vishvananda/netlink/nl)
%endif

Requires: golang(github.com/d2g/dhcp4)
Requires: golang(github.com/onsi/ginkgo)
Requires: golang(github.com/onsi/ginkgo/config)
Requires: golang(github.com/onsi/ginkgo/extensions/table)
Requires: golang(github.com/onsi/gomega)
Requires: golang(github.com/onsi/gomega/gbytes)
Requires: golang(github.com/onsi/gomega/gexec)
Requires: golang(github.com/vishvananda/netlink/nl)

%description unit-test-devel
This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%autosetup -Sgit -n %{repo}-%{built_tag_strip}
rm -rf plugins/main/windows

%build
export ORG_PATH="%{provider}.%{provider_tld}/%{project}"
export REPO_PATH="$ORG_PATH/%{repo}"

if [ ! -h gopath/src/${REPO_PATH} ]; then
        mkdir -p gopath/src/${ORG_PATH}
        ln -s ../../../.. gopath/src/${REPO_PATH} || exit 255
fi

export GOPATH=$(pwd)/gopath
mkdir -p $(pwd)/bin

echo "Building plugins"
export PLUGINS="plugins/meta/* plugins/main/* plugins/ipam/* plugins/sample"
for d in $PLUGINS; do
        if [ -d "$d" ]; then
                plugin="$(basename "$d")"
                echo "  $plugin"
                %gobuild -o "${PWD}/bin/$plugin" "$@" "$REPO_PATH"/$d
        fi
done

%install
install -d -p %{buildroot}%{_libexecdir}/cni/
install -p -m 0755 bin/* %{buildroot}/%{_libexecdir}/cni

# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . \( -iname "*.go" -or -iname "*.s" \) \! -iname "*_test.go" | grep -v "vendor") ; do
    dirprefix=$(dirname $file)
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$dirprefix
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list

    while [ "$dirprefix" != "." ]; do
        echo "%%dir %%{gopath}/src/%%{import_path}/$dirprefix" >> devel.file-list
        dirprefix=$(dirname $dirprefix)
    done
done
%endif

# testing files for this project
%if 0%{?with_unit_test} && 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test-devel.file-list
for file in $(find . -iname "*_test.go" | grep -v "vendor") ; do
    dirprefix=$(dirname $file)
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$dirprefix
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test-devel.file-list

    while [ "$dirprefix" != "." ]; do
        echo "%%dir %%{gopath}/src/%%{import_path}/$dirprefix" >> devel.file-list
        dirprefix=$(dirname $dirprefix)
    done
done
%endif

%if 0%{?with_devel}
sort -u -o devel.file-list devel.file-list
%endif

%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
%if ! 0%{?with_bundled}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%else
# Since we aren't packaging up the vendor directory we need to link
# back to it somehow. Hack it up so that we can add the vendor
# directory from BUILD dir as a gopath to be searched when executing
# tests from the BUILDROOT dir.
ln -s ./ ./vendor/src # ./vendor/src -> ./vendor

export GOPATH=%{buildroot}/%{gopath}:$(pwd)/vendor:%{gopath}
%endif

%if ! 0%{?gotest:1}
%global gotest go test
%endif

%gotest %{import_path}/libcni
%gotest %{import_path}/pkg/invoke
%gotest %{import_path}/pkg/ip
%gotest %{import_path}/pkg/ipam
%gotest %{import_path}/pkg/ns
%gotest %{import_path}/pkg/skel
%gotest %{import_path}/pkg/types
%gotest %{import_path}/pkg/types/020
%gotest %{import_path}/pkg/types/current
%gotest %{import_path}/pkg/utils
%gotest %{import_path}/pkg/utils/hwaddr
%gotest %{import_path}/pkg/version
%gotest %{import_path}/pkg/version/legacy_examples
%gotest %{import_path}/pkg/version/testhelpers
%gotest %{import_path}/plugins/ipam/dhcp
%gotest %{import_path}/plugins/ipam/host-local
%gotest %{import_path}/plugins/ipam/host-local/backend/allocator
%gotest %{import_path}/plugins/main/bridge
%gotest %{import_path}/plugins/main/ipvlan
%gotest %{import_path}/plugins/main/loopback
%gotest %{import_path}/plugins/main/macvlan
%gotest %{import_path}/plugins/main/ptp
%gotest %{import_path}/plugins/meta/flannel
%gotest %{import_path}/plugins/test/noop
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE
%doc *.md
%dir %{_libexecdir}/cni
%{_libexecdir}/cni/*

%if 0%{?with_devel}
%files devel -f devel.file-list
%license LICENSE
%doc *.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%files unit-test-devel -f unit-test-devel.file-list
%license LICENSE
%doc *.md
%endif

%changelog
* Fri Apr 30 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.9.0-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Making binaries paths compatible with CBL-Mariner's paths.

* Wed Dec  9 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.9.0-1
- autobuilt v0.9.0

* Wed Aug 26 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.8.7-1
- autobuilt v0.8.7

* Wed May 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.8.6-1
- autobuilt v0.8.6

* Thu Jan 30 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.8.5-1.1.gitf5c3d1b
- bump to v0.8.5
- autobuilt f5c3d1b

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-0.5.dev.git291ab6c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.8.2-0.4.dev.git291ab6c
- autobuilt 291ab6c

* Wed Sep 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.8.2-0.3.dev.git23d5525
- autobuilt 23d5525

* Wed Sep 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.8.2-0.2.dev.git4bb2881
- autobuilt 4bb2881

* Wed Aug 28 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.8.2-0.1.dev.git7e68430
- bump to 0.8.2
- autobuilt 7e68430

* Wed Aug 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.8.1-7.1.dev.git485be65
- autobuilt 485be65

* Wed Aug 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.8.1-6.1.dev.gitc9e1c0c
- autobuilt c9e1c0c

* Mon Aug 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.8.1-5.1.dev.git2d6d4b2
- autobuilt 2d6d4b2

* Wed Aug 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.8.1-4.1.dev.gitccd683e
- autobuilt ccd683e

* Wed Jul 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.8.1-3.1.dev.gitded2f17
- autobuilt ded2f17

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.8.1-2.1.dev.git7ba2bcf
- autobuilt 7ba2bcf

* Wed Jul 10 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.8.1-1.1.dev.git966bbcb
- built 966bbcb
- hook up to autobuild

* Fri Jun 07 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.8.1-1
- bump to v0.8.1

* Fri May 31 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.7.5-1
- Resolves: #1715758 - CVE-2019-9946
- bump to v0.7.5
- BR: git
- remove ExcludeArch: ppc64

* Wed Feb 27 2019 Jason Brooks <jbrooks@redhat.com> - 0.7.4-2
- add Provides kubernetes-cni for compatibility with upstream kubelet package

* Wed Feb 13 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.7.4-1
- bump to v0.7.4

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug 30 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.7.3-2
- correct upgrade path from older -cni package
- for whatever reason, "<" works but "<=" doesn't for obsoletion

* Mon Aug 20 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.7.3-1
- Resolves: #1613909 - rename package to containernetworking-plugins
- Obsoletes containernetworking-cni
- bump to v0.7.3

* Wed Jul 18 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.7.1-1
- Resolves: #1543200 - bump to v0.7.1
- remove patch in dist-git from 0.6.0-2 (already upstreamed)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr  2 2018 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.0-4
- Own the libexec cni directory

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Dan Williams <dcbw@redhat.com> - 0.6.0-2
- skip settling IPv4 addresses

* Mon Jan 08 2018 Frantisek Kluknavsky <fkluknav@redhat.com> - 0.6.0-1
- rebased to 7480240de9749f9a0a5c8614b17f1f03e0c06ab9

* Fri Oct 13 2017 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.2-7
- do not install to /opt (against Fedora Guidelines)

* Thu Aug 24 2017 Jan Chaloupka <jchaloup@redhat.com> - 0.5.2-6
- Enable devel subpackage

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 13 2017 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.2-3
- excludearch: ppc64 as it's not in goarches anymore
- re-enable s390x

* Fri Jun 30 2017 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.2-2
- upstream moved to github.com/containernetworking/plugins
- built commit dcf7368
- provides: containernetworking-plugins
- use vendored deps because they're a lot less of a PITA
- excludearch: s390x for now (rhbz#1466865)

* Mon Jun 12 2017 Timothy St. Clair <tstclair@heptio.com> - 0.5.2-1
- Update to 0.5.2 
- Softlink to default /opt/cni/bin directories

* Sun May 07 2017 Timothy St. Clair <tstclair@heptio.com> - 0.5.1-1
- Initial package

