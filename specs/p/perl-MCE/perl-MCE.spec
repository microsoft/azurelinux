# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-MCE
Version:        1.902
Release: 2%{?dist}
Summary:        Many-core Engine for Perl providing parallel processing capabilities
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/MCE
Source0:        https://cpan.metacpan.org/authors/id/M/MA/MARIOROY/MCE-%{version}.tar.gz
Patch0:         MCE-1.818-Fix-sharp-bang-line.patch
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:  perl(base)
BuildRequires:  perl(bytes)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Errno)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(if)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(overload)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Sereal) >= 3.015
BuildRequires:  perl(Socket)
BuildRequires:  perl(Storable) >= 2.04
BuildRequires:  perl(strict)
BuildRequires:  perl(threads)
BuildRequires:  perl(threads::shared)
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(warnings)
# Script Runtime
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(lib)
BuildRequires:  perl(vars)
# Test Suite
BuildRequires:  perl(open)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(utf8)
# Dependencies
Requires:       perl(File::Path)
Requires:       perl(POSIX)
Requires:       perl(Sereal) >= 3.015
Requires:       perl(Storable) >= 2.04
Requires:       perl(threads::shared)

%description
Many-core Engine (MCE) for Perl helps enable a new level of performance by
maximizing all available cores. MCE spawns a pool of workers and therefore
does not fork a new process per each element of data. Instead, MCE follows
a bank queuing model. Imagine the line being the data and bank-tellers the
parallel workers. MCE enhances that model by adding the ability to chunk
the next n elements from the input stream to the next available worker.

%package tools
Summary:        Many-core Engine command line tools
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       grep, gzip

%description tools
This package delivers command line tools like mce_grep(1) that utilize
the Many-core Engine (MCE) Perl library.

%prep
%setup -q -n MCE-%{version}

# Fix sharp-bang line
%patch -P 0

%build
MCE_INSTALL_TOOLS=1 perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

# Add symlinks for grep variants
ln -s mce_grep %{buildroot}%{_bindir}/mce_egrep
ln -s mce_grep %{buildroot}%{_bindir}/mce_fgrep
ln -s mce_grep %{buildroot}%{_bindir}/mce_zgrep
ln -s mce_grep %{buildroot}%{_bindir}/mce_zegrep
ln -s mce_grep %{buildroot}%{_bindir}/mce_zfgrep

%check
make test

%files
%license LICENSE Copying
%doc Changes Credits README.md
%doc %{perl_vendorlib}/MCE.pod
%doc %{perl_vendorlib}/MCE/Core.pod
%doc %{perl_vendorlib}/MCE/Examples.pod
%dir %{perl_vendorlib}/MCE/
%dir %{perl_vendorlib}/MCE/Core/
%{perl_vendorlib}/MCE.pm
%{perl_vendorlib}/MCE/Candy.pm
%{perl_vendorlib}/MCE/Channel/
%{perl_vendorlib}/MCE/Channel.pm
%{perl_vendorlib}/MCE/Child.pm
%{perl_vendorlib}/MCE/Core.pm
%{perl_vendorlib}/MCE/Core/Input/
%{perl_vendorlib}/MCE/Core/Manager.pm
%{perl_vendorlib}/MCE/Core/Validation.pm
%{perl_vendorlib}/MCE/Core/Worker.pm
%{perl_vendorlib}/MCE/Flow.pm
%{perl_vendorlib}/MCE/Grep.pm
%{perl_vendorlib}/MCE/Loop.pm
%{perl_vendorlib}/MCE/Map.pm
%{perl_vendorlib}/MCE/Mutex.pm
%{perl_vendorlib}/MCE/Mutex/
%{perl_vendorlib}/MCE/Queue.pm
%{perl_vendorlib}/MCE/Relay.pm
%{perl_vendorlib}/MCE/Signal.pm
%{perl_vendorlib}/MCE/Step.pm
%{perl_vendorlib}/MCE/Stream.pm
%{perl_vendorlib}/MCE/Subs.pm
%{perl_vendorlib}/MCE/Util.pm
%{_mandir}/man3/MCE.3*
%{_mandir}/man3/MCE::Candy.3*
%{_mandir}/man3/MCE::Channel.3*
%{_mandir}/man3/MCE::Channel::Mutex.3*
%{_mandir}/man3/MCE::Channel::MutexFast.3*
%{_mandir}/man3/MCE::Channel::Simple.3*
%{_mandir}/man3/MCE::Channel::SimpleFast.3*
%{_mandir}/man3/MCE::Channel::Threads.3*
%{_mandir}/man3/MCE::Channel::ThreadsFast.3*
%{_mandir}/man3/MCE::Child.3*
%{_mandir}/man3/MCE::Core.3*
%{_mandir}/man3/MCE::Core::Input::Generator.3*
%{_mandir}/man3/MCE::Core::Input::Handle.3*
%{_mandir}/man3/MCE::Core::Input::Iterator.3*
%{_mandir}/man3/MCE::Core::Input::Request.3*
%{_mandir}/man3/MCE::Core::Input::Sequence.3*
%{_mandir}/man3/MCE::Core::Manager.3*
%{_mandir}/man3/MCE::Core::Validation.3*
%{_mandir}/man3/MCE::Core::Worker.3*
%{_mandir}/man3/MCE::Examples.3*
%{_mandir}/man3/MCE::Flow.3*
%{_mandir}/man3/MCE::Grep.3*
%{_mandir}/man3/MCE::Loop.3*
%{_mandir}/man3/MCE::Map.3*
%{_mandir}/man3/MCE::Mutex.3*
%{_mandir}/man3/MCE::Mutex::Channel.3*
%{_mandir}/man3/MCE::Mutex::Channel2.3*
%{_mandir}/man3/MCE::Mutex::Flock.3*
%{_mandir}/man3/MCE::Queue.3*
%{_mandir}/man3/MCE::Relay.3*
%{_mandir}/man3/MCE::Signal.3*
%{_mandir}/man3/MCE::Step.3*
%{_mandir}/man3/MCE::Stream.3*
%{_mandir}/man3/MCE::Subs.3*
%{_mandir}/man3/MCE::Util.3*

