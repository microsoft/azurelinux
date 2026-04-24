# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# test dependencies are not available on el9+
%if 0%{?fedora}
%bcond_without tests
%else
%bcond_with tests
%endif

%global modname pycurl

Name:           python-%{modname}
Version:        7.45.6
Release: 6%{?dist}
Summary:        A Python interface to libcurl

License:        curl OR LGPL-2.1-or-later
URL:            http://pycurl.io
Source0:        %{pypi_source pycurl}

# drop link-time vs. run-time TLS backend check (#1446850)
Patch1:         0001-python-pycurl-7.45.1-tls-backend.patch

BuildRequires:  gcc
BuildRequires:  libcurl-devel
BuildRequires:  libcurl-full
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%if %{with tests}
BuildRequires:  python3-flaky
BuildRequires:  python3-flask
BuildRequires:  python3-pytest
BuildRequires:  vsftpd
%endif

# During its initialization, PycURL checks that the actual libcurl version
# is not lower than the one used when PycURL was built.
# Yes, that should be handled by library versioning (which would then get
# automatically reflected by rpm).
# For now, we have to reflect that dependency.
%global libcurl_sed '/^#define LIBCURL_VERSION "/!d;s/"[^"]*$//;s/.*"//;s/-.*$//;s/$/~/;q'
%global curlver_h /usr/include/curl/curlver.h
%global libcurl_ver %(sed %{libcurl_sed} %{curlver_h} 2>/dev/null || echo 0)

%global _description %{expand:
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.}

%description %_description

%package -n python3-%{modname}
Summary:        %{summary}
Requires:       libcurl%{?_isa} >= %{libcurl_ver}

%description -n python3-%{modname} %_description

%prep
%autosetup -n %{modname}-%{version} -p1

