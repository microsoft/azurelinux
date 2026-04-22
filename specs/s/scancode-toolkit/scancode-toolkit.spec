## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 12;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# This is built as an arched package, as its includes a cache as a Python
# pickle file which is apparently not an architecture-independent format (fails
# on s390x). Still, this needs does not produce any debug data.
%global debug_package %{nil}

%bcond tests 1

Name:           scancode-toolkit
Version:        32.4.1
Release:        %autorelease
Summary:        Scan code and detect licenses, copyrights, and more

# Apache-2.0: main program
# CC-BY-4.0: ScanCode datasets for license detection
License:        Apache-2.0 AND CC-BY-4.0
URL:            https://scancode-toolkit.readthedocs.io/
Source:         https://github.com/aboutcode-org/scancode-toolkit/archive/v%{version}/%{name}-%{version}.tar.gz

# TODO: Is this upstreamable?
Patch:          0001-tests-fix-pytest-traceback.patch
# See note in https://github.com/aboutcode-org/scancode-toolkit/issues/4541
# about why pkginfo2 was removed.
Patch:          0002-Replace-pkginfo2-with-pkginfo.patch
# Based on https://github.com/aboutcode-org/scancode-toolkit/pull/4539
Patch:          0003-packagedcode-don-t-use-removed-ast-module-attributes.patch
# Based on https://github.com/aboutcode-org/scancode-toolkit/pull/4532
Patch:          0004-packagedcode-replace-unmaintained-toml-with-tomllib-.patch

# scancode has dependencies that are not compatible with ix86
ExcludeArch:    %{ix86}

BuildRequires:  python3-devel
%if %{with tests}
BuildRequires:  python3dist(pytest)
%endif
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3dist(sphinx-copybutton)
BuildRequires:  python3dist(sphinx-reredirects)
BuildRequires:  python3dist(sphinx-rtd-theme)
BuildRequires:  tomcli

%global common_description %{expand:
ScanCode is an open-source tool to scan code and detect licenses, copyrights,
and more. It provides detailed information about discovered licenses,
copyrights, and other important details in various formats.}

%description %{common_description}

%package doc
Summary:        Documentation for python-%{name}
BuildArch:      noarch

%description doc
%{common_description}

This package is providing the documentation for %{name}.

%prep
%autosetup -p1
sed -i 's|\(fallback_version = "\)[^"]*|\1%{version}|' pyproject.toml
sed -Ei \
    -e '/doc8/d' \
    -e '/sphinx-rtd-dark-mode/d' \
    -e 's/Sphinx ==/Sphinx>=/' \
    -e 's|Beautifulsoup4\[chardet\]|Beautifulsoup4|' \
    -e '/sphinx-autobuild/d' \
    -e "s/^( *)(click .*);python_version<'3\.10'/\1\2/" \
    -e "/^ *click .*;python_version>='3\.10'/d" \
    -e 's/spdx_tools ==/spdx_tools ~=/' \
setup.cfg
sed -i '/"sphinx_rtd_dark_mode"/d' docs/source/conf.py
sed -i 's/JSON data/JSON text data/' tests/summarycode/data/todo/ignore_issue/invariant-2.2.4-expected.json

%generate_buildrequires
%pyproject_buildrequires -x docs

%build
# NOTE: Upstream's wheels include the license cache as a Python pickle, so
# let's build that here. Without this file, scancode tries to write the cache
# to site-packages itself which it doesn't have permissions for.
# TODO: Upstream's approach to caching is problematic.
# It treats pickles as a portable data format and tries to write a new cache to
# site-packages if the cache is invalid or does not exist.
# See https://github.com/aboutcode-org/scancode-toolkit/issues/3497.
# This should be fixed to prefer a user-writable cache directory.
PYTHONPATH="$(pwd)/src" %{python3} -m licensedcode.reindex
test -f src/licensedcode/data/cache/license_index/index_cache
%pyproject_wheel

# generate html docs
sphinx-build-3 -b html docs/source html
# remove the sphinx-build-3 leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%pyproject_install

