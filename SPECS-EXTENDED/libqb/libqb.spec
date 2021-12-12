Vendor:         Microsoft Corporation
Distribution:   Mariner
%bcond_without check

Name:           libqb
Version:        1.0.5
Release:        7%{?dist}
Summary:        Library providing high performance logging, tracing, ipc, and poll

License:        LGPLv2+
URL:            https://github.com/ClusterLabs/libqb
Source0:        https://github.com/ClusterLabs/libqb/releases/download/v%{version}/%{name}-%{version}.tar.xz
Patch0:         IPC-avoid-temporary-channel-priority-loss.patch
# https://github.com/ClusterLabs/libqb/pull/383
Patch1:         libqb-fix-list-handling-gcc10.patch
Patch2:         libqb-fix-list-handling-gcc10-2.patch

BuildRequires:  autoconf automake libtool
BuildRequires:  check-devel
BuildRequires:  doxygen
BuildRequires:  gcc
BuildRequires:  procps
# for ipc.test only (part of check scriptlet)
BuildRequires:  pkgconfig(glib-2.0)
# git-style patch application
BuildRequires:  git-core

%description
libqb provides high-performance, reusable features for client-server
architecture, such as logging, tracing, inter-process communication (IPC),
and polling.

%prep
%autosetup -p1 -S git_am  # for when patches around

%build
./autogen.sh
%configure --disable-static
%{make_build}

%if 0%{?with_check}
%check
make check V=1 \
  && make -C tests/functional/log_internal check V=1
%endif

