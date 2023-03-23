%bcond_without perl_Test_Simple_enables_optional_test

Summary:        Basic utilities for writing tests
Name:           perl-Test-Simple
Version:        1.302174
Release:        4%{?dist}
License:        (GPL+ OR Artistic) AND CC0 AND Public Domain
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Test-Simple
Source0:        https://cpan.metacpan.org/modules/by-module/Test/Test-Simple-%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(CPAN::Meta)
BuildRequires:  perl(CPAN::Meta::Requirements) >= 2.120920
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IO::Pipe)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(JSON::PP)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Module::Metadata)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(PerlIO) >= 1.02
BuildRequires:  perl(Scalar::Util) >= 1.13
BuildRequires:  perl(Storable)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Term::ANSIColor)
BuildRequires:  perl(Test::Harness) >= 2.03
BuildRequires:  perl(base)
BuildRequires:  perl(lib)
BuildRequires:  perl(mro)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(threads)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Data::Dumper)
Requires:       perl(JSON::PP)
Requires:       perl(Term::ANSIColor)
Requires:       perl(mro)
BuildArch:      noarch
%{?perl_default_filter}
%if !%{defined perl_bootstrap}
BuildRequires:  perl(Term::Table)
%endif
%if !%{defined perl_bootstrap}
%if %{with perl_Test_Simple_enables_optional_test}
BuildRequires:  perl(Test::Class)
BuildRequires:  perl(Test::Pod) >= 0.95
BuildRequires:  perl(Test::Script)
%endif
%endif
%if !%{defined perl_bootstrap}
Requires:       perl(Term::Table)
%endif

%description
This package provides the bulk of the core testing facilities. For more
information, see perldoc for Test::Simple, Test::More, etc.

This package is the CPAN component of the dual-lifed core package Test-Simple.

%prep
%autosetup -n Test-Simple-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PERLLOCAL=1 NO_PACKLIST=1
%make_build

%install
%make_install
%{_fixperms} -c %{buildroot}

%check
make test %{!?perl_bootstrap:AUTHOR_TESTING=1}

