# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Sphinx-generated HTML documentation is not suitable for packaging; see
# https://bugzilla.redhat.com/show_bug.cgi?id=2006555 for discussion.
#
# We can generate PDF documentation as a substitute.
%bcond doc_pdf 1
# Test with XWayland, instead of X11?
%bcond wayland %{undefined el9}

Name:           python-pyperclip
Version:        1.9.0
Release: 6%{?dist}
Summary:        A cross-platform clipboard module for Python

License:        BSD-3-Clause
URL:            https://github.com/asweigart/pyperclip
Source:         %{pypi_source pyperclip}

# Fix test suite for release 1.9.0
# https://github.com/asweigart/pyperclip/pull/270
Patch:          pyperclip-1.9.0-tests.patch

BuildArch:      noarch

BuildRequires:  dos2unix

# While upstream runs tests directly with Python/unittest, using pytest as the
# runner allows us to more easily skip tests.
BuildRequires:  python3dist(pytest)

# Support graphical tests in non-graphical environment
%if %{with wayland}
BuildRequires:  xwayland-run
%else
BuildRequires:  xorg-x11-server-Xvfb
%endif

# TestQt (module PyQt5.QtWidgets)
BuildRequires:  python3dist(pyqt5)

# TestXClip (executable xclip)
BuildRequires:  /usr/bin/xclip

# TestXSel (executable xsel)
# These tests *can* pass, but some of them are flaky. It would be nice to
# figure out why.
# BuildRequires:  /usr/bin/xsel

%if %{with wayland}
# TestWlClipboard (executables wl-copy/wl-paste)
# This only works in a Wayland session; otherwise, we get:
#   error: XDG_RUNTIME_DIR is invalid or not set in the environment.
#   Failed to connect to a Wayland server: No such file or directory
#   Note: WAYLAND_DISPLAY is unset (falling back to wayland-0)
BuildRequires:  /usr/bin/wl-copy
BuildRequires:  /usr/bin/wl-paste
%endif

# TestKlipper (executables klipper and qdbus)
# These would fail with:
#   Could not connect to D-Bus server:
#   org.freedesktop.DBus.Error.Spawn.ExecFailed: /usr/bin/dbus-launch
#   terminated abnormally without any error message
# and besides, klipper is not present in Fedora 40 and later.
# BuildRequires:  /usr/bin/klipper
# BuildRequires:  /usr/bin/qdbus

%global common_description %{expand:
Pyperclip is a cross-platform Python module for copy and paste clipboard
functions.}

%description %{common_description}


%package -n     python3-pyperclip
Summary:        %{summary}

%description -n python3-pyperclip %{common_description}


%package -n python-pyperclip-doc
Summary:        Pyperclip documentation

%if %{with doc_pdf}
BuildRequires:  make
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3-sphinx-latex
BuildRequires:  latexmk
%endif

%description -n python-pyperclip-doc
Documentation for pyperclip


%prep
%autosetup -p1 -n pyperclip-%{version}
dos2unix --keepdate AUTHORS.txt CHANGES.txt README.md docs/*


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel

%if %{with doc_pdf}
PYTHONPATH="${PWD}/src" %make_build -C docs latex \
    SPHINXOPTS='-j%{?_smp_build_ncpus}'
%make_build -C docs/_build/latex LATEXMKOPTS='-quiet'
%endif


%install
%pyproject_install
%pyproject_save_files -l pyperclip


%check
%pyproject_check_import

%if %{with wayland}
%global __pytest /usr/bin/xwfb-run -- pytest
%else
%global __pytest /usr/bin/xvfb-run -a %{python3} -m pytest
%endif
# Explicitly skip backends that we know will fail in the mock environment if
# their dependencies happen to be present. See notes in the BuildRequires.
k="${k-}${k+ and }not TestKlipper"
k="${k-}${k+ and }not TestWlCLipboard"
k="${k-}${k+ and }not TestXSel"
%pytest -k "${k-}" -v


%files -n python3-pyperclip -f %{pyproject_files}
%doc AUTHORS.txt
%doc CHANGES.txt
%doc README.md


%files -n python-pyperclip-doc
%license LICENSE.txt
%if %{with doc_pdf}
%doc docs/_build/latex/Pyperclip.pdf
%endif


%changelog
* Thu Sep 10 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 1.9.0-2
- Port to pyproject-rpm-macros (fix RHBZ#2378068)
- Let the EPEL8 branch diverge

* Thu Sep 10 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 1.9.0-1
- Update to 1.9.0
- Use xwayland-run for tests where we can
- Also fix end-of-line encodings in AUTHORS.txt and CHANGES.txt

* Thu Jul 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_45_Mass_Rebuild

* Thu Jun 04 2026 Python Maint <python-maint@redhat.com> - 1.8.2-17
- Rebuilt for Python 3.15

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.8.2-15
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.8.2-14
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.8.2-12
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.8.2-9
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 16 2023 Python Maint <python-maint@redhat.com> - 1.8.2-5
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 29 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.8.2-3
- Update License to SPDX

* Fri Aug 12 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.8.2-2
- Enable running most of the graphical tests
- Switch Sphinx documentation to PDF to sidestep guidelines issues

* Mon Aug 08 2022 Jonathan Wright <jonathan@almalinux.org> - 1.8.2-1
- Update to 1.8.2

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.8.0-7
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.8.0-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 16 2020 Ken Dreyer <kdreyer@redhat.com> - 1.8.0-1
- Update to 1.8.0 (rhbz#1697423)
- Use non-git autosetup for simplicity

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.6.4-8
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.6.4-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.6.4-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Mar 17 2019 Miro Hrončok <mhroncok@redhat.com> - 1.6.4-3
- Subpackage python2-pyperclip has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jul 25 2018 Haïkel Guémar <hguemar@fedoraproject.org> - 1.6.4-1
- Initial package.
