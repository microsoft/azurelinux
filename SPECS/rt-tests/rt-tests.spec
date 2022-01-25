%define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib; import sys; sys.stdout.write(get_python_lib(1))")

Summary:       Programs that test various rt-features
Name:          rt-tests
Version:       1.8
Release:       15%{?dist}
License:       GPLv2
Vendor:        Microsoft Corporation
Distribution:  Mariner
Group:         Development/Tools
URL:           git://git.kernel.org/pub/scm/utils/rt-tests/rt-tests.git
Source0:       https://www.kernel.org/pub/linux/utils/rt-tests/older/%{name}-%{version}.tar.xz
ExclusiveArch: x86_64
Requires:      bash
Requires:      bc
Requires:      python3
BuildRequires: libnuma-devel
BuildRequires: python3-devel
Patch1:        cyclictest-Fix-setaffinity-error-on-large-NUMA-machines.patch
Patch2:        rt-tests-queuelat-Fix-storing-unsigned-long-long-int.patch
Patch3:        rt-tests-cyclictest-remove-the-debug-log-pid-xxx-in-.patch
Patch4:        rt-tests-improvements-to-the-python-style-in-get_cyc.patch
Patch5:        rt-tests-pi_stress.8-Remove-unused-t-n-from-the-manp.patch
Patch6:        rt-tests-ptsematest.8-Update-the-ptsematest-man-page.patch
Patch7:        rt-tests-Add-a-man-page-for-get_cyclictest_snapshot.patch
Patch8:        rt-tests-Tweak-the-cyclictest-man-page.patch
Patch9:        rt-tests-get_cyclictest_snapshot-Warn-if-no-cyclicte.patch
Patch10:       rt-tests-Install-new-man-page-get_cyclictest_snapshot.patch
Patch11:       pi_stress-limit-the-number-of-inversion-groups-to-th.patch
Patch12:       rt-tests-cyclictest-Move-ftrace-helpers-into-rt-util.patch
Patch13:       rt-tests-oslat-Init-commit.patch
Patch14:       rt-tests-oslat-Proper-reformat-of-code.patch

%description
rt-tests is a set of programs that test and measure various components of
real-time kernel behavior. This package measures timer, signal, and hardware
latency. It also tests the functioning of priority-inheritance mutexes.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1

