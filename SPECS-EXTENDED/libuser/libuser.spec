%bcond_with tex_docs

Name: libuser
Version: 0.63
Release: 10%{?dist}
License: GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL: https://pagure.io/libuser
Source: https://releases.pagure.org/libuser/libuser-%{version}.tar.xz
BuildRequires: glib2-devel
%if %{with tex_docs}
BuildRequires: linuxdoc-tools
%endif
BuildRequires: pam-devel
BuildRequires: popt-devel
BuildRequires: cyrus-sasl-devel
BuildRequires: libselinux-devel
BuildRequires: openldap-devel
BuildRequires: python3-devel
BuildRequires: gcc
# For %%check
%if 0%{?with_check}
#BuildRequires: fakeroot
BuildRequires: openldap-clients
BuildRequires: openssl

# Missing test dependencies:
# BuildRequires: openldap-servers
%endif
BuildRequires: make
BuildRequires: bison
BuildRequires: libtool
BuildRequires: gettext-devel
BuildRequires: gtk-doc
BuildRequires: audit-libs-devel

Summary: A user and group account administration library

Patch0: %{url}/pull-request/49.patch#/libuser-0.63-PR49_add_yescrypt.patch
Patch1: libuser-0.63-downstream_test_xcrypt.patch

%global __provides_exclude_from ^(%{_libdir}/%{name}|%{python3_sitearch})/.*$

%description
The libuser library implements a standardized interface for manipulating
and administering user and group accounts.  The library uses pluggable
back-ends to interface to its data sources.

Sample applications modeled after those included with the shadow password
suite are included.

%package devel
Summary: Files needed for developing applications which use libuser
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: glib2-devel%{?_isa}

%description devel
The libuser-devel package contains header files, static libraries, and other
files useful for developing applications with libuser.

%package -n python3-libuser
Summary: Python 3 bindings for the libuser library
Requires: libuser%{?_isa} = %{version}-%{release}
Provides: libuser-python3 = %{version}-%{release}
Provides: libuser-python3%{?_isa} = %{version}-%{release}
Obsoletes: libuser-python3 < 0.63-4
%{?python_provide:%python_provide python3-libuser}

%description -n python3-libuser
The python3-libuser package contains the Python bindings for
the libuser library, which provides a Python 3 API for manipulating and
administering user and group accounts.

%prep
%autosetup -p 1

%build

# Disabling doc builds, if needed.
%if %{without tex_docs}
  sed -E -i "s|(SUBDIRS = .*) docs(.*)|\1\2|" Makefile.am
  sed -E -i "s|(AC_CONFIG_FILES.*) docs/Makefile(.*)|\1\2|" configure.ac
  sed -E -i "s|(AC_CONFIG_FILES.*) docs/reference/Makefile(.*)|\1\2|" configure.ac
%endif

./autogen.sh
%configure \
  --with-selinux \
  --with-ldap \
  %if %{with tex_docs}
  --with-html-dir=%{_datadir}/gtk-doc/html \
  %else
  --disable-gtk-doc \
  %endif
  PYTHON=%{python3}
make


%install
%make_install

%find_lang %{name}

%check
%make_build check || { cat test-suite.log; false; }

# Verify that all python modules load, just in case.
LD_LIBRARY_PATH=$RPM_BUILD_ROOT/%{_libdir}:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH
PYTHONPATH=$RPM_BUILD_ROOT%{python3_sitearch}
export PYTHONPATH
%{python3} -c "import libuser"


%ldconfig_scriptlets

