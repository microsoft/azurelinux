# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name trio-websocket
%global pypi_name_underscore %(echo "%{pypi_name}" | tr '-' '_')

Name: python-%{pypi_name}
Summary: WebSocket implementation focused on safety and correctness
License: MIT

Version: 0.12.2
Release: 5%{?dist}

URL: https://github.com/python-trio/trio-websocket
Source: %{URL}/archive/%{version}/%{pypi_name}-%{version}.tar.gz

BuildArch: noarch

BuildRequires: attr
BuildRequires: make
BuildRequires: pytest

BuildRequires: python3-devel
BuildRequires: python3-pytest-trio
BuildRequires: python3-sphinx
BuildRequires: python3-sphinx_rtd_theme
BuildRequires: python3-sphinxcontrib-trio
BuildRequires: python3-trustme

%global _description %{expand:
This library implements both server and client aspects of the the WebSocket
protocol, striving for safety, correctness, and ergonomics. It is based
on the wsproto project, which is a Sans-IO state machine that implements
the majority of the WebSocket protocol, including framing, codecs, and events.
This library handles I/O using the Trio framework.
This library passes the Autobahn Test Suite.
}

%description %_description

%package -n python3-%{pypi_name}
Summary: %{summary}

%description -n python3-%{pypi_name} %_description

%package doc
Summary: Documentation for %{pypi_name}
Provides: bundled(js-jquery)
Provides: bundled(nodejs-underscores)

%description doc
This package contains documentation (in HTML format)
for %{pypi_name}.


%prep
%autosetup -p1 -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel

export PYTHONPATH="$(pwd)"
%make_build -C docs html PYTHON=python3 BUILDDIR=build
rm docs/build/html/.buildinfo


%install
%pyproject_install
%pyproject_save_files %{pypi_name_underscore}


%check
%pyproject_check_import
%pytest


%files -n python3-%{pypi_name} -f %{pyproject_files}


%files doc
%license LICENSE
%doc docs/build/html


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.12.2-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.12.2-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.12.2-2
- Rebuilt for Python 3.14

* Tue Feb 25 2025 Artur Frenszek-Iwicki <fedora@svgames.pl> - 0.12.2-1
- Update to v0.12.2

* Tue Feb 18 2025 Artur Frenszek-Iwicki <fedora@svgames.pl> - 0.12.1-1
- Update to v0.12.1

* Mon Feb 17 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.0-1
- Update to 0.12.0 (close RHBZ#2346049)

* Tue Feb 11 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.0~dev^202501304247cd5-1
- Update to a snapshot for compatibility with trio>=0.25

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 0.11.1-5
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 04 2023 Artur Frenszek-Iwicki <fedora@svgames.pl> - 0.11.1-2
- Remove buildinfo file from -doc subpackage

* Mon Oct 02 2023 Artur Frenszek-Iwicki <fedora@svgames.pl> - 0.11.1-1
- Update to v0.11.1
- Drop Patch0 (remove "exceptiongroup" dependency - made optional by upstream)
- Add Provides for bundled JavaScript in the -doc subpackage
- Do not duplicate the LICENSE file in main package

* Thu Sep 21 2023 Artur Frenszek-Iwicki <fedora@svgames.pl> - 0.10.4-1
- Update to v0.10.4
- Fix LICENSE file missing from main package

* Wed Sep 13 2023 Artur Frenszek-Iwicki <fedora@svgames.pl> - 0.10.3-2
- Switch to using pyproject_xxx macros
- Build HTML documentation and add -doc subpackage
- Switch to using GitHub tarball as the source (needed for building the docs)

* Wed Sep 06 2023 Artur Frenszek-Iwicki <fedora@svgames.pl> - 0.10.3-1
- Initial packaging
