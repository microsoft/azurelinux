## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 12;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pkg  anthy-unicode
%bcond_without autoreconf

%if (0%{?fedora} > 35 || 0%{?rhel} > 7)
%bcond_with    xemacs
%else
%bcond_without xemacs
%endif


Name:  anthy-unicode
Version: 1.0.0.20240502
Release: %autorelease
# The entire source code is LGPLv2+ and dictionaries is GPLv2. the corpus data is under Public Domain.
License: LGPL-2.0-or-later AND GPL-2.0-or-later AND LicenseRef-Fedora-Public-Domain
URL:  https://github.com/fujiwarat/anthy-unicode/wiki
BuildRequires: emacs
BuildRequires: gcc
BuildRequires: git
%if %{with xemacs}
BuildRequires: xemacs
# overlay.el is required by anthy-unicode.el and anthy-unicode-isearch.el
BuildRequires: xemacs-packages-extra
%endif
%if %{with autoreconf}
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: make
%endif

Source0: https://github.com/fujiwarat/anthy-unicode/releases/download/%{version}/%{name}-%{version}.tar.gz
Source1: https://github.com/fujiwarat/anthy-unicode/releases/download/%{version}/%{name}-%{version}.tar.gz.sum
Source2: %{name}-init.el
# Upstreamed patches
#Patch0: %%{name}-HEAD.patch
Patch0: %{name}-HEAD.patch

Summary: Japanese character set input library for Unicode

%description
Anthy Unicode is another Anthy project and provides the library to input
Japanese on the applications, such as X applications and emacs. and the
user dictionaries and the users information which is used for the conversion,
is stored into their own home directory. So Anthy Unicode is secure than
other conversion server.

%package -n emacs-%{pkg}
Summary: Emacs files for %{pkg}
Requires: %{name} = %{version}-%{release}
Requires: emacs-filesystem >= %{_emacs_version}
BuildArch: noarch

%description -n emacs-%{pkg}
This package contains the byte compiled elips packages to run %{pkg}
with GNU Emacs.

%if %{with xemacs}
%package -n xemacs-%{pkg}
Summary: XEmacs files for %{pkg}
Requires: %{name} = %{version}-%{release}
Requires: xemacs-filesystem >= %{_xemacs_version}
BuildArch: noarch

%description -n xemacs-%{pkg}
This package contains the elips packages to run %{pkg} with GNU XEmacs.
%endif

%package devel
Summary: Header files and library for developing programs which uses Anthy Unicode
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
The anthy-devel package contains the development files which is needed to build
the programs which uses Anthy Unicode.


%prep
SAVED_SUM=$(grep sha512sum %SOURCE1 | awk '{print $2}')
MY_SUM=$(sha512sum %SOURCE0 | awk '{print $1}')
if test x"$SAVED_SUM" != x"$MY_SUM" ; then
    abort
fi
%autosetup -S git

%build
%if %{with autoreconf}
autoreconf -f -i -v
%endif
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# remove unnecessary files
rm $RPM_BUILD_ROOT%{_libdir}/lib*.la

pushd ./src-util
install -m 644 dic-tool-input $RPM_BUILD_ROOT%{_datadir}/%{pkg}
install -m 644 dic-tool-result $RPM_BUILD_ROOT%{_datadir}/%{pkg}
popd

## for emacs-anthy
mkdir -p $RPM_BUILD_ROOT%{_emacs_sitestartdir}
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_emacs_sitestartdir}

%if %{with xemacs}
## for xemacs-anthy
mkdir -p $RPM_BUILD_ROOT%{_xemacs_sitestartdir}
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_xemacs_sitestartdir}
# FIXME lisp build
pushd ./src-util
make clean
#make EMACS=xemacs lispdir="%%{_xemacs_sitelispdir}/%%{pkg}"
# The latest /usr/share/automake-*/am/lisp.am calls -L option for
# $(EMACS) --batch but -L is not supported by xemacs.
# Copy elisp-comp script here from old automake
xemacs --batch --eval '(setq load-path (cons nil load-path))' -f batch-byte-compile *.el
make
make install-lispLISP DESTDIR=$RPM_BUILD_ROOT EMACS=xemacs lispdir="%{_xemacs_sitelispdir}/%{pkg}" INSTALL="install -p"
popd
%endif

