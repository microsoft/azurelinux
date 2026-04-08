# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Copyright (C) 2024 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT
# License text: https://spdx.org/licenses/MIT

%bcond manpages 1
# Whether to build the scancode extra
%bcond scancode %{defined fedora}
# Only run scancode tests (and install scancode at buildtime) when arch is not i386
%bcond scancode_tests %[ %{with scancode} && "%{_arch}" != "i386"]

%global forgeurl https://gitlab.com/fedora/sigs/go/go-vendor-tools
%define tag v%{version_no_tilde %{quote:%nil}}

Name:           go-vendor-tools
Version:        0.10.0
%forgemeta
Release:        1%{?dist}
Summary:        Tools for handling Go library vendoring in Fedora [SEE NOTE IN DESCRIPTION]

# BSD-3-Clause: src/go_vendor_tools/archive.py
License:        MIT AND BSD-3-Clause
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildArch:      noarch

BuildRequires:  python3-devel

# Test dependencies
BuildRequires:  askalono-cli
BuildRequires:  trivy

%if %{with manpages}
BuildRequires:  scdoc
%endif

# First choice backend
Recommends:     askalono-cli
# Used by default for go_vendor_license report --autofill
Recommends:     go-vendor-tools+scancode
Recommends:     go-vendor-tools+all

# NOTE(gotmax23): Buildflags from go-rpm-macros are used by %%gocheck2 defined
# in this package, but we don't want to depend on it directly.
# Packages should still explicitly require go-rpm-macros, and the license
# scanning in this package could potentially be useful outside of the Go ecosystem,
# so it would be nice to avoid dependning on go-rpm-macros in this package.
# Requires:       go-rpm-macros


%global common_description %{expand:
go-vendor-tools provides tools and macros for handling Go library vendoring in
Fedora.

STABILITY NOTE:

go-vendor-tools is under active development and available in the stable Fedora
and Fedora EPEL repos for testing purposes.
Expect some breaking changes between releases.
Anyone using the `%%go_vendor_*` macros in active Fedora packages MUST join the
Fedora Golang Matrix room and Fedora Go SIG mailing list to be notified of any
major changes.}

%description %common_description


%package doc
Summary:        Documentation for go-vendor-tools
Enhances:       go-vendor-tools

%description doc %common_description


%prep
%autosetup -p1 %{forgesetupargs}


%generate_buildrequires
%pyproject_buildrequires -x all,test%{?with_scancode_tests:,scancode}


%build
%pyproject_wheel
%if %{with manpages}
./doc/man/mkman.sh
%endif

mkdir -p bash_completions fish_completions zsh_completions
for bin in go_vendor_archive go_vendor_license gocheck2; do
    register-python-argcomplete --shell bash "${bin}" > "bash_completions/${bin}"
    register-python-argcomplete --shell fish "${bin}" > "fish_completions/${bin}.fish"
    # Compatibility with old argcomplete versions that don't direcrly support zsh
    if ! (register-python-argcomplete --shell zsh "${bin}" > "zsh_completions/_${bin}"); then
        echo "#compdef ${bin}" > "zsh_completions/_${bin}"
        echo -e "autoload -Uz bashcompinit\nbashcompinit" >> "zsh_completions/_${bin}"
        cat "bash_completions/${bin}" >> "zsh_completions/_${bin}"
    fi
done


%install
%pyproject_install
%pyproject_save_files go_vendor_tools -l

# Install RPM macros
install -Dpm 0644 rpm/macros.go_vendor_tools -t %{buildroot}%{_rpmmacrodir}
install -Dpm 0644 rpm/macros.gocheck2 -t %{buildroot}%{_rpmmacrodir}

# Install documentation
mkdir -p %{buildroot}%{_docdir}/go-vendor-tools-doc
cp -rL doc/* %{buildroot}%{_docdir}/go-vendor-tools-doc

# Install manpages
%if %{with manpages}
install -Dpm 0644 doc/man/*.1 -t %{buildroot}%{_mandir}/man1/
install -Dpm 0644 doc/man/*.5 -t %{buildroot}%{_mandir}/man5/
%endif

# Install completions
install -Dpm 0644 bash_completions/* -t %{buildroot}%{bash_completions_dir}/
install -Dpm 0644 fish_completions/* -t %{buildroot}%{fish_completions_dir}/
install -Dpm 0644 zsh_completions/* -t %{buildroot}%{zsh_completions_dir}/


%check
export MACRO_DIR=%{buildroot}%{_rpmmacrodir}
%pytest


%files -f %{pyproject_files}
# Install top-level markdown files
%doc *.md
%{_bindir}/gocheck2
%{_bindir}/go_vendor*
%{bash_completions_dir}/go*
%{fish_completions_dir}/go*.fish
%{zsh_completions_dir}/_go*
%{_rpmmacrodir}/macros.gocheck2
%{_rpmmacrodir}/macros.go_vendor_tools
%if %{with manpages}
%{_mandir}/man1/go*.1*
%{_mandir}/man5/go*.5*
%endif


%files doc
%doc %{_docdir}/go-vendor-tools-doc/


%pyproject_extras_subpkg -n go-vendor-tools all %{?with_scancode:scancode}


%changelog
* Fri Oct 31 2025 Maxwell G <maxwell@gtmx.me> - 0.10.0-1
- Update to 0.10.0.

* Thu Oct 2 2025 Maxwell G <maxwell@gtmx.me> - 0.9.0-1
- Update to 0.9.0.

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.8.0-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Tue Aug 19 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 0.8.0-4
- Re-enable scancode on Python 3.14

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.8.0-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 17 2025 Maxwell G <maxwell@gtmx.me> - 0.8.0-1
- Update to 0.8.0.

* Tue Jun 10 2025 Maxwell G <maxwell@gtmx.me> - 0.7.0-2
- Disable scancode on Python 3.14

* Sun Mar 23 2025 Maxwell G <maxwell@gtmx.me> - 0.7.0-1
- Update to 0.7.0.

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 28 2024 Maxwell G <maxwell@gtmx.me> - 0.6.0-1
- Update to 0.6.0.

* Mon Aug 5 2024 Maxwell G <maxwell@gtmx.me> - 0.5.1-4
- Add note about project stability to description

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 14 2024 Maxwell G <maxwell@gtmx.me> - 0.5.1-2
- Rebuild for Python 3.13

* Fri Apr 12 2024 Maxwell G <maxwell@gtmx.me> - 0.5.1-1
- Update to 0.5.1.

* Wed Apr 3 2024 Maxwell G <maxwell@gtmx.me> - 0.3.0-3
- Fix directory ownership patch

* Wed Apr 3 2024 Maxwell G <maxwell@gtmx.me> - 0.3.0-2
- Backport patch to fix directory ownership for %%go_vendor_license_install filelist

* Thu Mar 28 2024 Maxwell G <maxwell@gtmx.me> - 0.3.0-1
- Initial package (rhbz#2268011).
