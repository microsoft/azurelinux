# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# See https://docs.fedoraproject.org/en-US/packaging-guidelines/#_compiler_macros
%global toolchain clang

%global nanobind_giturl https://github.com/wjakob/nanobind
%global nanobind_src_dir nanobind-%{version}

# The combination of an arched package with only noarch binary packages makes
# it easier for us to detect arch-dependent test failures, since the tests will
# always be run on every platform.
# Since the package still contains no compiled machine code, we still have no
# debuginfo.
%global debug_package %{nil}

Name:           python-nanobind
Version:        2.8.0
Release:        %autorelease
Summary:        Tiny and efficient C++/Python bindings

License:        BSD-3-Clause
URL:            https://nanobind.readthedocs.org/
VCS:            git:%{nanobind_giturl}.git
Source0:        %{nanobind_giturl}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  clang
BuildRequires:  cmake
BuildRequires:  eigen3-devel
BuildRequires:  librsvg2
BuildRequires:  ninja-build
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  robin-map-devel >= 1.3.0

%global _description %{expand:
nanobind is a small binding library that exposes C++ types
in Python and vice versa. It is reminiscent of Boost.Python
and pybind11 and uses near-identical syntax.
In contrast to these existing tools, nanobind is more
efficient: bindings compile in a shorter amount of time,
produce smaller binaries, and have better runtime performance.}

%description %_description

%package -n     python%{python3_pkgversion}-nanobind
Summary:        %{summary}
BuildArch:      noarch
Requires:       robin-map-devel >= 1.3.0
%py_provides    python%{python3_pkgversion}-nanobind-devel
Obsoletes:      python%{python3_pkgversion}-nanobind-devel < 2.6.1-4
%description -n python%{python3_pkgversion}-nanobind %_description


%prep
%autosetup -n %{nanobind_src_dir}
%py3_shebang_fix src/stubgen.py


%generate_buildrequires
%pyproject_buildrequires


%build
# See https://github.com/scikit-build/scikit-build-core?tab=readme-ov-file#configuration
%{pyproject_wheel: \
-C"build-dir=%{__cmake_builddir}" \
-C"cmake.define.NB_USE_SUBMODULE_DEPS=false" \
-C"cmake.build-type=RelWithDebInfo" \
-C"cmake.define.NB_TEST_SHARED_BUILD=false" \
-C"cmake.define.NB_TEST=true" \
-C"build.verbose=true" \
}

%install
%pyproject_install
%pyproject_save_files -L nanobind


%check
%pyproject_check_import
# Test files are not installed, hence we need
# to enter the build directory manually.
pushd %{__cmake_builddir}
%pytest
popd


%files -n python%{python3_pkgversion}-nanobind -f %{pyproject_files}
%license %{python3_sitelib}/nanobind-%{version}.dist-info/licenses/LICENSE
# Exclude not needed files
%exclude %{python3_sitelib}/nanobind/cmake/darwin-ld-cpython.sym
%exclude %{python3_sitelib}/nanobind/cmake/darwin-ld-pypy.sym


%changelog
%autochangelog
