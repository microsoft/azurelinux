# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global nameserver omniNames

%if 0%{?fedora} || 0%{?rhel} > 6
%global with_systemd 1
%endif

# openssl enabled by default, add conditional --without openssl
%bcond_without openssl

Name:           omniORB
Version:        4.3.3
Release: 8%{?dist}
Summary:        A robust high performance CORBA ORB for C++ and Python

License:        LGPL-2.0-or-later
URL:            http://omniorb.sourceforge.net
Source0:        http://downloads.sourceforge.net/project/omniorb/%{name}/%{name}-%{version}/%{name}-%{version}.tar.bz2
Source1:        omniORB-nameserver.init
Source2:        omniORB-nameserver.logrotate
Source3:        omniORB.cfg
Source4:        omniNames.service

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  python3-devel
BuildRequires:  byacc
BuildRequires:  zlib-devel
%{!?_without_openssl:BuildRequires:  openssl-devel}
%if 0%{?with_systemd}
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%else
Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(postun): initscripts
%endif

# we don't want to provide private python extension libs
%{?filter_setup:
%filter_provides_in %{python3_sitearch}/.*\.so$
%filter_setup
}

%description
omniORB is a robust high performance CORBA ORB for C++ and Python.
omniORB is a certified CORBA 2.1 implementation and largely CORBA 2.6
compliant.


%package        devel
Summary:        Development files for %{name}
License:        LGPL-2.0-or-later
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        doc
Summary:        Documentation files for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description    doc
The %{name}-doc package contains documentation files for
developing and administrating applications that use %{name}.

%package        servers
Summary:        OmniORB naming service
License:        GPL-2.0-or-later
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    servers
The %{name}-servers package contains omniNames naming server.

%package        utils
Summary:        Development files for %{name}
License:        GPL-2.0-or-later
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    utils
The %{name}-utils package contains supplementary command line tools for
developing applications that use %{name}.


%prep
%autosetup -p1
# Fix shebangs
sed -i '1s=^#!/usr/bin/\(python\|env python\)[0-9.]*=#!%{__python3}=' \
  ./src/tool/omniidl/python3/scripts/omniidlrun.py \
  ./src/tool/omniidl/python3/omniidl/main.py

# Create a sysusers.d config file
cat >omniorb.sysusers.conf <<EOF
u omniORB - 'OmniNames Naming Service' %{_sharedstatedir}/%{name} -
EOF

%build
# Per guidelines: if the same functionality is provided regardless of the interpreter version, only the python 3 version should be packaged
export PYTHON=%{__python3}
%configure --disable-static %{?with_openssl:--with-openssl=%{_prefix}}
%make_build



