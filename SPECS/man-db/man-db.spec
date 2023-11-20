Summary:        Programs for finding and viewing man pages
Name:           man-db
Version:        2.10.1
Release:        2%{?dist}
License:        GPLv2+
URL:            https://nongnu.org/man-db
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://download.savannah.nongnu.org/releases/%{name}/%{name}-%{version}.tar.xz
Provides:       man = %{version}-%{release}
Requires:       libpipeline
Requires:       gdbm
Requires:       xz
Requires:       groff
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun):/usr/sbin/userdel /usr/sbin/groupdel
%if %{with_check}
BuildRequires:  shadow-utils
%endif
BuildRequires:  libpipeline-devel
BuildRequires:  gdbm-devel
BuildRequires:  xz
BuildRequires:  groff
Provides:       man-pages-reader = %{version}

%description
The Man-DB package contains programs for finding and viewing man pages.

%prep
%setup -qn %{name}-%{version}
%build
%configure \
    --docdir=%{_defaultdocdir}/%{name}-%{version} \
    --disable-setuid \
    --with-browser=%{_bindir}/lynx \
    --with-systemdsystemunitdir=no \
    --with-vgrind=%{_bindir}/vgrind \
    --with-grap=%{_bindir}/grap

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete
%find_lang %{name} --all-name

# remove zsoelim man page - part of groff package
rm %{buildroot}%{_datadir}/man/man1/zsoelim.1

%check
getent group man >/dev/null || groupadd -r man
getent passwd man >/dev/null || useradd -c "man" -d /var/cache/man -g man \
        -s /bin/false -M -r man
make %{?_smp_mflags} check

%pre
getent group man >/dev/null || groupadd -r man
getent passwd man >/dev/null || useradd -c "man" -d /var/cache/man -g man \
        -s /bin/false -M -r man

%post -p /sbin/ldconfig

%postun
if [ $1 -eq 0 ] ; then
    getent passwd man >/dev/null && userdel man
    getent group man >/dev/null && groupdel man
fi
/sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%license COPYING
%{_sysconfdir}/man_db.conf
%{_bindir}/*
%{_sbindir}/*
%{_libexecdir}/man-db/*
%{_libdir}/man-db/*
%{_defaultdocdir}/%{name}-%{version}/*
%{_mandir}/*/*
%{_libdir}/tmpfiles.d/man-db.conf

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.10.1-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Feb 10 2022 Max Brodeur-Urbas <maxbr@microsoft.com> 2.10.1-1
- Upgrading to v2.10.1
- Correcting COPYING path in file section.
- Adding systemdsystemunitdir=no flag in build configure.
- Correcting source0 URL.

* Wed Jun 09 2021 Muhammad Falak Wani <mwani@microsoft.com> 2.8.4-8
- Add an explict provides for "man-pages-reader"

* Thu May 13 2021 Henry Li <lihl@microsoft.com> 2.8.4-7
- Remove zsoelim man page, which is provided by groff

* Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> 2.8.4-6
- Add explicit provide for "man"

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 2.8.4-5
- Added %%license line automatically

* Fri Apr 17 2020 Emre Girgin <mrgirgin@microsoft.com> 2.8.4-4
- Rename shadow to shadow-utils.

* Tue Apr 07 2020 Joe Schmitt <joschmit@microsoft.com> 2.8.4-3
- Update Source0 with valid URL.
- Update URL.
- Remove sha1 macro.
- License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.8.4-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Oct 22 2018 Sujay G <gsujay@vmware.com> 2.8.4-1
- Bump man-db version to 2.8.4

* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 2.7.6-4
- Remove shadow from requires and use explicit tools for post actions

* Fri Aug 04 2017 Chang Lee <changlee@vmware.com> 2.7.6-3
- Setup a testing environment before %check

* Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 2.7.6-2
- Add gdbm-devel to BuildRequires

* Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 2.7.6-1
- Update package version

* Mon Oct 03 2016 ChangLee <changlee@vmware.com> 2.7.5-5
- Modified check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.7.5-4
- GA - Bump release of all rpms

* Mon May 16 2016 Xiaolin Li <xiaolinl@vmware.com> 2.7.5-3
- Fix user man:man adding.

* Thu May 05 2016 Kumar Kaushik <kaushikk@vmware.com> 2.7.5-2
- Adding support for upgrade in pre/post/un scripts.

* Wed Feb 24 2016 Kumar Kaushik <kaushikk@vmware.com> 2.7.5-1
- Updated to new version.

* Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 2.6.6-2
- Handled locale files with macro find_lang

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.6.6-1
- Initial build. First version
