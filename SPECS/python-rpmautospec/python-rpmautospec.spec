## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 4;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Polyfill %%bcond() macro for platforms without it
%if 0%{!?bcond:1}
%define bcond() %[ (%2)\
    ? "%{expand:%%{!?_without_%{1}:%%global with_%{1} 1}}"\
    : "%{expand:%%{?_with_%{1}:%%global with_%{1} 1}}"\
]
%endif

# Set this to 1 when bootstrapping
%bcond bootstrap 0

%bcond tests 1
# Which packages to mask and which tests to do with native wrappers
%global wrapped_pkgs pygit2 rpm
%global wrappers_relevant_tests tests/rpmautospec/test_pkg_history.py tests/rpmautospec/subcommands/

# The pytest-xdist package is not available when bootstrapping or on RHEL
%bcond xdist %[%{without bootstrap} && %{undefined rhel}]

# Whether to build only the minimal package for RHEL buildroot
%bcond minimal %[%{defined rhel} && %{undefined epel}]

# While bootstrapping or building the minimal package, ignore manpages
%bcond manpages %[%{without bootstrap} && %{without minimal}]

# While building the minimal package, ignore shell completions
%bcond completions %{without minimal}

# Package the placeholder rpm-macros (moved to redhat-rpm-config in F40)
%if ! (0%{?fedora} >= 40 || 0%{?rhel} >= 10)
%bcond rpmmacropkg 1
%else
%bcond rpmmacropkg 0
%endif

# Appease old versions of hatchling
%if ! 0%{?fedora}%{?rhel} || 0%{?fedora} >= 41 || 0%{?rhel} >= 10
%bcond old_hatchling 0
%else
%bcond old_hatchling 1
%endif

# Although this supports a range of libgit2 and librpm versions upstream,
# we want to ensure newer versions don’t accidentally break all packages using this.
# Hence we artificially restrict the Required version to what was tested during the build.
# When libgit2/librpm soname is bumped, this package needs to be rebuilt (and tested).
%define libgit2_lower_bound 1.7
%define libgit2_upper_bound 1.10
%define libgit2_requires %(rpm -q --provides libgit2 | grep '^libgit2\.so\.' | sed 's/()(64bit)$//' | head -n 1)

%global srcname rpmautospec

Name: python-%{srcname}
Version: 0.8.3

%if %{with bootstrap}
Release: 0%{?dist}
%else
Release: %autorelease
%endif
Summary: Package and CLI tool to generate release fields and changelogs
License: MIT AND GPL-2.0-only WITH GCC-exception-2.0 AND (MIT OR GPL-2.0-or-later WITH GCC-exception-2.0)
URL: https://github.com/fedora-infra/%{srcname}
Source0: %{pypi_source %{srcname}}
Source1: rpmautospec.in

%if 0%{!?pyproject_files:1}
%global pyproject_files %{_builddir}/%{name}-%{version}-%{release}.%{_arch}-pyproject-files
%endif

BuildArch: noarch
BuildRequires: findutils
BuildRequires: git
# the langpacks are needed for tests
BuildRequires: glibc-langpack-de
BuildRequires: glibc-langpack-en

BuildRequires: python3-devel >= 3.9.0
# Needed to build man pages
%if %{with manpages}
BuildRequires: python3dist(click-man)
%endif

%if %{with tests}
# The dependencies needed for testing don’t get auto-generated.
BuildRequires: python3dist(pytest)
BuildRequires: python3dist(pyyaml)
%if %{with xdist}
BuildRequires: python3dist(pytest-xdist)
%endif
%endif

BuildRequires: sed

BuildRequires: (libgit2 >= %libgit2_lower_bound with libgit2 < %libgit2_upper_bound)
BuildRequires: rpm-libs
BuildRequires: rpm-build-libs

%global _description %{expand:
A package and CLI tool to generate RPM release fields and changelogs.}

%description %_description

%if %{without minimal}
%package -n python3-%{srcname}
Summary: %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %_description

%pyproject_extras_subpkg -n python3-%{srcname} click
%pyproject_extras_subpkg -n python3-%{srcname} pygit2
%pyproject_extras_subpkg -n python3-%{srcname} rpm
%pyproject_extras_subpkg -n python3-%{srcname} all
%endif

%package -n %{srcname}
Summary: CLI tool for generating RPM releases and changelogs

