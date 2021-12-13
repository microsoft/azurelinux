Vendor:         Microsoft Corporation
Distribution:   Mariner
%define realname bytesize
%define with_python3 1
%define with_gtk_doc 1
%define with_tools 1

%if %{with_tools} != 1
%define tools_opts --without-tools
%endif

%define configure_opts %{?python3_opts} %{?tools_opts}

Name:        libbytesize
Version:     2.5
Release:     2%{?dist}
Summary:     A library for working with sizes in bytes
License:     LGPLv2+
URL:         https://github.com/storaged-project/libbytesize
Source0:     https://github.com/storaged-project/libbytesize/releases/download/%{version}-%{release}/%{name}-%{version}.tar.gz

BuildRequires: gcc
BuildRequires: gmp-devel
BuildRequires: mpfr-devel
BuildRequires: pcre2-devel
BuildRequires: gettext-devel
%if %{with_python3}
BuildRequires: python3-devel
%endif
%if %{with_gtk_doc}
BuildRequires: gtk-doc
%endif

%description
The libbytesize is a C library that facilitates work with sizes in
bytes. Be it parsing the input from users or producing a nice human readable
representation of a size in bytes this library takes localization into
account. It also provides support for sizes bigger than MAXUINT64.

%package devel
Summary:  Development files for libbytesize
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains header files and pkg-config files needed for development
with the libbytesize library.

%if %{with_python3}
%package -n python3-%{realname}
Summary: Python 3 bindings for libbytesize
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: python3-six

%description -n python3-%{realname}
This package contains Python 3 bindings for libbytesize making the use of
the library from Python 3 easier and more convenient.
%endif

%if %{with_tools}
%package tools
Summary: Various nice tools based on libbytesize
Requires: python3-%{realname} = %{version}-%{release}

%description tools
Various nice tools based on libbytesize, in particular the calculator
for doing calculations with storage sizes.
%endif

%prep
%setup -q -n %{name}-%{version}

%build
%configure %{?configure_opts}
%{__make} %{?_smp_mflags}

%install
%{make_install}
find %{buildroot} -type f -name "*.la" | xargs %{__rm}
%find_lang %{name}


%ldconfig_scriptlets


%files -f %{name}.lang
%doc README.md
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_libdir}/libbytesize.so.*

%files devel
%{_libdir}/libbytesize.so
%dir %{_includedir}/bytesize
%{_includedir}/bytesize/bs_size.h
%{_libdir}/pkgconfig/bytesize.pc
%if %{with_gtk_doc}
%{_datadir}/gtk-doc/html/libbytesize
%endif