%check
sed -e "s|@datadir@|$PWD|" -e "s|@PACKAGE@|mkanthydic|" \
  anthy-unicode.conf.in > test.conf
_TEST_ENV="LD_LIBRARY_PATH=$PWD/src-main/.libs:$PWD/src-worddic/.libs"
_TEST_ENV="$_TEST_ENV CONFFILE=$PWD/test.conf"
cd test
env $_TEST_ENV ./anthy --all
env $_TEST_ENV ./checklib
cd ../src-util
env $_TEST_ENV ./anthy-dic-tool-unicode --load dic-tool-input
diff $HOME/.config/anthy/private_words_default dic-tool-result
env $_TEST_ENV ./anthy-dic-tool-unicode --dump
mkdir -p $HOME/.anthy
mv $HOME/.config/anthy/private_words_default $HOME/.anthy
env $_TEST_ENV ./anthy-dic-tool-unicode --migrate
diff $HOME/.config/anthy/private_words_default dic-tool-result
cd ..


%ldconfig_scriptlets

%files
%doc AUTHORS ChangeLog DIARY NEWS README
%license COPYING
%{_bindir}/*
# If new keywords are added in conf files, "noreplace" flag needs to be deleted
%config(noreplace) %{_sysconfdir}/*.conf
%{_libdir}/lib*.so.*
%{_datadir}/%{pkg}/

%files -n emacs-%{pkg}
%doc doc/ELISP
%{_emacs_sitelispdir}/%{pkg}/*.el
%{_emacs_sitelispdir}/%{pkg}/*.elc
%{_emacs_sitestartdir}/*.el
%dir %{_emacs_sitelispdir}/%{pkg}

%if %{with xemacs}
%files -n xemacs-%{pkg}
%doc doc/ELISP
%{_xemacs_sitelispdir}/%{pkg}/*.el
%if %{with xemacs}
%{_xemacs_sitelispdir}/%{pkg}/*.elc
%endif
%{_xemacs_sitestartdir}/*.el
%dir %{_xemacs_sitelispdir}/%{pkg}
%endif

%files devel
%doc doc/DICLIB doc/DICUTIL doc/GLOSSARY doc/GRAMMAR doc/GUIDE.english doc/ILIB doc/LEARNING doc/LIB doc/MISC doc/POS doc/SPLITTER doc/TESTING doc/protocol.txt
%{_datadir}/%{pkg}/dic-tool-input
%{_datadir}/%{pkg}/dic-tool-result
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc


%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 1.0.0.20240502-12
- Latest state for anthy-unicode

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0.20240502-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0.20240502-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Aug 17 2024 Takao Fujiwara <tfujiwar@redhat.com> - 1.0.0.20240502-9
- Delete unnecessary packages in CI

* Fri Aug 16 2024 Takao Fujiwara <tfujiwar@redhat.com> - 1.0.0.20240502-8
- Revert to drop emacs.i686

* Fri Aug 16 2024 Takao Fujiwara <tfujiwar@redhat.com> - 1.0.0.20240502-7
- Implement CI with TMT
- Add dic-tool-* test files to devel package

* Fri Aug 16 2024 Takao Fujiwara <tfujiwar@redhat.com> - 1.0.0.20240502-6
- Delete CI with STI

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0.20240502-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 15 2024 Takao Fujiwara <tfujiwar@redhat.com> - 1.0.0.20240502-4
- Fix some compiler warnings
- src-main/context.c: Fix warning[-Waddress] &ce->str will always evaluate
  as 'true'
- mkworddic/mkdic.c: Fix warning[-Wformat-overflow=] '%%s' directive
  argument is null

* Sat Jul 13 2024 Takao Fujiwara <tfujiwar@redhat.com> - 1.0.0.20240502-3
- Drop emacs.i686

* Fri Jul 12 2024 Takao Fujiwara <tfujiwar@redhat.com> - 1.0.0.20240502-2
- Fix license-validate

* Thu May 02 2024 Takao Fujiwara <tfujiwar@redhat.com> - 1.0.0.20240502-1
- Bump to 1.0.0.20240502

* Thu May 02 2024 Takao Fujiwara <tfujiwar@redhat.com> - 1.0.0.20211224-15
- Delete upstreamed anthy-unicode-HEAD.patch

* Thu Mar 14 2024 Takao Fujiwara <fujiwara@redhat.com> 1.0.0.20211224-13
- Resolves #2269401 Fix おきのえらぶ in gcanna.ctd

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0.20211224-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0.20211224-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0.20211224-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0.20211224-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 16 2022 Takao Fujiwara <fujiwara@redhat.com> 1.0.0.20211224-8
- Migrate license tag to SPDX

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0.20211224-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Takao Fujiwara <fujiwara@redhat.com> 1.0.0.20211224-6
- Rename master_dic_file to main_dic_file

* Fri May 06 2022 Takao Fujiwara <fujiwara@redhat.com> 1.0.0.20211224-5
- Fix GCC_ANALYZER_WARNING with -Wanalyzer-null-dereference

* Fri Feb 11 2022 Takao Fujiwara <fujiwara@redhat.com> 1.0.0.20211224-4
- Resolves: #2051670 xemacs is a dead package

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0.20211224-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 24 2021 Takao Fujiwara <fujiwara@redhat.com> 1.0.0.20211224-1
- Bump to 1.0.0.20211224-1

* Tue Oct 26 2021 Takao Fujiwara <fujiwara@redhat.com> 1.0.0.20201109-10
- Resolves: #1998727 Fix emacs-anthy-unicode

* Thu Oct 21 2021 Takao Fujiwara <fujiwara@redhat.com> 1.0.0.20201109-8
- Resolves: #2007482 Update gcanna.ctd with Shubitai

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0.20201109-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 13 2021 Takao Fujiwara <fujiwara@redhat.com> 1.0.0.20201109-6
- Fix covscan report

* Mon Jul 12 2021 Takao Fujiwara <fujiwara@redhat.com> 1.0.0.20201109-5
- Fix covscan report

* Mon May 03 2021 Takao Fujiwara <fujiwara@redhat.com> 1.0.0.20201109-4
- Delete unnecessary xemacs in tests/tests.yml

* Sat May 01 2021 Takao Fujiwara <fujiwara@redhat.com> 1.0.0.20201109-3
- Enable CI

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0.20201109-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 09 2020 Takao Fujiwara <fujiwara@redhat.com> 1.0.0.20201109-1
- Bump 1.0.0.20201109

* Fri Jul 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0.20191015-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0.20191015-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0.20191015-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Oct 21 2019 Takao Fujiwara <fujiwara@redhat.com> 1.0.0.20191015-2
- Add %%check to run local test programs

* Tue Oct 15 2019 Takao Fujiwara <fujiwara@redhat.com> 1.0.0.20191015-1
- Release anthy-unicode 1.0.0.20191015

* Wed Aug 07 2019 Takao Fujiwara <fujiwara@redhat.com> 1.0.0.20190412-1
- Initial package
- Update license
- Delete Group tags
- Make parse_modify_freq_command() for UTF-8
- Revert ptab.h to EUC-JP
- BuildRequire: git
- Genearate emacs- and xemacs- sub packages
- Fix some obsolete warnings in emacs batch-byte-compile
- Fix shared-lib-calls-exit
- Fix non-conffile-in-etc
- Fix description-line-too-long

## END: Generated by rpmautospec
