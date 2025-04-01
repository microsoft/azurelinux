## START: Set by rpmautospec
## (rpmautospec version 0.7.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 1;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

Name:           python-zmq
Version:        25.1.2
Release:        %autorelease
Summary:        Python bindings for zeromq

# As noted in https://github.com/zeromq/pyzmq/blob/v26.2.0/RELICENSE/README.md:
#   pyzmq starting with 26.0.0 is fully licensed under the 3-clause Modified
#   BSD License. A small part of the core (Cython backend only) was previously
#   licensed under LGPLv3 for historical reasons. Permission has been granted
#   by the contributors of the vast majority of those components to relicense
#   under MPLv2 or BSD. This backend has been completely replaced in pyzmq 26,
#   and the new implementation is fully licensed under BSD-3-Clause, so pyzmq
#   is now under a single license.
# Since this package is currently at 25.1.2, the entire source is BSD-3-Clause
# (LICENSE.BSD), except:
#   - Some core files (the low-level Cython bindings) are LGPL-3.0-or-later
#     (LICENSE.LESSER); based on comments in file headers, this is just
#     zmq/backend/cython/_device.pyx.
#   - zmq/ssh/forward.py, which is derived from a Paramiko demo, is
#     LGPL-2.1-or-later
#   - zmq/eventloop/zmqstream.py is Apache-2.0
# Additionally, the following do not affect the license of the binary RPMs:
#   - tools/run_with_env.cmd is CC0-1.0; for distribution in the source RPM, it
#     is covered by “Existing uses of CC0-1.0 on code files in Fedora packages
#     prior to 2022-08-01, and subsequent upstream versions of those files in
#     those packages, continue to be allowed. We encourage Fedora package
#     maintainers to ask upstreams to relicense such files.”
#     https://gitlab.com/fedora/legal/fedora-license-data/-/issues/91#note_1151947383
#   - examples/device/device.py and examples/win32-interrupt/display.py are
#     LicenseRef-Fedora-Public-Domain; approved in “Review of
#     python-zmq examples dedicated to the public domain,”
#     https://gitlab.com/fedora/legal/fedora-license-data/-/issues/616; see
#     https://gitlab.com/fedora/legal/fedora-license-data/-/merge_requests/716
License:        %{shrink:
                BSD-3-Clause AND
                LGPL-3.0-or-later AND
                LGPL-2.1-or-later AND
                Apache-2.0
                }
URL:            https://zeromq.org/languages/python/
%global forgeurl https://github.com/zeromq/pyzmq
Source0:        %{forgeurl}/archive/v%{version}/pyzmq-%{version}.tar.gz
# BUG: A file is licensed Apache-2.0, but the license text is not distributed
# https://github.com/zeromq/pyzmq/issues/2048
Source1:        https://www.apache.org/licenses/LICENSE-2.0.txt#/LICENSE.Apache-2.0

# Python 3.13 compatibility
Patch:          %{forgeurl}/pull/1961.patch

BuildRequires:  gcc
BuildRequires:  pkgconfig(libzmq)
BuildRequires:  python3-devel

%global common_description %{expand:
This package contains Python bindings for ZeroMQ. ØMQ is a lightweight and fast
messaging implementation.}

%description %{common_description}


%package -n python3-pyzmq
Summary:        %{summary}

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_provides_for_importable_modules
%py_provides    python3-zmq

# Beginning with Fedora 42, the binary packages are renamed from
# python3-zmq/python3-zmq-tests to python3-pyzmq/python3-pyzmq-tests to match
# the canonical package name. Ideally, the source package would also be called
# python-pyzmq, but it’s not worth going through the package renaming process
# for this. The Obsoletes/Conflicts provide a clean upgrade path, and can be
# removed after Fedora 44 end-of-life.
Obsoletes:      python3-zmq < 25.1.1-29
Conflicts:      python3-zmq < 25.1.1-29

%description -n python3-pyzmq %{common_description}


%package -n python3-pyzmq-tests
Summary:        %{summary}, testsuite
# This subpackage does not contain any of the files that are under other
# licenses; see the comment above the main License tag.
License:        BSD-3-Clause

Requires:       python3-pyzmq%{?_isa} = %{version}-%{release}

# See notes about binary package renaming in the python3-pyzmq subpackage.
%py_provides    python3-zmq-tests
Obsoletes:      python3-zmq-tests < 25.1.1-29
Conflicts:      python3-zmq-tests < 25.1.1-29

