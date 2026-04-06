## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 15;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name extractcode

Name:           python-%{pypi_name}
Version:        31.0.0
Release:        %autorelease
Summary:        File extraction library and CLI tool to extract almost any archive

License:        Apache-2.0 AND MIT
URL:            https://github.com/aboutcode-org/extractcode
Source:         %url/archive/v%{version}/%{pypi_name}-%{version}.tar.gz
# setup.cfg: fix invalid version spec
Patch:          %url/commit/6270a8805c7fb964e545a56ca8a92829d240a96a.patch#/0001-Add-COC-to-redistributed-license-like-files.patch
# Replace unmaintained patch by patch-ng
# https://github.com/aboutcode-org/extractcode/pull/56
Patch:          %url/pull/55.patch#/0001-Use-patch-ng-fork-instead-of-unmaintained-patch.patch
# Usage of dash-separated 'console-scripts' is deprecated
# Use the underscore name 'console_scripts' instead.
# https://github.com/aboutcode-org/extractcode/pull/56
Patch:          %url/pull/56.patch#/0001-Usage-of-dash-separated-console-scripts-is-deprecate.patch

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3dist(sphinx-rtd-theme)
BuildRequires:  python3dist(extractcode-7z-system-provided)
BuildRequires:  python3dist(extractcode-libarchive-system-provided)
BuildRequires:  python3dist(typecode-libmagic-system-provided)
BuildRequires:  p7zip-plugins
%if 0%{?fedora} >= 43
# The tests only work with p7zip-plugins from the p7zip package
BuildConflicts: 7zip
%endif

%global common_description %{expand:
A mostly universal file extraction library and CLI tool to extract almost any
archive in a reasonably safe way on Linux, macOS and Windows.}

%description %{common_description}

%package -n python3-%{pypi_name}
Summary:        %{summary}
Recommends:     python3dist(extractcode-7z-system-provided)
Recommends:     python3dist(extractcode-libarchive-system-provided)
Recommends:     python3dist(typecode-libmagic-system-provided)

%description -n python3-%{pypi_name} %{common_description}

%pyproject_extras_subpkg -n python3-%{pypi_name} full

%package -n python-%{pypi_name}-doc
Summary:        Documentation for python-%{pypi_name}
# BSD-2-Clause: Sphinx javascript
# MIT: jquery
License:        Apache-2.0 AND BSD-2-Clause AND MIT
BuildArch:      noarch
Requires:       python3-%{pypi_name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       bundled(js-sphinx_javascript_frameworks_compat)
Provides:       bundled(js-doctools)
Provides:       bundled(js-jquery)
Provides:       bundled(js-language_data)
Provides:       bundled(js-searchtools)

%description -n python-%{pypi_name}-doc
%{common_description}

This package is providing the documentation for %{pypi_name}.

%prep
%autosetup -p1 -n %{pypi_name}-%{version}
sed -i 's|\(fallback_version = "\)[^"]*|\1%{version}|' pyproject.toml
sed -i 's|extractcode-7z >= 16.5.210525|extractcode-7z-system-provided|' setup.cfg
sed -i 's|extractcode_libarchive >= 3.5.1.210525|extractcode_libarchive-system-provided|' setup.cfg

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

# generate html docs
sphinx-build-3 -b html docs/source html
# remove the sphinx-build-3 leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

%check
# TestExtractVmImage needs access to kernel
# Then https://github.com/aboutcode-org/extractcode/issues/53
%pytest -k %{shescape:%{shrink:
        not estExtractVmImage
    and not test_get_extractor_qcow2
    and not test_extract_rar_with_trailing_data
    and not test_extractcode_command_can_take_an_empty_directory
    and not test_extractcode_command_does_extract_verbose
    and not test_extractcode_command_always_shows_something_if_not_using_a_tty_verbose_or_not
    and not test_extractcode_command_works_with_relative_paths
    and not test_extractcode_command_works_with_relative_paths_verbose
    and not test_usage_and_help_return_a_correct_script_name_on_all_platforms
    and not test_extractcode_command_can_extract_archive_with_unicode_names_verbose
    and not test_extractcode_command_can_extract_archive_with_unicode_names
    and not test_extractcode_command_can_extract_shallow
    and not test_extractcode_command_can_ignore
    and not test_extractcode_command_does_not_crash_with_replace_originals_and_corrupted_archives
    and not test_extractcode_command_can_extract_nuget
    and not test_get_extractors_2
}}

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc AUTHORS.rst CHANGELOG.rst CODE_OF_CONDUCT.rst README.rst
%{_bindir}/extractcode

%files -n python-%{pypi_name}-doc
%doc html
%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 31.0.0-15
- Latest state for python-extractcode

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 31.0.0-14
- Rebuilt for Python 3.14.0rc3 bytecode

* Wed Sep 17 2025 Robert-André Mauchin <eclipseo@mauchin.fr> - 31.0.0-13
- Update project references

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 31.0.0-12
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 31.0.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 11 2025 Python Maint <python-maint@redhat.com> - 31.0.0-7
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 31.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 31.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 31.0.0-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 31.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 31.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Nov 02 2023 Robert-André Mauchin <zebob.m@gmail.com> - 31.0.0-1
- Initial import
## END: Generated by rpmautospec
