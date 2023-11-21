%global debug_package %{nil}
%ifarch x86_64
%define archname amd64
%endif
%ifarch aarch64
%define archname arm64
%endif
%define host_components 'kubelet kubectl kubeadm'
%define container_image_components 'kube-proxy kube-apiserver kube-controller-manager kube-scheduler'
Summary:        Microsoft Kubernetes
Name:           kubernetes
Version:        1.28.4
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Microsoft Kubernetes
URL:            https://kubernetes.io/
Source0:        https://dl.k8s.io/v%{version}/kubernetes-src.tar.gz#/%{name}-v%{version}.tar.gz
Source1:        kubelet.service
BuildRequires:  flex-devel
BuildRequires:  glibc-static >= 2.35-6%{?dist}
BuildRequires:  golang
BuildRequires:  rsync
BuildRequires:  systemd-devel
BuildRequires:  which
Requires:       cni
Requires:       cri-tools
Requires:       ebtables
Requires:       ethtool
Requires:       iproute
Requires:       iptables
Requires:       moby-containerd
Requires:       socat
Requires:       util-linux
Requires(postun): %{_sbindir}/groupdel
Requires(postun): %{_sbindir}/userdel
Requires(pre):  %{_sbindir}/groupadd
Requires(pre):  %{_sbindir}/useradd

%description
Microsoft Kubernetes %{version}.

%package        client
Summary:        Client utilities

%description    client
Client utilities for Microsoft Kubernetes %{version}.

%package        kubeadm
Summary:        Bootstrap utilities
Requires:       %{name} = %{version}-%{release}
Requires:       moby-containerd

%description    kubeadm
Bootstrap utilities for Microsoft Kubernetes %{version}.

%package        kube-proxy
Summary:        Kubernetes proxy
Requires:       ebtables-legacy
Requires:       ethtool
Requires:       iproute
Requires:       iptables

%description    kube-proxy
Network proxy for Microsoft Kubernetes %{version}.

%package        kube-apiserver
Summary:        Kubernetes API server

%description    kube-apiserver
API server for Microsoft Kubernetes %{version}.

%package        kube-controller-manager
Summary:        Kubernetes controller manager

%description    kube-controller-manager
Controller manager for Microsoft Kubernetes %{version}.

%package        kube-scheduler
Summary:        Kubernetes scheduler

%description    kube-scheduler
Scheduler for Microsoft Kubernetes %{version}.

%package        pause
Summary:        Kubernetes pause

%description    pause
Pause component for Microsoft Kubernetes %{version}.

%prep
%setup -q -c -n %{name}

%build
# set version information using KUBE_GIT_VERSION
# (see k8s code: hack/lib/version.sh for more detail)
export KUBE_GIT_TREE_STATE=archive
export KUBE_GIT_VERSION=v%{version}

# build host and container image related components
echo "+++ build kubernetes components"

mkdir -p %{_builddir}/%{name}/node/bin

components_to_build=%{host_components}
for component in ${components_to_build}; do
  echo "+++ host - building ${component}"
  make WHAT=cmd/${component}
  cp -f _output/local/bin/linux/%{archname}/${component} %{_builddir}/%{name}/node/bin
done

components_to_build=%{container_image_components}
for component in ${components_to_build}; do
  echo "+++ container image - building ${component}"
  make WHAT=cmd/${component}
  cp -f _output/local/bin/linux/%{archname}/${component} %{_builddir}/%{name}/node/bin
done

# build pause
pushd build/pause/linux
gcc -Os -Wall -Werror -static -o %{_builddir}/%{name}/node/bin/pause pause.c
strip %{_builddir}/%{name}/node/bin/pause
popd

%check
# patch test script so it supports golang 1.15 which is now used to build kubernetes
cd %{_builddir}/%{name}/src/hack/make-rules
patch -p1 test.sh < %{SOURCE2}

