# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Sphinx-generated HTML documentation is not suitable for packaging; see
# https://bugzilla.redhat.com/show_bug.cgi?id=2006555 for discussion.
#
# We can generate PDF documentation as a substitute.
%bcond_without doc_pdf

Name:           python-string_utils
Version:        1.0.0
Release: 23%{?dist}
Summary:        Utility functions for strings validation and manipulation

# SPDX
License:        MIT
URL:            https://github.com/daveoncode/python-string-utils
Source0:        %{url}/archive/v%{version}/python-string-utils-%{version}.tar.gz

# Remove README.md as packaged data in the wheel
# https://github.com/daveoncode/python-string-utils/pull/16
#
# This keeps it from being installed to the bizarre path
# %%{_prefix}/README/README.md.
Patch:          %{url}/pull/16.patch

BuildArch:      noarch

%global _description %{expand:
A handy library to validate, manipulate and generate strings, which is:

  • Simple and “pythonic”
  • Fully documented and with examples! (html version on readthedocs.io)
  • 100% code coverage! (see it with your own eyes on codecov.io)
  • Tested (automatically on each push thanks to Travis CI) against all
    officially supported Python versions
  • Fast (mostly based on compiled regex)
  • Free from external dependencies
  • PEP8 compliant}

%description %{_description}


# The source package is named python-string_utils for historical reasons.  The
# binary package, python3-python-string-utils, is named using the canonical
# project name[1]; see also [2].
#
# The %%py_provides macro is used to provide an upgrade path from
# python3-string_utils and to produce the appropriate Provides for the
# importable module[3].
#
# [1] https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_canonical_project_name
# [2] https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_library_naming
# [3] https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_provides_for_importable_modules
%package -n python3-python-string-utils
Summary:        %{summary}

# Provide an upgrade path
%py_provides python3-string_utils
Obsoletes:      python3-string_utils < 1.0.0-11

BuildRequires:  python3-devel

%description -n python3-python-string-utils %{_description}


%package doc
Summary:        Documentation for python-string-utils

%if %{with doc_pdf}
BuildRequires:  make
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3-sphinx-latex
BuildRequires:  latexmk
# The HTML theme is used as a Sphinx extension, so it is needed even when not
# producing HTML output.
BuildRequires:  python3dist(sphinx-rtd-theme)
%endif

%description doc
%{summary}.


%prep
%autosetup -n python-string-utils-%{version} -p1

# Remove bogus executable permissions from non-script files. This corresponds
# to the upstream pull request:
#
# Change files permissions to 644
# https://github.com/daveoncode/python-string-utils/pull/4
find . -type f -perm /0111 \
    -exec gawk '!/^#!/ { print FILENAME }; { nextfile }' '{}' '+' |
  xargs -r -t chmod -v a-x


%generate_buildrequires
%pyproject_buildrequires -t


%build
%pyproject_wheel

%if %{with doc_pdf}
%make_build -C docs latex SPHINXOPTS='-j%{?_smp_build_ncpus}'
%make_build -C docs/_build/latex LATEXMKOPTS='-quiet'
%endif


%install
%pyproject_install
%pyproject_save_files string_utils


%check
%tox


%files -n python3-python-string-utils -f %{pyproject_files}
%doc README.md
%doc CHANGELOG.md


%files doc
%license LICENSE
%if %{with doc_pdf}
%doc docs/_build/latex/PythonStringUtils.pdf
%endif


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.0.0-22
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.0.0-21
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.0.0-19
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.0.0-16
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu May 04 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.0.0-12
- Fix source archive committed to dist-git
- Stop pretending we will use this spec file for EPEL7/8
- Reduce macro indirection in the spec file
- Drop unnecessary BuildRequires on git
- Improve the source archive URL
- Update summary and description from upstream
- Rename the binary RPM to match the canonical project name
- Fix incorrect file and directory permissions
- Build docs as PDF instead of HTML to sidestep most issues with bundling etc.
- Adjust spec-file whitespace for readability
- Stop doing coverage analysis
- Package the changelog
- Confirm License is SPDX MIT
- Port to pyproject-rpm-macros
* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 1.0.0-11
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.0.0-8
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.0.0-5
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-2
- Rebuilt for Python 3.9

* Thu Apr 30 2020 Jason Montleon <jmontleo@redhat.com> - 1.0.0-1
- Update to 1.0.0. Drops Python 2 support.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 23 2020 Yatin Karel <ykarel@redhat.com> - 0.6.0-10
- Fix condition for El8

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-8
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-7
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 19 2018 Daniel Mellado <dmellado@redhat.com> 0.6.0-4
- Fix rpmlint permissions issues
- Fix docs
- Fix doctree removal
- Fix version mismatch in spec

* Tue Dec 4 2018 John Kim <jkim@redhat.com> 0.6.0-3
- Fixed URL, Source0
- Enable disable python3 for rhel
- Enable test
- Add doc

* Wed May 10 2017 Jason Montleon <jmontleo@redhat.com> 0.6.0-2
- Fix python_provide for EL7 python3

* Wed May 10 2017 Jason Montleon <jmontleo@redhat.com> 0.6.0-1
- Initial Build
