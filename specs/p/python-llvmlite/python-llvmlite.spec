## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 6;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond tests 1
# Sphinx-generated HTML documentation is not suitable for packaging; see
# https://bugzilla.redhat.com/show_bug.cgi?id=2006555 for discussion.
#
# We can generate PDF documentation as a substitute.
%bcond doc_pdf 1

# For 0.44.0, LLVM 15 is the default. LLVM 16 support is “experimental;” we can
# try it if we need to.
%global llvm_compat 15

Name:           python-llvmlite
Version:        0.44.0
Release:        %{autorelease}
Summary:        Lightweight LLVM Python binding for writing JIT compilers

# The entire source is BSD-2-Clause, except:
#   - The bundled versioneer.py, and the _version.py it generates (which is
#     packaged) is LicenseRef-Fedora-Public-Domain. In later versions of
#     versioneer, this becomes CC0-1.0 and then Unlicense.
#     Public-domain text added to fedora-license-data in commit
#     830d88d4d89ee5596839de5b2c1f48426488841f:
#     https://gitlab.com/fedora/legal/fedora-license-data/-/merge_requests/210
#   - ffi/memorymanager.{h,cpp} are Apache-2.0 WITH LLVM-exception
License:        %{shrink:
                BSD-2-Clause AND
                Apache-2.0 WITH LLVM-exception AND
                LicenseRef-Fedora-Public-Domain
                }
# Additionally, the following does not affect the license of the binary RPMs:
#   - conda-recipes/appveyor/run_with_env.cmd is CC0-1.0; for distribution in
#     the source RPM, it is covered by “Existing uses of CC0-1.0 on code files
#     in Fedora packages prior to 2022-08-01, and subsequent upstream versions
#     of those files in those packages, continue to be allowed. We encourage
#     Fedora package maintainers to ask upstreams to relicense such files.”
#     https://gitlab.com/fedora/legal/fedora-license-data/-/issues/91#note_1151947383
SourceLicense:  %{license} AND CC0-1.0
URL:            http://llvmlite.pydata.org/
%global forgeurl https://github.com/numba/llvmlite
Source:         %{forgeurl}/archive/v%{version}/llvmlite-%{version}.tar.gz

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist pytest}

BuildRequires:  llvm%{llvm_compat}-devel
BuildRequires:  gcc-c++

%global _description %{expand:
llvmlite is a project originally tailored for Numba‘s needs, using the
following approach:

  • A small C wrapper around the parts of the LLVM C++ API we need that are not
    already exposed by the LLVM C API.
  • A ctypes Python wrapper around the C API.
  • A pure Python implementation of the subset of the LLVM IR builder that we
    need for Numba.}

%description %_description

%package -n python3-llvmlite
Summary:        %{summary}

# ffi/memorymanager.{h,cpp} are copied from an unspecified version of LLVM
Provides:       bundled(llvm)

%description -n python3-llvmlite %_description

%package doc
Summary:        %{summary}

%if %{with doc_pdf}
BuildRequires:  make
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3-sphinx-latex
BuildRequires:  latexmk
%endif

BuildArch:      noarch

%description doc
Documentation for %{name}.

%prep
%autosetup -n llvmlite-%{version} -p1

# increase verbosity of tests to 2
sed -i 's/\(def run_tests.*verbosity=\)1/\12/' llvmlite/tests/__init__.py

# Comment out to remove /usr/bin/env shebangs
# Can use something similar to correct/remove /usr/bin/python shebangs also
# find . -type f -name "*.py" -exec sed -i '/^#![  ]*\/usr\/bin\/env.*$/ d' {} 2>/dev/null ';'

# No network access
echo 'intersphinx_mapping.clear()' >> docs/source/conf.py

%generate_buildrequires
# The HTML theme is imported in conf.py even when not generating HTML
%pyproject_buildrequires %{?with_doc_pdf:docs/rtd-requirements.txt}

%build
export LLVM_CONFIG="%{_libdir}/llvm%{llvm_compat}/bin/llvm-config"
%pyproject_wheel

%if %{with doc_pdf}
%make_build -C docs latex SPHINXOPTS='-j%{?_smp_build_ncpus}'
%make_build -C docs/_build/latex LATEXMKOPTS='-quiet'
%endif

%install
%pyproject_install
%pyproject_save_files -l llvmlite

