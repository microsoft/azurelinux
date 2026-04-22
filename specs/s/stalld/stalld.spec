# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		stalld
Version:	1.26.3
Release: 2%{?dist}
Summary:	Daemon that finds starving tasks and gives them a temporary boost

License:	GPL-2.0-or-later AND GPL-2.0-only
URL:		https://gitlab.com/rt-linux-tools/%{name}/%{name}.git
Source0:	https://gitlab.com/rt-linux-tools/%{name}/-/archive/v%{version}/%{name}-%{version}.tar.bz2

BuildRequires:	glibc-devel
BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	systemd-rpm-macros

Requires:	systemd

%ifnarch i686
BuildRequires:	bpftool
BuildRequires:	clang
BuildRequires:	llvm
BuildRequires:	libbpf-devel

Requires:	libbpf
%endif

%define _hardened_build 1

%description
The stalld program monitors the set of system threads,
looking for threads that are ready-to-run but have not
been given processor time for some threshold period.
When a starving thread is found, it is given a temporary
boost using the SCHED_DEADLINE policy. The default is to
allow 10 microseconds of runtime for 1 second of clock time.

%prep
%autosetup -p1

%build
%make_build CFLAGS="%{optflags} %{build_cflags} -DVERSION="\\\"%{version}\\\"""  LDFLAGS="%{build_ldflags}"

%install
%make_install DOCDIR=%{_docdir} MANDIR=%{_mandir} BINDIR=%{_bindir} DATADIR=%{_datadir} VERSION=%{version}
%make_install -C systemd UNITDIR=%{_unitdir}

%files
%{_bindir}/%{name}
%{_bindir}/throttlectl
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/sysconfig/stalld
%doc %{_docdir}/README.md
%doc %{_mandir}/man8/stalld.8*
%license gpl-2.0.txt

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%changelog
* Thu Jan 15 2026 Clark Williams <williams@redhat.com> - 1.26.3-1
- tests: Add pre-test and post-test cleanup of stalld processes
- Makefile: version bump to v1.26.3
- Makefile: Remove unnecessary -m64 compiler flag
- Makefile: version bump to v1.26.2
- Makefile: Remove LTO flags from build options
- Makefile: switch to using gzip for tarball compression
- Makefile: version bump to v1.26.1
- Makefile: Add support for riscv64
- Fix typo: rename 'merge_taks_info' to 'merge_tasks_info'
- gitignore: Exclude Serena and Claude Code metadata
- Makefile: Print BPF tool versions for debugging
- Makefile: Remove redundant GCC version check
- Makefile: Explicitly run the 'test' target in the tests directory
- Makefile: Improve compiler flag detection for -fcf-protection
- Makefile: Conditionally add -mno-omit-leaf-frame-pointer

