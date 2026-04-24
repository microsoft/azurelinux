# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond tests 1

# Package an unreleased snapshot to fix Python 3.14 issues,
# https://github.com/python-pendulum/pendulum/issues/900.
%global commit 628fd8510a8956647beedc685c0f0b6bfdc1eeec
%global snapdate 20251024

Name:           python-pendulum
Version:        3.2.0~dev0^%{snapdate}git%{sub %{commit} 1 7}
Release: 2%{?dist}
Summary:        Python datetimes made easy

License:        MIT
URL:            https://pendulum.eustace.io
%global forgeurl https://github.com/sdispater/pendulum
# Source:         %%{forgeurl}/archive/%%{version}/pendulum-%%{version}.tar.gz
Source:         %{forgeurl}/archive/%{commit}/pendulum-%{commit}.tar.gz

# Downstream-only: allow PyO3 0.26 until we have 0.27, RHBZ#2404994
Patch:          0001-Allow-PyO3-0.26-until-we-have-0.27-RHBZ-2404994.patch

BuildRequires:  python3-devel
BuildRequires:  cargo-rpm-macros
BuildRequires:  tomcli
BuildRequires:  tzdata

%if %{with tests}
# Even though there is now a [test] extra, some test dependencies are still
# only listed in [tool.poetry.group.test.dependencies].
BuildRequires:  %{py3_dist pytest}
%endif

%global common_description %{expand:
Unlike other datetime libraries for Python, Pendulum is a drop-in replacement
for the standard datetime class (it inherits from it), so, basically, you can
replace all your datetime instances by DateTime instances in you code.

It also removes the notion of naive datetimes: each Pendulum instance is
timezone-aware and by default in UTC for ease of use.}

%description %{common_description}

%package -n     python3-pendulum
Summary:        %{summary}
# Rust crates compiled into the executable contribute additional license terms.
# To obtain the following list of licenses, build the package and note the
# output of %%{cargo_license_summary}.
#
# MIT
# MIT OR Apache-2.0
License:        %{license} AND (MIT OR Apache-2.0)

Requires:       tzdata

%description -n python3-pendulum %{common_description}

%prep
%autosetup -n pendulum-%{commit} -p1
# Remove tzdata dependency. We can rely on a system-wide timezone database.
tomcli-set pyproject.toml lists delitem project.dependencies 'tzdata.*'
# Remove pytest-benchmark dependency. We don't care about it in RPM builds.
sed -i '/@pytest.mark.benchmark/d' $(find tests -type f -name '*.py')
%cargo_prep
cd rust
rm Cargo.lock
# Remove unpackaged feature. This is only needed for Windows.
tomcli-set Cargo.toml lists delitem dependencies.pyo3.features \
    'generate-import-lib'

%generate_buildrequires
# For unclear reasons, maturin checks for all crate dependencies when it is
# invoked as part of %%pyproject_buildrequires – including those corresponding
# to optional features.
#
# Since maturin always checks for dev-dependencies, we need -t so that they are
# generated even when the “check” bcond is disabled.
pushd rust >/dev/null
%cargo_generate_buildrequires -t
popd >/dev/null
%pyproject_buildrequires %{?with_tests:-x test}

%build
export RUSTFLAGS=%{shescape:%build_rustflags}

pushd rust
%cargo_license_summary
%{cargo_license} > ../LICENSES.dependencies
popd

%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l pendulum

%check
%pyproject_check_import
%if %{with tests}
%pytest
%endif

%files -n python3-pendulum -f %{pyproject_files}
%doc README.rst

%changelog
* Tue Oct 28 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 3.2.0~dev0^20251024git628fd85-1
- Update to an unreleased snapshot with Python 3.14 support

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.1.0-4
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.1.0-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 3.1.0-1
- Update to 3.1.0 (close RHBZ#2361121)

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 3.0.0-6
- Rebuilt for Python 3.14

* Tue Jan 21 2025 Fabio Valentini <decathorpe@gmail.com> - 3.0.0-5
- Backport support for PyO3 0.22 and Python 3.13.

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 3.0.0-2
- Rebuilt for Python 3.13

* Mon Feb 05 2024 Maxwell G <maxwell@gtmx.me> - 3.0.0-1
- Update to 3.0.0. Fixes rhbz#2147455.

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jul 25 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2.1.2-12
- Add setuptools BR for distutils in Python 3.12

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jul 02 2023 Python Maint <python-maint@redhat.com> - 2.1.2-10
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 2.1.2-7
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.1.2-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Sep 07 2020 Fabian Affolter <mail@fabian-affolter.ch> - 2.1.2-2
- Update build workflow

* Sun Aug 09 2020 Fabian Affolter <mail@fabian-affolter.ch> - 2.1.2-1
- Update to new upstream release 2.1.2 (#1876673)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.0.5-4
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 21 2020 Fabian Affolter <mail@fabian-affolter.ch> - 2.0.5-2
- Fix description (rhbz#1790074)

* Tue Jan 07 2020 Fabian Affolter <mail@fabian-affolter.ch> - 2.0.5-1
- Initial package for Fedora
