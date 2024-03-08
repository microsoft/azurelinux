%global srcname rdflib
Summary:        Python library for working with RDF
Name:           python-%{srcname}
Version:        6.2.0
Release:        2%{?dist}
License:        BSD-3-Clause
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/RDFLib/rdflib
Source0:        https://github.com/RDFLib/%{srcname}/releases/download/%{version}/%{srcname}-%{version}.tar.gz
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
Requires:       python3-importlib-metadata
Requires:       python3-isodate
Requires:       python3-pyparsing
Requires:       python3-setuptools
BuildArch:      noarch
%if 0%{?with_check}
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
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

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

# Various .py files within site-packages have a shebang line but aren't
# flagged as executable.
# I've gone through them and either removed the shebang or made them
# executable as appropriate:

# __main__ parses URI as N-Triples:
chmod +x %{buildroot}%{python3_sitelib}/rdflib/plugins/parsers/ntriples.py

# __main__ parses the file given on the command line:
chmod +x %{buildroot}%{python3_sitelib}/rdflib/plugins/parsers/notation3.py

# __main__ parses the file or URI given on the command line:
chmod +x %{buildroot}%{python3_sitelib}/rdflib/tools/rdfpipe.py

# __main__ runs a test (well, it's something)
chmod +x %{buildroot}%{python3_sitelib}/rdflib/extras/infixowl.py \
         %{buildroot}%{python3_sitelib}/rdflib/extras/external_graph_libs.py

# sed these headers out as they include no __main__
for lib in %{buildroot}%{python3_sitelib}/rdflib/extras/describer.py \
    %{buildroot}%{python3_sitelib}/rdflib/plugins/parsers/pyRdfa/extras/httpheader.py; do
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

%check
%{python3} -m pip install atomicwrites attrs more-itertools pluggy pytest-cov html5lib
%pytest -v test

%files -n python3-%{srcname}
%license LICENSE
%doc CHANGELOG.md README.md
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{srcname}-%{version}-py%{python3_version}.egg-info
%{_bindir}/csv2rdf
%{_bindir}/rdf2dot
%{_bindir}/rdfgraphisomorphism
%{_bindir}/rdfpipe
%{_bindir}/rdfs2dot

%changelog
* Wed Nov 23 2022 Sumedh Sharma <sumsharma@microsoft.com> - 6.2.0-2
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- License verified

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