# perform unit tests
# Note:
#   - components are not unit tested the same way
#   - not all components have unit
cd %{_builddir}/%{name}/src
components_to_test=$(ls -1 %{_builddir}/%{name}/node/bin)

for component in ${components_to_test}; do
  if [[ ${component} == "kubelet" || ${component} == "kubectl" ]]; then
    echo "+++ unit test pkg ${component}"
    make test WHAT=./pkg/${component}
  elif [[ ${component} == "kube-proxy" ]]; then
    echo "+++ unit test pkg ${component}"
    make test WHAT=./pkg/proxy
  elif [[ ${component} == "kube-scheduler" ]]; then
    echo "+++ unit test pkg ${component}"
    make test WHAT=./pkg/scheduler
  elif [[ ${component} == "kube-apiserver" ]]; then
    echo "+++ unit test pkg ${component}"
    make test WHAT=./pkg/kubeapiserver
  elif [[ ${component} == "kube-controller-manager" ]]; then
    echo "+++ unit test pkg ${component}"
    make test WHAT=./pkg/controller
  else
    echo "+++ no unit test available for ${component}"
  fi
done

%install
# install binaries
install -m 755 -d %{buildroot}%{_bindir}
cd %{_builddir}
binaries=%{host_components}
for bin in ${binaries}; do
  echo "+++ INSTALLING ${bin}"
  install -p -m 755 -t %{buildroot}%{_bindir} %{name}/node/bin/${bin}
done

install -m 755 -d %{buildroot}%{_exec_prefix}/local/bin
binaries=%{container_image_components}
for bin in ${binaries}; do
  echo "+++ INSTALLING ${bin}"
  install -p -m 755 -t %{buildroot}%{_exec_prefix}/local/bin %{name}/node/bin/${bin}
done

install -p -m 755 -t %{buildroot}%{_exec_prefix}/local/bin %{name}/node/bin/pause

# install service files
install -d -m 0755 %{buildroot}/%{_libdir}/systemd/system
install -p -m 644 -t %{buildroot}%{_libdir}/systemd/system %{SOURCE1}

# install config files
install -d -m 0755 %{buildroot}%{_sysconfdir}/kubernetes
install -d -m 644 %{buildroot}%{_sysconfdir}/kubernetes/manifests

# install the place the kubelet defaults to put volumes
install -dm755 %{buildroot}%{_sharedstatedir}/kubelet
install -dm755 %{buildroot}%{_var}/run/kubernetes

install -d -m 0755 %{buildroot}/%{_libdir}/tmpfiles.d
cat << EOF >> %{buildroot}/%{_libdir}/tmpfiles.d/kubernetes.conf
d %{_var}/run/kubernetes 0755 kube kube -
EOF

%pre
if [ $1 -eq 1 ]; then
    # Initial installation.
    getent group kube >/dev/null || groupadd -r kube
    getent passwd kube >/dev/null || useradd -r -g kube -d / -s /sbin/nologin \
            -c "Kubernetes user" kube
fi

%post
chown -R kube:kube %{_sharedstatedir}/kubelet
chown -R kube:kube %{_var}/run/kubernetes
systemctl daemon-reload

%post kubeadm
systemctl daemon-reload
systemctl stop kubelet
systemctl enable kubelet

%postun
if [ $1 -eq 0 ]; then
    # Package deletion
    userdel kube
    groupdel kube
    systemctl daemon-reload
fi

%files
%defattr(-,root,root)
%license LICENSES
%{_bindir}/kubelet
%{_libdir}/tmpfiles.d/kubernetes.conf
%dir %{_sysconfdir}/kubernetes
%dir %{_sysconfdir}/kubernetes/manifests
%dir %{_sharedstatedir}/kubelet
%dir %{_var}/run/kubernetes
%{_libdir}/systemd/system/kubelet.service

%files client
%defattr(-,root,root)
%{_bindir}/kubectl