%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

%if %{with tests}
# https://github.com/aboutcode-org/scancode-toolkit/issues/3496
mkdir -p venv/bin
ln -s %{buildroot}%{_bindir}/scancode venv/bin/regen-package-docs
ln -s %{buildroot}%{_bindir}/scancode venv/bin/scancode
ln -s %{buildroot}%{_bindir}/scancode venv/bin/scancode-license-data
ln -s %{buildroot}%{_bindir}/scancode venv/bin/scancode-reindex-licenses
# The tests expect that the directory of each file is added to sys.path, but
# this doesn't happen in importlib mode, so do it manually.
tomcli set pyproject.toml arrays str \
    tool.pytest.ini_options.pythonpath 'tests/packagedcode' 'tests/cluecode'
# The tests expect to be run from a source checkout.
export PYTHONPATH="$(pwd)/src"

# we use system libmagic 5.45 while upstream uses 5.39
# real failures start at test_is_licensing_works \
# to be reported upstream but probably some different library version somewhere too
# test_about_files: inside the venv we don't use
# Use importlib mode because some test files have the same filenames.
%pytest --import-mode importlib -vv -k '%{shrink:
    not test_json_pretty_print and not
        test_jsonlines and not
        test_json_compact and not
        test_json_with_extracted_license_statements and not
        test_yaml and not
        test_end_to_end_scan_with_license_policy and not
        test_scan_can_handle_weird_file_names and not
        test_scan_can_run_from_other_directory and not
        test_scan_produces_valid_yaml_with_extracted_license_statements and not
        test_classify_with_package_data and not
        test_consolidate_package and not
        test_consolidate_package_files_should_not_be_considered_in_license_holder_consolidated_component and not
        test_consolidate_component_package_from_json_can_run_twice and not
        test_consolidate_component_package_from_live_scan and not
        test_consolidate_package_always_include_own_manifest_file and not
        test_consolidate_component_package_build_from_live_scan and not
        test_end2end_todo_works_on_codebase_without_ambiguous_detections and not
        test_is_licensing_works and not
        test_parse_from_rb and not
        test_parse_from_rb_dependency_requirement and not
        test_scan_cli_works and not
        test_scan_cli_works_package_only and not
        test_package_command_scan_chef and not
        test_package_scan_pypi_end_to_end and not
        test_develop_with_parse and not
        test_develop_with_parse_metadata and not
        test_parse_with_eggfile and not
        test_parse_with_unpacked_wheel_meta and not
        test_parse_metadata_prefer_pkg_info_from_egg_info_from_command_line and not
        test_parse_dependency_file_with_invalid_does_not_fail and not
        test_recognize_rpmdb_sqlite and not
        test_collect_installed_rpmdb_xmlish_from_rootfs and not
        test_scan_system_package_end_to_end_installed_win_reg and not
        test_consolidate_report_minority_origin_directory and not
        test_about_files and not
        test_scan_works_on_rust_binary_with_inspector and not
        test_package_list_command and not
        test_get_file_info_include_size and not
        test_scan_cli_help and not
        %dnl 'sbin/fstrim' is a link to an absolute path
        %dnl These two are due to the tarfile module defaulting to the data filter in py3.14.
        %dnl Let upstream figure out what to do about this issue.
        test_can_get_installed_system_packages_with_license_from_alpine_container_layer and not
        test_can_scan_installed_system_package_in_alpine_container_layer and not
        %dnl These test failures have to do with the handling of tempfiles in the CLI
        %dnl and don't seem particularly important. Disable them for now
        test_scan_keep_temp_files_is_false_by_default and not
        test_scan_keep_temp_files_keeps_files and not
        %dnl https://github.com/aboutcode-org/scancode-toolkit/issues/4540
        test_license_reference_to_file_beside_package_manifest and not
        %dnl Add new entries above this line.
        placeholder}'
%endif

