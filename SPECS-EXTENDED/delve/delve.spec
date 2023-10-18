Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:                   delve
Version:                1.5.0
Release:                16%{?dist}
Summary:                A debugger for the Go programming language

License:                MIT
URL:                    https://github.com/go-delve/delve
Source0:                https://github.com/go-delve/delve/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

ExcludeArch:            ppc64le s390x aarch64 %{ix86} armv7hl

BuildRequires:          go-rpm-macros
BuildRequires:          golang
BuildRequires:          git
BuildRequires:          lsof

Provides:               dlv = %{version}

# https://github.com/go-delve/delve/pull/2223
Patch0:                 golang-1.15.4-TestStepIntoWrapperForEmbeddedPointer.patch


%description
Delve is a debugger for the Go programming language. The goal of the project 
is to provide a simple, full featured debugging tool for Go. Delve should be 
easy to invoke and easy to use. Chances are if you're using a debugger, things 
aren't going your way. With that in mind, Delve should stay out of your way as 
much as possible.


%prep
%setup -q

%patch0 -p1
rm -rf go.mod
mv vendor %{_builddir}/src
mkdir -p "%{_builddir}/src/github.com/go-delve/"
cp -r %{_builddir}/%{name}-%{version} %{_builddir}/src/github.com/go-delve/%{name}
mkdir -p %{_builddir}/%{name}-%{version}/_build
mv %{_builddir}/src %{_builddir}/%{name}-%{version}/_build/src


%build
export GO111MODULE=off
export GOPATH="%{_builddir}/%{name}-%{version}/_build"
export LDFLAGS=
%gobuild -o bin/dlv github.com/go-delve/delve/cmd/dlv


%install
export GO111MODULE=off
export GOPATH="%{_builddir}/%{name}-%{version}/_build"
install -Dpm 0755 bin/dlv %{buildroot}%{_bindir}/dlv


%check
export GO111MODULE=off
export GOPATH="%{_builddir}/%{name}-%{version}/_build"
cd "_build/src/github.com/go-delve/%{name}"
for d in $(go list ./... | grep -v cmd | grep -v scripts); do
    go test ${d}
done


%files
%license LICENSE
%doc CONTRIBUTING.md CHANGELOG.md
%doc Documentation/*
%{_bindir}/dlv


%changelog
* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.5.0-16
- Bump release to rebuild with go 1.20.10

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 1.5.0-15
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.5.0-14
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.5.0-13
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.5.0-12
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.5.0-11
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.5.0-10
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.5.0-9
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.5.0-8
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.5.0-7
- Bump release to rebuild with go 1.19.4

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.5.0-6
- Bump release to rebuild with go 1.18.8

* Tue Aug 23 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5.0-5
- License verified.

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.5.0-4
- Bump release to rebuild against Go 1.18.5

* Thu Sep 23 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5.0-3
- Initial CBL-Mariner import from CentOS 8 (license: MIT).
- Adding missing BR on 'go-rpm-macros'.
- Running with empty 'LDFLAGS' to fix the build.

* Tue Nov 24 2020 David Benoit <dbenoit@redhat.com> - 1.5.0-2
- Add golang-1.15.4 related patch
- Resolves: rhbz#1901189

* Wed Sep 09 2020 Alejandro Sáez <asm@redhat.com> - 1.5.0-1
- Rebase to 1.5.0
- Related: rhbz#1870531

* Mon May 25 2020 Alejandro Sáez <asm@redhat.com> - 1.4.1-1
- Rebase to 1.4.1
- Resolves: rhbz#1821281
- Related: rhbz#1820596

* Fri May 22 2020 Alejandro Sáez <asm@redhat.com> - 1.4.0-2
- Change i686 to a better macro
- Related: rhbz#1820596

* Tue Apr 28 2020 Alejandro Sáez <asm@redhat.com> - 1.4.0-1
- Rebase to 1.4.0
- Remove Patch1781
- Related: rhbz#1820596

* Thu Jan 16 2020 Alejandro Sáez <asm@redhat.com> - 1.3.2-3
- Resolves: rhbz#1758612
- Resolves: rhbz#1780554
- Add patch: 1781-pkg-terminal-Fix-exit-status.patch

* Wed Jan 15 2020 Alejandro Sáez <asm@redhat.com> - 1.3.2-2
- Added tests
- Related: rhbz#1758612

* Wed Nov 27 2019 Alejandro Sáez <asm@redhat.com> - 1.3.2-1
- First package for RHEL
- Related: rhbz#1758612
