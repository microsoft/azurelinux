# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Not packaged: python-hijri-converter (needed by calendars extra)
%bcond_with calendars
# Not packaged: python-fasttext (needed by fasttext extra)
%bcond_with fasttext
# Sphinx-generated HTML documentation is not suitable for packaging; see
# https://bugzilla.redhat.com/show_bug.cgi?id=2006555 for discussion.
#
# We can generate PDF documentation as a substitute.
# Skip PDF generation on EL9 due to missing /usr/bin/xindy dependency.
%if 0%{?el9} || 0%{?centos} >= 9 || 0%{?flatpak}
%bcond_with doc_pdf
%else
%bcond_without doc_pdf
%endif

Name:           python-dateparser
Version:        1.2.2
Release: 5%{?dist}
Summary:        Python parser for human readable dates

License:        BSD-3-Clause
URL:            https://github.com/scrapinghub/dateparser
Source0:        %{url}/archive/v%{version}/dateparser-%{version}.tar.gz
# Man page hand-written for Fedora in groff_man(7) format based on --help
Source1:        dateparser-download.1

BuildArch:      noarch

BuildRequires:  python3-devel

%global common_description %{expand:
Key Features

  • Support for almost every existing date format: absolute dates, relative
    dates ("two weeks ago" or "tomorrow"), timestamps, etc.
  • Support for more than 200 language locales.
  • Language autodetection
  • Customizable behavior through settings.
  • Support for non-Gregorian calendar systems.
  • Support for dates with timezones abbreviations or UTC offsets
    ("August 14, 2015 EST", "21 July 2013 10:15 pm +0500"…)
  • Search dates in longer texts.}

%description %{common_description}


%package -n python3-dateparser
Summary:        %{summary}

%py_provides python3-dateparser-cli
%py_provides python3-dateparser-data

%description -n python3-dateparser %{common_description}


%pyproject_extras_subpkg -n python3-dateparser %{?with_calendars:calendars} %{?with_fasttext:fasttext} langdetect


%package -n python3-dateparser-scripts
Summary:        %{summary}

Requires:       python3-dateparser = %{version}-%{release}
# From dateparser_scripts/requirements.txt; not included in the
# install_requires. It is questionable whether these scripts need to be
# installed at all. See:
# https://github.com/scrapinghub/dateparser/issues/705#issuecomment-1464503426.
Requires:       %{py3_dist gitpython}
Requires:       %{py3_dist parsel}
Requires:       %{py3_dist requests}
Requires:       %{py3_dist ruamel.yaml}

%description -n python3-dateparser-scripts %{common_description}

This package contains scripts used in developing the dateparser package.


%package doc
Summary:        Documentation for %{name}

%if %{with doc_pdf}
BuildRequires:  make
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3-sphinx-latex
BuildRequires:  latexmk
BuildRequires:  /usr/bin/xindy
BuildRequires:  tex-xetex-bin
# HTML theme is used as an extension even when building PDFs; we could perhaps
# patch it out of “extensions” in docs/conf.py, but it hardly seems worth the
# effort.
BuildRequires:  python3dist(sphinx-rtd-theme)
%endif

%description doc
%{summary}.


%prep
%autosetup -p1 -n dateparser-%{version}

%if %{without calendars}
sed -r -i '/\<calendars\>/d' tox.ini
%endif

%if %{without fasttext}
sed -r -i '/\<fasttext\>/d' tox.ini
%endif

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters
sed -r -i '/\<pytest-cov\>/d' tox.ini
sed -r -i 's/--cov[^[:blank:]]+//g' tox.ini

cat >> docs/conf.py <<'EOF'
# We cannot resolve remote Intersphinx mappings in an offline build.
intersphinx_mapping.clear()
# Since pdflatex cannot handle Unicode inputs in general:
latex_engine = 'xelatex'
EOF


%generate_buildrequires
%global toxenv -e all
%pyproject_buildrequires -t %{?toxenv} %{?with_calendars:-x calendar }%{?with_fasttext:-x fasttext }-x langdetect dateparser_scripts/requirements.txt


%build
%pyproject_wheel
%if %{with doc_pdf}
PYTHONPATH="${PWD}" %make_build -C docs latex SPHINXOPTS='%{?_smp_mflags}'
%make_build -C docs/_build/latex LATEXMKOPTS='-quiet'
%endif


%install
%pyproject_install
%pyproject_save_files dateparser dateparser_cli dateparser_data dateparser_scripts
install -t '%{buildroot}%{_mandir}/man1' -D -p -m 0644 '%{SOURCE1}'


