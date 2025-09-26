%global srcname simpleline

Name: 		python-%{srcname}
Summary: 	A Python library for creating text UI
Url: 		https://github.com/rhinstaller/python-%{srcname}
Version: 	1.9.0
Release: 	13%{?dist}
# This tarball was created from upstream git:
#   git clone https://github.com/rhinstaller/python-simpleline
#   cd python-simpleline && make archive
Source0: 	https://github.com/rhinstaller/python-%{srcname}/releases/download/%{version}/%{srcname}-%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Adding patch for missing po files, as a tarball without po files has been uploaded to blobstore.
Patch0:         0001-missing-po-files.patch
License: 	LGPL-3.0-or-later
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
BuildArch: 	noarch
BuildRequires: 	make
BuildRequires: 	python3-devel
BuildRequires: 	gettext
BuildRequires: 	python3-setuptools
BuildRequires: 	intltool
BuildRequires: 	python3-gobject-base

%description
Simpleline is a Python library for creating text UI.
It is designed to be used with line-based machines
and tools (e.g. serial console) so that every new line
is appended to the bottom of the screen.
Printed lines are never rewritten!


%package -n python3-%{srcname}
Summary: A Python3 library for creating text UI
Requires: 	rpm-python3

%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
Simpleline is a Python3 library for creating text UI.
It is designed to be used with line-based machines
and tools (e.g. serial console) so that every new line
is appended to the bottom of the screen.
Printed lines are never rewritten!

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%make_build

%install
make DESTDIR=%{buildroot} install
%find_lang python-%{srcname}

%check
make test

