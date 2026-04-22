# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define with_numactl          0%{!?_without_numactl:1}

# Numactl is not available on armhf
%ifarch armv7hl
%define with_numactl 0
%endif

%if %{with_numactl}
    %define arg_numactl --enable-numa
%else
    %define arg_numactl --disable-numa
%endif


Name:           lttng-ust
Version:        2.14.0
Release: 5%{?dist}

License:        LGPL-2.1-only AND MIT AND GPL-2.0-only AND BSD-3-Clause AND BSD-2-Clause
Summary:        LTTng Userspace Tracer library
URL:            https://lttng.org
Source0:        https://lttng.org/files/lttng-ust/%{name}-%{version}.tar.bz2
Source1:        https://lttng.org/files/lttng-ust/%{name}-%{version}.tar.bz2.asc
# gpg2 --export --export-options export-minimal 2A0B4ED915F2D3FA45F5B16217280A9781186ACF > gpgkey-2A0B4ED915F2D3FA45F5B16217280A9781186ACF.gpg
Source2:        gpgkey-2A0B4ED915F2D3FA45F5B16217280A9781186ACF.gpg
Patch0:         lttng-gen-tp-shebang.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gnupg2
BuildRequires:  libtool
BuildRequires:  libuuid-devel
BuildRequires:  pkgconfig
BuildRequires:  systemtap-sdt-devel
BuildRequires:  userspace-rcu-devel >= 0.12.0
%if %{with_numactl}
BuildRequires:  numactl-devel
%endif

%description
This library may be used by user-space applications to generate 
trace-points using LTTng.


%package -n %{name}-devel
Summary:        LTTng Userspace Tracer library headers and development files
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       userspace-rcu-devel
Requires:       systemtap-sdt-devel

%description -n %{name}-devel
The %{name}-devel package contains libraries and header to instrument
applications using %{name}


%package -n python3-lttngust
Summary:        Python bindings for LTTng UST
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires: make
%{?python_provide:%python_provide python3-lttngust}

%description -n python3-lttngust
The python3-lttngust package contains libraries needed to instrument
applications that use %{name}'s Python logging backend.


%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1

%build
# Reinitialize libtool with the fedora version to remove Rpath
autoreconf -vif

%ifarch armv7hl
export CPPFLAGS="-DUATOMIC_NO_LINK_ERROR"
%endif

%configure \
	--docdir=%{_docdir}/%{name} \
	--disable-static \
	--enable-python-agent \
	--with-sdt \
	%{?arg_numactl}

make %{?_smp_mflags} V=1

