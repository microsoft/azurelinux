%global _description %{expand:
A backwards/forwards-compatible fork of distutils.version.LooseVersion, for
times when PEP-440 isnt what you need.

The goal of this package is to be a drop-in replacement for the original
LooseVersion. It implements an identical interface and comparison logic to
LooseVersion. The only major change is that a looseversion.LooseVersion is
comparable to a distutils.version.LooseVersion, which means tools should not
need to worry whether all dependencies that use LooseVersion have migrated.

If you are simply comparing versions of Python packages, consider moving to
packaging.version.Version, which follows PEP-440. LooseVersion is better suited
to interacting with heterogeneous version schemes that do not follow PEP-440.}

Name:           python-looseversion
Version:        1.3.0
Release:        2%{?dist}
Summary:        Version numbering for anarchists and software realists

Vendor:         Microsoft Corporation
Distribution:   Azure Linux

License:        PSF-2.0
URL:            https://pypi.org/pypi/looseversion
Source0:        https://github.com/effigies/looseversion/archive/refs/tags/%{version}.tar.gz#/python-looseversion-%{version}.tar.gz

BuildArch:      noarch

%description %_description
%package -n python3-looseversion
Summary:        %{summary}
BuildRequires:  python3-devel
%if 0%{?with_check}
BuildRequires:  python3-pytest
%endif

BuildRequires:  python-rpm-macros
BuildRequires:  python3-hatchling
BuildRequires:  python3-packaging
BuildRequires:  python3-pathspec
BuildRequires:  python3-pluggy
BuildRequires:  python3-pip
BuildRequires:  python3-trove-classifiers

%description -n python3-looseversion %_description

%prep
%autosetup -n looseversion-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files looseversion
# Removing unpackaged license file - we add it through the %%license macro.
find %{buildroot}%{python3_sitelib} -name LICENSE -delete

%check
pip3 install iniconfig
%pytest -v tests.py

%files -n python3-looseversion -f %{pyproject_files}
%license LICENSE
%doc README.md CHANGES.md

%changelog
* Mon Mar 11 2024 corvus-callidus <108946721+corvus-callidus@users.noreply.github.com> - 1.3.0-2
- Initial Azure Linux import from Fedora 39 (license: MIT)
- License verified

* Mon Aug 14 2023 Packit <hello@packit.dev> - 1.3.0-1
- [packit] 1.3.0 upstream release

* Mon Aug 14 2023 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 1.2.0-5
- chore: add packit

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 14 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.2.0-3
- Avoid tox dependency

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 1.2.0-2
- Rebuilt for Python 3.12

* Fri Jun 09 2023 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 1.2.0-1
- feat: update to 1.2.0 (fixes rhbz#2210045)

* Wed Feb 22 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.2-1
- Update to 1.1.2 (close RHBZ#2172546)

* Tue Feb 21 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.1-1
- Update to 1.1.1 (close RHBZ#2171308)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jan 13 2023 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 1.0.3-4
- chore: upload sources (fixes rhbz#2160496)

* Fri Jan 13 2023 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 1.0.3-3
- feat: tweaks to prepare for import (fixes rbhz#2160496)

* Fri Jan 13 2023 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 1.0.3-2
- feat: ready for review

* Fri Jan 13 2023 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 1.0.3-1
- init