Provides: bundled(python3dist(rpmautospec)) = %{version}
Provides: bundled(python3dist(rpmautospec-core)) = %((rpm -q python3-rpmautospec-core --qf '%%{version}\n' || echo 0) | tail -n1)

%if "%libgit2_requires" != ""
Requires: (%{libgit2_requires}()(64bit) or %{libgit2_requires})
Suggests: %{libgit2_requires}()(64bit)
%else
Requires: this-is-broken-libgit2-missing-during-build
%endif
Requires: rpm-libs
Requires: rpm-build-libs

%if %{without minimal}
Recommends: python3-%{srcname} = %{version}-%{release}
Recommends: python3-%{srcname}+click = %{version}-%{release}
Recommends: python3-%{srcname}+pygit2 = %{version}-%{release}
Recommends: python3-%{srcname}+rpm = %{version}-%{release}
%endif

%description -n %{srcname}
CLI tool for generating RPM releases and changelogs

%if %{with rpmmacropkg}
%package -n rpmautospec-rpm-macros
Summary: Rpmautospec RPM macros for local rpmbuild
Requires: rpm

%description -n rpmautospec-rpm-macros
This package contains RPM macros with placeholders for building rpmautospec
enabled packages locally.
%endif

%generate_buildrequires
%pyproject_buildrequires %{!?with_minimal:-x all}

%prep
%autosetup -n %{srcname}-%{version}
%if %{with old_hatchling}
sed -i -e 's/license-files = \(\[.*\]\)/license-files = {globs = \1}/' pyproject.toml
%endif

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters
sed -i -e '/pytest-cov/d; /addopts.*--cov/d' pyproject.toml

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{srcname}

