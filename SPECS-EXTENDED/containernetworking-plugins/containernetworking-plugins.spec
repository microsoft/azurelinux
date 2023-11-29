%global with_debug 1

%if 0%{?with_debug}
%global _find_debuginfo_dwz_opts %{nil}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%global provider github
%global provider_tld com
%global project containernetworking
%global repo plugins
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path %{provider_prefix}
%global git0 https://%{import_path}

# Used for comparing with latest upstream tag
# to decide whether to autobuild (non-rawhide only)
%define built_tag v1.1.1
%define built_tag_strip %(b=%{built_tag}; echo ${b:1})
%global gen_version %(b=%{built_tag_strip}; echo ${b/-/"~"})
%define download_url %{git0}/archive/%{built_tag}.tar.gz

Name:          %{project}-%{repo}
Version:       1.1.1
Release:       13%{?dist}
Summary:       Libraries for writing CNI plugin
License:       ASL 2.0 and BSD and MIT
Vendor:        Microsoft Corporation
Distribution:  Mariner
URL:           %{git0}
Source0: %{download_url}#/%{name}-%{version}.tar.gz
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires: golang
BuildRequires: git
BuildRequires: go-md2man
BuildRequires: go-rpm-macros
BuildRequires: systemd-devel
Requires:      systemd


Obsoletes:     %{project}-cni < 0.7.1-2
Provides:      %{project}-cni = %{version}-%{release}
Provides:      kubernetes-cni
Provides:      container-network-stack = 1
# vendored libraries
# awk '{print "Provides: bundled(golang("$1")) = "$2}' go.mod | sort | uniq | sed -e 's/-/_/g' -e '/bundled(golang())/d' -e '/bundled(golang(go\|module\|replace\|require))/d'
Provides:      bundled(golang(github.com/Microsoft/go_winio)) = v0.4.17
Provides:      bundled(golang(github.com/Microsoft/hcsshim)) = v0.8.20
Provides:      bundled(golang(github.com/alexflint/go_filemutex)) = v1.1.0
Provides:      bundled(golang(github.com/buger/jsonparser)) = v1.1.1
Provides:      bundled(golang(github.com/containerd/cgroups)) = v1.0.1
Provides:      bundled(golang(github.com/containernetworking/cni)) = v1.0.1
Provides:      bundled(golang(github.com/coreos/go_iptables)) = v0.6.0
Provides:      bundled(golang(github.com/coreos/go_systemd/v22)) = v22.3.2
Provides:      bundled(golang(github.com/d2g/dhcp4)) = v0.0.0_20170904100407_a1d1b6c41b1c
Provides:      bundled(golang(github.com/d2g/dhcp4client)) = v1.0.0
Provides:      bundled(golang(github.com/d2g/dhcp4server)) = v0.0.0_20181031114812_7d4a0a7f59a5
Provides:      bundled(golang(github.com/fsnotify/fsnotify)) = v1.4.9
Provides:      bundled(golang(github.com/godbus/dbus/v5)) = v5.0.4
Provides:      bundled(golang(github.com/gogo/protobuf)) = v1.3.2
Provides:      bundled(golang(github.com/golang/groupcache)) = v0.0.0_20200121045136_8c9f03a8e57e
Provides:      bundled(golang(github.com/mattn/go_shellwords)) = v1.0.12
Provides:      bundled(golang(github.com/networkplumbing/go_nft)) = v0.2.0
Provides:      bundled(golang(github.com/nxadm/tail)) = v1.4.8
Provides:      bundled(golang(github.com/onsi/ginkgo)) = v1.16.4
Provides:      bundled(golang(github.com/onsi/gomega)) = v1.15.0
Provides:      bundled(golang(github.com/pkg/errors)) = v0.9.1
Provides:      bundled(golang(github.com/safchain/ethtool)) = v0.0.0_20210803160452_9aa261dae9b1
Provides:      bundled(golang(github.com/sirupsen/logrus)) = v1.8.1
Provides:      bundled(golang(github.com/vishvananda/netlink)) = v1.1.1_0.20210330154013_f5de75959ad5
Provides:      bundled(golang(github.com/vishvananda/netns)) = v0.0.0_20210104183010_2eb08e3e575f

%description
The CNI (Container Network Interface) project consists of a specification
and libraries for writing plugins to configure network interfaces in Linux
containers, along with a number of supported plugins. CNI concerns itself
only with network connectivity of containers and removing allocated resources
when the container is deleted.


%prep
%autosetup -Sgit -n %{repo}-%{built_tag_strip}
rm -rf plugins/main/windows

# Use correct paths in cni-dhcp unitfiles
sed -i 's|/opt/cni/bin|\%{_prefix}/libexec/cni|' plugins/ipam/dhcp/systemd/cni-dhcp.service

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

install -dp %{buildroot}%{_unitdir}
install -p plugins/ipam/dhcp/systemd/cni-dhcp.service %{buildroot}%{_unitdir}
install -p plugins/ipam/dhcp/systemd/cni-dhcp.socket %{buildroot}%{_unitdir}

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE
%doc *.md
%dir %{_libexecdir}/cni
%{_libexecdir}/cni/*
%{_unitdir}/cni-dhcp.service
%{_unitdir}/cni-dhcp.socket

%changelog
* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.1-13
- Bump release to rebuild with go 1.20.9

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 1.1.1-12
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.1-11
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.1-10
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.1-9
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.1-8
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.1-7
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.1-6
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.1-5
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.1-4
- Bump release to rebuild with go 1.19.4

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.1.1-3
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.1.1-2
- Bump release to rebuild against Go 1.18.5

* Fri Jul 22 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.1.1-1
- Upgrade version to 1.1.1.
- Updated SPEC file for compatibility with 1.1.1 version.

* Tue Mar 01 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.9.0-3
- Fixing usage of the '%%gobuild' macro.
- License verified.

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
