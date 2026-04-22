# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# This specfile is licensed under:
#
# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT
# License text: https://spdx.org/licenses/MIT.html

# bconds:
#   tests
#       Run unit tests
#   tomlkit
#       Enable tomlkit and all extras
#   manpages
#       Build manpages using scdoc
#   bootstrap
#       Disable tomlkit dependencies and unit tests.
#       Add ~bootstrap to %%dist
#       Allows tomcli to be built early in the new Python bootstrap process.

%bcond bootstrap 0
%bcond tomlkit %[%{without bootstrap} && (%{undefined rhel} || %{defined epel})]
%bcond tests %{without bootstrap}
%bcond manpages %[%{undefined rhel} || %{defined epel}]

# Add minimal py3_test_envvars for EPEL 9
%if %{undefined py3_test_envvars}
%define py3_test_envvars %{shrink:
PYTHONPATH=%{buildroot}%{python3_sitelib}
PATH=%{buildroot}%{_bindir}:${PATH}
}
%endif

Name:           tomcli
Version:        0.10.1
Release: 4%{?dist}
Summary:        CLI for working with TOML files. Pronounced "tom clee."

License:        MIT
URL:            https://sr.ht/~gotmax23/tomcli
%global furl    https://git.sr.ht/~gotmax23/tomcli
Source0:        %{furl}/refs/download/v%{version}/tomcli-%{version}.tar.gz
Source1:        %{furl}/refs/download/v%{version}/tomcli-%{version}.tar.gz.asc
Source2:        https://meta.sr.ht/~gotmax23.pgp

BuildArch:      noarch
BuildRequires:  gnupg2
BuildRequires:  python3-devel
%if %{with manpages}
BuildRequires:  scdoc
%endif

# One of the TOML backends is required
Requires:       (%{py3_dist tomcli[tomlkit]} or %{py3_dist tomcli[tomli]})
%if %{with tomlkit}
# Prefer the tomlkit backend
Suggests:       %{py3_dist tomcli[tomlkit]}
# Recommend the 'all' extra
Recommends:     %{py3_dist tomcli[all]}
%endif


%description
tomcli is a CLI for working with TOML files. Pronounced "tom clee."


%prep
%gpgverify -d0 -s1 -k2
%autosetup -p1


%generate_buildrequires
%{pyproject_buildrequires %{shrink:
    -x tomli
    %{?with_tomlkit:-x all,tomlkit}
    %{?with_tests:-x test}
}}


%build
%pyproject_wheel

%if %{with manpages}
for page in doc/*.scd; do
    dest="${page%.scd}"
    scdoc <"${page}" >"${dest}"
done
%endif


%install
%pyproject_install
%pyproject_save_files tomcli

%if %{with manpages}
# Install manpages
install -Dpm 0644 doc/*.1 -t %{buildroot}%{_mandir}/man1
%endif

# Install shell completions
(
export %{py3_test_envvars}
%{python3} compgen.py \
    --installroot %{buildroot} \
    --bash-dir %{bash_completions_dir} \
    --fish-dir %{fish_completions_dir} \
    --zsh-dir %{zsh_completions_dir}
)


%check
# Smoke test
(
export %{py3_test_envvars}
TOMCLI="%{buildroot}%{_bindir}/tomcli"
cp pyproject.toml test.toml
name="$($TOMCLI get test.toml project.name)"
test "${name}" = "tomcli"

$TOMCLI set test.toml str project.name not-tomcli
newname="$($TOMCLI get test.toml project.name)"
test "${newname}" = "not-tomcli"
)

%pyproject_check_import
%if %{with tests}
%pytest
%endif


%pyproject_extras_subpkg -n tomcli %{?with_tomlkit:all tomlkit} tomli


%files -f %{pyproject_files}
%license LICENSE
%doc README.md
%doc NEWS.md
%{_bindir}/tomcli*
%{bash_completions_dir}/tomcli*
%{fish_completions_dir}/tomcli*.fish
%{zsh_completions_dir}/_tomcli*
%if %{with manpages}
%{_mandir}/man1/tomcli*.1*
%endif


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.10.1-3
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.10.1-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 31 2025 Maxwell G <maxwell@gtmx.me> - 0.10.1-1
- Update to 0.10.1.

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jun 06 2025 Maxwell G <maxwell@gtmx.me> - 0.10.0-1
- Update to 0.10.0.

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.9.0-2
- Rebuilt for Python 3.14

* Sun Mar 02 2025 Maxwell G <maxwell@gtmx.me> - 0.9.0-1
- Update to 0.9.0.

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 16 2024 Maxwell G <maxwell@gtmx.me> - 0.8.0-1
- Update to 0.8.0.

* Wed Aug 28 2024 Maxwell G <maxwell@gtmx.me> - 0.7.0-1
- Update to 0.7.0.

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.6.0-2
- Rebuilt for Python 3.13

* Thu Mar 28 2024 Maxwell G <maxwell@gtmx.me> - 0.6.0-1
- Update to 0.6.0.

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 22 2023 Maxwell G <maxwell@gtmx.me> - 0.5.0-2
- Fix installation of license files

* Thu Dec 14 2023 Maxwell G <maxwell@gtmx.me> - 0.5.0-1
- Update to 0.5.0.

* Thu Sep 07 2023 Maxwell G <maxwell@gtmx.me> - 0.3.0-1
- Update to 0.3.0.

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 0.1.2-2
- Rebuilt for Python 3.12

* Sat May 20 2023 Maxwell G <maxwell@gtmx.me> - 0.1.2-1
- Update to 0.1.2.

* Wed May 03 2023 Maxwell G <maxwell@gtmx.me> - 0.1.1-1
- Initial package. Closes rhbz#2186902.
