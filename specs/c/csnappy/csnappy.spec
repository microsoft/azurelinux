# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run valgrind test
# valgrind is available only on selected arches
%ifarch %{valgrind_arches}
%bcond_without csnappy_enables_valgrind
%else
%bcond_with csnappy_enables_valgrind
%endif

%global commit 6c10c305e8dde193546e6b33cf8a785d5dc123e2
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:       csnappy 
Version:    0
Release: 33.20211216git%{shortcommit}%{?dist}
Summary:    Snappy compression library ported to C 
License:    BSD-3-Clause
URL:        https://github.com/zeevt/%{name}
Source0:    %{url}/archive/%{commit}/%{name}-%{commit}.tar.gz
# Fix parallel tests, <https://github.com/zeevt/csnappy/pull/40>
Patch0:     csnappy-6c10c305e8dde193546e6b33cf8a785d5dc123e2-Fix-parallel-tests-by-only-testing-the-current-optim.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  sed
# Tests:
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  gzip
%if %{with csnappy_enables_valgrind}
BuildRequires:  valgrind
%endif

%description
This is an ANSI C port of Google's Snappy library. Snappy is a compression
library designed for speed rather than compression ratios.

%package devel
Summary:    Development files for the %{name} library
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files for developing applications that use the %{name} library.


%prep
%autosetup -p1 -n %{name}-%{commit}

# Extract BSD license and copyright notices, bug #1152057
! test -e LICENSE
for F in $(< Makefile sed -e '/libcsnappy.so:/ s/.*:// p' -e 'd'); do
    < $F sed -e '/Copyright/,/\*\//p' -e 'd'
done > LICENSE
test -s LICENSE

%build
%{make_build} 'OPT_FLAGS=%{optflags}' 'LDFLAGS=%{?__global_ldflags}' \
    lib%{name}.so cl_tester

%check
make %{?_smp_mflags} 'OPT_FLAGS=%{optflags}' 'LDFLAGS=%{?__global_ldflags}' check_unaligned_uint64 cl_test
%if %{with csnappy_enables_valgrind}
make %{?_smp_mflags} 'OPT_FLAGS=%{optflags}' 'LDFLAGS=%{?__global_ldflags}' check_leaks
%endif

%install
%{make_install} 'DESTDIR=%{buildroot}' 'LIBDIR=%{_libdir}'

%files
%license LICENSE
%doc README TODO
# No soname <https://github.com/zeevt/csnappy/issues/33>
%{_libdir}/lib%{name}.so

%files devel
%{_includedir}/%{name}.h


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0-32.20211216git6c10c30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0-31.20211216git6c10c30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0-30.20211216git6c10c30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0-29.20211216git6c10c30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0-28.20211216git6c10c30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 21 2023 Petr Pisar <ppisar@redhat.com> - 0-27.20211216git6c10c30
- Migrate to SPDX license

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0-26.20211216git6c10c30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0-25.20211216git6c10c30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0-24.20211216git6c10c30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0-23.20211216git6c10c30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 16 2021 Petr Pisar <ppisar@redhat.com> - 0-22.20211216git6c10c30
- Rebased to 6c10c305e8dde193546e6b33cf8a785d5dc123e2 (fixes building on AIX,
  Sun; fixes an undefined behavior whith unaliagned memory access)

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0-21.20191203gitcbd205b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0-20.20191203gitcbd205b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-19.20191203gitcbd205b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Feb 04 2020 Petr Pisar <ppisar@redhat.com> - 0-18.20191203gitcbd205b
- Rebased to cbd205bfec1d2adfbe8a3b3b120b7a3556f982d1

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-17.20181121git973f62f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep 11 2019 Petr Pisar <ppisar@redhat.com> - 0-16.20181121git973f62f
- Rebased to 973f62f7eede7412e04be230adcb52e78dd25079

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0-15.20181121gitb476930
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0-14.20181121gitb476930
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 21 2018 Petr Pisar <ppisar@redhat.com> - 0-13.20181121gitb476930
- Rebased to b47693024402fa8760edcd4fed71131cbd5ac175

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-12.20180322git51802a8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 23 2018 David Abdurachmanov <david.abdurachmanov@gmail.com> - 0-11.20180322git51802a8
- Switch to %%{valgrind_arches}

* Thu Mar 22 2018 Petr Pisar <ppisar@redhat.com> - 0-10.20180322git51802a8
- Rebase to 51802a869db97326c803dcabdb6e6ed0797a715a

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-9.20150729gitd7bc683
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-8.20150729gitd7bc683
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-7.20150729gitd7bc683
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-6.20150729gitd7bc683
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0-5.20150729gitd7bc683
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jul 30 2015 Petr Pisar <ppisar@redhat.com> - 0-4.20150729gitd7bc683
- Rebase to d7bc683b6eaba225f483621485035a8044634376

* Wed Jul 29 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 0-3.20150331gitcf029fa
- Fix build on aarch64 (upstream issue https://github.com/zeevt/csnappy/issues/23 got note)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-2.20150331gitcf029fa
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May  3 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0-1.20150331gitcf029fa
- Rebase to 20150331
- Use same make flags for tests
- Use %%license

* Fri Jan 16 2015 Dan Horák <dan[at]danny.cz> - 0-1.20141010gitb43c183
- valgrind is available only on selected arches

* Mon Oct 13 2014 Petr Pisar <ppisar@redhat.com> - 0-0.20141010gitb43c183
- b43c183fdad31be0500a5f2ae022a54a66cb1a3d snapshot

