# Force out of source build
%undefine __cmake_in_source_build

%global commit da33770d22b404d7333e46e26495eaca0c5a6d8a
%global gittag 5.8.0
%global shortcommit %(c=%{commit}; echo ${c:0:7})

ExclusiveArch:  %{ix86} x86_64 aarch64

# Disable 32-bit builds on architectures with multilibs
# to avoid attempting pulling in 32-bit in to koji build.
%ifarch x86_64
%global disable32bit -Ddisable32bit=ON
%endif
Summary:        Tool to record and replay execution of applications
Name:           rr
Version:        5.8.0
Release:        2%{?dist}
# The entire source code is MIT with the exceptions of
# files in following directories:
#   third-party/blake2             CC0
#   third-party/gdb                BSD
#   third-party/proc-service       BSD
#   third-party/zen-pmu-workaround GPLv2
License:        MIT and CC0 and BSD and GPLv2
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            http://rr-project.org

Source: https://github.com/rr-debugger/rr/archive/%{gittag}/%{name}-%{version}.tar.gz

%if  0%{?rhel} == 7
BuildRequires: cmake3
BuildRequires: python36-pexpect
%else
BuildRequires: cmake
BuildRequires: python3-pexpect
%endif
BuildRequires: python3
BuildRequires: make gcc gcc-c++ gdb
BuildRequires: libgcc
BuildRequires: glibc-devel
BuildRequires: libstdc++-devel
BuildRequires: man-pages
BuildRequires: capnproto capnproto-libs capnproto-devel
BuildRequires: patchelf
BuildRequires: zlib-devel

%description
rr is a lightweight tool for recording and replaying execution
of applications (trees of processes and threads).
For more information, please visit http://rr-project.org

%package testsuite
Summary: Testsuite for checking rr functionality
Requires: rr
Requires: gdb
Requires: python3
%if  0%{?rhel} == 7
Requires: python36-pexpect
Requires: cmake3
%else
Requires: python3-pexpect
Requires: cmake
%endif
%description testsuite
rr-testsuite includes compiled test binaries and other files
which are used to test the functionality of rr.
 
%prep
%autosetup -p1 -n rr-%{gittag}

%build
%if  0%{?rhel} == 7
%cmake3 -DCMAKE_BUILD_TYPE=Release -DINSTALL_TESTSUITE=ON %{?disable32bit}
%cmake3_build
%else
%cmake -DCMAKE_BUILD_TYPE=Release -DINSTALL_TESTSUITE=ON %{?disable32bit}
%cmake_build
%endif

%install
%if  0%{?rhel} == 7
%cmake3_install
%else
%cmake_install
%endif

rm -rf %{buildroot}%{_datadir}/rr/src

# Using a small hack from the Dyninst testsuite which changes file permissions
# to prevent any stripping of debugging information. This is done for libraries
# and executables used by the testsuite.
find %{buildroot}%{_libdir}/rr/testsuite/obj/bin \
  -type f -name '*' -execdir chmod 644 '{}' '+'

find %{buildroot}%{_libdir} \
  -type f -name '*.so' -execdir chmod 644 '{}' '+'

# Some files contain invalid RPATHS.
patchelf --set-rpath '%{_libdir}/rr/' %{buildroot}%{_libdir}/rr/testsuite/obj/bin/constructor
patchelf --set-rpath '%{_libdir}/rr/' %{buildroot}%{_libdir}/rr/testsuite/obj/bin/step_into_lib