* Fri Nov 07 2025 Clark Williams <williams@redhat.com> - 1.25.1-1
- docs: add CLAUDE.md, .claude agents, and update .gitignore
- tests: Add comprehensive test suite with infrastructure and functional tests
- tests: Add Phase 2 command-line option tests (8 new tests)
- docs: Add project rules and agent usage guidelines
- docs: Update context snapshot with Phase 2 completion
- tests: Add Phase 3.1 core logic tests (starvation detection and parsing)
- tests: Add Phase 3.2 boosting mechanism tests (DEADLINE, FIFO, restoration)
- tests: Add Phase 3.3 task merging and idle detection tests - Phase 3 COMPLETE
- tests: Add RT throttling save/restore helpers
- tests: Automatically save and restore RT throttling state
- tests: Fix test_task_merging empty variable errors and add DL-server check
- tests: Add DL-server save/disable/restore support
- docs: Update TODO.md with DL-server management and recent improvements
- docs: Update context snapshot with Phase 3 completion and state management
- tests: Add legacy test integration and backend selection support
- test01: add ability to specify backend
- tests: remove binary accidentally committed
- tests: Fix cleanup EXIT trap to preserve test exit codes
- tests: Fix test_log_only.sh timing and starvation reliability
- tests: Add backend selection support to individual tests
- saved claude context snapshot and moved CLAUDE.md to .claude dir
- .claude: Add context-snapshot.json and update CLAUDE.md
- tests: Fix starvation_gen to create actual RT starvation
- tests: Fix test_starvation_detection.sh to respect backend selection
- tests: Fix test_starvation_detection.sh timing and idle detection issues
- tests: Fix EPERM errors in cleanup by improving process termination handling
- docs: Update CLAUDE.md with backend selection and debugfs/procfs clarification
- tests: Fix infinite hang in test_starvation_detection.sh Test 5
- tests: Rewrite test_cpu_selection.sh to use modern test framework
- tests: Rewrite test_boost_period.sh to fix hanging issues
- tests: Fix PID tracking and backgrounding issues in test suite
- tests: Rewrite test_starvation_threshold.sh to fix undefined variables
- tests: Fix test_starvation_threshold.sh log file collision issue
- tests: Update TODO.md with 2025-10-09 progress and old-style test issues
- tests: Update context snapshot for 2025-10-09 test framework hardening session
- tests: Rewrite all remaining old-style Phase 2 tests using modern framework
- tests: Fix EPERM errors in test cleanup by replacing wait with polling
- tests: Fix Phase 1 test issues (affinity, backend_selection, fifo_boosting)
- tests: Add -N flag to disable idle detection in starvation/FIFO tests
- tests: Fix argument ordering in backend selection tests
- tests: Fix hanging issues in test_boost_duration.sh
- tests: Fix test_boost_runtime.sh hanging and improve reliability
- save LLM context
- add helpers for git-scm-master AI agent
- tests: Fix output redirection issues in test_affinity.sh
- test: Fix test_pidfile.sh output handling and CLI options
- tests: Fix test_boost_period.sh helper integration and reliability
- test: Fix test_boost_restoration.sh for stability and standard infrastructure
- docs: Document mass test suite fixes session with 7 tests and 4 critical discoveries
- tests: Fix grep pattern in test_starvation_threshold.sh for actual log format
- docs: Update context snapshot for queue_track backend test fixes
- tests: Implement matrix testing for backends and threading modes
- docs: Update CLAUDE.md with correct threading mode flags and matrix testing
- context: Document matrix testing infrastructure implementation
- tests: Add timeout protection to test01_wrapper.sh
- Document queue_track backend limitation in test_starvation_threshold.sh
- docs: Update documentation with segfault fix and queue_track limitation
- tests: Add FIFO-on-FIFO priority starvation test
- tests: Enhance starvation_gen and fix test infrastructure
- .claude: Update context snapshot
- .claude: Update context snapshot - BPF RT task tracking fix completed
- tests: Change starvation_gen default work_target to 1
- .claude: Update context snapshot - 14/16 tests passing with queue_track
- tests: Improve starvation_gen thread coordination and shutdown
- .claude: Update context snapshot - starvation_gen improvements and test progress
- tests: Add --test option to run individual tests by name
- .claude: Update context snapshot - test infrastructure improvements complete
- tests: Fix test_boost_restoration to properly test SCHED_FIFO restoration
- tests: Add SCHED_OTHER option to starvation_gen
- tests: Update test_boost_restoration Test 3 to use SCHED_OTHER
- context snapshot
- tests: Add kworker denylist to test_boost_restoration
- tests: Fix Test 5 timing and parameter validation
- tests: Add journal logging for test activity correlation
- context snapshot
- tests: Increase test01 timeout and document kworker competition
- context snapshot
- tests: Add unified test environment management framework
- context snapshot
- tests: Fix timing race conditions in starvation detection tests
- docs: Update TODO.md with test suite timing race condition fixes
- docs: Add context snapshot for test suite timing race fixes
- tests: Fix timing race conditions in starvation detection tests
- tests: Fix timing race conditions in test_deadline_boosting
- tests: Fix timing race conditions in 4 remaining functional tests
- tests: Fix output buffering and kernel worker interference
- tests: Fix output buffering in test_starvation_detection Test 3
- docs: Context snapshot for Nov 3 evening session - timing fixes and buffering issues
- tests: Fix test_starvation_detection Test 3 flawed counting logic
- tests: Consolidate duplicate helper functions (Part 1 complete)
- context snapshot
- bpf: Add BPF CO-RE compatibility for older kernels
- Makefile: Make BPF compilation verbose
- Makefile: Append -std=c99 to CFLAGS
- doc: update Releases.md for repository instructions
- tests: Fix start_stalld() PID detection for daemon and slow architectures
- doc: Release notes for v1.25.1 release
- Makefile: version bump to v1.25.1