%check
%if %{with tests}
%ifarch riscv64
# Disable JIT tests on riscv64 since that feature is not supported
# upstream yet.  See:
# https://github.com/numba/llvmlite/issues/923
# https://github.com/felixonmars/archriscv-packages/blob/master/python-llvmlite/riscv64.patch
export PYTEST_ADDOPTS="\
        --deselect llvmlite/tests/test_binding.py::TestMCJit \
        --deselect llvmlite/tests/test_binding.py::TestGlobalConstructors \
        --deselect llvmlite/tests/test_binding.py::TestObjectFile::test_add_object_file \
        --deselect llvmlite/tests/test_binding.py::TestOrcLLJIT \
        --deselect llvmlite/tests/test_binding.py::TestDylib::test_bad_library"
%endif
%{pytest} -vv llvmlite/tests
%endif

%files -n python3-llvmlite -f %{pyproject_files}
%doc CHANGE_LOG README.rst

%files doc
%license LICENSE
%doc examples/
%if %{with doc_pdf}
%doc docs/_build/latex/llvmlite.pdf
%endif

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 0.44.0-6
- Latest state for python-llvmlite

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.44.0-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.44.0-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.44.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.44.0-2
- Rebuilt for Python 3.14

* Sat Feb 01 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0.44.0-1
- Update to 0.44.0 (close RHBZ#2327009)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.43.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.43.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 30 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.43.0-1
- Update to 0.43.0 (close RHBZ#2292256)

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.42.0-5
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.42.0-4
- Rebuilt for Python 3.13

* Tue Feb 20 2024 Richard W.M. Jones <rjones@redhat.com> - 0.42.0-3
- Deselect some tests on riscv64.

* Mon Feb 19 2024 Richard W.M. Jones <rjones@redhat.com> - 0.42.0-2
- Use pytest instead of the upstream runtests script

* Fri Feb 02 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.42.0-1
- Update to 0.42.0 (close RHBZ#2254414)
- Make the -doc subpackage noarch

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.41.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.41.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.41.1-2
- Assert that a license file is present in the .dist-info directory

* Fri Oct 20 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.41.1-1
- Update to 0.41.1 (close RHBZ#2244851)

* Tue Oct 17 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.41.0-2
- F38+: Use %%{py3_test_envvars} to set up the test environment

* Thu Sep 21 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.41.0-1
- Update to 0.41.0 (close RHBZ#2232746)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.40.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jul 01 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.40.1-1
- Update to 0.40.1 (close RHBZ#2213643)

* Sat Jul 01 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.40.0-3
- Use new (rpm 4.17.1+) bcond style

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 0.40.0-2
- Rebuilt for Python 3.12

* Wed May 10 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.40.0-1
- Update to 0.40.0 (close RHBZ#2185127)

* Thu May 04 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.39.1-10
- Use a simpler description from the upstream README.rst

* Thu May 04 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.39.1-9
- Drop “forge” macros

* Tue Apr 25 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.39.1-8
- Don’t assume %%_smp_mflags is -j%%_smp_build_ncpus

* Tue Apr 25 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.39.1-7
- Simplify test-suite invocation

* Tue Apr 25 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.39.1-6
- Drop unnecessary manual BR on pyproject-rpm-macros

* Tue Apr 25 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.39.1-5
- Replace a downstream patch with a backported upstream commit

* Wed Mar 22 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.39.1-4
- Add public-domain text link in license breakdown

* Wed Mar 08 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.39.1-3
- Patch out max. Python version check entirely

* Tue Mar 07 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.39.1-2
- Allow Python 3.12 (downstream-only); close RHBZ#2176128

* Tue Mar 07 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.39.1-1
- Update to 0.39.1

* Tue Mar 07 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.37.0-9
- Convert to SPDX

* Tue Mar 07 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.37.0-8
- Build Sphinx docs as PDF instead of HTML

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.37.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.37.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.37.0-5
- Rebuilt for Python 3.11

* Fri May 06 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.37.0-4
- Allow Python 3.11 in version guard (fix RHBZ#2022282)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.37.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Nov 12 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.37.0-2
- Use upstream PR#769 for Python 3.10 support

* Mon Sep 13 2021 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 0.37.0-1
- feat: init
## END: Generated by rpmautospec
