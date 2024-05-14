%bcond_without python
%if %{with python}
%define python_sitearch %(python3 -c "from distutils.sysconfig import get_python_lib; print (get_python_lib(1))")
%define python_prefix %(python3 -c "import sys; print (sys.prefix)")
%{?filter_setup:
%filter_provides_in %{python3_sitearch}/perfmon/.*\.so$
%filter_setup
}
%endif

Name:		libpfm
Version:	4.10.1
Release:	11%{?dist}

Summary:	Library to encode performance events for use by perf tool

License:	MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:		https://perfmon2.sourceforge.net/
Source0:	https://sourceforge.net/projects/perfmon2/files/libpfm4/%{name}-%{version}.tar.gz
Patch2:		libpfm-python3-setup.patch

BuildRequires:	gcc
%if %{with python}
BuildRequires:	python3
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
BuildRequires:	swig
%endif

%description

libpfm4 is a library to help encode events for use with operating system
kernels performance monitoring interfaces. The current version provides support
for the perf_events interface available in upstream Linux kernels since v2.6.31.

%package devel
Summary:	Development library to encode performance events for perf_events based tools
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Development library and header files to create performance monitoring
applications for the perf_events interface.

%package static
Summary:	Static library to encode performance events for perf_events based tools
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description static
Static version of the libpfm library for performance monitoring
applications for the perf_events interface.

%if %{with python}
%package -n python3-libpfm
%{?python_provide:%python_provide python3-libpfm}
# Remove before F30
Provides: %{name}-python = %{version}-%{release}
Provides: %{name}-python%{?_isa} = %{version}-%{release}
Obsoletes: %{name}-python < %{version}-%{release}
Summary:	Python bindings for libpfm and perf_event_open system call
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description -n python3-libpfm
Python bindings for libpfm4 and perf_event_open system call.
%endif

%prep
%setup -q
%patch 2 -p1 -b .python3

%build
%if %{with python}
%global python_config CONFIG_PFMLIB_NOPYTHON=n
%else
%global python_config CONFIG_PFMLIB_NOPYTHON=y
%endif
make %{python_config} %{?_smp_mflags} \
     OPTIM="%{optflags}" LDFLAGS="%{build_ldflags}"


%install
rm -rf $RPM_BUILD_ROOT

%if %{with python}
%global python_config CONFIG_PFMLIB_NOPYTHON=n PYTHON_PREFIX=$RPM_BUILD_ROOT/%{python_prefix}
%else
%global python_config CONFIG_PFMLIB_NOPYTHON=y
%endif

make \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    LIBDIR=$RPM_BUILD_ROOT%{_libdir} \
    %{python_config} \
    LDCONFIG=/bin/true \
    install

%ldconfig_scriptlets

%files
%doc README
%{_libdir}/lib*.so.*

%files devel
%{_includedir}/*
%{_mandir}/man3/*
%{_libdir}/lib*.so

%files static
%{_libdir}/lib*.a

%if %{with python}
%files -n python3-libpfm
%{python3_sitearch}/*
%endif

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.10.1-11
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 4.10.1-9
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 4.10.1-8
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 17 2018 Miro Hrončok <mhroncok@redhat.com> - 4.10.1-5
- Update Python macros to new packaging standards
  (See https://fedoraproject.org/wiki/Changes/Move_usr_bin_python_into_separate_package)

* Sun Jul 15 2018 William Cohen <wcohen@redhat.com> - 4.10.1-4
- Add gcc Buildrequires.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 4.10.1-2
- Rebuilt for Python 3.7

* Fri Jun 15 2018 William Cohen <wcohen@redhat.com> - 4.10.1-1
- Rebase on libpfm-4.10.1.

* Tue Jun 12 2018 William Cohen <wcohen@redhat.com> - 4.10.0-2
- Use upstream libpfm cavium patch.

* Fri Jun 8 2018 William Cohen <wcohen@redhat.com> - 4.10.0-1
- Rebase on libpfm-4.10.0.
- Use Python 3.

* Mon Feb 26 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.0-6
- Pass in LDFLAGS for build.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 William Cohen <wcohen@redhat.com> - 4.9.0-4
- Address truncation issues.

* Tue Jan 30 2018 William Cohen <wcohen@redhat.com> - 4.9.0-3
- Use the RPM build flags. (RHBZ #1540262)

* Tue Jan 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 4.9.0-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jan 4 2018 William Cohen <wcohen@redhat.com> - 4.9.0-1
- Rebase on libpfm-4.9.0.

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.8.0-8
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.8.0-7
- Python 2 binary package renamed to python2-libpfm
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 4.8.0-4
- Rebuild due to bug in RPM (RHBZ #1468476)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 7 2016 William Cohen <wcohen@redhat.com> - 4.8.0-1
- Rebase on libpfm-4.8.0.

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 11 2016 William Cohen <wcohen@redhat.com> - 4.7.0-1
- Rebase on libpfm-4.7.0.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 4 2015 William Cohen <wcohen@redhat.com> - 4.6.0-2
- Correct requires for subpackages.

* Thu Mar 5 2015 William Cohen <wcohen@redhat.com> - 4.6.0-1
- Rebase on libpfm-4.6.0.

* Wed Feb 11 2015 William Cohen <wcohen@redhat.com> - 4.5.0-6
- Bump version and rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 30 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 4.5.0-4
- Replace python-setuptools-devel BR with python-setuptools

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 William Cohen <wcohen@redhat.com> 4.5.0-2
- Add cortex a53 support.

* Fri May 23 2014 William Cohen <wcohen@redhat.com> 4.5.0-1
- Rebase on libpfm-4.5.0.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 19 2013 William Cohen <wcohen@redhat.com> 4.4.0-2
- Add IBM power 8 support.

* Mon Jun 17 2013 William Cohen <wcohen@redhat.com> 4.4.0-1
- Rebase on libpfm-4.4.0.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 28 2012 William Cohen <wcohen@redhat.com> 4.3.0-2
- Turn off LDCONFIG and remove patch.

* Tue Aug 28 2012 William Cohen <wcohen@redhat.com> 4.3.0-1
- Rebase on libpfm-4.3.0.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 8 2012 William Cohen <wcohen@redhat.com> 4.2.0-7
- Eliminate swig error.

* Thu Jun 7 2012 William Cohen <wcohen@redhat.com> 4.2.0-6
- Eliminate rpm_build_root macro in build section.
- Correct location of shared library files.

* Thu Jun 7 2012 William Cohen <wcohen@redhat.com> 4.2.0-5
- Use siginfo_t for some examples.

* Mon Jun 4 2012 William Cohen <wcohen@redhat.com> 4.2.0-4
- Correct python files.

* Wed Mar 28 2012 William Cohen <wcohen@redhat.com> 4.2.0-3
- Additional spec file fixup for rhbz804666.

* Wed Mar 14 2012 William Cohen <wcohen@redhat.com> 4.2.0-2
- Some spec file fixup.

* Wed Jan 12 2011 Arun Sharma <asharma@fb.com> 4.2.0-0
Initial revision
