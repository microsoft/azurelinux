Vendor:         Microsoft Corporation
Distribution:   Azure Linux

%global srcname Automat
%global pkgname automat

Name:           python-%{srcname}
Version:        24.8.1
Release:        1%{?dist}
Summary:        Self-service finite-state machines for the programmer on the go
License:        MIT
URL:            https://github.com/glyph/automat
Source0:        https://files.pythonhosted.org/packages/8d/2d/ede4ad7fc34ab4482389fa3369d304f2fa22e50770af706678f6a332fa82/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-wheel

%global common_description %{expand:
Automat is a library for concise, idiomatic Python expression of finite-state
automata (particularly deterministic finite-state transducers).}

%description %{common_description}

%package -n python3-%{srcname}
Summary:        %{summary}
# Lowercase alias so dependents can require python3-automat regardless of the
# upstream capitalized package name.
Provides:       python3-%{pkgname} = %{version}-%{release}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %{common_description}

%prep
%autosetup -p1 -n %{pkgname}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pkgname}

%check
# Exclude the optional submodules that import third-party libraries not needed
# for the core state-machine API: automat._visualize requires graphviz and
# automat._discover requires Twisted (both are visualize-only extras).
%pyproject_check_import -e '*._visualize' -e '*._discover'

%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.md
%{_bindir}/automat-visualize

%changelog
* Tue Jun 16 2026 Adit Jha <aditjha@microsoft.com> - 24.8.1-1
- Initial Azure Linux import from Fedora 43 (license: MIT).
- License verified.
- Drop the optional Sphinx/pydoctor documentation subpackage; build the library only.
