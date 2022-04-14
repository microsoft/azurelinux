Vendor:         Microsoft Corporation
Distribution:   Mariner
%global libreportver 2.0.18-1

Summary:  A python library for handling exceptions
Name: python-meh
Url: https://github.com/rhinstaller/python-meh
Version: 0.48
Release: 3%{?dist}
# This is a Red Hat maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.
# This tarball was created from upstream git:
#   git clone https://github.com/rhinstaller/python-meh
#   cd python-meh && make archive
Source0: https://github.com/rhinstaller/python-meh/archive/%{name}-%{version}.tar.gz

License: GPLv2+
BuildArch: noarch
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: libreport-cli >= %{libreportver}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-dbus
BuildRequires: python3-libreport >= %{libreportver}

%global _description\
The python-meh package is a python library for handling, saving, and reporting \
exceptions.

%description %_description

%package -n python3-meh
Summary:  A python 3 library for handling exceptions
%{?python_provide:%python_provide python3-meh}
Obsoletes: python-meh < 0.46-1
Obsoletes: python2-meh < 0.46-1
Requires: python3
Requires: python3-dbus
Requires: python3-rpm
Requires: libreport-cli >= %{libreportver}
Requires: python3-libreport >= %{libreportver}

%description -n python3-meh
The python3-meh package is a python 3 library for handling, saving, and reporting
exceptions.

%package -n python3-meh-gui
Summary: Graphical user interface for the python3-meh library
%{?python_provide:%python_provide python3-meh-gui}
Obsoletes: python-meh-gui < 0.46-1
Obsoletes: python2-meh-gui < 0.46-1
Requires: python3-meh = %{version}-%{release}
Requires: python3-gobject

%description -n python3-meh-gui
The python3-meh-gui package provides a GUI for the python3-meh library.

%prep
%setup -q

%build
make

%check
make test

%install
make DESTDIR=%{buildroot} install

%find_lang %{name}

