
%global srcname rdflib

%bcond docs 0
%bcond tests 0
%if 0%{?fedora}
%bcond docs 1
%bcond tests 1
%endif

Name:           python-%{srcname}
Version:        7.0.0
Release:        6%{?dist}
Summary:        Python library for working with RDF
License:        BSD-3-Clause
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/RDFLib/rdflib
BuildArch:      noarch

Source:         %{pypi_source}#/%{name}-%{version}.tar.gz
Patch:          %{srcname}-py3_13-fix-pickler.diff
# Backported from https://github.com/RDFLib/rdflib/pull/2817
Patch:          rdflib-7.0.0-pytest8.patch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires: 	python3-pip
BuildRequires: 	python3-wheel
BuildRequires: 	python3-poetry

%if %{with tests}
BuildRequires:  python3dist(pytest)
%endif

%if %{with docs}
BuildRequires:  python3dist(myst-parser)
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3dist(sphinx-autodoc-typehints)
BuildRequires:  python3dist(sphinxcontrib-apidoc)
BuildRequires:  python3dist(typing-extensions)
%endif

%description
RDFLib is a pure Python package for working with RDF. RDFLib contains most
things you need to work with RDF, including parsers and serializers for
RDF/XML, N3, NTriples, N-Quads, Turtle, TriX, Trig and JSON-LD, a Graph
interface which can be backed by any one of a number of Store implementations,
store implementations for in-memory, persistent on disk (Berkeley DB) and
remote SPARQL endpoints, a SPARQL 1.1 implementation - supporting SPARQL 1.1
Queries and Update statements - and SPARQL function extension mechanisms.

%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{summary}

%description -n python%{python3_pkgversion}-%{srcname}
RDFLib is a pure Python package for working with RDF. RDFLib contains most
things you need to work with RDF, including parsers and serializers for
RDF/XML, N3, NTriples, N-Quads, Turtle, TriX, Trig and JSON-LD, a Graph
interface which can be backed by any one of a number of Store implementations,
store implementations for in-memory, persistent on disk (Berkeley DB) and
remote SPARQL endpoints, a SPARQL 1.1 implementation - supporting SPARQL 1.1
Queries and Update statements - and SPARQL function extension mechanisms.

%if %{with docs}
%package -n python%{python3_pkgversion}-%{srcname}-docs
Summary:        Documentation for %{srcname}

%description -n python%{python3_pkgversion}-%{srcname}-docs
Documentation for %{srcname}, a Python library for working with RDF.
%endif

%prep
%autosetup -p1 -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install

# Various .py files within site-packages have a shebang line but aren't
# flagged as executable.
# I've gone through them and either removed the shebang or made them
# executable as appropriate:

# __main__ parses URI as N-Triples:
chmod +x %{buildroot}%{python3_sitelib}/rdflib/plugins/parsers/ntriples.py

# __main__ parses the file or URI given on the command line:
chmod +x %{buildroot}%{python3_sitelib}/rdflib/tools/rdfpipe.py

# __main__ runs a test (well, it's something)
chmod +x %{buildroot}%{python3_sitelib}/rdflib/extras/external_graph_libs.py

# sed these headers out as they include no __main__
for lib in %{buildroot}%{python3_sitelib}/rdflib/extras/describer.py; do
 sed '1{\@^#!/usr/bin/env python@d}' $lib > $lib.new &&
 touch -r $lib $lib.new &&
 mv $lib.new $lib
done

# sed shebangs
sed -i '1s=^#!/usr/bin/\(python\|env python\).*=#!%{__python3}='  \
    %{buildroot}%{python3_sitelib}/rdflib/extras/infixowl.py \
    %{buildroot}%{python3_sitelib}/rdflib/extras/external_graph_libs.py \
    %{buildroot}%{python3_sitelib}/rdflib/plugins/parsers/ntriples.py \
    %{buildroot}%{python3_sitelib}/rdflib/tools/rdfpipe.py \
    %{buildroot}%{python3_sitelib}/rdflib/plugins/parsers/notation3.py

%if %{with docs}
# generate html docs
PYTHONPATH=%{buildroot}%{python3_sitelib} sphinx-build-3 -b html -d docs/_build/doctree docs docs/_build/html
# remove the sphinx-build-3 leftovers
rm -rf docs/_build/html/.{doctrees,buildinfo}
%endif

%pyproject_save_files %{srcname}

%if %{with tests}
%check
%pytest -k "not rdflib and not rdflib.extras.infixowl and not \
            test_example and not test_suite and not \
            test_infix_owl_example1 and not test_context and not \
            test_service and not test_simple_not_null and not \
            test_sparqleval and not test_parser"
%endif

%files -n python%{python3_pkgversion}-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.md
%{_bindir}/csv2rdf
%{_bindir}/rdf2dot
%{_bindir}/rdfgraphisomorphism
%{_bindir}/rdfpipe
%{_bindir}/rdfs2dot

%if %{with docs}
%files -n python%{python3_pkgversion}-%{srcname}-docs
%license LICENSE
%doc docs/_build/html
%endif

%changelog
* Wed Feb 26 2025 Akhila Guruju <v-guakhila@microsoft.com> - 7.0.0-6
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 02 2024 Nils Philippsen <nils@tiptoe.de> - 7.0.0-4
- Fix testing with pytest 8

* Thu Jun 13 2024 Michel Lind <salimma@fedoraproject.org> - 7.0.0-3
- Work around inability to override Pickler/Unpickler methods in Python
  3.13

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 7.0.0-2
- Rebuilt for Python 3.13

* Sat May 25 2024 Robert-André Mauchin <zebob.m@gmail.com> - 7.0.0-1
- Update to 7.0.0
- Use current Python macros
- Run tests
- Build docs

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 6.2.0-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Aug 30 2022 Simone Caronni <negativo17@gmail.com> - 6.2.0-1
- Update to 6.2.0.
- Update SPEC file.
- Trim changelog.

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 5.0.0-6
- Rebuilt for pyparsing-3.0.9

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 5.0.0-5
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 5.0.0-2
- Rebuilt for Python 3.10

* Mon Feb 15 2021 Dan Callaghan <djc@djc.id.au> - 5.0.0-1
- New upstream release 5.0.0:
  https://github.com/RDFLib/rdflib/blob/5.0.0/CHANGELOG.md

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 4.2.1-15
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

## END: Generated by rpmautospec