%files kubeadm
%defattr(-,root,root)
%{_bindir}/kubeadm

%files kube-proxy
%defattr(-,root,root)
%license LICENSES
%{_exec_prefix}/local/bin/kube-proxy

%files kube-apiserver
%defattr(-,root,root)
%license LICENSES
%{_exec_prefix}/local/bin/kube-apiserver

%files kube-controller-manager
%defattr(-,root,root)
%license LICENSES
%{_exec_prefix}/local/bin/kube-controller-manager

%files kube-scheduler
%defattr(-,root,root)
%license LICENSES
%{_exec_prefix}/local/bin/kube-scheduler

%files pause
%defattr(-,root,root)
%license LICENSES
%{_exec_prefix}/local/bin/pause

%changelog
* Tue Nov 21 2023 Bala <bkannan@microsoft.com> - 1.28.3-1
- Upgrade to 1.28.4 to fix CVE-2023-5528

* Fri Nov 10 2023 Muhammad Falak <mwani@microsoft.com> - 1.28.3-2
- Fix version subcommand for components

* Mon Oct 23 2023 Nicolas Guibourge <nicolasg@microsoft.com> - 1.28.3-1
- Upgrade to 1.28.3 to address CVE-2023-44487 and CVE-2023-39325.

* Thu Oct 12 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.28.2-3
- Bump release to rebuild with updated version of Go.

* Fri Oct 06 2023 Henry Beberman <henry.beberman@microsoft.com> - 1.28.2-2
- Bump release to rebuild against glibc 2.35-6

* Wdd Sep 20 2023 Nicolas Guibourge <nicolasg@microsoft.com> - 1.28.2-1
- Upgrade to 1.28.2
- License verified.

* Wed Jul 12 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.26.3-4
- Force re-build by bumping release number

* Tue Jun 20 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.26.3-3
- Force re-build by bumping release number

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.26.3-2
- Force re-build by bumping release number

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.26.3-1
- Auto-upgrade to 1.26.3

* Tue Feb 21 2023 Nicolas Guibourge <nicolasg@microsoft.com> - 1.26.1-2
- Remove golang version in BR and replace mobly-cli requires with moby-containerd

* Wed Feb 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.26.1-1
- Auto-upgrade to 1.26.1

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.23.5-6
- Increment release to force republishing using golang 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.23.5-5
- Increment release to force republishing using golang 1.18.8

* Wed Oct 26 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 1.23.5-4
- add glibc-static build requires and requires moby-containerd instead of moby-engine.

* Thu Aug 25 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.23.5-3
- Increment release to force republishing using golang 1.18.5

* Fri Jun 24 2022 Mandeep Plaha <mandeepplaha@microsoft.com> - 1.23.5-2
- Remove kubernetes dependency for kubernetes client.

* Wed Apr 20 2022 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.23.5-1
- Update to version "1.23.5-hotfix.20220331".

* Wed Apr 20 2022 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.23.3-1
- Update to version "1.23.3-hotfix.20220401".

* Thu Mar 31 2022 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.22.6-4
- Update to version "1.22.6-hotfix.20220330".

* Wed Mar 23 2022 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.22.6-3
- Update to version "1.22.6-hotfix.20220310".

* Tue Mar 15 2022 Muhammad Falak <mwani@microsoft.com> - 1.22.6-2
- Bump release to force rebuild with golang 1.16.15

* Tue Feb 22 2022 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.22.6-1
- Update to version "1.22.6-hotfix.20220130".

* Tue Feb 22 2022 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.22.4-4
- Update to version "1.22.4-hotfix.20220201".

* Fri Feb 18 2022 Thomas Crain <thcrain@microsoft.com> - 1.22.4-3
- Increment release to force republishing using golang 1.16.14.

* Wed Jan 19 2022 Henry Li <lihl@microsoft.com> - 1.22.4-2
- Increment release to force republishing using golang 1.16.12.