%files
%dir %{_libdir}/rr
%{_libdir}/rr/*.so
%exclude %{_libdir}/rr/libtest_lib*.so
%{_bindir}/rr
%{_bindir}/rr_exec_stub*
%{_bindir}/signal-rr-recording.sh
%{_bindir}/rr-collect-symbols.py
%{_datadir}/bash-completion/completions/rr
%dir %{_datadir}/rr
%{_datadir}/rr/*.xml

%attr(755,root,root) %{_libdir}/rr/*.so

%files testsuite
%{_libdir}/rr/libtest_lib*.so
%dir %{_libdir}/rr/testsuite
%{_libdir}/rr/testsuite/*

%attr(755,root,root) %{_libdir}/rr/libtest_lib*.so
%attr(755,root,root) %{_libdir}/rr/testsuite/obj/bin/*

%license LICENSE

%changelog
* Fri Jun 14 2024 Henry Beberman <henry.beberman@microsoft.com> - 5.8.0-2
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Mon May 20 2024 William Cohen <wcohen@redhat.com> - 5.8.0-1
- Rebase to rr-5.8.0.

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 4 2023 William Cohen <wcohen@redhat.com> - 5.7.0-9
- Rebase to rr-5.7.0.

* Tue Sep 12 2023 William Cohen <wcohen@redhat.com> - 5.6.0-8
- Rebuild for capnproto 1.0.1

* Fri Sep 08 2023 Neal Gompa <ngompa@fedoraproject.org> - 5.6.0-7
- Rebuild for capnproto 1.0.1

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 William Cohen <wcohen@redhat.com> - 5.6.0-5
- Fix FTBFS issue with gcc-13.

* Sat Dec  3 2022 Florian Weimer <fweimer@redhat.com> - 5.6.0-4
- Avoid implicit function declaration in test (C99 compatibility)

* Fri Dec 02 2022 Fabio Valentini <decathorpe@gmail.com> - 5.6.0-3
- Rebuild for capnproto 0.10.3 / CVE-2022-46149

* Tue Nov 29 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.6.0-2
- Rebuild for capnproto 0.10.2

* Mon Aug 8 2022 William Cohen <wcohen@redhat.com> - 5.6.0-1
- Rebase to rr-5.6.0.

* Fri Aug 5 2022 William Cohen <wcohen@redhat.com> - 5.5.0-5.20220805gitda33770
- Sync with upstream branch master,
  commit da33770d22b404d7333e46e26495eaca0c5a6d8a.

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 21 2021 Neal Gompa <ngompa@fedoraproject.org> - 5.5.0-2
- Rebuild for capnproto 0.9.1

* Mon Sep 20 2021 William Cohen <wcohen@redhat.com> - 5.5.0-1
- Rebase to rr-5.5.0.

* Thu Jul 29 2021 William Cohen <wcohen@redhat.com> - 5.4.0-4
- Fix FTBFS (rhbz#1987924)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 2 2020 William Cohen <wcohen@redhat.com> - 5.4.0-1
- Rebase to rr-5.4.0.

* Fri Aug 28 2020 Sagar Patel <sapatel@redhat.com> - 5.3.0-19.20200828gitb53e4d9
- Sync with upstream branch master,
  commit b53e4d990b873e1b57284994ad7a65f3626880f5.
- Fix package requirements for rr-testsuite.
- Note: There is an issue causing rr to hang on RHEL7 (RHBZ#1873266).
- Note: There are some pathing issues with rr-testsuite.

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-17.20200427gitbab9ca9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 18 2020 Neal Gompa <ngompa13@gmail.com> - 5.3.0-16.20200427gitbab9ca9
- Rebuilt for capnproto 0.8.0 again

* Sat Jul 18 2020 Neal Gompa <ngompa13@gmail.com> - 5.3.0-15.20200427gitbab9ca9
- Rebuilt for capnproto 0.8.0

* Mon Apr 27 2020 Sagar Patel <sapatel@redhat.com> 14.20200427gitbab9ca9
- Sync with upstream branch master,
  commit bab9ca94fc03d893cf6b8bf58f7b4522a0113466.
- Build failures from the previous release are now fixed.

* Fri Apr 24 2020 Sagar Patel <sapatel@redhat.com> 13.20200424gitcf5169b
- Sync with upstream branch master,
  commit cf5169bb3e29ce9db4a73e26164bec0e92b083fb.
- Introduces support for installable testsuite.

* Mon Feb 24 2020 Sagar Patel <sapatel@redhat.com> 11.20200224git4513b23
- Sync with upstream branch master,
  commit 4513b23c8092097dc42c73f3cbaf4cfaebd04efe.
- New patches enable rr to be built on older compilers.

* Thu Feb 13 2020 Sagar Patel <sapatel@redhat.com> 10.20200213gitabd3442
- Sync with upstream branch master,
  commit abd344288878c9b4046e0b8664927992947a46eb.
- New patches enable rr to be built on RHEL7.2 and later.

* Tue Jan 14 2020 William Cohen <wcohen@redhat.com> 5.3.0-8.20200124git7908fea
- Sync with upstream branch master,
  commit 70ba28f7ab2923d4e36ffc9d5d2e32357353b25c.
- SRPM buildable on Fedora koji or other rpm build systems.
