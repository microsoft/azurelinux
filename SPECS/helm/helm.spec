%global debug_package %{nil}

Name:          helm
Version:       3.4.1
Release:       2%{?dist}
Summary:       The Kubernetes Package Manager
Group:         Applications/Networking
License:       Apache 2.0
Vendor:        Microsoft Corporation
Distribution:  Mariner
Url:           https://github.com/helm/helm
#Source0:      https://github.com/%{name}/%{name}/archive/v%{version}.tar.gz
Source0:       helm-%{version}.tar.gz
Source1:       %{name}-%{version}-gocache.tar.gz

BuildRequires: golang >= 1.15.5
BuildRequires: glide
BuildRequires: git
BuildRequires: ca-certificates

%description
Helm is a tool that streamlines installing and managing Kubernetes applications. Think of it like apt/yum/homebrew for Kubernetes.

%prep
%setup -q -n helm-%{version}

%build
# print diagnostics
go version
go env

export GOPATH=$PWD

# must comment from pushd to popd to create gocache.tar.gz
pushd $GOPATH
 export GOOS=linux
 set GO111MODULE to off to make sure that go will get its modules from local cache
 # which is under GOPATH folder
 export GO111MODULE=off
 export GOARCH=amd64
 tar -xvf %{SOURCE1} 
popd
# end must comment

mkdir -p src/k8s.io/helm
shopt -s extglob dotglob

mv $(ls | grep -v "^src$") src/k8s.io/helm

shopt -u extglob dotglob
pushd src/k8s.io/helm/
make GIT_TAG=v%{version} GIT_DIRTY=clean
bin/helm completion bash > helm-bash-completion
bin/helm completion zsh > helm-zsh-completion
popd
pushd $GOPATH
# create gocache.tar.gz 
# must comment section indicated above
# tar -cvp -f gocache.tar.gz pkg src bin
popd

%install
install -d -m 755 $RPM_BUILD_ROOT%{_bindir}
install -m 755 src/k8s.io/helm/bin/helm $RPM_BUILD_ROOT%{_bindir}
install -Dm 644 src/k8s.io/helm/helm-zsh-completion $RPM_BUILD_ROOT%{_datadir}/zsh/site-functions/_%{name}
install -Dm 644 src/k8s.io/helm/helm-bash-completion $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d/%{name}
# install -m 755 gocache.tar.gz $RPM_BUILD_ROOT%{_bindir}

%files
%{_bindir}/helm
%{_datadir}/zsh/site-functions/_%{name}
%{_sysconfdir}/bash_completion.d/%{name}
# %{_bindir}/gocache.tar.gz

%changelog
* Wed Nov 25 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> 3.4.1-1
- Update helm version 3

* Tue Jun 02 2020 Paul Monson <paulmon@microsoft.com> 2.14.3-2
- Rename go to golang
- Add ca-certificates temporarily

* Thu Oct 17 2019 Andrew Phelps <anphel@microsoft.com> 2.14.3-1
- Initial version for Mariner