%files -n python3-meh -f %{name}.lang
%doc ChangeLog COPYING
%{python3_sitelib}/*
%exclude %{python3_sitelib}/meh/ui/gui.py*
%exclude %{python3_sitelib}/meh/ui/__pycache__/gui.*

%files -n python3-meh-gui
%{python3_sitelib}/meh/ui/gui.py*
%{python3_sitelib}/meh/ui/__pycache__/gui.*
%{_datadir}/python-meh

%changelog
* Tue Mar 02 2021 Henry Li <lihl@microsoft.com> - 0.48-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove gtk3 and libreport-gtk from build dependencies

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 23 2019 Martin Kolman <mkolman@redhat.com> - 0.48-1
- Merge pull request #23 from poncovka/master-decode_bytes (mkolman)
- Handle bytes and strings from RPM (#1764642) (vponcova)

* Mon Jul 23 2018 Martin Kolman <mkolman@redhat.com> - 0.47-1
- Make sure gettext returns strings not bytes (mkolman)
- Spec: Move TUI back to main package (awilliam)

* Wed Feb 14 2018 Adam Williamson <awilliam@redhat.com> - 0.46-2
- Move TUI back to main package (inadvertently moved to -gui in 0.46-1)

* Mon Feb 12 2018 Martin Kolman <mkolman@redhat.com> - 0.46-1
- Drop Python 2 support (mkolman)

* Tue May 23 2017 Martin Kolman <mkolman@redhat.com> - 0.45-1
- update translations (mkolman)

* Fri Feb 19 2016 Martin Kolman <mkolman@redhat.com> - 0.44-1
- Some rpmlint fixes (mkolman)
- Remove the removal of the eintr checker, which has been removed (dshea)

* Mon Oct 05 2015 Martin Kolman <mkolman@redhat.com> - 0.43-1
- Set translations domain for glade files (vtrefny)

* Tue Sep 29 2015 Martin Kolman <mkolman@redhat.com> - 0.42-1
- Add tests and ChangeLog to MANIFEST.in (vtrefny)
- Fix clicking on buttons on error pop-up doesn't work (#1250942) (vtrefny)
- Add Makefile to MANIFEST.in (vtrefny)
- Add archive target to Makefile (vtrefny)
- Add .gitignore (vtrefny)

* Wed Sep 16 2015 Martin Kolman <mkolman@redhat.com> - 0.41-1
- Make sure the Meh window has focus even if a dialog is displayed (mkolman)
- Run pylint as part of "make ci". (clumens)
- Add a new makefile target that does everything needed for jenkins. (clumens)
- Fix the other pylint-discovered errors. (clumens)
- Use isinstance instead of type. (clumens)
- Fix all the places we're redefining something. (clumens)
- Don't use [] as the default argument in a method. (clumens)
- Take care of exception-related pylint messages. (clumens)
- Get rid of all the unused variable warnings. (clumens)
- Get rid of all unused and wildcard imports. (clumens)
- Add pocketlint support to python-meh. (clumens)
- Use gi.require_version for Gtk import (vtrefny)

* Tue Apr 28 2015 Martin Kolman <mkolman@redhat.com> - 0.40-1
- Make sure the date in RPM changelog is always in English (mkolman)
- Update upstream URL (mkolman)

* Wed Apr 01 2015 Martin Kolman <mkolman@redhat.com> - 0.39-1
- Handle LANG=C (mkolman)

* Tue Mar 31 2015 Martin Kolman <mkolman@redhat.com> - 0.38-1
- Switch to Zanata for translations (mkolman)
- Run both Python 2 and Python 3 tests for "make test" (mkolman)
- Python 3 compatibility fixes for the Unicode test (mkolman)
- Make it possible to specify file open mode (mkolman)
- Add missing six dependency (mkolman)
- Fix date in changelog (mkolman)

* Fri Mar 27 2015 Martin Kolman <mkolman@redhat.com> - 0.37-1
- Fix dumping file attachments in Python 3 (vtrefny)
- meh has not required openssh-clients since 2009 (awilliam)

* Thu Mar 05 2015 Martin Kolman <mkolman@redhat.com> - 0.36-1
- Package's epoch returned by RPM is an integer (#1199263) (vpodzime)

* Tue Feb 17 2015 Martin Kolman <mkolman@redhat.com> - 0.35-1
- Add option to remove the 'Debug' option/button for mainExceptionWindow (vtrefny)

* Tue Dec 09 2014 Vratislav Podzimek <vpodzime@redhat.com> - 0.34-1
- Encode str/unicode object before hashing it (vpodzime)
- Use dict.items() instead of dict.iteritems() (vpodzime)
- Add one more flag to test (for Python3) (vpodzime)
- Make sure we work with strings when we think we do (vpodzime)

* Fri Dec 05 2014 Vratislav Podzimek <vpodzime@redhat.com> - 0.33-1
- Make sure fresh translations are always fetched (vpodzime)
- Add pieces needed to build the python3- subpackage (#985294) (mhroncok)
- Remove yum from requires and fix setuptools requires (mhroncok)
- raw_input is replaced by input in Python3 (vpodzime)
- Raise exception in a Python3 compatible way (mhroncok)
- Remove the --disable-overwrite parameter for the Transifex client (mkolman)
- Use /usr/bin/python2 in scripts (mkolman)
- Add example code using python-meh (vpodzime)

* Mon Apr 28 2014 Martin Kolman <mkolman@redhat.com> - 0.32-1
- Translation update

* Fri Mar 21 2014 Martin Kolman <mkolman@redhat.com> - 0.31-1
- Translation update

* Wed Dec 18 2013 Vratislav Podzimek <vpodzime@redhat.com> - 0.30-1
- Exclude compiled versions of gui.py from the non-gui package (dshea)
- Skip callbacks providing no information (vpodzime)

* Wed Nov 20 2013 Vratislav Podzimek <vpodzime@redhat.com> - 0.29-1
- Split GUI out into a separate package (vpodzime)
- Create archives in one Makefile target and reuse it (vpodzime)

* Tue Nov 05 2013 Vratislav Podzimek <vpodzime@redhat.com> - 0.28-1
- Introduce support for Python 3 while keeping Python 2 working (miro)
- Sync spec with downstream (vpodzime)

* Wed Oct 09 2013 Vratislav Podzimek <vpodzime@redhat.com> - 0.27-1
- Use join method instead of the joinfields function
- Translate the hints on how to quit debugger and shell
- Add a way to run shell when exception appears
- Get rid of constants that are no longer used anywhere
- Filter local variables in a nicer way and fix docstring

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Vratislav Podzimek <vpodzime@redhat.com> - 0.26-1
- Output binary data correctly as hexa strings (#986515) (vpodzime)
- Add newline before dumping callbacks' outputs (vpodzime)

* Tue Jun 18 2013 Vratislav Podzimek <vpodzime@redhat.com> - 0.25-1
- Add and use the safe_string module and the SafeStr class (vpodzime)
- Give translators hint about the cryptic strings (vpodzime)

* Thu May 02 2013 Vratislav Podzimek <vpodzime@redhat.com> - 0.24-1
- Epoch of the package from RPM db can be None (#957789) (vpodzime)

* Wed Apr 17 2013 Vratislav Podzimek <vpodzime@redhat.com> - 0.23-1
- Use Sphinx syntax for docstrings (vpodzime)
- Allow a change of the I/O functions (vpodzime)
- Reword the 'Debug' button warning (#948256) (vpodzime)

* Thu Apr 04 2013 Vratislav Podzimek <vpodzime@redhat.com> - 0.22-1
- Some more stuff for ABRT/libreport (#929181) (vpodzime)
- Tell ABRT we are reporting a Python excetion (vpodzime)
- Use named tuples instead of our magic tuples (vpodzime)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Vratislav Podzimek <vpodzime@redhat.com> - 0.21-1
- New purely textual text interface (vpodzime)
- Add dumb enableNetwork implementation to GraphicalIntf (vpodzime)
- Destroy main window after running it (vpodzime)
- Get rid of the accountManager and use new libreport API (vpodzime)
- Add a way to override previously registered callback (vpodzime)
- Allow callbacks marked as attachment only (vpodzime)
- Add support for callbacks providing additional data (vpodzime)

* Tue Dec 11 2012 Vratislav Podzimek <vpodzime@redhat.com> - 0.20-1
- Handle non-ascii dict keys and values correctly (#883641) (vpodzime)

* Wed Nov 14 2012 Vratislav Podzimek <vpodzime@redhat.com> - 0.19-1
- Add test for handling unicode strings and files (vpodzime)
- Read files as UTF-8 and ignore errors (#874250) (vpodzime)
- Add check section to the spec file (vpodzime)
- Fix tests (vpodzime)

* Thu Oct 25 2012 Vratislav Podzimek <vpodzime@redhat.com> - 0.18-1
- Handle tracebacks with no stack (#866441) (vpodzime)
- Parse component name correctly (#866526) (vpodzime)
- Spelling corrections (#865993) (vpodzime)

* Tue Oct 09 2012 Vratislav Podzimek <vpodzime@redhat.com> - 0.17-1
- Handle unicode strings correctly (#854959) (vpodzime)

* Tue Sep 11 2012 Vratislav Podzimek <vpodzime@redhat.com> - 0.16-1
- Do not overwrite process information with files having the same basename (vpodzime)
- Encode dump as utf-8 before writing to file (#854959) (vpodzime)

* Mon Aug 20 2012 Vratislav Podzimek <vpodzime@redhat.com> - 0.15-1
- Add main_window property to the MainExceptionWindow (vpodzime)
- Don't try to dump objects without __dict__ (vpodzime)
- Change require from rpm to rpm-python (vpodzime)

* Fri Aug 03 2012 Vratislav Podzimek <vpodzime@redhat.com> - 0.14-1
- Use just a basename of the attached file as the item name (vpodzime)
- Set the type hint for the mainExceptionWindow to Dialog (vpodzime)
- Store and then write out the string representation of the traceback and object dump (vpodzime)

* Fri Jul 27 2012 Vratislav Podzimek <vpodzime@redhat.com> - 0.13-1
- Add files specified in the Config object as attachments to bugreports (vpodzime)
- Display hint how to quit the debugger (vpodzime)
- Do not kill the process when 'continue' is used in pdb (vpodzime)
- Port to Gtk3 and the new design (vpodzime)
- Remove the rc attribute and getrc methods (vpodzime)
- Fix 'all' and 'install' Makefile targets (vpodzime)
- Migrate l10n to Transifex (vpodzime)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Dec 20 2011 Vratislav Podzimek <vpodzime@redhat.com> 0.12
- Use new libreport API to get more information to bugzilla (vpodzime).
- Adapt to the new API of libreport (vpodzime).
- Move "import rpm" to where it's needed to avoid nameserver problems (clumens).
  Resolves: rhbz#749330
- Change dependency to libreport-* (mtoman).
  Resolves: rhbz#730924
- Add abrt-like information to bug reports (vpodzime).
  Resolves: rhbz#728871
- Propagate the screen attr when using text mode (jmoskovc).

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011 Chris Lumens <clumens@redhat.com> - 0.11-1
- Update the spec file URL to something valid (#670601). (clumens)
- Don't use _D for Debug, since that's already used by the expander (#640929). (clumens)
- Translation updates.

* Tue Jun 22 2010 Chris Lumens <clumens@redhat.com> 0.10-1
- Treat classes like simple types, too. (clumens)

* Thu Jun 10 2010 Chris Lumens <clumens@redhat.com> - 0.9-1
- Remove the requirement on python-bugzilla (#602794). (clumens)
- Rename ba.po -> bs.po (#583055). (clumens)
- Translation updates.

* Thu Mar 04 2010 Chris Lumens <clumens@redhat.com> - 0.8-1
- And add a requirement for report as well. (clumens)
- filer.py is now completely taken over by meh. (clumens)
- Everything from savers.py has moved into report. (clumens)
- Remove unused UI code now that report handles all this for me. (clumens)
- Switch ExceptionHandler to use report (#562656). (clumens)
- Don't allow an exception when writing out an attribute stop the whole dump. (clumens)
- Credit where credit is due. (clumens)

* Tue Nov 03 2009 Chris Lumens <clumens@redhat.com> - 0.7-1
- Add a test case framework.
- Move src -> meh for ease of test case writing.
- Another attempt at making the attrSkipList work (#532612, #532737).

* Thu Oct 08 2009 Chris Lumens <clumens@redhat.com> - 0.6-1
- Make idSkipList work again.
- Support dumping objects derived from Python's object.
- Use the right method to set text on a snack.Entry (#526884).

* Tue Sep 29 2009 Chris Lumens <clumens@redhat.com> - 0.5-1
- Always compare version numbers as strings (#526188).

* Fri Sep 25 2009 Chris Lumens <clumens@redhat.com> - 0.4-1
- Add a default description to bug reports.
- Handle the user pressing Escape by continuing to show the dialog.
- Lots more translation updates.

* Thu Sep 10 2009 Chris Lumens <clumens@redhat.com> - 0.3-1
- Pull in lots of new translations (#522410).

* Wed Aug 19 2009 Chris Lumens <clumens@redhat.com> - 0.2-1
- Add a title to the main exception dialog so it looks right in anaconda.
- Don't include an extra '/' in the displayed bug URL (#517515).
- Now that there's .po files, package them.
- Use the new exception icon (#517164).

* Tue Jul 28 2009 Chris Lumens <clumens@redhat.com> - 0.1-1
- Initial package.