%files -n python3-%{srcname} -f python-%{srcname}.lang
%license LICENSE.md
%doc README.md
%{python3_sitelib}/*

%changelog
* Fri Dec 20 2024 Akhila Guruju <v-guakhila@microsoft.com> - 1.9.0-13
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.9.0-11
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 1.9.0-7
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 19 2022 Jiri Konecny <jkonecny@redhat.com> - 1.9.0-5
- Migrate to SPDX license: https://fedoraproject.org/wiki/Changes/SPDX_Licenses_Phase_1#Detailed_Description

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.9.0-3
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Oct 11 2021 Packit Service <user-cont-team+packit-service@redhat.com> - 1.9.0-1
- New version - 1.9.0 (Jiri Konecny)
- Adapt Makefile bumpver target for x.y.z versioning (Jiri Konecny)
- Add tests for UIScreen wide disabling of concurrency check (Jiri Konecny)
- Rename helper test classes to have Mock postfix (Jiri Konecny)
- Call App.initialize() in the setUp phase of GlobalConfiguration test (Jiri Konecny)
- Abstract registering signal handler in the InputHandler constructor (Jiri Konecny)
- Allow to disable concurrency check for all UIScreen inputs (Jiri Konecny)
- Use {} and [] instead of dict() and list() (Jiri Konecny)
- Specify encoding for open() (Jiri Konecny)
- Remove 'u' prefix from strings (Jiri Konecny)

* Tue Aug 31 2021 Jiri Konecny <jkonecny@redhat.com> - 1.8.2-1
- New version - 1.8.2 (Jiri Konecny)
- Remove changelog from the upstream spec file (Jiri Konecny)
- Fix spec file archive link (Jiri Konecny)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.8-2
- Rebuilt for Python 3.10

* Mon Feb 22 2021 Packit Service <user-cont-team+packit-service@redhat.com> - 1.8-1
- New version - 1.8 (Jiri Konecny)
- Add missing make command to spec file (Jiri Konecny)
- Don't translate the prompt keys (Vendula Poncova)
- Enable daily build for Anaconda-devel COPR repository (Jiri Konecny)
- Use Fedora container registry instead of Dockerhub (Jiri Konecny)
- Migrate COPR daily COPR builds to Packit (Jiri Konecny)
- Test build on Fedora ELN (Jiri Konecny)
- Remove packit get-current-action (Jiri Konecny)
- Run tests in GitHub workflow (Martin Pitt)
- Fix raise-missing-from (W0707) pylint warnings (Martin Pitt)
- Fix pylint to check test code correctly (Jiri Konecny)
- Use script to run unit tests (Jiri Konecny)
- Use relative imports in tests (Jiri Konecny)
- Change directory structure of unit tests (Jiri Konecny)
- Fix documentation of _process_screen method (Jiri Konecny)
- Fix pylint issues (Jiri Konecny)
- Use pylint instead of pocketlint (Jiri Konecny)
- Add coverage support (Jiri Konecny)
- Make link to exmples directory in Readme (Jiri Konecny)
- Fix homepage of the project in setup.py (Jiri Konecny)
- Fix classifiers in setup.py (Jiri Konecny)
- Add pypi-upload to Makefile (Jiri Konecny)
- Use correct variant of the field (Jiri Konecny)
- Propose Fedora update only to Fedora in development (Jiri Konecny)
- Add upstream tag template to packit for releasing (Jiri Konecny)
- Packit will download archive from Source0 if needed (Jiri Konecny)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jiri Konecny <jkonecny@redhat.com> - 1.7-1
- new upstream release: 1.7

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 1.6-4
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.6-2
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Thu Aug 22 2019 Jiri Konecny <jkonecny@redhat.com> - 1.6-1
- Always close the password dialog (vponcova)
- Remove unnecessary pass statements (jkonecny)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 1.5-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 13 2019 Jiri Konecny <jkonecny@redhat.com> - 1.5-1
- Update spec file from the downstream (jkonecny)
- Fix translation issue for lt language (jkonecny)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 19 2018 Jiri Konecny <jkonecny@redhat.com> - 1.4-1
- Fix and add tests for the new changes (#1646568) (jkonecny)
- Add should_run_with_empty_stack configuration (#1646568) (jkonecny)
- Remove wrong line in password_function conf (jkonecny)
- Tweak date lang settings in make bumpver command (jkonecny)
- Drop python-pocketlint build dependency (jkonecny)
- Update spec file from Fedora (jkonecny)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 1.3-4
- Rebuilt for Python 3.7

* Wed Jun 20 2018 Jiri Konecny <jkonecny@redhat.com> - 1.3-3
- Drop python-pocketlint dependency

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 1.3-2
- Rebuilt for Python 3.7

* Mon Jun 11 2018 Jiri Konecny <jkonecny@redhat.com> - 1.3-1
- Fix pylint errors raised by new pylint version (jkonecny)
- Setup logging handler properly for a library (jkonecny)

* Tue May 29 2018 Jiri Konecny <jkonecny@redhat.com> - 1.2-1
- Document GlobalConfiguration class (jkonecny)
- Add advanced input processing section to docs (jkonecny)
- Make makefile zanata check more robust (jkonecny)
- Add missing newline characters at the end (jkonecny)
- Abstract widget buffer extensions (jkonecny)
- Use python 3 sphinx module (jkonecny)

* Tue Apr 10 2018 Jiri Konecny <jkonecny@redhat.com> - 1.1-1
- Add global configuration initialize test (jkonecny)
- Use default password function from GlobalConfiguration (jkonecny)
- Add tests for GlobalConfiguration class (jkonecny)
- Move default width to GlobalConfiguration class (jkonecny)
- Add GlobalConfiguration object (jkonecny)
- Fix a missing article in docs. (jkonecny)
- Add tests for UIScreen get_user_input method (jkonecny)
- Only InputManager is used to get input in UIScreen (jkonecny)
- Move emit of InputReadySignal to InputRequest (jkonecny)
- Get only last input on concurrent input (jkonecny)
- Add concurrency tests for InputHandler (jkonecny)
- Add requester source to the InputHandler (#1557472) (jkonecny)
- Use InputManager as screen helper not in ScreenScheduler (#1557472) (jkonecny)
- Add test to check InputThreadManager after initialization (jkonecny)
- Reinitialize InputThreadManager when app is initialized (jkonecny)
- Input requests are now handled by InputThreadManager (jkonecny)
- Remove io_manager property from ScreenScheduler (jkonecny)
- Rename io_manager to input_manager (jkonecny)
- Change IOManager to InputManager (jkonecny)
- Move draw from IOManager to ScreenScheduler (jkonecny)
- Separate password input to PasswordInputHandler (jkonecny)
- Add DEFAULT_WIDTH constant (jkonecny)
- Add tests for InputHandler (jkonecny)
- Replace get_input_without_check by new property (jkonecny)
- Separate input to a new module (jkonecny)

* Wed Feb 28 2018 Jiri Konecny <jkonecny@redhat.com> - 1.0-1
- Fix docs based on the new PROCESSED feature (jkonecny)
- Use new PROCESS_AND* in examples (jkonecny)
- Add tests for PROCESSED_AND_{CLOSE|REDRAW} (jkonecny)
- Use new PROCESSED_AND_{CLOSE|REDRAW} in advanced widgets (jkonecny)
- Support PROCESSED_AND_CLOSE UserInputState (jkonecny)
- Rename UserInputResult to UserInputAction (jkonecny)
- Support PROCESSED_AND_REDRAW (jkonecny)
- Fix link to the documentation in README (jkonecny)
- Add link to the documentation (jkonecny)
- Write documentation for Simpleline (jkonecny)
- Disable pylint error for doc copyright variable (jkonecny)
- Add new example used in the documentation (jkonecny)
- Mock modules for readthedocs (jkonecny)
- Do a small fixes to improve documentation (jkonecny)
- Get version from the spec file (jkonecny)
- Add documentation skeleton (jkonecny)

* Thu Oct 19 2017 Jiri Konecny <jkonecny@redhat.com> - 0.8-1
- Test clean-up (jkonecny)
- Move and rename force_quit loop (jkonecny)
- Add dump screen stack method (jkonecny)

* Tue Oct 17 2017 Jiri Konecny <jkonecny@redhat.com> - 0.7-1
- Fix crash when container callback is not set (jkonecny)
- Add EntryWidget to show item title and value (jkonecny)
- Add GetPasswordInputScreen for getting passwords (jkonecny)
- UIScreen can have hidden input (jkonecny)
- Move getpass func inside locks (jkonecny)
- Implement GetInputScreen (jkonecny)
- Do not print new line with empty container (jkonecny)
- Add no_separator to UIScreen (jkonecny)
- Fix HelpScreen title (jkonecny)
- Remove original classes from GLib tests (jkonecny)
- Fix test case name (jkonecny)
- Move tests to subfolder (jkonecny)
- Move base widgets as second example (jkonecny)
- Add example with basic widgets usage (jkonecny)
- Improve README.md (jkonecny)
- Improve example starting script (jkonecny)
- Add glib loop example (jkonecny)
- Add prefixes to examples to impress difficulty (jkonecny)
- Add comments to the examples (jkonecny)
- Update examples to use new features (jkonecny)

* Fri Sep 08 2017 Jiri Konecny <jkonecny@redhat.com> - 0.6-1
- Implement the force quit all loops feature (jkonecny)
- Improved GLib event loop testing (jkonecny)
- Handle GLib event loop exceptions better (jkonecny)
- Support for GLib event loop (jkonecny)
- Wrap exceptions from handlers as ExceptionSignal (jkonecny)
- Only highest priority events are processed in one iteration (jkonecny)
- Move parts from MainLoop to AbstractEventLoop (jkonecny)
- MainLoop won't wait in busy loop anymore (jkonecny)
- Don't block loop when waiting on user input (jkonecny)
- Fix user input lock (jkonecny)

* Mon Sep 04 2017 Jiri Konecny <jkonecny@redhat.com> - 0.5-1
- Fix exception in Screen input caused infinite loop (jkonecny)
- Add test if app is initialized (jkonecny)
- Redraw on first scheduled screen (#1487326) (jkonecny)
- Redraw after YesNoDialog modal window close (jkonecny)

* Fri Aug 18 2017 Jiri Konecny <jkonecny@redhat.com> - 0.4-1
- Screen scheduling is moved to ScreenHandler (jkonecny)
- Remove merge commits from changelog (jkonecny)

* Thu Aug 17 2017 Jiri Konecny <jkonecny@redhat.com> - 0.3-1
- Remove merge commits from changelog (jkonecny)
- Fix bad input processing for list containers (jkonecny)
- Rename quit callback and add args there. (jkonecny)
- Add tests for new container feature (jkonecny)
- List containers take max width if not specified (jkonecny)
- Remove leftover print in containers parsing input (jkonecny)

* Mon Aug 14 2017 Jiri Konecny <jkonecny@redhat.com> - 0.2-1
- Merge pull request #26 from jkonecny12/master-fix-ExitMainLoop-exception (jkonecny)
- Merge pull request #28 from jkonecny12/master-fix-container-callback (jkonecny)
- Fix docs for container callbacks (jkonecny)
- Merge pull request #25 from jkonecny12/master-fix-big-screen-printing (jkonecny)
- Remove missed test helper for local testing (jkonecny)
- The ExitMainLoop exception should kill whole app (jkonecny)
- Do not run an old event queue from modal screen (jkonecny)
- Merge pull request #23 from jkonecny12/master-add-possibility-to-end-loop-politely (jkonecny)
- Merge pull request #24 from jkonecny12/master-fix-compatibility (jkonecny)
- Add possibility to end loop politely (jkonecny)
- Merge pull request #22 from jkonecny12/master-add-logging (jkonecny)
- Fix printing issues for bigger screens (jkonecny)
- Set default screen height to 30 (jkonecny)
- Keep backward compatibility for UIScreen args (jkonecny)
- Add logging to the Simpleline (jkonecny)
- Merge pull request #19 from jkonecny12/master-rework-wait-on-input (jkonecny)
- Merge pull request #21 from jkonecny12/master-fix-adv-widgets (jkonecny)
- Merge pull request #20 from jkonecny12/master-move-InputState (jkonecny)
- Wait on input thread to finish (jkonecny)
- return_after don't skip signals in recursion (jkonecny)
- Add TicketMachine helper class (jkonecny)
- Return user input in the signal handler (jkonecny)
- Merge pull request #16 from jkonecny12/master-modify-exception-handling (jkonecny)
- Merge pull request #18 from jkonecny12/master-ignore-pylint-with-lock (jkonecny)
- Reflect changes in adv_widgets (jkonecny)
- Move InputState next to UIScreen (jkonecny)
- Break App's cyclic imports (jkonecny)
- Add temporal pylint-disable for with Lock (jkonecny)
- Re-raise exception only if no handler is registered (jkonecny)
- Merge pull request #15 from jkonecny12/master-thread-safe-eventqueue (jkonecny)
- Merge pull request #11 from jkonecny12/master-add-args-to-scheduler-shortcut (jkonecny)
- Make the EventQueue thread safe (jkonecny)
- Merge pull request #13 from jkonecny12/master-enhance-WindowContainer-add (jkonecny)
- Merge pull request #12 from jkonecny12/master-fix-ready-collision (jkonecny)
- Add args param to the scheduler_handler shortcuts (jkonecny)
- Fix bad param name for scheduling methods (jkonecny)
- Merge pull request #10 from jkonecny12/master-add-hidden-user-input (jkonecny)
- Merge pull request #8 from jkonecny12/master-remove-base-file (jkonecny)
- Merge pull request #9 from jkonecny12/master-remove-quit-message (jkonecny)
- Add method add_with_separator to WindowContainer (jkonecny)
- Fix `ready` property collision with Anaconda (jkonecny)
- Add hidden parameter to UIScreen get input (jkonecny)
- Remove unused quit message (jkonecny)
- Move App from base to __init__.py (jkonecny)
- Merge pull request #6 from jkonecny12/fix-make-potfile-generation (jkonecny)
- Merge pull request #7 from jkonecny12/master-fix-make-archive (jkonecny)
- Fix make archive (jkonecny)
- Fix potfile generation (jkonecny)
- Merge pull request #5 from jkonecny12/master-add-containers (jkonecny)
- Examples now using WindowContainer (jkonecny)
- Fix error when getting input directly (jkonecny)
- Add WindowContainer and use it in UIScreen (jkonecny)
- Add SeparatorWidget (jkonecny)
- Add input processing to containers (jkonecny)
- Add containers numbering (jkonecny)
- Add containers, checkbox and center widget tests (jkonecny)
- Add row and column list containers (jkonecny)
- Merge pull request #4 from jkonecny12/master-split-renderer (jkonecny)
- Fix setup.py modules (jkonecny)
- Change INPUT_PROCESSED and INPUT_DISCARDED to Enum (jkonecny)
- Rename renderer and event_loop in App class (jkonecny)
- Add scheduler_handler and rename switch_screen (jkonecny)
- Process signals when waiting on user input (jkonecny)
- Move draw screen to the InOutManager (jkonecny)
- Change UIScreen properties (jkonecny)
- Move input processing to the InOutManager class (jkonecny)
- Move SignalHandler to the screen module (jkonecny)
- Move ui_screen to the screen module (jkonecny)
- Rename Renderer to ScreenScheduler (jkonecny)
- Merge pull request #3 from jkonecny12/master-change-close-to-signal (jkonecny)
- Change separator tests to reflect close as signal (jkonecny)
- Close screen is now signal (jkonecny)
- Rename emit_draw_signal to redraw (jkonecny)
- Merge pull request #2 from jkonecny12/master-fix-modal (jkonecny)
- Add missing doc for EventQueue and ScreeStack (jkonecny)
- Add tests for event queue (jkonecny)
- Modal screens are now executing new event loop (jkonecny)
- Separator should be printed just before show_all() (jkonecny)
- Move screen scheduling tests to new file (jkonecny)
- Merge pull request #1 from jkonecny12/master-refactorization (jkonecny)
- Implement small fixes and tweaks (jkonecny)
- Move ScreenStack to render module (jkonecny)
- Add SimplelineError as base class for Exceptions (jkonecny)
- Clean up unused code and do a small tweaks (jkonecny)
- Fix pylint errors (jkonecny)
- Modify examples to reflect new changes (jkonecny)
- Add emit_draw_signal to the SignalHandler (jkonecny)
- Do not call draw when prompt is not present (jkonecny)
- Remove old INPUT_* constants (jkonecny)
- Do not redraw when input was processed (jkonecny)
- Add license to all test classes (jkonecny)
- Add new tests for render_screen, renderer, widgets (jkonecny)
- Remove hubQ (jkonecny)
- Split input from drawing (jkonecny)
- Fix rendering errors by removing _redraw variable (jkonecny)
- Replace array with priority by Signal ordering (jkonecny)
- Add tests for SignalHandler (jkonecny)
- Use SignalHandler (jkonecny)
- Add screen rendering tests (jkonecny)
- Raise exceptions instead of silently quitting (jkonecny)
- Reflect code changes in tests (jkonecny)
- Fix missing super().__init__() in Signals (jkonecny)
- Fix modal screen by removing execute_new_loop (jkonecny)
- Fail when UIScreen is not closing itself (jkonecny)
- Add constants INPUT_PROCESSED and INPUT_DISCARDED (jkonecny)
- Fix issues in Renderer and MainLoop (jkonecny)
- Use RenderScreenSignal signal for rendering (jkonecny)
- Add App.run as a shortcut to start application (jkonecny)
- Move widgets and adv_widgets to render module (jkonecny)
- Fix cosmetic bugs in widgets (jkonecny)
- Move prompt to render module (jkonecny)
- Modify ScreenStack tests to reflect UIScreen changes (jkonecny)
- Modify UIScreen to use new App class structure (jkonecny)
- Fix renderer tests after moving the Renderer class (jkonecny)
- Move renderer to separate file renderer.py (jkonecny)
- Add quit_callback to the event loop abstract class (jkonecny)
- Add tests for the App class (jkonecny)
- Change base class to singleton like class (jkonecny)
- Add tests for event loop processing (jkonecny)
- Implementation of defualt event loop and signals (jkonecny)
- Add abstract base classes for EventLoop and Event (jkonecny)
- Remove ScheduleScreen tests (jkonecny)
- Add tests for renderer (jkonecny)
- Extract renderer from App class to render directory (jkonecny)
- Add tests for new ScreenStack and ScreenData (jkonecny)
- Extract screen stack to its own object and data class (jkonecny)
- Modify comments in the spec file (jkonecny)
- Package is named python-simpleline (jkonecny)
- Fix spec file (jkonecny)
- Fix summary in the spec file (jkonecny)
- Fix names according to tagging (jkonecny)

* Fri May 5 2017 Jiri Konecny <jkonecny@redhat.com> - 0.1-3
- Modify comments in the spec file

* Thu May 4 2017 Jiri Konecny <jkonecny@redhat.com> - 0.1-2
- Drop clean section
- Drop Group, it is not needed
- Use make_build macro
- Reorder check and install sections
- Rename package to python-simpleline but rpm will be python3-simpleline

* Fri Dec 16 2016 Jiri Konecny <jkonecny@redhat.com> - 0.1-1
- Initial package
