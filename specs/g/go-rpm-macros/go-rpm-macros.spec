## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond tests 1
%global forgeurl  https://gitlab.com/fedora/sigs/go/go-rpm-macros
Version:   3.8.0
%forgemeta

%global debug_package %{nil}

#https://src.fedoraproject.org/rpms/redhat-rpm-config/pull-request/51
%global _spectemplatedir %{_datadir}/rpmdevtools/fedora
%global _docdir_fmt     %{name}

# Master definition that will be written to macro files
%global golang_arches_future x86_64 %{arm} aarch64 ppc64le s390x riscv64
%global golang_arches   %{ix86} %{golang_arches_future}
%global gccgo_arches    %{mips}
%if 0%{?rhel} >= 9
%global golang_arches   x86_64 aarch64 ppc64le s390x
%endif
%if 0%{?rhel} >= 10
%global golang_arches   x86_64 aarch64 ppc64le s390x riscv64
%endif
# Go sources can contain arch-specific files and our macros will package the
# correct files for each architecture. Therefore, move gopath to _libdir and
# make Go devel packages archful
%global gopath          %{_datadir}/gocode

Name:      go-rpm-macros
Release:   %autorelease
Summary:   Build-stage rpm automation for Go packages

License:   GPL-3.0-or-later
URL:       %{forgeurl}
Source:    %{forgesource}

%if %{with tests}
BuildRequires: pyproject-rpm-macros
%endif

Requires:  go-srpm-macros = %{version}-%{release}
Requires:  go-filesystem  = %{version}-%{release}
Requires:  golist

%ifarch %{golang_arches}
Requires:  golang
Provides:  compiler(golang)
Provides:  compiler(go-compiler) = 2
Obsoletes: go-compilers-golang-compiler < %{version}-%{release}
%endif

%ifarch %{gccgo_arches}
Requires:  gcc-go
Provides:  compiler(gcc-go)
Provides:  compiler(go-compiler) = 1
Obsoletes: go-compilers-gcc-go-compiler < %{version}-%{release}
%endif

%description
This package provides build-stage rpm automation to simplify the creation of Go
language (golang) packages.

It does not need to be included in the default build root: go-srpm-macros will
pull it in for Go packages only.

%package -n go-srpm-macros
Summary:   Source-stage rpm automation for Go packages
BuildArch: noarch
Requires:  redhat-rpm-config
# macros.forge and forge.lua were split into a separate package.
# redhat-rpm-config pulls in forge-srpm-macros but better to explicitly Require
# it.
%if (0%{?fedora} >= 40 || 0%{?rhel} >= 10)
Requires:  forge-srpm-macros
%endif

%description -n go-srpm-macros
This package provides SRPM-stage rpm automation to simplify the creation of Go
language (golang) packages.

It limits itself to the automation subset required to create Go SRPM packages
and needs to be included in the default build root.

The rest of the automation is provided by the go-rpm-macros package, that
go-srpm-macros will pull in for Go packages only.

%package -n go-filesystem
Summary:   Directories used by Go packages
License:   LicenseRef-Fedora-Public-Domain

%description -n go-filesystem
This package contains the basic directory layout used by Go packages.

%package -n go-rpm-templates
Summary:   RPM spec templates for Go packages
License:   MIT
# go-rpm-macros only exists on some architectures, so this package cannot be noarch
Requires:  go-rpm-macros = %{version}-%{release}
#https://src.fedoraproject.org/rpms/redhat-rpm-config/pull-request/51
#Requires:  redhat-rpm-templates

%description -n go-rpm-templates
This package contains documented rpm spec templates showcasing how to use the
macros provided by go-rpm-macros to create Go packages.

