%global rcluadir %{_rpmconfigdir}/lua/azl
%global rpmmacrodir %{_rpmconfigdir}/macros.d

Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global forgeurl  https://pagure.io/go-rpm-macros
Version:   3.6.0
%forgemeta

%global _spectemplatedir %{_datadir}/rpmdevtools/azl
%global _docdir_fmt     %{name}

# Master definition that will be written to macro files
%global golang_arches   %{ix86} x86_64 %{arm} aarch64 ppc64le s390x
%global gccgo_arches    %{mips}
# Go sources can contain arch-specific files and our macros will package the
# correct files for each architecture. Therefore, move gopath to _libdir and
# make Go devel packages archful
%global gopath          %{_datadir}/gocode

ExclusiveArch: %{golang_arches} %{gccgo_arches}

Name:      go-rpm-macros
Release:   1%{?dist}
Summary:   Build-stage rpm automation for Go packages

License:   GPLv3+
URL:       %{forgeurl}
Source0:  https://pagure.io/go-rpm-macros/archive/3.6.0/%{name}-%{version}.tar.gz
Source1:    %{forgesource}

Requires:  go-srpm-macros = %{version}-%{release}
Requires:  go-filesystem  = %{version}-%{release}

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

%description -n go-srpm-macros
This package provides SRPM-stage rpm automation to simplify the creation of Go
language (golang) packages.

It limits itself to the automation subset required to create Go SRPM packages
and needs to be included in the default build root.

The rest of the automation is provided by the go-rpm-macros package, that
go-srpm-macros will pull in for Go packages only.

%package -n go-filesystem
Summary:   Directories used by Go packages
License:   Public Domain

%description -n go-filesystem
This package contains the basic directory layout used by Go packages.

%package -n go-rpm-templates
Summary:   RPM spec templates for Go packages
License:   MIT
BuildArch: noarch
Requires:  go-rpm-macros = %{version}-%{release}

%description -n go-rpm-templates
This package contains documented rpm spec templates showcasing how to use the
macros provided by go-rpm-macros to create Go packages.

%prep
%forgeautosetup -p1
%writevars -f rpm/macros.d/macros.go-srpm golang_arches gccgo_arches gopath
for template in templates/rpm/*\.spec ; do
  target=$(echo "${template}" | sed "s|^\(.*\)\.spec$|\1-bare.spec|g")
  grep -v '^#' "${template}" > "${target}"
  touch -r "${template}" "${target}"
done

%install
install -m 0755 -vd   %{buildroot}%{gopath}/src

install -m 0755 -vd   %{buildroot}%{_spectemplatedir}

install -m 0644 -vp   templates/rpm/*spec \
                      %{buildroot}%{_spectemplatedir}

install -m 0755 -vd   %{buildroot}%{_bindir}
install -m 0755 bin/* %{buildroot}%{_bindir}

install -m 0755 -vd   %{buildroot}%{rpmmacrodir}
install -m 0644 -vp   rpm/macros.d/macros.go-* \
                      %{buildroot}%{rpmmacrodir}
install -m 0755 -vd   %{buildroot}%{rcluadir}/srpm
install -m 0644 -vp   rpm/lua/srpm/*lua \
                      %{buildroot}%{rcluadir}/srpm
install -m 0755 -vd   %{buildroot}%{rcluadir}/rpm
install -m 0644 -vp   rpm/lua/rpm/*lua \
                      %{buildroot}%{rcluadir}/rpm
install -m 0755 -vd   %{buildroot}%{_rpmconfigdir}/fileattrs
install -m 0644 -vp   rpm/fileattrs/*.attr \
                      %{buildroot}%{_rpmconfigdir}/fileattrs/
install -m 0755 -vp   rpm/*\.{prov,deps} \
                      %{buildroot}%{_rpmconfigdir}/

%ifarch %{golang_arches}
install -m 0644 -vp   rpm/macros.d/macros.go-compilers-golang \
                      %{buildroot}%{rpmmacrodir}/macros.go-compiler-golang
%endif

%ifarch %{gccgo_arches}
install -m 0644 -vp   rpm/macros.d/macros.go-compilers-gcc \
                      %{buildroot}%{rpmmacrodir}/macros.go-compiler-gcc
%endif

%files
%license LICENSE.txt
%doc README.md
%{_bindir}/*
%{_rpmconfigdir}/fileattrs/*.attr
%{_rpmconfigdir}/*.prov
%{_rpmconfigdir}/*.deps
%{rpmmacrodir}/macros.go-rpm*
%{rpmmacrodir}/macros.go-compiler*
%{rcluadir}/rpm/*.lua

%files -n go-srpm-macros
%license LICENSE.txt
%doc README.md
%{rpmmacrodir}/macros.go-srpm
%{rcluadir}/srpm/*.lua

%files -n go-filesystem
%dir %{gopath}
%dir %{gopath}/src

%files -n go-rpm-templates
%license LICENSE-templates.txt
%doc README.md
%dir %{dirname:%{_spectemplatedir}}
%dir %{_spectemplatedir}
%{_spectemplatedir}/*.spec

%changelog
* Wed Nov 20 2024 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 3.6.0-1
- Update to 3.6.0.
- License verified

* Tue Mar 01 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.0.9-3
- Fixing Go's linker flags.
- License verified.

* Thu Sep 23 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.0.9-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).
- Adjusting directories to CBL-Mariner.
- Removed dependency on 'golist'.

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
