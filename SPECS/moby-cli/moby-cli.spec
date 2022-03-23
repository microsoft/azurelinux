Summary: The open-source application container engine client.
Name: moby-cli
Version: 19.03.15+azure
Release: 7%{?dist}
License: ASL 2.0
Group: Tools/Container

# Git clone is a standard practice of producing source files for moby-* packages.
# Please look at ./generate-sources.sh for generating source tar ball.
# REPO = https://github.com/docker/cli.git
%define CLI_COMMIT 48d30b5b32e99c932b4ea3edca74353feddd83ff
#Source0: https://github.com/docker/cli/archive/v19.03.15.tar.gz
Source0: moby-cli-%{version}.tar.gz
Source1: NOTICE
Source2: LICENSE
URL: https://github.com/docker/cli
Vendor: Microsoft Corporation
Distribution: Mariner

BuildRequires: golang
BuildRequires: bash
BuildRequires: gcc
BuildRequires: libltdl-devel
BuildRequires: make
BuildRequires: git
BuildRequires: go-md2man

Requires: /bin/sh
Requires: tar
Requires: xz

%description
%{summary}

%define OUR_GOPATH  %{_topdir}/.gopath

%prep
%setup -q -n %{name}-%{version} -c
mkdir -p %{OUR_GOPATH}/src/github.com/docker
ln -sfT %{_topdir}/BUILD/%{name}-%{version} %{OUR_GOPATH}/src/github.com/docker/cli
# Fix incorrect package name reference for go-md2man
sed -i 's/md2man/go-md2man/g' ./man/md2man-all.sh

%build
export GOPATH=%{OUR_GOPATH}
export GOCACHE=%{OUR_GOPATH}/.cache
export GOPROXY=off
export GO111MODULE=off
#export GOFLAGS=-trimpath
export DISABLE_WARN_OUTSIDE_CONTAINER=1
export GOGC=off
export CGO_ENABLED=1

cd %{OUR_GOPATH}/src/github.com/docker/cli
make \
    LDFLAGS='' \
    VERSION=%{version} \
    GITCOMMIT=%{CLI_COMMIT} \
    dynbinary

# Generating man pages.
make manpages

%install
mkdir -p %{buildroot}/%{_bindir}
cp -aLT build/docker %{buildroot}/%{_bindir}/docker

install -dp %{buildroot}%{_mandir}/man{1,5,8}
install -p -m 644 man/man1/*.1 %{buildroot}/%{_mandir}/man1
install -p -m 644 man/man5/*.5 %{buildroot}/%{_mandir}/man5
install -p -m 644 man/man8/*.8 %{buildroot}/%{_mandir}/man8

install -d %{buildroot}/usr/share/bash-completion/completions
install -d %{buildroot}/usr/share/zsh/vendor-completions
install -d %{buildroot}/usr/share/fish/vendor_completions.d
install -p -m 644 contrib/completion/bash/docker %{buildroot}/usr/share/bash-completion/completions/docker
install -p -m 644 contrib/completion/zsh/_docker %{buildroot}/usr/share/zsh/vendor-completions/_docker
install -p -m 644 contrib/completion/fish/docker.fish %{buildroot}/usr/share/fish/vendor_completions.d/docker.fish

mkdir -p %{buildroot}/usr/share/doc/%{name}-%{version}
cp %{SOURCE1} %{buildroot}/usr/share/doc/%{name}-%{version}/NOTICE
cp %{SOURCE2} %{buildroot}/usr/share/doc/%{name}-%{version}/LICENSE

# list files owned by the package here
%files
%license LICENSE
/usr/share/doc/%{name}-%{version}/*
/%{_bindir}/docker
/%{_mandir}/man1/*
/%{_mandir}/man5/*
/%{_mandir}/man8/*
/usr/share/bash-completion/completions/docker
/usr/share/zsh/vendor-completions/_docker
/usr/share/fish/vendor_completions.d/docker.fish

%changelog
* Tue Mar 15 2022 Muhammad Falak <mwani@microsoft.com> - 19.03.15+azure-7
- Bump release to force rebuild with golang 1.16.15

* Fri Feb 18 2022 Thomas Crain <thcrain@microsoft.com> - 19.03.15+azure-6
- Bump release to force rebuild with golang 1.16.14

* Wed Jan 19 2022 Henry Li <lihl@microsoft.com> - 19.03.15+azure-5
- Increment release for force republishing using golang 1.16.12

* Tue Nov 02 2021 Thomas Crain <thcrain@microsoft.com> - 19.03.15+azure-4
- Increment release for force republishing using golang 1.16.9

* Fri Aug 06 2021 Nicolas Guibourge <nicolasg@microsoft.com> 19.03.15+azure-3
- Increment release to force republishing using golang 1.16.7.

* Tue Jun 08 2021 Henry Beberman <henry.beberman@microsoft.com> 19.03.15+azure-2
- Increment release to force republishing using golang 1.15.13.

* Thu Apr 15 2021 Andrew Phelps <anphel@microsoft.com> 19.03.15+azure-1
- Update to version 19.03.15+azure
- Rename 'md2man' to 'go-md2man' in md2man-all.sh

* Thu Dec 10 2020 Andrew Phelps <anphel@microsoft.com> 19.03.11+azure-2
- Increment release to force republishing using golang 1.15.

* Thu Jun 11 2020 Andrew Phelps <anphel@microsoft.com> 19.03.11+azure-1
- Update to version 19.03.11+azure

* Wed May 20 2020 Joe Schmitt <joschmit@microsoft.com> 3.0.12~rc.1+azure-5
- Remove reliance on existing GOPATH environment variable.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 3.0.12~rc.1+azure-4
- Added %%license line automatically

* Tue May 05 2020 Eric Li <eli@microsoft.com> 3.0.12~rc.1+azure-3
- Add #Source0:, update URL:, and license verified

* Fri May 01 2020 Emre Girgin <mrgirgin@microsoft.com> 3.0.12~rc.1+azure-2
- Renaming go to golang

* Fri Apr 03 2020 Mohan Datla <mdatla@microsoft.com> 3.0.12~rc.1+azure-1
- Initial CBL-Mariner import from Azure.

* Mon Jan 27 2020 Brian Goffs <brgoff@microsoft.com>
- Use dynamic linking and issue build commands from rpm spec

* Tue Aug 7 2018 Robledo Pontes <rafilho@microsoft.com>
- Adding to moby build tools.

* Mon Mar 12 2018 Xing Wu <xingwu@microsoft.com>
- First draft
