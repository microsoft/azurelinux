## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Sphinx-generated HTML documentation is not suitable for packaging; see
# https://bugzilla.redhat.com/show_bug.cgi?id=2006555 for discussion.
#
# We can generate PDF documentation as a substitute.
%bcond doc_pdf 1

Name:           python-fastavro
Version:        1.12.1
Release:        %autorelease
Summary:        Fast Avro for Python

# The fastavro project is licensed MIT, but is derived from Apache Avro which
# is ASL 2.0; see LICENSE and also NOTICE.txt.
#
# The following source files are specifically known to include ASL 2.0 content:
#
#   • fastavro/_read_py.py
#   • fastavro/_write_py.py
#   • fastavro/_write.pyx
#   • fastavro/_read.pyx
#
# SPDX:
License:        MIT AND Apache-2.0
URL:            https://github.com/fastavro/fastavro
Source:         %{pypi_source fastavro}

# Upstream does not test, nor support 32 bit systems
# Issue: https://github.com/fastavro/fastavro/issues/526
# Fedora bug: https://bugzilla.redhat.com/show_bug.cgi?id=1943932
ExcludeArch:    %{arm32} %{ix86}

BuildRequires:  python3-devel
BuildRequires:  gcc

BuildRequires:  make
BuildRequires:  %{py3_dist sphinx}
BuildRequires:  %{py3_dist sphinx_rtd_theme}
%if %{with doc_pdf}
BuildRequires:  python3-sphinx-latex
BuildRequires:  latexmk
%endif

%global _description %{expand:
Because the Apache Python avro package is written in pure Python, it is
relatively slow. In one test case, it takes about 14 seconds to iterate through
a file of 10,000 records. By comparison, the JAVA avro SDK reads the same file
in 1.9 seconds.

The fastavro library was written to offer performance comparable to the Java
library. With regular CPython, fastavro uses C extensions which allow it to
iterate the same 10,000 record file in 1.7 seconds. With PyPy, this drops to
1.5 seconds (to be fair, the JAVA benchmark is doing some extra JSON
encoding/decoding).

Supported Features

  • File Writer
  • File Reader (iterating via records or blocks)
  • Schemaless Writer
  • Schemaless Reader
  • JSON Writer
  • JSON Reader
  • Codecs (Snappy, Deflate, Zstandard, Bzip2, LZ4, XZ)
  • Schema resolution
  • Aliases
  • Logical Types
  • Parsing schemas into the canonical form
  • Schema fingerprinting

Missing Features

  • Anything involving Avro’s RPC features}

%description %{_description}


%package -n python3-fastavro
Summary:        %{summary}

%description -n python3-fastavro %{_description}


%pyproject_extras_subpkg -n python3-fastavro codecs snappy zstandard lz4


%package doc
Summary:        %{summary}
%description doc
Documentation for python-fastavro.


%prep
%autosetup -p1 -n fastavro-%{version}

# Remove the already generated C files so we generate them ourselves
find fastavro/ -name '*.c' -print -delete

# Drop intersphinx mappings, since we can’t download remote inventories and
# can’t easily produce working hyperlinks from inventories in local
# documentation packages.
echo 'intersphinx_mapping.clear()' >> docs/conf.py

# Do not generate dependencies on linters, formatters, typecheckers, etc.:
sed -r -e '/^(black|check-manifest|flake8|mypy|twine)\b/d' \
    -e '/^(coverage|pytest-cov)\b/d' \
    developer_requirements.txt | tee developer_requirements-filtered.txt


%generate_buildrequires
# codecs includes snappy, zstandard, and lz4
%pyproject_buildrequires -x codecs
# For some reason, combining this with the above does not work, even though it
# should. It would be nice to investigate this.
%pyproject_buildrequires developer_requirements-filtered.txt


%build
%pyproject_wheel

BLIB="${PWD}/build/lib.%{python3_platform}-cpython-%{python3_version_nodots}"
PYTHONPATH="${BLIB}" %make_build -C docs man \
    SPHINXOPTS='-n -j%{?_smp_build_ncpus}'
%if %{with doc_pdf}
PYTHONPATH="${BLIB}" %make_build -C docs latex \
    SPHINXOPTS='-n -j%{?_smp_build_ncpus}'
%make_build -C docs/_build/latex LATEXMKOPTS='-quiet'
%endif


%install
%pyproject_install
%pyproject_save_files -l fastavro

install -t '%{buildroot}%{_mandir}/man1' -p -m 0644 -D \
    'docs/_build/man/fastavro.1'


