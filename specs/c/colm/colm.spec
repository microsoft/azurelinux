# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           colm
Version:        0.14.7
Release:        10%{?dist}
Summary:        Programming language designed for the analysis of computer languages

# aapl/ and some headers from src/ are the LGPLv2+
# Automatically converted from old format: MIT and LGPLv2+ - review is highly recommended.
License:        LicenseRef-Callaway-MIT AND LicenseRef-Callaway-LGPLv2+
URL:            https://www.colm.net/open-source/colm/
Source0:        https://www.colm.net/files/%{name}/%{name}-%{version}.tar.gz
Patch0:		fc61ecb3a22b89864916ec538eaf04840e7dd6b5.diff
# backport commit that allows AC_CHECK_LIB to detect libfsm
Patch1:         https://github.com/adrian-thurston/colm/commit/28b6e0a01157049b4cb279b0ef25ea9dcf3b46ed.patch#/%{name}-libfsm-ac_check_lib.diff
# Correctly use off_t in cookie_seek_function_t in src/stream.c
Patch2:         colm-0.14.7-ac_sys_largefile-for-off_t.patch
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  asciidoc

# Unfortunately, upstream doesn't exist and not possible to find version
Provides:       bundled(aapl)

%description
Colm is a programming language designed for the analysis and transformation
of computer languages. Colm is influenced primarily by TXL. It is
in the family of program transformation languages.

%package devel
Summary:        Development libraries and header files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
%{summary}.

%prep
%autosetup -p1
# Do not pollute with docs
sed -i -e "/dist_doc_DATA/d" Makefile.am
# Remove incompatible SIZEOF_LONG definition
sed -i -e '\@SIZEOF_LONG@d' test/rlparse.d/config.h

%build
autoreconf -vfi
%configure --disable-static
%make_build

%install
%make_install
find %{buildroot}%{_libdir} -type f -name '*.la' -print -delete
install -p -m 0644 -D %{name}.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax/%{name}.vim

%ldconfig_scriptlets

%files
%license COPYING
%doc README
%{_bindir}/%{name}*
%{_libdir}/lib%{name}-%{version}.so
%dir %{_datadir}/vim
%dir %{_datadir}/vim/vimfiles
%dir %{_datadir}/vim/vimfiles/syntax
%{_datadir}/vim/vimfiles/syntax/%{name}.vim
%{_datadir}/doc/%{name}/*
%{_datadir}/*.lm
%{_datadir}/runtests

%files devel
%{_libdir}/lib%{name}.so
%{_libdir}/libfsm*
%{_includedir}/%{name}/
%{_includedir}/libfsm*
%{_includedir}/aapl*


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 23 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.14.7-8
- Correctly use off_t in cookie_seek_function_t especially on 32bit
- Remove incompatible SIZEOF_LONG definition in test suite

* Wed Aug 28 2024 Miroslav Suchý <msuchy@redhat.com> - 0.14.7-7
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon May 08 2023 Michel Alexandre Salim <salimma@fedoraproject.org> - 0.14.7-2
- Backport commit that allows AC_CHECK_LIB to detect libfsm

* Tue Apr 25 2023 Filipe Rosset <rosset.filipe@gmail.com> - 0.14.7-1
- Update to 0.14.7 fixes rhbz#1825150

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jul 28 2019 Christian Glombek <lorbus@fedoraproject.org> - 0.13.0.7-1
- Updated to version 0.13.0.7

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jul 06 2018 Christian Glombek <lorbus@fedoraproject.org> - 0.13.0.6-1
- Updated to version 0.13.0.6

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Dec 10 2017 Jason Taylor <jtfas90@gmail.com> - 0.13.0.5-1
- Upstream bugfix release
- Correction to spec license add MIT license
- Added asciidoc BuildRequires and docdir files

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 01 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.13.0.4-1
- Initial package
