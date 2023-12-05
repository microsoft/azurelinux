Vendor:         Microsoft Corporation
Distribution:   Mariner

%bcond_without python3

%bcond_with python2

Summary: Python module for GNU parted
Name:    pyparted
Version: 3.11.4
Release: 4%{?dist}
License: GPLv2+
URL:     https://github.com/dcantrell/pyparted

Source0: https://github.com/dcantrell/pyparted/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source1: https://github.com/dcantrell/pyparted/releases/download/v%{version}/%{name}-%{version}.tar.gz.asc
Source2: keyring.gpg
Source3: trustdb.gpg

BuildRequires: gcc
BuildRequires: parted-devel >= 3.2-18
BuildRequires: pkgconfig
BuildRequires: e2fsprogs
BuildRequires: gnupg2

%if %{with python3}
BuildRequires: python3-devel
BuildRequires: python3-six
%endif

%if %{with python2}
BuildRequires: python2-devel
BuildRequires: python2-six
%endif

%global _description\
Python module for the parted library.  It is used for manipulating\
partition tables.

%description %_description

%if %{with python2}
%package -n python2-pyparted
Summary: %summary
%{?python_provide:%python_provide python2-pyparted}
# Remove before F30
Provides: pyparted = %{version}-%{release}
Provides: pyparted%{?_isa} = %{version}-%{release}
Obsoletes: pyparted < %{version}-%{release}

%description -n python2-pyparted %_description
%endif

%if %{with python3}
%package -n python3-pyparted
Summary: Python 3 module for GNU parted

%description -n python3-pyparted
Python module for the parted library.  It is used for manipulating
partition tables. This package provides Python 3 bindings for parted.
%endif

%prep
# Verify source archive signature
# Remove "use-keyboxd" from gnupg configuration; if present, since it will wait forever if the service is not running
sed -i '/use-keyboxd/d' ~/.gnupg/common.conf
gpg --no-default-keyring --keyring %{SOURCE2} --trustdb-name %{SOURCE3} --verify %{SOURCE1} %{SOURCE0} || exit 1

%setup -q

%if %{with python3}
everything=$(ls)
mkdir -p py3dir
cp -a $everything py3dir
%endif

%build
%if %{with python2}
PYTHON=python2 make %{?_smp_mflags} CFLAGS="%{optflags} -fcommon"
%endif

%if %{with python3}
pushd py3dir
PYTHON=python3 make %{?_smp_mflags} CFLAGS="%{optflags} -fcommon"
popd
%endif

%check
%if %{with python2}
PYTHON=python2 make test
%endif

%if %{with python3}
pushd py3dir
PYTHON=python3 make test
popd
%endif

%install
%if %{with python2}
PYTHON=python2 make install DESTDIR=%{buildroot}
%endif

%if %{with python3}
pushd py3dir
PYTHON=python3 make install DESTDIR=%{buildroot}
popd
%endif

%if %{with python2}
%files -n python2-pyparted
%doc AUTHORS COPYING NEWS README TODO
%{python2_sitearch}/_ped.so
%{python2_sitearch}/parted
%{python2_sitearch}/%{name}-%{version}-*.egg-info
%endif

%if %{with python3}
%files -n python3-pyparted
%doc AUTHORS COPYING NEWS README TODO
%{python3_sitearch}/_ped.*.so
%{python3_sitearch}/parted
%{python3_sitearch}/%{name}-%{version}-*.egg-info
%endif

%changelog
* Mon Dec 04 2023 Andrew Phelps <anphel@microsoft.com> - 3.11.4-4
- Fix build issue with gpg keyboxd

* Mon Nov 01 2021 Muhammad Falak <mwani@microsoft.com> - 3.11.4-3
- Remove epoch

* Mon Mar 01 2021 Henry Li <lihl@microsoft.com> - 1:3.11.4-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Disable python2 build and enable python3 build only

