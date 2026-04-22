# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global forgeurl https://github.com/akheron/jansson
Version:        2.14
%forgemeta

Name:		jansson
Release: 4%{?dist}
Summary:	C library for encoding, decoding and manipulating JSON data

# src/lookup3.h is LicenseRef-Fedora-Public-Domain
License:	MIT AND LicenseRef-Fedora-Public-Domain
URL:		%{forgeurl}
Source0:	%{forgesource}

# Fix the tests.
# Upstream commit 0677666f65b988b2dd44d02966a08fea490d5883
Patch:          0001-Fix-the-check-exports-tests-for-versioned-symbols.patch

BuildRequires:	gcc
BuildRequires:	python3-sphinx
BuildRequires:  make
BuildRequires:  autoconf, automake, libtool

%description
Small library for parsing and writing JSON documents.

%package devel
Summary: Header files for jansson
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files for developing applications making use of jansson.

%package devel-doc
Summary: Development documentation for jansson
BuildArch: noarch

%description devel-doc
Development documentation for jansson.

%prep
%forgeautosetup -p1

%if 0%{?rhel} == 6
%{__sed} -i 's/code-block:: shell/code-block:: none/g' doc/*.rst
%endif

%build
autoreconf -f -i -v
%configure --disable-static
%make_build
make html

%check
make check

%install
%make_install
rm "$RPM_BUILD_ROOT%{_libdir}"/*.la

%files
%license LICENSE
%doc CHANGES
%{_libdir}/*.so.*

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/*

%files devel-doc
%doc doc/_build/html/*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 22 2024 Richard W.M. Jones <rjones@redhat.com> - 2.14-1
- New upstream version 2.14
- Switch to using forge macros for easier maintenance.
- Fix upstream URL and source.
- Unconditionally run autoreconf.
- Remove obsolete %%ldconfig_scriptlets macro.

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 24 2020 Charalampos Stratakis <cstratak@redhat.com> - 2.13.1-1
- Update to 2.13.1 (#1831402)
- Fix docs build failures with Sphinx 3 (#1823532)
- Use make macros: https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.12-7
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Aug  3 2019 Peter Robinson <pbrobinson@fedoraproject.org> 2.12-4
- Fix build deps, use %%license

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 26 2018 Corey Farrell <git@cfware.com> - 2.12-1
- Update to Jansson 2.12

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Mar 10 2018 Corey Farrell <git@cfware.com> - 2.11-1
- Update to Jansson 2.11

* Mon Feb 19 2018 Jared Smith <jsmith@fedoraproject.org> - 2.10-7
- Add missing BuildRequires on gcc

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.10-5
- Switch to %%ldconfig_scriptlets

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 10 2017 Nathaniel McCallum <npmccallum@redhat.com> - 2.10-2
- Add upstream patch for optional arguments to json_pack()
- Migrate to use autosetup macro

* Thu Mar 02 2017 Nathaniel McCallum <npmccallum@redhat.com> - 2.10-1
- Update to Jansson 2.10

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Sep 20 2016 Nathaniel McCallum <npmccallum@redhat.com> - 2.9-1
- Update to Jansson 2.9

* Fri Sep 16 2016 Nathaniel McCallum <npmccallum@redhat.com> - 2.8-1
- Update to Jansson 2.8
- Add json_auto_t patch

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 05 2015 Jiri Pirko <jpirko@redhat.com> 2.7-1
- Update to Jansson 2.7

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 15 2014 Jiri Pirko <jpirko@redhat.com> 2.6-3
- Create devel-doc package

* Tue Mar 11 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2.6-2
- Package cleanups

* Thu Feb 13 2014 Jared Smith <jsmith@fedoraproject.org> - 2.6-1
- Update to Jansson 2.6 for CVE-2013-6401 

* Sat Jan 25 2014 Jiri Pirko <jpirko@redhat.com> 2.5-1
- Update to Jansson 2.5.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 08 2012 Jiri Pirko <jpirko@redhat.com> 2.4-1
- Update to Jansson 2.4.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 03 2012 Jiri Pirko <jpirko@redhat.com> 2.3-1
- Update to Jansson 2.3.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 11 2011 Sean Middleditch <sean@middleditch.us> 2.1-1
- Update to Jansson 2.1.
- Drop Sphinx patch, no longer necessary.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 03 2010 Sean Middleditch <sean@middleditch.us> 1.3-1
- Update to Jansson 1.3.
- Disable warnings-as-errors for Sphinx documentation.

* Thu Jan 21 2010 Sean Middleditch <sean@middleditch.us> 1.2-1
- Update to Jansson 1.2.

* Thu Jan 11 2010 Sean Middleditch <sean@middleditch.us> 1.1.3-4
- Update jansson description per upstream's suggestions.
- Removed README from docs.

* Thu Jan 09 2010 Sean Middleditch <sean@middleditch.us> 1.1.3-3
- Correct misspelling of jansson in the pkg-config file.

* Thu Jan 09 2010 Sean Middleditch <sean@middleditch.us> 1.1.3-2
- Fix Changelog dates.
- Mix autoheader warning.
- Added make check.
- Build and install HTML documentation in -devel package.

* Thu Jan 07 2010 Sean Middleditch <sean@middleditch.us> 1.1.3-1
- Initial packaging for Fedora.
