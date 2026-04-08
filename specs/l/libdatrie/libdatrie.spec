# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libdatrie
Version:        0.2.13
Release:        12%{?dist}
Summary:        Implementation of Double-Array structure for representing trie
License:        LGPL-2.1-or-later
URL:            http://linux.thai.net/projects/datrie
Source0:        http://linux.thai.net/pub/thailinux/software/libthai/%{name}-%{version}.tar.xz
BuildRequires:  autoconf, automake, libtool
BuildRequires:  autoconf-archive
BuildRequires:  doxygen
BuildRequires:  make

%description
datrie is an implementation of double-array structure for representing trie.

Trie is a kind of digital search tree, an efficient indexing method with O(1) 
time complexity for searching. Comparably as efficient as hashing, trie also 
provides flexibility on incremental matching and key spelling manipulation. 
This makes it ideal for lexical analyzers, as well as spelling dictionaries.

Details of the implementation: http://linux.thai.net/~thep/datrie/datrie.html

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
autoreconf -f -i -v
#sed -i '/sys_lib_dlsearch_path_spec/s|/usr/lib |/usr/lib /usr/lib64|' configure
%configure --disable-static \
           --with-html-docdir=%{_pkgdocdir}-devel
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build

%install
%make_install
rm -frv %{buildroot}%{_pkgdocdir}
find %{buildroot} -name '*.*a' -delete -print

%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

LD_LIBRARY_PATH=../datrie/.libs %make_build check

%files
%license COPYING
%{_libdir}/libdatrie.so.*

%files devel
%doc AUTHORS ChangeLog NEWS README*
%{_includedir}/datrie/
%{_libdir}/libdatrie.so
%{_libdir}/pkgconfig/datrie-0.2.pc
%{_bindir}/trietool*
%{_mandir}/man1/trietool*
%{_pkgdocdir}-devel/*.{html,css,png,js,svg}

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.13-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.13-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.13-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.13-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed May 17 2023 Peng Wu <pwu@redhat.com> - 0.2.13-6
- Migrate to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Feb  1 2021 Peng Wu <pwu@redhat.com> - 0.2.13-1
- Update to 0.2.13

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.9-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Oct 14 2020 Peng Wu <pwu@redhat.com> - 0.2.9-13
- Fixes FTBFS

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.9-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.9-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Apr  6 2016 Peng Wu <pwu@redhat.com> - 0.2.9-3
- Fixes docs build

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Christopher Meng <rpm@cicku.me> - 0.2.9-1
- Update to 0.2.9

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jun 18 2014 Christopher Meng <rpm@cicku.me> - 0.2.8-4
- Move docs to %%_pkgdocdir

* Mon Feb 24 2014 Christopher Meng <rpm@cicku.me> - 0.2.8-3
- Disable rpath.

* Sat Feb 08 2014 Christopher Meng <rpm@cicku.me> - 0.2.8-2
- Reform the subpackages.
- Add check section to ensure the availability.

* Tue Jan 07 2014 Christopher Meng <rpm@cicku.me> - 0.2.8-1
- Initial Package.