* Fri Oct 24 2025 Clark Williams <williams@redhat.com> - 1.24.1-1
- sched_debug: Unify parsing methods for task_info
- sched_debug: Fix runqueue task parsing logic and state filtering
- sched_debug: Fix double-free crash in fill_waiting_task()
- stalld.c: remove noisy idle report and added report to should_skip_idle_cpus()
- stalld.c: initialize cpu_info->idle_time to be -1
- stalld.c: get rid of misleading print about DL-Server
- stalld.c: Add starvation logging in single-threaded log-only mode
- stalld: Add -N/--no_idle_detect flag to disable idle detection
- stalld: Add defensive checks in print_boosted_info
- Makefile: Add support for legacy kernels
- scripts: fix run-local if bashism
- sched_debug: Fix segfault in adaptive/aggressive modes
- Makefile: Remove redhat-specific checks
- Makefile: Add a help target
- Makefile: Check compatible compiler versions
- stalld.c: Ensure queue_track backend is not referenced when USE_BPF=0
- Makefile: version bump to v1.24.1
	      
* Tue Sep 30 2025 Clark Williams <williams@redhat.com> - 1.23.1-1
- stalld:  make the queue_track (eBPF) backend the default
- Makefile: version bump to v1.23.1

* Tue Sep 30 2025 Clark Williams <williams@redhat.com> - 1.22.1-1
- bpf: Reduce arguments to log() to fix verifier error
- stalld: Always reset starving vector in merge_taks_info
- stalld: Remove forced log-only mode with DL-server
- Makefile: version bump to v1.22.1

* Fri Sep 12 2025 Clark Williams <williams@redhat.com> - 1.21.1-1
- refactor: Remove unused 'exiting' variable
- bpf: Introduce task_is_rt() helper
- bpf: Correctly update nr_rt_running on sched_switch
- Simplify __die() function to use abort()
- Refactor: Use path length macros in check_dl_server_dir_exists
- Refactor: Remove duplicated find_debugfs function
- utils: Remove unused find_mount() function
- bpf: Reorder functions to prepare for future changes
- bpf: Pass stalld_cpu_data pointer to queuing functions
- bpf: Make update_or_add_task() return void
- bpf: Reuse enqueue_task() in update_or_add_task()
- bpf: Use tracepoints to avoid fentry startup stall
- bpf: Centralize monitoring check in get_cpu_data()
- bpf: Remove unused 'task' variable
- bpf: Use task_cpu() to get the correct CPU data
- bpf: Handle wakeup of new tasks with sched_wakeup_new
- daemon: Refactor cleanup logic into a helper function
- daemon: Clean up stale tasks during the boost phase
- bpf: Document and enhance dequeue_task return value
- bpf: Handle task migrations with sched_migrate_task
- bpf: a task is dequeued just by setting its pid to 0
- bpf: Improve logging in stalld.bpf.c
- bpf: Use BPF CO-RE for task CPU field access
- bpf: Add const qualifier to task_struct pointers
- bpf: Add task iterator for initial state snapshot
- bpf: Simplify task queue management by removing redundant rt parameter
- bpf: Add cpu to log_task_prefix
- stalld: Refactor tgid_field handling to use sizeof
- refactor: Move helper functions to utils.c
- stalld: Simplify get_cpu_idle_time() function using sscanf
- refactor: Simplify update_cpu_starving_vector()
- refactor: Remove unused headers from stalld.c
- stalld: Extract repeated buffer reallocation pattern
- stalld: Flatten nested conditionals using early returns
- refactor: Extract common idle detection pattern into helper function
- refactor: Standardize memory allocation with calloc-compatible helper
- bpf: Use CO-RE to check for running tasks
- systemd:  change systemd service startup to use RuntimeDirectory
- Makefile: version bump to v1.21.1

* Mon Aug 18 2025 Clark Williams <williams@redhat.com> - 1.20.4-1
- Makefile: version bump to v1.20.4
- stalld.service: Fix duplicate ExecStart in service files

* Tue Aug 12 2025 Clark Williams <williams@redhat.com> - 1.20.3-1
- Makefile: bump version to v1.20.3
- stalld.service: Fix failure to set FIFO scheduling class

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 17 2025 Clark Williams <williams@redhat.com> - 1.21.2-1
- Makefile: bump version to v1.20.1
- bpf: Improve task tracking in sched_switch
- bpf/stalld: Introduce compute_ctxswc helper and update ctxswc on sched_switch