%install
make DESTDIR=%{buildroot} install
rm -vf %{buildroot}%{_libdir}/*.la

%check
make check

%ldconfig_scriptlets

%files
%{_libdir}/*.so.*
%{_mandir}/man3/do_tracepoint.3.gz
%{_mandir}/man3/lttng-ust.3.gz
%{_mandir}/man3/lttng-ust-cyg-profile.3.gz
%{_mandir}/man3/lttng-ust-dl.3.gz
%{_mandir}/man3/lttng_ust_do_tracepoint.3.gz
%{_mandir}/man3/lttng_ust_tracef.3.gz
%{_mandir}/man3/lttng_ust_tracelog.3.gz
%{_mandir}/man3/lttng_ust_tracepoint.3.gz
%{_mandir}/man3/lttng_ust_tracepoint_enabled.3.gz
%{_mandir}/man3/lttng_ust_vtracef.3.gz
%{_mandir}/man3/lttng_ust_vtracelog.3.gz
%{_mandir}/man3/tracef.3.gz
%{_mandir}/man3/tracelog.3.gz
%{_mandir}/man3/tracepoint.3.gz
%{_mandir}/man3/tracepoint_enabled.3.gz

%dir %{_docdir}/%{name}
%{_docdir}/%{name}/ChangeLog
%{_docdir}/%{name}/java-agent.md
%{_docdir}/%{name}/python-agent.md
%{_docdir}/%{name}/LICENSE
%{_docdir}/%{name}/README.md


%files -n %{name}-devel
%{_bindir}/lttng-gen-tp
%{_mandir}/man1/lttng-gen-tp.1.gz
%{_prefix}/include/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/lttng-ust*.pc

%dir %{_docdir}/%{name}/examples
%{_docdir}/%{name}/examples/*

%files -n python3-lttngust
%{python3_sitelib}/lttngust/
%{python3_sitelib}/lttngust-*.egg-info

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.14.0-4
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.14.0-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 03 2025 Michael Jeanson <mjeanson@efficios.com> - 2.14.0-1
- New upstream release

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 2.13.9-2
- Rebuilt for Python 3.14

* Tue Apr 15 2025 Michael Jeanson <mjeanson@efficios.com> - 2.13.9-1
- New upstream release

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.13.8-2
- Rebuilt for Python 3.13

* Fri Apr 19 2024 Kienan Stewart <kstewart@efficios.com> - 2.13.8-1
- New upstream release

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 12 2024 Michael Jeanson <mjeanson@efficios.com> - 2.13.7-1
- New upstream release

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.13.6-4
- Rebuilt for Python 3.12

* Wed Jun 07 2023 Kienan Stewart <kstewart@efficios.com> - 2.13.6-1
- New upstream release

* Mon May 08 2023 Michael Jeanson <mjeanson@efficios.com> - 2.13.5-3
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Oct 18 2022 Michael Jeanson <mjeanson@efficios.com> - 2.13.5-1
- New upstream release
- Add builddep on python3-setuptools in prevision of python 3.12 removing distutils

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 2.13.3-2
- Rebuilt for Python 3.11

* Wed Jun 15 2022 Michael Jeanson <mjeanson@efficios.com> - 2.13.3-1
- New upstream release

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.13.2-2
- Rebuilt for Python 3.11

* Tue Mar 29 2022 Michael Jeanson <mjeanson@efficios.com> - 2.13.2-1
- New upstream release

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 10 2021 Michael Jeanson <mjeanson@efficios.com> - 2.13.1-1
- New upstream release
- Fix dotnet segfault when dlopening liblttng-ust (#2031143)

* Wed Oct 20 2021 Michael Jeanson <mjeanson@efficios.com> - 2.13.0-1
- New upstream release
- SONAME bump of liblttng-ust.so to 1
- SONAME bump of liblttng-ust-ctl.so to 5

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 07 2021 Michael Jeanson <mjeanson@efficios.com> - 2.12.2-4
- Rebuilt for liburcu 0.13 (SONAME 8)

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.12.2-2
- Rebuilt for Python 3.10

* Wed May 19 2021 Michael Jeanson <mjeanson@efficios.com> - 2.12.2-1
- New upstream release

* Thu Feb 18 2021 Michael Jeanson <mjeanson@efficios.com> - 2.12.1-1
- New upstream release

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.12.0-2
- Rebuilt for Python 3.9

* Tue Apr 14 2020 Michael Jeanson <mjeanson@efficios.com> - 2.12.0-1
- New upstream release

* Fri Mar 06 2020 Michael Jeanson <mjeanson@efficios.com> - 2.11.1-1
- New upstream release
- Add requires systemtap-sdt-devel to lttng-ust-devel (#1386412)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 23 2020 Michael Jeanson <mjeanson@efficios.com> - 2.11.0-3
- Enable SystemTAP SDT support (#1386412)

* Wed Jan 22 2020 Michael Jeanson <mjeanson@efficios.com> - 2.11.0-2
- Add patch to fix build failure with GCC 10

* Tue Oct 22 2019 Michael Jeanson <mjeanson@efficios.com> - 2.11.0-1
- New upstream release

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.10.4-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.10.4-3
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 03 2019 Michael Jeanson <mjeanson@efficios.com> - 2.10.4-1
- New upstream release
- Add patch to build on glibc >= 2.30

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 07 2018 Michael Jeanson <mjeanson@efficios.com> - 2.10.2-1
- New upstream release
- Add python3-lttngust sub-package.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.10.1-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Michael Jeanson <mjeanson@efficios.com> - 2.10.1-1
- New upstream release

* Fri Aug 18 2017 Dan Horák <dan[at]danny.cz> - 2.10.0-2
- drop the s390(x) build workaround

* Wed Aug 02 2017 Michael Jeanson <mjeanson@efficios.com> - 2.10.0-1
- New upstream release

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 22 2017 Michael Jeanson <mjeanson@efficios.com> - 2.9.1-1
- New upstream release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 30 2016 Michael Jeanson <mjeanson@efficios.com> - 2.9.0-1
- New upstream release

* Wed Jun 22 2016 Michael Jeanson <mjeanson@efficios.com> - 2.8.1-2
- Re-add rpath removing
- Fix spelling errors

* Tue Jun 21 2016 Michael Jeanson <mjeanson@efficios.com> - 2.8.1-1
- New upstream release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Aug 6 2015 Suchakra Sharma <suchakra@fedoraproject.org> - 2.6.2-2
- Remove remaining BR for SystemTap SDT and add python as a BR

* Thu Jul 23 2015 Michael Jeanson <mjeanson@gmail.com> - 2.6.2-1
- New upstream release
- Drop SystemTap SDT support
- Remove patches applied upstream

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Dec  9 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2.5.1-2
- Add patch to fix aarch64 support

* Mon Nov 03 2014 Suchakra Sharma <suchakra@fedoraproject.org> - 2.5.1-1
- New upstream release
- Update URL

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 20 2014 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.4.1-1
- New upstream bugfix release

* Sat Mar 1 2014 Suchakra Sharma <suchakra@fedoraproject.org> - 2.4.0-1
- New upstream release
- Add new files (man and doc)

* Sat Feb 22 2014 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.3.0-2
- Rebuilt for URCU Soname change

* Fri Sep 20 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.3.0-1
- New upstream release (include snapshop feature)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.2.1-1
- New upstream release
- Bump URCU dependency

* Thu May 23 2013 Dan Horák <dan[at]danny.cz> - 2.1.2-2
- add build workaround for s390(x)

* Fri May 17 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.1.2-1
- New upstream bugfix release
- Remove patches applied upstream

* Wed Feb 27 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.1.1-2
- Remove dependency of probes on urcu-bp

* Tue Feb 26 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.1.1-1
- New upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 23 2012 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.0.5-1
- New upstream release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.0.4-2
- Add dependency on systemtap-sdt-devel for devel package

* Tue Jun 19 2012 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.0.4-1
- New upstream release
- Updates from review comments

* Thu Jun 14 2012 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.0.3-1
- New package, inspired by the one from OpenSuse