%check
# Avoid importing the “un-built” package. The tests really assume we have built
# the extensions in-place, and occasionally use relative paths to the package
# source directory. We would prefer to test the extensions as installed (and
# avoid an extra build step), so we use a symbolic link to make the tests
# appear alongside the built package.
mkdir -p _empty
cd _empty
cp -rp ../tests/ .
ln -s '%{buildroot}%{python3_sitearch}/fastavro' .

# These fail because there are no source lines in the tracebacks from Cython
# modules, even though this works in the upstream CI. We haven’t figured out
# the root cause, but it doesn’t seem to represent a real problem.
k="${k-}${k+ and }not test_regular_vs_ordered_dict_map_typeerror"
k="${k-}${k+ and }not test_regular_vs_ordered_dict_record_typeerror"

%pytest -k "${k-}"


%files -n python3-fastavro -f %{pyproject_files}
%{_bindir}/fastavro
%{_mandir}/man1/fastavro.*


%files doc
%license LICENSE NOTICE.txt
%doc ChangeLog
%doc README.md
%if %{with doc_pdf}
%doc docs/_build/latex/fastavro.pdf
%endif


%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 1.12.1-2
- Latest state for python-fastavro

* Fri Oct 10 2025 Packit <hello@packit.dev> - 1.12.1-1
- Update to 1.12.1 upstream release
- Resolves: rhbz#2403095

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.12.0-3
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.12.0-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 31 2025 Packit <hello@packit.dev> - 1.12.0-1
- Update to 1.12.0 upstream release
- Resolves: rhbz#2385822

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 11 2025 Python Maint <python-maint@redhat.com> - 1.11.1-3
- Rebuilt for Python 3.14

