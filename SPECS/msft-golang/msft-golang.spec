%global goroot          %{_libdir}/golang
%global gopath          %{_datadir}/gocode
%global ms_go_filename  go1.22.8-20241001.6.src.tar.gz
%global ms_go_revision  1
%ifarch aarch64
%global gohostarch      arm64
%else
%global gohostarch      amd64
%endif
%define debug_package %{nil}
%define __strip /bin/true
# rpmbuild magic to keep from having meta dependency on libc.so.6
%define _use_internal_dependency_generator 0
%define __find_requires %{nil}
Summary:        Go
Name:           msft-golang
Version:        1.22.8
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://github.com/microsoft/go
Source0:        https://github.com/microsoft/go/releases/download/v%{version}-%{ms_go_revision}/%{ms_go_filename}
# bootstrap 00, same content as https://dl.google.com/go/go1.4-bootstrap-20171003.tar.gz
Source1:        https://github.com/microsoft/go/releases/download/v1.4.0-1/go1.4-bootstrap-20171003.tar.gz
# bootstrap 01
Source2:        https://github.com/microsoft/go/releases/download/v1.19.12-1/go.20230802.5.src.tar.gz
# bootstrap 02
Source3:        https://github.com/microsoft/go/releases/download/v1.20.14-1/go.20240206.2.src.tar.gz
Patch0:         go14_bootstrap_aarch64.patch
Conflicts:      go
Conflicts:      golang

%description
Go is an open source programming language that makes it easy to build simple, reliable, and efficient software.

%prep
# Setup go 1.4 bootstrap source
tar xf %{SOURCE1} --no-same-owner
patch -Np1 --ignore-whitespace < %{PATCH0}
mv -v go go-bootstrap-00

tar xf %{SOURCE2} --no-same-owner
mv -v go go-bootstrap-01

tar xf %{SOURCE3} --no-same-owner
mv -v go go-bootstrap-02

%setup -q -n go

%build
# go 1.4 bootstraps with C.
# go 1.20 bootstraps with go >= 1.17.13
# go >= 1.22 bootstraps with go >= 1.20.14
#
# These conditions make building the current go compiler from C a multistep
# process. Approximately once a year, the bootstrap requirement is moved
# forward, adding another step.
#
# PS: Since go compiles fairly quickly, the extra overhead is around 2-3 minutes
#     on a reasonable machine.

# Use prev bootstrap to compile next bootstrap.
function go_bootstrap() {
  local bootstrap=$1
  local new_root=%{_topdir}/BUILD/go-bootstrap-${bootstrap}
  (
    cd ${new_root}/src
    CGO_ENABLED=0 ./make.bash
  )
  # Nuke the older bootstrapper
  rm -rf %{_libdir}/golang
  # Install the new bootstrapper
  mv -v $new_root %{_libdir}/golang
  export GOROOT=%{_libdir}/golang
  export GOROOT_BOOTSTRAP=%{_libdir}/golang
}

go_bootstrap 00
go_bootstrap 01
go_bootstrap 02

# Build current go version
export GOHOSTOS=linux
export GOHOSTARCH=%{gohostarch}
export GOROOT_BOOTSTRAP=%{goroot}

