Name:           libdatrie
Version:        0.2.9
Release:        12%{?dist}
Summary:        Implementation of Double-Array structure for representing trie
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://linux.thai.net/projects/datrie
Source0:        https://linux.thai.net/pub/thailinux/software/libthai/%{name}-%{version}.tar.xz
Patch0:         libdatrie-fixes-docs.patch
BuildRequires:  autoconf, automake, libtool

%description
datrie is an implementation of double-array structure for representing trie.

Trie is a kind of digital search tree, an efficient indexing method with O(1) 
time complexity for searching. Comparably as efficient as hashing, trie also 
provides flexibility on incremental matching and key spelling manipulation. 
This makes it ideal for lexical analyzers, as well as spelling dictionaries.

Details of the implementation: https://linux.thai.net/~thep/datrie/datrie.html

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch 0 -p1 -b .docs

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
LD_LIBRARY_PATH=../datrie/.libs %make_build check

%ldconfig_scriptlets

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

%changelog
* Mon Nov 02 2020 Joe Schmitt <joschmit@microsoft.com> - 0.2.9-12
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove doxygen dependency.

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
