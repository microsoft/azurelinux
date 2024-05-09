Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global sover 0
%global git_url https://github.com/troydhanson/%{name}

%global common_desc							\
Any C structure can be stored in a hash table using uthash.  Just	\
add a UT_hash_handle to the structure and choose one or more fields	\
in your structure to act as the key.  Then use these macros to store,	\
retrieve or delete items from the hash table.

# Setup _pkgdocdir if not defined already
%{!?_pkgdocdir:%global _pkgdocdir %{_docdir}/%{name}-%{version}}


Name:		uthash
Version:	2.0.2
Release:	9%{?dist}
Summary:	A hash table for C structures

License:	BSD
URL:		https://troydhanson.github.io/%{name}
Source0:	%{git_url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

%if (0%{?rhel} && 0%{?rhel} <= 6)
# Downstream patch for asciidoc generation.
Patch1000:	%{name}-%{version}_fix-asciidoc.patch
%endif # (0#{?rhel} && 0#{?rhel} <= 6)

BuildRequires:  gcc
BuildRequires:	asciidoc
BuildRequires:	perl-interpreter

%description
%{common_desc}


%package	devel
Summary:	A hash table for C structures (headers only)

Provides:	%{name}-static	== %{version}-%{release}

BuildArch:	noarch

%description    devel
%{common_desc}


%package doc
Summary:	Documentation-files for %{name}.
BuildArch:	noarch

%description doc
This package contains the documentation-files for %{name}.


%package -n libut
Summary:	Library-implementation of utvector

%description -n libut
The utvector is an alternative to utarray.  It is a bit more
efficient.  It's object code, not just a header.


%package -n libut-devel
Summary:	Development-files for libut

Requires:	%{name}-devel	== %{version}-%{release}
Requires:	libut%{?_isa}	== %{version}-%{release}

%description -n libut-devel
Development-files for libut.


%prep
%autosetup -p 1


%build
%configure || :
export CFLAGS="-fPIC ${CFLAGS}"
%make_build -C libut
%{__cc} -shared ${CFLAGS} ${LDFLAGS}					\
	-Wl,-soname,libut.so.%{sover}					\
	-o libut/libut.so.%{sover} libut/*.o
%make_build -C doc


%install
%{__mkdir} -p html							\
	%{buildroot}%{_includedir}					\
	%{buildroot}%{_libdir}						\
	%{buildroot}%{_pkgdocdir}/{html,libut}
%{__install} -pm 0644 src/*.h %{buildroot}%{_includedir}
%{__install} -pm 0755 libut/libut.so.0 %{buildroot}%{_libdir}
/bin/ln -s %{_libdir}/libut.so.0 %{buildroot}%{_libdir}/libut.so

# Install doc.
%{__install} -pm 0644 doc/*.txt %{buildroot}%{_pkgdocdir}
%{__install} -pm 0644 doc/*.html doc/*.css doc/*.png %{buildroot}%{_pkgdocdir}/html
%{__install} -pm 0644 libut/README.md %{buildroot}%{_pkgdocdir}/libut
%if (0%{?rhel} && 0%{?rhel} <= 6)
%{__install} -pm 0644 LICENSE %{buildroot}%{_pkgdocdir}
%endif # (0#{?rhel} && 0#{?rhel} <= 6)


%check
%configure || :
%make_build -C tests
%make_build -C tests/threads
%make_build -C libut/tests


%ldconfig_scriptlets -n libut


%files devel
%if !(0%{?rhel} && 0%{?rhel} <= 6)
%license LICENSE
%else  # !(0%{?rhel} && 0%{?rhel} <= 6)
%doc %{_pkgdocdir}/LICENSE
%endif # !(0%{?rhel} && 0%{?rhel} <= 6)
%doc %dir %{_pkgdocdir}
%exclude %{_includedir}/utvector.h
%{_includedir}/ut*.h

%files doc
%if !(0%{?rhel} && 0%{?rhel} <= 6)
%license %{_datadir}/licenses/%{name}*
%endif # !(0%{?rhel} && 0%{?rhel} <= 6)
%doc %{_pkgdocdir}

%files -n libut
%if !(0%{?rhel} && 0%{?rhel} <= 6)
%license %{_datadir}/licenses/%{name}*
%else  # !(0%{?rhel} && 0%{?rhel} <= 6)
%doc %{_pkgdocdir}/LICENSE
%endif # !(0%{?rhel} && 0%{?rhel} <= 6)
%doc %dir %{_pkgdocdir}
%{_libdir}/libut.so.%{sover}

%files -n libut-devel
%doc %dir %{_pkgdocdir}
%doc %{_pkgdocdir}/libut
%{_includedir}/libut.h
%{_includedir}/ringbuf.h
%{_includedir}/utvector.h
%{_libdir}/libut.so


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.2-9
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Mar 04 2017 Björn Esser <besser82@fedoraproject.org> - 2.0.2-1
- New upstream release (rhbz#1429106)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 30 2016 Björn Esser <bjoern.esser@gmail.com> - 2.0.1-6
- Fix dir-ownership in %%doc

* Fri Dec 30 2016 Björn Esser <bjoern.esser@gmail.com> - 2.0.1-5
- Introduce doc-subpackage
- Use unified %%_pkgdocdir
- Updated Patch0 and use on el <= 6, only
- Rename Patch0 --> Patch 1000
- Clean-up indentation


* Thu Dec 29 2016 Björn Esser <bjoern.esser@gmail.com> - 2.0.1-4
- Include plain ascii-docs, too

* Thu Dec 29 2016 Björn Esser <bjoern.esser@gmail.com> - 2.0.1-3
- Properly build the documentation

* Sun Dec 18 2016 Björn Esser <fedora@besser82.io> - 2.0.1-2
- Run testsuite with threads, too

* Sat Dec 17 2016 Björn Esser <fedora@besser82.io> - 2.0.1-1
- Update to new upstream release v2.0.1
- Introduce libut / libvector
- Add BR: perl

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Björn Esser <bjoern.esser@gmail.com> - 1.9.9-6
- add `%%global debug_package %%{nil}` to avoid empty debuginfo-pkg.

* Thu May 22 2014 Björn Esser <bjoern.esser@gmail.com> - 1.9.9-5
- revert "Root package should be noarch too".
- add provides %%{name} for -devel subpkg.
- add a note about why the mainpkg is arched.

* Wed May 21 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.9.9-4
- Root package should be noarch too

* Wed May 21 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.9.9-3
- Build as noarch

* Sun May 18 2014 Christopher Meng <rpm@cicku.me> - 1.9.9-2
- Move all files to -devel subpkg.

* Sat Mar 29 2014 Christopher Meng <rpm@cicku.me> - 1.9.9-1
- Update to 1.9.9

* Sat Jun 15 2013 Christopher Meng <rpm@cicku.me> - 1.9.8-3
- Add virtual provide.
- Remove 2 wrong tests.

* Fri Jun 14 2013 Christopher Meng <rpm@cicku.me> - 1.9.8-2
- Remove unneeded BR and make files section more clear.

* Sat Jun 01 2013 Christopher Meng <rpm@cicku.me> - 1.9.8-1
- Initial Package.