%files
%license LICENSE
%doc Changes README examples/ t/
%dir %{perl_vendorlib}/Test/
%{perl_vendorlib}/ok.pm
%{perl_vendorlib}/Test/Builder.pm
%{perl_vendorlib}/Test/Builder/
%{perl_vendorlib}/Test/More.pm
%{perl_vendorlib}/Test/Simple.pm
%{perl_vendorlib}/Test/Tester.pm
%{perl_vendorlib}/Test/Tester/
%doc %{perl_vendorlib}/Test/Tutorial.pod
%{perl_vendorlib}/Test/use/
%{perl_vendorlib}/Test2.pm
%{perl_vendorlib}/Test2/
%{_mandir}/man3/ok.3*
%{_mandir}/man3/Test::Builder.3*
%{_mandir}/man3/Test::Builder::Formatter.3*
%{_mandir}/man3/Test::Builder::IO::Scalar.3*
%{_mandir}/man3/Test::Builder::Module.3*
%{_mandir}/man3/Test::Builder::Tester.3*
%{_mandir}/man3/Test::Builder::Tester::Color.3*
%{_mandir}/man3/Test::Builder::TodoDiag.3*
%{_mandir}/man3/Test::More.3*
%{_mandir}/man3/Test::Simple.3*
%{_mandir}/man3/Test::Tester.3*
%{_mandir}/man3/Test::Tester::Capture.3*
%{_mandir}/man3/Test::Tester::CaptureRunner.3*
%{_mandir}/man3/Test::Tutorial.3*
%{_mandir}/man3/Test::use::ok.3*
%{_mandir}/man3/Test2.3*
%{_mandir}/man3/Test2::API.3*
%{_mandir}/man3/Test2::API::Breakage.3*
%{_mandir}/man3/Test2::API::Context.3*
%{_mandir}/man3/Test2::API::Instance.3*
%{_mandir}/man3/Test2::API::Stack.3*
%{_mandir}/man3/Test2::Event.3*
%{_mandir}/man3/Test2::Event::Bail.3*
%{_mandir}/man3/Test2::Event::Diag.3*
%{_mandir}/man3/Test2::Event::Encoding.3*
%{_mandir}/man3/Test2::Event::Exception.3*
%{_mandir}/man3/Test2::Event::Fail.3*
%{_mandir}/man3/Test2::Event::Generic.3*
%{_mandir}/man3/Test2::Event::Note.3*
%{_mandir}/man3/Test2::Event::Ok.3*
%{_mandir}/man3/Test2::Event::Pass.3*
%{_mandir}/man3/Test2::Event::Plan.3*
%{_mandir}/man3/Test2::Event::Skip.3*
%{_mandir}/man3/Test2::Event::Subtest.3*
%{_mandir}/man3/Test2::Event::TAP::Version.3*
%{_mandir}/man3/Test2::Event::V2.3*
%{_mandir}/man3/Test2::Event::Waiting.3*
%{_mandir}/man3/Test2::EventFacet.3*
%{_mandir}/man3/Test2::EventFacet::About.3*
%{_mandir}/man3/Test2::EventFacet::Amnesty.3*
%{_mandir}/man3/Test2::EventFacet::Assert.3*
%{_mandir}/man3/Test2::EventFacet::Control.3*
%{_mandir}/man3/Test2::EventFacet::Error.3*
%{_mandir}/man3/Test2::EventFacet::Hub.3*
%{_mandir}/man3/Test2::EventFacet::Info.3*
%{_mandir}/man3/Test2::EventFacet::Info::Table.3*
%{_mandir}/man3/Test2::EventFacet::Meta.3*
%{_mandir}/man3/Test2::EventFacet::Parent.3*
%{_mandir}/man3/Test2::EventFacet::Plan.3*
%{_mandir}/man3/Test2::EventFacet::Render.3*
%{_mandir}/man3/Test2::EventFacet::Trace.3*
%{_mandir}/man3/Test2::Formatter.3*
%{_mandir}/man3/Test2::Formatter::TAP.3*
%{_mandir}/man3/Test2::Hub.3*
%{_mandir}/man3/Test2::Hub::Interceptor.3*
%{_mandir}/man3/Test2::Hub::Interceptor::Terminator.3*
%{_mandir}/man3/Test2::Hub::Subtest.3*
%{_mandir}/man3/Test2::IPC.3*
%{_mandir}/man3/Test2::IPC::Driver.3*
%{_mandir}/man3/Test2::IPC::Driver::Files.3*
%{_mandir}/man3/Test2::Tools::Tiny.3*
%{_mandir}/man3/Test2::Transition.3*
%{_mandir}/man3/Test2::Util.3*
%{_mandir}/man3/Test2::Util::ExternalMeta.3*
%{_mandir}/man3/Test2::Util::Facets2Legacy.3*
%{_mandir}/man3/Test2::Util::HashBase.3*
%{_mandir}/man3/Test2::Util::Trace.3*

%changelog
* Tue Mar 07 2023 Muhammad Falak <mwani@microsoft.com> - 1.302174-4
- License verified

* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 1.302174-3
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3:1.302174-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Mar 31 2020 Paul Howarth <paul@city-fan.org> - 3:1.302174-1
- Update to 1.302174
  - Fall back to Data::Dumper if JSON::PP is not available during IPC errors

* Fri Mar 27 2020 Paul Howarth <paul@city-fan.org> - 3:1.302173-1
- Update to 1.302173
  - Add extra debugging for "Not all files from hub '...' have been collected!"