export GOROOT="`pwd`"
export GOPATH=%{gopath}
export GOROOT_FINAL=%{_bindir}/go
rm -f  %{gopath}/src/runtime/*.c
(
  cd src
  ./make.bash --no-clean
)

%install

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{goroot}

cp -R api bin doc lib pkg src misc VERSION go.env %{buildroot}%{goroot}

# remove the unnecessary zoneinfo file (Go will always use the system one first)
rm -rfv %{buildroot}%{goroot}/lib/time

# remove the doc Makefile
rm -rfv %{buildroot}%{goroot}/doc/Makefile

# put binaries to bindir, linked to the arch we're building,
# leave the arch independent pieces in %%{goroot}
mkdir -p %{buildroot}%{goroot}/bin/linux_%{gohostarch}
ln -sfv ../go %{buildroot}%{goroot}/bin/linux_%{gohostarch}/go
ln -sfv ../gofmt %{buildroot}%{goroot}/bin/linux_%{gohostarch}/gofmt
ln -sfv %{goroot}/bin/gofmt %{buildroot}%{_bindir}/gofmt
ln -sfv %{goroot}/bin/go %{buildroot}%{_bindir}/go

# ensure these exist and are owned
mkdir -p %{buildroot}%{gopath}/src/github.com/
mkdir -p %{buildroot}%{gopath}/src/bitbucket.org/
mkdir -p %{buildroot}%{gopath}/src/code.google.com/p/

install -vdm755 %{buildroot}%{_sysconfdir}/profile.d
cat >> %{buildroot}%{_sysconfdir}/profile.d/go-exports.sh <<- "EOF"
export GOROOT=%{goroot}
export GOPATH=%{_datadir}/gocode
export GOHOSTOS=linux
export GOHOSTARCH=%{gohostarch}
export GOOS=linux
EOF

%post -p /sbin/ldconfig
%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  #This is uninstall
  rm %{_sysconfdir}/profile.d/go-exports.sh
  rm -rf /opt/go
  exit 0
fi

%files
%defattr(-,root,root)
%license LICENSE
%exclude %{goroot}/src/*.rc
%exclude %{goroot}/include/plan9
%{_sysconfdir}/profile.d/go-exports.sh
%{goroot}/*
%{gopath}/src
%exclude %{goroot}/src/pkg/debug/dwarf/testdata
%exclude %{goroot}/src/pkg/debug/elf/testdata
%{_bindir}/*

%changelog
* Thu Oct 24 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.22.8-1
- Auto-upgrade to 1.22.8 - To fix CVE-2022-41717

* Mon Sep 09 2024 Henry Beberman <henry.beberman@microsoft.com> - 1.22.7-1
- Bump version to 1.22.7 to address CVE-2024-34158, CVE-2024-34156, CVE-2024-34155

* Thu Jul 04 2024 Muhammad Falak <mwani@microsoft.com> - 1.22.5-1
- Bump version to 1.22.4

* Fri Jun 07 2024 Muhammad Falak <mwani@microsoft.com> - 1.22.4-1
- Bump version to 1.22.4

* Wed May 15 2024 Muhammad Falak <mwani@microsoft.com> - 1.22.3-1
- Introduce function in spec to simplify bootstrapping
- Bump version to 1.22.3

* Mon Apr 15 2024 Muhammad Falak <mwani@microsoft.com> - 1.22.2-1
- Bump version to 1.22.2

* Fri Mar 22 2024 Muhammad Falak <mwani@microsoft.com> - 1.21.8-1
- Bump version to 1.21.8

* Wed Mar 06 2024 Muhammad Falak <mwani@microsoft.com> - 1.21.6-2
- Include go.env in GOROOT

* Mon Jan 29 2024 Muhammad Falak <mwani@microsoft.com> - 1.21.6-1
- Bump version to 1.21.6

* Wed Nov 22 2023 Andrew Phelps <anphel@microsoft.com> - 1.20.11-1
- Upgrade to 1.20.11
- Keep go 1.19.12 source to provide additional go boostrap

* Wed Aug 16 2023 Brian Fjeldstad <bfjelds@microsoft.com> - 1.19.12-1
- Upgrade to 1.19.12 to fix CVE-2023-39533
1.22.2
* Tue Jun 06 2023 Bala <balakumaran.kannan@microsoft.com> - 1.19.10-1
- Upgrade to 1.19.10 to fix CVE-2023-29404

* Wed Apr 05 2023 Muhammad Falak <mwani@microsoft.com> - 1.19.8-1
- Bump version to address CVE-2023-24534, CVE-2023-24536, CVE-2023-24537, CVE-2023-24538

* Tue Mar 28 2023 Muhammad Falak <mwani@microsoft.com> - 1.19.7-1
- Bump version to address CVE-2022-41722, CVE-2022-41724, CVE-2022-41725, CVE-2022-41723, CVE-2023-24532

* Sat Sep 24 2022 Muhammad Falak <mwani@microsoft.com> - 1.19.1-2
- Drop the explict VERSION in build

* Thu Sep 22 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 1.19.1-1
- Uograde to version to 1.19.1

* Thu May 05 2022 Muhammad Falak <mwani@microsoft.com> - 1.18.1-1
- Switch to `microsoft/go` for a fips compliant version of go

* Tue Apr 12 2022 Muhammad Falak <mwani@microsoft.com> - 1.17.8-1
- Bump version to 1.17.8 to address CVE-2021-44716

* Thu Feb 17 2022 Andrew Phelps <anphel@microsoft.com> - 1.17.1-2
- Use _topdir instead of hard-coded value /usr/src/mariner
- License verified

* Wed Sep 15 2021 Andrew Phelps <anphel@microsoft.com> - 1.17.1-1
- Updated to version 1.17.1

* Tue Jun 08 2021 Henry Beberman <henry.beberman@microsoft.com> - 1.15.13-1
- Updated to version 1.15.13 to fix CVE-2021-33194 and CVE-2021-31525

* Mon Apr 26 2021 Nicolas Guibourge <nicolasg@microsoft.com> - 1.15.11-1
- Updated to version 1.15.11 to fix CVE-2021-27918

* Wed Feb 03 2021 Andrew Phelps <anphel@microsoft.com> - 1.15.7-1
- Updated to version 1.15.7 to fix CVE-2021-3114

* Mon Nov 23 2020 Henry Beberman <henry.beberman@microsoft.com> - 1.15.5-1
- Updated to version 1.15.5

* Fri Oct 30 2020 Thomas Crain <thcrain@microsoft.com> - 1.13.15-2
- Patch CVE-2020-24553

* Tue Sep 08 2020 Nicolas Ontiveros <niontive@microsoft.com> - 1.13.15-1
- Updated to version 1.13.15, which fixes CVE-2020-14039 and CVE-2020-16845.

* Sun May 24 2020 Mateusz Malisz <mamalisz@microsoft.com> - 1.13.11-1
- Updated to version 1.13.11

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.12.5-7
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 1.12.5-6
- Renaming go to golang

* Thu Apr 23 2020 Nicolas Ontiveros <niontive@microsoft.com> - 1.12.5-5
- Fix CVE-2019-14809.

* Fri Mar 27 2020 Andrew Phelps <anphel@microsoft.com> - 1.12.5-4
- Support building standalone by adding go 1.4 bootstrap.

* Thu Feb 27 2020 Henry Beberman <hebeberm@microsoft.com> - 1.12.5-3
- Remove meta dependency on libc.so.6

* Thu Feb 6 2020 Andrew Phelps <anphel@microsoft.com> - 1.12.5-2
- Remove ExtraBuildRequires

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.12.5-1
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Jan 21 2019 Bo Gan <ganb@vmware.com> - 1.9.7-1
- Update to 1.9.7

* Wed Oct 24 2018 Alexey Makhalov <amakhalov@vmware.com> - 1.9.4-3
- Use extra build requires

* Mon Apr 02 2018 Dheeraj Shetty <dheerajs@vmware.com> - 1.9.4-2
- Fix for CVE-2018-7187

* Thu Mar 15 2018 Xiaolin Li <xiaolinl@vmware.com> - 1.9.4-1
- Update to golang release v1.9.4

* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> - 1.9.1-2
- Aarch64 support

* Wed Nov 01 2017 Vinay Kulkarni <kulkarniv@vmware.com> - 1.9.1-1
- Update to golang release v1.9.1

* Wed May 31 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.8.1-2
- Remove mercurial from buildrequires and requires.

* Tue Apr 11 2017 Danut Moraru <dmoraru@vmware.com> - 1.8.1-1
- Update Golang to version 1.8.1, updated patch0

* Wed Dec 28 2016 Xiaolin Li <xiaolinl@vmware.com> - 1.7.4-1
- Updated Golang to 1.7.4.

* Thu Oct 06 2016 ChangLee <changlee@vmware.com> - 1.6.3-2
- Modified %check

* Wed Jul 27 2016 Anish Swaminathan <anishs@vmware.com> - 1.6.3-1
- Update Golang to version 1.6.3 - fixes CVE 2016-5386

* Fri Jul 8 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 1.6.2-1
- Updated the Golang to version 1.6.2

* Thu Jun 2 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.4.2-5
- Fix script syntax

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.4.2-4
- GA - Bump release of all rpms

* Thu May 05 2016 Kumar Kaushik <kaushikk@vmware.com> - 1.4.2-3
- Handling upgrade scenario pre/post/un scripts.

* Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> - 1.4.2-2
- Edit post script.

* Mon Aug 03 2015 Vinay Kulkarni <kulkarniv@vmware.com> - 1.4.2-1
- Update to golang release version 1.4.2

* Fri Oct 17 2014 Divya Thaluru <dthaluru@vmware.com> - 1.3.3-1
- Initial build.  First version
