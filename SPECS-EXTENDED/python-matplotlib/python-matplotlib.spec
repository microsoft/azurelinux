Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global srcname matplotlib

Name:           python-%{srcname}
Version:        3.9.4
Release:        1%{?dist}
Summary:        Python plotting package

License:        matplotlib
URL:            https://matplotlib.org
# Pinned to the 3.9 series, the last that builds against Azure Linux's
# pybind11 2.11 (matplotlib 3.10+ requires pybind11 >= 2.13.2 and uses the
# 3-argument PYBIND11_MODULE form).
Source0:        https://files.pythonhosted.org/packages/df/17/1747b4154034befd0ed33b52538f5eb7752d05bb51c5e2a31470c3bc7d52/%{srcname}-%{version}.tar.gz

# NOTE: matplotlib is a compiled (meson-python) package. In addition to the
# build tooling pulled in by %%pyproject_buildrequires (meson-python, pybind11,
# setuptools_scm, numpy) it requires the C/C++ toolchain and the system FreeType
# and libpng development libraries below. Its runtime dependencies
# (contourpy, cycler, fonttools, kiwisolver, pillow, python-dateutil, numpy,
# packaging, pyparsing) are all packaged in the distro.
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig
BuildRequires:  freetype-devel
BuildRequires:  libpng-devel
BuildRequires:  qhull-devel
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  python3-meson-python
BuildRequires:  python3-pyproject-metadata
BuildRequires:  python3-packaging
BuildRequires:  python3-pybind11
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-numpy

%global _description %{expand:
Matplotlib is a comprehensive library for creating static, animated, and
interactive visualizations in Python. It produces publication-quality figures
in a variety of formats and interactive environments across platforms.}

%description %_description

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{srcname}-%{version}

%generate_buildrequires
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
# Link the system FreeType and qhull rather than letting meson download and
# vendor them (the build chroot has no network access).
%pyproject_buildrequires -C setup-args=-Dsystem-freetype=true -C setup-args=-Dsystem-qhull=true

%build
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_wheel -C setup-args=-Dsystem-freetype=true -C setup-args=-Dsystem-qhull=true

%install
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_install
%pyproject_save_files matplotlib mpl_toolkits pylab

%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE/*
%doc README.md

%changelog
* Wed Jun 03 2026 Andy Zaugg <azaugg@linkedin.com> - 3.9.4-1
- Initial Azure Linux import from the source project (license: same as "License" tag).
- License verified.