%install
%make_install
find %{buildroot} -name '*.la' -delete
# fix rpmlint warnings: unstripped-binary-or-object
chmod 0755 %{buildroot}%{_libdir}/*.so.*
chmod 0755 %{buildroot}%{python3_sitearch}/*.so.*
# fix rpmlint errors: non-standard-dir-perm
chmod 0755 %{buildroot}%{_includedir}/{omnithread,COS}
chmod 0755 %{buildroot}%{_includedir}/omniORB4/{,internal}
chmod 0755 %{buildroot}%{_datadir}/idl/%{name}/COS
chmod 0755 %{buildroot}%{python3_sitelib}/omniidl
chmod 0755 %{buildroot}%{python3_sitelib}/omniidl_be
chmod 0755 %{buildroot}%{python3_sitelib}/omniidl_be/cxx/{,skel,impl,dynskel,header}
# fix rpmlint error: non-executable-script
chmod +x %{buildroot}%{python3_sitelib}/omniidl/main.py
%if 0%{?with_systemd}
# install systemd unit
mkdir -p %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE4} %{buildroot}%{_unitdir}
%else
# install service init script
mkdir -p %{buildroot}%{_initddir}
install -m 0755 %{SOURCE1} %{buildroot}%{_initddir}/%{nameserver}
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}
mkdir -p %{buildroot}%{_localstatedir}/run/%{name}
%endif
# install server configuration stuff
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d/
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{nameserver}
mkdir -p %{buildroot}%{_sysconfdir}/
install -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}.cfg
mkdir -p %{buildroot}%{_localstatedir}/log/%{name}
# install man pages
pushd man
mkdir -p %{buildroot}%{_mandir}/man1
install -m 0644 man1/* %{buildroot}%{_mandir}/man1/
mkdir -p %{buildroot}%{_mandir}/man8
install -m 0644 man8/* %{buildroot}%{_mandir}/man8/
popd

install -m0644 -D omniorb.sysusers.conf %{buildroot}%{_sysusersdir}/omniorb.conf

%ldconfig_scriptlets


%if 0%{?with_systemd}
%post servers
%systemd_post omniNames.service

%preun servers
%systemd_preun omniNames.service

%postun servers
%systemd_postun omniNames.service

%else
%post servers
/sbin/chkconfig --add %{nameserver}

%preun servers
if [ $1 = 0 ] ; then
  /sbin/service  stop >/dev/null 2>&1
  /sbin/chkconfig --del  %{nameserver}
fi

%postun servers
if [ $1 -ge 1 ] ; then
    /sbin/service  %{nameserver} condrestart >/dev/null 2>&1 || :
fi
%endif

%files
%license COPYING.LIB
%doc README.FIRST.txt README.unix.txt
%{_libdir}/libCOS4.so.3*
%{_libdir}/libCOSDynamic4.so.3*
%{_libdir}/libomniCodeSets4.so.3*
%{_libdir}/libomniConnectionMgmt4.so.3*
%{_libdir}/libomniDynamic4.so.3*
%{_libdir}/libomniORB4.so.3*
%{_libdir}/libomniZIOP4.so.3*
%{_libdir}/libomniZIOPDynamic4.so.3*
%{_libdir}/libomnisslTP4.so.3*
%{_libdir}/libomnihttpCrypto4.so.3*
%{_libdir}/libomnihttpTP4.so.3*
%{_libdir}/libomnithread.so.4*

%files servers
%if 0%{?with_systemd}
%{_unitdir}/omniNames.service
%else
%{_initddir}/%{nameserver}
%dir %attr(0755, %{name}, root) %{_sharedstatedir}/%{name}
%dir %attr(0755, %{name}, root) %{_localstatedir}/run/%{name}
%endif
%config(noreplace) %{_sysconfdir}/%{name}.cfg
%config(noreplace) %{_sysconfdir}/logrotate.d/%{nameserver}
%dir %attr(0755, %{name}, root) %{_localstatedir}/log/%{name}
%{_bindir}/omniMapper
%{_bindir}/%{nameserver}
%{_mandir}/man8/*
%{_sysusersdir}/omniorb.conf

%files devel
%doc doc/
%{_bindir}/omniidl
%{_bindir}/omniidlrun.py
%{_bindir}/omnicpp
%{_bindir}/omkdepend
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/idl/%{name}/*
%{python3_sitelib}/*
%{python3_sitearch}/*
%{_mandir}/man1/omniidl.1.gz
%{_mandir}/man1/omnicpp.1.gz

%files doc
%doc doc/

%files utils
%license COPYING
%{_bindir}/catior
%{_bindir}/convertior
%{_bindir}/genior
%{_bindir}/nameclt
%{_mandir}/man1/catior.1.gz
%{_mandir}/man1/convertior.1.gz
%{_mandir}/man1/genior.1.gz
%{_mandir}/man1/nameclt.1.gz


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 4.3.3-7
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 4.3.3-6
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 10 2025 Python Maint <python-maint@redhat.com> - 4.3.3-4
- Rebuilt for Python 3.14

* Tue Jun 10 2025 Sandro Mani <manisandro@gmail.com> - 4.3.3-3
- Remove unnecessary postrotate script from logrotate configuration

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 4.3.3-2
- Rebuilt for Python 3.14

* Wed Apr 02 2025 Sandro Mani <manisandro@gmail.com> - 4.3.3-1
- Update to 4.3.3

* Tue Feb 11 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.3.2-8
- Add sysusers.d config file to allow rpm to create users/groups automatically

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 26 2024 Miroslav Suchý <msuchy@redhat.com> - 4.3.2-6
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 4.3.2-4
- Rebuilt for Python 3.13

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 17 2024 Sandro Mani <manisandro@gmail.com> - 4.3.2-1
- Update to 4.3.2

* Thu Aug 31 2023 Sandro Mani <manisandro@gmail.com> - 4.3.1-1
- Update to 4.3.1

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 4.3.0-8
- Rebuilt for Python 3.12

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 20 2022 Sandro Mani <manisandro@gmail.com> - 4.3.0-6
- Remove last usage of distutils

* Mon Dec 19 2022 Sandro Mani <manisandro@gmail.com> - 4.3.0-5
- Add patch to fix build against python-3.12

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 4.3.0-3
- Rebuilt for Python 3.11

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 10 2022 Sandro Mani <manisandro@gmail.com> - 4.3.0-1
- Update to 4.3.0

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 4.2.4-7
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.2.4-5
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 4.2.4-2
- Rebuilt for Python 3.9

* Tue Apr 07 2020 Sandro Mani <manisandro@gmail.com> - 4.2.4-1
- Update to 4.2.4

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 4.2.3-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 4.2.3-5
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 02 2019 Sandro Mani <manisandro@gmail.com> - 4.2.3-3
- Add missing BR: zlib-devel (#1705703)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 17 2018 Sandro Mani <manisandro@gmail.com> - 4.2.3-1
- Update to 4.2.3

* Mon Oct 15 2018 Peter Robinson <pbrobinson@fedoraproject.org> 4.2.2-10
- Fix systemd conditional for Fedora

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 4.2.2-8
- Rebuilt for Python 3.7

* Wed Feb 21 2018 Iryna Shcherbina <ishcherb@redhat.com> - 4.2.2-7
- Fix shebangs for Python 3

* Mon Feb 19 2018 Sandro Mani <manisandro@gmail.com> - 4.2.2-6
- Add missing BR: gcc-c++, make

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Aug 04 2017 Sandro Mani <manisandro@gmail.com> - 4.2.2-4
- Build against python3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 11 2017 Sandro Mani <manisandro@gmail.com> - 4.2.2-1
- Update to 4.2.2

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 4.2.1-6
- Rebuild due to bug in RPM (RHBZ #1468476)

* Sun Feb 19 2017 Sandro Mani <manisandro@gmail.com> - 4.2.1-5
- Add patch to fix build against OpenSSL-1.1

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.1-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Oct 05 2015 Sandro Mani <manisandro@gmail.com> - 4.2.1-1
- Update to 4.2.1
- Modernize spec

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Apr 11 2015 Sandro Mani <manisandro@gmail.com> - 4.2.0-4
- Add patch for bug #1210340 (omniORB loses SSL peer information), thanks Alexey Kosilin

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 08 2014 Sandro Mani <manisandro@gmail.com> - 4.2.0-1
- upstream 4.2.0

* Tue Sep 10 2013 Haïkel Guémar <hguemar@fedoraproject.org> - 4.1.7-1
- upstream 4.1.7 (RHBZ #1005607)
- macroized systemd scriptlets (RHBZ #850239)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 20 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 4.1.6-2
- enable openssl support
- fix typo in omniNames.service

* Wed Jul 13 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 4.1.6-1
- upstream 4.1.6
- use systemd for fedora >= 15

* Sun May 08 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 4.1.5-2
- spec cleanup

* Sun Jan 09 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 4.1.5-1
- upstream 4.1.5

* Wed Nov 24 2010 Haïkel Guémar <hguemar@fedoraproject.org> - 4.1.4-1
- initial packaging
