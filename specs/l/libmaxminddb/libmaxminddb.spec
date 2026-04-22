# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary:        C library for reading MaxMind DB files
Name:           libmaxminddb
Version:        1.12.2
Release: 6%{?dist}
# BSD-3-Clause (src/maxminddb-compat-util.h) and Apache-2.0 (the rest)
License:        Apache-2.0 AND BSD-3-Clause
URL:            https://maxmind.github.io/libmaxminddb/
Source0:        https://github.com/maxmind/libmaxminddb/releases/download/%{version}/%{name}-%{version}.tar.gz
Source1:        maxminddb_config.h
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gcc
BuildRequires:  make
# Testsuite in %%check
BuildRequires:  gcc-c++
BuildRequires:  perl-interpreter
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(IPC::Run3)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Output)

%description
The libmaxminddb library provides a C library for reading MaxMind DB
files, including the GeoIP2 databases from MaxMind. This is a custom
binary format designed to facilitate fast lookups of IP addresses
while allowing for great flexibility in the type of data associated
with an address.

The MaxMind DB format is an open file format. The specification is
available at https://maxmind.github.io/MaxMind-DB/ and licensed under
the Creative Commons Attribution-ShareAlike 3.0 Unported License.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
autoreconf --force --install

%build
%configure --disable-static
%make_build

%install
%make_install

# Don't install any libtool .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}.la

# Avoid file conflicts in multilib installations of -devel subpackage
mv -f $RPM_BUILD_ROOT%{_includedir}/maxminddb_config{,-%{__isa_bits}}.h
install -p -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_includedir}/maxminddb_config.h

%check
# Tests are linked dynamically, preload the library as RPATH is removed
LD_PRELOAD=$RPM_BUILD_ROOT%{_libdir}/%{name}.so make check

%files
%license LICENSE
%doc Changes.md README.md
%{_bindir}/mmdblookup
%{_libdir}/%{name}.so.0*
%{_mandir}/man1/mmdblookup.1*

%files devel
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/maxminddb.h
%{_includedir}/maxminddb_config.h
%{_includedir}/maxminddb_config-%{__isa_bits}.h
%{_mandir}/man3/%{name}.3*
%{_mandir}/man3/MMDB_*.3*

%changelog
* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Jan 12 2025 Robert Scheck <robert@fedoraproject.org> 1.12.2-1
- Upgrade to 1.12.2 (#2337039)

* Thu Jan 09 2025 Robert Scheck <robert@fedoraproject.org> 1.12.1-1
- Upgrade to 1.12.1 (#2336410)

* Wed Jan 08 2025 Robert Scheck <robert@fedoraproject.org> 1.12.0-1
- Upgrade to 1.12.0 (#2336283)

* Thu Aug 22 2024 Robert Scheck <robert@fedoraproject.org> 1.11.0-1
- Upgrade to 1.11.0 (#2307227)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Robert Scheck <robert@fedoraproject.org> 1.10.0-1
- Upgrade to 1.10.0 (#2291420)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Robert Scheck <robert@fedoraproject.org> 1.9.1-1
- Upgrade to 1.9.1 (#2257602)

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 15 2023 Robert Scheck <robert@fedoraproject.org> 1.8.0-1
- Upgrade to 1.8.0 (#2248696)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Oct 02 2022 Robert Scheck <robert@fedoraproject.org> 1.7.1-1
- Upgrade to 1.7.1 (#2131161 #c1)

* Sat Oct 01 2022 Robert Scheck <robert@fedoraproject.org> 1.7.0-1
- Upgrade to 1.7.0 (#2131161)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> 1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Nov 28 2021 Igor Raits <ignatenkobrain@fedoraproject.org> 1.6.0-1
- Update to 1.6.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Mar 15 2021 Michal Ruprich <mruprich@redhat.com> - 1.5.2-1
- Update to 1.5.2

* Tue Jan 26 2021 Michal Ruprich <mruprich@redhat.com> - 1.5.0-1
- Update to 1.5.0

* Thu Dec 10 2020 Michal Ruprich <mruprich@redhat.com> - 1.4.3-1
- Update to 1.4.3
- Resolves: #1758843 - libmaxminddb-devel i686 can't be installed in parallel to x86_64
- Fix for CVE-2020-28241

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 02 2020 Michal Ruprich <michalruprich@gmail.com> - 1.4.2-2
- Move manpage for mmdblookup from -devel to the main package

* Tue May 12 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.4.2-1
- Update to 1.4.2

* Mon Mar 30 2020 Michal Ruprich <mruprich@redhat.com> - 1.3.2-3
- Move mmdblookup binary from -devel to the main package

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Oct 21 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.2-1
- Update to 1.3.2

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Mar 27 2016 Jan Vcelak <jvcelak@fedoraproject.org> 1.2.0-1
- rebase to new version

* Mon Mar 21 2016 Jan Vcelak <jvcelak@fedoraproject.org> 1.1.5-1
- rebase to new version

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Sep 15 2015 Jan Vcelak <jvcelak@fedoraproject.org> 1.1.1-5
- add pkg-config file from the upcoming upstream version

* Mon Sep 14 2015 Jan Vcelak <jvcelak@fedoraproject.org> 1.1.1-4
- remove utils subpackage and place mmdblookup into devel subpackage
- remove Group from the spec file
- move NOTICE and Changes.md to devel subpackage

* Thu Sep 03 2015 Jan Vcelak <jvcelak@fedoraproject.org> 1.1.1-3
- updated package licence
- added --as-needed linker flag

* Tue Sep 01 2015 Jan Vcelak <jvcelak@fedoraproject.org> 1.1.1-1
- initial version of the package