# Based on test-requirements.txt; see test-requirement-filtered.txt, as
# generated in %%prep. The BR’s duplicate the generated ones, which is
# unfortunate, but necessary to make sure that we don’t have unsatisfied
# runtime/install-time dependencies. It would be better if we didn’t have to
# ship the tests at all – maybe we don’t?
BuildRequires:  %{py3_dist cython}
Requires:       %{py3_dist cython}
BuildRequires:  %{py3_dist pymongo}
Requires:       %{py3_dist pymongo}
BuildRequires:  %{py3_dist pytest}
Requires:       %{py3_dist pytest}
BuildRequires:  %{py3_dist pytest-asyncio}
Requires:       %{py3_dist pytest-asyncio}
BuildRequires:  %{py3_dist setuptools}
Requires:       %{py3_dist setuptools}
BuildRequires:  %{py3_dist tornado}
Requires:       %{py3_dist tornado}

# Add some manual test dependencies that aren’t in test-requirements.txt, but
# which enable additional tests.
#
# Tests in zmq/tests/mypy.py require mypy, but see:
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters
#
# Some tests in zmq/tests/test_context.py and zmq/tests/test_socket.py require
# pyczmq, which is not packaged and has not been updated in a decade.
#
# Enable more tests in zmq/tests/test_message.py:
BuildRequires:  %{py3_dist numpy}
Recommends:     %{py3_dist numpy}

%description -n python3-pyzmq-tests %{common_description}

This package contains the test suite for the Python bindings.


%prep
%autosetup -p1 -n pyzmq-%{version}

# Remove any Cython-generated .c files in order to regenerate them:
find zmq -name '*.c' -print -delete

# Remove shebangs from non-script sources. The find-then-modify pattern
# preserves mtimes on sources that did not need to be modified.
find 'src' -type f -name '*.py' \
    -exec gawk '/^#!/ { print FILENAME }; { nextfile }' '{}' '+' |
  xargs -r sed -r -i '1{/^#!/d}'

# BUG: A file is licensed Apache-2.0, but the license text is not distributed
# https://github.com/zeromq/pyzmq/issues/2048
cp -p '%{SOURCE1}' .

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters
sed -r \
    -e 's/^(black|codecov|coverage|flake8|mypy|pytest-cov)\b/# &/' \
    test-requirements.txt | tee test-requirements-filtered.txt


%generate_buildrequires
%pyproject_buildrequires test-requirements-filtered.txt


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l zmq


%check
# to avoid partially initialized zmq module from cwd
mkdir -p _empty
cd _empty
ln -s %{buildroot}%{python3_sitearch}/zmq/ ../pytest.ini ./

# test_draft seems to get incorrectly run:
# https://github.com/zeromq/pyzmq/issues/1853
k="${k-}${k+ and }not test_draft"

%ifarch ppc64le
# These crash on Python 3.12; TODO: investigate
k="${k-}${k+ and }not test_green_device"
k="${k-}${k+ and }not (Green and (test_raw or test_timeout or test_poll))"
%endif

%pytest --maxfail 2 -k "${k-}" -v -rs zmq/tests


%files -n python3-pyzmq -f %{pyproject_files}
%doc README.md
%exclude %{python3_sitearch}/zmq/tests/


%files -n python3-pyzmq-tests
%{python3_sitearch}/zmq/tests/


%changelog
## START: Generated by rpmautospec
* Mon Nov 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.1.2-1
- Update to 25.1.2

* Mon Nov 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.1.1-32
- Fix the Source0 URL
- Previously, the source RPM contained the GitHub archive, but `Source0`
  referenced the PyPI sdist.

* Mon Nov 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.1.1-31
- Update comment about LicenseRef-Fedora-Public-Domain

* Mon Nov 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.1.1-30
- Make the dependency on python3-pyzmq from python3-pyzmq-tests arch-
  specific

* Mon Nov 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.1.1-29
- Rename binary subpackages python3-zmq(-tests) to python3-pyzmq(-tests)

* Mon Nov 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.1.1-28
- Fix test dependencies added to python3-zmq instead of python3-zmq-tests

* Mon Nov 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.1.1-27
- Add dependencies to enable a few more tests

* Mon Nov 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.1.1-25
- Drop manual test dependency on gevent
- Upstream only wants it for Python 3.10 and older now.

* Mon Nov 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.1.1-24
- Fix subpackage License fields

* Mon Nov 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.1.1-23
- Try to add appropriate dependencies to python3-zmq-tests

* Mon Nov 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.1.1-22
- Print reasons for skipped tests

* Mon Nov 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.1.1-21
- Re-run failing tests once, as upstream does

* Mon Nov 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.1.1-20
- Generate dependencies for testing

* Mon Nov 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.1.1-19
- Tidy up obsolete workarounds in %%prep