%install
%{make_install}
find $RPM_BUILD_ROOT -name '*.la' -delete
rm -rf $RPM_BUILD_ROOT/%{_docdir}/*

%ldconfig_scriptlets

%files
%license COPYING
%{_sbindir}/qb-blackbox
%{_libdir}/libqb.so.*
%{_mandir}/man8/qb-blackbox.8*

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%files          devel
%doc README.markdown
%{_includedir}/qb/
%{_libdir}/libqb.so
%{_libdir}/pkgconfig/libqb.pc
%{_mandir}/man3/qb*3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.5-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Apr 23 2020 Christine Caulfield <ccaulfie@redhat.com> 1.0.5-6
- Further fix for qblist when compiling on gcc10
  Affects users of the package rather than libqb itself

* Mon Apr  6 2020 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.5-5
- Upstream fix for test failures (fix FTBFS)
- spec cleanups

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 12 2019 Jan Pokorný <jpokorny+rpm-libqb@redhat.com> - 1.0.5-2
- Fix temporary channel priority loss, up to deadlock-worth
  (upstream patchset https://github.com/ClusterLabs/libqb/pull/354)

* Fri Apr 26 2019 Jan Pokorný <jpokorny+rpm-libqb@redhat.com> - 1.0.5-1
- Update to libqb-1.0.5, for list of changes see:
  https://github.com/ClusterLabs/libqb/releases/tag/v1.0.4
  https://github.com/ClusterLabs/libqb/releases/tag/v1.0.5
  (note that 1.0.4 is botched from pacemaker/corosync cluster stack
  perspective so that is intentionally skipped)
- Includes an important fix for a security issue (CVE-2019-12779,
  https://github.com/ClusterLabs/libqb/issues/338)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 07 2018 Adam Williamson <awilliam@redhat.com> - 1.0.3-4
- Rebuild to fix GCC 8 mis-compilation
  See https://da.gd/YJVwk ("GCC 8 ABI change on x86_64")

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.3-3
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Dec 21 2017 Jan Pokorný <jpokorny+rpm-libqb@redhat.com> - 1.0.3-1
- Update to libqb-1.0.3, for list of changes see:
  https://github.com/ClusterLabs/libqb/releases/tag/v1.0.3

* Tue Dec 12 2017 Jan Pokorný <jpokorny+rpm-libqb@redhat.com> - 1.0.2-15
- Evolution of the previous (rhbz#1478089)

* Wed Nov 15 2017 Jan Pokorný <jpokorny+rpm-libqb@redhat.com> - 1.0.2-14
- Evolution of the previous (rhbz#1478089)
- Make -devel package dependency on the main package arch-qualified

* Tue Oct 31 2017 Jan Pokorný <jpokorny+rpm-libqb@redhat.com> - 1.0.2-13
- Evolution of the previous (rhbz#1478089)

* Wed Oct 25 2017 Jan Pokorný <jpokorny+rpm-libqb@redhat.com> - 1.0.2-12
- Evolution of the previous (rhbz#1478089)

* Wed Oct 18 2017 Jan Pokorný <jpokorny+rpm-libqb@redhat.com> - 1.0.2-11
- Evolution of the previous (rhbz#1478089)

* Fri Oct 13 2017 Jan Pokorný <jpokorny+rpm-libqb@redhat.com> - 1.0.2-10
- Evolution of the previous (rhbz#1478089)

* Mon Oct 09 2017 Jan Pokorný <jpokorny+rpm-libqb@redhat.com> - 1.0.2-9
- Evolution of the previous (rhbz#1478089)

* Fri Oct 06 2017 Jan Pokorný <jpokorny+rpm-libqb@redhat.com> - 1.0.2-8
- Evolution of the previous (rhbz#1478089)
- New test included in check phase (as per upsteam)

* Mon Sep 04 2017 Jan Pokorný <jpokorny+rpm-libqb@redhat.com> - 1.0.2-7
- Evolution of the previous (rhbz#1478089)

* Fri Sep 01 2017 Jan Pokorný <jpokorny+rpm-libqb@redhat.com> - 1.0.2-6
- Better approach so as to mitigate changed treatment of orphaned sections
  in ld.bfd/binutils-2.29, resulting in logging facility silently out of order
  (rhbz#1478089)
- Related to that, build commands now shown in full to ease the sanity checking
- Adapt spec file per the upstream version (conditionalizing build through
  --enable-syslog-tests no longer relevant since v1.0.2)

* Fri Aug 11 2017 Kalev Lember <klember@redhat.com> - 1.0.2-5
- Bump and rebuild for an rpm signing issue

* Thu Aug 10 2017 Jan Pokorný <jpokorny+rpm-libqb@redhat.com> - 1.0.2-4
- Mitigate changed treatment of orphaned sections in ld.bfd/binutils-2.29,
  resulting in logging facility silently out of order (rhbz#1478089)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri May 19 2017 Jan Pokorný <jpokorny+rpm-libqb@redhat.com> - 1.0.2-1
- Update to libqb-1.0.2, for list of changes see:
  https://github.com/ClusterLabs/libqb/releases/tag/v1.0.2

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov 25 2016 Jan Pokorný <jpokorny+rpm-libqb@redhat.com> - 1.0.1-1
- Update to libqb-1.0.1, for list of changes see:
  https://github.com/ClusterLabs/libqb/releases/tag/v1.0.1
- Move qb-blackbox manual page from libqb-devel to libqb
  (where the utility itself resides)

* Mon Apr 4 2016 Jan Pokorný <jpokorny+rpm-libqb@redhat.com> - 1.0-1
- Update to libqb-1.0, for list of changes see, in order:
  https://github.com/ClusterLabs/libqb/releases/tag/v1.0rc1
  https://github.com/ClusterLabs/libqb/releases/tag/v1.0rc2
  https://github.com/ClusterLabs/libqb/releases/tag/v1.0rc3
  https://github.com/ClusterLabs/libqb/releases/tag/v1.0rc4
  https://github.com/ClusterLabs/libqb/releases/tag/v1.0
- Adapt spec file per the upstream version (drop defattr statements,
  autogen.sh call with %%build, conditionalize build process)
- Add gcc as an explicit BuildRequires (required per the new guidelines)
- Do not depend on the rpmbuild-imposed man page archiving method

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Oct 15 2015 Jan Pokorný <jpokorny+rpm-libqb@redhat.com> - 0.17.2-1
- Update to libqb-0.17.2 + fix check_ipc tests, for list of changes see:
  https://github.com/ClusterLabs/libqb/releases/tag/v0.17.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Aug 26 2014 David Vossel <dvossel@redhat.com> - 0.17.1-1
Fix: ipcs: Correctly allocate receive buffer size
Fix: ipc_socket: Signalhandler must be resetted to Default, use only cleanup_sigpipe to return from qb_ipc_dgram_sock_setup.
Fix: trie: allow modifying the trie map during the notify callback
Fix: fix invalid option when run 'ipcclient -h'
Fix: epoll: don't miss poll events under high load
Fix: ipc_shm: fix error handling in qb_ipcs_shm_connect()
Fix: ringbuffer: fix size in qb_rb_create_from_file()
Fix: ringbuffer: fix qb_rb_open_2() debug format string
Fix: trie: fixes regression caused by ref count refactoring
Fix: ipcc: Properly timeout during recv when timeout value is provided

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild


* Thu Feb 20 2014 David Vossel <dvossel@redhat.com> - 0.17.0-2
Fix testsuite timing values

* Wed Feb 19 2014 David Vossel <dvossel@redhat.com> - 0.17.0-1
Fix: build: Allow 'make rpm' to work with lightweight tags for release candidates
Fix: spec: reference correct url in spec file
Doc: update broken doxygen link to something that exists
Bump version to 0.17.0
Low: ipc_socket: further optimize max msg size calculations for fbsd portability tests
Low: ipc_socket: Allow socket max msg size to be calculated more accurately
Fix: fixes travis compile time error
Low: tests: Fixes compile time issue with make check
High: ipcs: Prevent ipc server use after free.
Low: ipc: Remove ipc connection reference given to dispatch functions
High: ipc: Fixes memory leak in server connection accept when client partially connects
IPC: Increase the listen backlog of IPC server
Low: ipcs: Clarifications to the ipcs server callback documentation.
Fix rb.test to avoid overwriting memory during reading.
Low: example: Update client/server example to use server enforced buffer size
Low: Client side buffer retrieval regression test
Feature: New api function to retrieve client buffer size
Low: check_ipc.c: Verify server enforced buffer sizes work
Feature: Enforce buffer size limits on the server side
Low: regession tests for regex log filters
Feature: Filter logs using regex patter on function, format, or filename
ipc_setup: Set SO_PASSCRED on listener socket
Fix: log: Filtering by function and file must match exactly, no substring matches
Low: blackbox: Abort blackbox logging on ringbuffer overwrite reclaim error
High: ipcs: Api function allowing server to retrieve client connection's ipc buffer size
Low: ringbuffer: Abort during chunk reclaim if OVERWRITE flag is set and reclaim fails.
High: blackbox: unique blackbox ringbuffer files per pid
Low: ipc_socket: Fixes fd leak in socket ipc client disconnection
Use sizeof to get the correct size of the sockaddr_un sun_path member in a portable way. Fixes corosync on Mac OS X.
Detect the max signal value that can be used using NSIG macro
Avoid double-decrement of level->todo

* Thu Aug 1 2013 David Vossel <dvossel@redhat.com> - 0.16.0-1
Bump version to 0.16.0 ... do not use version 0.15.0
Update release gpg sign key
Bump the version to 0.15.0
Merge pull request #83 from davidvossel/master
Low: ipc_socket: Output send event failure as debug instead of error
Low: ipcserver.c: Fix example server's glib mainloop implementation
High: ipc_socket.c: Detect EOF connection on connection STREAM socket
Merge pull request #81 from davidvossel/dgram_max_msg
Low: tests: Add dgram max size detection test
Low: ipc_socket.c: Handle the unlikely event of an EAGAIN or EINTR during dgram max size detection
Merge pull request #82 from davidvossel/master
Fixes detect disconnect on send for tcp example
Fixes sem leak
Fixes less-than-zero comparision of unsigned int
fixes double close
Fixes double close
Fixes double fd close
Fixes fd leak
Prevent use after free in benchmark util
Fixes use ater free in shm disconnect
Fixes use after free during ipcs client disconnect
Remove dead code
Low: check_ipc.c: Verify dgram max size during tests
High: ipcc: Add abilty to verify dgram kernel buffer size meets max msg value
Fixes travis build error
Merge pull request #80 from davidvossel/master
Low: check_ipc.c: fix debug message to only display once.
High: ringbuffer: Make max_size of ringbuffer accurate so shm ipc max msg size value is honored
Low: ipcs: For shm ipc, always retry outstanding notifications when next event is sent
Low: tests: Added test to verify sending ipc msg equal to max size succeeds
Merge pull request #79 from davidvossel/master
Merge pull request #78 from davidvossel/master
Fix: ipcs: Fixes compile time issue reported by travis
Merge pull request #77 from davidvossel/stress_tests_fixes
Low: loop_pool_kqueue: remove potentially noisy dbug statement
Low: tests: rework bulk event msg ipc test
Account for fbsd ENOBUFS during stress test
Low: tests: Adds ipc event stress test to testsuite
Low: ipc_socket: In fbsd send() returns ENOBUFS when dgram queue is full, this should be treated similar to EAGAIN
High: kqueue: Properly enable kqueue filter in poll loop
Low: ipcs: Attempt to resend outstanding event notifications during event send
Merge pull request #75 from davidvossel/ref_count_cleanup
Low: qbipcs.h: update ipcs connection iterator documentation
Merge pull request #74 from davidvossel/ref_count_cleanup
Fix: ipcs: Disconnect shm ipc connection when poll socket returns error on msg receive
Fix: ipcs: Properly disconnect client connection on POLLNVAL or any other error causing connection removal from mainloop.
Simplify internal ipcs ref counting, add comments and document api behavior
Simplifies connection ref counting without changing behavior
Low remove ref-count error in example ipcserver.
Merge pull request #73 from davidvossel/ref_count_cleanup
Merge pull request #72 from davidvossel/master
Low: tests: Verify reading valid blackbox file works
Fix: refcount leak
Fix: ringbuffer: Add file header version field and detect reading corrupted blackbox files using hash value
Fix: tests: On some platforms -ECONNRESET is returned rather than -ENOTCONN after server failure
Fix: tests: Make blackbox_segfault.sh not depend on bash
Hopefully this is the last travis link fix
Fix travis icon (travis is case sensitive)
Fix the github links
Merge pull request #70 from yuusuke/fix_logging
fix a problem when the character string beyond the number of the maximum characters is passed
Merge pull request #68 from r1mikey/upstream
Add a IPC service context pointer and accessors from both the connection and service level.
Enable distcheck on the travis tests
Add atomic_int.h to noinst_HEADERS
Use the new atomic ops in the ringbuffer
Add internal support for the new __atomic gcc builtins
Rename the configure macros from atomic to sync
ringbuffer: use atomic ops on ringbuffer chunk magic
Remove some test code mistakenly committed to the example program.
IPC: make each connection ref the owning service
Indicate when/why qb_rb_force_close() fails to remove share memory files
Typo fixed in configure
Fix "make srpm"
Remove doxygen from travis deps to try and get the job working.
Fix make distcheck
Merge pull request #60 from t-matsuo/fix-makefile-of-tests
add file_change_bytes into check_PROGRAMS and fix a typo
Deal better with corrupt blackbox files.
Merge pull request #58 from inouekazu/fix_connection_state_checking
IPC: fix the connection state checking
LOG: copy the function/filename for dynamic callsites
Deal with /dev/shm issue on Travis builders
Properly discover SO_NOSIGPIPE and MSG_SIGNAL
IPC: fix call to QB_SUN_LEN
list: don't splice empty lists onto the head.
rpl_sem: make destroy more compliant
test: fix unused-but-set-variable warning
test: fix missing-format-attribute warning
RB: make the "sem" abstraction into a notifier
IPC: clean up the connection state checking
Use dgram sockets for message oriented communications
IPC: don't interpret EMSGSIZE and ENOMSG as a disconnect
POLL: prevent a spin if the fd is not removed from the mainloop
add TAGS and ~ files to .gitignore
docs: install qb-blackbox.8 if doxygen is not available.
IPC: seperate ipc_us.c into 2 files
IPC: move utility functions to unix.c
IPC: make sure we return a consistent error when the message is too big.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 17 2013 Angus Salkeld <asalkeld@redhat.com> - 0.14.4-1
LOG: prevent the last char of the blackbox message from getting lost.
Example: make the blackbox example more practical.
Add the processing which remove notifier at skiplist_destroy function
Add the processing which remove hash node and notifier at hashtable_destroy function
Unify to QB_TRUE/QB_FALSE a boolean value
Document the default prefix in INSTALL
Unify the list processing with qb_list function
Add travis link to the readme.
Fix return code which is an error occurred at pthread function
TEST: add a progam to compare the speed of vsnprintf and qb_vsnprintf_serialize
LOG: add a test for a padded hex int.
Fedora's splint has a strange syntax error, don't fail on it.
LOG: fix truncation in some messages that get padded.
Fix the blackbox formatter when specifing the string len/precision
Fix strlcpy and strlcat functions
IPC: don't over log on disconnect
Make sure we don't use the format string whilst it is getting changed.
ptrie: deref the current node in trie_iter_free()
LOG: fix the format comparison to avoid generating multiple entries.
LOG: set the return code when calloc fails
IPC: call poll if we are mid message and get EAGAIN
Remove extra ";"
IPC: set the error more correctly when qb_sys_mmap_file_open() fails.
Make sure that mmap'ed files smaller than a page size are written to.
example/test: check for error in qb_ipc_run()
example: check for error in qb_ipc_run()
TEST: fix typo s/,/; in check_ipc.c

* Mon Oct 29 2012 Angus Salkeld <asalkeld@redhat.com> - 0.14.3-2
Fix test code highlighted by new check version
Remove the call to autogen.sh - not needed anymore.

* Mon Oct 29 2012 Angus Salkeld <asalkeld@redhat.com> - 0.14.3-1
IPC: Pass the timeout to poll() if the recv function returns EAGAIN
LOG: make the format comparison safe and sane
LOG: don't break on empty callsites, just ignore them
LOG: use the array callback to register new callsites
array: add a mechanism to get a callback when a bin is allocated
Solaris based operating systems don't define MSG_NOSIGNAL and SO_NOSIGPIPE.
Make sure atomic's are initialized (for non-gcc atomic).

* Wed Sep 12 2012 Angus Salkeld <asalkeld@redhat.com> - 0.14.2-2
Fix a crash in ptrie if you iterate over the map in the deleted notifier.

* Mon Sep 10 2012 Angus Salkeld <asalkeld@redhat.com> - 0.14.2-1
Get libqb building on cygwin.
ipc_us: slightly more robust cmsg handling
ipc_us: on Linux, set SO_PASSCRED on the sending socket too
ipc_us: clear request unused fields
TEST: Include writing and reading the blackbox in the log_long_msg test
LOG: fix qb_vsnprintf_deserialize()
blackbox: fix 64-bit big-endian issues
Remove IPC_NEEDS_RESPONSE_ACK and turn off shm ipc on solaris
Define unix path max for openbsd
Only turn on ipc_needs_response_ack=yes for solaris
Some improvements to kqueue usage.
kqueue: drop log message to trace.
Fix splint warning
openbsd requires netinet/in.h before arpa/inet.h
Avoid strcpy() use strlcpy() instead.
Fix kqueue complile warnings
openbsd doesn't have EBADMSG
openbsd has a different UNIX_PATH_MAX
LOG: change qb_vsprintf_serialize() into qb_vsnprintf_serialize()
TEST: increase timeout to 6 secs as the recv timeout is 5 secs
TEST: get the logic right - grrr.
Turn off attribute_section on netbsd
Some missing pshared semaphore checks
Cleanup the checks for pshared semaphores
Add a config check for pthread_mutexattr_setpshared
Remove uses of timersub and use qb_util_stopwatch
RB: change the #error to ENOTSUP if no usable shared process sem
LOOP-KQUEUE: fix reference before assignment.
build: fix libqb.pc creation and make maintainer-clean
LOG: Make sure the semaphores are initialized.
build: remove bashism in cc support check
Catch disconnected sockets on Solaris
Don't free rb->shared_hdr in qb_rb_create_from_file()
Check error return of qb_ipcs_uc_recv_and_auth()
Fix removal of automatically installed doc files when building rpms
Add the mailing list to the travis email notifications.
Work around debian not setting the arch path in splint.
Remove color-tests and parallel-tests automake options.
Add travis continuous integration config
LOG: Invoke custom log filter function if tag changes
tests/rbwriter: don't ignore write failure
ipcs: avoid use-after-free for size-0 || disconnect-request

* Wed Jul 18 2012 Angus Salkeld <asalkeld@redhat.com> - 0.14.1-1
RB: set the new read pointer after clearing the header (#839605).
RB: improve the debug print outs
RB: be more explicit about the word alignment
RB: cleanup the macros for wrapping the index
RB: use sem_getvalue as a tie breaker when read_pt == write_pt
RB: if read or peek don't get the message then re-post to the semaphore
RB: convert the rb_peek() status into a recv like status.
RB: use internal reclaim function
IPC: use calloc instead of malloc to fix valgrind warnings
Upgrade the doxygen config.
Fix a valgrind error.

* Sun Jun 24 2012 Angus Salkeld <asalkeld@redhat.com> - 0.14.0-1
LOG: fix threaded logging.
Add user control of the permissions that are set on the shared mem files
LOG: Restrict string trucation during serialization to when a precision is specified
LOG: Gracefully fail when the caller exceeds QB_LOG_MAX_LEN
LOG: Observe field widths when serializing string arguments
RB: use the same mechanism in reclaim as read/peek to detect end-of-ring
Add needs_response_ack option to ./check
RB: fix wrong sem_flg IPC_NOWAIT option
TESTS: fix warning about unused functions
Remove D_FORTIFY_SOURCE from check.
Open shared mem file in /dev/shm only for linux
Don't use msg_flags on solaris (recvmsg).
Turn off attribute_section on solaris
ipc example: add -e (events) option
IPC: if the server returns EAGAIN or ETIMEOUT the check the connection
LOG: make it possible to fsync() on each file log.
IPC: make sure that the created callback happens before dispatches
LOG: fix the printing of %%p in the blackbox
IPC: On bsd's use the notifier for responses
IPC: interpret ECONNRESET and EPIPE as ENOTCONN
cleanup some warnings
config: use newer AC_COMPILE_IFELSE()
blackbox: fix %%p formatting
LOG: put all fields in the blackbox (added priority and tags)
example: make the priority uint8_t
Remove strerror out of check_funcs
RB: fix compiler warning.
Add replacement function stpcpy
Add missing AC_TYPE_UINT16_T to configure.ac
Use AC_FUNC_STRERROR_R and STRERROR_R_CHAR_P
Add stpcpy strcasecmp to the check_funcs
Move some conditional defines into code (from the configure script)
Remove some unused configure checks
Remove message queues
Check for union semun properly
Blackbox: provide more space for log messages when reading from the blackbox.
Add the blackbox reader manpage to the spec file
Enable error logging for the blackbox reader
RB: Read the file size into an initialized variable of the correct size
Add a tool to dump the blackbox.
RB: to be safer save the read and write pointers at the top of the blackbox
avoid unwarranted use of strncpy: use memcpy instead
blackbox: fix the print_from_file()
RB: add an option to not use any semaphores
LOG: tweak the blackbox format string
LOG: accept NULL strings into the blackbox
LOG: protect close and reload from calling log
Add benchmark option (-b) to examples/ipcclient
TEST: make rbreader/writer more like the other benchmarking apps
IPC: log the connection description in all logs
TEST: re-organise the ipc test suites
IPC: only modify the dispatch if we get EAGAIN
Correctly display timestamp in blackbox

* Thu May 10 2012 Angus Salkeld <asalkeld@redhat.com> - 0.13.0-1
- Remove unneccessary __attribute__ ((aligned(8))) from internal headers
- IPC: add a new function to get (and alloc) the extended stats.
- Revert "Add the event queue length to the connection stats."
- IPC: cleanup better on a failed client connect.
- IPC(soc): be more consistent with control struct size
- IPC: kill a compiler warning
- IPC(soc): pass in the correct size into munmap()
- TEST: Use /bin/sh not /bin/bash
- TEST: check for lost shared mem on bsd too
- rb: cleanup the semaphores
- Fix some small issues in ./check
- Cleanup the .gitignore files
- configure.ac tweaks
- Remove HZ and use sysconf instead.
- SUN_LEN() macro is present if __EXTENSIONS__ is defined on Illumos
- PF_UNIX is a POSIX standard name
- Test for log facility names
- IPC: drop log message to debug.
- IPC: fix retrying of partial recv's and sends.
- IPC: initialize enough shared mem for all 3 one way connections.
- IPC: keep retrying to recv the socket message if partially recv'ed (part 2)
- IPC: keep retrying to recv the socket message if partially recv'ed
- IPC: handle the server shutdown better
- IPC: handle a connection disconnect from the server better
- IPC: make it possible to send events in the connected callback.
- Add the event queue length to the connection stats.
- IPC: add a is_connected client side function.
- Fix typo in ./check
- docs: clarify the need to use request/response headers
- Remove unused local variable
- IPC: change the socket recv function to read the response header.
- Add some special commands into the ipc example
- TEST: improve the tracing in the ipc tests.
- Make "make (s)rpm" work more reliably
- TEST: add a test to confirm we get the events we send.
- TEST: reuse send_and_check for events.
- IPC: make it possible for a root client to talk to a non-root server.
- Run ./Lindent in the examples directory
- Add some debug code to the ipcclient example
- IPC: make sure ipc (socket) clients can connect to a server running as root.
- IPC: allow qb to bump the max_message_size
- IPC: check for a sane minimum max_message_size
- add rpl_sem.h loop_poll_int.h to noinst_headers
- Handle errors more consistently
- call recv_ready on socket types
- Handle a recv of size 0
- make bsd shm path better by default.
- Fix kqueue on freebsd.
- Get the example socket includes right.
- Fix kqueue compiling.
- POLL: seperate out the poll/epoll and add kqueue
- Test existence of getpeer* functions
- Add inet header to tcpclient example
- Don't link with setpshared if unavailable
- NetBSD doesn't have semun defined
- Use MADV_NOSYNC only on systems where available
- Use SCHED_BATCH only on platforms where available
- Fix a bug introduced by the bsd patch.
- Cleanup the selection of semaphores to use
- Fix some leaks in the logging.
- Try and improve the portability on bsd variants.

* Sun Mar 11 2012  Angus Salkeld <asalkeld@redhat.com> - 0.11.1-1
- configue libqb to not use epoll as it seems broken (#800865)
- LOOP: remove some old timerfd code.
- TEST: add a test to check the order of the jobs
- LOOP: when new jobs are added they are added to the head instead of the tail.
- LOG: Now the array is self locking we can make the lookup array dynamic
- Add locking to the array when growing.
- IPC: make the _request_q_len_get() function more obvious.
- IPC: fix multiple receives from qb_ipc_us_recv()
- IPC: make sure that the wrong union member is not written to.
- TIMER: check for null timer handle

Wed Mar 7 2012  Angus Salkeld <asalkeld@redhat.com> - 0.11.0-1
- ARRAY: cleanup the pointer sizeof()
- LOG: turn off __attribute__(section) for powerpc (not working)
- TESTS: move the util tests into "slow-tests" (i.e. optional)
- TEST: make the test_priority the same type as in the callsite
- LOG: make the log arrays manually grow-able since we need to lock the calls.
- RB: fix test failure on ppc
- RB: change the name of the size to word_size to be more clear
- TEST: add some more signal tests.
- LOOP: fix deletion of signal handlers when they are pending
- LOOP: signal handlers were always added as high priority.
- TEST: deal with mac's limited sed
- check: add debugging to the configure options and remove unused options
- TEST: properly clear the filters
- LOG: expose the mechanism to get a dynamic callsite.
- Revert part of my COARSE grained timer commit
- Remove timerfd usage and go back to timelist.
- UTIL: if possible use COARSE resolution clocks - they are much faster.
- ARRAY: save memory (in the bins array) and allow holes in the array
- LOOP: add qb_loop_timer_is_running()
- LOOP: allow stop() and run() to be called with NULL loop instance.
- LOOP: fix doxygen parameter comment
- LOG: add stdout target
- LOOP: add a function to delete jobs
- LOG: remove debug printf's
- LOG: remove an old/incorrect doxygen comment.
- LOG: add a hostname %%H format specifier.
- LOG: Add qb_log_filter_fn_set()

* Tue Feb 14 2012 Angus Salkeld <asalkeld@redhat.com> - 0.10.1-1
- Fix "make distcheck" add include path to AM_CPPFLAGS
- Bump the version to 0.10.1
- clang: Remove unused code
- TEST: make the ipc failure test closer to corosync's case.
- RB: add a debug message if trying to read a message of the wrong size
- IPC: split up the recv into chuncks of 2 seconds. (#788742)
- Be more consistent with the internal logs.
- LOOP: make it possible to pass in NULL as the default loop instance
- RB: use the proper struct not the typedef in the implementation.
- RB: Fix potential mem leak
- Don't mix enums (QB_TRUE/TRUE)
- use random() not rand()
- Remove dead code
- set umask before calling mkstemp()
- Use safer versions of string functions (strcpy -> strlcpy)
- Increase the coverity aggressiveness
- TEST: make the loop ratelimit test more forgiving.

* Tue Feb 07 2012 Angus Salkeld <asalkeld@redhat.com> - 0.10.0-1
- LOOP: handle errors from the poll function
- LOOP: make the item type applicable to jobs too.
- LOOP: fix the todo calculations.
- TEST: check for a single job causing a cpu spin
- LOOP: prevent jobs from consuming too much cpu.
- Get coverity to ignore this warning.
- Change example code to use fgets instead of gets
- LOG: pass the result of qb_log_thread_start() back to the user
- Fix some issues found by clang
- Add clang-analyzer check
- Add a split timer to the stopwatch.
- IPC: merge common code into new function
- IPC: better handle a disconnect been called from within connection_created()
- IPC: fix scary typo
- IPC: fix server error handling

* Mon Feb 06 2012 Angus Salkeld <asalkeld@redhat.com> - 0.9.0-2
- Fix a spin in the mainloop when a timer or poll gets removed
  When in the job queue (#787196).

* Fri Jan 27 2012  Angus Salkeld <asalkeld@redhat.com> - 0.9.0-1
- Rebased to 0.9.0

* Tue Jan 10 2012  Angus Salkeld <asalkeld@redhat.com> - 0.8.1-2
- fix qb_timespec_add_ms()

* Thu Jan 5 2012  Angus Salkeld <asalkeld@redhat.com> - 0.8.1-1
- Rebased to 0.8.1 (#771914)

* Thu Nov 17 2011 Angus Salkeld <asalkeld@redhat.com> - 0.7.0-1
- Rebased to 0.7.0 (#754610)

* Thu Sep 1 2011 Angus Salkeld <asalkeld@redhat.com> - 0.6.0-2
- LOG: fix the default syslog filter

* Tue Aug 30 2011 Angus Salkeld <asalkeld@redhat.com> - 0.6.0-1
- Rebased to 0.6.0 which includes (#734457):
- Add a stop watch
- LOG: serialize the va_list, don't snprintf
- LOG: change active list into array access
- atomic: fix qb_atomic_pointer macros
- LOG: allow the thread priority to be set.
- Fix splint warning on ubuntu 11.04

* Mon Jul 18 2011 Angus Salkeld <asalkeld@redhat.com> - 0.5.1-1
- Rebased to 0.5.1 which includes:
- LOOP: make the return more consistent in qb_loop_timer_expire_time_get()
- LOG: add string.h to qblog.h
- Add a qb_strerror_r wrapper.
- don't let an invalid time stamp provoke a NULL dereference
- LOG: move priority check up to prevent unnecessary format.
- rename README to README.markdown

* Wed Jun 8 2011 Angus Salkeld <asalkeld@redhat.com> - 0.5.0-1
- Rebased to 0.5.0 which includes:
- new logging API
- support for sparc
- coverity fixes

* Tue Feb 8 2011 Angus Salkeld <asalkeld@redhat.com> - 0.4.1-2
- SPEC: improve devel files section
- SPEC: remove global variables

* Mon Jan 31 2011 Angus Salkeld <asalkeld@redhat.com> - 0.4.1-1
- SPEC: add procps to BuildRequire
- SPEC: remove automake and autoconf from BuildRequire
- SPEC: remove call to ./autogen.sh
- SPEC: update to new upstream version 0.4.1
- LOOP: check read() return value
- DOCS: add missing @param on new timeout argument
- BUILD: only set -g and -O options if explicitly requested.
- BUILD: Remove unneccessary check for library "dl"
- BUILD: improve the release build system

* Fri Jan 14 2011 Angus Salkeld <asalkeld@redhat.com> - 0.4.0-2
- remove "." from Summary
- Add "check-devel to BuildRequires
- Add "make check" to check section
- Changed a buildroot to RPM_BUILD_ROOT
- Document alphatag, numcomm and dirty variables.

* Sun Jan 09 2011 Angus Salkeld <asalkeld@redhat.com> - 0.4.0-1
- Initial release
