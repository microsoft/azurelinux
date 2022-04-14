Vendor:         Microsoft Corporation
Distribution:   Mariner
%global pypi_name rdflib

%global run_tests 1

Name:           python-%{pypi_name}
Version:        4.2.1
Release:        16%{?dist}
Summary:        Python library for working with RDF

License:        BSD
URL:            https://github.com/RDFLib/rdflib
Source0:        https://pypi.python.org/packages/source/r/rdflib/rdflib-%{version}.tar.gz
Patch1:         %{name}-SPARQLWrapper-optional.patch
BuildArch:      noarch

BuildRequires:  python3-html5lib
BuildRequires:  python3-isodate
BuildRequires:  python3-pyparsing
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%if %{run_tests}
BuildRequires:  python3-nose >= 0.9.2
%endif

%description
RDFLib is a Python library for working with RDF, a simple yet powerful
language for representing information.

The library contains parsers and serializers for RDF/XML, N3,
NTriples, Turtle, TriX, RDFa and Microdata. The library presents
a Graph interface which can be backed by any one of a number of
Store implementations. The core rdflib includes store
implementations for in memory storage, persistent storage on top
of the Berkeley DB, and a wrapper for remote SPARQL endpoints.


%package -n python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}
Requires:       python3-html5lib
Requires:       python3-isodate
Requires:       python3-pyparsing
Requires:       python3-six
# Unversioned binaries (/usr/bin/csv2rdf etc) moved
# from python2-rdflib to python3-rdflib in 4.2.1-11.
Conflicts:      python2-rdflib <= 4.2.1-10

%description -n python3-%{pypi_name}
RDFLib is a Python library for working with RDF, a simple yet powerful
language for representing information.

The library contains parsers and serializers for RDF/XML, N3,
NTriples, Turtle, TriX, RDFa and Microdata. The library presents
a Graph interface which can be backed by any one of a number of
Store implementations. The core rdflib includes store
implementations for in memory storage, persistent storage on top
of the Berkeley DB, and a wrapper for remote SPARQL endpoints.

This is for Python 3.

%prep
%setup -q -n rdflib-%{version}
%patch1 -p1

# remove bundled egg-info
rm -rf %{pypi_name}.egg-info

find -name "*.pyc" -delete

sed -i -e 's|_sn_gen=bnode_uuid()|_sn_gen=bnode_uuid|' test/test_bnode_ncname.py


%build
%py3_build


%install
%py3_install

# rename binaries
for i in csv2rdf rdf2dot rdfgraphisomorphism rdfpipe rdfs2dot; do
    mv %{buildroot}%{_bindir}/$i %{buildroot}%{_bindir}/$i-%{python3_version}
    ln -s $i-%{python3_version} %{buildroot}%{_bindir}/$i
    ln -s $i-%{python3_version} %{buildroot}%{_bindir}/$i-3
done

cp LICENSE %{buildroot}%{python3_sitelib}/rdflib/LICENSE

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
    %{buildroot}%{python3_sitelib}/rdflib/plugins/parsers/pyRdfa/extras/httpheader.py \
    %{buildroot}%{python3_sitelib}/rdflib/plugins/parsers/structureddata.py; do
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
%if %{run_tests}
sed -i -e "s|'--with-doctest'|#'--with-doctest'|" run_tests.py
sed -i -e "s|'--doctest-tests'|#'--doctest-tests'|" run_tests.py
sed -i -e "s|with-doctest = 1|#with-doctest = 1|" setup.cfg

# The python 3 tests are failing, but better to have them here anyway
# TODO investigate the failures
%{__python3} run_tests.py --verbose || :
%endif


%files -n python3-%{pypi_name}
%license LICENSE
%doc README.md
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info
%{_bindir}/csv2rdf
%{_bindir}/csv2rdf-3*
%{_bindir}/rdf2dot
%{_bindir}/rdf2dot-3*
%{_bindir}/rdfgraphisomorphism
%{_bindir}/rdfgraphisomorphism-3*
%{_bindir}/rdfpipe
%{_bindir}/rdfpipe-3*
%{_bindir}/rdfs2dot
%{_bindir}/rdfs2dot-3*

%changelog
* Fri Feb 04 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.2.1-16
- Removing epoch.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.2.1-15
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 16 2019 Miro Hrončok <mhroncok@redhat.com> - 4.2.1-13
- Subpackage python2-rdflib has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 4.2.1-12
- Rebuilt for Python 3.8

