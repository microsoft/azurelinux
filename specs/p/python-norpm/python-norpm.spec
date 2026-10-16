# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python-norpm
Version:        1.11
Release: 2%{?dist}
Summary:        RPM Macro Expansion in Python

License:        LGPL-2.1-or-later
URL:            https://github.com/praiskup/norpm
Source:         %pypi_source norpm

BuildArch:      noarch
BuildRequires:  python3-devel


%global _description %{expand:
Parse RPM macro and spec files, expanding macros safely—without any potential
Turing-complete side effects.

This is a standalone library and set of tools that depend only on the standard
Python library and PLY (used for expression parsing).
}

%description %_description


%package -n     python3-norpm
Summary:        %summary

%description -n python3-norpm %_description


%prep
%autosetup -p1 -n norpm-%version

%if 0%{?rhel} == 9
cat > setup.py <<EOF
from setuptools import setup
setup(
    name='norpm',
    version='%version',
    packages=['norpm', 'norpm.cli'],
    install_requires=['lark-parser'],
    entry_points={
        'console_scripts': [
            'norpm-expand-specfile = norpm.cli.expand_specfile:_main',
            'norpm-conditions-for-arch-statements = norpm.cli.conditions_for_arch_statements:_main',
        ],
    },
)
EOF
%endif


%generate_buildrequires
%pyproject_buildrequires -g test


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l norpm


%check
%pyproject_check_import
%pytest


%files -n python3-norpm -f %pyproject_files
%doc README.md
%_bindir/norpm-conditions-for-arch-statements
%_bindir/norpm-expand-specfile


%changelog
* Fri Jun 26 2026 Pavel Raiskup <praiskup@redhat.com> - 1.11-1
- new release, per upstream release notes:
  https://github.com/praiskup/norpm/blob/main/NEWS.md

* Fri Jun 26 2026 Pavel Raiskup <praiskup@redhat.com> - 1.10-1
- new release, per upstream release notes:
  https://github.com/praiskup/norpm/blob/main/NEWS.md

* Wed Jun 03 2026 Python Maint <python-maint@redhat.com> - 1.9-2
- Rebuilt for Python 3.15

* Sat Feb 21 2026 Pavel Raiskup <praiskup@redhat.com> - 1.9-1
- New upstream release

* Mon Feb 02 2026 Pavel Raiskup <praiskup@redhat.com> - 1.8-3
- add support for epel9 builds

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Mon Nov 24 2025 Pavel Raiskup <praiskup@redhat.com> - 1.8-1
- new upstream release:
  https://github.com/praiskup/norpm/releases/tag/v1.8

* Sun Nov 09 2025 Pavel Raiskup <praiskup@redhat.com> - 1.7-1
- new upstream release:
  https://github.com/praiskup/norpm/releases/tag/v1.7

* Tue Oct 14 2025 Pavel Raiskup <praiskup@redhat.com> - 1.6-1
- new upstream release:
  https://github.com/praiskup/norpm/releases/tag/v1.6

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.5-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Sun Sep 07 2025 Pavel Raiskup <praiskup@redhat.com> - 1.5-1
- new upstream release, per release notes:
  https://github.com/praiskup/norpm/releases/tag/v1.5

* Tue Sep 02 2025 Pavel Raiskup <praiskup@redhat.com> - 1.4-1
- new upstream release, v"version" expression support, if[n]arch support,
  many bugfixes

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.3-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Mon Aug 11 2025 Pavel Raiskup <praiskup@redhat.com> - 1.3-1
- Initial packaging
