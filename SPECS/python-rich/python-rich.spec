Name:           python-rich
Version:        13.7.1
Release:        4%{?dist}
Summary:        Render rich text and beautiful formatting in the terminal
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
License:        MIT
URL:            https://github.com/Textualize/rich
Source0:        %{url}/archive/v%{version}/rich-%{version}.tar.gz

BuildArch:      noarch

Patch0:         3229.patch
Patch1:         ptest-warning.patch 

BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-attrs
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
BuildRequires:  python3-poetry
BuildRequires:  python3-setuptools
%if 0%{?with_check}
BuildRequires:  python3-markdown-it-py
%endif

%description
Rich is a Python library for rich text and beautiful formatting in the terminal.
The Rich API makes it easy to add color and style to terminal output. Rich can
also render pretty tables, progress bars, markdown, syntax highlighted source
code, tracebacks, and more — out of the box.

%package -n     python3-rich
Summary:        %{summary}
Requires:       python3-markdown-it-py
Requires:       python3-pygments
Requires:       python3-typing-extensions
# This was previously misnamed, remove the obsolete in Fedora 38, EPEL 10
Obsoletes:      python-rich < 10.16.1-2

%description -n python3-rich
Rich is a Python library for rich text and beautiful formatting in the terminal.
The Rich API makes it easy to add color and style to terminal output. Rich can
also render pretty tables, progress bars, markdown, syntax highlighted source
code, tracebacks, and more — out of the box.

%prep
%autosetup -p1 -n rich-%{version}

%build
%pyproject_wheel
%install
%pyproject_install
%pyproject_save_files rich

%check
# add below to make sure initial build will catch runtime import errors
pip3 install iniconfig
%pyproject_check_import
%pytest -vv

%files -n python3-rich -f %{pyproject_files}
%license LICENSE
%doc README.md

%changelog
* Mon May 13 2024 Sam Meluch <sammeluch@microsoft.com> - 13.7.1-4 
- Add missing iniconfig dependency to check section

* Fri May 10 2024 Riken Maharjan <rmaharjan@microsoft.com> - 13.7.1-3
- Fix pygments name in Requires.

* Thu Mar 28 2024 Riken Maharjan <rmaharjan@microsoft.com> - 13.7.1-2
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Thu Mar 14 2024 Parag Nemade <pnemade@fedoraproject.org> - 13.7.1-1
- local build

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 13.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 13.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Dec 12 2023 Karolina Surma <ksurma@redhat.com> - 13.7.0-3
- Skip tests failing with Python 3.13

* Tue Nov 21 2023 Parag Nemade <pnemade@fedoraproject.org> - 13.7.0-2
- Remove upstreamed patch

* Thu Nov 16 2023 Parag Nemade <pnemade@fedoraproject.org> - 13.7.0-1
- local build

* Sun Oct 08 2023 Parag Nemade <pnemade@fedoraproject.org> - 13.6.0-1
- local build

* Mon Sep 18 2023 Parag Nemade <pnemade@fedoraproject.org> - 13.5.3-1
- Update to 13.5.3 version (#2239337)

* Thu Aug 03 2023 Parag Nemade <pnemade@fedoraproject.org> - 13.5.2-1
- Update to 13.5.2 version (#2227446)

* Fri Jul 21 2023 Parag Nemade <pnemade@fedoraproject.org> - 13.4.2-3
- Mark this as SPDX license expression converted

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 13.4.2-2
- Rebuilt for Python 3.12

* Tue Jun 20 2023 Parag Nemade <pnemade@fedoraproject.org> - 13.4.2-1
- local build

* Fri May 19 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 13.3.5-3
- Backport upstream patch to fix failing tests with Python 3.12

* Wed May 10 2023 Parag Nemade <pnemade@fedoraproject.org> - 13.3.5-2
- tests are running successfully now so revert skipping some tests

* Fri Apr 28 2023 Parag Nemade <pnemade@fedoraproject.org> - 13.3.5-1
- local build

* Mon Apr 10 2023 Parag Nemade <pnemade@fedoraproject.org> - 13.3.3-3
- Add new manual BR: python3-attrs for new update pytest-7.3.0

* Wed Mar 29 2023 Parag Nemade <pnemade@fedoraproject.org> - 13.3.3-2
- Add missing BR:python3-setuptools for executing tests

* Wed Mar 29 2023 Parag Nemade <pnemade@fedoraproject.org> - 13.3.3-1
- local build

* Tue Mar 07 2023 Parag Nemade <pnemade@fedoraproject.org> - 13.3.2-1
- local build

* Mon Jan 30 2023 Parag Nemade <pnemade@fedoraproject.org> - 13.3.1-1
- local build

* Mon Jan 23 2023 Parag Nemade <pnemade@fedoraproject.org> - 13.2.0-1
- local build

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 13.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 02 2023 Parag Nemade <pnemade@fedoraproject.org> - 13.0.0-1
- local build

* Mon Oct 17 2022 Miro Hrončok <miro@hroncok.cz> - 12.6.0-2
- Remove superfluous build-time dependency on python3-toml

* Mon Oct 03 2022 Parag Nemade <pnemade@fedoraproject.org> - 12.6.0-1
- local build

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 12.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 12 2022 Parag Nemade <pnemade@fedoraproject.org> - 12.5.1-1
- local build

* Sat Jul 09 2022 Parag Nemade <pnemade@fedoraproject.org> - 12.4.4-4
- Add %pyproject_check_import to detect runtime errors

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 12.4.4-3
- Rebuilt for Python 3.11

* Thu Jun 02 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 12.4.4-2
- Temporarily disable some test so package builds with Python 3.11

* Tue May 31 2022 Parag Nemade <pnemade@fedoraproject.org> - 12.4.4-1
- local build

* Fri May 13 2022 Parag Nemade <pnemade@fedoraproject.org> - 12.4.1-2
- Remove upstreamed patch

* Fri May 13 2022 Parag Nemade <pnemade@fedoraproject.org> - 12.4.1-1
- local build

* Wed May 11 2022 Charalampos Stratakis <cstratak@redhat.com> - 12.3.0-2
- Fix a test case with Pygments 2.12.0

* Wed Apr 27 2022 Parag Nemade <pnemade@fedoraproject.org> - 12.3.0-1
- local build

* Tue Apr 12 2022 Parag Nemade <pnemade@fedoraproject.org> - 12.2.0-1
- local build

* Wed Mar 23 2022 Parag Nemade <pnemade@fedoraproject.org> - 12.0.1-1
- local build