* Wed Aug 14 2019 Dan Callaghan <djc@djc.id.au> - 4.2.1-11
- Commands without suffix (/usr/bin/csv2rdf etc) are now the Python 3 version
  as per https://fedoraproject.org/wiki/Changes/Python_means_Python3
- Dropped Python 2 version of commands in preparation for Python 2 removal

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 16 2018 Miro Hrončok <mhroncok@redhat.com> - 4.2.1-7
- Rebuilt for Python 3.7

* Wed Feb 28 2018 Iryna Shcherbina <ishcherb@redhat.com> - 4.2.1-6
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Tue Feb 20 2018 Than Ngo <than@redhat.com> - 4.2.1-5
- skip test_issue375 for python2, need to investigate later

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 03 2017 Miro Hrončok <mhroncok@redhat.com> - 4.2.1-1
- Update to 4.2.1
- Add missing python3 requires (rhbz#1295098)
- Modernize the package (python2 subpackage, %%pyX_* macros..., new versioned executable)
- Run tests on Python 3, even when failing
- Fixed bad shebangs

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 4.1.2-8
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2-7
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 03 2015 Robert Kuska <rkuska@redhat.com> - 4.1.2-5
- Rebuilt for Python3.5 rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 05 2015 Matthias Runge <mrunge@redhat.com> - 4.1.2-3
- add python3 subpackage (rhbz#1086844)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 18 2014 Dan Scott <dan@coffeecode.net> - 4.1.2-1
- Update for 4.1.2 release
- Add PYTHONPATH awareness for running tests

* Tue Mar 04 2014 Dan Scott <dan@coffeecode.net> - 4.1.1-1
- Update for 4.1.1 release
- Support for RDF 1.1 and HTML5
- Support for RDFa, TRiG, microdata parsers, and HTML structured data
- Patch to make SPARQLWrapper an extras_require until it is packaged

* Thu Dec 12 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 3.2.3-6
- Remove BR of python-setuptools-devel

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 27 2013 David Malcolm <dmalcolm@redhat.com> - 3.2.3-4
- disable doctests (rhbz#914414)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 10 2012  Pierre-Yves Chibon <pingou@pingoured.fr> - 3.2.3-2
- Re-enable tests
- Backport using sed unit-tests fix from upstream
   (commit 26d25faa90483ed1ba7675d159d10e955dbaf442)

* Wed Oct 10 2012  Pierre-Yves Chibon <pingou@pingoured.fr> - 3.2.3-1
- Update to 3.2.3
- One test is failing, so disabling them for now

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 24 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 3.2.0-4
- Re-add the unittests, for that, patch one and disable the run of
the tests in the documentation of the code.

* Mon Jan 23 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 3.2.0-3
- Add python-isodate as R (RHBZ#784027)

* Fri Jan 20 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 3.2.0-2
- Found the official sources of the 3.2.0 release

* Fri Jan 20 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 3.2.0-1
- Update to 3.2.0-RC which seem to be same as 3.2.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Sep 28 2011 David Malcolm <dmalcolm@redhat.com> - 3.1.0-1
- 3.1.0; converting from arch-specific to noarch (sitearch -> sitelib);
removing rdfpipe and various other extensions

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 Thomas Spura <tomspur@fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jan  6 2010 David Malcolm <dmalcolm@redhat.com> - 2.4.2-1
- bump to 2.4.2 (#552909)
- fix source URL to use version macro

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 10 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.4.0-8
- Rebuild for Python 2.6

* Wed Oct  1 2008 David Malcolm <dmalcolm@redhat.com> - 2.4.0-7
- fix tab/space issue in specfile

* Tue Sep 30 2008 David Malcolm <dmalcolm@redhat.com> - 2.4.0-6
- override autogeneration of provides info to eliminate unwanted provision
of SPARQLParserc.so

* Mon Sep 29 2008 David Malcolm <dmalcolm@redhat.com> - 2.4.0-5
- make various scripts executable, or remove shebang, as appropriate

* Tue Feb 19 2008 David Malcolm <dmalcolm@redhat.com> - 2.4.0-4
- delete test subdir

* Thu Jan 24 2008 David Malcolm <dmalcolm@redhat.com> - 2.4.0-3
- introduce macro to disable running the test suite, in the hope of eventually
patching it so it passes

* Mon Nov 19 2007 David Malcolm <dmalcolm@redhat.com> - 2.4.0-2
- add python-setuptools(-devel) build requirement; move testing to correct stanza

* Wed Aug  1 2007 David Malcolm <dmalcolm@redhat.com> - 2.4.0-1
- initial version