# use %%{python3} instead of python to invoke tests
sed -e 's|python |%{python3} |' -i tests/ext/test-suite.sh
%py3_shebang_fix tests/*.py setup.py

%build
%py3_build -- --with-openssl

%install
export PYCURL_SSL_LIBRARY=openssl
%py3_install
rm -rf %{buildroot}%{_datadir}/doc/pycurl

%if %{with tests}
%check
# relax crypto policy for the test-suite to make it pass again (#1863711)
export OPENSSL_SYSTEM_CIPHERS_OVERRIDE=XXX
export OPENSSL_CONF=

export PYTHONPATH=%{buildroot}%{python3_sitearch}
export PYCURL_SSL_LIBRARY=openssl
export PYCURL_VSFTPD_PATH=vsftpd

# disable test_http_version_3 since curl in Fedora does not support it (#2175216)
# disable tests incompatible with curl 8.4.0 and newer
export PYTEST_ADDOPTS="--ignore examples -m 'not online'"
%py3_test_envvars make test PYTHON='%{python3}' PYTEST="%{__pytest}" PYFLAKES=true
%endif

%files -n python3-%{modname}
%license COPYING-LGPL COPYING-MIT
%doc ChangeLog README.rst examples doc
%{python3_sitearch}/curl/
%{python3_sitearch}/%{modname}.*.so
%{python3_sitearch}/%{modname}-%{version}-*.egg-info

%changelog
* Fri Oct 03 2025 Jacek Migacz <jmigacz@redhat.com> - 7.45.6-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 7.45.6-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.45.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 7.45.6-2
- Rebuilt for Python 3.14

* Mon Apr 07 2025 Jacek Migacz <jmigacz@redhat.com> - 7.45.6-1
- Update to 7.45.6 (#2350521)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.45.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 13 2024 Lukáš Zaoral <lzaoral@redhat.com> - 7.45.4-1
- Update to 7.45.4 (#2332217)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.45.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 7.45.3-3
- Rebuilt for Python 3.13

* Wed Apr 24 2024 Miro Hrončok <mhroncok@redhat.com> - 7.45.3-2
- Use flask for testing, rather than bottle, to unblock Python 3.13 rebuild

* Wed Apr 03 2024 Lukáš Zaoral <lzaoral@redhat.com> - 7.45.3-1
- rebase to latest upstream version (rhbz#2264713)
- remove Python 2 support

* Mon Feb 12 2024 Lukáš Zaoral <lzaoral@redhat.com> - 7.45.2-11
- require libcurl-full for the test suite

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.45.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Lukáš Zaoral <lzaoral@redhat.com> - 7.45.2-9
- fix FTBFS on Rawhide

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.45.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 15 2023 Lukáš Zaoral <lzaoral@redhat.com> - 7.45.2-7
- do not package tests as documentation

* Fri Sep 15 2023 Lukáš Zaoral <lzaoral@redhat.com> - 7.45.2-6
- migrate to SPDX license format

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.45.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 28 2023 Python Maint <python-maint@redhat.com> - 7.45.2-4
- Rebuilt for Python 3.12

* Tue Mar 07 2023 Lukáš Zaoral <lzaoral@redhat.com> - 7.45.2-3
- temporarily disable test_http_version_3 (rhbz#2175216)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.45.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 16 2022 Kamil Dudka <kdudka@redhat.com> - 7.45.2-1
- update to 7.45.2 (#2154427)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.45.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 7.45.1-3
- Rebuilt for Python 3.11

* Tue May 03 2022 Lukáš Zaoral <lzaoral@redhat.com> - 7.45.1-2
- fix failing test-suite with curl 7.83+

* Tue Mar 15 2022 Lukáš Zaoral <lzaoral@redhat.com> - 7.45.1-1
- update to 7.45.1 (#2062500)
- do not ship tests/__pycache__

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.44.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Nov 03 2021 Lukáš Zaoral <lzaoral@redhat.com> - 7.44.1-4
- do not use deprecated unittest features (#2019410)

* Fri Sep 17 2021 Scott Talbert <swt@techie.net> - 7.44.1-3
- Cleanup test overrides & enable more tests

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 7.44.1-2
- Rebuilt with OpenSSL 3.0.0

* Mon Aug 16 2021 Kamil Dudka <kdudka@redhat.com> - 7.44.1-1
- update to 7.44.1

* Tue Aug 10 2021 Kamil Dudka <kdudka@redhat.com> - 7.44.0-1
- update to 7.44.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.43.0.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 20 2021 Kamil Dudka <kdudka@redhat.com> - 7.43.0.6-9
- use release tarball uploaded by upstream

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 7.43.0.6-8
- Rebuilt for Python 3.10

* Thu Jun 03 2021 Kamil Dudka <kdudka@redhat.com> - 7.43.0.6-7
- skip tests which are incompatible with recent releases of libcurl (#1965235)

* Wed Feb 17 2021 Kamil Dudka <kdudka@redhat.com> - 7.43.0.6-5
- temporarily remove a failing test-case (#1927655)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.43.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 18 2021 Kamil Dudka <kdudka@redhat.com> - 7.43.0.6-3
- make build dependencies for upstream tests optional

* Tue Oct 27 2020 Kamil Dudka <kdudka@redhat.com> - 7.43.0.6-2
- make the code compile against python-3.10.0a1 (#1890442)

* Thu Sep 03 2020 Kamil Dudka <kdudka@redhat.com> - 7.43.0.6-1
- update to 7.43.0.6

* Tue Aug 04 2020 Kamil Dudka <kdudka@redhat.com> - 7.43.0.5-6
- relax crypto policy for the test-suite to make it pass again (#1863711)

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.43.0.5-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.43.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Kamil Dudka <kdudka@redhat.com> - 7.43.0.5-3
- do not use discontinued %%_python_bytecompile_extra macro
- explicitly require python3-setuptools for build

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 7.43.0.5-2
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Kamil Dudka <kdudka@redhat.com> - 7.43.0.5-1
- update to 7.43.0.5

* Wed Jan 15 2020 Kamil Dudka <kdudka@redhat.com> - 7.43.0.4-1
- update to 7.43.0.4

* Fri Nov 15 2019 Kamil Dudka <kdudka@redhat.com> - 7.43.0.2-10
- do not build python2-pycurl on f32+

* Tue Sep 24 2019 Miro Hrončok <mhroncok@redhat.com> - 7.43.0.2-9
- Drop unused Python 2 BuildRequires

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 7.43.0.2-8
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.43.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Kamil Dudka <kdudka@redhat.com> - 7.43.0.2-6
- reintroduce the python2-pycurl subpackage on Fedora (#1672061)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.43.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 Kamil Dudka <kdudka@redhat.com> - 7.43.0.2-4
- fix programming mistakes detected by static analyzers

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.43.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 7.43.0.2-2
- Rebuilt for Python 3.7

* Mon Jun 04 2018 Kamil Dudka <kdudka@redhat.com> - 7.43.0.2-1
- update to 7.43.0.2

* Wed May 30 2018 Kamil Dudka <kdudka@redhat.com> - 7.43.0-17
- make the python2 and python3 subpackages optional

* Wed May 23 2018 Kamil Dudka <kdudka@redhat.com> - 7.43.0-16
- fix build failure caused by NotImplemented exceptions in winbuild.py

* Wed Mar 14 2018 Kamil Dudka <kdudka@redhat.com> - 7.43.0-15
- enable vsftpd-based tests
- run the test-suite for Python 3 only
- do not disable TLS-SRP test because it is now supported by OpenSSL in Fedora

* Mon Feb 19 2018 Kamil Dudka <kdudka@redhat.com> - 7.43.0-14
- add explicit BR for the gcc compiler

* Fri Feb 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 7.43.0-13
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.43.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.43.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.43.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 02 2017 Kamil Dudka <kdudka@redhat.com> - 7.43.0-9
- drop link-time vs. run-time TLS backend check (#1446850)

* Thu Apr 27 2017 Kamil Dudka <kdudka@redhat.com> - 7.43.0-8
- make pycurl compile against libcurl-openssl (#1445153)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.43.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 12 2016 Stratakis Charalampos <cstratak@redhat.com> - 7.43.0-6
- Rebuild for Python 3.6

* Tue Nov 29 2016 Charalampos Stratakis <cstratak@redhat.com> - 7.43.0-5
- Fix python2 subpackage name

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.43.0-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Apr 14 2016 Igor Gnatenko <ignatenko@redhat.com> - 7.43.0-3
- Follow new packaging guidelines

* Fri Feb 26 2016 Kamil Dudka <kdudka@redhat.com> - 7.43.0-2
- require libcurl of the same architecture as python-pycurl

* Sat Feb 06 2016 Kamil Dudka <kdudka@redhat.com> - 7.43.0-1
- update to 7.43.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.21.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 06 2016 Kamil Dudka <kdudka@redhat.com> - 7.21.5-3
- remove explicit dependency on keyutils-libs (reported by rpmlint)
- update FSF address in COPYING-LGPL (detected by rpmlint)

* Tue Jan 05 2016 Kamil Dudka <kdudka@redhat.com> - 7.21.5-2
- avoid installing binaries generated in %%check to /usr/share

* Tue Jan 05 2016 Kamil Dudka <kdudka@redhat.com> - 7.21.5-1
- update to 7.21.5

* Sat Nov 14 2015 Toshio Kuratomi <toshio@fedoraproject.org> - - 7.19.5.3-3
- Remove build dependency on cherrypy as it's no longer needed for testing

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Nov 03 2015 Kamil Dudka <kdudka@redhat.com> - 7.19.5.3-1
- update to 7.19.5.3

* Mon Nov 02 2015 Kamil Dudka <kdudka@redhat.com> - 7.19.5.2-1
- update to 7.19.5.2

* Mon Sep 07 2015 Kamil Dudka <kdudka@redhat.com> - 7.19.5.1-3
- introduce CURL_SSLVERSION_TLSv1_[0-2] (#1260408)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 12 2015 Kamil Dudka <kdudka@redhat.com> - 7.19.5.1-1
- update to 7.19.5.1

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Aug  3 2014 Tom Callaway <spot@fedoraproject.org> - 7.19.5-2
- fix license handling

* Mon Jul 14 2014 Kamil Dudka <kdudka@redhat.com> - 7.19.5-1
- update to 7.19.5

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 7.19.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Thu Feb 06 2014 Kamil Dudka <kdudka@redhat.com> - 7.19.3.1-1
- update to 7.19.3.1

* Fri Jan 10 2014 Kamil Dudka <kdudka@redhat.com> - 7.19.3-2
- add python3 subpackage (#1014583)

* Fri Jan 10 2014 Kamil Dudka <kdudka@redhat.com> - 7.19.3-1
- update to 7.19.3

* Thu Jan 02 2014 Kamil Dudka <kdudka@redhat.com> - 7.19.0.3-1
- update to 7.19.0.3

* Tue Oct 08 2013 Kamil Dudka <kdudka@redhat.com> - 7.19.0.2-1
- update to 7.19.0.2

* Wed Sep 25 2013 Kamil Dudka <kdudka@redhat.com> - 7.19.0.1-1
- update to 7.19.0.1

* Thu Aug 08 2013 Kamil Dudka <kdudka@redhat.com> - 7.19.0-18.20130315git8d654296
- sync with upstream 8d654296

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.0-17.20120408git9b8f4e38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 09 2013 Kamil Dudka <kdudka@redhat.com> - 7.19.0-16.20120408git9b8f4e38
- sync with upstream 9b8f4e38 (fixes #928370)
- add the GLOBAL_ACK_EINTR constant to the list of exported symbols (#920589)
- temporarily disable tests/multi_socket_select_test.py

* Wed Mar 06 2013 Kamil Dudka <kdudka@redhat.com> - 7.19.0-15
- allow to return -1 from the write callback (#857875) 
- remove the patch for curl-config --static-libs no longer needed
- run the tests against the just built pycurl, not the system one

* Mon Feb 25 2013 Kamil Dudka <kdudka@redhat.com> - 7.19.0-14
- apply bug-fixes committed to upstream CVS since 7.19.0 (fixes #896025)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 22 2012 Jan Synáček <jsynacek@redhat.com> - 7.19.0-12
- Improve spec

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Dennis Gilmore <dennis@ausil.us> - 7.19.0-8
- add Missing Requires on keyutils-libs

* Tue Aug 17 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.19.0-7
- Add patch developed by David Malcolm to fix segfaults caused by a missing incref

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 7.19.0-6
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Mar  2 2010 Karel Klic <kklic@redhat.com> - 7.19.0-5
- Package COPYING2 file
- Added MIT as a package license

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr 17 2009 Stepan Kasal <skasal@redhat.com> - 7.19.0-3
- fix typo in the previous change

* Fri Apr 17 2009 Stepan Kasal <skasal@redhat.com> - 7.19.0-2
- add a require to reflect a dependency on libcurl version (#496308)

* Thu Mar  5 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.19.0-1
- Update to 7.19.0

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.18.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 7.18.2-2
- Rebuild for Python 2.6

* Thu Jul  3 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.18.2-1
- Update to 7.18.2
- Thanks to Ville Skyttä re-enable the tests and fix a minor problem
  with the setup.py. (Bug # 45400)

* Thu Jun  5 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.18.1-1
- Update to 7.18.1
- Disable tests because it's not testing the built library, it's trying to
  test an installed library.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 7.16.4-3
- Autorebuild for GCC 4.3

* Thu Jan  3 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.16.4-2
- BR openssl-devel

* Wed Aug 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.16.4-1
- Update to 7.16.4
- Update license tag.

* Sat Jun  9 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.16.2.1-1
- Update to released version.

* Thu Dec  7 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.16.0-0.1.20061207
- Update to a CVS snapshot since development has a newer version of curl than is in FC <= 6

* Thu Dec  7 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.15.5.1-4
- Add -DHAVE_CURL_OPENSSL to fix PPC build problem.

* Thu Dec  7 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.15.5.1-3
- Don't forget to Provide: pycurl!!!

* Thu Dec  7 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.15.5.1-2
- Remove INSTALL from the list of documentation
- Use python_sitearch for all of the files

* Thu Dec  7 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 7.15.5.1-1
- First version for Fedora Extras
