# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# git tag
#%%global commit 5dd505f3aba255c5fbc2a6dbed57fcba51b400f6
#%%global commitdate 20201009
#%%global shortcommit %%(c=%%{commit}; echo ${c:0:7})

Name: libtraceevent
Version: 1.8.4
Release: 4%{?dist}
License: LGPL-2.1-only AND LGPL-2.1-or-later AND GPL-2.0-only AND GPL-2.0-or-later
Summary: Library to parse raw trace event formats

URL: https://git.kernel.org/pub/scm/libs/libtrace/libtraceevent.git/
# If upstream does not provide tarballs, to generate:
# git clone git://git.kernel.org/pub/scm/libs/libtrace/libtraceevent.git
# cd libtraceevent
# git archive --prefix=libtraceevent-%%{version}/ -o libtraceevent-%%{version}.tar.gz %%{git_commit}
#Source0: libtraceevent-%%{version}.tar.gz
Source0: https://git.kernel.org/pub/scm/libs/libtrace/libtraceevent.git/snapshot/libtraceevent-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires: xmlto
BuildRequires: asciidoc

%global __provides_exclude_from ^%{_libdir}/traceevent/plugins


%description
libtraceevent is a library to parse raw trace event formats.

%package devel
Summary: Development headers of %{name}
Requires: %{name}%{_isa} = %{version}-%{release}

%description devel
Development headers of %{name}-libs

%prep
%setup -q

%build
MANPAGE_DOCBOOK_XSL=`rpm -ql docbook-style-xsl | grep manpages/docbook.xsl`
# Parallel build does not work
make -O -j1 V=1 VERBOSE=1 CFLAGS="%{build_cflags}" LDFLAGS="%{build_ldflags}" prefix=%{_prefix} libdir=%{_libdir} MANPAGE_XSL=%{MANPAGE_DOCBOOK_XSL} all doc

%install
%make_install prefix=%{_prefix} libdir=%{_libdir} install doc-install
rm -rf %{buildroot}/%{_libdir}/libtraceevent.a

%files
%license LICENSES/LGPL-2.1
%license LICENSES/GPL-2.0
%{_libdir}/traceevent/
%{_libdir}/libtraceevent.so.%{version}
%{_libdir}/libtraceevent.so.1
%{_mandir}/man3/tep_*.3.*
%{_mandir}/man3/libtraceevent.3.*
%{_mandir}/man3/trace_seq*.3.*
%{_mandir}/man3/kbuffer_*.3.gz
%{_docdir}/%{name}-doc

%files devel
%{_includedir}/traceevent/
%{_libdir}/libtraceevent.so
%{_libdir}/pkgconfig/libtraceevent.pc

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 17 2024 Zamir SUN <sztsian@gmail.com> - 1.8.4-1
- Update to 1.8.4

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 18 2024 Jerome Marchand <jmarchan@redhat.com> - 1.8.2-3
- Use the distribution building flags

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 23 2024 Zamir SUN <sztsian@gmail.com> - 1.8.2-1
- Update to 1.8.2 (#2213358)

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 05 2023 Zamir SUN <sztsian@gmail.com> - 1.7.2-2
- SPDX migration

* Wed Apr 05 2023 Zamir SUN <sztsian@gmail.com> - 1.7.2-1
- Update to 1.7.2

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Oct 11 2022 Zamir SUN <sztsian@gmail.com> - 1.6.3-1
- Update to 1.6.3

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Apr 15 2022 Zamir SUN <sztsian@gmail.com> - 1.5.3-2
- Disable parallel compile

* Thu Apr 14 2022 Zamir SUN <sztsian@gmail.com> - 1.5.3-1
- Update to 1.5.3

* Tue Feb 15 2022 Zamir SUN <sztsian@gmail.com> - 1.5.0-1
- Update to 1.5.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 07 2021 Justin Forbes <jforbes@fedoraproject.org>
- Remove erroneus "Conflicts: perf" which broke perf.

* Mon Apr 19 2021 Zamir SUN <sztsian@gmail.com> - 1.2.1-1
- Update to 1.2.1

* Mon Feb 08 2021 Zamir SUN <sztsian@gmail.com> - 1.1.1-1
- Update to 1.1.1

* Sat Oct 17 2020 Zamir SUN <sztsian@gmail.com> - 1.1.0-1
- Update to 1.1.0

* Fri Oct 09 2020 Zamir SUN <sztsian@gmail.com> - 0-0.1.20201009git5dd505f
- Initial libtraceevent