* Tue Feb 11 2020 David Cantrell <dcantrell@redhat.com> - 1:3.11.4-1
- Use Decimal for Device.getSize() operations, return a
  float (#1801355)
- Update the 'twine upload' line in the Makefile
- Don't intentionally prohibit Python 2 usage (#67)
- mips64 support

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.11.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 15 2019 David Cantrell <dcantrell@redhat.com> - 1:3.11.3-1
- Fix deprecation warning in parted/cachedlist.py (#1772060)

* Sun Oct 20 2019 Miro Hrončok <mhroncok@redhat.com> - 1:3.11.2-5
- Remove python2-pyparted from Fedora 32+

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1:3.11.2-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 1:3.11.2-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 David Cantrell <dcantrell@redhat.com> - 1:3.11.2-1
- pyparted-3.11.2 (dcantrell)
- Do not remove the generated tarballs. (dcantrell)
- Update the RELEASE file. (dcantrell)
- tests: Fix flag_get_name tests (bcl)
- Avoid potential NULL dereferences in pydisk.c and pytimer.c
  (dcantrell)
- New - example to query device capacity (jflorian)
- correct spelling mistake (edward)
- _ped's *_flag_get_name methods now throw a PartedException instead of
  ValueError on unsupported flags. (lukasz.zemczak)
- Make the partition name a property on parted.Partition objects (#34)
  (dcantrell)

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 1:3.11.0-17
- Rebuild with fixed binutils

* Fri Jul 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:3.11.0-16
- Rebuild for new binutils

* Thu Jul 26 2018 David Cantrell <dcantrell@redhat.com> - 1:3.11.0-15
- Do not disable python2 builds by default.  There are still some packages
  that have not been updated to python3 and require python2-pyparted.

* Wed Jul 25 2018 David Cantrell <dcantrell@redhat.com> - 1:3.11.0-14
- Conditionalize python2 and python3 builds to make the SRPM more portable
  across releases.  On RHEL > 7 and Fedora > 28, do not build for python2.
  On RHEL <= 7, do not build for python3.

* Tue Jul 24 2018 David Cantrell <dcantrell@redhat.com> - 1:3.11.0-13
- Use 'python2' when building the Python 2.x bindings (#1605566)
- BuildRequires gcc (#1605566)
- %%{python_sitearch} -> %%{python2_sitearch} (#1605566)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.11.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 1:3.11.0-11
- Rebuilt for Python 3.7

* Mon Apr 02 2018 Adam Williamson <awilliam@redhat.com> - 1:3.11.0-10
- Make pyparted provides/obsoletes include the epoch

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.11.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 15 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1:3.11.0-8
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:3.11.0-7
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:3.11.0-6
- Python 2 binary package renamed to python2-pyparted
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.11.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.11.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 13 2017 David Cantrell <dcantrell@redhat.com> - 1:3.11.0-3
- Require parted-3.2-18 in order to ensure #25 does not occur

* Mon Jun 26 2017 David Cantrell <dcantrell@redhat.com> - 1:3.11.0-2
- BuildRequires python[3]-six

* Thu Jun 22 2017 David Cantrell <dcantrell@redhat.com> - 1:3.11.0-1
- Upgrade to pyparted-3.11.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.10.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 1:3.10.7-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.10.7-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.10.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Oct 15 2015 Robert Kuska <rkuska@redhat.com> - 1:3.10.7-2
- Rebuilt for Python3.5 rebuild

* Thu Aug 27 2015 David Cantrell <dcantrell@redhat.com> - 3.10.7-1
- test__ped_filesystem.py for for Python 2 vs 3. (dcantrell)

* Thu Aug 27 2015 David Cantrell <dcantrell@redhat.com> - 3.10.6-1
- Use sys.exit instead of os._exit with pocketlint. (clumens)
- Use addCleanup instead of tearDown for removing temp-device. (clumens)
- Add a new makefile target that does everything needed for jenkins.
  (clumens)
- Merge pull request #13 from atodorov/fix_imports (david.l.cantrell)
- Merge pull request #14 from vpodzime/master (david.l.cantrell)
- Do not support and use hashing on pyparted's objects (#1229186) (vpodzime)
- Fix pylint errors (atodorov)
- Merge pull request #12 from atodorov/remove_hardcoded_paths
  (david.l.cantrell)
- Merge pull request #8 from atodorov/tests_ped_filesystem (david.l.cantrell)
- Merge pull request #10 from atodorov/tests_ped_partition (david.l.cantrell)
- Merge pull request #6 from atodorov/add_coverage (david.l.cantrell)
- Remove hard-coded paths. You should have all tools in PATH when working on
  pyparted. (atodorov)
- run the test suite under python-coverage and report the results (atodorov)
- add test coverage for _ped.Partition (atodorov)
- Merge pull request #9 from atodorov/tests_dont_skip_if_root
  (david.l.cantrell)
- Merge pull request #11 from atodorov/fix_api_docs (david.l.cantrell)
- update pydoc descriptions based on actual behavior (atodorov)
- don't skip DeviceGetNextTestCase if running as root (atodorov)
- add test cases for _ped.FileSystem (atodorov)
- Merge pull request #7 from atodorov/tests_readme (david.l.cantrell)
- Remove old BUGS file. (david.l.cantrell)
- add simple test documentation (atodorov)
- Merge pull request #5 from vpodzime/master (david.l.cantrell)
- Beware of Python 3's version of the map() built-in function (vpodzime)
- Remove the MANIFEST file when doing 'make release' (dcantrell)
- Remove fedorahosted steps from the RELEASE file. (dcantrell)
- Update documentation and Makefile for github. (dcantrell)
- Stop using type() to do comparisons. (clumens)
- Merge pull request #4 from vpodzime/master-python3 (david.l.cantrell)
- Don't blindly expect that everything is hashable (vpodzime)
- Replace filter() call with list comprehension (vpodzime)
- Fix an incorrect reference to "type". (clumens)
- Merge pull request #3 from clumens/master (clumens)
- Only run pylint against a python3 build of pyparted. (clumens)
- Fix the fdisk example up to pass pylint. (clumens)
- Catch exact exceptions in a couple places. (clumens)
- Ignore some pylint warnings. (clumens)
- Don't use string formatting in calls to log.whatever. (clumens)
- Fix a couple unused variable warnings. (clumens)
- Define things in the setUp methods, not in runTest. (clumens)
- Don't redefine reserved or already used function names. (clumens)
- Fix import errors turned up by pylint. (clumens)
- Convert to using pocketlint to run pylint. (clumens)
- Don't run "git clean -fdx" in the "make clean" target. (clumens)
- Add extension whitelist for _ped to pylint call (bcl)
- Merge pull request #2 from jflorian/master (david.l.cantrell)
- New - example to create a single bootable partition (john_florian)
- Remember to pass the arguments to the exception handler. (clumens)
- Put new _ped constants and functions into the parted module. (clumens)
- PyInt_FromLong doesn't exist in python3, so always use PyLong_FromLong.
  (clumens)
- Add new functions to extend exception handling. (clumens)
- Add function for resetting partition's number. (vpodzime)
- Fix localeC imports in a handful of src/parted/*.py files. (dcantrell)
- Disable false positive E0611 errors on src/parted/__init__.py (dcantrell)
- ped_unit_get_size() returns a long long, not just a long. (dcantrell)
- Adjust test cases to deal with run-time support. (dcantrell)
- Only import partition types that exist. (dcantrell)
- Note x.y.z version number. (dcantrell)
- Remove .travis.yml and tox.ini (dcantrell)
- Skip 'aix' diskType in FreshDiskTestCase (dcantrell)
- Handle running the test suite on armv7l hosts. (dcantrell)
- Fix getPartitionByPath for disks that are just plain files. (dlehman)
- ext2 may be smaller than the end of the device (#1095904) (bcl)
- support ppc64le in pyparted (hamzy)
- Fix up the PYTHONPATH for "make check" and "make test". (clumens)
- Remove geom tests that don't fail (bcl)
- Add btrfs and ext4 for filesystem type test (bcl)
- Revert "Add support for hfs_esp flag" (bcl)
- Teach pyparted that aarch64 support GPT partitions. (dcantrell)
- And disable the length one, too. (clumens)
- Disable one test case that fails on ppc64, for the moment. (clumens)
- Update pylint options for the latest version of that program. (clumens)
- Fix 'make bumpver' to handle multiple decimal points. (dcantrell)
- Add support for hfs_esp flag (dcantrell)
- Add support for esp flag (dcantrell)
- Add support for irst flag (dcantrell)
- Add support for msftdata flag (dcantrell)
- Don't assume tools will be in the user's $PATH. (clumens)
- Fix a lot of problems pylint caught. (clumens)
- Move from pychecker to pylint. (clumens)
- Have pychecker ignore some fale positives on missing class attrs. (clumens)
- setattr doesn't return any value. (clumens)
- Fix up pychecker errors reported by Jenkins. (dcantrell)
- Subject: [PATCH] pyparted: export ped_disk_new functionality (rnsastry)
- Correct boilerplate modifications. (dcantrell)
- Tests also require the parted binary. (g2p.code)
- Work around Travis's broken defaults. (g2p.code)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.10.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 07 2015 David Cantrell <dcantrell@redhat.com> - 3.10.5-1
- Upgrade to pyparted-3.10.5

* Tue May 05 2015 David Cantrell <dcantrell@redhat.com> - 3.10.4-1
- Upgrade to pyparted-3.10.4

* Fri Jan 16 2015 David Cantrell <dcantrell@redhat.com> - 3.10.3-1
- Upgrade to pyparted-3.10.3

* Wed Nov 26 2014 David Cantrell <dcantrell@redhat.com> - 3.10.2-1
- Upgrade to pyparted-3.10.2

* Mon Nov 10 2014 David Cantrell <dcantrell@redhat.com> - 3.10.1-1
- Upgrade to pyparted-3.10.1

* Wed Sep 24 2014 David Cantrell <dcantrell@redhat.com> - 3.10.0a-1
- Upgrade to pyparted-3.10.0
- Add python3 subpackage (#985308)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 24 2014 David Cantrell <dcantrell@redhat.com> - 3.9.5-1
- Upgrade to pyparted-3.9.5

* Tue Jun 24 2014 David Cantrell <dcantrell@redhat.com> - 3.9.4-2
- Handle building on armv7l hosts

* Tue Jun 24 2014 David Cantrell <dcantrell@redhat.com> - 3.9.4-1
- Support gpt and msdos disk labels on aarch64 (#1095904)

* Thu Jun 12 2014 David Cantrell <dcantrell@redhat.com> - 3.9.3-3
- Fix GetLabelsTestCase for aarch64 (#1102854)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 07 2014 Chris Lumens <clumens@redhat.com> 3.9.3-1
- Upgrade to pyparted-3.9.3
- Revert "Add support for hfs_esp flag" (bcl)
- Add btrfs and ext4 for filesystem type test (bcl)
- Remove geom tests that don't fail (bcl)

* Mon Sep 09 2013 David Cantrell <dcantrell@redhat.com> - 3.9.2-1
- Upgrade to pyparted-3.9.2
- Enable 'make check' in the spec file, patch for koji use
- Add armv7l to the list of acceptable arches for gpt and msdos disklabels

* Mon Sep 09 2013 David Cantrell <dcantrell@redhat.com> - 3.9.1-1
- Fix 'make bumpver' to handle multiple decimal points. (dcantrell)
- Add support for hfs_esp flag (dcantrell)
- Add support for esp flag (bcl)
- Add support for irst flag (bcl)
- Add support for msftdata flag (bcl)
- Subject: [PATCH] pyparted: export ped_disk_new functionality (rnsastry)
- Convert Constraint to __ped.Constraint in partition.getMaxGeometry()
  (chris)
- Do not traceback when calling setlocale (#875354). (clumens)
- Enable 'make check' in the spec file, patch for koji use
- Add armv7l to the list of acceptable arches for gpt and msdos disklabels

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 08 2013 David Cantrell <dcantrell@redhat.com> - 3.9-3
- Revert to pyparted-3.9 plus critical patches due to issues with the 3.10
  release which are actively being worked on.  The 3.10 release does not
  work with the installer right now.

* Thu May 23 2013 David Cantrell <dcantrell@redhat.com> - 3.10-2
- Fix build errors.

* Thu May 23 2013 David Cantrell <dcantrell@redhat.com> - 3.10-1
- Upgrade to pyparted-3.10 (#886033)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 05 2012 David Cantrell <dcantrell@redhat.com> - 3.9-1
- Upgrade to pyparted-3.9

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 13 2012 Brian C. Lane <bcl@redhat.com> - 3.8-4
- Rebuild against parted 3.1

* Thu Feb 02 2012 Brian C. Lane <bcl@redhat.com> - 3.8-3
- Add patch for new parted PED_DISK_GPT_PMBR_BOOT flag

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 29 2011 David Cantrell <dcantrell@redhat.com> - 3.8-1
- Upgraded to pyparted-3.8

* Wed Jun 29 2011 David Cantrell <dcantrell@redhat.com> - 3.7-2
- BR parted-devel >= 3.0
- Adjust for distutils build method

* Wed Jun 29 2011 David Cantrell <dcantrell@redhat.com> - 3.7-1
- Upgraded to pyparted-3.7 (compatibility with parted-3.0)

* Wed Mar 23 2011 David Cantrell <dcantrell@redhat.com> - 3.6-1
- Upgraded to pyparted-3.6

* Thu Mar 17 2011 David Cantrell <dcantrell@redhat.com> - 3.5-3
- Add support for PED_PARTITION_LEGACY_BOOT partition flag now in libparted

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 David Cantrell <dcantrell@redhat.com> - 3.5-1
- Drop dependency on python-decorator module. (dcantrell)
- Differentiate the "Could not commit" messages. (jgranado)
- Import _ped.DiskLabelException into parted namespace (cjwatson)
- Return PED_EXCEPTION_NO for yes/no interactive exceptions. (dcantrell)

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri May 21 2010 David Cantrell <dcantrell@redhat.com> - 3.4-2
- Spec file cleanups to comply with current packaging policies

* Thu Apr 29 2010 David Cantrell <dcantrell@redhat.com> - 3.4-1
- Handle PED_EXCEPTION_WARNING with PED_EXCEPTION_YES_NO (#575749)
  (dcantrell)

* Wed Apr 21 2010 Chris Lumens <clumens@redhat.com> - 3.3-1
- Upgrade to pyparted-3.3 (#583628).

* Wed Mar 31 2010 David Cantrell <dcantrell@redhat.com> - 3.2-2
- Rebuild for libparted soname change

* Thu Mar 25 2010 Chris Lumens <clumens@redhat.com> - 3.2-1
- Upgrade to pyparted-3.2 (#571940).

* Mon Mar 01 2010 David Cantrell <dcantrell@redhat.com> - 3.1-1
- Upgrade to pyparted-3.1 (#567576).

* Tue Jan 12 2010 David Cantrell <dcantrell@redhat.com> - 3.0-1
- Upgrade to pyparted-3.0.

* Mon Jan 11 2010 Hans de Goede <hdegoede@redhat.com> - 2.5-4
- Rebuild for new parted-2.1
- Remove py_disk_clobber_exclude function binding, as this function was
  removed from parted-2.1

* Thu Jan  7 2010 Hans de Goede <hdegoede@redhat.com> - 2.5-3
- Change python_sitearch macro to use %%global as the new rpm will break
  using %%define here, see:
  https://www.redhat.com/archives/fedora-devel-list/2010-January/msg00093.html

* Sat Dec 19 2009 David Cantrell <dcantrell@redhat.com> - 2.5-2
- Exclude pyparted-2.4.tar.gz from source RPM (oops)

* Sat Dec 19 2009 David Cantrell <dcantrell@redhat.com> - 2.5-1
- Update release instructions. (dcantrell)
- Remove old cylinder alignment test cases for _ped. (dcantrell)
- Add tests for max partition length / start sector (hdegoede)
- Add _pedmodule and parted functions for max partition length / start
  sector (hdegoede)
- Remove align_to_cylinders function bindings (hdegoede)
- Add tests for disk flag methods (hdegoede)
- Add _pedmodule and parted functions for per disk flags (hdegoede)
- Every tuple member requires a comma after it. (dcantrell)
- Fill out a lot of simple _ped.Disk test cases. (dcantrell)
- Disable DeviceDestroyTestCase for now. (dcantrell)
- Add RequiresLabeledDevice to tests/_ped/baseclass.py. (dcantrell)
- Attempt at fixing _ped.Device.destroy(), no dice. (dcantrell)
- Fix UnitFormatCustomTestCase and UnitFormatTestCase. (dcantrell)
- Fix UnitFormatCustomByteTestCase and UnitFormatByteTestCase. (dcantrell)
- Add DeviceStrTestCase, disable DeviceDestroyTestCase. (dcantrell)
- Add DeviceDestroyTestCase and DeviceCacheRemoveTestCase. (dcantrell)
- Implemented ConstraintIsSolutionTestCase(). (dcantrell)
- Implement ConstraintSolveMaxTestCase(). (dcantrell)
- Implement ConstraintSolveNearestTestCase(). (dcantrell)
- Correct py_ped_file_system_probe_specific() for NULL returns. (dcantrell)
- Implement FileSystemProbeSpecificTestCase(). (dcantrell)
- Implement FileSystemProbeTestCase(). (dcantrell)
- Add RequiresFileSystem to tests/_ped/baseclass.py. (dcantrell)
- Add disk alignment test cases in test_ped.py. (dcantrell)
- Fix CHSGeometryStrTestCase(). (dcantrell)
- Fix ConstraintDuplicateTestCase...finally. (dcantrell)
- Put a deprecation warning in py_ped_constraint_duplicate(). (dcantrell)
- Note that we need parted from Fedora for pyparted. (dcantrell)
- Fix UnitGetSizeTestCase in _ped test cases for _ped.UNIT_PERCENT.
  (dcantrell)
- Add testcase for new _ped disk get_partition_alignment method (hdegoede)

* Fri Nov 06 2009 David Cantrell <dcantrell@redhat.com> - 2.4-1
- Upgrade to pyparted-2.4:
      Use PedDevice length instead of DIY (#532023) (hdegoede)
      Use sectorSize not physicalSectorSize for size calculations (hdegoede)

* Tue Nov 03 2009 David Cantrell <dcantrell@redhat.com> - 2.3-1
- Upgrade to pyparted-2.3:
      Remove root user requirement in _ped
      Add testcases for new _ped device methods
      Add python wrapper for new PedDisk partition alignment info function
      Add support for new PedDisk parition alignment info function
      Add python wrappers for new PedDevice alignment info functions
      Add support for new PedDevice alignment info functions
      Fix a whole pile of test cases.
      Remove ped_disk_commit_to_dev() call from py_ped_disk_new_fresh()
      Fix error in Constraint __str__ method
      Make _ped_Device2PedDevice properly set / throw exceptions
      Fixup various errorhandling issues in pydisk.c
      Add missing _ped_Device2PedDevice() retval checks
      Use libparted commit() for parted.disk.Disk.commit() (hdegoede).
- BR parted-devel >= 1.9.0-20

* Fri Oct 02 2009 David Cantrell <dcantrell@redhat.com> - 2.2-1
- Upgrade to pyparted-2.2:
      Fixes PedDisk2_ped_Disk() and avoids losing disk label data
      in the conversion process (#526999)

* Mon Aug 17 2009 Chris Lumens <clumens@redhat.com> - 2.1.2-1
- Upgrade to pyparted-2.1.2:
      PED_DEVICE_DM is always defined in libparted these days.
      Handle parted exceptions arising from ped_device_get (#495433).

* Tue Aug 04 2009 David Cantrell <dcantrell@redhat.com> - 2.1.1-1
- Upgrade to pyparted-2.1.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 David Cantrell <dcantrell@redhat.com> - 2.1.0-1
- Upgrade to pyparted-2.1.0, requires parted-1.9.0-1 or higher

* Fri Jul 10 2009 David Cantrell <dcantrell@redhat.com> - 2.0.12-2
- Rebuild for new parted

* Tue Apr 14 2009 David Cantrell <dcantrell@redhat.com> - 2.0.12-1
- Upgrade to pyparted-2.0.12

* Mon Apr 13 2009 David Cantrell <dcantrell@redhat.com> - 2.0.11-1
- Upgrade to pyparted-2.0.11

* Fri Apr 03 2009 David Cantrell <dcantrell@redhat.com> - 2.0.10-1
- Upgrade to pyparted-2.0.10
      Fix LVM problems around parted.Disk.commit() (#491746)

* Mon Mar 23 2009 David Cantrell <dcantrell@redhat.com> - 2.0.9-1
- Upgrade to pyparted-2.0.9

* Fri Mar 20 2009 David Cantrell <dcantrell@redhat.com> - 2.0.8-1
- Upgrade to pyparted-2.0.8

* Thu Mar 19 2009 David Cantrell <dcantrell@redhat.com> - 2.0.7-1
- Upgrade to pyparted-2.0.7

* Thu Mar 12 2009 David Cantrell <dcantrell@redhat.com> - 2.0.6-1
- Upgrade to pyparted-2.0.6

* Thu Mar 05 2009 David Cantrell <dcantrell@redhat.com> - 2.0.5-1
- Upgrade to pyparted-2.0.5

* Sat Feb 28 2009 David Cantrell <dcantrell@redhat.com> - 2.0.4-1
- Upgrade to pyparted-2.0.4

* Fri Feb 27 2009 David Cantrell <dcantrell@redhat.com> - 2.0.3-1
- Upgrade to pyparted-2.0.3

* Wed Feb 25 2009 David Cantrell <dcantrell@redhat.com> - 2.0.2-1
- Upgrade to pyparted-2.0.2

* Mon Feb 16 2009 David Cantrell <dcantrell@redhat.com> - 2.0.1-1
- Upgrade to pyparted-2.0.1 (#485632)

* Thu Feb 12 2009 David Cantrell <dcantrell@redhat.com> - 2.0.0-1
- Upgrade to pyparted-2.0.0

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.8.9-6
- Rebuild for Python 2.6

* Fri Feb 08 2008 David Cantrell <dcantrell@redhat.com> - 1.8.9-5
- Rebuild for gcc-4.3

* Wed Jan 02 2008 David Cantrell <dcantrell@redhat.com> - 1.8.9-4
- Rebuild

* Mon Nov 19 2007 Jeremy Katz <katzj@redhat.com> - 1.8.9-3
- Add support for exact constraints

* Tue Aug 21 2007 David Cantrell <dcantrell@redhat.com> - 1.8.9-2
- Rebuild

* Fri Aug 10 2007 David Cantrell <dcantrell@redhat.com> - 1.8.9-1
- Update license tag to indicate GPL v2 or later
- Update URLs to point to new upstream location

* Fri Jun 15 2007 David Cantrell <dcantrell@redhat.com> - 1.8.8-1
- Clean up wording in package description (#226337)
- BR pkgconfig (#226337)

* Fri Jun 15 2007 David Cantrell <dcantrell@redhat.com> - 1.8.7-1
- Merge review (#226337)

* Mon Apr 23 2007 David Cantrell <dcantrell@redhat.com> - 1.8.6-2
- Ensure build env CFLAGS are included (#226337)

* Thu Apr 19 2007 David Cantrell <dcantrell@redhat.com> - 1.8.6-1
- Merge review (#226337)

* Tue Mar 20 2007 David Cantrell <dcantrell@redhat.com> - 1.8.5-4
- Rebuild for GNU parted-1.8.6

* Tue Mar 20 2007 David Cantrell <dcantrell@redhat.com> - 1.8.5-3
- Rebuild for GNU parted-1.8.5

* Mon Mar 19 2007 David Cantrell <dcantrell@redhat.com> - 1.8.5-2
- Rebuild for GNU parted-1.8.4

* Thu Feb 08 2007 David Cantrell <dcantrell@redhat.com> - 1.8.5-1
- Define and use python_sitearch rather than python_sitelib

* Thu Feb 08 2007 David Cantrell <dcantrell@redhat.com> - 1.8.4-1
- Use preferred BuildRoot (package review)
- Define and use python_sitelib macro (package review)

* Fri Jan 12 2007 David Cantrell <dcantrell@redhat.com> - 1.8.3-1
- Required parted-1.8.2 or higher

* Wed Jan 10 2007 Jeremy Katz <katzj@redhat.com> - 1.8.2-1
- use PyObject_DEL instead of PyMem_DEL

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 1.8.1-3
- rebuild for python 2.5

* Tue Dec 05 2006 David Cantrell <dcantrell@redhat.com> - 1.8.1-2
- Rebuild for GNU parted-1.8.1

* Thu Nov 30 2006 David Cantrell <dcantrell@redhat.com> - 1.8.1-1
- Determine Python version to use in %%build so the source RPM is more
  easily moved between distribution releases.

* Fri Nov 17 2006 David Cantrell <dcantrell@redhat.com> - 1.8.0-1
- Bump version to 1.8.0 and require parted >= 1.8.0
- Remove python-abi Requires line since rpm handles that automatically

* Wed Aug 30 2006 David Cantrell <dcantrell@redhat.com> - 1.7.3-1
- Include parted/constraint.h in required header files

* Wed Aug 30 2006 David Cantrell <dcantrell@redhat.com> - 1.7.2-2
- Require parted-1.7.1 or higher

* Tue Jul 25 2006 David Cantrell <dcantrell@redhat.com> - 1.7.2-1
- Add HPSERVICE, PALO, PREP, and MSFT_RESERVED to partition types list

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.7.1-1.1
- rebuild

* Sun May 28 2006 David Cantrell <dcantrell@redhat.com> - 1.7.1-1
- Bump version to 1.7.1 and require parted >= 1.7.1

* Fri May 19 2006 David Cantrell <dcantrell@redhat.com> - 1.7.0-1
- Bump version to 1.7.0 and require parted >= 1.7.0

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 11 2005 Peter Jones <pjones@redhat.com> - 1.6.10-1
- rebuild for new parted.
- add debugging options for make so debuginfo isn't useless

* Wed Nov  9 2005 Jeremy Katz <katzj@redhat.com> - 1.6.9-5
- rebuild for new parted

* Wed Aug 31 2005 Chris Lumens <clumens@redhat.com> 1.6.9-4
- Rebuilt for new parted library.

* Wed Mar 16 2005 Chris Lumens <clumens@redhat.com> 1.6.9-3
- Updated for gcc4 and python2.4.  Fixed build warnings.

* Tue Dec 14 2004 Jeremy Katz <katzj@redhat.com> - 1.6.9-2
- add support for sx8 devices

* Mon Nov  8 2004 Jeremy Katz <katzj@redhat.com> - 1.6.8-3
- rebuild for python 2.4

* Mon Oct 11 2004 Warren Togami <wtogami@redhat.com> - 1.6.8-2
- #135100 req python-abi (Robert Scheck)

* Tue Aug 17 2004 Jeremy Katz <katzj@redhat.com> - 1.6.8-1
- update for new parted ABI
  - device -> heads, sectors, cylinders now refer to the bios geometry
- require parted >= 1.6.12

* Thu Jul 22 2004 Jeremy Katz <katzj@redhat.com> - 1.6.7-3
- build on ppc64 again

* Thu May 13 2004 Jeremy Katz <katzj@redhat.com> - 1.6.7-1
- fix build for newer versions of gcc (fix from Jeff Law)

* Tue Mar 16 2004 Jeremy Katz <katzj@redhat.com> 1.6.6-2
- fix PARTITION_PROTECTED definition (#118451)

* Fri Mar 12 2004 Jeremy Katz <katzj@redhat.com>
- Initial build split out into separate source from the parted package.
- Don't build on ppc64 right now due to parted build problems (#118183)
