%global gangver     3.7.2
%global webver      3.7.5

%global systemd         1
%global _hardened_build 1

%if 0%{?rhel} && 0%{?rhel} < 8
%global py2             1
%endif

Summary:            Distributed Monitoring System
Name:               ganglia
Version:            %{gangver}
Release:            41%{?dist}
License:            MPL
URL:                http://ganglia.sourceforge.net/
Source0:            http://downloads.sourceforge.net/sourceforge/ganglia/ganglia-%{version}.tar.gz
Source1:            https://github.com/ganglia/ganglia-web/archive/%{webver}/ganglia-web-%{webver}.tar.gz
Source2:            gmond.service
Source3:            gmetad.service
Source4:            ganglia-httpd24.conf.d
Source5:            ganglia-httpd.conf.d
Source6:            conf.php
Patch0:             ganglia-web-3.7.2-path.patch
Patch1:             ganglia-3.7.2-apache.patch
Patch2:             ganglia-3.7.2-sflow.patch
Patch3:             ganglia-3.7.2-tirpc-hack.patch
Patch4:             ganglia-web-5ee6b7.patch
Vendor:             Microsoft Corporation
%if 0%{?systemd}
BuildRequires:      systemd
%endif
%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires:      rpcgen
BuildRequires:      libtirpc-devel
BuildRequires:      autoconf
BuildRequires:      automake
BuildRequires:      libtool
%endif
BuildRequires:      apr-devel >= 1
BuildRequires:      cyrus-sasl-devel
BuildRequires:      expat-devel
BuildRequires:      freetype-devel
BuildRequires:      gcc
BuildRequires:      libart_lgpl-devel
BuildRequires:      libconfuse-devel
BuildRequires:      libmemcached-devel
BuildRequires:      libpng-devel
BuildRequires:      make
%if 0%{?fedora} < 38 || 0%{?rhel}
BuildRequires:      pcre-devel
%endif
%{?py2:BuildRequires:      python2-devel}
BuildRequires:      rrdtool-devel
BuildRequires:      rsync
BuildRequires:      /usr/bin/pod2man
BuildRequires:      /usr/bin/pod2html
%description
Ganglia is a scalable, real-time monitoring and execution environment
with all execution requests and statistics expressed in an open
well-defined XML format.

%package            web
Summary:            Ganglia Web Frontend
Version:            %{webver}
Requires:           rrdtool
Requires:           php
Requires:           php-gd
Requires:           %{name}-gmetad = %{gangver}-%{release}
%if 0%{?fedora} || 0%{?rhel} > 7
Requires:           php-xml
%endif
%description        web
This package provides a web frontend to display the XML tree published
by ganglia, and to provide historical graphs of collected
metrics. This website is written in the PHP.

%package            gmetad
Summary:            Ganglia Metadata collection daemon
Requires:           %{name} = %{gangver}-%{release}
%if 0%{?systemd}
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd
%else
Requires(post):     /sbin/chkconfig
Requires(preun):    /sbin/chkconfig
Requires(preun):    /sbin/service
%endif
%description        gmetad
Ganglia is a scalable, real-time monitoring and execution environment
with all execution requests and statistics expressed in an open
well-defined XML format.

This gmetad daemon aggregates monitoring data from several clusters to
form a monitoring grid. It also keeps metric history using rrdtool.

%package            gmond
Summary:            Ganglia Monitoring daemon
Requires:           %{name} = %{gangver}-%{release}
%if 0%{?systemd}
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd
%else
Requires(post):     /sbin/chkconfig
Requires(preun):    /sbin/chkconfig
Requires(preun):    /sbin/service
%endif
%description        gmond
Ganglia is a scalable, real-time monitoring and execution environment
with all execution requests and statistics expressed in an open
well-defined XML format.

This gmond daemon provides the ganglia service within a single cluster
or Multicast domain.

%if 0%{?py2}
%package         -n python2-ganglia-gmond
Summary:            Ganglia Monitor daemon python DSO and metric modules
Requires:           ganglia-gmond
Requires:           python2
%{?python_provide:%python_provide python2-ganglia-gmond}
# Remove before F30
Provides:           ganglia-gmond-python = %{version}-%{release}
%description     -n python2-ganglia-gmond
Ganglia is a scalable, real-time monitoring and execution environment
with all execution requests and statistics expressed in an open
well-defined XML format.

This package provides the gmond python DSO and python gmond modules,
which can be loaded via the DSO at gmond daemon start time.
%endif

