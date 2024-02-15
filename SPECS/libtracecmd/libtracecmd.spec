Name: libtracecmd
Version: 1.5.1
Release: 3%{?dist}
License: LGPL-2.1-only AND LGPL-2.1-or-later AND GPL-2.0-only AND GPL-2.0-or-later
Summary: A library for reading tracing instances stored in a trace file

URL: https://git.kernel.org/pub/scm/utils/trace-cmd/trace-cmd.git/
Source0: https://git.kernel.org/pub/scm/utils/trace-cmd/trace-cmd.git/snapshot/trace-cmd-libtracecmd-%{version}.tar.gz#/%{name}-%{version}.tar.gz

ExcludeArch: %{ix86} %{arm}

BuildRequires: make
BuildRequires: gcc
BuildRequires: xmlto
BuildRequires: asciidoc
BuildRequires: mlocate
BuildRequires: graphviz doxygen
BuildRequires: libxml2-devel
BuildRequires: gcc-c++
BuildRequires: freeglut-devel
BuildRequires: json-c-devel
BuildRequires: libtraceevent-devel >= 1.8.0
BuildRequires: libtracefs-devel >= 1.8.0
BuildRequires: chrpath
BuildRequires: libzstd-devel

%description
A library containing functions for getting information and reading
tracing instances stored in a trace file that can be used without the
trace-cmd application.

%package -n libtracecmd-devel
Summary: Development files for libtracecmd
Requires: libtracecmd%{_isa} = %{version}-%{release}

%description -n libtracecmd-devel
Development files of the libtracecmd library

%prep
%autosetup -n trace-cmd-libtracecmd-%{version}

%build
# MANPAGE_DOCBOOK_XSL define is hack to avoid using locate
MANPAGE_DOCBOOK_XSL=`rpm -ql docbook-style-xsl | grep manpages/docbook.xsl`
CFLAGS="%{optflags} -D_GNU_SOURCE" LDFLAGS="%{build_ldflags}" BUILD_TYPE=Release \
  make V=9999999999 MANPAGE_DOCBOOK_XSL=$MANPAGE_DOCBOOK_XSL \
  prefix=%{_prefix} libdir=%{_libdir} %{?_smp_mflags}\
  PYTHON_VERS=python3 libs doc

%install
make libdir=%{_libdir} prefix=%{_prefix} V=1 DESTDIR=%{buildroot}/ CFLAGS="%{optflags} -D_GNU_SOURCE" LDFLAGS="%{build_ldflags} -z muldefs " BUILD_TYPE=Release install_libs install_doc
# Remove trace-cmd man pages and docs, leaving only the libtracecmd ones, as there are no separate makefile target for libtracecmd documents
find %{buildroot}%{_mandir} -iname trace-cmd\* -exec rm -rf {} \;
rm -rf %{buildroot}/%{_docdir}/trace-cmd
chrpath --delete %{buildroot}/%{_libdir}/libtracecmd.so*

%files
%license COPYING COPYING.LIB
%doc README
%{_libdir}/libtracecmd.so.1
%{_libdir}/libtracecmd.so.1.5.1
%{_docdir}/libtracecmd-doc
%{_mandir}/man3/libtracecmd*
%{_mandir}/man3/tracecmd*

%files -n libtracecmd-devel
%{_libdir}/pkgconfig/libtracecmd.pc
%{_libdir}/libtracecmd.so
%{_includedir}/trace-cmd

%changelog
* Thu Feb 15 2024 Aadhar Agarwal <aadagarwal@microsoft.com> - 1.5.1-3
- Initial CBL-Mariner import from Fedora 40 (license: MIT)
- License Verified

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 23 2024 Zamir SUN <sztsian@gmail.com> - 1.5.1-1
- Update to 1.5.1

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 05 2023 Zamir SUN <sztsian@gmail.com> - 1.3.1-2
- SPDX migration

* Tue Apr 18 2023 Zamir SUN <sztsian@gmail.com> - 1.3.1-1
- Update to 1.3.1

* Fri Mar 31 2023 Jerome Marchand <jmarchan@redhat.com> - 1.2.0-3
- Fix build: RHBZ#2171769

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Oct 11 2022 Zamir SUN <sztsian@gmail.com> - 1.2.0-1
- Update to 1.2.0

* Thu Sep 8 2022 Zamir SUN <sztsian@gmail.com> - 1.1.3-4
- Add zstd support
- Fixes: RHBZ#2121037

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Apr 15 2022 Zamir SUN <sztsian@gmail.com> - 1.1.3-2
- Rebuild with newer libtraceevent

* Wed Apr 13 2022 Zamir SUN <sztsian@gmail.com> - 1.1.3-1
- Update to 1.1.3

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Apr 19 2021 Zamir SUN <sztsian@gmail.com> - 1.1.0-1
- Initial libtracecmd 1.1.0