%global debug_package %{nil}
%global _binaries_in_noarch_packages_terminate_build   0

Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global srcname Genshi

Name:           python-genshi
Version:        0.7.5
Release:        4%{?dist}
Summary:        Toolkit for stream-based generation of output for the web

License:        BSD
URL:            https://genshi.edgewall.org/

Source0:        %pypi_source

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-six

%description
Genshi is a Python library that provides an integrated set of
components for parsing, generating, and processing HTML, XML or other
textual content for output generation on the web. The major feature is
a template language, which is heavily inspired by Kid.


%package -n python3-genshi
Summary:        %{summary}

%description -n python3-genshi
Genshi is a Python library that provides an integrated set of
components for parsing, generating, and processing HTML, XML or other
textual content for output generation on the web. The major feature is
a template language, which is heavily inspired by Kid.


%prep
%autosetup -p1 -n %{srcname}-%{version}

# Remove bundled egg-info in case it exists
rm -rf %{modname}.egg-info

find examples -type f | xargs chmod a-x


%build
%py3_build


%install
%py3_install
rm -r %{buildroot}%{python3_sitelib}/genshi/tests
rm -r %{buildroot}%{python3_sitelib}/genshi/{filters,template}/tests
rm %{buildroot}%{python3_sitelib}/genshi/*.c


%check
%{python3} setup.py test


%files -n python3-genshi
%license COPYING
%doc ChangeLog doc examples README.txt
%{python3_sitelib}/%{srcname}-%{version}-py*.egg-info/
%{python3_sitelib}/genshi/


%changelog
* Wed Mar 24 2021 Henry Li <lihl@microsoft.com> - 0.7.5-4
- Initial CBL-Mariner import from Fedora 34 (license: MIT).
- Disable debuginfo 
- Disable RPM complaining about shipping *.so binaries as noarch

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 21 2020 Miro Hrončok <mhroncok@redhat.com> - 0.7.5-2
- Drop python2-genshi

* Wed Nov 18 2020 Felix Schwarz <fschwarz@fedoraproject.org> - 0.7.5-1
- update to 0.7.5

* Wed Nov 04 2020 Felix Schwarz <fschwarz@fedoraproject.org> - 0.7.4-1
- update to 0.7.4

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 15 2020 Felix Schwarz <fschwarz@fedoraproject.org> - 0.7.3-7
- add patches for Python 3.9 compatibility

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.7.3-6
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.7.3-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 0.7.3-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 28 2019 Felix Schwarz <fschwarz@fedoraproject.org> - 0.7.3-1
- update to new upstream version 0.7.3

* Mon Apr 29 2019 Felix Schwarz <fschwarz@fedoraproject.org> - 0.7.2-1
- update to new upstream version 0.7.2

* Mon Feb 04 2019 Felix Schwarz <fschwarz@fedoraproject.org> - 0.7.1-1
- update to new upstream version 0.7.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Miro Hrončok <mhroncok@redhat.com> - 0.7-21
- Rebuilt for Python 3.7

* Fri Jun 29 2018 Felix Schwarz <fschwarz@fedoraproject.org> - 0.7-20
- add patches for Python 3.7 compatibility

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.7-19
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 26 2016 Felix Schwarz <fschwarz@fedoraproject.org> - 0.7-14
- update spec file to match Fedora's Python2/3 package versioning policies

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.7-13
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-12
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 13 2015 Felix Schwarz <fschwarz@fedoraproject.org> - 0.7-10
- add patch for Python 3.5 (Genshi bug 602)
- use license macro

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-9
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Nov 12 2014 Felix Schwarz <fschwarz@fedoraproject.org> - 0.7-7
- fix dependency on python3-babel (bz 1163067)

* Thu Oct 30 2014 Felix Schwarz <fschwarz@fedoraproject.org> - 0.7-6
- fix tests on Python 2.7.8 (RHBZ 1106778)
- enable python3 subpackage again as we have Babel 1.3 now in the repos

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 10 2013 Luke Macken <lmacken@redhat.com> - 0.7-2
- Disable the python3 subpackage until python-babel is ported

* Tue Apr  9 2013 Luke Macken <lmacken@redhat.com> - 0.7-1
- Update to 0.7
- Add a python3 subpackage

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 18 2010 Luke Macken <lmacken@redhat.com> - 0.6-2
- Build with the optional C speed-enhancements

* Sun Aug 22 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.6-1
- Version 0.6
- https://svn.edgewall.org/repos/genshi/tags/0.6.0/
- (Apr 22 2010, from branches/stable/0.6.x)
-
-  * Support for Python 2.3 has been dropped.
-  * Rewrite of the XPath evaluation engine for better performance and improved
-    correctness. This is the result of integrating work done by Marcin Kurczych
-    during GSoC 2008.
-  * Updated the Python AST processing for template code evaluation to use the
-    `_ast` module instead of the deprecated `compiler` package, including an
-    adapter layer for Python 2.4. This, too, is the result of integrating work
-    done by  Marcin Kurczych during GSoC 2008.
-  * Added caching in the serialization stage for improved performance in some
-    cases.
-  * Various improvements to the HTML sanitization filter.
-  * Fix problem with I18n filter that would get confused by expressions in
-    attribute values when inside an `i18n:msg` block (ticket #250).
-  * Fix problem with the transformation filter dropping events after the
-    selection (ticket #290).
-  * `for` loops in template code blocks no longer establish their own locals
-    scope, meaning you can now access variables assigned in the loop outside
-    of the loop, just as you can in regular Python code (ticket #259).
-  * Import statements inside function definitions in template code blocks no
-    longer result in an UndefinedError when the imported name is accessed
-    (ticket #276).
-  * Fixed handling of relative URLs with fragment identifiers containing colons
-    in the `HTMLSanitizer` (ticket #274).
-  * Added an option to the `HTMLFiller` to also populate password fields.
-  * Match template processing no longer produces unwanted duplicate output in
-    some cases (ticket #254).
-  * Templates instantiated without a loader now get an implicit loader based on
-    their file path, or the current directory as a fallback (ticket #320).
-  * Added documentation for the `TemplateLoader`.
-  * Enhanced documentation for internationalization.

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.5.1-8
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Sep 11 2009 Luke Macken <lmacken@redhat.com> - 0.5.1-7
- Add a patch to work around some recent Python2.6.2 behavior

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 01 2009 Luke Macken <lmacken@redhat.com> - 0.5.1-5
- Add python-babel as a requirement

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.5.1-3
- Rebuild for Python 2.6

* Thu Oct  9 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.5.1-2
- Add patch from upstream that fixes problems when using Genshi in
- conjuction with Babel.

* Tue Oct  7 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.5.1-1
- Version 0.5.1
- https://svn.edgewall.org/repos/genshi/tags/0.5.1/
- (Jul 9 2008, from branches/stable/0.5.x)
- 
-  * Fix problem with nested match templates not being applied when buffering
-    on the outer `py:match` is disabled. Thanks to Erik Bray for reporting the
-    problem and providing a test case!
-  * Fix problem in `Translator` filter that would cause the translation of
-    text nodes to fail if the translation function returned an object that was
-    not directly a string, but rather something like an instance of the
-    `LazyProxy` class in Babel (ticket #145).
-  * Fix problem with match templates incorrectly being applied multiple times.
-  * Includes from templates loaded via an absolute path now include the correct
-    file in nested directories as long if no search path has been configured
-    (ticket #240).
-  * Unbuffered match templates could result in parts of the matched content
-    being included in the output if the match template didn't actually consume
-    it via one or more calls to the `select()` function (ticket #243).

* Mon Jun  9 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.5-1
- Update to released version of Genshi.

* Thu Apr 24 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.5-0.1.svn847
- Update to snapshot of 0.5

* Tue Aug 28 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.4.4-2
- BR python-setuptools-devel

* Mon Aug 27 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.4.4-1
- Update to 0.4.4

* Mon Jul  9 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.4.2-2
- BR python-setuptools so that egg-info files get installed.  Fixes #247430.

* Thu Jun 21 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.4.2-1
- Update to 0.4.2

* Sat Jun  9 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.4.1-1
- Update to 0.4.1

* Wed Apr 18 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.4.0-1
- Update to 0.4.0

* Thu Apr 12 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.3.6-1
- First version for Fedora Extras

