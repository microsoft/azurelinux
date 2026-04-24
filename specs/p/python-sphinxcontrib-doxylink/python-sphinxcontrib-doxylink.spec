# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:      python-sphinxcontrib-doxylink
Version:   1.13.0
Release: 7%{?dist}
Summary:   A Sphinx extension to link to external Doxygen API documentation
License:   BSD-2-Clause
URL:       https://github.com/sphinx-contrib/doxylink
Source0:   https://github.com/sphinx-contrib/doxylink/archive/refs/tags/%{version}.tar.gz
BuildArch: noarch

BuildRequires: doxygen
BuildRequires: python3-devel
BuildRequires: python3-pyparsing
BuildRequires: python3-pytest
BuildRequires: python3-sphinx
BuildRequires: python3-testfixtures

%global _description %{expand:
This package contains a Sphinx extension to link to external Doxygen API
documentation. It allows you to specify C++ symbols and it will convert
them into links to the HTML page of their Doxygen documentation.}

%description %_description

%package -n python3-sphinxcontrib-doxylink
Summary: %{summary}

%description -n python3-sphinxcontrib-doxylink %_description

%prep
%autosetup -n doxylink-%{version} -p1

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -L sphinxcontrib

%check
%pyproject_check_import
%{pytest}

%files -n python3-sphinxcontrib-doxylink -f %{pyproject_files}
%license LICENSE
%doc README.rst

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.13.0-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Thu Sep 04 2025 Milan Zamazal <mzamazal@redhat.com> - 1.13.0-5
- Name changed to python-sphinxcontrib-doxylink.
- Redundant Requires removed.

* Wed Aug 27 2025 Milan Zamazal <mzamazal@redhat.com> - 1.13.0-4
- Build-require python3-devel to fix directory owners

* Fri Aug 15 2025 Milan Zamazal <mzamazal@redhat.com> - 1.13.0-3
- Fix of a macro reference in changelog

* Thu Aug 14 2025 Milan Zamazal <mzamazal@redhat.com> - 1.13.0-2
- Missing `dist' macro added to Release

* Mon Aug 11 2025 Milan Zamazal <mzamazal@redhat.com> - 1.13.0-1
- Initial package