%if %{with manpages}
# Man pages
PYTHONPATH=%{buildroot}%{python3_sitelib} click-man rpmautospec
install -m755 -d %{buildroot}%{_mandir}/man1
install -m644 man/*.1 %{buildroot}%{_mandir}/man1
%endif

# RPM macros
%if %{with rpmmacropkg}
mkdir -p %{buildroot}%{rpmmacrodir}
install -m 644 rpm_macros.d/macros.rpmautospec %{buildroot}%{rpmmacrodir}/
%endif

%if %{with completions}
# Shell completion
for shell_path in \
        bash:%{bash_completions_dir}/rpmautospec \
        fish:%{fish_completions_dir}/rpmautospec.fish \
        zsh:%{zsh_completions_dir}/_rpmautospec; do
    shell="${shell_path%%:*}"
    path="${shell_path#*:}"
    dir="${path%/*}"

    install -m 755 -d "%{buildroot}${dir}"

    PYTHONPATH=%{buildroot}%{python3_sitelib} \
    _RPMAUTOSPEC_COMPLETE="${shell}_source" \
    %{__python3} -c \
    "import sys; sys.argv[0] = 'rpmautospec'; from rpmautospec.cli import cli; sys.exit(cli())" \
    > "%{buildroot}${path}"
done
%endif

# Fill in the real version for the fallback method
touch -r %{buildroot}%{python3_sitelib}/rpmautospec/version.py timestamp
sed -i -e 's|0\.0\.0|%{version}|g' %{buildroot}%{python3_sitelib}/rpmautospec/version.py
touch -r timestamp %{buildroot}%{python3_sitelib}/rpmautospec/version.py

# Install bootstrapping copies of rpmautospec, rpmautospec_core packages
mkdir -p %{buildroot}%{_datadir}/rpmautospec-fallback
cp -r %{python3_sitelib}/rpmautospec_core %{buildroot}%{_datadir}/rpmautospec-fallback/
cp -r %{buildroot}%{python3_sitelib}/rpmautospec %{buildroot}%{_datadir}/rpmautospec-fallback/
find %{buildroot}%{_datadir}/rpmautospec-fallback \
    -depth -type d -a -name __pycache__ -exec rm -r {} \;

# Override the standard executable with a custom one that knows how to fall back
sed -e 's|@PYTHON3@|%{python3} -%{py3_shebang_flags}|g; s|@DATADIR@|%{_datadir}|g' \
    < %{S:1} \
    > %{buildroot}%{_bindir}/rpmautospec
chmod 755 %{buildroot}%{_bindir}/rpmautospec
touch -r %{S:1} %{buildroot}%{_bindir}/rpmautospec

%check
# Always run the import checks, even when other tests are disabled
%pyproject_check_import %{?with_minimal:-e '*click*'}

%if %{with tests}
%if %{without minimal}
%pytest \
%if %{with xdist}
--numprocesses=auto
%endif
%endif

%if ! 0%{?rhel} || 0%{?rhel} >= 10
# And redo tests that are relevant for native bindings, but with the direct native wrappers, but not
# on EL <= 9 because the tests somehow run out of file descriptors.

# Poison the official package names…
mkdir -p poison-pill
for mod in %wrapped_pkgs; do
    echo "raise ImportError" > "poison-pill/${mod}.py"
    if PYTHONPATH="$PWD/poison-pill:$PYTHONPATH" %__python3 -c "import ${mod}" 2>/dev/null; then
        echo "Failed to poison-pill ${mod}!" >&2
        exit 1
    fi
done

%py3_test_envvars \
PYTHONPATH="$PWD/poison-pill:$PYTHONPATH" \
%__pytest \
%if %{with xdist}
--numprocesses=auto \
%endif
%wrappers_relevant_tests

%endif
%endif

%if %{without minimal}
%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst
%endif

%files -n %{srcname}
%{_bindir}/rpmautospec
%{_datadir}/rpmautospec-fallback

%if %{with manpages}
%{_mandir}/man1/rpmautospec*.1*
%endif
%if %{with completions}
%dir %{bash_completions_dir}
%{bash_completions_dir}/rpmautospec
%dir %{fish_completions_dir}
%{fish_completions_dir}/rpmautospec.fish
%dir %{zsh_completions_dir}
%{zsh_completions_dir}/_rpmautospec
%endif
%if %{with minimal}
%license licenses/*
%exclude %{python3_sitelib}
%endif

%if %{with rpmmacropkg}
%files -n rpmautospec-rpm-macros
%{rpmmacrodir}/macros.rpmautospec
%endif

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 0.8.3-4
- Latest state for python-rpmautospec

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.8.3-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Wed Sep 10 2025 Nils Philippsen <nils@redhat.com> - 0.8.3-1
- Update to 0.8.3

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.8.2-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 09 2025 Nils Philippsen <nils@redhat.com> - 0.8.2-1
- Update to 0.8.2

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.8.1-12
- Rebuilt for Python 3.14

* Wed Apr 16 2025 Miro Hrončok <miro@hroncok.cz> - 0.8.1-8
- Generate BuildRequires for extras, drop unused click-plugins dependency

* Wed Apr 16 2025 Miro Hrončok <miro@hroncok.cz> - 0.8.1-7
- On RHEL, only build the minimal package

* Wed Apr 16 2025 Miro Hrončok <miro@hroncok.cz> - 0.8.1-6
- Make sure only one libgit2 package is BuildRequired during the build

* Tue Apr 15 2025 Miro Hrončok <miro@hroncok.cz> - 0.8.1-5
- Add bundled() provides for bundled self and rpmautospec-core

* Tue Apr 15 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 0.8.1-4
- Drop pyproject_macros conditional

* Mon Apr 14 2025 Nils Philippsen <nils@redhat.com> - 0.8.1-2
- Pin libgit2 to soname version tested during build

* Tue Apr 08 2025 Nils Philippsen <nils@redhat.com> - 0.8.1-1
- Update to 0.8.1

* Tue Apr 08 2025 Miro Hrončok <miro@hroncok.cz> - 0.8.0-4
- Stop trying to Require libraries with %%_isa

* Tue Apr 08 2025 Miro Hrončok <miro@hroncok.cz> - 0.8.0-3
- Add missing flags to /usr/bin/rpmautospec shebang

* Tue Apr 08 2025 Nils Philippsen <nils@redhat.com> - 0.8.0-1
- Update to 0.8.0
- Update license
- Make using click, pygit2, rpm Python packages optional and enable
  fallbacks

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Oct 11 2024 Nils Philippsen <nils@redhat.com> - 0.7.3-1
- Update to 0.7.3

* Fri Sep 20 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 0.7.2-2
- Fix build without poetry

* Fri Aug 30 2024 Nils Philippsen <nils@redhat.com> - 0.7.2-1
- Update to 0.7.2

* Wed Aug 21 2024 Miro Hrončok <miro@hroncok.cz> - 0.7.1-3
- Bootstrap build: Remove a bogus changelog

* Tue Aug 20 2024 Stephen Gallagher <sgallagh@redhat.com> - 0.7.1-2
- Enable bootstrapping macros

* Tue Aug 13 2024 Nils Philippsen <nils@redhat.com> - 0.7.1-1
- Update to 0.7.1

* Mon Aug 12 2024 Nils Philippsen <nils@redhat.com> - 0.7.0-1
- Update to 0.7.0
- Split off man pages for sub-commands
- Ship scriptlets needed for shell completion

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 18 2024 Nils Philippsen <nils@redhat.com> - 0.6.5-1
- Update to 0.6.5

* Tue Jun 11 2024 Python Maint <python-maint@redhat.com> - 0.6.4-2
- Rebuilt for Python 3.13

* Mon Jun 10 2024 Nils Philippsen <nils@redhat.com> - 0.6.4-1
- Update to 0.6.4
- Install man page

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.6.3-2
- Rebuilt for Python 3.13

* Wed Feb 21 2024 Nils Philippsen <nils@redhat.com> - 0.6.3-1
- Update to 0.6.3

* Mon Feb 19 2024 Nils Philippsen <nils@redhat.com> - 0.6.2-1
- Update to 0.6.2

* Fri Feb 09 2024 Nils Philippsen <nils@redhat.com> - 0.6.1-1
- Update to 0.6.1

* Sat Jan 27 2024 Nils Philippsen <nils@redhat.com> - 0.6.0-1
- Update to 0.6.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 16 2024 Nils Philippsen <nils@redhat.com> - 0.5.1-1
- Update to 0.5.1

* Mon Jan 15 2024 Nils Philippsen <nils@redhat.com> - 0.5.0-1
- Update to 0.5.0

* Thu Jan 11 2024 Nils Philippsen <nils@redhat.com> - 0.4.2-1
- Update to 0.4.2

* Mon Jan 08 2024 Nils Philippsen <nils@redhat.com> - 0.4.1-2
- Update patch for old poetry versions

* Fri Dec 15 2023 Nils Philippsen <nils@redhat.com> - 0.4.1-1
- Update to 0.4.1

* Sun Dec 03 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 0.4.0-2
- Drop unwanted python-pytest-cov dependency

* Thu Nov 30 2023 Nils Philippsen <nils@redhat.com> - 0.4.0-1
- Update to 0.4.0

* Tue Nov 14 2023 Nils Philippsen <nils@redhat.com> - 0.3.8-1
- Update to 0.3.8

* Tue Nov 14 2023 Nils Philippsen <nils@redhat.com> - 0.3.7-1
- Update to 0.3.7

* Tue Nov 14 2023 Nils Philippsen <nils@redhat.com> - 0.3.6-1
- Update to 0.3.6

* Tue Aug 22 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 0.3.5-5
- Disable the macros subpackage in F40+

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 0.3.5-3
- Rebuilt for Python 3.12

* Wed May 24 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 0.3.5-2
- Avoid pytest-cov, disable xdist in RHEL builds

* Wed Feb 08 2023 Nils Philippsen <nils@redhat.com> - 0.3.5-1
- Update to 0.3.5

* Wed Feb 08 2023 Nils Philippsen <nils@redhat.com> - 0.3.4-1
- Update to 0.3.4

* Wed Feb 08 2023 Nils Philippsen <nils@redhat.com> - 0.3.3-1
- Update to 0.3.3

* Tue Jan 24 2023 Nils Philippsen <nils@redhat.com> - 0.3.2-1
- Update to 0.3.2

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Nov 11 2022 Nils Philippsen <nils@redhat.com> - 0.3.1-1
- Update to 0.3.1

* Wed Jul 27 2022 Nils Philippsen <nils@redhat.com> - 0.3.0-1
- Update to 0.3.0

* Wed Jun 08 2022 Nils Philippsen <nils@redhat.com>
- Generally BR: python3-pytest-xdist, also on EL9

* Mon May 16 2022 Nils Philippsen <nils@redhat.com> - 0.2.8-1
- Update to 0.2.8
- Don't require python3-pytest-xdist for building on EL9

* Mon May 16 2022 Nils Philippsen <nils@redhat.com> - 0.2.7-1
- Update to 0.2.7

* Mon Apr 25 2022 Nils Philippsen <nils@redhat.com> - 0.2.6-1
- Update to 0.2.6
- Require python3-pytest-xdist for building
- Remove EL7 quirks, pkg isn't built there

* Fri Mar 04 2022 Nils Philippsen <nils@redhat.com>
- require python3-pyyaml for building

* Sun Nov 07 2021 Nils Philippsen <nils@redhat.com>
- require python3-babel and glibc langpacks (the latter for testing)

* Fri Aug 06 2021 Nils Philippsen <nils@redhat.com> - 0.2.5-1
- Update to 0.2.5

* Thu Aug 05 2021 Nils Philippsen <nils@redhat.com> - 0.2.4-1
- Update to 0.2.4

* Wed Jun 16 2021 Nils Philippsen <nils@redhat.com> - 0.2.3-1
- Update to 0.2.3

* Fri Jun 04 2021 Nils Philippsen <nils@redhat.com> - 0.2.2-1
- Update to 0.2.2

* Thu May 27 2021 Nils Philippsen <nils@redhat.com> - 0.2.1-1
- Update to 0.2.1

* Thu May 27 2021 Stephen Coady <scoady@redhat.com> - 0.2.0-1
- Update to 0.2.0

* Thu May 27 2021 Nils Philippsen <nils@redhat.com>
- don't ship obsolete Koji configuration snippet

* Wed May 19 2021 Nils Philippsen <nils@redhat.com>
- remove git-core, fix RPM related dependencies

* Wed May 12 2021 Nils Philippsen <nils@redhat.com>
- depend on python3-pygit2

* Thu Apr 22 2021 Nils Philippsen <nils@redhat.com>
- remove the hub plugin

* Thu Apr 15 2021 Nils Philippsen <nils@redhat.com> - 0.1.5-1
- Update to 0.1.5
- Have lowercase URLs, because Pagure d'oh

* Thu Apr 15 2021 Nils Philippsen <nils@redhat.com> - 0.1.4-1
- Update to 0.1.4
- explicitly BR: python3-setuptools

* Thu Apr 09 2020 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.1.3-1
- Update to 0.1.3

* Thu Apr 09 2020 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.1.2-1
- Update to 0.1.2

* Thu Apr 09 2020 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.1.1-1
- Update to 0.1.1

* Thu Apr 09 2020 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.1.0-1
- Update to 0.1.0

* Wed Apr 08 2020 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.0.23-1
- Update to 0.023

* Wed Apr 08 2020 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.0.22-1
- Update to 0.0.22

* Wed Apr 08 2020 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.0.21-1
- Update to 0.0.21

* Wed Apr 08 2020 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.0.20-1
- Update to 0.0.20

* Wed Apr 08 2020 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.0.19-1
- Update to 0.0.19

* Wed Apr 08 2020 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.0.18-1
- Update to 0.0.18

* Tue Apr 07 2020 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.0.17-1
- Update to 0.0.17

* Tue Apr 07 2020 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.0.16-1
- Update to 0.0.16

* Tue Apr 07 2020 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.0.15-1
- Update to 0.0.15

* Tue Apr 07 2020 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.0.14-1
- Update to 0.0.14

* Tue Apr 07 2020 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.0.13-1
- Update to 0.0.13

* Tue Apr 07 2020 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.0.12-1
- Update to 0.0.12

* Mon Apr 06 2020 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.0.11-1
- Update to 0.0.11

* Fri Apr 03 2020 Nils Philippsen <nils@redhat.com> - 0.0.10-1
- Update to 0.0.10

* Fri Apr 03 2020 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.0.9-1
- Update to 0.0.9

* Fri Apr 03 2020 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.0.8-1
- Update to 0.0.8

* Fri Apr 03 2020 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.0.7-1
- Update to 0.0.7

* Thu Apr 02 2020 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.0.6-1
- Update to 0.0.6

* Tue Mar 31 2020 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.0.5-1
- Update to 0.0.5

* Tue Mar 31 2020 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.0.4-1
- Update to 0.0.4

* Tue Mar 31 2020 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.0.3-1
- Update to 0.0.3

* Tue Mar 31 2020 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.0.2-1
- Update to 0.0.2

* Wed Mar 18 2020  Adam Saleh <asaleh@redhat.com> - 0.0.1-1
- initial package for Fedora

## END: Generated by rpmautospec