%prep
%forgeautosetup -p1
%writevars -f rpm/macros.d/macros.go-srpm golang_arches golang_arches_future gccgo_arches gopath
for template in templates/rpm/*\.spec ; do
  target=$(echo "${template}" | sed "s|^\(.*\)\.spec$|\1-bare.spec|g")
  grep -v '^#' "${template}" > "${target}"
  touch -r "${template}" "${target}"
done

%if %{with tests}
%generate_buildrequires
%pyproject_buildrequires -g test -RN
%endif

%install
install -m 0755 -vd   %{buildroot}%{rpmmacrodir}

install -m 0755 -vd   %{buildroot}%{_rpmluadir}/fedora/srpm
install -m 0644 -vp   rpm/lua/srpm/*lua \
                      %{buildroot}%{_rpmluadir}/fedora/srpm

%ifarch %{golang_arches} %{gccgo_arches}
# Some of those probably do not work with gcc-go right now
# This is not intentional, but mips is not a primary Fedora architecture
# Patches and PRs are welcome

install -m 0755 -vd   %{buildroot}%{gopath}/src

install -m 0755 -vd   %{buildroot}%{_spectemplatedir}

install -m 0644 -vp   templates/rpm/*spec \
                      %{buildroot}%{_spectemplatedir}

install -m 0755 -vd   %{buildroot}%{_bindir}
install -m 0755 bin/* %{buildroot}%{_bindir}

install -m 0644 -vp   rpm/macros.d/macros.go-*rpm* \
                      %{buildroot}%{rpmmacrodir}
install -m 0755 -vd   %{buildroot}%{_rpmluadir}/fedora/rpm
install -m 0644 -vp   rpm/lua/rpm/*lua \
                      %{buildroot}%{_rpmluadir}/fedora/rpm
install -m 0755 -vd   %{buildroot}%{_rpmconfigdir}/fileattrs
install -m 0644 -vp   rpm/fileattrs/*.attr \
                      %{buildroot}%{_rpmconfigdir}/fileattrs/
install -m 0755 -vp   rpm/*\.{prov,deps} \
                      %{buildroot}%{_rpmconfigdir}/
%else
install -m 0644 -vp   rpm/macros.d/macros.go-srpm \
                      %{buildroot}%{rpmmacrodir}
%endif

%ifarch %{golang_arches}
install -m 0644 -vp   rpm/macros.d/macros.go-compilers-golang{,-pie} \
                      %{buildroot}%{_rpmconfigdir}/macros.d/
%endif

%ifarch %{gccgo_arches}
install -m 0644 -vp   rpm/macros.d/macros.go-compilers-gcc \
                      %{buildroot}%{_rpmconfigdir}/macros.d/
%endif

%check
%if %{with tests}
export MACRO_DIR=%{buildroot}%{_rpmmacrodir}
export MACRO_LUA_DIR="%{buildroot}%{_rpmluadir}"
%pytest -v
%endif

%ifarch %{golang_arches} %{gccgo_arches}
%files
%license LICENSE.txt
%doc README.md
%doc NEWS.md
%{_bindir}/*
%{_rpmconfigdir}/fileattrs/*.attr
%{_rpmconfigdir}/*.prov
%{_rpmconfigdir}/*.deps
%{_rpmmacrodir}/macros.go-rpm*
%{_rpmmacrodir}/macros.go-compiler*
%{_rpmluadir}/fedora/rpm/*.lua

%files -n go-rpm-templates
%license LICENSE-templates.txt
%doc README.md
%doc NEWS.md
# https://src.fedoraproject.org/rpms/redhat-rpm-config/pull-request/51
%dir %{dirname:%{_spectemplatedir}}
%dir %{_spectemplatedir}
%{_spectemplatedir}/*.spec

%files -n go-filesystem
%dir %{gopath}
%dir %{gopath}/src
%endif

# we only build go-srpm-macros on all architectures
%files -n go-srpm-macros
%license LICENSE.txt
%doc README.md
%doc NEWS.md
%{_rpmmacrodir}/macros.go-srpm
%{_rpmluadir}/fedora/srpm/*.lua

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 3.8.0-2
- Latest state for go-rpm-macros

* Thu Sep 04 2025 Maxwell G <maxwell@gtmx.me> - 3.8.0-1
- Update to 3.8.0.

* Thu Jul 24 2025 Maxwell G <maxwell@gtmx.me> - 3.7.0-4
- Revert "HOTFIX: gobuild: set GOEXPERIMENT=nodwarf5"

* Wed Jul 23 2025 Maxwell G <maxwell@gtmx.me> - 3.7.0-3
- HOTFIX: gobuild: set GOEXPERIMENT=nodwarf5

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 17 2025 Maxwell G <maxwell@gtmx.me> - 3.7.0-1
- Update to 3.7.0

* Wed Mar 26 2025 Andrea Bolognani <abologna@redhat.com> - 3.6.0-7
- Add riscv64 to golang_arches for RHEL 10+

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 07 2024 Edjunior Machado <emachado@redhat.com> - 3.6.0-5
- Migrate tests to tests/go-rpm-macros namespace

* Thu Jul 25 2024 Adam Williamson <awilliam@redhat.com> - 3.6.0-4
- Fix SRPM URL in gobuild-grafana test for Fedora 38 being archived

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 17 2024 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 3.6.0-2
- Fix FTBFS

* Sat Apr 13 2024 Maxwell G <maxwell@gtmx.me> - 3.6.0-1
- Update to 3.6.0.

* Fri Mar 01 2024 Maxwell G <maxwell@gtmx.me> - 3.5.0-1
- Update to 3.5.0.

* Thu Feb 08 2024 Edjunior Machado <emachado@redhat.com> - 3.4.0-2
- tests: Use older version of grafana srpm with %%gotest

* Tue Feb 06 2024 Maxwell G <maxwell@gtmx.me> - 3.4.0-1
- Update to 3.4.0.

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Nov 05 2023 Robert-André Mauchin <zebob.m@gmail.com> - 3.3.1-1
- Update to 3.3.1

* Sat Oct 28 2023 Robert-André Mauchin <zebob.m@gmail.com> - 3.3.0-1
- Update to 3.3.0

* Thu Sep 07 2023 Maxwell G <maxwell@gtmx.me> - 3.2.0-7
- Add explicit dependency on forge-srpm-macros

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Apr 24 2023 Edjunior Machado <emachado@redhat.com> - 3.2.0-4
- tests: Fix fmf plan deprecated attributes

* Sun Apr 16 2023 Nianqing Yao <imbearchild@outlook.com> - 3.2.0-3
- Add riscv64 to %%golang_arches

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Sep 02 2022 Maxwell G <gotmax@e.email> - 3.2.0-1
- Update to 3.2.0.

* Fri Sep 02 2022 Maxwell G <gotmax@e.email> - 3.1.0-5
- Use %%{_rpmmacrodir} macro

* Tue Aug 09 2022 Maxwell G <gotmax@e.email> - 3.1.0-4
- Use correct SPDX identifier for Public Domain

* Mon Aug 08 2022 Maxwell G <gotmax@e.email> - 3.1.0-3
- Convert top level license to SPDX.

* Mon Aug 08 2022 Maxwell G <gotmax@e.email> - 3.1.0-2
- Stop installing duplicate go-compilers macros

* Mon Aug 08 2022 Maxwell G <gotmax@e.email> - 3.1.0-1
- Update to 3.1.0.

* Fri Jul 29 2022 Maxwell G <gotmax@e.email> - 3.0.15-4
- Add %%%%golang_arches_future macro

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 02 2022 Miro Hrončok <miro@hroncok.cz> - 3.0.15-2
- Drop ExclusiveArch, always build go-srpm-macros and go-filesystem

* Sun Jan 30 2022 Maxwell G <gotmax@e.email> - 3.0.15-1
- Update to 3.0.15.

* Sat Jan 29 2022 Maxwell G <gotmax@e.email> - 3.0.14-1
- Update to 3.0.14.

* Sat Jan 22 2022 Robert-André Mauchin <zebob.m@gmail.com> - 3.0.13-4
- Fix typo

* Sat Jan 22 2022 Robert-André Mauchin <zebob.m@gmail.com> - 3.0.13-3
- Fix typo

* Sat Jan 22 2022 Robert-André Mauchin <zebob.m@gmail.com> - 3.0.13-2
- Fix archive upload

* Sat Jan 22 2022 Robert-André Mauchin <zebob.m@gmail.com> - 3.0.13-1
- Update to 3.0.13

* Sat Jan 22 2022 Robert-André Mauchin <zebob.m@gmail.com> - 3.0.12-3
- Update to 3.0.12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 17 2021 Robert-André Mauchin <zebob.m@gmail.com> - 3.0.11-1
- Update to 3.0.11

* Mon Apr 26 2021 Alejandro Sáez <asm@redhat.com> - 3.0.10-1
- Update to 3.0.10

* Thu Feb 11 2021 Jeff Law  <law@redhat.com> - 3.0.9-3
- Drop 32 bit arches in EL 9 (originally from Petr Sabata)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Aug 13 2020 Neal Gompa <ngompa13@gmail.com> - 3.0.9-1
- Update to 3.0.9

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 05 2019 Nicolas Mailhot <nim@fedoraproject.org>
- 3.0.8-3
- initial Fedora import, for golist 0.10.0 and redhat-rpm-config 130

## END: Generated by rpmautospec
