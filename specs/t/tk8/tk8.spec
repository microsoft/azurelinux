# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define majorver 8.6
%define vers %{majorver}.16

Summary: The graphical toolkit for the Tcl scripting language, version 8
Name: tk8
Version: %{vers}
Release: 3%{?dist}
Epoch:   1
License: TCL AND HPND-Pbmplus AND CC-BY-SA-3.0 AND MIT-open-group AND MIT
URL: http://tcl.sourceforge.net
Source: http://download.sourceforge.net/sourceforge/tcl/tk%{version}-src.tar.gz
Requires: tcl8 = %{epoch}:%{vers}
BuildRequires: make
BuildRequires: gcc
BuildRequires: tcl8-devel = %{epoch}:%{vers}
BuildRequires: autoconf
BuildRequires: libX11-devel
BuildRequires: libXft-devel
# panedwindow.n from itcl conflicts
Conflicts: itcl <= 3.2
Provides: tile = 0.8.2
Patch: tk-8.6.12-make.patch
Patch: tk-8.6.15-conf.patch
# https://core.tcl-lang.org/tk/tktview/dccd82bdc70dc25bb6709a6c14880a92104dda43
Patch: tk-8.6.10-font-sizes-fix.patch

%description
When paired with the Tcl scripting language, Tk provides a fast and powerful
way to create cross-platform GUI applications.

%package devel
Summary: Tk graphical toolkit development files
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: tcl8-devel = %{epoch}:%{vers}
Requires: libX11-devel libXft-devel
Provides: tk-devel = %{epoch}:%{version}-%{release}
Conflicts: tk-devel >= 1:9.0.0-1

%description devel
When paired with the Tcl scripting language, Tk provides a fast and powerful
way to create cross-platform GUI applications.

The package contains the development files and man pages for tk.

%prep
%autosetup -p1 -n tk%{vers}

%build
cd unix
autoconf
%configure --enable-threads
%make_build CFLAGS="%{optflags}" TK_LIBRARY=%{_datadir}/tk%{majorver}

%check
# do not run "make test" by default since it requires an X display
%{?_with_check: %define _with_check 1}
%{!?_with_check: %define _with_check 0}

%if %{_with_check}
#  make test
%endif

%install
make install -C unix INSTALL_ROOT=%{buildroot} TK_LIBRARY=%{_datadir}/tk%{majorver}

ln -s wish%{majorver} %{buildroot}%{_bindir}/wish8

# for linking with -ltk
ln -s libtk%{majorver}.so %{buildroot}%{_libdir}/libtk.so

mkdir -p %{buildroot}/%{_includedir}/tk-private/{generic/ttk,unix}
find generic unix -name "*.h" -exec cp -p '{}' %{buildroot}/%{_includedir}/tk-private/'{}' ';'
( cd %{buildroot}/%{_includedir}
  for i in *.h ; do
    [ -f %{buildroot}/%{_includedir}/tk-private/generic/$i ] && ln -sf ../../$i %{buildroot}/%{_includedir}/tk-private/generic ;
  done
)

# remove buildroot traces
sed -i -e "s|$PWD/unix|%{_libdir}|; s|$PWD|%{_includedir}/tk-private|" %{buildroot}/%{_libdir}/tkConfig.sh

# rename manual page
mv %{buildroot}/%{_mandir}/man1/wish.1 %{buildroot}/%{_mandir}/man1/wish8.1

# drop the API manual pages, not needed for the compat
rm -f %{buildroot}%{_mandir}/mann/*
rmdir %{buildroot}%{_mandir}/mann

%if 0%{?flatpak}
mkdir -p %{buildroot}%{_usr}/bin
ln -s %{_bindir}/wish8 %{_bindir}/wish%{majorver} %{buildroot}%{_usr}/bin/
%endif

%pre
[ ! -h %{_prefix}/%{_lib}/tk%{majorver} ] || rm %{_prefix}/%{_lib}/tk%{majorver}

%files
%{_bindir}/wish8*
%{_datadir}/tk%{majorver}
%exclude %{_datadir}/tk%{majorver}/tkAppInit.c
%{_libdir}/libtk%{majorver}.so
%{_libdir}/tk%{majorver}
%{_mandir}/man1/*
%if 0%{?flatpak}
%{_usr}/bin/wish8*
%endif
%doc README.md changes
%license license.terms

%files devel
%{_includedir}/*
%{_libdir}/libtk.so
%{_libdir}/libtkstub%{majorver}.a
%{_libdir}/tkConfig.sh
%{_libdir}/pkgconfig/tk.pc
%{_mandir}/man3/*
%{_datadir}/tk%{majorver}/tkAppInit.c

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:8.6.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 09 2025 Jaroslav Škarvada  <jskarvad@redhat.com> - 1:8.6.16-1
- New version
  Related: rhbz#2376818

* Sun Feb  2 2025 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.15-5
- Rebuilt for new gcc

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:8.6.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec 10 2024 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.15-3
- Updated according to the fedora review

* Thu Dec  5 2024 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.15-2
- Initial version based on the tk package