* Wed Dec 29 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.22.4-1
- Update to version "1.22.4".

* Wed Dec 29 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.22.2-1
- Update to version "1.22.2-hotfix.20211115".

* Wed Dec 29 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.21.7-1
- Update to version "1.21.7".

* Wed Nov 17 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.21.2-7
- Update to version "1.21.2-hotfix.20211115".

* Tue Nov 02 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.21.2-6
- Update to version "1.21.2-hotfix.20211101".

* Mon Oct 25 2021 Nicolas Guibourge <nicolasg@microsoft.com> 1.21.2-5
- Add CVE-2021-25741.nopatch

* Mon Oct 25 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.21.2-4
- Update to version "1.21.2-hotfix.20211022".

* Wed Oct 13 2021 Andrew Phelps <anphel@microsoft.com> - 1.21.2-3
- Replace incorrect %%{_lib} usage with %%{_libdir}

* Mon Oct 11 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.21.2-2
- Update to version "1.21.2-hotfix.20211005".

* Thu Sep 02 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.21.2-1
- Update to version "1.21.2-hotfix.20210830".

* Thu Sep 02 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.21.1-1
- Update to version "1.21.1-hotfix.20210827".

* Thu Sep 02 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.20.9-1
- Update to version "1.20.9-hotfix.20210830".

* Thu Sep 02 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.20.7-3
- Update to version "1.20.7-hotfix.20210816".

* Wed Jul 07 2021 Nicolas Guibourge <nicolasg@microsoft.com> 1.20.7-2
- Move binary to /usr/local/bin (container only).

* Fri Jun 18 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.20.7-1
- Update to version "1.20.7-hotfix.20210603".

* Tue Jun 01 2021 Nicolas Guibourge <nicolasg@microsoft.com> 1.20.2-6
- Move spec to new git repository and change source tarball.

* Wed May 26 2021 Nicolas Guibourge <nicolasg@microsoft.com> 1.20.2-5
- Update to version  "1.20.2-hotfix.20210525".

* Mon May 17 2021 Nicolas Guibourge <nicolasg@microsoft.com> 1.20.2-4
- Manually set version variables.

* Thu May 13 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.20.2-3
- Update to version  "1.20.2-hotfix.20210511".

* Mon May 03 2021 Nicolas Guibourge <nicolasg@microsoft.com> 1.20.2-2
- Increment release to force republishing using golang 1.15.11.

* Thu Apr 29 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.20.2-2
- Update to version  "1.20.2-hotfix.20210428".

* Thu Apr 22 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.20.2-1
- Update to version  "1.20.2-hotfix.20210310".
- Adjust "pause" building steps with the new sources layout.

* Thu Apr 22 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.19.9-1
- Update to version  "1.19.9-hotfix.20210322".

* Thu Mar 18 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.19.7-1
- Update to version  "1.19.7-hotfix.20210310".

* Thu Mar 18 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.19.6-2
- Update to version  "1.19.6-hotfix.20210310".

* Wed Jan 20 2021 Nicolas Guibourge <nicolasg@microsoft.com> - 1.19.6-1
- Move to version 1.19.6

* Fri Jan 15 2021 Nicolas Guibourge <nicolasg@microsoft.com> - 1.19.1-5
- Packages for container images

* Tue Jan 05 2021 Nicolas Guibourge <nicolasg@microsoft.com> - 1.19.1-4
- CVE-2020-8563

* Mon Jan 04 2021 Nicolas Guibourge <nicolasg@microsoft.com> - 1.19.1-3
- CVE-2020-8564, CVE-2020-8565, CVE-2020-8566

* Thu Dec 17 2020 Nicolas Guibourge <nicolasg@microsoft.com> - 1.19.1-2
- Rename spec file

* Wed Dec 02 2020 Nicolas Guibourge <nicolasg@microsoft.com> - 1.19.1-1
- Original version for CBL-Mariner