%package            devel
Summary:            Ganglia Library
Requires:           %{name} = %{gangver}-%{release}
Requires:           apr-devel
Requires:           libconfuse-devel
%description        devel
The Ganglia Monitoring Core library provides a set of functions that
programmers can use to build scalable cluster or grid applications

%prep
%setup -q
# fix broken systemd support
install -m 0644 %{SOURCE2} gmond/gmond.service.in
install -m 0644 %{SOURCE3} gmetad/gmetad.service.in
%patch1 -p0
%patch2 -p0
%if 0%{?fedora} || 0%{?rhel} > 7
%patch3 -p1
%endif
# web part
%setup -q -T -D -a 1
mv ganglia-web-%{webver} web
pushd web
%patch0 -p1
%patch4 -p1
popd

%build
touch Makefile.am
%if 0%{?fedora} || 0%{?rhel} > 7
aclocal -I m4
autoheader
automake --add-missing --copy --foreign 2>/dev/null
libtoolize --automake --copy
automake --add-missing --copy --foreign
autoconf -f || exit 1
%endif

%if 0%{?fedora} > 36
pushd libmetrics
aclocal -I m4
autoheader
automake --add-missing --copy --foreign 2>/dev/null
libtoolize --automake --copy
automake --add-missing --copy --foreign
autoconf -f || exit 1
popd
%endif

export CFLAGS="%{optflags} -fcommon"
%configure \
    --enable-setuid=ganglia \
    --enable-setgid=ganglia \
    --with-gmetad \
    --with-memcached \
    --disable-static \
    --enable-shared \
%if 0%{?fedora} > 37
    --with-libpcre=no \
%endif
%if 0%{?py2}
    --with-python=%{__python2} \
%else
    --disable-python \
%endif
    --sysconfdir=%{_sysconfdir}/ganglia

# Remove rpaths
%{__sed} -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
%{__sed} -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

## Default to run as user ganglia instead of nobody
%{__perl} -pi.orig -e 's|nobody|ganglia|g' \
    gmond/gmond.conf.html ganglia.html gmond/conf.pod

%{__perl} -pi.orig -e 's|.*setuid_username.*|setuid_username ganglia|' \
    gmetad/gmetad.conf.in

## Don't have initscripts turn daemons on by default
%{__perl} -pi.orig -e 's|2345|-|g' gmond/gmond.init gmetad/gmetad.init

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

## Create directory structures
%{?py2:mkdir -p %{buildroot}%{_libdir}/ganglia/python_modules}
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}/rrds

## Install services
%if 0%{?systemd}
install -Dp -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/gmond.service
install -Dp -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}/gmetad.service
%else
install -Dp -m 0755 gmond/gmond.init %{buildroot}%{_sysconfdir}/init.d/gmond
install -Dp -m 0755 gmetad/gmetad.init %{buildroot}%{_sysconfdir}/init.d/gmetad
%endif

## Build default gmond.conf from gmond using the '-t' flag
LD_LIBRARY_PATH=lib/.libs gmond/gmond -t | %{__perl} -pe 's|nobody|ganglia|g' \
    > %{buildroot}%{_sysconfdir}/ganglia/gmond.conf

%if 0%{?py2}
## Python bits
# Copy the python metric modules and .conf files
cp -p gmond/python_modules/conf.d/*.pyconf %{buildroot}%{_sysconfdir}/ganglia/conf.d/
cp -p gmond/modules/conf.d/*.conf %{buildroot}%{_sysconfdir}/ganglia/conf.d/
cp -p gmond/python_modules/*/*.py %{buildroot}%{_libdir}/ganglia/python_modules/
%endif

## Web bits
pushd web
make install DESTDIR=%{buildroot}
install -p -m 0644 %{SOURCE6} %{buildroot}%{_sysconfdir}/ganglia/conf.php
ln -s ../../..%{_sysconfdir}/%{name}/conf.php \
    %{buildroot}%{_datadir}/%{name}/conf.php
popd

## httpd config
%if 0%{?fedora} || 0%{?rhel} > 6
install -Dp -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
%else
install -Dp -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
%endif

## Various clean up after install:

## Don't install the status modules and example.conf
rm -f %{buildroot}%{_sysconfdir}/ganglia/conf.d/{modgstatus,example}.conf

## Disable the diskusage module until it is configured properly
## mv %{buildroot}%{_sysconfdir}/ganglia/conf.d/diskusage.pyconf \
##   %{buildroot}%{_sysconfdir}/ganglia/conf.d/diskusage.pyconf.off