* Mon Mar  9 2020 Paul Howarth <paul@city-fan.org> - 3:1.302172-1
- Update to 1.302172
  - Fix transition documentation
  - Fix warnings from info/debug tap

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3:1.302171-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Paul Howarth <paul@city-fan.org> - 3:1.302171-1
- Update to 1.302171
  - Fix 5.6
  - Fix EBCDIC
  - Upgrade Object::HashBase
  - Clarify error message in test (GH#841)
  - Spelling/Grammar fixes

* Thu Jan 02 2020 Petr Pisar <ppisar@redhat.com> - 3:1.302170-2
- Require mro

* Tue Dec  3 2019 Paul Howarth <paul@city-fan.org> - 3:1.302170-1
- Update to 1.302170
  - Fix unwanted END phase event (GH#840)

* Tue Nov 19 2019 Paul Howarth <paul@city-fan.org> - 3:1.302169-1
- Update to 1.302169
  - Update inlined Object::HashBase
  - Avoid 'used only once' warnings in BEGIN and END blocks

* Fri Sep  6 2019 Paul Howarth <paul@city-fan.org> - 3:1.302168-1
- Update to 1.302168
  - Fix typo in a Test2::API::Breakage warning
  - Delay loading of Term::Table until needed

* Mon Aug 26 2019 Paul Howarth <paul@city-fan.org> - 3:1.302167-1
- Update to 1.302167
  - Add test2_is_testing_done api method
  - Fix string compare warning

* Fri Aug 16 2019 Paul Howarth <paul@city-fan.org> - 3:1.302166-1
- Update to 1.302166
  - Better diagnostics when a context is destroyed unexpectedly
  - Add an event to notify when END phase starts

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3:1.302164-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3:1.302164-3
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3:1.302164-2
- Perl 5.30 rebuild

* Sun Apr 28 2019 Paul Howarth <paul@city-fan.org> - 2:1.302164-1
- Update to 1.302164
  - Do not use threads::shared in Test::Tester::Capture (GH#826)
  - Add missing version info to Info/Table
  - Fix event in global destruction bug (GH#827)
  - Proper fix for todo = '' (GH#812, GH#829)
- Modernize spec using %%{make_build} and %%{make_install}
- Drop obsoletes/provides for perl-Test2 dating back to Fedora 25

* Wed Feb  6 2019 Paul Howarth <paul@city-fan.org> - 2:1.302162-1
- Update to 1.302162
  - Remove SHM Optimization
  - Typo fixes in documentation

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.302160-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jan 19 2019 Paul Howarth <paul@city-fan.org> - 2:1.302160-1
- Update to 1.302160
  - Fix minor typos and missing doc sections
  - Add table support in info facet and TAP formatter
  - Fix TAP test on Windows
  - Fix math errors in table indentation
  - Devel requires Term::Table
  - Add table support to ctx->fail and ctx->fail_and_return
  - Fix Instance.t on haiku-os

* Tue Jan  8 2019 Paul Howarth <paul@city-fan.org> - 2:1.302156-1
- Update to 1.302156
  - Fix Windows fork+test failure (GH#814)
  - Documentation updates (GH#819)
  - Fix verbose TAP newline regression (GH#810)
  - Fix local $TODO bugs (GH#812, GH#817)
  - Fix shm read warning (GH#815)
  - Merge doc fix PR's from magnolia-k
  - Fix failure to check error code on shmwrite (GH#815)
  - Fix localization error in new test (GH#820)
  - Fix SHM test to work on machines without SHM
  - Fix locale errors in Instance.t
  - Windows test fixes
  - Perl 5.6 test fixes
  - Add trace to SHM error when possible
  - Fix test not to fail in non-english locales

* Sun Dec  2 2018 Paul Howarth <paul@city-fan.org> - 2:1.302141-1
- Update to 1.302141
  - Fix bug where IPC init failed in preload+fork environments

* Tue Aug 14 2018 Paul Howarth <paul@city-fan.org> - 2:1.302140-1
- Update to 1.302140
  - Mask warning from the recent IPC fix generated when threaded Test tools are
    loaded at run-time

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.302138-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 12 2018 Paul Howarth <paul@city-fan.org> - 2:1.302138-1
- Update to 1.302138
  - Make it safe to fork before events in IPC

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2:1.302136-3
- Perl 5.28 re-rebuild of bootstrapped packages

* Tue Jun 26 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2:1.302136-2
- Perl 5.28 rebuild

* Thu Apr 19 2018 Paul Howarth <paul@city-fan.org> - 1:1.302136-1
- Update to 1.302136
  - Add test2_add_callback_testing_done to Test2::API

* Fri Mar 30 2018 Paul Howarth <paul@city-fan.org> - 1:1.302135-1
- Update to 1.302135
  - Make sure all hubs, events, and contexts get a unique (per run) id
  - Use a common generator for unique(enough) id's (not UUIDs)

* Mon Mar 12 2018 Paul Howarth <paul@city-fan.org> - 1:1.302133-1
- Update to 1.302133
  - Make sure event puts the uuid into the about facet
  - Add method to validate facet data
  - Add Test2::Event::V2 event class, and context helpers
  - Improve how events handle facets
  - Break out meta_facet_data
  - Document and fix Facets2Legacy
  - Fix nested and in_subtest to look at hub facets
  - Fix event->related and trace with uuid

* Thu Mar  8 2018 Paul Howarth <paul@city-fan.org> - 1:1.302130-1
- Update to 1.302130
  - Make hubs tag events with a new facet

* Tue Mar 06 2018 Petr Pisar <ppisar@redhat.com> - 1:1.302128-1
- Update to 1.302128
  - Add optional UUID tagging

* Thu Feb 22 2018 Paul Howarth <paul@city-fan.org> - 1:1.302125-1
- Update to 1.302125
  - Make it possible to disable IPC
  - Fix a test to skip without threads

* Tue Feb  6 2018 Paul Howarth <paul@city-fan.org> - 1:1.302122-1
- Update to 1.302122
  - Add 'mode' to render facet

* Mon Feb  5 2018 Paul Howarth <paul@city-fan.org> - 1:1.302121-1
- Update to 1.302121
  - Update Copyright
  - Add 'render' facet

* Thu Nov 30 2017 Paul Howarth <paul@city-fan.org> - 1:1.302120-1
- Update to 1.302120
  - Fix IPC reload bug

* Wed Nov 29 2017 Paul Howarth <paul@city-fan.org> - 1:1.302118-1
- Update to 1.302118
  - Added pre-subtest hook to Test2::API (GH#801)
  - ipc_wait now reports exit and signal values
  - Add better interface for ipc_wait
  - Fix event Out of Order bug
  - Add driver_abort() hook for IPC Drivers

* Tue Nov 21 2017 Paul Howarth <paul@city-fan.org> - 1:1.302113-1
- Update to 1.302113
  - Fix test on threaded 5.8
  - Fix SIGPIPE in IPC test
  - Mark t/Test2/regression/gh_16.t as usually AUTHOR_TESTING only

* Mon Nov 20 2017 Paul Howarth <paul@city-fan.org> - 1:1.302111-1
- Update to 1.302111
  - Fix some fragile tests
  - Apply p5p test patch from Craig A. Berry
  - Allow regexp in Test::Tester

* Mon Oct 23 2017 Paul Howarth <paul@city-fan.org> - 1:1.302106-1
- Update to 1.302106
  - Combine multiple diags into one event
  - Make version number in HashBase sane

* Mon Oct 16 2017 Paul Howarth <paul@city-fan.org> - 1:1.302103-1
- Update to 1.302103
  - Fix some TODO edge cases that were not previously accounted for

* Fri Oct 13 2017 Paul Howarth <paul@city-fan.org> - 1:1.302101-1
- Update to 1.302101
  - Bump Test::Builder::IO::Scalar version for core

* Wed Oct 11 2017 Paul Howarth <paul@city-fan.org> - 1:1.302100-1
- Update to 1.302100
  - Fix run_subtest inherit_trace option

* Tue Oct  3 2017 Paul Howarth <paul@city-fan.org> - 1:1.302098-1
- Update to 1.302098
  - Add docs for test2_stdout and test2_stderr
  - Fix 5.6 support

* Tue Oct 3 2017 Paul Howarth <paul@city-fan.org> - 1:1.302097-1
- Update to 1.302097
  - Fix hub->process bug that could let an error pass
  - Fix modification of read only value (#789)
  - Fix typo in Test::Builder when looking for IPC (#777)
  - Fix clone_io broke on scalar io layer (#791)
  - Fix Exception event stringify exception (#756, #790)
  - Localize $^E in context (#780)
  - Fix test that failed in verbose mode (#770)

* Mon Sep 11 2017 Paul Howarth <paul@city-fan.org> - 1:1.302096-1
- Update to 1.302096
  - Introduce 'Facets' for events
  - Performance enhancements
  - Upgrade inline HashBase
  - Move Test2::Util::Trace to Test2::EventFacet::Trace
  - Track hub id in Trace
  - Remove Info event
  - Add Pass and Fail events
  - Remove Event JSON interface
  - Fix tests on perl 5.25+ with newer Data::Dumper
  - Fix plan in buffered subtest so that the facts say it is buffered
  - Fix test that unintentionally required Test2::Suite
  - Add 'new_root' constructor for formatters
  - Add intercept_deep() to the API
  - Fix bug in Version event
  - Add 'number' attribute to assertion facet
  - Fix bug in Facets for TodoDiag
  - Add API command to reset after a fork
  - Add 'important' flag to info event facet
  - Make sure Test::Builder does not initialize Test2 too soon
  - Fix Test::Builder in a preload scenario
  - Make several tests work with preload
  - Fix to work with subref-in-stash optimization

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.302086-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 21 2017 Paul Howarth <paul@city-fan.org> - 1:1.302086-1
- Update to 1.302086
  - Make it possible to turn off result logging in Test::Builder

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.302085-2
- Perl 5.26 rebuild

* Tue May  2 2017 Paul Howarth <paul@city-fan.org> - 1.302085-1
- Update to 1.302085
  - Better IO management
  - Allow access to the STDERR/STDOUT Test2::API uses
  - Formatters should use the Test2::API handles

* Sat Apr 15 2017 Paul Howarth <paul@city-fan.org> - 1.302083-1
- Update to 1.302083
  - Fixes for '. in @INC' changes (#768)
  - Timeout when waiting for child procs and threads (#765)
  - Fix SIGSYS localization issue (#758)
  - Fix outdated docs (#759, #754)
  - Fix bail-out in buffered subtest (#747)
  - Fix threads timeout for older perls (as best we can)
  - Fix test that incorrectly called private function as method
  - Update some breakage info for Test::More::Prefix and
    Test::DBIx::Class::Schema

* Thu Mar  2 2017 Paul Howarth <paul@city-fan.org> - 1.302078-1
- Update to 1.302078
  - Fix crash when TB->reset used inside subtest
  - Fix #762, newlines for todo subtest
  - Revisit #637, fix rare race condition it created

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.302075-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 11 2017 Paul Howarth <paul@city-fan.org> - 1.302075-1
- Update to 1.302075
  - Add 'cid' to trace
  - Add signatures to trace
  - Add related() to events
  - Now it is possible to check if events are related
  - Add 'no_fork' option to run_subtest()

* Mon Dec 19 2016 Paul Howarth <paul@city-fan.org> - 1.302073-1
- Update to 1.302073
  - Add TO_JSON and from_json methods to Test2::Event and Test2::Trace::Util to
    facilitate transferring event data between processes (#741)
  - Generate HashBase from Object::HashBase, which has been split out
  - When a subtest is marked as todo, all of its contained Ok and Subtest
    events are now updated so that they return true for $e->effective_pass
    (#742)
  - Added two new event classes, Test2::Event::Encoding and
    Test2::Event::TAP::Version; these are primarily being added for the benefit
    of Test2::Harness now, but they could be useful for other Test2 event
    consumer tools in the future (#743)
  - Expose tools.pl as Test2::Tools::Tiny

* Thu Nov 24 2016 Paul Howarth <paul@city-fan.org> - 1.302067-1
- Update to 1.302067
  - Fix double release when 'throw' is used in context_do()
  - Repo management improvements
  - Better handling of info vs. diag in ->send_event
  - Fix test that used 'parent'
  - Better handling of non-bumping failures (#728)
  - Set the TEST_ACTIVE env var to true
  - Set the TEST2_ACTIVE env var to true
  - Fix cmp_ok output in some confusing cases (#6)
  - Update travis config
  - Add missing author deps
  - Fix handling of negative pids on Windows
  - Add can() to Test::Tester::Delegate (despite deprecation)
  - Fix some minor test issues
  - Handle cases where SysV IPC can be available but not enabled
  - Import 'context' into Test2::IPC; it is used by 'cull'
  - Propagate warnings settings to use_ok (#736)
  - Fix context test for recent blead

* Thu Oct 20 2016 Paul Howarth <paul@city-fan.org> - 1.302062-1
- Update to 1.302062
  - Formatters now have terminate() and finalize() methods; these are called
    when there is a skip_all or bail event (terminate), or when a test suite is
    exiting normally (finalize), which allows formatters to finalize their
    output - this is important for any sort of document-oriented format (as
    opposed to a stream format like TAP) (#723)
  - Removed a warning when using a non-TAP formatter with Test::Builder about
    the formatter not supporting "no_header" and "no_diag"; this happened even
    if the alternative formatter class implemented these attributes

* Mon Sep 26 2016 Paul Howarth <paul@city-fan.org> - 1.302059-1
- Update to 1.302059
  - Documentation fixes
  - Win32 color support in Test::Builder::Tester
  - Support v-strings in is_deeply
  - A streamed subtest run inside a buffered subtest will automatically be
    converted to a buffered subtest; otherwise, the output from inside the
    subtest is lost entirely (#721)
  - Mask warning when comparing $@ in Test2::API::Context
- Drop obsoletes/provides for perl-Test-Tester and perl-Test-use-ok, which
  were integrated into this package in Fedora 22

* Tue Sep 13 2016 Paul Howarth <paul@city-fan.org> - 1.302056-1
- Update to 1.302056
  - Fix skip_all in require in intercept (#696)
  - Documentation of what is better in Test2 (#663)
  - Document Test::Builder::Tester plan limitations
  - Document limitations in is_deeply (#595)
  - Better documentation of done_testing purpose (#151)
  - Make ctx->send_event detect termination events (#707)
  - Allow '#' and '\n' in ok names
  - Fix special case of ok line ending in backslash
  - Improve a test that captures STDERR/STDOUT

* Sun Aug 14 2016 Paul Howarth <paul@city-fan.org> - 1.302052-1
- Update to 1.302052
  - Add contact info to main doc and readme
  - Fix setting hub when getting context

* Fri Jul 29 2016 Paul Howarth <paul@city-fan.org> - 1.302049-1
- Update to 1.302049
  - Add 'active' attribute to hub

* Sat Jul 23 2016 Paul Howarth <paul@city-fan.org> - 1.302047-1
- Update to 1.302047
  - Restore traditional note/diag return values (#694)

* Tue Jul 19 2016 Paul Howarth <paul@city-fan.org> - 1.302045-1
- Update to 1.302045
  - Work around IPC bug on windows
  - Fix IPC event ordering bug
  - Fix TODO in mixed T2/TB subtests
  - Fix test that segv'd on older perls

* Sun Jul 10 2016 Paul Howarth <paul@city-fan.org> - 1.302040-1
- Update to 1.302040
  - Fix broken MANIFEST.SKIP entries (#689)
  - Add Info event for better diagnostics

* Mon Jul  4 2016 Paul Howarth <paul@city-fan.org> - 1.302037-1
- Update to 1.302037
  - Restore PerlIO layer cloning on STDERR and STDOUT
- Bump obsoletes/provides versions for perl-Test2 to maintain upgrade path from
  packages in third-party repositories

* Tue Jun 28 2016 Paul Howarth <paul@city-fan.org> - 1.302035-1
- Update to 1.302035
  - Fix some breakage info
  - POD fixes

* Fri Jun 24 2016 Paul Howarth <paul@city-fan.org> - 1.302033-1
- Update to 1.302033
  - Fix nested TODO handling of diags (#684)

* Wed Jun 22 2016 Paul Howarth <paul@city-fan.org> - 1.302031-1
- Update to 1.302031
  - Remove Carp from dependency list (#682)

* Sun Jun 19 2016 Paul Howarth <paul@city-fan.org> - 1.302030-1
- Update to 1.302030
  - Use pre_filter instead of filter for TODO in Test::Builder (fix #683)
  - Fix typos in transitions doc (#681)
  - Add 'inherit_trace' param to run_subtest
  - Properly skip thread test when threads are broken

* Tue Jun 14 2016 Paul Howarth <paul@city-fan.org> - 1.302026-1
- Update to 1.302026
  - Do not fail if Test2::API::Breakage cannot load (rare 5.10.0 issue)
  - Potential fix for t/Legacy/Regression/637.t
  - Make t/Legacy/Regression/637.t AUTHOR_TESTING for now
  - Add Generic event type
  - Make sure enabling culling/shm sets pid and tid (fix #679)

* Sun May 29 2016 Paul Howarth <paul@city-fan.org> - 1.302022-1
- Update to 1.302022
  - Many micro-optimizations
  - Spelling fixes and tests
  - Fix leaky File.t file so that tmp doesn't fill up
  - Move some modules out of the known broken list in xt tests
  - Add Test2-based tools to downstream testing
  - Change when PID/TID are stashed (for forkprove)
  - VMS fixes for Files.t and IPC system
  - Improve thread checks to better detect broken 5.10 builds
  - Use thread checks to skip/run t/Legacy/Regression/637.t

* Mon May 23 2016 Petr Pisar <ppisar@redhat.com> - 1.302019-2
- Obsolete perl-Test2-0.000044-2 too

* Thu May 19 2016 Paul Howarth <paul@city-fan.org> - 1.302019-1
- Update to 1.302019
  - Block signals in critical IPC section (fix #661 and #668)
  - Merge Examples and examples into one dir (#660)
  - Documentation and typo fixes
  - Make Test2::Util::get_tid have a consistent prototype (#665)
  - Make TB->no_plan a no-op if a plan is set
  - Fix util.t win32 bug
  - Handle Test::Builder::Exception properly
  - Silence noisy STDERR in test suite
  - POD spelling fixes
- BR: perl-generators

* Wed May 18 2016 Paul Howarth <paul@city-fan.org> - 1.302015-1
- Update to 1.302015
  - Major refactoring of existing API on top of (included) Test2
- Obsolete/Provide perl-Test2

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.001014-365
- Increase release to favour standalone package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.001014-347
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.001014-346
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.001014-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.001014-3
- Perl 5.22 rebuild

* Wed Mar 04 2015 Petr Šabata <contyk@redhat.com> - 1.001014-2
- Correct the license tag

* Wed Jan  7 2015 Paul Howarth <paul@city-fan.org> - 1.001014-1
- Update to 1.001014
  - Fix a unit test that broke on some platforms with spaces in the $^X path
  - Add a test to ensure that the Changes file is updated

* Wed Dec 24 2014 Paul Howarth <paul@city-fan.org> - 1.001012-1
- Update to 1.001012
  - Move test that was dropped in the wrong directory

* Tue Dec 23 2014 Paul Howarth <paul@city-fan.org> - 1.001011-1
- Update to 1.001011
  - Fix windows test bug (GH#491)
  - Integrate Test::Tester and Test::use::ok for easier downgrade from trial
  - Remove POD Coverage test
- Obsolete/Provide perl-Test-Tester and perl-Test-use-ok
- Classify buildreqs by usage
- Use features from recent ExtUtils::MakeMaker to simplify spec
- Run tests with AUTHOR_TESTING=1 so we do the threads test too

* Tue Nov  4 2014 Paul Howarth <paul@city-fan.org> - 1.001009-1
- Update to 1.001009
  - Backport cmp_ok fix from alphas (GH#478)

* Thu Oct 16 2014 Paul Howarth <paul@city-fan.org> - 1.001008-1
- Update to 1.001008
  - Fix subtest name when skip_all is used

* Tue Sep  9 2014 Paul Howarth <paul@city-fan.org> - 1.001006-1
- Update to 1.001006
  - Documentation updates
  - Subtests accept args
  - Outdent subtest diag
  - Changed install path for perl 5.12 or higher

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.001003-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.001003-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 22 2014 Paul Howarth <paul@city-fan.org> - 1.001003-1
- Update to 1.001003
  - Documentation updates for maintainer change
- This release by EXODIST -> update source URL
- Drop obsoletes/provides for old tests sub-package

* Tue Nov  5 2013 Paul Howarth <paul@city-fan.org> - 1.001002-1
- Update to 1.001002
  - Restore ability to use regex with test_err and test_out (CPAN RT#89655)
- Drop upstreamed regex patch

* Sat Oct 12 2013 Paul Howarth <paul@city-fan.org> - 0.99-1
- 0.99 bump
- This release by RJBS -> update source URL

* Fri Aug 09 2013 Petr Pisar <ppisar@redhat.com> - 0.98.05-3
- Pass regular expression intact

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 0.98.05-1
- 0.98_05 bump

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 0.98-244
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98-243
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 21 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.98-242
- Update dependencies and comments

* Thu Aug 23 2012 Paul Howarth <paul@city-fan.org> - 0.98-241
- Merge tests sub-package back into main package
- Don't need to remove empty directories from the buildroot
- Drop %%defattr, redundant since rpm 4.4
- Make %%files list more explicit
- Don't use macros for commands
- Mark Tutorial.pod as %%doc
- Drop explicit dependency on perl-devel

* Mon Aug 13 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.98-240
- Bump release to override sub-package from perl.spec

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 0.98-6
- Perl 5.16 rebuild

* Thu May 31 2012 Petr Pisar <ppisar@redhat.com> - 0.98-5
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.98-3
- Change path on vendor, so our debuginfo are not conflicting with
  perl core debuginfos

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.98-2
- Perl mass rebuild

* Thu Feb 24 2011 Iain Arnell <iarnell@gmail.com> - 0.98-1
- Update to latest upstream version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.96-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Nov 20 2010 Iain Arnell <iarnell@gmail.com> - 0.96-1
- Update to latest upstream version
- Clean up spec for modern rpmbuild

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.94-2
- Mass rebuild with perl-5.12.0

* Tue Mar 16 2010 Chris Weyl <cweyl@alumni.drew.edu> - 0.94-1
- Specfile by Fedora::App::MaintainerTools 0.006