%if %{with_python3}
%files -n python3-%{realname}
%dir %{python3_sitearch}/bytesize
%{python3_sitearch}/bytesize/*
%endif

%if %{with_tools}
%files tools
%{_bindir}/bscalc
%{_mandir}/man1/bscalc.1*
%endif

%changelog
* Thu Mar 04 2021 Henry Li <lihl@microsoft.com> - 2.5-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove condition checking that does not apply to CBL-Mariner

* Wed Jan 27 2021 Vojtech Trefny <vtrefny@redhat.com> - 2.5-1
- Translated using Weblate (Hebrew) (sh.yaron)
- Added translation using Weblate (Hebrew) (sh.yaron)
- Add support to ppc64le for debian build (74309971+gururajrkatti)
- Translated using Weblate (Finnish) (ricky.tigg)
- tools: Read input from stdin when not running in a tty (vtrefny)
- travis: Print logs after failed tests (vtrefny)
- tests: Run pylint and pycodestyle on bscalc (vtrefny)
- bscalc: Add option to print only single "human readable" result (vtrefny)
- travis: Add --nogpgcheck when using dnf on Fedora (vtrefny)
- Translated using Weblate (Asturian) (fitoschido)
- Update translation files (noreply)
- Translated using Weblate (Spanish) (fitoschido)
- Sync spec with downstream (vtrefny)

* Fri Jul 31 2020 Vojtech Trefny <vtrefny@redhat.com> - 2.4-1
- Add Travis build status badge (vtrefny)
- Add Travis CI config and Dockerfiles for running tests (vtrefny)
- Add ansible playbook for installing test dependencies (vtrefny)
- remove msgcat dependency (Aduskett)
- Translated using Weblate (Bengali (India)) (akarshan.biswas)
- Update translation files (noreply)
- Added translation using Weblate (Bengali (India)) (akarshan.biswas)
- Fix library version in pkgconfig file (vtrefny)

* Thu May 21 2020 Vojtech Trefny <vtrefny@redhat.com> - 2.3-1
- Fix memory leak in bs_size_new_from_str (vtrefny)
- Translated using Weblate (Turkish) (oguzersen)
- add translation platform widget (jean-baptiste)
- Update translation files (noreply)
- Do not regenerate POT file during 'make release' (vtrefny)
- Remove Zanata from our build and release processes (vtrefny)
- Add PO files to git (vtrefny)
- Sync spec with downstream (vtrefny)

* Thu Jan 30 2020 Vojtech Trefny <vtrefny@redhat.com> - 2.2-1
- Require the same version of python3-bytesize in libbytesize-tools (v.podzimek)
- src/gettext: fix warning if gettext is already present (giulio.benetti)
- Update README.md (vpodzime)
- fix build on shells where test == fails (tbier)
- Add POT file to git and do not rebuild it during every build (vtrefny)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct  9 2019 Jerry James <loganjerry@gmail.com> - 2.1-5
- Rebuild for mpfr 4

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.1-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 2.1-3
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 03 2019 Vojtech Trefny <vtrefny@redhat.com> - 2.1-1
- fix out of tree build failure (hongxu.jia)
- Fix return value for round_to_nearest when using Size (vtrefny)

* Thu Apr 25 2019 Vojtech Trefny <vtrefny@redhat.com> - 2.0-1
- Assume the given expression is in bytes if no unit is given (v.podzimek)
- Add a man page for the bscalc tool (v.podzimek)
- Add the '--version' option to bs_calc.py (v.podzimek)
- Fix parsing of exponential representations of real numbers (v.podzimek)
- Only support modulo between two Size instances (v.podzimek)
- Add a summary to the end of ./configure output (v.podzimek)
- Exit with 1 from configure if there were failures (v.podzimek)
- Add tools to autotools and packaging (v.podzimek)
- Add a simple bytesize calculator tool (v.podzimek)
- Add support for floor division by a non-integer number in Python (v.podzimek)
- Port to pcre2 (vtrefny)
- Remove Python 2 support (vtrefny)
- Allow running tests using installed library (vtrefny)
- Add all "public" python API  symbols to __init__.py (vtrefny)
- Run all libbytesize tests from one script (vtrefny)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug 02 2018 Vojtech Trefny <vtrefny@redhat.com> - 1.4-1
- Squashed 'translation-canary/' changes from 840c2d6..fccbb1b (vtrefny)
- Make sure the test script fails if one of the test runs fail (vtrefny)
- Do not try to run python2 tests without python2 support (vtrefny)
- Fix licence header for "gettext.h" (vtrefny)
- Do not use rpm to check for Zanata client (vtrefny)
- Use new ldconfig_scriptlets macro in spec (vtrefny)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 1.3-4
- Rebuilt for Python 3.7

* Fri Jun 29 2018 Vojtech Trefny <vtrefny@redhat.com> - 1.3-3
- Use new ldconfig_scriptlets macro in spec

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 1.3-2
- Rebuilt for Python 3.7

* Thu Apr 19 2018 Vojtech Trefny <vtrefny@redhat.com> - 1.3-1
- Allow building libbytesize without Python 2 support (vtrefny)
- Sync spec with downstream (vtrefny)
- Add gcc to BuildRequires (vtrefny)
- Fix links for documentation and GH project (vtrefny)
- Add a HACKING.rst file (vpodzime)
- Do not segfault when trying to bs_size_free NULL (vtrefny)

* Wed Feb 21 2018 Vojtech Trefny <vtrefny@redhat.com> - 1.2-4
- Add gcc to BuildRequires (vtrefny)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 05 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.2-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Sep 29 2017 Vratislav Podzimek <vpodzime@redhat.com> - 1.2-1
- Use only version as a tag of the last release (vpodzime)
- Do not require the glib-2.0 pkgconfig package (vpodzime)
- Do not lie about tag creation (vpodzime)

* Thu Sep 28 2017 Troy Dawson <tdawson@redhat.com> - 1.1-2
- Cleanup spec file conditionals

* Thu Sep 21 2017 Vratislav Podzimek <vpodzime@redhat.com> - 1.1-1
- Add NEWS.rst file (vtrefny)
- Fix source and url in spec file (vtrefny)
- Use only one git tag for new releases (vtrefny)
- Actually translate the units when expected (vpodzime)
- Add two temporary test files to .gitignore (vpodzime)

* Thu Sep 14 2017 Vratislav Podzimek <vpodzime@redhat.com> - 1.0-1
- Make more space for CI status image (vtrefny)
- Include limits.h to make sure ULONG_MAX is defined (vpodzime)
- Remove extra 'is' in two docstrings (vpodzime)
- Properly support 64bit operands (vpodzime)

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.11-4
- Python 2 binary package renamed to python2-libbytesize
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 14 2017 Vratislav Podzimek <vpodzime@redhat.com> - 0.11-1
- Fix README file name (vtrefny)
- Add a build status image to the README.md (vpodzime)
- Remove "glibc-all-langpacks" from test dependencies (vtrefny)
- Check for requires in generated spec file, not in the template (vtrefny)
- Fix checking for available locales (vtrefny)
- Fix library name in acinclude.m4 (vtrefny)
- Do not try to run translation tests on CentOS/RHEL 7 (vtrefny)
- Skip tests if they require unavailable locales (vpodzime)

* Wed Apr 19 2017 Vratislav Podzimek <vpodzime@redhat.com> - 0.10-1
- Fix installation without specifying --exec-prefix (martin)
- Sync the spec file with downstream (vpodzime)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 11 2017 Vratislav Podzimek <vpodzime@redhat.com> - 0.9-1
- Allow the Size python class to be easily imported (vpodzime)
- Make sure pyexecdir is defined (vpodzime)
- Do not run Python 3 tests without python3 (vpodzime)
- Disable python3 on RHEL (vpodzime)
- Reflect the configuration in the spec file template (vpodzime)
- Make documentation generation conditional (vpodzime)
- Make python3 support conditional (vpodzime)
- Require lower version of libpcre (vpodzime)
- Sync the spec file with downstream (vpodzime)

* Wed Dec 21 2016 Adam Williamson <awilliam@redhat.com> - 0.8-2
- Rebuild for Python 3.6, again

* Fri Dec 16 2016 Vratislav Podzimek <vpodzime@redhat.com> - 0.8-1
- Add a docstring to python bindings (vpodzime)
- Neutralize None as an operand for math operations (vpodzime)
- Add targets for checking and installing test requirements (vpodzime)
- Fix 'make local' (vtrefny)
- Make the python packages own their package directories (vpodzime)
- Don't compare translated and untranslated representations (vpodzime)
- replace_char_with_str: Fix the character count. (dshea)
- Ditch autopoint. (dshea)

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.7-4
- Rebuild for Python 3.6

* Tue Sep 20 2016 Vratislav Podzimek <vpodzime@redhat.com> - 0.7-3
- Prevent ignored exceptions in __del__ from happening (vpodzime)

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue May 17 2016 Vratislav Podzimek <vpodzime@redhat.com> - 0.7-1
- Re-run autogen.sh and configure before updating the .pot file (vpodzime)
- Change where tests on translated strings are run. (dshea)
- Squashed 'translation-canary/' changes from d6c0708..840c2d6 (dshea)
- Make sure we get the tests result report in 'make ci' (vpodzime)
- Add a new generic error code/enum for failures (vpodzime)
- Do not ignore the return value from asprintf() (vpodzime)
- Beware of the radix char when converting to Decimal (#1325705) (vpodzime)

* Fri May  6 2016 Vratislav Podzimek <vpodzime@redhat.com> - 0.6-2
- Beware of unsigned long int on 32bit arches (#1333149) (vpodzime)

* Tue May 03 2016 Vratislav Podzimek <vpodzime@redhat.com> - 0.6-1
- Add support for the ROUND_HALF_UP rounding mode (vpodzime)
- Make sure we return the right radix char in human_readable() (vpodzime)
- Allocate enough memory for char->str replacements (vpodzime)

* Tue Apr 26 2016 Vratislav Podzimek <vpodzime@redhat.com> - 0.5-1
- Create both libbytesize-$version and $version tags (vpodzime)
- Update the .pot file with the new version (vpodzime)
- Improve how we create changelog (vpodzime)
- Try harder when getting OverflowError in division (#1326897) (vpodzime)
- Neutralize the radix char before passing string to MPFR (#1326108) (vpodzime)
- Run tests with en_US and fr_FR locales (vpodzime)
- Run the tests with both python2 and python3 again (vpodzime)
- Do not run the same tests 3 times as part of the 'ci' target (vpodzime)
- Don't fail if just the best-effort cleanup fails (vpodzime)
- Throw away the new .pot file when just running tests (vpodzime)
- Make sure we return one of -1, 0, 1 from cmp functions (#1326113) (vpodzime)
- Use cmp_bytes(size, bytes) when comparing to 0 (vpodzime)
- Ignore all .po~ files (vpodzime)
- Add translator comments (dshea)
- Integrate translation-canary into the build. (dshea)
- Run the translation-canary tests from make check. (dshea)
- Squashed 'translation-canary/' content from commit d6c0708 (dshea)
- Make 'make check' work. (dshea)
- Remove files from po/ we don't need to track (vpodzime)
- Ignore the compiled translation files (vpodzime)
- Distribute and package the translations (vpodzime)
- Add the necessary pieces for getting translations (vpodzime)

* Thu Apr 14 2016 Vratislav Podzimek <vpodzime@redhat.com> - 0.4-3
- Only require -lgmp and -lmpfr for static linking (vpodzime)

* Fri Mar 11 2016 Vratislav Podzimek <vpodzime@redhat.com> - 0.4-2
- Do not try to delete the C struct twice (vpodzime)

* Wed Mar 09 2016 Vratislav Podzimek <vpodzime@redhat.com> - 0.4-1
- Add the __init__.py file to provide a proper package (vpodzime)
- Merge pull request #7 from vpodzime/master-decimal_locale (vpodzime)
- Make sure we pass a locale-agnostic string to Decimal() (vpodzime)
- Adapt the package description to no longer using GI (vpodzime)
- Make Size instances hashable (vpodzime)
- Sync the spec file with downstream (vpodzime)

* Wed Mar  9 2016 Vratislav Podzimek <vpodzime@redhat.com> - 0.3-3
- Make sure we pass a locale-agnostic string to Decimal() (vpodzime)

* Mon Mar  7 2016 Vratislav Podzimek <vpodzime@redhat.com> - 0.3-2
- Make Size instances hashable (vpodzime)

* Fri Feb 26 2016 Vratislav Podzimek <vpodzime@redhat.com> - 0.3-1
- Packaging changes related to getting rid of GLib/GObject (vpodzime)
- Adapt the python bindings and tests (vpodzime)
- Get rid of GObject and GLib (vpodzime)
- Define the __divmod__ method even for not dividing by Size (vpodzime)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Oct 23 2015 Vratislav Podzimek <vpodzime@redhat.com> - 0.2-1
- Distribute the tests for overrides (vpodzime)
- Fix the rpmlog target (vpodzime)
- Respect the signs when doing division (vpodzime)
- Add two more internal methods that may be required (vpodzime)
- Do not pass negative numbers as guint64 when comparing with negative ints (vpodzime)
- Round toward zero when converting bytes from float to int (vpodzime)
- Make sure we return Size if doing operations with big integers (vpodzime)
- Implement the __divmod__() method (vpodzime)
- Do not try to convert negative int to an unsigned int when multiplying (vpodzime)
- Fix and test the __deepcopy__ method (vpodzime)
- Implement the evaluation of Size instance as a bool value (vpodzime)
- Fix some issues in comparison functions and add tests (vpodzime)
- Add a function for getting string representation of a unit (vpodzime)
- Hook the overrides tests to the 'test' target (vpodzime)
- Merge pull request #4 from japokorn/master-tests_03_python_override (vpodzime)
- Added tests for Python override (japokorn)
- Make sure our tests don't get broken by installed overrides (vpodzime)

* Wed Oct 07 2015 Vratislav Podzimek <vpodzime@redhat.com> - 0.1-1
- Initial release