* Wed Jul 16 2025 Clark Williams <williams@redhat.com> - 1.21.1-1
- Makefile:  update version to 1.20.1
- scripts:  add a script for running a local build for debuggin
- stalld: Automatically switch to log-only mode if DL-server present
- bpf/stalld: Implement and use find_queued_task helper in dequeue_task
- bpf/stalld: Introduce and use for_each_task_entry/for_each_queued_task macros
- build/debug: Control optimization and debug levels via DEBUG variable
- stalld: sched_attr: Do not define for glibc >= 2.41
- stalld: Refactor verbose logging with dedicated macros
- stalld/queue_track: Consolidate print_queued_tasks verbosity control
- gitignore: Add common build and tag files
- build/debug: Allow DEBUG_STALLD to be controlled by 'DEBUG' Makefile variable
- build/bpf/stalld: Pave way for DEBUG_STALLD command-line override
- bpf/stalld: Introduce generic 'log' macro for BPF debug prints
- bpf/stalld: Unify and generalize debug macro to DEBUG_STALLD

* Thu May 22 2025 John Kacur <jkacur@redhat.com> - 1.19.8-3
- Add patch to conditionally use glibc sched attar if available

* Wed Feb 19 2025 Clark Williams <williams@redhat.com> - 1.19.8-2
- sync up with other builds

* Wed Feb 19 2025 Clark Williams <williams@redhat.com> - 1.19.8
- Fix incorrect DAEMON_UMASK value
- Add 'errexit' to throttlectl.sh
- Added glibc41 fix to source tree, removed patch
- stalld.h:  fix prototype mis-match with cleanup_regex()

* Tue Jan 21 2025 Clark Williams <williams@redhat.com> - 1.19.7
- stalld.c: use a more reasonable size for reading /proc/stat
- systemd/Makefile:  remove typo in uninstall line
- Makefile:  change modes on throttled and stalld
- throttlectl: clean up throttling script due to reported CVE-2024-54159

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 31 2024 Clark Williams <williams@redhat.com> - 1.19.6
- systemd: add BE environment variable to select backend
- Makefile: add uninstall target
- version bump to 1.19.6

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jul 12 2024 Clark Williams <williams@redhat.com> - 1.19.5
- Makefile:  refactor CFLAGS/LDFLAGS for local and koji builds
- doc/Releases.md:  Add a note about tagging

* Thu Jul 11 2024 Clark Williams <williams@redhat.com> - 1.19.4-2
- stalld.spec: pass USE_BPF=1 in CFLAGS

* Thu Jul 11 2024 Clark Williams <williams@redhat.com> - 1.19.4
- Makefile: refactor options to pass annocheck

* Wed Jun  5 2024 Clark Williams <williams@redhat.com> - 1.19.3-2
- systemd: ensure that pidfile directory exists

* Thu May 16 2024 Clark Williams <williams@redhat.com> - 1.19.3
- src/utils.c: fix off-by-one error in buffer allocation
- Makefile:  change build to use FORTIFY_SOURCE=3

* Wed Apr 24 2024 Clark Williams <williams@redhat.com> - 1.19.2
- Make fill_process_comm() open comm file as READ_ONLY
- throttlectl.sh: use legal value for exit on fail
- stalld: free malloc'd buffer on function exit
- throttling.c:  null terminate input buffer
- stalld.conf: Fix stalld service start fail
- Conditionalize BPF and queue_track build per architecture
- clean up Makefile install logic and add .bz2 to .gitignore
- modify Makefiles so install works with relative paths
- rename 'redhat' to 'systemd' and remove redhat packaging logic
- update SPDX tags to non-deprecated values
- stalld: Add -a/--affinity option
- Adding SPDX license info to each file
- man/stalld.8:  change starving threshold to match code
- utils: Fix freeing of invalid pointer
- add bpftool as BuildRequires

* Mon Dec 25 2023 Clark Williams <williams@redhat.com> - 1.18.1
- queue_track: Use LIBBPF_MAJOR/MINOR_VERSION to detect deprecated functions
- utils: Close file descriptor
- stalld: Fix function name of daemonize()
- docs: Fix typo in the manual
- queue_track: Use bpf_map__resize on older libbpf versions
- utils: Let tgid to arrive at the fill proccess comm
- stalld: Fix log message on idle detection
- stalld: Add -b/--backend option
- stalld: Add queue track eBPF based backend
- stalld: Add fill_process_comm helper
- stalld: Include regex.h on stalld.h
- stalld: Get nr of cpus only once
- stalld: Add the backend abstraction
- sched_debug: Move sched debug functions to an specific file