## Remove unwanted files from web dir
rm -rf %{buildroot}%{_datadir}/%{name}/{Makefile*,debian,ganglia-web.spec*,ganglia-web}
rm -rf %{buildroot}%{_datadir}/%{name}/{conf_default.php.in,version.php.in}
rm -rf %{buildroot}%{_localstatedir}/lib/%{name}-web/conf/sql

## Included as doc
rm -rf %{buildroot}%{_datadir}/%{name}/{README,TODO,AUTHORS,COPYING}

## House cleaning
rm -f %{buildroot}%{_libdir}/*.la

# Remove execute bit
chmod 0644 %{buildroot}%{_datadir}/%{name}/header.php
%{?py2:chmod 0644 %{buildroot}%{_libdir}/%{name}/python_modules/*.py}
chmod 0644 %{buildroot}%{_datadir}/%{name}/css/smoothness/jquery-ui-1.10.2.custom.css
chmod 0644 %{buildroot}%{_datadir}/%{name}/css/smoothness/jquery-ui-1.10.2.custom.min.css

# Remove shebang
%{?py2:sed -i '1{\@^#!@d}' %{buildroot}%{_libdir}/%{name}/python_modules/*.py}

%pre
## Add the "ganglia" user
/usr/sbin/useradd -c "Ganglia Monitoring System" \
        -s /sbin/nologin -r -d %{_localstatedir}/lib/%{name} ganglia 2> /dev/null || :

%if 0%{?systemd}
%post gmond
%systemd_post gmond.service

%preun gmond
%systemd_preun gmond.service

%postun gmond
%systemd_postun_with_restart gmond.service

%post gmetad
%systemd_post gmetad.service

%preun gmetad
%systemd_preun gmetad.service

%postun gmetad
%systemd_postun_with_restart gmetad.service

%else 

%post gmond
/sbin/chkconfig --add gmond

%post gmetad
/sbin/chkconfig --add gmetad

%preun gmetad
if [ "$1" = 0 ]; then
  /sbin/service gmetad stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del gmetad
fi

%preun gmond
if [ "$1" = 0 ]; then
  /sbin/service gmond stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del gmond
fi

%endif

# https://fedoraproject.org/wiki/Packaging:Directory_Replacement#Scriptlet_to_replace_a_symlink_to_a_directory_with_a_directory
%pretrans web -p <lua>
path = "/usr/share/ganglia/lib/Zend"
st = posix.stat(path)
if st and st.type == "link" then
  os.remove(path)
end

%files
%license COPYING
%doc AUTHORS NEWS README ChangeLog
%{_libdir}/libganglia*.so.*
%dir %{_libdir}/ganglia
%{_libdir}/ganglia/*.so
%{?py2:%exclude %{_libdir}/ganglia/modpython.so}

%files gmetad
%dir %{_localstatedir}/lib/%{name}
%attr(0755,ganglia,ganglia) %{_localstatedir}/lib/%{name}/rrds
%{_sbindir}/gmetad
%if 0%{?systemd}
%{_unitdir}/gmetad.service
%else
%{_sysconfdir}/init.d/gmetad
%endif
%{_mandir}/man1/gmetad.1*
%{_mandir}/man1/gmetad.py.1*
%dir %{_sysconfdir}/ganglia
%config(noreplace) %{_sysconfdir}/ganglia/gmetad.conf

%files gmond
%{_bindir}/gmetric
%{_bindir}/gstat
%{_sbindir}/gmond
%if 0%{?systemd}
%{_unitdir}/gmond.service
%else
%{_sysconfdir}/init.d/gmond
%endif
%{_mandir}/man5/gmond.conf.5*
%{_mandir}/man1/gmond.1*
%{_mandir}/man1/gstat.1*
%{_mandir}/man1/gmetric.1*
%dir %{_sysconfdir}/ganglia
%{?py2:%dir %{_sysconfdir}/ganglia/conf.d}
%config(noreplace) %{_sysconfdir}/ganglia/gmond.conf
%{?py2:%config(noreplace) %{_sysconfdir}/ganglia/conf.d/*.conf}
%{?py2:%exclude %{_sysconfdir}/ganglia/conf.d/modpython.conf}

%if 0%{?py2}
%files -n python2-ganglia-gmond
%dir %{_libdir}/ganglia/python_modules/
%{_libdir}/ganglia/python_modules/*.py*
%{_libdir}/ganglia/modpython.so*
%config(noreplace) %{_sysconfdir}/ganglia/conf.d/*.pyconf*
%config(noreplace) %{_sysconfdir}/ganglia/conf.d/modpython.conf
%endif

%files devel
%{_bindir}/ganglia-config
%{_includedir}/*.h
%{_libdir}/libganglia*.so

%files web
%license web/COPYING
%doc web/AUTHORS web/README web/TODO
%config(noreplace) %{_sysconfdir}/%{name}/conf.php
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%{_datadir}/%{name}
%dir %attr(0755,apache,apache) %{_localstatedir}/lib/%{name}-web/conf
%config(noreplace) %attr(0644,apache,apache) %{_localstatedir}/lib/%{name}-web/conf/*.json
%dir %attr(0755,apache,apache) %{_localstatedir}/lib/%{name}-web/dwoo
%dir %attr(0755,apache,apache) %{_localstatedir}/lib/%{name}-web/dwoo/cache
%dir %attr(0755,apache,apache) %{_localstatedir}/lib/%{name}-web/dwoo/compiled

%changelog
* Thu Jul 06 2023 Navjot Singh <navjotsingh@microsoft.com> - 3.7.2-41
- Initial CBL-Mariner import from Fedora 38 (license: MIT).
- License verified

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.2-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 12 2023 Terje Rosten <terje.rosten@ntnu.no> - 3.7.2-40
- Fix implicit dep on php-xml (rhbz#2016302)
- Remove dep on pcre in Fedora 38+ (rhbz#2128294)
- RHEL7+ have httpd 2.4 too
- Simplify fedora conditionals
- Fix autoconf problem in libmetrics

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.2-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.2-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Sep 09 2021 Terje Rosten <terje.rosten@ntnu.no> - 3.7.2-37
- Need sasl bits to build

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.2-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 02 2021 Zbigniew JÄ™drzejewski-Szmek <zbyszek@in.waw.pl> - 3.7.2-35
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.2-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct 08 2020 Germano Massullo <germano.massullo@gmail.com> - 3.7.2-33
- removed all occurrencies of "# systemd" after %%endif since they are not allowed.

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.2-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Feb 10 2020 Terje Rosten <terje.rosten@ntnu.no> - 3.7.2-31
- Bring Zend back to fix rhbz#1797111 and rhbz#1734255

* Sat Feb 01 2020 Terje Rosten <terje.rosten@ntnu.no> - 3.7.2-30
- Update to ganglia-web 3.7.5 + latest from git
- Add hack to fix GCC10 build issue

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.2-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Aug 18 2019 Terje Rosten <terje.rosten@ntnu.no> - 3.7.2-28
- Fix conditionals

* Wed Aug 14 2019 Terje Rosten <terje.rosten@ntnu.no> - 3.7.2-27
- Drop Python 2 stuff in newer distros

* Tue Aug 13 2019 Terje Rosten <terje.rosten@ntnu.no> - 3.7.2-26
- Fix deps

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.2-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.2-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Terje Rosten <terje.rosten@ntnu.no> - 3.7.2-23
- Add path to python
- Add C compiler

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.2-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 20 2018 Iryna Shcherbina <ishcherb@redhat.com> - 3.7.2-21
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 14 2018 Terje Rosten <terje.rosten@ntnu.no> - 3.7.2-20
- Add hack to build with tirpc

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.2-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Aug 08 2017 Zbigniew JÄ™drzejewski-Szmek <zbyszek@in.waw.pl> - 3.7.2-18
- Python 2 binary package renamed to python2-ganglia-gmond
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu May 25 2017 Gwyn Ciesla <limburgher@gmail.com> - 3.7.2-15
- libconfuse rebuild.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 23 2017 Terje Rosten <terje.rosten@ntnu.no> - 3.7.2-13
- Reorg file locations to fix rhbz#1238325

* Mon Dec 05 2016 Terje Rosten <terje.rosten@ntnu.no> - 3.7.2-12
- Add patch to fix sflow issue (rhbz#1400932), thanks to Glenn L. Jenkins!

* Sun Oct 02 2016 Terje Rosten <terje.rosten@ntnu.no> - 3.7.2-11
- Subpackage -devel needs apr and confuse devel packages

* Wed Aug 24 2016 Terje Rosten <terje.rosten@ntnu.no> - 3.7.2-10
- ganglia-web 3.7.2

* Wed Jun 15 2016 Jon Ciesla <limburgher@gmail.com> - 3.7.2-9
- libconfuse rebuild.

* Sat Apr 30 2016 Terje Rosten <terje.rosten@ntnu.no> - 3.7.2-8
- rebuild: rrdtool 1.6

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Oct 11 2015 Terje Rosten <terje.rosten@ntnu.no> - 3.7.2-6
- ganglia-web 3.7.1

* Fri Aug 28 2015 Terje Rosten <terje.rosten@ntnu.no> - 3.7.2-5
- Increase release to 5 to get web subpackage forward

* Wed Aug 19 2015 Nick Le Mouton <nick@noodles.net.nz> - 3.7.2-1
- ganglia 3.7.2
- fix for apache 2.4.16

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Terje Rosten <terje.rosten@ntnu.no> - 3.7.1-3
- Let gmond service start after network is ready (bz#585891)

* Tue Jun 09 2015 Terje Rosten <terje.rosten@ntnu.no> - 3.7.1-2
- ganglia-web 3.7.0

* Tue Apr 07 2015 Terje Rosten <terje.rosten@ntnu.no> - 3.7.1-1
- 3.7.1 & ganglia-web 3.6.2

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Jan 11 2014 Terje Rosten <terje.rosten@ntnu.no> - 3.6.0-4
- Update to ganglia-web 3.5.12

* Sat Nov 30 2013 Terje Rosten <terje.rosten@ntnu.no> - 3.6.0-3
- Update to ganglia-web 3.5.10
- Add patch as workaround for CVE-2013-6395 (bz #1034527)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jun 02 2013 Terje Rosten <terje.rosten@ntnu.no> - 3.6.0-1
- Update to ganglia 3.6.0 and ganglia-web 3.5.8

* Thu May 09 2013 Terje Rosten <terje.rosten@ntnu.no> - 3.5.0-4
- Hardened build in FC > 18.

* Wed Feb 20 2013 Terje Rosten <terje.rosten@ntnu.no> - 3.5.0-3
- Update to ganglia-web 3.5.7
- Add extra patch for XSS security

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 06 2013 Terje Rosten <terje.rosten@ntnu.no> - 3.5.0-1
- 3.5.0

* Tue Dec 18 2012 Terje Rosten <terje.rosten@ntnu.no> - 3.4.0-1
- 3.4.0
- Add ganglia-web 3.5.4 tarball
- Add support for non systemd builds
- Support httpd >= 2.4
- Use new systemd macros
- Various clean up (rpmlint)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 14 2012 Jon Ciesla <limburgher@gmail.com> - 3.3.7-4
- Unbundle Zend.

* Fri May 11 2012 Terje Rosten <terje.rosten@ntnu.no> - 3.3.7-3
- Fix web frontend

* Fri May 11 2012 Jon Ciesla <limburgher@gmail.com> - 3.3.7-2
- scriptlet corrections.

* Mon May 07 2012 Terje Rosten <terje.rosten@ntnu.no> - 3.3.7-1
- Update to 3.3.7
- Split buildreq/req
- Remove svn tag
- Fix src url
- Remove patches now upstream
- More man pages
- Move web config
- Move ganglia-config to -devel
- Systemd support

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 3.1.7-6
- Rebuild against PCRE 8.30

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 14 2011 Kostas Georgiou <georgiou@fedoraproject.org> - 3.1.7-4
- Fix buffer overflow in moddisk.so #689483

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 31 2010 Thomas Spura <tomspur@fedoraproject.org> - 3.1.7-2
- Rebuild for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Apr 22 2010 Kostas Georgiou <georgiou@fedoraproject.org> - 3.1.7-1
- New upstream release
- Spec file cleanups
- Use the new name_match feature to enable the diskusage plugin by default

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 29 2009 Kostas Georgiou <k.georgiou@imperial.ac.uk> - 3.1.2-3
- Rebuilt for #492703, no obvious reasons why the previous build was bad :(

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Kostas Georgiou <k.georgiou@imperial.ac.uk> - 3.1.2-1
- Update to 3.1.2
- Remove unneeded patch for CVE-2009-0241

* Tue Jan 20 2009 Kostas Georgiou <k.georgiou@imperial.ac.uk> - 3.1.1-4
- [480236] Updated patch for the buffer overflow from upstream with
  additional fixes

* Wed Jan 14 2009 Kostas Georgiou <k.georgiou@imperial.ac.uk> - 3.1.1-3
- Fix for gmetad server buffer overflow
- The private_clusters file should not be readable by everyone

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 3.1.1-2
- Rebuild for Python 2.6

* Fri Oct 24 2008 Jarod Wilson <jarod@redhat.com> 3.1.1-1
- Update to 3.1.1

* Thu Aug 28 2008 Michael Schwendt <mschwendt@fedoraproject.org> 3.1.0-2
- Include unowned directories.

* Mon Aug 11 2008 Kostas Georgiou <k.georgiou@imperial.ac.uk> 3.1.0-1
- Upstream patches from 3.1.1
- Move private_clusters config to /etc and mark it as a config file
- Only allow connections from localhost by default on the web frontend
- Add some extra module config files (modules are always loaded at the
  moment so removing the configs has no effect beyond metric collection
  (upstream is working on way way to disable module loading from the
  configs)

* Tue Jul 29 2008 Kostas Georgiou <k.georgiou@imperial.ac.uk> 3.1.0-0.5
- Add the config files for the python module

* Thu Jul 17 2008 Kostas Georgiou <k.georgiou@imperial.ac.uk> 3.1.0-0.4
- Update to the 3.1.0 pre-release
- Fixes gmond.conf to use the ganglia user and not nobody
- Removal of the ppc64 work-around
 
* Fri Jun 13 2008 Jarod Wilson <jwilson@redhat.com> 3.1.0-0.3.r1399
- One more try at work-around. Needs powerpc64, not ppc64...

* Fri Jun 13 2008 Jarod Wilson <jwilson@redhat.com> 3.1.0-0.2.r1399
- Work-around for incorrectly hard-coded libdir on ppc64

* Wed Jun 11 2008 Jarod Wilson <jwilson@redhat.com> 3.1.0-0.1.r1399
- Update to 3.1.x pre-release snapshot, svn rev 1399

* Mon Jun 09 2008 Jarod Wilson <jwilson@redhat.com> 3.0.7-2
- Bump and rebuild against latest rrdtool

* Wed Feb 27 2008 Jarod Wilson <jwilson@redhat.com> 3.0.7-1
- New upstream release
- Fixes "Show Hosts" toggle
- Fixes to host view metric graphs
- Fixes two memory leaks

* Thu Feb 14 2008 Jarod Wilson <jwilson@redhat.com> 3.0.6-2
- Bump and rebuild with gcc 4.3

* Mon Dec 17 2007 Jarod Wilson <jwilson@redhat.com> 3.0.6-1
- New upstream release (security fix for web frontend
  cross-scripting vulnerability) {CVE-2007-6465}

* Wed Oct 24 2007 Jarod Wilson <jwilson@redhat.com> 3.0.5-2
- Reorg packages to fix multilib conflicts (#341201)

* Wed Oct 03 2007 Jarod Wilson <jwilson@redhat.com> 3.0.5-1
- New upstream release

* Fri May 18 2007 Jarod Wilson <jwilson@redhat.com> 3.0.4-3
- Add missing Req: php-gd so people will see nifty pie charts

* Sat Mar 24 2007 Jarod Wilson <jwilson@redhat.com> 3.0.4-2
- Own created directories (#233790)

* Tue Jan 02 2007 Jarod Wilson <jwilson@redhat.com> 3.0.4-1
- New upstream release

* Thu Nov 09 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-11
- gmond also needs ganglia user (#214762)

* Tue Sep 05 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-10
- Rebuild for new glibc

* Fri Jul 28 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-9
- Add missing Reqs on chkconfig and service
- Make %%preun sections match Fedora Extras standards
- Minor %%configure tweak

* Tue Jul 11 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-8
- Add missing php req for ganglia-web
- Misc tiny spec cleanups

* Tue Jun 13 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-7
- Clean up documentation

* Mon Jun 12 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-6
- Remove misplaced execute perms on source files

* Thu Jun 08 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-5
- Whack Obsoletes/Provides, since its never been in FE before
- Use mandir macro
- Check if service is running before issuing a stop in postun
- Remove shadow-utils Prereq, its on the FE exception list

* Mon Jun 05 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-4
- Run things as user ganglia instead of nobody
- Don't turn on daemons by default

* Mon Jun 05 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-3
- Kill off static libs
- Add URL for Source0

* Mon Jun 05 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-2
- Move web-frontend from /var/www/html/ to /usr/share/
- Make everything arch-specific

* Thu Jun 01 2006 Jarod Wilson <jwilson@redhat.com> 3.0.3-1
- Initial build for Fedora Extras, converting existing spec to
  (attempt to) conform with Fedora packaging guidelines