%check
%if %{without calendars}
# Uses hijri_convert
# --ignore does not seem to prevent doctest collection in tests/
rm -vf tests/test_hijri.py
ignore="${ignore-} --ignore=tests/test_hijri.py"
ignore="${ignore-} --ignore=dateparser/calendars/hijri.py"
ignore="${ignore-} --ignore=dateparser/calendars/hijri_parser.py"
# Uses convertdate
# --ignore does not seem to prevent doctest collection in tests/
rm -vf tests/test_jalali.py
ignore="${ignore-} --ignore=tests/test_jalali.py"
ignore="${ignore-} --ignore=dateparser/calendars/jalali.py"
ignore="${ignore-} --ignore=dateparser/calendars/jalali_parser.py"
%endif

%if %{without fasttext}
# Uses fasttext
# --ignore does not seem to prevent doctest collection in tests/
rm -vf tests/test_language_detect.py
ignore="${ignore-} --ignore=dateparser/custom_language_detection/fasttext.py"
ignore="${ignore-} --ignore=tests/test_language_detect.py"
%endif

# Fuzzing tests requires atheris which is not packaged in fedora.
# --ignore does not seem to prevent doctest collection in fuzzing/
rm -vf fuzzing/dateparser_fuzzer.py
rm -vf fuzzing/fuzz_helpers.py
ignore="${ignore-} --ignore=fuzzing/dateparser_fuzzer.py"
ignore="${ignore-} --ignore=fuzzing/fuzz_helpers.py"

# From the docstring containing this doctest:
#   In the example below, since no day information is present, the day is
#   assumed to be current day ``16`` from *current date* (which is June 16,
#   2015, at the moment of writing this). Hence, the level of precision is
#   ``month``:
# Obviously, yet bizarrely, this only works when it is *executed* on the 16th
# of some month.
k="${k-}${k+ and }not (DateDataParser and get_date_data)"

# The doctest parser does not like the line continuation here:
#     File "<doctest dateparser.search.search_dates[2]>", line 1
#       search_dates('The first artificial Earth satellite was launched on 4 October 1957.',
#                   ^
#   SyntaxError: '(' was never closed
k="${k-}${k+ and }not search_dates"

%tox -- -- ${ignore-} -k "${k-}" -v


%files -n python3-dateparser -f %{pyproject_files}
%exclude %{python3_sitelib}/dateparser_scripts/

%{_bindir}/dateparser-download
%{_mandir}/man1/dateparser-download.1*


%files -n python3-dateparser-scripts
%{python3_sitelib}/dateparser_scripts/


%files doc
%license LICENSE
%doc AUTHORS.rst
%doc CONTRIBUTING.rst
%doc HISTORY.rst
%doc README.rst
%if %{with doc_pdf}
%doc docs/_build/latex/dateparser.pdf
%endif


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.2.2-4
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.2.2-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.2.2-1
- 1.2.2

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.2.1-3
- Rebuilt for Python 3.14

* Tue May 27 2025 Lumír Balhar <lbalhar@redhat.com> - 1.2.1-2
- Fix compatibility with Python 3.14 beta 1 (rhbz#2367245)

* Sat Mar 01 2025 Romain Geissler <romain.geissler@amadeus.com> - 1.2.1-1
- Update to 1.2.1 (close RHBZ#2336931)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 1.1.7-6
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 19 2023 Python Maint <python-maint@redhat.com> - 1.1.7-2
- Rebuilt for Python 3.12

* Fri Mar 10 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.7-1
- Update to 1.1.7 (close RHBZ#2115204)
- Port to pyproject-rpm-macros
- Add extras metapackages
- Build Sphinx documentation as PDF rather than HTML to avoid issues with
  bundled and precompiled JavaScript etc.
- Split out a python3-dateparser-scripts subpackage

* Fri Mar 03 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.7.6-10
- migrated to SPDX license

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 20 2022 Miro Hrončok <mhroncok@redhat.com> - 0.7.6-7
- Run the tests during build
- Drop unused requirement of deprecated nose
- Fix incompatibility with regex 2022.3.15+
- Fixes: rhbz#2080221

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.7.6-6
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 0.7.6-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Oct 26 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.7.6-1
- 0.7.6, disabled tests due to missing packages.

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.4-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.7.4-3
- BR python3-setuptools

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 0.7.4-2
- Rebuilt for Python 3.9

* Tue Mar 10 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.7.4-1
- Fix license tag (rhbz#1748956)

* Tue Nov 19 2019 Fabian Affolter <mail@fabian-affolter.ch> - 0.7.2-4
- Fix license tag (rhbz#1748956)

* Mon Nov 18 2019 Fabian Affolter <mail@fabian-affolter.ch> - 0.7.2-3
- Disable tests

* Mon Nov 18 2019 Fabian Affolter <mail@fabian-affolter.ch> - 0.7.2-2
- Fix BRs

* Thu Oct 17 2019 Fabian Affolter <mail@fabian-affolter.ch> - 0.7.2-1
- Update to latest upstream release 0.7.2

* Tue Sep 03 2019 Fabian Affolter <mail@fabian-affolter.ch> - 0.7.1-1
- Initial package for Fedora
