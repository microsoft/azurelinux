%global pypi_name boltons
Summary:        Functionality that should be in the standard library
Name:           python-boltons
Version:        25.0.0
Release:        2%{?dist}
License:        BSD-3-Clause
URL:            https://github.com/mahmoud/boltons
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:         %{pypi_source}
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  make
BuildRequires:  python3-sphinx
BuildRequires:  python3-pip
BuildRequires:  python3-flit-core
%global _description %{expand:
Boltons is a set of over 230 BSD-licensed, pure-Python utilities in the same
spirit as — and yet conspicuously missing from — the standard library,
including:

 * Atomic file saving, bolted on with fileutils
 * A highly-optimized OrderedMultiDict, in dictutils
 * Two types of PriorityQueue, in queueutils
 * Chunked and windowed iteration, in iterutils
 * Recursive data structure iteration and merging, with iterutils.remap
 * Exponential backoff functionality, including jitter, through
   iterutils.backoff
 * A full-featured TracebackInfo type, for representing stack traces, in
   tbutils}

%description %_description

%package -n python3-boltons
Summary:        %{summary}

%description -n python3-boltons %_description


%prep
%autosetup -p1 -n boltons-%{version}

%build
%pyproject_wheel
export READTHEDOCS=True
make -C docs man

%install
%pyproject_install
mkdir -p %{buildroot}%{_mandir}/man1
install -m644 docs/_build/man/boltons.1 %{buildroot}%{_mandir}/man1/
%pyproject_save_files boltons

%check
%pytest -v


%files -n python3-boltons -f %{pyproject_files}
%doc CHANGELOG.md README.md TODO.rst
%{_mandir}/man1/boltons.1*


%changelog
* Wed Feb 26 2025 Riken Maharjan <rmaharjan@microsoft.com> - 25.0.0-2
- Initial Azure Linux import from Fedora 40 (license: MIT)
- License Verified

* Mon Feb 03 2025 Orion Poplawski <orion@nwra.com> - 25.0.0-1
- Update to 25.0.0

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 24.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 24.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 24.0.0-2
- Rebuilt for Python 3.13

* Sat Apr 06 2024 Orion Poplawski <orion@nwra.com> - 24.0.0-1
- Update to 24.0.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 29 2023 Orion Poplawski <orion@nwra.com> - 23.1.1-2
- Build man page

* Tue Nov 28 2023 Orion Poplawski <orion@nwra.com> - 23.1.1-1
- Initial Fedora package