%files
%doc AUTHORS.rst CHANGELOG.rst CODE_OF_CONDUCT.rst
%doc CONTRIBUTING.rst README.rst ROADMAP.rst
%license NOTICE apache-2.0.LICENSE cc-by-4.0.LICENSE
%{_bindir}/scancode
%{_bindir}/scancode-license-data
%{_bindir}/scancode-reindex-licenses
# TODO: Should these extra utility binaries be included in the package?
# They are installed as console_scripts but may not be meant for end-user
# consumption.
%{_bindir}/add-required-phrases
%{_bindir}/gen-new-required-phrases-rules
%{_bindir}/regen-package-docs

%{python3_sitelib}/scancode_toolkit-*.dist-info/
%{python3_sitelib}/cluecode
%{python3_sitelib}/formattedcode
%{python3_sitelib}/licensedcode
%{python3_sitelib}/packagedcode
%{python3_sitelib}/scancode
%pycached %{python3_sitelib}/scancode_config.py
%{python3_sitelib}/summarycode
%{python3_sitelib}/textcode

%files doc
%doc html
%license NOTICE apache-2.0.LICENSE cc-by-4.0.LICENSE

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 32.4.1-12
- Latest state for scancode-toolkit

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 32.4.1-11
- Rebuilt for Python 3.14.0rc3 bytecode

* Wed Sep 17 2025 Robert-André Mauchin <eclipseo@mauchin.fr> - 32.4.1-10
- Fix the link

* Wed Sep 17 2025 Maxwell G <maxwell@gtmx.me> - 32.4.1-9
- Relax spdx-tools dependency pin

* Wed Sep 17 2025 Robert-André Mauchin <eclipseo@mauchin.fr> - 32.4.1-8
- Update project references

* Tue Sep 02 2025 Miro Hrončok <miro@hroncok.cz> - 32.4.1-7
- Unpin click to allow us to revert to click 8.1.7

* Sat Aug 30 2025 Maxwell G <maxwell@gtmx.me> - 32.4.1-6
- Refresh patches after submitting upstream.

* Sat Aug 30 2025 Maxwell G <maxwell@gtmx.me> - 32.4.1-3
- Add new binaries to package

* Sat Aug 30 2025 Maxwell G <maxwell@gtmx.me> - 32.4.1-2
- Backport python-toml -> tomllib patch. python-toml is deprecated.

* Sat Aug 30 2025 Maxwell G <maxwell@gtmx.me> - 32.4.1-1
- Update to 32.4.1. Fixes rhbz#2375106.

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 32.3.3-9
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Aug 06 2025 Maxwell G <maxwell@gtmx.me> - 32.3.3-8
- Remove spdx-tools dependency patch for now

* Wed Aug 06 2025 Maxwell G <maxwell@gtmx.me> - 32.3.3-6
- Refresh Python 3.14 support patches

* Wed Aug 06 2025 Maxwell G <maxwell@gtmx.me> - 32.3.3-5
- Relax spdx-tools dependency

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 32.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 11 2025 Maxwell G <maxwell@gtmx.me> - 32.3.3-3
- Remove sphinx-autobuild build dependency

* Tue Jun 10 2025 Maxwell G <maxwell@gtmx.me> - 32.3.3-2
- Replace pkginfo2 with pkginfo

* Tue Mar 25 2025 Maxwell G <maxwell@gtmx.me> - 32.3.3-1
- Update to 32.3.3. Fixes rhbz#2295723.

* Mon Mar 24 2025 Maxwell G <maxwell@gtmx.me> - 32.3.2-2
- Properly handle license cache

* Mon Mar 24 2025 Maxwell G <maxwell@gtmx.me> - 32.3.2-1
- Update to 32.3.2. Fixes rhbz#2295723.

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 32.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 32.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 21 2024 Robert-André Mauchin <zebob.m@gmail.com> - 32.2.0-1
- Update to 32.2.0

* Fri Jun 21 2024 Robert-André Mauchin <zebob.m@gmail.com> - 32.1.0-1
- Initial import
## END: Generated by rpmautospec
