Summary:        Process Management Interface Exascale (PMIx)
Name:           pmix
Version:        5.0.1
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://pmix.org/
Source0:        https://github.com/openpmix/openpmix/releases/download/v%{version}/%{name}-%{version}.tar.bz2
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  hwloc-devel
BuildRequires:  libevent-devel
BuildRequires:  libtool
BuildRequires:  munge-devel
BuildRequires:  perl-File-Find
BuildRequires:  perl-interpreter

%description
The Process Management Interface (PMI) has been used for quite some time as
a means of exchanging wireup information needed for interprocess
communication. Two versions (PMI-1 and PMI-2) have been released as part of
the MPICH effort. While PMI-2 demonstrates better scaling properties than its
PMI-1 predecessor, attaining rapid launch and wireup of the roughly 1M
processes executing across 100k nodes expected for exascale operations remains
challenging.

PMI Exascale (PMIx) represents an attempt to resolve these questions by
providing an extended version of the PMI standard specifically designed to
support clusters up to and including exascale sizes. The overall objective of
the project is not to branch the existing pseudo-standard definitions - in
fact, PMIx fully supports both of the existing PMI-1 and PMI-2 APIs - but
rather to (a) augment and extend those APIs to eliminate some current
restrictions that impact scalability, and (b) provide a reference
implementation of the PMI-server that demonstrates the desired level of
scalability.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        tools
Summary:        Tools for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    tools
The %{name}-tools package contains for use with PMIx-based RMs and language-
based starters (e.g., mpirun).

* pinfo - show MCA params, build info, etc.
* pps - get list of active nspaces, retrieve status of jobs/nodes/procs
* pevent - inject an event into the system

%prep
%autosetup -p1

echo touching lexer sources to recompile them ...
find src -name \*.l -print -exec touch --no-create {} \;

%build
%{_builddir}/%{name}-%{version}/autogen.pl
%configure \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir}/%{name} \
    --disable-static \
    --disable-silent-rules \
    --enable-shared \
    --enable-pmi-backward-compatibility \
    --with-munge

%make_build

%check
%make_build check

%install
%make_install

# remove libtool archives
find %{buildroot} -type f -name "*.la" -delete -print

%ldconfig_scriptlets
%ldconfig_scriptlets devel

%files
%license LICENSE
%doc README
%dir %{_datadir}/%{name}
%dir %{_libdir}/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*.conf
%{_datadir}/%{name}/*.txt
%{_libdir}/libpmix.so.2*
%{_libdir}/%{name}/*.so
%{_mandir}/man1/*.1*

%files devel
%{_datadir}/%{name}/*.supp
%{_includedir}/pmix*.h
%{_includedir}/pmix/
%{_libdir}/libpmix.so
%{_libdir}/pkgconfig/*.pc

%files tools
%{_bindir}/*

%changelog
* Wed Jan 24 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.0.1-1
- Auto-upgrade to 5.0.1 - none

* Thu Sep 21 2023 Sumedh Sharma <sumsharma@microsoft.com> - 4.1.3-1
- Bump version to address CVE-2023-41915

* Thu Feb 02 2023 Riken Maharjan <rmaharjan@microsoft.com> - 4.1.2-1
- Move from Extended to core
- Update to 4.1.2 (from Fedora 38 (license: MIT))
- License verified

* Fri Jan 08 2021 Ruying Chen <v-ruyche@microsoft.com> - 3.1.5-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Add build requirement perl-File-Find.

* Mon Feb 24 2020 Philip Kovacs <pkfed@fedoraproject.org> - 3.1.5-1
- Update to 3.1.5

* Thu Feb 20 2020 Philip Kovacs <pkfed@fedoraproject.org> - 3.1.5-0.4.rc4
- Update to 3.1.5rc4

* Wed Feb 12 2020 Philip Kovacs <pkfed@fedoraproject.org> - 3.1.5-0.3.rc3
- Update to 3.1.5rc3

* Mon Feb 10 2020 Philip Kovacs <pkfed@fedoraproject.org> - 3.1.5-0.2.rc2
- Update to 3.1.5rc2

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Aug 25 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.1.4-2
- Rebuilt for hwloc-2.0

* Fri Aug 9 2019 Philip Kovacs <pkfed@fedoraproject.org> - 3.1.4-1
- Update to 3.1.4

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.4-0.4.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jul 21 2019 Philip Kovacs <pkfed@fedoraproject.org> - 3.1.4-0.3.rc2
- Create pmix-pmi and pmix-pmi-devel subpackages for pmi/pmi2 libs
- Remove rpm-generated pkgconfig files until upstream provides them
- Do not pull dependencies with pkgconfig unless package uses it

* Sat Jul 20 2019 Philip Kovacs <pkfed@fedoraproject.org> - 3.1.4-0.2.rc2
- Update to 3.1.4rc2

* Fri Jul 19 2019 Philip Kovacs <pkfed@fedoraproject.org> - 3.1.4-0.1.rc1
- Update to 3.1.4rc1

* Sat Jul 13 2019 Philip Kovacs <pkfed@fedoraproject.org> - 3.1.3-1
- Update to 3.1.3

* Tue Jul 2 2019 Philip Kovacs <pkfed@fedoraproject.org> - 3.1.2-2
- Install libpmi/pmi2 backward-compatible libraries normally,
- not as a pmi environment module

* Wed Jun 19 2019 Philip Kovacs <pkfed@fedoraproject.org> - 3.1.2-1
- Update to 3.1.2
- Replace __make with make

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 25 2018 Orion Poplawski <orion@nwra.com> - 3.0.2-1
- Update to 3.0.2

* Mon Oct 1 2018 Philip Kovacs <pkfed@fedoraproject.org> - 2.1.4-1
- Update to 2.1.4

* Fri Mar 16 2018 Philip Kovacs <pkfed@fedoraproject.org> - 2.1.1-1
- Update to 2.1.1

* Sun Feb 18 2018 Philip Kovacs <pkfed@fedoraproject.org> - 2.1.0-3
- Add patch to remove unneeded check for C++

* Thu Feb 15 2018 Philip Kovacs <pkfed@fedoraproject.org> - 2.1.0-2
- Rebuild for libevent soname bump

* Sat Feb 10 2018 Philip Kovacs <pkfed@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0
- Added enviromnent module for pmi/pmix
- Added pkgconfig files for pmix/pmi/pmi2
- Ensure lexer sources are rebuilt
- Removed obsolete sasl support
- Use new ldconfig_scriplets macro

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 21 2017 Orion Poplawski <orion@cora.nwra.com> - 1.2.2-1
- Update to 1.2.2

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Sep 7 2016 Orion Poplawski <orion@cora.nwra.com> - 1.1.5-1
- Update to 1.1.5

* Fri Jun 10 2016 Orion Poplawski <orion@cora.nwra.com> - 1.1.4-1
- Update to 1.1.4

* Tue Mar 8 2016 Orion Poplawski <orion@cora.nwra.com> - 1.1.3-1
- Update to 1.1.3

* Mon Nov 16 2015 Orion Poplawski <orion@cora.nwra.com> - 1.1.1-1
- Update to 1.1.1

* Sat Nov 14 2015 Orion Poplawski <orion@cora.nwra.com> - 1.1.0-1
- Update to 1.1.0

* Tue Sep  1 2015 Orion Poplawski <orion@cora.nwra.com> - 1.0.0-1
- Initial version
