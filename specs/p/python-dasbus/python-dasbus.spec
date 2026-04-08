# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname dasbus

Name:           python-%{srcname}
Version:        1.7
Release:        13%{?dist}
Summary:        DBus library in Python 3

License:        LGPL-2.1-or-later
URL:            https://pypi.python.org/pypi/dasbus
%if %{defined suse_version}
Source0:        %{srcname}-%{version}.tar.gz
Group:          Development/Libraries/Python
%else
Source0:        %{pypi_source}
%endif

BuildArch:      noarch

%global _description %{expand:
Dasbus is a DBus library written in Python 3, based on
GLib and inspired by pydbus. It is designed to be easy
to use and extend.}

%description %{_description}

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{defined suse_version}
BuildRequires:  fdupes
BuildRequires:  python-rpm-macros
Requires:       python3-gobject
%else
Requires:       python3-gobject-base
%endif
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %{_description}

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install
%if %{defined suse_version}
%python_expand %fdupes %{buildroot}%{python3_sitelib}
%endif

%files -n python3-%{srcname}
%license LICENSE
%doc README.md
%{python3_sitelib}/%{srcname}-*.egg-info/
%{python3_sitelib}/%{srcname}/

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.7-13
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.7-12
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.7-10
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.7-7
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.7-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 07 2022 Vendula Poncova <vponcova@redhat.com> - 1.7-1
- CI: Use dnf instead of yum to install CentOS packages (vponcova)
- Documentation: Improve the installation instruction (vponcova)
- Remove untracked files from the git repository interactively (vponcova)
- UnixFD: Document the support for Unix file descriptors (vponcova)
- Documentation: Clean up examples in the documentation (vponcova)
- Documentation: Simplify the README.md file (vponcova)
- Documentation: Fix bullet point lists (vponcova)
- Documentation: Simplify the hostname example (vponcova)
- CI: Run tests for all supported Python version (vponcova)
- UnixFD: Handle DBus signals with Unix file descriptors (vponcova)
- UnixFD: Add tests for DBus properties with Unix file descriptors (vponcova)
- UnixFD: Clean up tests of DBus calls with Unix file descriptors (vponcova)
- UnixFD: Clean up tests for swapping Unix file descriptors (vponcova)
- UnixFD: Clean up `GLibClientUnix` and `GLibServerUnix` (vponcova)
- UnixFD: Process results of client calls in the low-level library (vponcova)
- UnixFD: Move the support for Unix file descriptors to dasbus.unix (vponcova)
- CI: Always pull the latest container image (vponcova)
- CI: Disable the unhashable-member warning (vponcova)
- Revert "Don't use pylint from pip on Fedora Rawhide" (vponcova)
- UnixFD: Move the unit tests to a new file (vponcova)
- UnixFD: Manage the testing bus on set up and tear down (vponcova)
- UnixFD: Don't add arguments to the DBusTestCase.setUp method (vponcova)
- UnixFD: Create a new testing DBus interface (vponcova)
- UnixFD: Fix the indentation in unit tests (vponcova)
- Add unit tests for variants with variant types (vponcova)
- Simplify the code for replacing values of the UnixFD type (vponcova)
- Add classes for unpacking and unwrapping a variant (vponcova)
- Don't use pylint from pip on Fedora Rawhide (vponcova)
- UnixFD: Rename a parameter to server_arguments (vponcova)
- UnixFD: Revert a change in GLibClient._async_call_finish (vponcova)
- Raise TimeoutError if a DBus call times out (vponcova)
- Fix pylint tests in CentOS Stream 8 (vponcova)
- Fix the ENV instruction in Dockerfiles (vponcova)
- Fix pylint issues (vponcova)
- run forked tests using subprocess, instead of multiprocessing (wdouglass)
- use mutable list for return value in fd_test_async make fd getters more explicit (wdouglass)
- Add test case for method call only returning fd (jlyda)
- Always use call_with_unix_fd_list* to properly handle returned fds (jlyda)
- fix some lint discovered errors (wdouglass)
- seperate unixfd functionality, to better support systems that don't have them (wdouglass)
- Remove note in documentation about unsupported Unix file descriptors (wdouglass)
- Add a test for UnixFD transfer (wdouglass)
- Allow UnixFDs to be replaced and passed into Gio (wdouglass)
- Fix rpm lint warnings for OpenSUSE 15.3 (christopher.m.cantalupo)
- Extend the .coveragerc file (vponcova)
- Disable builds for Fedora ELN on commits (vponcova)
- Test Debian with Travis (vponcova)
- Test Ubuntu with Travis (vponcova)
- Test CentOS Stream 9 with Travis (vponcova)
- Use CentOS Stream 8 for testing (vponcova)
- add remove dbus object function on bus and update tests (matthewcaswell)
- properly measure coverage across multiprocess test cases (wdouglass)
- Move handle typing tests into a new class (and a new file) (wdouglass)
- Add another test for a crazy data type, fix a bug discovered via the test (wdouglass)
- Add functions for generating/consuming fdlists with variants (wdouglass)
- Provide a language argument for the code blocks (seahawk1986)
- Change the type of 'h' glib objects from 'File' to 'UnixFD' (wdouglass)
- Allow to run tests in a container (vponcova)
- Add C0209 to the ignore list for pylint (tjoslin)
- Use the latest distro in Travis CI (vponcova)
- Always update the container (vponcova)
- Document limitations of the DBus specification generator (vponcova)
* Mon May 31 2021 Vendula Poncova <vponcova@redhat.com> - 1.6-1
- Add support for SUSE packaging in spec file (christopher.m.cantalupo)
- Allow to generate multiple output arguments (vponcova)
- Support multiple output arguments (vponcova)
- Add the is_tuple_of_one function (vponcova)
- Configure the codecov tool (vponcova)
* Mon May 03 2021 Vendula Poncova <vponcova@redhat.com> - 1.5-1
- Disable builds for Fedora ELN on pull requests (vponcova)
- Provide additional info about the DBus call (vponcova)
- Run the codecov uploader from a package (vponcova)
- Switch to packit new fedora-latest alias (jkonecny)
- Add daily builds for our Fedora-devel COPR repository (jkonecny)
- Use Fedora container registry instead of Dockerhub (jkonecny)
- Migrate daily COPR builds to Packit (jkonecny)
- Switch Packit tests to copr builds instead (jkonecny)
- Enable Packit build in ELN chroot (jkonecny)
- Rename TestMessageBus class to silence pytest warning (luca)
- Fix the raise-missing-from warning (vponcova)
* Fri Jul 24 2020 Vendula Poncova <vponcova@redhat.com> - 1.4-1
- Handle all errors of the DBus call (vponcova)
- Fix tests for handling DBus errors on the server side (vponcova)
- Run packit smoke tests for all Fedora (jkonecny)
- Fix packit archive creation (jkonecny)
- Add possibility to change setup.py arguments (jkonecny)
* Wed Jun 17 2020 Vendula Poncova <vponcova@redhat.com> - 1.3-1
- Document differences between dasbus and pydbus (vponcova)
- Improve the support for interface proxies in the service identifier (vponcova)
- Improve the support for interface proxies in the message bus (vponcova)
- Test the interface proxies (vponcova)
- Make the message bus of a service identifier accessible (vponcova)
- Fix the testing environment for Fedora Rawhide (vponcova)
* Mon May 18 2020 Vendula Poncova <vponcova@redhat.com> - 1.2-1
- Replace ABC with ABCMeta (vponcova)
- Fix typing tests (vponcova)
- Run tests on the latest CentOS (vponcova)
- Install sphinx from PyPI (vponcova)
* Thu May 14 2020 Vendula Poncova <vponcova@redhat.com> - 1.1-1
- Include tests and examples in the source distribution (vponcova)
- Fix the pylint warning signature-differs (vponcova)
* Tue May 05 2020 Vendula Poncova <vponcova@redhat.com> - 1.0-1
- Fix the documentation (vponcova)
- Fix minor typos (yurchor)
- Enable Codecov (vponcova)
- Test the documentation build (vponcova)
- Extend the documentation (vponcova)
- Add configuration files for Read the Docs and Conda (vponcova)
- Fix all warnings from the generated documentation (vponcova)
* Wed Apr 08 2020 Vendula Poncova <vponcova@redhat.com> - 0.4-1
- Replace the error register with the error mapper (vponcova)
- Propagate additional arguments for the client handler factory (vponcova)
- Propagate additional arguments in the class AddressedMessageBus (vponcova)
- Generate the documentation (vponcova)
* Thu Apr 02 2020 Vendula Poncova <vponcova@redhat.com> - 0.3-1
- Remove generate_dictionary_from_data (vponcova)
- Improve some of the error messages (vponcova)
- Check the list of DBus structures to convert (vponcova)
- Add the Inspiration section to README (vponcova)
- Enable syntax highlighting in README (vponcova)
- Use the class EventLoop in README (vponcova)
- Use the --no-merges option (vponcova)
- Clean up the Makefile (vponcova)
- Add examples (vponcova)
- Add the representation of the event loop (vponcova)
- Enable copr builds and add packit config (dhodovsk)
- Extend README (vponcova)
* Mon Jan 13 2020 Vendula Poncova <vponcova@redhat.com> - 0.2-1
- Unwrap DBus values (vponcova)
- Unwrap a variant data type (vponcova)
- Add a default DBus error (vponcova)
- Use the minimal image in Travis CI (vponcova)
- Remove GLibErrorHandler (vponcova)
- Remove map_error and map_by_default (vponcova)
- Extend arguments of dbus_error (vponcova)
- Extend arguments of dbus_interface (vponcova)
- The list of callbacks in signals can be changed during emitting (vponcova)
- Don't import from mock (vponcova)
- Enable checks in Travis CI (vponcova)
- Fix too long lines (vponcova)
- Don't use wildcard imports (vponcova)
- Add the check target to the Makefile (vponcova)
- Enable Travis CI (vponcova)
- Catch logged warnings in the unit tests (vponcova)
- Add the coverage target to the Makefile (vponcova)
- Rename tests (vponcova)
- Create Makefile (vponcova)
- Create a .spec file (vponcova)
- Add requirements to the README file (vponcova)

* Thu Oct 31 2019 Vendula Poncova <vponcova@redhat.com> - 0.1-1
- Initial package
