Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           compat-lua
Version:        5.1.5
Release:        17%{?dist}
Summary:        Powerful light-weight programming language (compat version)
License:        MIT
URL:            https://www.lua.org/
Source0:        https://www.lua.org/ftp/lua-%{version}.tar.gz
Patch0:         lua-5.1.4-autotoolize.patch
Patch1:         lua-5.1.4-lunatic.patch
Patch2:         lua-5.1.4-idsize.patch
Patch3:         lua-5.1.4-pc-compat.patch
BuildRequires:  readline-devel ncurses-devel libtool
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Provides:       lua = 5.1
Provides:       lua5.1 = %{version}-%{release}
Provides:       lua5.1%{?_isa} = %{version}-%{release}

%description
This package contains a compatibility version of the lua-5.1 binaries.


%package libs
Summary:        Powerful light-weight programming language (compat version)
Provides:       lua(abi) = 5.1
Provides:       lua5.1-libs = %{version}-%{release}
Provides:       lua5.1-libs%{?_isa} = %{version}-%{release}

%description libs
This package contains a compatibility version of the lua-5.1 libraries.


%package devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Provides:       lua5.1-devel = %{version}-%{release}
Provides:       lua5.1-devel%{?_isa} = %{version}-%{release}

%description devel
This package contains development files for compat-lua-libs.


%prep
%setup -q -n lua-%{version}
%patch 0 -p1 -E -z .autoxxx
%patch 1 -p0 -z .lunatic
%patch 2 -p1 -z .idsize
%patch 3 -p1
# fix perms on auto files
chmod u+x autogen.sh config.guess config.sub configure depcomp install-sh missing
# Avoid make doing auto-reconf itself, killing our rpath removal in the process
autoreconf -i -f


%build
%configure --with-readline
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# hack so that only /usr/bin/lua gets linked with readline as it is the
# only one which needs this and otherwise we get License troubles
make %{?_smp_mflags} LIBS="-lm -ldl" luac_LDADD="liblua.la -lm -ldl"
# also remove readline from lua.pc
sed -i 's/-lreadline -lncurses //g' etc/lua.pc


%install
%make_install
rm $RPM_BUILD_ROOT%{_libdir}/liblua.{a,la}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/lua/5.1
mkdir -p $RPM_BUILD_ROOT%{_datadir}/lua/5.1
# Rename some files to avoid conflicts with 5.2
mv $RPM_BUILD_ROOT%{_bindir}/lua $RPM_BUILD_ROOT%{_bindir}/lua-5.1
mv $RPM_BUILD_ROOT%{_bindir}/luac $RPM_BUILD_ROOT%{_bindir}/luac-5.1
mv $RPM_BUILD_ROOT%{_mandir}/man1/lua.1 \
  $RPM_BUILD_ROOT%{_mandir}/man1/lua-5.1.1
mv $RPM_BUILD_ROOT%{_mandir}/man1/luac.1 \
  $RPM_BUILD_ROOT%{_mandir}/man1/luac-5.1.1
mkdir -p $RPM_BUILD_ROOT%{_includedir}/lua-5.1
mv $RPM_BUILD_ROOT%{_includedir}/l*h* $RPM_BUILD_ROOT%{_includedir}/lua-5.1
rm $RPM_BUILD_ROOT%{_libdir}/liblua.so
mv $RPM_BUILD_ROOT%{_libdir}/pkgconfig/lua.pc \
  $RPM_BUILD_ROOT%{_libdir}/pkgconfig/lua-5.1.pc


%ldconfig_scriptlets libs


%files
%{_bindir}/lua-5.1
%{_bindir}/luac-5.1
%{_mandir}/man1/lua*5.1.1*

%files libs
%doc COPYRIGHT HISTORY README doc/*.html doc/*.css doc/*.gif doc/*.png
%{_libdir}/liblua-5.1.so
%dir %{_libdir}/lua
%dir %{_libdir}/lua/5.1
%dir %{_datadir}/lua
%dir %{_datadir}/lua/5.1

%files devel
%{_includedir}/lua-5.1/
%{_libdir}/pkgconfig/lua-5.1.pc


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.1.5-17
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.5-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Robert Scheck <robert@fedoraproject.org> - 5.1.5-15
- Provide lua5.1 for https://pagure.io/packaging-committee/issue/878

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.5-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5.1.5-13
- Rebuild for readline 8.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 5.1.5-6
- Rebuild for readline 7.x

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 25 2015 Yaakov Selkowitz <yselkowi@redhat.com> - 5.1.5-4
- Also use lib64 instead of lib on aarch64

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 19 2014 Hans de Goede <hdegoede@redhat.com> - 5.1.5-1
- Rebase to 5.1.5 (rhbz#1111013)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug  3 2013 Hans de Goede <hdegoede@redhat.com> - 5.1.4-5
- New Fedora package with full lua-5.1 for use with applications not yet
  ported to 5.2
- Release fields start at 5 to be newer the compat-lua-libs from the
  non-compat lua package
