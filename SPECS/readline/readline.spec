Summary:        Command-line editing and history capabilities
Name:           readline
Version:        8.2
Release:        1%{?dist}
License:        GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://tiswww.case.edu/php/chet/readline/rltop.html
Source0:        https://ftp.gnu.org/gnu/readline/%{name}-%{version}.tar.gz
BuildRequires:  ncurses-devel
Requires:       ncurses-libs

%description
The Readline package is a set of libraries that offers command-line
editing and history capabilities.

%package        devel
Summary:        Header and development files for readline
Requires:       %{name} = %{version}

%description        devel
It contains the libraries and header files to create applications

%prep
%setup -q
sed -i '/MV.*old/d' Makefile.in
sed -i '/{OLDSUFF}/c:' support/shlib-install

%build
./configure \
    --prefix=%{_prefix} \
    --disable-silent-rules
make SHLIB_LIBS=-lncursesw

%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}%{_libdir}
ln -sfv ../..%{_libdir}/$(readlink %{buildroot}%{_libdir}/libreadline.so) %{buildroot}%{_libdir}/libreadline.so
ln -sfv ../..%{_libdir}/$(readlink %{buildroot}%{_libdir}/libhistory.so ) %{buildroot}%{_libdir}/libhistory.so
install -vdm 755 %{buildroot}%{_defaultdocdir}/%{name}-%{version}
install -v -m644 doc/*.{ps,pdf,html,dvi} %{buildroot}%{_defaultdocdir}/%{name}-%{version}
rm -rf %{buildroot}%{_infodir}

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/libreadline.so.8
%{_libdir}/libhistory.so.8
%{_libdir}/libhistory.so.%{version}
%{_libdir}/libreadline.so.%{version}

%files devel
%{_includedir}/%{name}/keymaps.h
%{_includedir}/%{name}/history.h
%{_includedir}/%{name}/rlstdc.h
%{_includedir}/%{name}/chardefs.h
%{_includedir}/%{name}/readline.h
%{_includedir}/%{name}/rlconf.h
%{_includedir}/%{name}/rltypedefs.h
%{_includedir}/%{name}/tilde.h
%{_libdir}/libreadline.a
%{_libdir}/libhistory.a
%{_libdir}/libhistory.so
%{_libdir}/libreadline.so
%{_datadir}/%{name}/hist_purgecmd.c
%{_datadir}/%{name}/rlbasic.c
%{_datadir}/%{name}/rltest.c
%{_datadir}/%{name}/rlversion.c
%{_datadir}/%{name}/rlptytest.c
%{_datadir}/%{name}/rlevent.c
%{_datadir}/%{name}/rl-callbacktest.c
%{_datadir}/%{name}/rlcat.c
%{_datadir}/%{name}/histexamp.c
%{_datadir}/%{name}/rl-fgets.c
%{_datadir}/%{name}/rl.c
%{_datadir}/%{name}/excallback.c
%{_datadir}/%{name}/manexamp.c
%{_datadir}/%{name}/hist_erasedups.c
%{_datadir}/%{name}/fileman.c
%{_datadir}/%{name}/rlkeymaps.c
%{_datadir}/%{name}/rl-timeout.c
%{_docdir}/%{name}/INSTALL
%{_docdir}/%{name}/README
%{_docdir}/%{name}/CHANGES
%{_docdir}/%{name}-%{version}/readline.html
%{_docdir}/%{name}-%{version}/readline.dvi
%{_docdir}/%{name}-%{version}/history.pdf
%{_docdir}/%{name}-%{version}/rluserman.html
%{_docdir}/%{name}-%{version}/rluserman.dvi
%{_docdir}/%{name}-%{version}/history.dvi
%{_docdir}/%{name}-%{version}/readline.ps
%{_docdir}/%{name}-%{version}/history.ps
%{_docdir}/%{name}-%{version}/rluserman.ps
%{_docdir}/%{name}-%{version}/readline.pdf
%{_docdir}/%{name}-%{version}/history_3.ps
%{_docdir}/%{name}-%{version}/readline_3.ps
%{_docdir}/%{name}-%{version}/history.html
%{_docdir}/%{name}-%{version}/rluserman.pdf
%{_mandir}/man3/history.3.gz
%{_mandir}/man3/readline.3.gz
%{_libdir}/pkgconfig/readline.pc
%{_libdir}/pkgconfig/history.pc

%changelog
* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.2-1
- Auto-upgrade to 8.2 - Azure Linux 3.0 - package upgrades

* Mon Nov 22 2021 Andrew Phelps <anphel@microsoft.com> 8.1-1
- Update to version 8.1
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 7.0-4
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 7.0-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sun Jun 04 2017 Bo Gan <ganb@vmware.com> 7.0-2
- Fix dependency

* Fri Jan 13 2017 Dheeraj Shetty <dheerajs@vmware.com> 7.0-1
- Updated to version 7.0

* Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> 6.3-6
- Move docs and man to the devel package

* Tue Oct 04 2016 ChangLee <changlee@vmware.com> 6.3-5
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.3-4
- GA - Bump release of all rpms

* Wed Jun 3 2015 Divya Thaluru <dthaluru@vmware.com> 6.3-3
- Adding ncurses to run time require package

* Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 6.3-2
- Update according to UsrMove.

* Wed Oct 22 2014 Divya Thaluru <dthaluru@vmware.com> 6.3-1
- Initial build.    First version