%files tools
%{_bindir}/mce_grep
%{_bindir}/mce_egrep
%{_bindir}/mce_fgrep
%{_bindir}/mce_zgrep
%{_bindir}/mce_zegrep
%{_bindir}/mce_zfgrep

%changelog
* Wed Sep 10 2025 Paul Howarth <paul@city-fan.org> - 1.902-1
- Update to 1.902 (rhbz#2394255)
  - Add support for Iterator:: classes

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.901-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.901-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan  3 2025 Paul Howarth <paul@city-fan.org> - 1.901-1
- Update to 1.901 (rhbz#2335354)
  - Add MCE::Core package for future development

* Tue Sep 10 2024 Paul Howarth <paul@city-fan.org> - 1.900-1
- Update to 1.900 (rhbz#2310966)
  - Improve MCE::Child exiting when signaled

* Fri Sep  6 2024 Paul Howarth <paul@city-fan.org> - 1.899-1
- Update to 1.899 (rhbz#2310353)
  - Fix for MCE::Child and MCE::Channel signal anomaly (GH#24)

* Thu Aug 22 2024 Paul Howarth <paul@city-fan.org> - 1.898-1
- Update to 1.898 (rhbz#2307114)
  - Fix for MCE::Child, Can't call method "len" on an undefined value
    during global destruction (GH#22)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.897-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jun 20 2024 Paul Howarth <paul@city-fan.org> - 1.897-1
- Update to 1.897
  - In scalar context, the init function in MCE Child and models Flow, Grep,
    Loop, Map, Step, and Stream returns a guard to call finish automatically
    upon leaving the { scope } (i.e. omitting finish)
  - Add out_iter_callback to MCE::Candy

* Wed Jun 12 2024 Paul Howarth <paul@city-fan.org> - 1.896-1
- Update to 1.896 (rhbz#2291411)
  - Weaken internal core MCE reference to reap workers automatically upon
    leaving the scope i.e. omitting shutdown
    - Note: No change to MCE models Flow, Grep, Loop, Map, Step, and Stream
    - Call finish explicitly to reap workers
    - This resolves the case when omitting calling $mce->run(), $mce->run(1) or
      $mce->shutdown() inside a scope, causing workers to linger around until
      completion of the script

* Tue Jun 11 2024 Paul Howarth <paul@city-fan.org> - 1.895-1
- Update to 1.895 (rhbz#2291112)
  - Revert back to calling CORE::rand() to set the internal seed; MCE and
    MCE::Child cannot assume the srand or setter function used by the
    application for predictability
    - https://perlmonks.org/?node_id=11159834
    - https://perlmonks.org/?node_id=11159827
  - Add class methods MCE->seed and MCE::Child->seed to retrieve the seed

* Mon Jun 10 2024 Paul Howarth <paul@city-fan.org> - 1.894-1
- Update to 1.894 (rhbz#2291112)
  - Improve support for PDL

* Sun Jun  9 2024 Paul Howarth <paul@city-fan.org> - 1.893-1
- Update to 1.893 (rhbz#2291021)
  - Remove check if spinning threads i.e. use_threads: predictable output
    matches non-threads for CORE, Math::Prime::Util and
    Math::Random::MT::Auto (see https://perlmonks.org/?node_id=11159834)
  - Preserve functionality for older Perl, non-threads

* Thu Jun  6 2024 Paul Howarth <paul@city-fan.org> - 1.891-1
- Update to 1.891 (rhbz#2290695)
  - Apply workaround for PDL::srand in MCE and MCE::Child
    (https://www.perlmonks.org/?node_id=11159773)
  - Add PDL::srand (v2.062~v2.089) and PDL::srandom (v2.089_01+)
  - Call CORE::srand inside child processes, only

* Sun May 26 2024 Paul Howarth <paul@city-fan.org> - 1.890-1
- Update to 1.890 (rhbz#2283161)
  - Improve reaping of completed workers in MCE::Child
  - Fix the _sprintf function, failing multiple arguments

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.889-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.889-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Sep 14 2023 Paul Howarth <paul@city-fan.org> - 1.889-1
- Update to 1.889 (rhbz#2238875)
  - Add Android support
  - Revert defer signal-handling in MCE::Channel (send2 method)
  - Improve mutex synchronize (a.k.a. enter) with guard capability
  - Fix mutex re-entrant lock on the Windows platform
  - Add mutex guard_lock method

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.888-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 22 2023 Paul Howarth <paul@city-fan.org> - 1.888-1
- Update to 1.888 (rhbz#2216582)
  - Fix typos caught by lintian (GH#17)

* Fri Jun  9 2023 Paul Howarth <paul@city-fan.org> - 1.887-1
- Update to 1.887 (rhbz#2213846)
  - Fix typo in Queue dequeue_timed documentation

* Wed Jun  7 2023 Paul Howarth <paul@city-fan.org> - 1.886-1
- Update to 1.886 (rhbz#2212959)
  - Added dequeue_timed method to MCE::Queue
  - Fixed taint mode in MCE->printf and _sprintf
  - Improved reliability on the Windows platform

* Wed May 31 2023 Paul Howarth <paul@city-fan.org> - 1.885-1
- Update to 1.885 (rhbz#2211269)
  - Improved reliability on the Windows platform
- Avoid use of deprecated patch syntax

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.884-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan  5 2023 Paul Howarth <paul@city-fan.org> - 1.884-1
- Update to 1.884
  - Disabled non-blocking dequeue_nb and recv_nb tests on the Windows platform,
    since the author cannot reproduce failing tests reported by CPAN Tester
    aero

* Wed Jan  4 2023 Paul Howarth <paul@city-fan.org> - 1.883-1
- Update to 1.883 (rhbz#2158062)
  - Fix typo in MCE::Channel::SimpleFast documentation
  - Improve 05_mce_child.t test

* Sat Dec  3 2022 Paul Howarth <paul@city-fan.org> - 1.882-1
- Update to 1.882 (rhbz#2150467)
  - Added ABRT to the list of signals to trap in MCE::Signal
  - Added a guard to MCE::Core::Worker for checking if exited prematurely
  - Added init_relay and use_threads import options to MCE and MCE Models
  - Separated input mutexes from the rest of IPC for lesser latency
  - Auto-detect if init_relay is defined and set chunk_size to 1 in MCE::Grep,
    MCE::Map, and MCE::Stream
  - Update the import function in MCE models, detecting if the caller is
    another MCE module, to not export model functions
  - Update the error status if MCE::Child died due to receiving a signal
  - Improved reaping in MCE::Child, before creating a new child
  - Improved the timeout handler in MCE::Child and MCE::Mutex::Channel
  - Fixed private functions _quit and _trap not setting the return value

* Fri Oct 14 2022 Paul Howarth <paul@city-fan.org> - 1.881-1
- Update to 1.881 (rhbz#2134723)
  - Improved the private _parse_chunk_size function for better utilization of
    CPU cores in MCE::Grep, MCE::Map, and MCE::Stream, processing small input
    sizes
    - Previously, chunk_size => 'auto' equals 2 minimally
    - Starting with MCE v1.881, 'auto' equals 1 minimally

* Mon Oct 10 2022 Paul Howarth <paul@city-fan.org> - 1.880-1
- Update to 1.880 (rhbz#2133410)
  - Improved reliability on the Windows platform
  - Improved MCE::Mutex::Channel::timedwait on the Windows platform
  - Improved MCE::Mutex::Channel performance on UNIX platforms
  - Resolved edge case in MCE::Child reaching deadlock
- Use SPDX-format license tag

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.879-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.879-2
- Perl 5.36 rebuild

* Tue May 24 2022 Paul Howarth <paul@city-fan.org> - 1.879-1
- Update to 1.879
  - Replace http with https in documentation and meta files
  - Call PDL::set_autopthread_targ(1); disables PDL auto-threading

* Sun Feb 20 2022 Paul Howarth <paul@city-fan.org> - 1.878-1
- Update to 1.878
  - Fix for the fast channel implementations

* Sun Feb 20 2022 Paul Howarth <paul@city-fan.org> - 1.877-1
- Update to 1.877
  - Improved suppressing the PDL CLONE warning; piddles should not be naively
    copied into new threads
  - Added fast channel implementations optimized for non-Unicode strings:
    - MCE::Channel::MutexFast
    - MCE::Channel::SimpleFast
    - MCE::Channel::ThreadsFast
    The main difference is that these lack freeze-thaw serialization

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.876-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec  3 2021 Paul Howarth <paul@city-fan.org> - 1.876-1
- Update to 1.876
  - Allow percentage above 100%% for max_workers in MCE
  - MCE::Child update
    - Improved _ordhash
    - Renamed JOINED to REAPED in code for better clarity
    - Specify a percentage for max_workers
    - Added t/05_mce_child_max_workers.t

* Tue Nov 16 2021 Paul Howarth <paul@city-fan.org> - 1.875-1
- Update to 1.875
  - Specify a percentage for max_workers
    (https://www.perlmonks.org/?node_id=11134439)
  - Added t/03_max_workers.t
- Use %%license unconditionally

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.874-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.874-3
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.874-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 19 2020 Paul Howarth <paul@city-fan.org> - 1.874-1
- Update to 1.874
  - Improved MCE->yield when used together with MCE::Relay

* Sun Aug  2 2020 Paul Howarth <paul@city-fan.org> - 1.873-1
- Update to 1.873
  - Removed unused variable in MCE::Mutex::Channel

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.872-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.872-2
- Perl 5.32 rebuild

* Mon Jun 15 2020 Paul Howarth <paul@city-fan.org> - 1.872-1
- Update to 1.872
  - Added open to required dependencies
  - Set default encodings on standard filehandles in tests using UTF-8
  - Bumped minimal Perl version to 5.8.1
  - Bumped MCE version to 1.872 to align with MCE::Shared
  - The MCE project is feature complete

* Mon May 11 2020 Paul Howarth <paul@city-fan.org> - 1.868-1
- Update to 1.868
  - Bug fix for UTF-8 issues during inter-process communication:
    - This update required undoing optimizations specific to scalar args
    - Essentially, IPC involves serialization for everything going forward
    - Install Sereal::Encoder and Sereal::Decoder for better performance in
      Perl 5.8.8+
  - MCE options flush_stdout, flush_stderr, and flush_file now default to
    enabled for the MCE->print, MCE->printf, and MCE->say output routines
  - Improved MCE::Child with threads-like detach capability (see POD)
  - Improved IPC in MCE::Queue with permanent fast-like dequeue including
    dequeue_nb; going forward, the fast and barrier options are silently
    ignored if specified (i.e. no-op)
  - Improved IPC performance on Linux
  - Completed threads-like detach capability in MCE::Child
  - Resolved MCE::Channel failing when calling dequeue multiple times on an
    ended channel
  - MCE->say, MCE->print, and MCE->printf now return 1

* Sun Feb  9 2020 Paul Howarth <paul@city-fan.org> - 1.866-1
- Update to 1.866
  - Bug fix for restart_worker, race condition introduced in 1.863

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.865-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Dec 26 2019 Paul Howarth <paul@city-fan.org> - 1.865-1
- Update to 1.865
  - Bug fix for two-way IPC stalling on Windows in MCE::Channel::Threads:
    see https://www.perlmonks.org/?node_id=11110612
  - Remove the check for MSWin32 in MCE::Channel::Mutex; MCE::Channel since
    the 1st release silently defaults to MCE::Channel::Threads on Windows
  - Small tweak to MCE::Signal

* Wed Dec  4 2019 Paul Howarth <paul@city-fan.org> - 1.864-1
- Update to 1.864
  - Bug fix to MCE::Signal - Shared manager not exiting, introduced in 1.863
  - Use monotonic clock if available in MCE->yield and MCE::Child->yield:
    see https://www.perlmonks.org/?node_id=11109673

* Mon Nov 25 2019 Paul Howarth <paul@city-fan.org> - 1.863-1
- Update to 1.863
  - On Cygwin, silently use Mutex in MCE::Channel when Threads is specified for
    better performance
  - New defer capability in MCE::Signal, which applies to MCE::Shared 1.863;
    see POD section labelled "DEFER SIGNAL" in MCE::Signal
  - Reverted $child->exit back to sending the SIGQUIT signal in MCE::Child now
    that MCE::Shared::Server 1.863 defers signal during IPC
  - Improved reliability for spawning MCE and MCE::Child inside threads
    including nested parallelization, made possible using a global lock
    $MCE::_GMUTEX
  - Updated signal handling in mce-examples/framebuffer on GitHub

* Thu Sep 19 2019 Paul Howarth <paul@city-fan.org> - 1.862-1
- Update to 1.862
  - The edge cases regarding signal handling have finally been resolved for
    MCE::Child; see mce-examples/framebuffer on GitHub

* Mon Sep 16 2019 Paul Howarth <paul@city-fan.org> - 1.860-1
- Update to 1.860
  - Signal-handling update release
  - Localized input and output record separators in MCE::Channel
  - IPC safety in MCE::Child during SIGINT and SIGTERM
  - Method $child->exit in MCE::Child now sends the SIGINT signal for extra
    reliability with MCE::Shared (previously SIGQUIT)

* Mon Sep  9 2019 Paul Howarth <paul@city-fan.org> - 1.850-1
- Update to 1.850 (no changes)

* Mon Sep  9 2019 Paul Howarth <paul@city-fan.org> - 1.849-1
- Update to 1.849
  - Fixed edge case in MCE::Child when reaping inside a signal handler
  - Added list_pids class method to MCE::Child

* Wed Sep  4 2019 Paul Howarth <paul@city-fan.org> - 1.848-1
- Update to 1.848
  - Improved IO::All::{ File, Pipe, STDIO } output via MCE->print($io, ...),
    printf, and say; this resolves a bug introduced in 1.845 when using
    App::Cmd::Tester to capture output

* Tue Sep  3 2019 Paul Howarth <paul@city-fan.org> - 1.847-1
- Update to 1.847
  - Obsolete RedHat MCE-1.840-Sereal-deps.patch file; this patch file is no
    longer needed and finally resolved with this release
  - PDL random numbers now unique between threads:
    see https://www.perlmonks.org/?node_id=1214439
  - Replaced "PF_UNIX" with "AF_UNIX" in MCE::Util

* Tue Aug 27 2019 Paul Howarth <paul@city-fan.org> - 1.846-1
- Update to 1.846
  - Fixed code tags in documentation

* Mon Aug 26 2019 Paul Howarth <paul@city-fan.org> - 1.845-1
- Update to 1.845
  - Croak if is_joinable, is_running, or join is called by a non-managed
    process in MCE::Child; added LIMITATION section to the documentation
  - Improved is_joinable, is_running, list_joinable, and list_running in
    MCE::Child
  - Added example (consumer requests item) to MCE::Channel documentation
  - Support the task_end option regardless of whether user_tasks is specified
  - Support IO::All::{ File, Pipe, STDIO } for input data including output
    via MCE->print($io, ...), printf, and say
  - Support gather ⇒ MCE::Candy::out_iter_fh($io) using MCE::Candy

* Thu Aug 15 2019 Paul Howarth <paul@city-fan.org> - 1.844-1
- Update to 1.844
  - Resolved MCE stalling when specifying max_retries with init_relay, ditto
    for loop_timeout with init_relay on UNIX platforms
  - Enhanced loop_timeout to handle workers dieing uncontrollably from any
    user_tasks (i.e. task_id ≥ 0); previously, only task_id == 0
  - Improved IPC on the Windows platform for edge case when a worker is
    awaiting input while the manager process is restarting a worker
  - MCE, MCE::Child workers exit immediately upon receiving a SIGSEGV signal;
    this safeguards IPC from stalling inside the manager process
  - Enhanced the _wait_one private function in MCE::Child
  - Removed Prima from the list for auto-enabling the posix_exit option; Prima
    (since 1.52) is parallel safe during global cleanup
  - Reached 100%% Pod coverage

* Wed Jul 24 2019 Paul Howarth <paul@city-fan.org> - 1.843-1
- Update to 1.843
  - Updated results in MCE::Child (Parallel::ForkManager-like demonstration)
  - Completed missing interrupt signal-safety for the non-blocking methods in
    MCE::Channel::Mutex and MCE::Channel::Threads

* Mon Jul 22 2019 Paul Howarth <paul@city-fan.org> - 1.842-1
- Update to 1.842
  - Fixed race condition abnormalities in MCE::Child
  - Added Parallel::ForkManager-like demonstration to MCE::Child

* Mon Jul  8 2019 Paul Howarth <paul@city-fan.org> - 1.841-1
- Update to 1.841
  - Disabled t/04_channel_threads testing on Unix platforms for Perl less than
    5.10.1; basically, the MCE::Channel::Threads implementation is not supported
    on older Perls unless the OS vendor applied upstream patches (i.e. works on
    RedHat/CentOS 5.x running Perl 5.8.x)
  - Added LIMITATIONS section to MCE::Channel::Threads

* Sun Jul  7 2019 Paul Howarth <paul@city-fan.org> - 1.840-1
- Update to 1.840
  New Features
  - Added MCE::Mutex::Channel2 providing two locks using a single channel; the
    secondary lock is accessible by calling methods with the '2' suffix, e.g.
    primary mutex ->lock, ->unlock; secondary mutex ->lock2, ->unlock2
  - Added MCE::Channel providing queue-like and two-way communication
    supporting threads and processes
  - Added MCE::Child and compatibility with Perl 5.8; MCE::Child is based on
    MCE::Hobo, but using MCE::Channel for data retrieval without involving a
    shared-manager process
  - Added MCE::Channel examples { channel1.pl and channel2.pl } using threads
    and MCE::Child respectively
  Enhancements
  - IPC update; removed unnecessary overhead including private methods _sysseek
    and _syswrite from MCE::Util (no longer needed)
  - Improved MCE->do, now callable by workers and the manager process
  - Updated MCE::{ Flow, Grep, Loop, Map, Step, and Stream } documentation on
    passing an array reference versus a list for deeply input data
  - Updated and re-organized the top-level MCE documentation, particularly
    improved clarity for the 'MCE Models' section
  - Removed MANIFEST.SKIP
  - Update MCE::Channel POD documentation

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.838-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.838-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Paul Howarth <paul@city-fan.org> - 1.838-1
- Update to 1.838
  - IPC update, raising reliability across multiple platforms
  - Improved hack for the Windows platform for nested MCE sessions
  - Added _sysread, _sysseek, _syswrite, and _nonblocking to MCE::Util
  - Added barrier option to MCE::Queue: allows one to disable

* Tue Aug 28 2018 Paul Howarth <paul@city-fan.org> - 1.837-1
- Update to 1.837
  - Seeds the Math::Random::MT::Auto generator automatically when present for
    non-threads, similarly to Math::Random and Math::Prime::Util, to
    avoid child processes sharing the same seed value as the parent and
    each other; the new seed is computed using the current seed

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.836-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.836-2
- Perl 5.28 rebuild

* Tue Jun 26 2018 Paul Howarth <paul@city-fan.org> - 1.836-1
- Update to 1.836
  - Moved validation code from MCE::Util to MCE::Core::Validation
  - Applied small optimizations

* Wed Mar 14 2018 Paul Howarth <paul@city-fan.org> - 1.835-1
- Update to 1.835
  - Added gather and relay demonstrations to MCE::Relay
  - Load IO::Handle for extra stability, preventing workers loading uniquely
  - Load Net::HTTP and Net::HTTPS before spawning if present LWP::UserAgent
    See http://www.perlmonks.org/?node_id=1199760
    and http://www.perlmonks.org/?node_id=1199891

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.834-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Paul Howarth <paul@city-fan.org> - 1.834-1
- Update to 1.834
  - Improved Queue await and dequeue performance on the Windows platform
  - Added chameneos-redux parallel demonstrations on GitHub:
    https://github.com/marioroy/mce-examples/tree/master/chameneos
- Rebase Sereal-deps patch

* Sun Dec 31 2017 Paul Howarth <paul@city-fan.org> - 1.833-1
- Update to 1.833
  - Fixed bug with sequence, broken in 1.832 (GH#10)

* Wed Nov 22 2017 Paul Howarth <paul@city-fan.org> - 1.832-1
- Update to 1.832
  - Added LWP::UserAgent to list for enabling posix_exit
  - Improved number-sequence generation for big integers
  - Improved wantarray support in MCE::Mutex synchronize
  - Removed limit check on chunk_size option

* Mon Oct  9 2017 Paul Howarth <paul@city-fan.org> - 1.831-1
- Update to 1.831
  - Added STFL (Terminal UI) to list for enabling posix_exit
    (see http://www.perlmonks.org/?node_id=1200923)
  - Math::Prime::Util random numbers now unique between MCE workers
    (see http://www.perlmonks.org/?node_id=1200960)

* Wed Sep 13 2017 Paul Howarth <paul@city-fan.org> - 1.830-1
- Update to 1.830
  Bug Fixes
  - Fixed MCE and MCE::Relay stalling when setting the input record separator
    (see http://www.perlmonks.org/?node_id=1196701)
  - Fixed bug with dequeue_nb in MCE::Queue (GH#8)
  - Fixed signal handler (GH#9)
  Enhancements
  - Added Coro and Win32::GUI to list for enabling posix_exit
  - Added support for Haiku to get_ncpu in MCE::Util
  - Allow gathering to a shared array in MCE::Candy
  - Improved CPU count on the AIX platform in MCE::Util
  - Improved signal handling, including nested parallel-sessions
  - Improved running MCE::Hobo inside MCE workers
  - Improved running MCE with PDL
  - Refactored logic for MCE->do, bi-directional callback feature
  - Preserve lexical type for numbers during IPC: MCE->do and MCE::Queue
  - No longer loads threads on the Windows platform in MCE::Signal; this
    enables MCE::Hobo 1.827 to spin faster, including lesser memory
    consumption (threads isn't required to run MCE::Hobo)
  - Removed extra white-space from POD documentation
  - Validated MCE on SmartOS
- Rebase Sereal-deps patch

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.829-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.829-2
- Perl 5.26 rebuild

* Wed May  3 2017 Paul Howarth <paul@city-fan.org> - 1.829-1
- Update to 1.829
  - Reduced memory consumption

* Sat Apr 29 2017 Paul Howarth <paul@city-fan.org> - 1.828-1
- Update to 1.828
  - Do not enable barrier mode for Queue on the Windows platform
  - Fixed MCE::Mutex::Flock, tmp_file missing script name in path
  - Added Curses and Prima to list for enabling the posix_exit option
  - Allow a hash as input_data: Core API, MCE::{ Flow, Loop, Step }
  - Improved API documentation on MCE models with more synopsis
  - Enhanced IPC and signal handling, reduced memory consumption
  - Make tmp_dir on demand in MCE::Signal; ditto for sess_dir in MCE
  - Load Fcntl, File::Path, Symbol on demand

* Wed Apr  5 2017 Paul Howarth <paul@city-fan.org> - 1.827-1
- Update to 1.827
  - Do not enable barrier mode in Queue if constructed inside a thread or by
    MCE Model (e.g. Step, Stream); ditto for fast => 1 option
  - Updated MCE not to croak when running Perl in taint mode via perl -T;
    failing -T were MCE::Core::Input::{ Generator, Sequence }, MCE::Signal and
    MCE::Util
  - Added Denis Fateyev, Felipe Gasper and Paul Howarth to Credits

* Mon Apr  3 2017 Paul Howarth <paul@city-fan.org> - 1.826-1
- Update to 1.826
  - Performance improvements in MCE::Queue
  - Is now safe running MCE with the Wx GUI toolkit (wxWidgets)
- BR:/R: perl(Sereal) unconditionally

* Sat Apr  1 2017 Paul Howarth <paul@city-fan.org> - 1.824-1
- Update to 1.824
  - Check for EINTR during sysread and syswrite
  - Improved reliability when running nested MCE sessions
  - Updated MCE::Mutex with Channel and Fcntl implementations
  - Calibrated the number of data-channels for IPC
  - Completed validation for using MCE with 200+ cores
  - Completed validation for running MCE on a box having 100+ cores
  - Tuned the number of data-channels for IPC, setting upper limit in
    MCE::Core::Input::{ Handle and Sequence } to not impact the OS kernel; the
    result is better performance, yet graceful

* Sun Mar 19 2017 Paul Howarth <paul@city-fan.org> - 1.821-1
- Update to 1.821
  - Improved reliability when running MCE with threads
  - Added parallel Net::Pcap and Ping demonstrations on GitHub:
    https://github.com/marioroy/mce-examples/tree/master/network
  - Optimized 'dequeue' method in MCE::Queue
  - Optimized 'synchronize' method in MCE::Mutex

* Thu Mar  9 2017 Paul Howarth <paul@city-fan.org> - 1.820-1
- Update to 1.820
  - Improved reliability when running MCE inside an eval block

* Sat Mar  4 2017 Paul Howarth <paul@city-fan.org> - 1.819-1
- Update to 1.819
  - Fixed issue with localizing AUTOFLUSH variable before autoflush handles

* Thu Mar  2 2017 Paul Howarth <paul@city-fan.org> - 1.818-1
- Update to 1.818
  - Updated bin/mce_grep for determining chunk level and chunk size
  - Fixed an issue for not seeing STDERR output with '--chunk-level=file'
  - Added support for zgrep, zegrep, and zfgrep
  - Replaced Sereal with Sereal::Decoder and Sereal::Encoder in Makefile,
    inside recommends section; ditto for META files
  - Refactored MCE::Queue: merged local and manager code base into one
  - Removed t/04_norm_que_local.t and t/04_prio_que_local.t
  - Added 'end' method to MCE::Queue
  - Updated documentation on dequeue and pending
- Add symlinks for mce_grep variants

* Sat Feb 25 2017 Paul Howarth <paul@city-fan.org> - 1.817-1
- Update to 1.817
  - Revised the description of max_retries in MCE::Core.pod
  - Improved bin/mce_grep with -r parameter:
    - If no paths are given, start recursively in the current directory
      rather than await data from STDIN
    - Set chunk-level accordingly to list mode

* Fri Feb 24 2017 Paul Howarth <paul@city-fan.org> - 1.815-1
- Update to 1.815
  - Fixed divide-by-zero error in MCE->yield
  - Refactored code for the interval option by moving the code to the manager
    process, which allows the manager process to accommodate the next available
    worker ready to run; previously, a worker taking a long time resulted in
    empty time slots
  - Revised the description of posix_exit in MCE::Core.pod

* Mon Feb 20 2017 Paul Howarth <paul@city-fan.org> - 1.814-1
- Update to 1.814
  - Enhanced the progress option for use with MCE->process
  - Updated progress demonstrations in MCE::Core.pod

* Thu Feb 16 2017 Paul Howarth <paul@city-fan.org> - 1.813-1
- Update to 1.813
  - Added progress option, a code block for receiving info on progress made;
    see MCE::Core.pod for demonstrations accommodating all input data types

* Wed Feb 15 2017 Paul Howarth <paul@city-fan.org> - 1.812-1
- Update to 1.812
  - Bumped minimum requirement for Sereal to 3.015 when available; added check
    ensuring matching version for Encoder and Decoder
- Add patch to avoid unintentional hard dependencies on Sereal

* Tue Feb 14 2017 Paul Howarth <paul@city-fan.org> - 1.811-1
- Update to 1.811
  - Fixed bug in MCE::Queue (dequeue_nb) when queue has zero items
  - Applied small optimization in MCE::Core::Input::Sequence and Generator
  - Added cross-platform template to MCE::Examples for making an executable
  - Removed signal handling for XCPU and XFSZ from MCE::Signal
  - Imply posix_exit => 1 if Gearman::XS or Gearman::Util is present during
    MCE construction
  - Added MCE + Gearman demonstrations (xs and non-xs) on GitHub:
    https://github.com/marioroy/mce-examples/tree/master/gearman_xs
    https://github.com/marioroy/mce-examples/tree/master/gearman
  - Changed kilobytes and megabytes to kibiBytes (KiB) and mebiBytes (MiB)
    respectively inside the documentation

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.810-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Dec 10 2016 Paul Howarth <paul@city-fan.org> - 1.810-1
- Update to 1.810
  - Updated check for IO handle allowed; this allows $gather_fh = *STDOUT{IO}
    construction in Perl ≤ 5.10.1

* Thu Nov 24 2016 Paul Howarth <paul@city-fan.org> - 1.809-1
- Update to 1.809
  - Bug fixes for running MCE inside threads
  - Random numbers are unique between workers

* Sat Nov  5 2016 Paul Howarth <paul@city-fan.org> - 1.808-1
- Update to 1.808
  - Workers persist unless shutdown explicitly while running alongside the
    Mojolicious framework

* Wed Nov  2 2016 Paul Howarth <paul@city-fan.org> - 1.807-1
- Update to 1.807
  - Enhanced relay capabilities
    - Added Mandelbrot example to MCE::Example
    - Added extra demonstrations to MCE::Relay
    - Added test script
  - Tweaked manager-loop delay for special cases - applies to MSWin32 only

* Wed Oct 12 2016 Paul Howarth <paul@city-fan.org> - 1.806-1
- Update to 1.806
  - Fixed two typos
  - Support input_data with nested arrays in MCE Models

* Fri Sep  2 2016 Paul Howarth <paul@city-fan.org> - 1.805-1
- Update to 1.805
  - Fixed bug in MCE::Queue (GH#4)
  - Improved support for running MCE with Tk; added Tk demonstrations to
    MCE::Examples

* Fri Jul 29 2016 Paul Howarth <paul@city-fan.org> - 1.804-1
- Update to 1.804
  - Removed the sleep statement in MCE->restart_worker
  - Added FCGI::ProcManager demonstrations to MCE::Examples
  - Automatically set posix_exit to 1 whenever (F)CGI.pm is present
    (https://github.com/marioroy/mce-perl/issues/1)

* Mon Jul 11 2016 Paul Howarth <paul@city-fan.org> - 1.803-1
- Update to 1.803
  - Re-enabled Sereal 3.008+ for Perl < v5.12.0, if available
  - Optimized dequeue methods in MCE::Queue

* Mon Jul  4 2016 Paul Howarth <paul@city-fan.org> - 1.802-1
- Update to 1.802
  - Default to Storable for serialization in Perl less than v5.12.0;
    Sereal 3.008+, if available, is loaded automatically in Perl v5.12+

* Sun Jul  3 2016 Paul Howarth <paul@city-fan.org> - 1.801-1
- Update to 1.801
  - Fixed race condition in Queue->await
  - MCE 1.801 is stable on all supported platforms
  - Completed work supporting cyclical include of MCE Core / Models
  - Updated MCE to support Perl included with Git Bash
  - Renamed temp dir from 'mce' to 'Perl-MCE' under user's %%TEMP%% location on
    Windows, e.g. Native Perl, Cygwin, Git Bash
- BR: perl-generators unconditionally

* Sun Jun 19 2016 Paul Howarth <paul@city-fan.org> - 1.800-1
- Update to 1.800
  - Fixed dequeue (count) in MCE::Queue for standalone mode
  - On Windows, improved stablity and feature parity with UNIX
  - Use Sereal 3.008+ automatically if available on the box
  - Added support for cyclical include of MCE Core, MCE Models, and MCE Queue
    by scoping the configuration to the local package (CPAN RT#107384)

* Sun May 29 2016 Paul Howarth <paul@city-fan.org> - 1.708-1
- Update to 1.708
  - Improved import routine in MCE Models and MCE::Subs; this resolves an issue
    where functions are not exported; e.g. mce_flow, mce_flow_s
  - Added support for IO::TieCombine handles, which enables MCE->print and
    MCE->sendto to work reliably with App::Cmd and App::Cmd::Tester; see
    Testing and Capturing Output in MCE::Examples

* Thu May 26 2016 Paul Howarth <paul@city-fan.org> - 1.707-1
- Update to 1.707
  - Fixed logic when workers exit; improved reliability on Windows
  - Applied MCE-1.700-provides.patch from Red Hat
  - Added META.json to the distribution
- BR: perl-generators where available
- Drop upstreamed provides patch

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.706-2
- Perl 5.24 rebuild

* Sun Apr 24 2016 Paul Howarth <paul@city-fan.org> - 1.706-1
- Update to 1.706
  - Time::HiRes sleep resolution is 15 milliseconds on Windows and Cygwin;
    adjusted timeout values accordingly
  - Reinstated the hack for faster IO when use_slurpio => 1 is specified; tuned
    chunk_size => 'auto'

* Fri Apr 15 2016 Paul Howarth <paul@city-fan.org> - 1.705-1
- Update to 1.705
  - Bumped version for Test::More to 0.88
- BR:/R: perl(Sereal) where available

* Thu Apr 14 2016 Paul Howarth <paul@city-fan.org> - 1.704-1
- Update to 1.704
  BUG FIXES
  - Fixed restart on the Windows platform, bug introduced in 1.700
  - Reached *stable* on all major platforms for MCE 1.7x
  ENHANCEMENTS
  - Enabled auto-destroy for MCE objects
  - Enabled freeze callbacks for Sereal
  - Switched bug tracking to GitHub
  - Tweaked test scripts

* Sun Mar 20 2016 Paul Howarth <paul@city-fan.org> - 1.703-1
- Update to 1.703
  - Completed IPC optimizations for 1.7

* Wed Mar 16 2016 Paul Howarth <paul@city-fan.org> - 1.702-1
- Update to 1.702
- Use a patch to fix unversioned provides of perl(MCE)
- Get rid of redundant provides/requires filters
- Make %%files list more explicit

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.608-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.608-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.608-2
- Perl 5.22 rebuild

* Fri Apr 10 2015 Petr Šabata <contyk@redhat.com> - 1.608-1
- 1.608 bump

* Thu Apr 09 2015 Petr Šabata <contyk@redhat.com> - 1.606-1
- 1.606 bump

* Wed Apr 08 2015 Petr Šabata <contyk@redhat.com> - 1.605-1
- 1.605 bump

* Mon Mar 23 2015 Petr Šabata <contyk@redhat.com> - 1.604-1
- 1.604 bump

* Wed Feb 11 2015 Petr Pisar <ppisar@redhat.com> - 1.600-3
- Move mce_grep tool into a separate sub-package

* Tue Feb 10 2015 Petr Pisar <ppisar@redhat.com> - 1.600-2
- Correct dependencies

* Wed Feb 04 2015 Petr Šabata <contyk@redhat.com> - 1.600-1
- 1.600 bump

* Mon Jan 05 2015 Petr Šabata <contyk@redhat.com> - 1.522-1
- 1.522 bump

* Wed Dec 17 2014 Petr Šabata <contyk@redhat.com> - 1.521-1
- 1.521 bump

* Tue Nov 11 2014 Petr Šabata <contyk@redhat.com> 1.520-1
- Initial packaging