* Wed Jun 11 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1.11.1-2
- Rebuilt for Python 3.14 (close RHBZ#2371901)

* Sun May 18 2025 Packit <hello@packit.dev> - 1.11.1-1
- Update to 1.11.1 upstream release
- Resolves: rhbz#2367031

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 20 2024 Packit <hello@packit.dev> - 1.10.0-1
- Update to 1.10.0 upstream release
- Resolves: rhbz#2333498

* Sun Sep 08 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1.9.7-1
- Update to 1.9.7 upstream release
- Resolves: rhbz#2310338

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 10 2024 Packit <hello@packit.dev> - 1.9.5-1
- Update to 1.9.5 upstream release
- Resolves: rhbz#2297035

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 1.9.4-2
- Rebuilt for Python 3.13

* Wed Feb 14 2024 Packit <hello@packit.dev> - 1.9.4-1
- [packit] 1.9.4 upstream release

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1.8.4-5
- Skip tests that fail with zlib-ng

* Wed Jan 03 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1.8.4-4
- Assert that a license file is present in the .dist-info directory

* Tue Nov 07 2023 Miro Hrončok <miro@hroncok.cz> - 1.8.4-3
- Fix tests that fail without sphinxcontrib_jsmath-*-nspkg.pth

* Mon Oct 09 2023 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 1.8.4-2
- chore: add packit

* Fri Oct 06 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.8.4-1
- Update to 1.8.4 (close RHBZ#2241972)

* Sat Sep 09 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.8.3-2
- Drop the manual Cython BuildRequires

* Sat Sep 09 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.8.3-1
- Update to 1.8.3 (close RHBZ#2238056)

* Wed Jul 19 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.8.2-1
- Update to 1.8.2 (close RHBZ#2221332)

* Wed Jul 19 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.7.4-3
- Use new (rpm 4.17.1+) bcond style

* Wed Jun 28 2023 Python Maint <python-maint@redhat.com> - 1.7.4-2
- Rebuilt for Python 3.12

* Sat May 06 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.7.4-1
- Update to 1.7.4 (close RHBZ#2193327)

* Sat May 06 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.7.3-2
- Don’t assume %%_smp_mflags is -j%%_smp_build_ncpus

* Fri Mar 10 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.7.3-1
- Update to 1.7.3 (close RHBZ#2176743)

* Thu Mar 09 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.7.2-2
- Drop %%pyproject_build_lib (F37+)

* Sat Feb 25 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.7.2-1
- Update to 1.7.2 (close RHBZ#2172972)

* Fri Feb 17 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.7.1-1
- Update to 1.7.1 (close RHBZ#2165194)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Oct 30 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.7.0-1
- Update to 1.7.0 (close RHBZ#2137908)

* Sun Sep 11 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.6.1-1
- Update to 1.6.1 (close RHBZ#2125826)

* Tue Aug 16 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.6.0-1
- Update to 1.6.0 (close RHBZ#2118528)

* Tue Aug 02 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.5.4-1
- Update to 1.5.4 (close RHBZ#2112610)

* Tue Aug 02 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.5.3-2
- Convert License to SPDX

* Wed Jul 20 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.5.3-1
- Update to 1.5.3 (close RHBZ#2108901)

* Sat Jul 16 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.5.2-1
- Update to 1.5.2 (close RHBZ#2101870)

* Mon Jul 11 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.5.1-4
- Fix extra newline in description

* Wed Jun 15 2022 Python Maint <python-maint@redhat.com> - 1.5.1-3
- Rebuilt for Python 3.11

* Sat Jun 11 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.5.1-2
- Do not generate dependencies on linters, formatters, typecheckers, etc.

* Fri Jun 10 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.5.1-1
- Update to 1.5.1 (close RHBZ#2094653)

* Fri Jun 10 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.4.12-2
- Drop a workaround for F34 since it is EOL

* Thu May 19 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.4.12-1
- Update to 1.4.12 (close RHBZ#2088391)

* Sat Apr 30 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.4.11-1
- Update to 1.4.11 (close RHBZ#2079637)

* Mon Apr 11 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.4.10-1
- Update to 1.4.10 (close RHBZ#2061019)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Jan 09 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.4.9-1
- Update to 1.4.9 (close RHBZ#2038426)

* Mon Dec 27 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.4.8-2
- Use provisional %%%%pyproject_build_lib macro

* Mon Dec 27 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.4.8-1
- Update to 1.4.8 (close RHBZ#2035758)

* Tue Dec 07 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.4.7-5
- Simplify setting PYTHONPATH for doc build

* Sat Nov 27 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.4.7-2
- Reduce LaTeX PDF build verbosity

* Fri Oct 29 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.4.7-1
- Update to 1.4.7 (close RHBZ#2018577)

* Mon Oct 25 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.4.6-3
- Fix: test_ancient_datetime test fails in timezone with offset that changed
  since 1960

* Mon Oct 25 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.4.6-2
- Work around RHBZ#1905174 in F34 in python-check-manifest

* Mon Oct 25 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.4.6-1
- Update to 1.4.6

* Mon Oct 11 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.4.5-1
- Update to 1.4.5 (close RHBZ#2007469)
- Switch to pyproject-rpm-macros (“new guidelines”)
- Add extras metapackages
- Build PDF documentation instead of HTML due to JS bundling issues
- Change license from ASL 2.0 to (MIT and ASL 2.0)

* Mon Aug 16 2021 Shane Allcroft <shaneallcroft AT fedoraproject DOT org> - 1.4.4-1
- Update to latest release

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.4.1-2
- Rebuilt for Python 3.10

* Sat May 22 2021 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.4.1-1
- Update to latest release

* Sun Mar 28 2021 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.3.4-1
- Update to latest release
- add new BRs
- remove unneeded pyprovide macro
- exclude 32 bit arches that upstream does not support
- Enable tests

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.23.3-2
- Rebuilt for Python 3.9

* Fri May 01 2020 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.23.3-1
- Update to latest release
- Remove py2 bits

* Sun Feb 02 2020 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.22.9-1
- Update to 0.22.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.22.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 9 2019 Aniket Pradhan <major AT fedoraproject DOT org> - 0.22.7-1
- Update to 0.22.7
- Remove Cython version constraint, F29 is no more maintained

* Sat Oct 12 2019 Aniket Pradhan <major AT fedoraproject DOT org> - 0.22.5-1
- Update to 0.22.5

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.22.4-2
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 31 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.22.4-1
- Update to 0.22.4

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.22.2-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.22.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 28 2019 Luis M. Segundo <blackfile@fedoraproject.org> - 0.22.2-1
- New Upstream version

* Fri May 31 2019 Luis M. Segundo <blackfile@fedoraproject.org> - 0.21.24-1
- Update to 0.19.8

* Mon May 13 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.21.23-1
- Update to latest release

* Sun Feb 03 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.21.17-1
- Update to latests upstream release

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 12 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.21.13-1
- Disable py3 on F30+
- Update to latest release
- Use pypi source

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 0.19.8-2
- Rebuilt for Python 3.7

* Fri Jun 29 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.19.8-1
- Update to 0.19.8

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.19.6-2
- Rebuilt for Python 3.7

* Sat Jun 09 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.19.6-1
- Update to new release
- Tests still failing for i686 so disabling

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.17.3-3
- Re-enable tests for testing

* Mon Jan 22 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.17.3-2
- Disable tests temporarily - fail on i686 only. Issue filed upstream.

* Sun Jan 21 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.17.3-1
- Update for review (rhbz#1534787)
- Update to latest upstream release
- Generate separate doc subpackage for docs
- Install man page
- Rectify license
- Fix tests

* Mon Jan 15 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.17.1-1
- Initial build

## END: Generated by rpmautospec