* Mon Nov 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.1.1-18
- Assert that .dist-info contains at leas one license file

* Mon Nov 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.1.1-16
- Write test skips one per line; respect pytest.ini

* Sun Nov 24 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.1.1-15
- Use simplified Summary and description from upstream

* Sun Nov 24 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.1.1-14
- Correct License and update to SPDX
- Ship an Apache-2.0 license file, and report its absence upstream

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 25.1.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 25.1.1-11
- Rebuilt for Python 3.13

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 25.1.1-10
- Bootstrap for Python 3.13

* Sat Apr 13 2024 Miroslav Suchý <msuchy@redhat.com> - 25.1.1-9
- convert MPLv2.0 license to SPDX

* Tue Mar 12 2024 Miro Hrončok <miro@hroncok.cz> - 25.1.1-8
- Python 3.13 compatibility

* Sun Feb 18 2024 Orion Poplawski <orion@nwra.com> - 25.1.1-6
- Ignore test_draft failures

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 25.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 25.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Oct 22 2023 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 25.1.1-3
- Fixed the ZeroMQ dependency

* Sun Oct 22 2023 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 25.1.1-2
- Upstream upgrade to v25.1.1

* Sun Oct 22 2023 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 25.1.1-1
- Build for ZeroMQ 4.3.5

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 25.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 28 2023 Miro Hrončok <miro@hroncok.cz> - 25.1.0-2
- Temporarily deselect tests crashing on ppc64le to unblock the Py3.12
  rebuild

* Wed Jun 28 2023 Orion Poplawski <orion@nwra.com> - 25.1.0-1
- Update to 25.1.0

* Thu Jun 22 2023 Python Maint <python-maint@redhat.com> - 24.0.1-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 24.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Jan 08 2023 Kevin Fenzi <kevin@scrye.com> - 24.0.1-1
- Update to 24.0.1. Fixes rhbz#2128693

* Sun Sep 18 2022 Kevin Fenzi <kevin@scrye.com> - 24.0.0-1
- Update to 24.0.0. Fixes rhbz#2127189

* Wed Aug 03 2022 Miro Hrončok <miro@hroncok.cz> - 23.2.0-3
- Remove old cruft

* Wed Aug 03 2022 Miro Hrončok <miro@hroncok.cz> - 23.2.0-2
- Run the tests

* Wed Aug 03 2022 Charalampos Stratakis <cstratak@redhat.com> - 23.2.0-1
- Update to 23.2.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 22.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 22.3.0-3
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 22.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Jan 09 2022 Kevin Fenzi <kevin@scrye.com> - 22.3.0-1
- Update to 22.3.0. Fixes rhbz#2004837

* Sun Aug 08 2021 Kevin Fenzi <kevin@scrye.com> - 22.2.1-1
- Update to 22.2.1. Fixes rhbz#1989975

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 22.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 22.0.3-2
- Rebuilt for Python 3.10

* Sat Feb 13 2021 Kevin Fenzi <kevin@scrye.com> - 22.0.3-1
- Update to 22.0.3. Fixes rhbz#1928104

* Wed Feb 03 2021 Kevin Fenzi <kevin@scrye.com> - 22.0.2-1
- Update to 22.0.2. Fixes rhbz#1922110

* Fri Jan 29 2021 Kevin Fenzi <kevin@scrye.com> - 21.0.2-1
- Update to 21.0.2. Fixes rhbz#1920351

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 21.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 16 2021 Kevin Fenzi <kevin@scrye.com> - 21.0.0-1
- Update to 21.0.0. Fixes rhbz#1916136

* Fri Jan 01 2021 Kevin Fenzi <kevin@scrye.com> - 20.0.0-1
- Update to 20.0.0. Fixes rhbz#1832893

* Tue Nov 24 2020 Joel Capitao <jcapitao@redhat.com> - 19.0.2-1
- Update to 19.0.2

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 19.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <miro@hroncok.cz> - 19.0.0-2
- Rebuilt for Python 3.9

* Sat Apr 04 2020 Carl George <carl@george.computer> - 19.0.0-1
- Update to 19.0.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 18.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 14 2020 Jochen Breuer <brejoc@gmail.com> - 18.1.0-3
- Adding python-pyzqm in provides

* Fri Nov 29 2019 Miro Hrončok <miro@hroncok.cz> - 18.1.0-2
- Subpackages python2-zmq, python2-zmq-test have been removed

* Sun Oct 06 2019 Kevin Fenzi <kevin@scrye.com> - 18.1.0-1
- Update to 18.1.0. Fixes bug #1742606