%build
make %{?_smp_mflags} NUMA=1 HAVE_PARSE_CPUSTRING_ALL=1

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
mkdir -p %{buildroot}/%{python3_sitelib}
make %{?_smp_mflags} DESTDIR=%{buildroot} prefix=%{_prefix} install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%license COPYING
%caps(cap_sys_rawio+ep) /usr/bin/cyclictest
/usr/bin/pi_stress
/usr/bin/signaltest
/usr/bin/hwlatdetect
/usr/bin/rt-migrate-test
/usr/bin/pip_stress
/usr/bin/ptsematest
/usr/bin/sigwaittest
/usr/bin/svsematest
/usr/bin/pmqtest
/usr/bin/hackbench
/usr/bin/cyclicdeadline
/usr/bin/deadline_test
/usr/bin/queuelat
/usr/bin/ssdd
/usr/bin/oslat
/usr/bin/determine_maximum_mpps.sh
/usr/bin/get_cpuinfo_mhz.sh
/usr/bin/get_cyclictest_snapshot
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/*
%doc
/usr/share/man/man8/cyclictest.8.gz
/usr/share/man/man8/hackbench.8.gz
/usr/share/man/man8/hwlatdetect.8.gz
/usr/share/man/man8/pi_stress.8.gz
/usr/share/man/man8/pmqtest.8.gz
/usr/share/man/man8/ptsematest.8.gz
/usr/share/man/man8/rt-migrate-test.8.gz
/usr/share/man/man8/signaltest.8.gz
/usr/share/man/man8/sigwaittest.8.gz
/usr/share/man/man8/svsematest.8.gz
/usr/share/man/man8/pip_stress.8.gz
/usr/share/man/man8/queuelat.8.gz
/usr/share/man/man8/deadline_test.8.gz
/usr/share/man/man8/cyclicdeadline.8.gz
/usr/share/man/man8/ssdd.8.gz
/usr/share/man/man8/oslat.8.gz
/usr/share/man/man8/get_cyclictest_snapshot.8.gz

%changelog
* Thu Jan 20 2022 Cameron Baird <cameronbaird@microsoft.com> 1.8-14
- Initial import into CBL Mariner (License: GPL+)
- License verified

* Wed Mar 17 2021 Hernan Gatta <hegatta@microsoft.com> 1.8-12
- Initial import into ECF Mariner (License: GPLv2)

* Thu Aug 20 2020 John Kacur <jkacur@redhat.com> - 1.8-11
- Add SPDX license to oslat, and reformat source code to match suite
Resolves: rhbz#1870666

* Wed Aug 19 2020 John Kacur <jkacur@redhat.com> - 1.8-10
- Remove undated Obsoletes from the specfile
Resolves: rhbz#1870212

* Wed Aug 19 2020 John Kacur <jkacur@redhat.com> - 1.8-9
- Add the oslat program to the rt-tests suite
Resolves: rhbz#1869882

* Wed Jul 22 2020 John Kacur <jkacur@redhat.com> - 1.8-8
- Change the conversion format to %ld for the num_processors in pi_stress
Resolves: rhbz#1859397

* Wed Jul 22 2020 John Kacur <jkacur@redhat.com> - 1.8-7
- Limit the number of inversion groups in pi_stress
Resolves: rhbz#1859397

* Mon Jul 06 2020 John Kacur <jkacur@redhat.com> - 1.8-6
- Install new man page get_cyclictest_snapshot
Resolves: rhbz#1826777

* Mon Jul 06 2020 John Kacur <jkacur@redhat.com> - 1.8-5
- get_cyclictest_snapshot: print a warning message if there are no
  running cyclictest instances
Resolves: rhbz#1826783

* Mon Jul 06 2020 John Kacur <jkacur@redhat.com> - 1.8-4
- Add a get_cyclictest_snapshot man page and various small fixes
Resolves: rhbz#1826777

* Tue May 12 2020 John Kacur <jkacur@redhat.com> - 1.8-3
- Fix integer overflow in queuelat
Resolves: rhbz#1803862

* Mon May 04 2020 John Kacur <jkacur@redhat.com> - 1.8-2
- Fix setaffinity error on large numa machines
Resolves: rhbz#1831269

* Mon Apr 20 2020 John Kacur <jkacur@redhat.com> - 1.8-1
- Update to upstream rt-tests-1.8
Resolves: rhbz#1816370

* Thu Jan 23 2020 John Kacur <jkacur@redhat.com> - 1.5-18
- Add a man page for cyclicdeadline
- Sync cyclictest man page with the help option
- Sync pi_stress man page with the help option
- Add pi_stress short options to usage message
- Add -S --smp to svsematest man page
- Update ptsematest man page and add -h option
- queuelat man page and help fixes
- display svsematest help without an error message
Resolves: rhbz#1766656

* Fri Jan 17 2020 John Kacur <jkacur@redhat.com> - 1.5-17
- Fix more quoting problems to prevent work splitting
- get_cpuinfo_mhz.sh should print one value
Resolves: rhbz#1719493

* Wed Jan 15 2020 John Kacur <jkacur@redhat.com> - 1.5-16
- Fix hardcoded path to queuelat in determine_maximum_mpps.sh
Resolves: rhbz#1791403

* Mon Nov 25 2019 John Kacur <jkacur@redhat.com> - 1.5-15
- Respun Add SPDX tags patch to correct two incorrect licenes
Resolves: rhbz#1721215

* Mon Nov 25 2019 John Kacur <jkacur@redhat.com> - 1.5-14
- Add SPDX tags
Resolves: rhbz#1721215

* Fri Nov 22 2019 John Kacur <jkacur@redhat.com> - 1.5-13
- Improved version of getting a snapshot of cyclictest without interrupting
- Fixes some problems uncovered by covscan
Resolves: rhbz#1469185

* Tue Nov 19 2019 John Kacur <jkacur@redhat.com> - 1.5-12
- Get a running snapshot of cyclictest without interrupting it
Resolves: rhbz#1469185

* Tue Nov 12 2019 John Kacur <jkacur@redhat.com> - 1.5-11
- Add short and long options and help to ssdd
Resolves: rhbz#1720360

* Mon Nov 11 2019 John Kacur <jkacur@redhat.com> - 1.5-10
- Fix some warnings in determine_maximum_mpps.sh
Resolves: rhbz#1719493

* Wed Oct 30 2019 John Kacur <jkacur@redhat.com> - 1.5-9
-Use libnuma version 2 by default
Resolves: rhbz#1753758

* Wed Oct 30 2019 John Kacur <jkacur@redhat.com> - 1.5-8
- Don't allow OPT_SYSTEM with OPT_POSIX_TIMERS
Resolves: rhbz#1753026

* Wed Oct 30 2019 John Kacur <jkacur@redhat.com> - 1.5-7
- Set affinity before applying numa
Resolves: rhbz#1749958

* Tue Oct 29 2019 John Kacur <jkacur@redhat.com> - 1.5-6
- Increase buffers to avoid overflow
Resolves: rhbz#1753317

* Fri Oct 25 2019 John Kacur <jkacur@redhat.com> - 1.5-5
- Remove invalid / obsolete tracing options from cyclictest manpage
Resolves: rhbz#1749238

* Fri Oct 25 2019 John Kacur <jkacur@redhat.com> - 1.5-4
- Make tracemark work correctly again
Resolves: rhbz#1725134

* Wed Oct 23 2019 John Kacur <jkacur@redhat.com> - 1.5-3
- Add Requires bc for queuelat
Resolves: rhbz#1764290

* Tue Oct 15 2019 John Kacur <jkacur@redhat.com> - 1.5-2
- Add bash as a Require in the spec file, since the suite contains some scripts
Resolves: rhbz#1744983

* Tue Oct 15 2019 John Kacur <jkacur@redhat.com> - 1.5-1
- Rebase to upstream rt-tests-1.5
Resolves: rhbz#1722521

* Wed Jul 31 2019 John Kacur <jkacur@redhat.com> - 1.3-21
- Fix problem when tests use tracing_enabled which is no longer supported
Resolves: rhbz#1731336

* Fri Jun 14 2019 John Kacur <jkacur@redhat.com> - 1.3-20
- Add a manpage for ssdd
Resolves: rhbz#1718735

* Fri May 10 2019 John Kacur <jkacur@redhat.com> - 1.3-19
- Disable/enable c-state transitions during hwlatdetect run
Resolves: rhbz#1707505

* Tue May 07 2019 John Kacur <jkacur@redhat.com> - 1.3-18
- Install queuelat scripts
Resolves: rhbz#1686494

* Thu Apr 25 2019 John Kacur <jkacur@redhat.com> - 1.3-17
- Add ssdd test to the rt-tests suite
Resolves: rhbz#1666351

* Thu Mar 28 2019 John Kacur <jkacur@redhat.com> - 1.3-16
- cyclictest-Make-sure-affinity-is-respected-when-numa.patch
- cyclictest-Fix-compiler-warning-about-srncpy-output.patch
- cyclictest-fix_with_expected_identifier_in_latest.patch
Resolves: rhbz#1596857

* Tue Jan 08 2019 John Kacur <jkacur@redhat.com> - 1.3-13
- queuelat: use mfence for rdtsc ordering
Resolves: rhbz#1663865

* Thu Nov 15 2018 John Kacur <jkacur@redhat.com> - 1.3-12
- Add NULL check before freeing setcpu_buf
Resolves: rhbz#1641971

* Tue Nov 06 2018 John Kacur <jkacur@redhat.com> - 1.3-11
- Fix the spec file to remove debuginfo from the standard queuelat files
Resolves: rhbz#1641978

* Mon Nov 05 2018 John Kacur <jkacur@redhat.com> - 1.3-10
- Remove numa from help since it is invokved automatically
Resolves: rhbz#1646121

* Fri Nov 02 2018 John Kacur <jkacur@redhat.com> - 1.3-9
- Add a manpage for deadline_test
Resolves: rhbz#1645071

* Mon Oct 08 2018 John Kacur <jkacur@redhat.com> - 1.3-8
- Remove backfire and sendme
Resolves: rhbz#1624885

* Fri Sep 28 2018 John Kacur <jkacur@redhat.com> - 1.3-7
- Change python3 to platform-python
Resolves: rhbz#1633607

* Mon Sep 17 2018 John Kacur <jkacur@redhat.com> - 1.3-6
- rt-tests-pi_stress-remove-unused-report-options.patch
- rt-tests-pip_stress-Add-an-initial-man-page-for-pip_stress.patch
- add-h-option-to-queuelat.patch
- Add-queuelat-manpage.patch
- Modify makefile for queuelat.8 and pip_stress.8
Resolves: rhbz#1614783

* Fri Jun 22 2018 John Kacur <jkacur@redhat.com> - 1.3-5
- Reimplement the removal of --numa, and automate it's detction
Resolves: rhbz#1594273

* Tue Jun 12 2018 John Kacur <jkacur@redhat.com> - 1.3-4
- A few more python3 changes

* Wed May 30 2018 John Kacur <jkacur@redhat.com> - 1.3-3
- Add patches that remove --sma and --numa and automate it
Resolves: rhbz#1518708

* Wed May 30 2018 John Kacur <jkacur@redhat.com> - 1.3-2
- cyclictest: remove tracing, in favour of external tracing
Resolves: rhbz#1518268

* Mon Apr 30 2018 John Kacur <jkacur@redhat.com> - 1.3-1
- New build
- Add test queuelat
- Adds changes for python3 in hwlatdetect
Resolves: rhbz#1543030
Resolves: rhbz#1559520

* Tue Mar 27 2018 John Kacur <jkacur@redhat.com> - 1.2-1
- Remove old patches from the source files
Resolves: rhbz#1559930

* Mon Mar 26 2018 John Kacur <jkacur@redhat.com> - 1.2-0
- Initial Build for 8.0
Resolves: rhbz#1559930

* Wed Dec 20 2017 John Kacur <jkacur@redhat.com> - 1.0.13
- rt-tests-Need-to-generate-debug-info-for-rpms.patch
Resolves: rhbz#1523752

* Thu Nov 02 2017 John Kacur <jkacur@redhat.com> - 1.0.12
- cyclictest: cannot stop when running with -M option
Resolves: rhbz#1473786

* Tue Apr 25 2017 John Kacur <jkacur@redhat.com> - 1.0.11
- cyclictest-touch-threadstacks-on-numa-to-pre-fault-t.patch
Resolves: rhbz1445058

* Thu Mar 23 2017 John Kacur <jkacur@redhat.com> - 1.0.10
- hwlatdetect: modify hwlatdetector.py to use the ftrace hwlatdetector
- hwlatdetect: removed smi_detector support
Resolves: rhbz1365961

* Thu Mar 23 2017 John Kacur <jkacur@redhat.com> - 1.0.9
- hwlatdetect: Add --hardlimit to define the real test failing criteria
Resolves: rhbz1434827

* Thu Mar 23 2017 John Kacur <jkacur@redhat.com> - 1.0.8
- cyclicdeadline: Fix minor spelling mistake
- cyclictest: Correct short option 's'
Resolves: rhbz1434825

* Tue Mar 21 2017 John Kacur <jkacur@redhat.com> - 1.0.7
- rt-tests: hwlatdetect: Improve message if max latency is below threshold
Resolves: rhbz1366289

* Thu Jun 30 2016 John Kacur <jkacur@redhat.com> - 1.0-6
- deadline_test: Made '-i' work and added help text for it
Resolves: rhbz1346771

* Tue Jun 28 2016 John Kacur <jkacur@redhat.com> - 1.0-5
- z-stream release

* Thu Jun 23 2016 John Kacur <jkacur@redhat.com> - 1.0-4
- Add cyclicdeadline and deadline_test to rt-tests
Resolves: rhbz#1349032

* Fri Jun 17 2016 John Kacur <jkacur@redhat.com> - 1.0-3
- Install cyclictest with cap_sys_rawio to access msr and cpuid registers
- Fixed url in Source0
Resolves: rhbz#1346771

* Wed Jun 01 2016 John Kacur <jkacur@redhat.com> - 1.0-2
- cyclictest: new CPUs with SMI counter support
Resolves: rhbz#1341226

* Fri May 20 2016 John Kacur <jkacur@redhat.com> - 1.0-1
- Upgrade to 1.0
Clark Williams (1):
  cyclictest: stop any tracing after hitting a breaktrace threshold
John Kacur (8):
  rt-tests: Makefile: Assume numa_parse_cpustring_all available
  rt-tests: Add man page for rt-migrate-test
  rt-tests: Update the cyclictest man page
  rt-tests: Add missing option to hwlatdetect man page
  rt-tests: Housekeeping fix some spelling errors.
  rt-tests: hwlat.txt: smidetect renamed to hwlatdetect
  rt-tests: Remove doc/release-checklist.txt
  rt-tests: Makefile - bump version to 1.0
- Add patch to install rt-migrate-test.8-man-page
Resolves: rhbz#1283264
- The latest build also includes fixes for undocumented options in cyclictest and hwlatdetect, as well as many more documentation fixes.
Resolves: rhbz#1263718
- Also documenting here that the new feature cyclictest: SMI count/detection via MSR/SMI counter was added in v0.97
Resolves: rhbz#1314869

* Tue May 10 2016 John Kacur <jkacur@redhat.com> - 0.97-3
- cyclictest: stop any tracing after hitting a breaktrace threshold
- Resolves: rhbz#1333762

* Tue Apr 26 2016 John Kacur <jkacur@redhat.com> - 0.97-2
- Change spec file to compile with HAVE_PARSE_CPUSTRING_ALL=1
	- This makes numa_parse_cpustring_all() available which is needed for
		running cyclictest on isolated cpus.
- Resolves: rhbz#1330468

* Mon Apr 04 2016 John Kacur <jkacur@redhat.com> - 0.97-1
- Changes from v0.93 to v0.97
Clark Williams (9):
  hwlatdetect: initial cut at tracking the amount of SMIs that occurred
    during a run
  rt-migrate-test: updated to latest code from rostedt
  Makefile: add target to create OBJDIR before use
  specfile: add signaltest manpage to files section and remove trailing
    whitespace in changelog
  Makefile: have distclean remove .asc file for tarball
  Makefile: fixed dropped quote in help target text
  hwlatdetect: handle hwlat_detector being builtin rather than module
  hwlatdetect: modify to handle python3 prints
  hwlatdetect: make reading sample date work with python2 and python3
Daniel Bristot de Oliveira (2):
  cyclictest: SMI count/detection via MSR/SMI counter
  cyclictest: Add --smi description on cyclictest man page
Darren Hart (2):
  rt-tests: Allow for user-specified PYLIB
  rt-tests: Break out install_hwlatdetect
Henrik Austad (10):
  Add CROSS_COMPILE-switch to CC and AR
  Add syscall-number for sched_(gs)etattr() for tile
  Add a rebuild-switch to Makefile
  Makefile: add librttest to rt-migrate-test
  android: adjust target for android
  cyclictest: move redefine of CPUSET back to uclib
  Android: clean up the bypass ifdeffery
  Android: rename arch from bionic to android
  Android: Expand match for android in ostype
  rt-sched.h: do not unconditionally define syscall-numbers
John Kacur (26):
  Fix VERSION in rt-migrate-test
  numa_on_and_available: Remove from main in cyclictest
  Version bump to v0.94
  Explicitly separate VPATH paths with a colon
  build: Generate .o, .a, and .d files in bld dir
  signaltest: call process_options before calling check_privs
  signaltest: Check the status of pthread_create
  rt-utils: Add John Kacur to the copyright
  rt-utils: Fix some checkpatch errors in rt-utils.c
  signaltest: Add a man page to signaltest
  Makefile: Document certain compiling options
  Makefile: Only call cc -dumpmachine once in the makefile
  Bionic: Move android functionality into it's own arch Makefile
  maintainence: VERSION bump and Change-log update
  cyclictest: Clean-ups in timerthread before working on it
  Makefile: OBJDIR should be an order-only-prerequisite
  Makefile: Move TARGETS back to a more logical place in the Makefile
  cyclictest: Add a feature to record spikes
  cyclictest: fix #ifdef broken by NO_PTHREAD_SETAFFINITY
  Makefile: Version bump to v0.96
  Remove rt-tests.spec-in
  gitattributes: add doc, remove rt.spec-in
  Makefile: Remove anything to do with rpms, specs etc
  Revert changes to rt-migrate-test for exit(1)
  cyclictest: Make the tracemark option imply notrace
  rt-tests: Makefile: Bump version number to 0.97
Josh Cartwright (8):
  rt-tests: workaround poor gzip implementations
  hackbench: cleanup error handling in create_worker
  cyclictest: consistently make all functions 'static'
  cyclictest: use correct type when allocating cpu bitmask size
  cyclictest: drop impossible use_fifo conditional
  cyclictest: fail if use_fifo && thread creation failed
  error: mark fatal, err_exit, err_quit as being noreturn
  cyclictest: add option for dumping the histogram in a file
Khem Raj (1):
  Makefile: Set CC/AR variable only if it doesn't have a value
Luiz Capitulino (5):
  don't use exit(-1) for failures
  cyclictest: move tracemark_fd handling to its own function
  cyclictest: tracing(): check for notrace
  cyclictest: move debugfs init code to its own function
  cyclictest: add --tracemark option
Uwe Kleine-König (5):
  backfire: remove unused header file
  remove several unused Makefiles
  rt-migrate-test: remove space before \n
  drop compiling without NPTL support
  Fix some trivial typos found by codespell(1)
- Resolves: rhbz#1283264

 * Wed Aug 12 2015 Clark Williams <williams@redhat.com> - 0.93-1
John Kacur (6):
  makefile: Create an rt-tests.tar file using git-archiv
  makefile: Change VERSION_STRING to VERSIO
  Add .tar files to .gitignor
  Create a .gitattribute file to specify what files git-archive should ignore
  pi_stress: Fix possible exit on error without releasing mutex
  pip_stress: Fix warning: unused variable ‘c’
Alexander Stein (1):
  cyclictest: Fix long priority help text option
Clark Williams (3):
  hwlatdetect: added --watch option to watch output in realtime
  doc: fix VERSION in release-checklist.tx
  makefile: fixed release targ

 * Tue Jun 09 2015 John Kacur <jkacur@redhat.com> - 0.92-1
Anna-Maria Gleixner (2):
  cyclictest: Convert the offset of the alignment option to microseconds
  cyclictest: Align measurement threads to the next full second
  cyclictest: Ensure that next wakeup time is never in the past
Daniel Wagner (1):
  pi_stress: Clear affinity for DEADLINE tasks
John Kacur (3):
  Fix minor grammar mistake in the help output
  Allow building with -DHAVE_PARSE_CPUSTRING_ALL
  Add a MAINTAINERS file
Michael Olbrich (2):
  Makefile: pi_stress need librttest.a so it should depend on it
  Makefile: cleanup linking to librttest.a
Sebastian Andrzej Siewior (1):
  cyclictest: consider the 4 as the major version

 * Tue Feb 17 2015 Clark Williams <williams@redhat.com> - 0.91-1
- From Boris Egorov <egorov@linux.com>
  - rt-migrate-test: exit early if nr_runs is non-positive
  - rt-migrate-test: use variables instead of macros
- From Uwe Kleine-König <u.kleine-koenig@pengutronix.de>
  - pi_stress: remove timestamp of compilation from version output
- rt-migrate-test: make sure input parameters are converted to correct units
- rt-migrate-test: sanity check --prio value

* Tue Jan 27 2015 Clark Williams <williams@redhat.com> - 0.90-1
- pip_stress: parameterize usleep value to work-around platform issues
- From Daniel Wagner <daniel.wagner@bmw-carit.de>:
  - pi_stress: Store schedule attributes per thread
  - rt-utils: Add gettid()
  - rt-utils: Add helper to parse/print scheduling policies
  - rt-sched: Add sched_setattr/sched_getattr API
  - pi_stress: Use error.h for logging and debugging
  - error: Add debug() function
  - pi_stress: Remove unused TIMER_SIGNAL definition
  - rt-tests.h: Remove unused header file
  - hackbench: Don't re-assign context for each fd
- From Joakim Hernberg <jbh@alchemy.lu>:
  - cyclictest: make affinity option only use number of online cpus
- From John Kacur <jkacur@redhat.com>:
  - cyclictest: Add long option --laptop to preserve battery power
  - cyclictest: Fix help for long options only
  - cyclictest: Change the output from function sighand() to stderr
  - cyclictest: Always print an err message if write of 0 to cpu-dma_latency fails
  - rt_numa.h: Suppress discards 'const' qualifier warning
  - lib: Rework err_msg_n to output strerror after message
- From Alexey Brodkin <Alexey.Brodkin@synopsys.com>:
  - Makefile: allow building selected tests with non-NPTL toolchain

* Sun Mar 30 2014 Clark Williams <williams@redhat.com> - 0.89-1
- clean up debugging comments and printfs from last release
- ran hwlatdetect.py through 2to3, works for both python2 and 3

* Fri Mar 28 2014 Clark Williams <williams@redhat.com> - 0.88-1
- From Uwe Kleine-König <u.kleine-koenig@pengutronix.de>:
  - cyclictest: Fix tracemark output when the latency threshold is hit on ARM
- From Gary S. Robertson <gary.robertson@linaro.org>:
  - cyclictest: Restore CPU affinity function for non-NUMA builds
  - cyclictest: Don't offer --numa option when unavailable

* Wed Dec 11 2013 Clark Williams <williams@redhat.com> - 0.87-1
- From Aaron Fabbri <ajfabbri@gmail.com>:
  - cyclictest: CPU affinity now takes arbitrary set of cpus

* Fri Nov 15 2013 Clark Williams <williams@redhat.com> - 0.86-1
- cyclictest: allow break threshold without doing any tracing
- cyclictest: add named fifo for statistics
- from John Kacur <jkacur@redhat.com>:
  - cyclictest: Align option fixes
  - Makefile: Don't tag files in dir BUILD from rpm builds
  - Makefile: Add BUILDROOT and SPECS to the dirs to remove for distclean
  - Makefile: Add tmp dir to distclean and "make release" call distclean
  - Makefile: Don't tag tmp files created when making a release
- from Nicholas Mc Guire <der.herr@hofr.at>:
  - cyclictest: add align thread wakeup times option
- cyclictest: modify option handling to use enumerated types
- from Sebastian Andrzej Siewior <bigeasy@linutronix.de>:
  - hackbench: init child's struct before using it
- from Jim Somerville <Jim.Somerville@windriver.com>:
  - cyclictest: finish removal of 1 second first loops
- from Frank Rowand <frank.rowand@am.sony.com>:
  - rt-tests: NUMA optional for make rpm
  - cyclictest: white space cleanup

* Tue Nov 13 2012 Clark Williams <williams@redhat.com> - 0.85-1
- [cyclictest] add tracemark function back to breaktrace logic
- from Frank Rowand <frank.rowand@am.sony.com>:
  - [cyclictest] report large measured clock latency
  - [cyclictest] cleanup getopt_long() parameters
- from John Kacur <jkacur@redhat.com>:
  - [Makefile] add CPPFLAGS to pattern rule for dependencies
  - [gitignore] exclude patches and .a archives
- from Uwe Kleine-König <u.kleine-koenig@pengutronix.de>:
  - Makefile: separate CFLAGS and CPPFLAGS
  - have printf use %s format for strings
- from Bhavesh Davda <bhavesh@vmware.com>:
  - cyclictest: histogram overflow instance tracking
  - cyclictest: whitespace cleanup

* Wed May  9 2012 Clark Williams <williams@redhat.com> - 0.84-1
- [cyclictest] added -Q/--priospread option to
- from Markus Kohlhase <mail@markus-kohlhase.de>
  - [docs] added description from osadl.org
- from Darren Hart <dvhart@linux.intel.com>
  - Makefile: Support user supplied CFLAGS and LDFLAGS
- from Steven Rostedt <rostedt@goodmis.org>
  - rt-tests: Update rt-migrate-test to use ftrace infrastructure
- from John Kacur <jkacur@redhat.com>
  - .gitignore: differentiate between program names and directories
  - pi_stress: Check the status of sched_getaffinity
  - Makefile: Introduce a static library
  - Move info, warn, and fatal functions to error.[ch]
  - install: Fix failed to create symbolic link hwlatdetect file exists
  - cyclictest: Make cyclictest fail if it cannot run with requested priority
- from Frank Rowand <frank.rowand@am.sony.com>
  - cyclictest: segfault with '-a'
  - cyclictest: avoid unneeded warning
  - cyclictest: warn of interaction between '-a', '--smp', and '--numa'
  - Makefile: get machinetype from compiler instead of uname
  - cyclictest: incorrect first latency value for --verbose option
  - cyclictest: printf format compile warning

* Mon Sep 26 2011 Clark Williams <williams@redhat.com> - 0.83-1
- modified Makefile to be smarter about building with NUMA

* Wed Sep 21 2011 Clark Williams <williams@redhat.com> - 0.82-1
- fix print that causes error in histogram processing

* Tue Sep 20 2011 Clark Williams <williams@redhat.com> - 0.81-1
- cleaned up previous hack for /dev/cpu_dma_latency interface

* Tue Sep 20 2011 Clark Williams <williams@redhat.com> - 0.80-1
- use /dev/cpu_dma_latency interface to prevent cstate transitions
  in cyclictest

* Thu Sep 15 2011 Clark Williams <williams@redhat.com> - 0.79-1
- added signal_workers routine to hackbench
- added -F/--fifo option to hackbench

* Wed Sep 14 2011 Clark Williams <williams@redhat.com> - 0.78-1
- modified hackebench signal logic

* Fri Sep  9 2011 Clark Williams <williams@redhat.com> - 0.77-1
- removed tracemark functions (too much contention on multiprocessors)

* Wed Sep  7 2011 Clark Williams <williams@redhat.com> - 0.76-1
- only turn on /proc/sys/kernel/ftrace_enabled for a tracer that
  needs it
- make sure to set current_tracer to function for -f switch

* Fri Sep  2 2011 Clark Williams <williams@redhat.com> - 0.75-1
- added utility routines for mounting debugfs and event/tracing manipulation
- from Steven Rostedt <srostedt@redhat.com>:
  - allow events for all tracers
  - Have -I and -P together also be -B
  - do not touch tracing_thresh
  - only check file descriptor in tracemark() function
  - use interval on first loop instead of 1 second
  - allow tracemark() to take variable args

* Thu Aug 18 2011 Clark Williams <williams@redhat.com> - 0.74-1
- changes to deal with 3.0 kernel
- fixed buildrequires in specfile for Python
- fixed spelling error in printf in cyclictest
- from John Kacur <jkacur@redhat.com>
  - Make the function header style consistent with the rest of cyclictest.
  - Spelling clean-ups
- from Uwe Kleine-König <u.kleine-koenig@pengutronix.de>
  - fix possible buffer overflow in string handling

* Mon May  9 2011 Clark Williams <williams@redhat.com> - 0.73-1
- fixed signal handling in hackbench (avoid thousands of zombies)
- from Geunsik Lim <geunsik.lim@samsung.com>
  - fix incorrect wakeup interface in cyclictest
- from Wolfram Sang <w.sang@pengutronix.de>
  - Simplify Makefile using -D option to install
- from Carsten Emde <C.Emde@osadl.org>
  - add histogram summary column option (-H) to cyclictest
- from Daniel Sangorrin <daniel.sangorrin@gmail.com>
  - fix sched_setaffinity type error when building with UCLIB
- from Uwe Kleine-König <u.kleine-koenig@pengutronix.de>
  - install backfire's Makefile
  - modernize backfire's Makefile

* Fri Jun 25 2010 Clark Williams <williams@redhat.com> - 0.72-1
- changed 'diff' variable in timerthread() routine to be unsigned
  64-bit to avoid overflow issues in debugging
- included <stdint.h> and changed all 'long long' declarations to
  use uint64_t and int64_t

* Tue May 18 2010 Clark Williams <williams@redhat.com> - 0.71-1
- from Michal Schmit <mschmidt@redhat.com>:
  - fix accumulating overruns in periodic timer mode

* Fri Apr  9 2010 Clark Williams <williams@redhat.com> - 0.70-1
- from Olaf Hering <olaf@aepfle.de>
  - skip python dependency during install if python not available

* Fri Apr  9 2010 Clark Williams <williams@redhat.com> - 0.69-1
- fix bus error in cyclictest on NUMA systems with more than 16 cores
- reset default cyclictest policy to SCHED_OTHER
- from Carsten Emde <C.Emde@osadl.org>
  - add pmqest program for testing posix message queue performance
  - misc doc fixes

* Fri Mar 19 2010 Clark Williams <williams@redhat.com> - 0.68-1
- fix tracing difference between 2.6.24 and 2.6.33

* Tue Mar 16 2010 Clark Williams <williams@redhat.com> - 0.67-1
- modified specfile to add hackbench
- modified internal ftrace logic for correct tracing
- Changed rpm %description field to be more descriptive (BZ# 572323)
- from Carsten Emde <c.emde@osadl.org>
  - added smp option to svsematest
  - fixed policy display in cyclictest
- from John Kacur <jkacur@redhat.com>
  - changed default scheduling policy to SCHED_FIFO
  - fixed spelling mistake on cyclictest man page
  - use symbolic names for scheduling policy
  - reverted commit 582be2a52c43801a10d318de7491f1cc7243d5cf to
    deal with bug in priority distribution
- from Uwe Kleine-König <u.kleine-koenig@pengutronix.de>
  - renamed pip to pip_stress
  - eliminated use of temp files in dependency generation
  - install backfire.c module source in /usr/src/backfire
- from David Sommerseth <davids@redhat.com>
  - added new-and-improved hackbench to rt-tests

* Mon Feb 15 2010 Clark Williams <williams@redhat.com> - 0.66-1
- fix incorrect usage of sched_setscheduler in check_privs()

* Mon Feb  8 2010 Clark Williams <williams@redhat.com> - 0.65-1
- add workaround to hwlatdetect for incorrect initializer in
  smi_detector.ko

* Fri Jan 29 2010 Clark Williams <williams@redhat.com> - 0.64-1
- from John Kacur <jkacur@redhat.com>
  - automatic dependency generation
  - style cleanups
  - libnuma code cleanups
  - add copyright to rt_numa.h

* Wed Jan 27 2010 Clark Williams <williams@redhat.com> - 0.63-1
- added support for libnuma V1 API

* Tue Jan 26 2010 Clark Williams <williams@redhat.com> - 0.62-1
- added NUMA option
- patch from Uwe Kleine-König <u.kleine-koenig@pengutronix.de>
  to clarify source copyrights
- moved hwlatdetect to python site-library

* Wed Jan 13 2010 Clark Williams <williams@redhat.com> - 0.61-1
- added --smp/-S option to setup for basic SMP testing
- added warn() and fatal() utility functions

* Tue Dec 29 2009 Clark Williams <williams@redhat.com> - 0.60-1
- John Kacur <jkacur@redhat.com>:
  - added pip test (process based priority inheritance)
  - refactored some error routines into the common library
  - added 'make tags' option to Makefile
- Michael Olbrich <m.olbrich@pengutronix.de> added an unbuffered
  output option to cyclictest (-u/--unbuffered)

* Mon Dec 21 2009 Clark Williams <williams@redhat.com> - 0.59-1
- deleted classic_pi
- David Sommerseth <davids@redhat.com>:
  - added help text for -M (refresh-on-max) option for cyclictest
  - fixed parsing of --mlockall in signaltest
- Carsten Emde <C.Emde@osadl.org> provided a better explaination
  for using the kernel module with the backfire program
- John Kacur <jkacur@redhat.com> cleaned up the trailing comments
  on the guard macros in src/lib/rt-utils.h

* Mon Dec 21 2009 Clark Williams <williams@redhat.com> - 0.58-1
- merged jkacur's portable getcpu() code
- fixed inadvertent conversion of some source to DOS text files

* Mon Dec 14 2009 Clark Williams <williams@redhat.com> - 0.57-1
- John Kacur <jkacur@redhat.com> folded in Carsten Emde's tests
    - ptsematest
    - sigwaittest
    - svsematest
    - sendme
- Carsten Emde <carsten.emde@osadl.org> created a utility library
  moving functions from cyclictest into src/lib/rt-utils.c
- Makefile cleanups from jkacur

* Thu Dec 10 2009 Clark Williams <williams@redhat.com> - 0.56-1
- cyclictest: added code to print break thread id with -b

* Thu Nov 19 2009 Clark Williams <williams@redhat.com> - 0.55-1
- pi_stress: cosmetic newline added
- fixes from John Kacur <jkacur@redhat.com>
  - pi_stress: Remove racy state variables that cause watchdog to trigger
  - pi_stress: Check whether quiet is set, before taking shutdown_mtx
  - pi_stress: Use a pthread_mutex_t for the global variable shutdown

* Tue Nov 17 2009 Clark Williams <williams@redhat.com> - 0.54-1
- patches from John Kacur <jkacur@redhat.com>
  - fix source style issues in pi_stress
  - add a DEBUG option to the Makefile
  - use CFLAGS for C compiler options
  - label targets as PHONY if not generating actual file
- patch to remove rt-tests.spec from .PHONY in Makefile

* Mon Nov 16 2009 Clark Williams <williams@redhat.com> - 0.53-2
- added back missing dist tag for release

* Tue Oct  6 2009 Clark Williams <williams@redhat.com> - 0.53-1
- fixed incorrect format string in hwlatdetect.py
- added docs/release-checklist.txt

* Mon Sep 21 2009 Clark Williams <williams@redhat.com> - 0.52-1
- fixes and cleanups to pi_stress from jkacur
- added rostedt's rt-migrate-test

* Thu Sep  3 2009 Clark Williams <williams@redhat.com> - 0.51-1
- two manpage fixes from Uwe Kleine-König <u.kleine-koenig@pengutronix.de>
- added -M option from Arnaldo Carvahlo de Melo <acme@redhat.com>
  (for use on low-bandwidth connections, defer's update until new max hit)

* Fri Jul 24 2009 Clark Williams <williams@redhat.com> - 0.50-2
- minor patch to fix reporting option of hwlatdetect

* Thu Jul 16 2009 Clark Williams <williams@redhat.com> - 0.50-1
- patch to cyclictest from Sebastian Andrzej Siewior <bigeasy@linutronix.de>
  to process options before checking for root user
- patch to cyclictest from Sebastian Andrzej Siewior <bigeasy@linutronix.de>
  to exit with proper error code on exit
- added scripts/do-git-push script
- added push target to Makefile
- rewrite of hwlatdetect script to handle old smi_detector module

* Sun Jul  5 2009 Clark Williams <williams@redhat.com> - 0.47-1
- patch from GeunSik Lim <leemgs1@gmail.com> to reorder options for readability
- patch from GeunSik Lim <leemgs1@gmail.com> to add --policy option
- patch from GeunSik Lim <leemgs1@gmail.com> to clarify -h option usage
- modified --policy to take scheduler policy name instead of integers

* Thu Jul  2 2009 Clark Williams <williams@redhat.com> - 0.46-1
- added fix from Daniel Gollub <dgollub@suse.de> (doomsday latency)

* Thu Jul  2 2009 Clark Williams <williams@redhat.com> - 0.45-1
- bugfix from Daniel Gollub <dgollub@suse.de> (fix cyclictest segfault)
- cyclictest format change from Sven-Thorsten Dietrich <sdietrich@suse.de>
- added help target to Makefile

* Tue Jun 30 2009 Clark Williams <williams@redhat.com> - 0.44-1
- fix to specfile (renamed smidetect to hwlatdetect)
- added code to hwlatdetect allow setting window and width properly

* Thu Jun 25 2009 Clark Williams <williams@redhat.com> - 0.43-1
- manpage fixes from Uwe Kleine-Konig <u.kleine-koenig@pengutronix.de>

* Fri Jun 12 2009 Clark Williams <williams@redhat.com> - 0.42-1
- renamed smidetect -> hwlatdetect

* Thu May 28 2009 Clark Williams <williams@redhat.com> - 0.41-1
- added Stefan Agner's patch to fix calculating time difference
  when delta is bigger than 2147 seconds

* Wed May 13 2009 Clark Williams <williams@redhat.com> - 0.40-1
- added smidetect

* Thu Jan 03 2008 Clark Williams <williams@redhat.com> - 0.18-1
- Initial build.