* Thu Dec 21 2023 Clark Williams <williams@redhat.com> - 1.17.1
- stalld: Fix memory leak in print_boosted_info()
- utils: Check if the system is in lockdown mode
- stalld: print process comm and cpu when boosting
- stalld: Detect runnable dying tasks
- stalld: Fix nr_periods calculation in do_fifo_boost()
- stalld.conf: Lower threshold to 20
- utils.c: Exit early if enabling HRTICK fails when using SCHED_DEADLINE
- Add support for loongarch

* Mon Dec 18 2023 Clark Williams <williams@redhat.com> - 1.16.7
- fix to sync versions

* Mon Dec 18 2023 Clark Williams <williams@redhat.com> - 1.16.6
- remove un-needed BuildRequire for bpftool

* Mon Dec 18 2023 Clark Williams <williams@redhat.com> - 1.16.5
- changed package license to match SPDX values

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Mar 31 2022 Fernando Pacheco <fpacheco@redhat.com> - 1.16-1
- stald/utils: Space, lines and voids clenaups
- stalld: Add an option to easily set stalld as SCHED_DEADLINE
- stalld: Comments cleanup
- src/utils: Comments cleanup
- src/throttling: Comments cleanup
- src/stalld.h Comments cleanup

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 15 2021 Fernando Pacheco <fpacheco@redhat.com> - 1.15-1
- stalld: Fix incorrect open() return value checks
- stalld: Pass errno to strerror() on sig*set() failures
- throttling: Always null terminate sched_rt_runtime_us output
- stalld: Remove unreachable statement in detect_task_format()
- tests: Fix uninitialized value action.sa_mask
- utils: Bail if malloc() returns null in parse_cpu_list()
- stalld: Use correct format specifier for long types

* Mon Jul 19 2021 Fernando Pacheco <fpacheco@redhat.com> - 1.14.1-1
- stalld: Coding style cleanup
- stalld: spaces in place of <TAB>
- throttling: Use RT_RUNTIME_PATH in rt_throttling_is_off()
- throttling: Check open() on turn_off_rt_throttling
- throttling: Adjust variables in restore_rt_throttling()
- stalld.c: utils.c: Remove complex assignments from variable declarations
- stalld.h: Define MAX_PATH/DIR_PATH/FILE_NAME and use them
- stalld: Adjust variables in parse_old_task_format()
- utils.c: Use MAX_PATH for pidfile
- stalld.c: Remove variable declaration from the middle of  the function
- stalld: Respect -l option in single threaded mode
- utils: s/try_to_open_file/check_file_exists/
- utils: use check_file_exists in setup_hr_tick()
- utils: Check for the new sched_features path

* Fri Jul 02 2021 Fernando Pacheco <fpacheco@redhat.com> - 1.13-1
- stalld: Fix log message on boost_cpu_starving_vector()
- stalld: Add the overload control to the single-threaded mode
- stalld: Add the adaptive mode option
- stalld: Use the last mode set in the cmdline
- stalld: Fallback to the adaptive mode if force_fifo is selected
- stalld: Make single-threaded mode the default one
- stalld.service: Always restart stalld on exit
- utils.c: Fail if user is not root
- utils.c: Make the path to sched_debug path dynamic

* Tue Jun 29 2021 Fernando Pacheco <fpacheco@redhat.com> - 1.12-1
- stalld.8: fix diff cruft left in manpage source
- stalld.c: clean up handling of nr_running
- stalld.c: remove duplicate parameter to fill_waiting_task()
- stalld: Add error handling in get_cpu_idle_time()
- stalld.service: Run stalld as sched_fifo via systemd
- packaging: clean up Makefiles and rpm specfile
- stalld: Always print current function for info messages
- stalld: Always print current function for warn messages
- stalld: Always print current function for die messages
- utils: change PATHMAX to 4096

* Thu May 13 2021 Clark Williams <williams@redhat.com> - 1.11-1
- redhat/stalld.spec: pick up gating test version for changelog
- utils.c: set daemon umask to restrict global write/execute (1934586)
- hardening fixes from coverity scan (1934590)

* Tue Apr 27 2021 Clark Williams <williams@redhat.com> - 1.10-1
- utils: Fix bounds check on cpu and end_cpu variables
- stalld: Support denylisting of tasks in stalld
- src/utils: use right argument for warning printf

* Wed Feb 17 2021 Clark Williams <williams@redhat.com> - 1.9-2
- update to pick up latest gating test

* Wed Feb 17 2021 Clark Williams <williams@redhat.com> - 1.9-1
- Set starvation threshold default to 30 seconds
- rework read buffer allocation to properly find page size
- Add the -g/--granularity option
- Change the default granularity to five seconds
- Implement idle detection
- Implement the single-threaded mode
- Add HRTICK_DL support