* Thu Oct 03 2019 Miro Hrončok <miro@hroncok.cz> - 18.0.2-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <miro@hroncok.cz> - 18.0.2-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 18.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 30 2019 Kevin Fenzi <kevin@scrye.com> - 18.0.2-1
- Update to 18.0.2. Fixes bug #1724706

* Tue May 14 2019 Miro Hrončok <miro@hroncok.cz> - 18.0.1-2
- Regenerate Cython files

* Mon Apr 29 2019 Kevin Fenzi <kevin@scrye.com> - 18.0.1-1
- Update to 18.0.1. Fixes bug #1601128

* Tue Feb 12 2019 Miro Hrončok <miro@hroncok.cz> - 17.0.0-7
- https://fedoraproject.org/wiki/Changes/Python_Extension_Flags

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 17.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 17.0.0-5
- Remove obsolete Group tag

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 17.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 17.0.0-3
- add BuildRequires: gcc

* Sun Jun 17 2018 Miro Hrončok <miro@hroncok.cz> - 17.0.0-2
- Rebuilt for Python 3.7

* Sat May 12 2018 Miro Hrončok <miro@hroncok.cz> - 17.0.0-1
- Update to 17.0.0 (#1538381), fix shebangs

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 16.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Iryna Shcherbina <shcherbina.iryna@gmail.com> - 16.0.2-6
- Update Python 2 dependency declarations to new packaging standards

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 16.0.2-5
- Rebuilt for
  https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 16.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 16.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <miro@hroncok.cz> - 16.0.2-2
- Rebuild for Python 3.6

* Wed Nov 23 2016 Kevin Fenzi <kevin@scrye.com> - 16.0.2-1
- Update to 16.0.2. Fixes bug #1397615

* Sun Nov 13 2016 Thomas Spura <thomas.spura@gmail.com> - 16.0.1-1
- Update to 16.0.1
- Build twice: once for installing later and once for in-place testing:
  Testing in-place and installing conflicts (you seem to be able to do only
  one of them at the same time). Building twice seems to fix this

* Tue Jul 19 2016 Fedora Release Engineering <releng@fedoraproject.org> - 15.3.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_
  Packages

* Tue Jul 12 2016 Orion Poplawski <orion@cora.nwra.com> - 15.3.0-1
- Update to 15.3.0

* Tue Jul 12 2016 Orion Poplawski <orion@cora.nwra.com> - 14.7.0-13
- Use modern provides filtering

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 14.7.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 16 2015 Thomas Spura <thomas.spura@gmail.com> - 14.7.0-11
- Use setupegg.py for building/installing to have an unzip'ed egg

* Tue Nov 10 2015 Peter Robinson <pbrobinson@fedoraproject.org> - 14.7.0-10
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Oct 16 2015 Thomas Spura <thomas.spura@gmail.com> - 14.7.0-9
- rebuilt to pick up new obsoletes/provides

* Wed Oct 14 2015 Thomas Spura <thomas.spura@gmail.com> - 14.7.0-8
- Close %%if properly

* Wed Oct 14 2015 Thomas Spura <thomas.spura@gmail.com> - 14.7.0-7
- Disable python3 tests again as they are randomly hanging on koji

* Wed Oct 14 2015 Thomas Spura <thomas.spura@gmail.com> - 14.7.0-6
- Cleanup spec and use py_build macros

* Wed Oct 14 2015 Thomas Spura <thomas.spura@gmail.com> - 14.7.0-5
- use python_provide macro

* Tue Sep 01 2015 Ralph Bean <rbean@redhat.com> - 14.7.0-4
- Get ready to support python34 on EPEL7.

* Tue Jun 23 2015 Thomas Spura <thomas.spura@gmail.com> - 14.7.0-3
- temporarily disable python3 testsuite as it hangs on koji

* Tue Jun 23 2015 Thomas Spura <thomas.spura@gmail.com> - 14.7.0-2
- czmq currently FTBFS, so enable it some time later

* Tue Jun 23 2015 Thomas Spura <thomas.spura@gmail.com> - 14.7.0-1
- update to 14.7.0

* Thu Jun 18 2015 Dennis Gilmore <dennis@ausil.us> - 14.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Nov 17 2014 Thomas Spura <thomas.spura@gmail.com> - 14.4.1-1
- Update to 14.4.1 and rebuild against zeromq-4

* Wed Aug 27 2014 Thomas Spura <thomas.spura@gmail.com> - 14.3.1-1
- update to 14.3.1

* Sun Aug 17 2014 Peter Robinson <pbrobinson@fedoraproject.org> - 13.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Dennis Gilmore <dennis@ausil.us> - 13.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 16 2014 Slavek Kabrda <bkabrda@redhat.com> - 13.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Aug 05 2013 Thomas Spura <thomas.spura@gmail.com> - 13.0.2-1
- Fix changelog/release from last commit

* Mon Aug 05 2013 Thomas Spura <thomas.spura@gmail.com> - 13.0.0-3
- update to new version (fixes FTBFS)

* Sun Aug 04 2013 Dennis Gilmore <dennis@ausil.us> - 13.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 20 2013 Thomas Spura <thomas.spura@gmail.com> - 13.0.0-1
- update to 13.0.0

* Thu Feb 14 2013 Dennis Gilmore <dennis@ausil.us> - 2.2.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 15 2012 Thomas Spura <thomas.spura@gmail.com> - 2.2.0.1-3
- not all *.c files may be deleted, when receneration of .c files by
  Cython/remove bundled folder explicitely

* Mon Oct 15 2012 Thomas Spura <thomas.spura@gmail.com> - 2.2.0.1-2
- Fix date in changelog

* Mon Oct 15 2012 Thomas Spura <thomas.spura@gmail.com> - 2.2.0.1-1
- update to 2.2.0.1 and move to BR zeromq3

* Sun Aug 05 2012 David Malcolm <dmalcolm@redhat.com> - 2.2.0-5
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug 03 2012 David Malcolm <dmalcolm@redhat.com> - 2.2.0-4
- force regeneration of .c files by Cython (needed for python 3.3 support)

* Fri Aug 03 2012 David Malcolm <dmalcolm@redhat.com> - 2.2.0-3
- remove rhel logic from with_python3 conditional

* Sat Jul 21 2012 Dennis Gilmore <dennis@ausil.us> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 26 2012 Thomas Spura <thomas.spura@gmail.com> - 2.2.0-1
- update to 2.2.0

* Wed Mar 07 2012 Thomas Spura <thomas.spura@gmail.com> - 2.1.11-1
- update to new version

* Sat Jan 14 2012 Dennis Gilmore <dennis@ausil.us> - 2.1.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 14 2011 Thomas Spura <thomas.spura@gmail.com> - 2.1.9-5
- tests package requires main package - filter python3 libs

* Thu Dec 08 2011 Thomas Spura <thomas.spura@gmail.com> - 2.1.9-4
- don't include tests twice

* Thu Dec 08 2011 Thomas Spura <thomas.spura@gmail.com> - 2.1.9-3
- also bump the release

* Thu Dec 08 2011 Thomas Spura <thomas.spura@gmail.com> - 2.1.9-2
- use proper buildroot macro

* Wed Sep 21 2011 Thomas Spura <thomas.spura@gmail.com> - 2.1.9-1
- update to new version - run testsuite on python3

* Sun Jul 31 2011 Thomas Spura <thomas.spura@gmail.com> - 2.1.4-4
- don't delete the tests, needed by ipython-tests on runtime - don't use
  _sourcedir macro

* Wed Apr 06 2011 Thomas Spura <tomspur@fedoraproject.org> - 2.1.4-3
- upload buildutils, fetched from upstream git repo

* Wed Apr 06 2011 Thomas Spura <tomspur@fedoraproject.org> - 2.1.4-2
- also upload new sources

* Wed Apr 06 2011 Thomas Spura <tomspur@fedoraproject.org> - 2.1.4-1
- update to new version 2.1.4 (#690199)

* Wed Mar 23 2011 Thomas Spura <tomspur@fedoraproject.org> - 2.1.1-1
- update to new version

* Wed Feb 09 2011 Dennis Gilmore <dennis@ausil.us> - 2.0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 30 2011 Thomas Spura <tomspur@fedoraproject.org> - 2.0.10.1-1
- update to new version (fixes memory leak) - no need to run 2to3 on
  python3 subpackage

* Tue Jan 18 2011 Thomas Spura <tomspur@fedoraproject.org> - 2.0.10-1
- update to new version - remove patch (is upstream) - run tests
  differently

* Thu Dec 30 2010 David Malcolm <dmalcolm@redhat.com> - 2.0.8-3
- rebuild for newer python3

* Thu Sep 23 2010 Thomas Spura <tomspur@fedoraproject.org> - 2.0.8-2
- forgot to upload the new sources

* Thu Sep 23 2010 Thomas Spura <tomspur@fedoraproject.org> - 2.0.8-1
- update to new version to be comply with zeromq

* Sun Aug 22 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.1.20100725git18f5d06-2
- rebuild with python3.2
  http://lists.fedoraproject.org/pipermail/devel/2010-August/141368.html

* Mon Aug 16 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.1.20100725git18f5d06-1
- initial import (#603245)
## END: Generated by rpmautospec