%files -f %{name}.lang
%license COPYING
%doc AUTHORS NEWS README TODO docs/*.txt
%config(noreplace) %{_sysconfdir}/libuser.conf

%attr(0755,root,root) %{_bindir}/*
%{_libdir}/*.so.*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so
%attr(0755,root,root) %{_sbindir}/*
%{_mandir}/man1/*

%if %{with tex_docs}
%{_mandir}/man5/*
%endif

%exclude %{_libdir}/*.la
%exclude %{_libdir}/%{name}/*.la

%files -n python3-libuser
%doc python/modules.txt
%{python3_sitearch}/*.so
%exclude %{python3_sitearch}/*.la

%files devel
%{_includedir}/libuser
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%if %{with tex_docs}
%{_datadir}/gtk-doc/html/*
%endif

%changelog
* Thu Aug 31 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.63-10
- Disabling missing test dependency.
- License verified.

* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 0.63-9
- Remove epoch

* Thu Aug 26 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.63-8
- Initial CBL-Mariner import from Fedora 35 (license: MIT).
- Conditionally build tex-based documentation, and turn off documentation building by default
- Conditionally depend on check requirements at build-time
- Remove deprecated nscd dependency

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.63-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 15 2021 Björn Esser <besser82@fedoraproject.org> - 0.63-6
- Add patches to add support for the yescrypt hash method
- Re-enable testsuite

* Tue Jun 15 2021 Björn Esser <besser82@fedoraproject.org> - 0.63-5
- Fix renaming of the python package (#1964587)

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.63-4
- Rebuilt for Python 3.10

* Thu May 20 2021 Tomas Halman <thalman@redhat.com> 
- Enable audit library in the build

* Tue May 11 2021 Tomas Halman <thalman@redhat.com> 
- Renaming python package according to the standard

* Tue Apr 20 2021 Jiri Kucera <jkucera@redhat.com> - 0.63-2
- Comment out fakeroot (unused)

* Mon Mar 1 2021 Tomas Halman <thalman@redhat.com> - 0.63-1
- Release new version 0.63

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.62-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Sep 09 2020 Tom Stellard <tstellar@redhat.com> - 0.62-30
 - Use make macros
 - https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Wed Sep 02 2020 Merlin Mathesius <mmathesi@redhat.com> - 0.62-29
- Pull in upstream patch that fixes FTBFS for Rawhide and ELN

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.62-28
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.62-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul  3 2020 Jakub Hrozek <jhrozek@redhat.com> - 0.62-26
- Temporarily disable tests, nothing changed since forever so this should be
  safe and would unblock FTBFS
- Related: rhbz#1817666 - libuser fails to build with Python 3.9: FAIL: tests/fs_test

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.62-25
- Rebuilt for Python 3.9

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.62-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 26 2019 Miro Hrončok <mhroncok@redhat.com> - 0.62-23
- Subpackage python2-libuser has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.62-22
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.62-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.62-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 0.62-19
- Rebuilt for libcrypt.so.2 (#1666033)

* Fri Jul 20 2018 Jakub Hrozek <jhrozek@redhat.com> - 0.62-19
- BuildRequires: gcc
- Related: rhbz#1604682 - libuser: FTBFS in Fedora rawhide

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.62-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul  9 2018 Jakub Hrozek <jhrozek@redhat.com> - 0.62-16
- Use python2 explicitly in tests of python2 bindings instead of just "python"
- Related: rhbz#1582899 - libuser: FTBFS in Fedora 28

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.62-15
- Rebuilt for Python 3.7

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.62-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 0.62-13
- Rebuilt for switch to libxcrypt

* Sat Oct 21 2017 Miloslav Trmač <mitr@redhat.com> - 0.62-12
- Update URL: and Source: to point to Pagure instead of fedorahosted.org
  Resolves: #1502354

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.62-11
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.62-10
- Python 2 binary package renamed to python2-libuser
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.62-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.62-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 15 2017 Stephen Gallagher <sgallagh@redhat.com> - 0.62-7
- Fix FTBFS on Fedora 26+
- Add patch to fix issues with -Werror=format-security
- Ensure that the python 3 tests use a locale guaranteed to be present

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.62-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.62-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.62-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.62-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.62-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jul 23 2015 Miloslav Trmač <mitr@redhat.com> - 0.62-1
- Update to libuser-0.62
  Resolves: #1246225 (CVE-2015-3245, CVE-2015-3246)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.61-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 25 2015 Miloslav Trmač <mitr@redhat.com> - 0.61-1
- Update to libuser-0.61, notably adding Python 3 bindings
  Resolves: #1014555
- Filter out libuser plugin and Python extension Provides:

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.60-7
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> - 0.60-5
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Oct 15 2013 Miloslav Trmač <mitr@redhat.com> - 0.60-3
- Fix the -2 change, %%check should fail on test suite failure

* Mon Oct 14 2013 Miloslav Trmač <mitr@redhat.com> - 0.60-2
- Include test suite output in build log on failure

* Mon Oct 14 2013 Miloslav Trmač <mitr@redhat.com> - 0.60-1
- Update to libuser-0.60
  Resolves: #910774, #985569, #1008825

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.59-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 28 2013 Miloslav Trmač <mitr@redhat.com> - 0.59-1
- Update to libuser-0.59 (CVE-2012-5630, CVE-2012-5644)
  Resolves: #928846

* Mon Feb  4 2013 Miloslav Trmač <mitr@redhat.com> - 0.58-2
- Always use secure_getenv() or __secure_getenv(), fail build if neither is
  available.  Patch by Viktor Hercinger <vhercing@redhat.com>.

* Thu Nov  8 2012 Miloslav Trmač <mitr@redhat.com> - 0.58-1
- Update to libuser-0.58
  Resolves: #844140, #854236

* Mon Sep 24 2012 Miloslav Trmač <mitr@redhat.com> - 0.57.7-1
- Update to libuser-0.57.7

* Tue Aug 21 2012 Miloslav Trmač <mitr@redhat.com> - 0.57.6-3
- Drop no longer necessary %%clean and %%defattr commands.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.57.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 22 2012 Miloslav Trmač <mitr@redhat.com> - 0.57.6-1
- Update to libuser-0.57.6
  Resolves: #803840

* Sat Mar  3 2012 Miloslav Trmač <mitr@redhat.com> - 0.57.5-1
- Update to libuser-0.57.5
- BuildRequires: openssl, the testsuite needs /usr/bin/openssl

* Fri Feb 10 2012 Miloslav Trmač <mitr@redhat.com> - 0.57.4-1
- Update to libuser-0.57.4
  Resolves: #788521

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.57.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct  4 2011 Miloslav Trmač <mitr@redhat.com> - 0.57.3-2
- Wait up to 30 seconds for slapd to start in the test suite

* Tue Oct  4 2011 Miloslav Trmač <mitr@redhat.com> - 0.57.3-1
- Update to libuser-0.57.3
  Resolves: #717116, #724986

* Thu Mar 31 2011 Miloslav Trmač <mitr@redhat.com> - 0.57.2-1
- Update to libuser-0.57.2
  Resolves: #671494
- Reenable (make check)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.57.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb  4 2011 Miloslav Trmač <mitr@redhat.com> - 0.57.1-4
- Use %%{?_isa} in Requires:

* Fri Jan 21 2011 Miloslav Trmač <mitr@redhat.com> - 0.57.1-3
- Disable (make check) to allow parallel 32-bit and 64-bit builds

* Thu Jan 20 2011 Miloslav Trmač <mitr@redhat.com> - 0.57.1-2
- Don't default commonName to gecos if it is empty
  Resolves: #670151

* Fri Jan 14 2011 Miloslav Trmač <mitr@redhat.com> - 0.57.1-1
- Update to libuser-0.57.1
  Resolves: #668855

* Mon Jan 10 2011 Miloslav Trmač <mitr@redhat.com> - 0.57-1
- Update to libuser-0.57
  Resolves: #497333 #610172

* Wed Sep 29 2010 Miloslav Trmač <mitr@redhat.com> - 0.56.18-2
- Handle matchpathcon() failing with ENOENT
  Resolves: #631717

* Tue Sep 14 2010 Miloslav Trmač <mitr@redhat.com> - 0.56.18-1
- Update to libuser-0.56.18

* Wed Sep  1 2010 Miloslav Trmač <mitr@redhat.com> - 0.56.17-2
- Change default crypt_style to sha512
  Resolves: #629001

* Thu Aug 26 2010 Miloslav Trmač <mitr@redhat.com> - 0.56.17-1
- Update to libuser-0.56.17

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.56.16-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul  2 2010 Miloslav Trmač <mitr@redhat.com> - 0.56.16-2
- Provide LU_VALUE_INVALID_ID and id_t validation in the Python module
  Resolves: #610838

* Thu Mar 25 2010 Miloslav Trmač <mitr@redhat.com> - 0.56.16-1
- Update to libuser-0.56.16.

* Thu Mar  4 2010 Miloslav Trmač <mitr@redhat.com> - 0.56.15-1
- Update to libuser-0.56.15.
- Drop no longer necessary references to BuildRequires

* Mon Feb  8 2010 Miloslav Trmač <mitr@redhat.com> - 0.56.14-1
- Update to libuser-0.56.14.

* Tue Jan  5 2010 Miloslav Trmač <mitr@redhat.com> - 0.56.13-2
- s/%%define/%%global/

* Fri Dec 11 2009 Miloslav Trmač <mitr@redhat.com> - 0.56.13-1
- Update to libuser-0.56.13.
  Resolves: #251951
  Resolves: #454079
  Resolves: #456373
  Resolves: #456382
  Resolves: #530513

* Fri Oct  2 2009 Miloslav Trmač <mitr@redhat.com> - 0.56.12-1
- Update to libuser-0.56.12.

* Mon Sep 14 2009 Miloslav Trmač <mitr@redhat.com> - 0.56.11-1
- Update to libuser-0.56.11.
  Resolves: #454091
  Resolves: #456267
  Resolves: #456270
  Resolves: #487129

* Thu Jul 30 2009 Miloslav Trmač <mitr@redhat.com> - 0.56.10-3
- Fix nscd cache invalidation
  Resolves: #506628
- Preserve timestamps during (make install)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.56.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 15 2009 Miloslav Trmač <mitr@redhat.com> - 0.56.10-1
- Update to libuser-0.56.10.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.56.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.56.9-2
- Rebuild for Python 2.6

* Wed Apr  9 2008 Miloslav Trmač <mitr@redhat.com> - 0.56.9-1
- Update to libuser-0.56.9.

* Sat Feb 23 2008 Miloslav Trmač <mitr@redhat.com> - 0.56.8-1
- New home page at https://fedorahosted.org/libuser/ .

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.56.7-2
- Autorebuild for GCC 4.3

* Wed Jan  9 2008 Miloslav Trmač <mitr@redhat.com> - 0.56.7-1
- Add support for SHA256 and SHA512 in password hashes
  Related: #173583
- Fix file locking on some architectures
- Rename sr@Latn.po to sr@latin.po
  Resolves: #426584
- Address issues from a review by Jason Tibbitts:
  - Remove default.-c, moving the provided functions to libuser proper
  - Remove the WITH_SELINUX build option
  - Move Python library test to %%check
  Resolves: #226054

* Mon Jan 07 2008 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.56.6-4
- Add the usual "there is no upstream" notice.

* Tue Dec 04 2007 Release Engineering <rel-eng at fedoraproject dot org> - 0.56.6-4
 - Rebuild for openldap bump

* Tue Dec  4 2007 Miloslav Trmač <mitr@redhat.com> - 0.56.6-3
- Rebuild with openldap-2.4.

* Wed Oct 31 2007 Miloslav Trmač <mitr@redhat.com> - 0.56.6-2
- Fix uninitialized memory usage when SELinux is disabled

* Thu Oct 25 2007 Miloslav Trmač <mitr@redhat.com> - 0.56.6-1
- Set SELinux file contexts when creating home directories, preserve them when
  moving home directories
  Resolves: #351201

* Thu Oct 11 2007 Miloslav Trmač <mitr@redhat.com> - 0.56.5-1
- Work around spurious error messages when run against the Fedora Directory
  server
- Fix error reporting when creating home directories and creating/removing mail
  spool files
  Resolves: #318121

* Wed Sep  5 2007 Miloslav Trmač <mitr@redhat.com> - 0.56.4-3
- s/popt/popt-devel/ in BuildRequires
  Resolves: #277541

* Wed Aug  8 2007 Miloslav Trmač <mitr@redhat.com> - 0.56.4-2
- Split the Python module to a separate subpackage (original patch by Yanko
  Kaneti)
- Update the License: tag

* Fri Jun 15 2007 Miloslav Trmač <mitr@redhat.com> - 0.56.4-1
- Update the last password change date field when changing passwords
  Resolves: #243854

* Sat Jun  9 2007 Miloslav Trmač <mitr@redhat.com> - 0.56.3-1
- Allow specifying a SASL mechanism (original patch by Simo Sorce)
  Resolves: #240904

* Thu Apr 19 2007 Miloslav Trmac <mitr@redhat.com> - 0.56.2-1
- New release with updated translations

* Fri Feb 23 2007 Miloslav Trmac <mitr@redhat.com> - 0.56.1-1
- When changing passwords, only silently ignore know shadow markers, not all
  invalid hashes
  Resolves: #225495

* Sat Feb 17 2007 Miloslav Trmac <mitr@redhat.com> - 0.56-1
- Tighten the API and implementation to avoid corrupting number-like strings;
  the module interface ABI has changed
  Resolves: #226976

* Sat Jan  6 2007 Jeremy Katz <katzj@redhat.com> - 0.55-2
- Fix inconsistent PyObject/PyMem usage (#220679)

* Sun Dec 10 2006 Miloslav Trmac <mitr@redhat.com> - 0.55-1
- Update to support the 64-bit API of Python 2.5
- Drop the quota library and Python module

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 0.54.8-2
- rebuild against python2.5
- follow python packaging guidelines

* Thu Nov  2 2006 Miloslav Trmac <mitr@redhat.com> - 0.54.8-1
- Add importing of HOME from default/useradd
  Related: #204707

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 0.54.7-2
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 25 2006 Miloslav Trmac <mitr@redhat.com> - 0.54.7-1
- New release with updated translations

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.54.6-2.1
- rebuild

* Wed Jun  7 2006 Miloslav Trmac <mitr@redhat.com> - 0.54.6-2
- Configure without --enable-gtk-doc to fix multilib conflict (#192715)

* Mon May  1 2006 Miloslav Trmac <mitr@redhat.com> - 0.54.6-1
- Fix bugs in handling of invalid lines in the files and shadow modules
- Fix pattern matching in lu_*_enumerate_full in the files and shadow modules
- Add more error reporting, return non-zero exit status on error from utils
- Use the skeleton directory specified in libuser.conf by Python
  admin.createHome and admin.addUser, add parameter skeleton= to admin.addUser
  (#189984)

* Tue Feb 21 2006 Miloslav Trmac <mitr@redhat.com> - 0.54.5-1
- Fix multilib conflict on libuser.conf.5

* Mon Feb 13 2006 Miloslav Trmac <mitr@redhat.com> - 0.54.4-1
- New release with updated translations

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.54.3-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.54.3-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Dec  2 2005 Miloslav Trmac <mitr@redhat.com> - 0.54.3-1
- Fix crash in lpasswd when user is not specified (#174801)

* Fri Nov 11 2005 Miloslav Trmac <mitr@redhat.com> - 0.54.2-1
- Avoid using deprecated openldap functions

* Fri Nov 11 2005 Miloslav Trmac <mitr@redhat.com> - 0.54.1-2
- Rebuild with newer openldap

* Tue Oct 11 2005 Miloslav Trmac <mitr@redhat.com> - 0.54.1-1
- Support importing of configuration from shadow-utils (/etc/login.defs and
  /etc/default/useradd)
- Add libuser.conf(5) man page

* Wed Oct  5 2005 Matthias Clasen <mclasen@redhat.com> - 0.54-2
- Use gmodule-no-export in the .pc file

* Tue Sep 13 2005 Miloslav Trmac <mitr@redhat.com> - 0.54-1
- Make sure attributes with no values can never appear
- Fix crash in the "files" module when an attribute is missing
- Use hidden visibility for internal functions, remove them from
  libuser/user_private.h; this changes module interface ABI

* Wed Jun  8 2005 Miloslav Trmac <mitr@redhat.com> - 0.53.8-1
- Permit "portable" user and group names as defined by SUSv3, plus trailing $
  (#159452)
- Don't build static libraries

* Sat Apr 30 2005 Miloslav Trmac <mitr@redhat.com> - 0.53.7-1
- Rebuild with updated translations, add missing translations.

* Sun Apr 24 2005 Miloslav Trmac <mitr@redhat.com> - 0.53.6-1
- Allow empty configuration values (#155402)

* Fri Apr 15 2005 Miloslav Trmac <mitr@redhat.com> - 0.53.5-1
- Ignore nss_compat lines in the "files" module (#154651)
- Autodetect Python version (#154096)
- Add BuildRequires: libselinux-devel, s/BuildPrereq/BuildRequires/

* Wed Apr  6 2005 Miloslav Trmac <mitr@redhat.com> - 0.53.4-1
- Fix adding objectclasses to existing LDAP entries (#152960)

* Wed Mar 30 2005 Miloslav Trmac <mitr@redhat.com> - 0.53.3-2
- Add Requires: glib2-devel to libuser-devel (#152501)
- Run ldconfig using %%post{,un} -p to let RPM play tricks

* Sat Mar  5 2005 Miloslav Trmac <mitr@redhat.com> - 0.53.3-1
- Don't silently ignore some I/O errors
- Don't include a Cyrus SASL v1 header file when libldap links to v2 (#150046)
- Rebuild with gcc 4

* Mon Jan 17 2005 Miloslav Trmac <mitr@redhat.com> - 0.53.2-1
- Important bug fixes in lchage, lgroupmod, lnewusers and lusermod
- Minor bug fixes in lpasswd and luseradd
- Add man pages for the utilities (#61673)

* Mon Dec 13 2004 Miloslav Trmac <mitr@redhat.com> - 0.53.1-1
- Export UT_NAMESIZE from <utmp.h> to Python (#141273)

* Sun Nov 14 2004 Miloslav Trmac <mitr@redhat.com> - 0.53-1
- Support UID and GID values larger than LONG_MAX (#124967)
- Fix updating of groups after user renaming in lusermod
- Allow setting a shadow password even if the current shadow password is
  invalid (#131180)
- Add lu_{user,group}_unlock_nonempty (#86414); module interface ABI has 
  changed
- Miscellaneous bug and memory leak fixes

* Mon Nov  8 2004 Jeremy Katz <katzj@redhat.com> - 0.52.6-2
- rebuild against python 2.4

* Tue Nov  2 2004 Miloslav Trmac <mitr@redhat.com> - 0.52.6-1
- Make error reporting more consistent, more verbose and always on stderr
  (partly #133861, original patch by Pawel Salek)
- Mark strings previously blocked by string freeze for translation

* Tue Oct 12 2004 Miloslav Trmac <mitr@redhat.com> - 0.52.5-1
- Fix home directory renaming in ADMIN.modifyUser (#135280)
- Further Python reference counting fixes

* Sun Oct 10 2004 Miloslav Trmac <mitr@redhat.com> - 0.52.4-1
- Fix memory leaks (#113730)
- Build with updated translations

* Wed Sep 29 2004 Miloslav Trmac <mitr@redhat.com> - 0.52.3-1
- Fix compilation without libuser headers already installed (#134085)

* Tue Sep 28 2004 Miloslav Trmac <mitr@redhat.com> - 0.52.2-1
- Allow LDAP connection using ldaps, custom ports or without TLS (original
  patch from Pawel Salek).

* Mon Sep 27 2004 Miloslav Trmac <mitr@redhat.com> - 0.52.1-1
- Fix freecon() of uninitialized value in files/shadow module

* Mon Sep 27 2004 Miloslav Trmac <mitr@redhat.com> - 0.52-1
- Usable LDAP backend (#68052, #99435, #130404)
- Miscellaneous bug fixes

* Fri Sep 24 2004 Miloslav Trmac <mitr@redhat.com> - 0.51.12-1
- Don't claim success and exception at the same time (#133479)
- LDAP fixes, second round
- Various other bugfixes

* Thu Sep 23 2004 Miloslav Trmac <mitr@redhat.com> - 0.51.11-1
- Allow documented optional arguments in Python
  ADMIN.{addUser,modifyUser,deleteUser} (#119812)
- Add man pages for lchfn and lchsh
- LDAP fixes, first round
- Avoid file conflict on multilib systems
- Call ldconfig correctly

* Fri Sep  3 2004 Miloslav Trmac <mitr@redhat.com> - 0.51.10-1
- Don't attempt to lookup using original entity name after entity
  modification (rename in particular) (#78376, #121252)
- Fix copying of symlinks from /etc/skel (#87572, original patch from gLaNDix)
- Make --enable-quota work, and fix the quota code to at least compile (#89114)
- Fix several bugs (#120168, original patch from Steve Grubb)
- Don't hardcode python version in spec file (#130952, from Robert Scheck)
- Properly integrate the SELinux patch, it should actually be used now, even
  though it was "enabled" since 0.51.7-6

* Tue Aug 31 2004 Miloslav Trmac <mitr@redhat.com> - 0.51.9-1
- Fix various typos
- Document library interfaces
- Build all shared libraries with -fPIC (#72536)

* Wed Aug 25 2004 Miloslav Trmac <mitr@redhat.com> - 0.51.8-1
- Update to build with latest autotools and gtk-doc
- Update ALL_LINGUAS and POTFILES.in
- Rebuild to depend on newer openldap

* Mon Jan 26 2004 Dan Walsh <dwalsh@redhat.com> 0.51.7-7
- fix is_selinux_enabled call

* Sun Dec 14 2003 Jeremy Katz <katzj@redhat.com> 0.51.7-6
- rebuild against python 2.3
- enable SELinux

* Mon Sep 08 2003 Dan Walsh <dwalsh@redhat.com> 0.51.7-5
- Turn off SELinux 

* Wed Aug 06 2003 Dan Walsh <dwalsh@redhat.com> 0.51.7-3
- Add SELinux support

* Wed Feb 19 2003 Nalin Dahyabhai <nalin@redhat.com> 0.51.7-1
- ldap: set error codes correctly when we encounter failures initializing
- don't double-close modules which fail initialization
- ldap: don't set an error in cases where one is already set

* Tue Feb 18 2003 Nalin Dahyabhai <nalin@redhat.com> 0.51.6-1
- use a crypt salt consistent with the defaults/crypt_style setting when
  setting new passwords (#79337)

* Thu Feb  6 2003 Nalin Dahyabhai <nalin@redhat.com> 0.51.5-2
- rebuild

* Wed Feb  5 2003 Nalin Dahyabhai <nalin@redhat.com> 0.51.5-1
- expose lu_get_first_unused_id() as a package-private function
- provide libuser.ADMIN.getFirstUnusedUid and libuser.ADMIN.getFirstUnusedGid
  in python

* Thu Dec 19 2002 Nalin Dahyabhai <nalin@redhat.com> 0.51.4-1
- fix not freeing resources properly in files.c(generic_is_locked), spotted by
  Zou Pengcheng

* Wed Dec 11 2002 Nalin Dahyabhai <nalin@redhat.com> 0.51.2-1
- degrade gracefully
- build with --with-pic and -fPIC
- remove unpackaged man page

* Tue Aug 27 2002 Nalin Dahyabhai <nalin@redhat.com> 0.51.1-2
- translation updates

* Wed Jul 24 2002 Nalin Dahyabhai <nalin@redhat.com> 0.51.1-1
- doc updates -- cvs tree moved
- language updates
- disallow weird characters in account names

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 20 2002 Nalin Dahyabhai <nalin@redhat.com> 0.51-1
- files: ignore blank lines in files
- libuser: disallow creation of accounts with names containing whitespace,
  control characters, or non-ASCII characters

* Tue Apr 16 2002 Nalin Dahyabhai <nalin@redhat.com> 0.50.2-1
- refresh translations
- fix a heap-corruption bug in the python bindings

* Mon Apr 15 2002 Nalin Dahyabhai <nalin@redhat.com> 0.50-1
- bump version
- refresh translations

* Thu Mar 14 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.102-1
- ldap: cache an entity's dn in the entity structure to try to speed things up

* Mon Mar 11 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.101-3
- rebuild in new environment

* Thu Mar  7 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.101-2
- add missing buildreqs on cyrus-sasl-devel and openldap-devel (#59456)
- translation refresh

* Fri Mar  1 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.101-1
- fix python bindings of enumerateFull functions
- adjust prompter wrapping to not error out on successful returns

* Thu Feb 28 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.100-1
- be more careful about printing error messages
- fix refreshing after adding of accounts
- ldap: try to use a search to convert names to DNs, and only fall back to
  guessing if it turns up nothing
- files: fix an off-by-one in removal of entries

* Mon Feb 25 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.99-1
- refresh translations
- fix admin() constructor comments in the python module

* Thu Feb 21 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.98-1
- automatically refresh entities after add, modify, setpass, removepass,
  lock, and unlock operations
- remove debug spewage when creating and removing mail spools
- files: fix saving of multi-valued attributes
- rename MEMBERUID attribute for groups to MEMBERNAME

* Wed Feb 20 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.97-1
- files: fix bug in removals
- ldap: revert attempts at being smart at startup time, because it makes UIs
  very messy (up the three whole dialogs just to start the ldap stuff!)

* Sat Feb 16 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.96-1
- fix thinko in dispatch routines

* Wed Feb 13 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.95-1
- lgroupmod: fix thinko

* Thu Jan 31 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.94-2
- rebuild in new environment

* Tue Jan 29 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.93-1
- move shadow initialization for groups to the proper callback
- rework locking in the files module to not require that files be writable

* Tue Jan 29 2002 Nalin Dahyabhai <nalin@redhat.com>
- expose lu_strerror()
- add various typedefs for types used by the library

* Mon Jan 28 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.92-1
- add removepass() functions

* Thu Jan 24 2002 Nalin Dahyabhai <nalin@redhat.com>
- lchfn,lchsh,lpasswd - reorder PAM authentication calls
- include API docs in the package

* Thu Jan 24 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.91-1
- ldap: finish port to new API
- sasl: finish port to new API (needs test)
- libuser: don't commit object changes before passing data to service
  functions which might need differing data sets to figure out what to
  change (for example, ldap)

* Thu Jan 17 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49.90-1
- bind the internal mail spool creation/removal functions for python

* Wed Jan 16 2002 Nalin Dahyabhai <nalin@redhat.com>
- renamed the python module
- revamped internals to use gobject's gvalues and gvaluearrays instead of
  glists of cached strings
- add enumeration-with-data functions to the C library

* Mon Jan 07 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- require linuxdoc-tools instead of sgml-tools for rawhide

* Tue Nov 13 2001 Nalin Dahyabhai <nalin@redhat.com>
- fixup build files to allow building for arbitrary versions of python

* Wed Aug 29 2001 Nalin Dahyabhai <nalin@redhat.com> 0.32-1
- link the python module against libpam
- attempt to import the python modules at build-time to verify dependencies

* Tue Aug 28 2001 Nalin Dahyabhai <nalin@redhat.com> 0.31-1
- fix a file-parsing bug that popped up in 0.29's mmap modifications

* Mon Aug 27 2001 Nalin Dahyabhai <nalin@redhat.com> 0.30-1
- quotaq: fix argument order when reading quota information
- user_quota: set quota grace periods correctly
- luseradd: never create home directories for system accounts

* Tue Aug 21 2001 Nalin Dahyabhai <nalin@redhat.com>
- add da translation files
- update translations

* Tue Aug 21 2001 Nalin Dahyabhai <nalin@redhat.com> 0.29-1
- add an explicit build dependency on jade (for the docs)

* Mon Aug 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- HUP nscd on modifications
- userutil.c: mmap files we're reading for probable speed gain
- userutil.c: be conservative with the amount of random data we read
- docs fixes

* Wed Aug 15 2001 Nalin Dahyabhai <nalin@redhat.com> 0.28-1
- apps: print usage on errors
- lnewusers.c: initialize groups as groups, not users
- lnewusers.c: set passwords for new accounts
- luseradd.c: accept group names in addition to IDs for the -g flag
- luseradd.c: allow the primary GID to be a preexisting group

* Tue Aug 14 2001 Nalin Dahyabhai <nalin@redhat.com> 0.27-1
- add ko translation files
- files.c: fix a heap corruption bug in lock/unlock (#51750)
- files.c: close a memory leak in reading of files

* Mon Aug 13 2001 Nalin Dahyabhai <nalin@redhat.com>
- files.c: remove implementation limits on lengths of lines

* Thu Aug  9 2001 Nalin Dahyabhai <nalin@redhat.com> 0.26-1
- lusermod: change user name in groups the user is a member of during renames
- lgroupmod: change primary GID for users who are in the group during renumbers
- ldap.c: handle new attributes more gracefully if possible
- add ru translation files

* Tue Aug  7 2001 Nalin Dahyabhai <nalin@redhat.com> 0.25.1-1
- rename the quota source files to match the library, which clears up a
  file conflict with older quota packages
- add ja translation files

* Thu Aug  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- add lu_ent_clear_all() function

* Thu Aug  2 2001 Nalin Dahyabhai <nalin@redhat.com> 0.25-1
- close up some memory leaks
- add the ability to include resident versions of modules in the library

* Wed Aug  1 2001 Nalin Dahyabhai <nalin@redhat.com> 0.24-4
- fix incorrect Py_BuildValue invocation in python module

* Tue Jul 31 2001 Nalin Dahyabhai <nalin@redhat.com> 0.24-3
- stop leaking descriptors in the files module
- speed up user creation by reordering some checks for IDs being in use
- update the shadowLastChanged attribute when we set a password
- adjust usage of getXXXXX_r where needed
- fix assorted bugs in python binding which break prompting

* Mon Jul 30 2001 Nalin Dahyabhai <nalin@redhat.com> 0.23-1
- install sv translation
- make lpasswd prompt for passwords when none are given on the command line
- make sure all user-visible strings are marked for translation
- clean up some user-visible strings
- require PAM authentication in lchsh, lchfn, and lpasswd for non-networked modules

* Fri Jul 27 2001 Nalin Dahyabhai <nalin@redhat.com>
- print uids and gids of users and names in lid app
- fix tree traversal in users_enumerate_by_group and groups_enumerate_by_users
- implement enumerate_by_group and enumerate_by_user in ldap module
- fix id-based lookups in the ldap module
- implement islocked() method in ldap module
- implement setpass() method in ldap module
- add lchfn and lchsh apps
- add %%d substitution to libuser.conf

* Thu Jul 26 2001 Nalin Dahyabhai <nalin@redhat.com> 0.21-1
- finish adding a sasldb module which manipulates a sasldb file
- add users_enumerate_by_group and groups_enumerate_by_users

* Wed Jul 25 2001 Nalin Dahyabhai <nalin@redhat.com> 
- luserdel: remove the user's primary group if it has the same name as
  the user and has no members configured (-G disables)
- fixup some configure stuff to make libuser.conf get generated correctly
  even when execprefix isn't specified

* Tue Jul 24 2001 Nalin Dahyabhai <nalin@redhat.com> 0.20-1
- only call the auth module when setting passwords (oops)
- use GTrees instead of GHashTables for most internal tables
- files: complain properly about unset attributes
- files: group passwords are single-valued, not multiple-valued
- add lpasswd app, make sure all apps start up popt with the right names

* Mon Jul 23 2001 Nalin Dahyabhai <nalin@redhat.com> 0.18-1
- actually make the new optional arguments optional
- fix lu_error_new() to actually report errors right
- fix part of the python bindings
- include tools in the binary package again
- fixup modules so that password-changing works right again
- add a "key" field to prompt structures for use by apps which like to
  cache these things
- add an optional "mvhomedir" argument to userModify (python)

* Fri Jul 20 2001 Nalin Dahyabhai <nalin@redhat.com> 0.16.1-1
- finish home directory population
- implement home directory moving
- change entity get semantics in the python bindings to allow default values for .get()
- add lu_ent_has(), and a python has_key() method to Entity types
- don't include tools in the binary package
- add translated strings

* Thu Jul 19 2001 Nalin Dahyabhai <nalin@redhat.com>
- lib/user.c: catch and ignore errors when running stacks
- lusermod: fix slightly bogus help messages
- luseradd: when adding a user and group, use the gid of the group
  instead of the user's uid as the primary group
- properly set the password field in user accounts created using
  auth-only auth modules (shadow needs "x" instead of "!!")
- implement home directory removal, start on population

* Wed Jul 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix group password setting in the files module
- setpass affects both auth and info, so run both stacks

* Tue Jul 17 2001 Nalin Dahyabhai <nalin@redhat.com>
- make the testbed apps noinst

* Mon Jul 16 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix errors due to uninitialized fields in the python bindings
- add kwargs support to all python wrappers
- add a mechanism for passing arguments to python callbacks

* Wed Jul 11 2001 Nalin Dahyabhai <nalin@redhat.com>
- stub out the krb5 and ldap modules so that they'll at least compile again
 
* Tue Jul 10 2001 Nalin Dahyabhai <nalin@redhat.com>
- don't bail when writing empty fields to colon-delimited files
- use permissions of the original file when making backup files instead of 0600

* Fri Jul  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- finish implementing is_locked methods in files/shadow module
- finish cleanup of the python bindings
- allow conditional builds of modules so that we can build without
  all of the prereqs for all of the modules

* Thu Jun 21 2001 Nalin Dahyabhai <nalin@redhat.com>
- add error reporting facilities
- split public header into pieces by function
- backend cleanups

* Mon Jun 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- make %%{name}-devel require %%{name} and not %%{name}-devel

* Fri Jun 15 2001 Nalin Dahyabhai <nalin@redhat.com>
- clean up quota bindings some more
- finish most of the ldap bindings
- fix a subtle bug in the files module that would show up when renaming accounts
- fix mapping methods for entity structures in python

* Thu Jun 14 2001 Nalin Dahyabhai <nalin@redhat.com>
- get bindings for prompts to work correctly
- clean up some of the add/remove semantics (set source on add)
- ldap: implement enumeration
- samples/enum: fix the argument order

* Wed Jun 13 2001 Nalin Dahyabhai <nalin@redhat.com>
- clean up python bindings for quota

* Tue Jun 12 2001 Nalin Dahyabhai <nalin@redhat.com> 0.11
- finish up python bindings for quota support

* Sun Jun 10 2001 Nalin Dahyabhai <nalin@redhat.com>
- finish up quota support libs

* Fri Jun  8 2001 Nalin Dahyabhai <nalin@redhat.com>
- start quota support library to get some type safety

* Thu Jun  7 2001 Nalin Dahyabhai <nalin@redhat.com>
- start looking at quota manipulation

* Wed Jun  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- add functions for enumerating users and groups, optionally per-module
- lusermod.c: -s should specify the shell, not the home directory

* Fri Jun  1 2001 Nalin Dahyabhai <nalin@redhat.com> 0.10
- finish the python bindings and verify that the file backend works again

* Wed May 30 2001 Nalin Dahyabhai <nalin@redhat.com>
- remove a redundant check which was breaking modifications

* Tue May 29 2001 Nalin Dahyabhai <nalin@redhat.com>
- finish adding setpass methods

* Wed May  2 2001 Nalin Dahyabhai <nalin@redhat.com> 0.9
- get a start on some Python bindings

* Tue May  1 2001 Nalin Dahyabhai <nalin@redhat.com> 0.8.2
- make binary-incompatible change in headers

* Mon Apr 30 2001 Nalin Dahyabhai <nalin@redhat.com> 0.8.1
- add doxygen docs and a "doc" target for them

* Sat Jan 20 2001 Nalin Dahyabhai <nalin@redhat.com> 0.8
- add a "quiet" prompter
- add --interactive flag to sample apps and default to using quiet prompter
- ldap: attempt a "self" bind if other attempts fail
- krb5: connect to the password-changing service if the user principal has
  the NULL instance

* Wed Jan 10 2001 Nalin Dahyabhai <nalin@redhat.com>
- the great adding-of-the-copyright-statements
- take more care when creating backup files in the files module

* Wed Jan  3 2001 Nalin Dahyabhai <nalin@redhat.com> 0.7
- add openldap-devel as a buildprereq
- krb5: use a continuous connection
- krb5: add "realm" config directive
- ldap: use a continuous connection
- ldap: add "server", "basedn", "binddn", "user", "authuser" config directives
- ldap: actually finish the account deletion function
- ldap: don't send cleartext passwords to the directory
- fix naming attribute for users (should be uid, not gid)
- refine the search-by-id,convert-to-name,search-by-name logic
- fix handling of defaults when the config file is read in but contains no value
- implement an LDAP information store
- try to clean up module naming with libtool
- luseradd: pass plaintext passwords along
- luseradd: use symbolic attribute names instead of hard-coded
- lusermod: pass plaintext passwords along
- lgroupadd: pass plaintext passwords along
- lgroupmod: pass plaintext passwords along
- add libuser as a dependency of libuser-devel

* Tue Jan  2 2001 Nalin Dahyabhai <nalin@redhat.com> 0.6
- initial packaging