* Fri Feb  5 2021 Clark Williams <williams@redhat.com> - 1.8-1
- Fix Readiness Protocol Mismatch with systemd
- test01:  update to use buildin atomic operations
- test01: add throttling check

* Tue Feb  2 2021 Clark Williams <williams@redhat.com> - 1.7-1
- rework detect_task_format and buffer_size logic
- make CFLAGS for local compile match rpmbuild CFLAGS

* Tue Jan 26 2021 Clark Williams <williams@redhat.com> - 1.6-1
- add systemd handling of RT Throttling

* Wed Jan 20 2021 Clark Williams <williams@redhat.com> - 1.5-1
- fix signal handler to catch SIGTERM

* Fri Dec 11 2020 Clark Williams <williams@redhat.com> - 1.4-1
- stalld: Set rt_runtime to -1 before trying the SCHED_DEADLINE
- Fix incorrect recursion of specfile version field

* Fri Nov 20 2020 Clark Williams <williams@redhat.com> - 1.3-1
- Readme: Add information about repositories
- Add version management and version option
- create doc and scripts directory and add info on releases

* Mon Nov  2 2020 Clark Williams <williams@redhat.com> - 1.2-1
- utils.c: added info() functions
- detect and correctly parse old-style /proc/sched_debug
- src/stalld: Fix an retval check while reading sched_debug
- src/throttling: Fix a compilation warning
- ensure we only count task lines in old-format sched_debug info
- Add comments, clean up trailing whitespace
- src/utils: Fix runtime parameters check
- stalld: Do not take actions if log_only is set
- remove warning from parse_old_task_format

* Tue Oct 27 2020 Clark Williams <williams@redhat.com> - 1.1-1
- Fix an option in README.md; consistency in user facing docs.
- Makefile: add 'static' target to link stalld statically
- gitignore: ignore object files and the stalld executable
- use FIFO for boosting (v3)
- stalld.c: fix sched_debug parsing and modify waiting task parsing
- redhat:  update release for features and bugfix
- stalld: Do not die if sched_debug returns an invalid value
- src/stalld: Do not die if the comm is too large
- src/stalld: Do not die if cannot write a message to the log
- src/stalld: Do not die if the main runs while a thread is monitoring the CPU
- implement RT throttling management and refactor source files
- more refactoring
- src/stalld: Reuse already read nr_running nr_rt_running
- src/stalld: Gracefully handle CPUs not found on sched_debug
- src/stalld: Use dynamically allocated memory to read sched_debug
- src/utils: Die with a divizion by zero if verbose
- src/stalld: Add config_buffer_size variable
- src/stalld: Increase the sched_debug read buffer if it gets too small
- src/stalld: Fix an retval check while reading sched_debug
- src/throttling: Fix a compilation warning

* Sun Oct  4 2020 Clark Williams <williams@redhat.com> - 1.0-4
- Fix an option in README.md; consistency in user facing docs.
- gitignore: ignore object files and the stalld executable
- Makefile: add 'static' target to link stalld statically
- use FIFO for boosting (v3)
- stalld: update usage message to include --force_fifo/-F option
- stalld.c: fix sched_debug parsing and modify waiting task parsing

* Tue Sep  1 2020 Clark Williams <williams@redhat.com> - 1.0-3
- Place BuildRequires on individual lines
- Fix changelog notations
- Modify build command to pass in CFLAGS and LDFLAGS
- fix compiler warnings in stalld.c

* Mon Aug 31 2020 Clark Williams <williams@redhat.com> - 1.0-2
- use _docdir macro for README.md
- use _mandir macro for stalld.8 manpage
- use tabs for spacing
- added push Makefile target to copy latest to upstream URL

* Tue Aug 25 2020 Clark Williams <williams@redhat.com> - 1.0-1
- rename project to stalld
- set version to 1.0
- clean up rpmlint complaints

* Fri Aug 21 2020 Clark Williams <williams@redhat.com> - 0.2-1
- add pidfile logic

* Thu Aug 20 2020 Clark Williams <williams@redhat.com> - 0.1-1
- Added systemd service to redhat subdirectory
- added make and rpm logic for systemd files

* Wed Aug 19 2020 Clark Williams <williams@redhat.com> - 0.0-1
- initial version of specfile
- Makefile mods for RPM builds
- added systemd service and config files
