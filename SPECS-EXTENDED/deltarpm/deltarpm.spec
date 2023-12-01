Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           deltarpm
Summary:        Create deltas between rpms
Version:        3.6.2
Release:        7%{?dist}
License:        BSD
URL:            https://github.com/rpm-software-management/deltarpm
Source:         %{url}/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  bzip2-devel
BuildRequires:  libzstd-devel
BuildRequires:  perl-generators
BuildRequires:  xz-devel
BuildRequires:  rpm-devel
BuildRequires:  popt-devel
BuildRequires:  zlib-devel

%description
A deltarpm contains the difference between an old
and a new version of a rpm, which makes it possible
to recreate the new rpm from the deltarpm and the old
one. You don't have to have a copy of the old rpm,
deltarpms can also work with installed rpms.

%package -n drpmsync
Summary:        Sync a file tree with deltarpms
Requires:       %{name}%{_isa} = %{version}-%{release}

%description -n drpmsync
This package contains a tool to sync a file tree with
deltarpms.

%package -n deltaiso
Summary:        Create deltas between isos containing rpms
Requires:       %{name}%{_isa} = %{version}-%{release}

%description -n deltaiso
This package contains tools for creating and using deltasisos,
a difference between an old and a new iso containing rpms.

%package -n python3-%{name}
Summary:        Python bindings for deltarpm
%{?python_provide:%python_provide python3-%{name}}
BuildRequires:  python3-devel
Requires:       %{name}%{_isa} = %{version}-%{release}

%description -n python3-%{name}
This package contains python bindings for deltarpm.

Python 3 version.

%prep
%autosetup -p1

%build
%{__make} %{?_smp_mflags} CFLAGS="%{build_cflags} -DWITH_ZSTD=1" LDFLAGS="%{build_ldflags}" \
    bindir=%{_bindir} libdir=%{_libdir} mandir=%{_mandir} prefix=%{_prefix} \
    zlibbundled='' zlibldflags='-lz' zlibcppflags=''

%{__make} %{?_smp_mflags} CFLAGS="%{build_cflags} -DWITH_ZSTD=1" LDFLAGS="%{build_ldflags}" \
    bindir=%{_bindir} libdir=%{_libdir} mandir=%{_mandir} prefix=%{_prefix} \
    zlibbundled='' zlibldflags='-lz' zlibcppflags='' \
    python

%install
%makeinstall pylibprefix=%{buildroot}

%files
%license LICENSE.BSD
%doc README NEWS
%{_bindir}/applydeltarpm
%{_mandir}/man8/applydeltarpm.8*
%{_bindir}/combinedeltarpm
%{_mandir}/man8/combinedeltarpm.8*
%{_bindir}/makedeltarpm
%{_mandir}/man8/makedeltarpm.8*
%{_bindir}/rpmdumpheader

%files -n deltaiso
%{_bindir}/applydeltaiso
%{_mandir}/man8/applydeltaiso.8*
%{_bindir}/fragiso
%{_mandir}/man8/fragiso.8*
%{_bindir}/makedeltaiso
%{_mandir}/man8/makedeltaiso.8*

%files -n drpmsync
%{_bindir}/drpmsync
%{_mandir}/man8/drpmsync.8*

%files -n python3-%{name}
%{python3_sitearch}/%{name}.py
%{python3_sitearch}/_%{name}module.so
%{python3_sitearch}/__pycache__/%{name}.*

%changelog
* Tue Jun 01 2021 Olivia Crain <oliviacrain@microsoft.com> - 3.6.2-7
- Remove unneeded deletion of Python 2 sitelib in buildroot

* Fri Mar 05 2021 Henry Li <lihl@microsoft.com> - 3.6.2-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove python2 instances

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.6.2-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.6.2-3
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 13 13:46:17 EDT 2019 Neal Gompa <ngompa13@gmail.com> - 3.6.2-1
- Update to 3.6.2
- Drop all upstreamed patches
- Enable zstd payload support

* Mon Jun 10 22:13:18 CET 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.6-32
- Rebuild for RPM 4.15

* Mon Jun 10 15:42:01 CET 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.6-31
- Rebuild for RPM 4.15

* Sun Mar 17 2019 Miro Hrončok <mhroncok@redhat.com> - 3.6-30
- Subpackage python2-deltarpm has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Jonathan Dieter <jdieter@gmail.com> - 3.6-28
- Fix python2 build error

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.6-26
- Rebuilt for Python 3.7

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Aug 11 2017 Igor Gnatenko <ignatenko@redhat.com> - 3.6-24
- Rebuilt after RPM update (№ 3)

* Thu Aug 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 3.6-23
- Rebuilt for RPM soname bump

* Thu Aug 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 3.6-22
- Rebuilt for RPM soname bump

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 3.6-18
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-17
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Apr 13 2016 Igor Gnatenko <ignatenko@redhat.com> - 3.6-16
- Make python3 builds conditionally
- Follow new packaging guidelines
- Use modern macroses like %%autosetup
- Remove duplicated doc files

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Jonathan Dieter <jdieter@lesbg.com> - 3.6-14
- Remove unneeded defattr

* Sat Nov 14 2015 Jonathan Dieter <jdieter@lesbg.com> - 3.6-13
- Enable PIE (RHBZ: #1281830)

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-12
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Sat Sep 05 2015 Kalev Lember <klember@redhat.com> - 3.6-11
- Rebuilt for librpm soname bump

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 3.6-9
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Wed Jan 14 2015 Jonathan Dieter <jdieter@lesbg.com> - 3.6-8
- Add upstream patch to fix rare off-by-one error
- Add upstream patch to do more fflush()'s in applydeltaiso (#725791)

* Mon Jan 12 2015 Jonathan Dieter <jdieter@lesbg.com> - 3.6-7
- Add upstream patches to fix a few small bugs
- Do better error check in low memory situations (#791359)
 
* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 3.6-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 3.6-2
- Perl 5.18 rebuild

* Thu Jun 20 2013 Jonathan Dieter <jdieter@lesbg.com> - 3.6-1
- Update to 3.6 which, among other things, fixes a bug when applying a deltarpm
  to create a gzip-compressed rpm using full compression

* Mon May 20 2013 Jonathan Dieter <jdieter@lesbg.com> - 3.6-0.13.20130520git
- Clearer error message when applydeltaiso fails (#825428) (Thanks, John!)
- Add details to applydeltaiso and makedeltaiso man pages (#569499)
- Add fragiso man page to deltaiso package (#569776)
- Fix section for applydeltaiso (#548970)
- Add arch-specific requires (#677060)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-0.12.20110223git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 03 2012 David Malcolm <dmalcolm@redhat.com> - 3.6-0.11.20110223git
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 3.6-0.10.20110223git
- remove rhel logic from with_python3 conditional

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-0.9.20110223git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 20 2012 Jindrich Novy <jnovy@redhat.com> - 3.6-0.8.20110223git
- rebuild against new rpm

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-0.7.20110223git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 23 2011 - Jonathan Dieter <jdieter@lesbg.com> - 3.6-0.6.20110223git
- Fix makedeltaiso so it (partially) works when compression formats change
- Fix fix for makedeltaiso so it gets checksums right

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-0.5.20110121git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 21 2011 - Jonathan Dieter <jdieter@lesbg.com> - 3.6-0.4.20110121git
- Python 3 module now works again

* Tue Jan 18 2011 - Jonathan Dieter <jdieter@lesbg.com> - 3.6-0.4.20110118git
- Re-enable Python 3 support, but it still won't work even though it builds
- Remove upstreamed patches

* Tue Jan 18 2011 - Richard W.M. Jones <rjones@redhat.com> - 3.6-0.3.20101230git
- Disable Python 3 support, since it is quite broken.

* Thu Dec 30 2010 Jonathan Dieter <jdieter@lesbg.com> - 3.6-0.1.20101230git
- Update to current git
- Temporary extra verbosity patch
- Add groups to subpackages for EL5

* Thu Jul  8 2010 Jonathan Dieter <jdieter@lesbg.com> - 3.6-0.1.20100708git
- Deltarpm can now limit memory usage when generating deltarpms

* Wed Feb 10 2010 Thomas Spura <tomspur@fedoraproject.org> - 3.5-0.7.20100121git
- build python3-deltarpm

* Thu Jan 21 2010 Jonathan Dieter <jdieter@lesbg.com> - 3.5-0.6.20100121git
- Make rpmio link explicit

* Tue Dec 08 2009 Jesse Keating <jkeating@redhat.com> - 3.5-0.5.20090913git
- Rebuild for new rpm

* Wed Sep 30 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 3.5-0.4.20090913git
- Update patch to properly detect when an rpm is built with an rsync-friendly
  zlib and bail out.

* Wed Sep 30 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 3.5-0.3.20090913git
- Make building with system zlib selectable at build time.
- Fix cfile_detect_rsync() to detect rsync even if we don't have a zlib capable
  of making rsync-friendly compressed files.

* Wed Sep 30 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 3.5-0.2.20090913git
- Correct prerelease rlease numbering.
- Build against the system zlib, not the bundled library.  This remedies the
  fact that the included zlib is affected by CAN-2005-1849.

* Sun Sep 13 2009 Jonathan Dieter <jdieter@lesbg.com> - 3.5-0.git.20090913
- Merge python error patch upstream

* Thu Sep 10 2009 Bill Nottingham <notting@redhat.com> - 3.5-0.git.20090831.1.4
- fix python bindings to not require kernel >= 2.6.27

* Wed Sep  9 2009 Bill Nottingham <notting@redhat.com> - 3.5-0.git.20090831.1.3
- fix python bindings to:
  - call _exit(), not exit()
  - properly pythonize errors
  - not leak file descriptors

* Mon Aug 31 2009 Jonathan Dieter <jdieter@lesbg.com> - 3.5-0.git.20090831.1
- Add python bindings sub-package
- Fix build error

* Mon Aug 17 2009 Jonathan Dieter <jdieter@gmail.com> - 3.5-0.git.20090729.1
- Explain where we get the source from
- Split *deltaiso commands into deltaiso subpackage (#501953)

* Wed Jul 29 2009 Jonathan Dieter <jdieter@gmail.com> - 3.5-0.git.20090729
- Fix bug in writing Fedora's xz-compressed rpms (surely that's the last one)

* Mon Jul 27 2009 Jonathan Dieter <jdieter@gmail.com> - 3.5-0.git.20090727.1
- Fix bug in reading Fedora's xz-compressed rpms

* Mon Jul 27 2009 Jonathan Dieter <jdieter@gmail.com> - 3.5-0.git.20090727
- Update to current upstream git repository
- Add upstream xz compression support
- Drop all patches (they're now in upstream)
- Fix spelling mistakes (#505713)
- Fix url error (#506179)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 22 2009 Jonathan Dieter <jdieter@gmail.com> - 3.4-16
- Split drpmsync into a separate subpackage (#489231)

* Thu Mar 26 2009 Jonathan Dieter <jdieter@gmail.com> - 3.4-15
- Fix bug when checking sequence with new sha256 file digests

* Tue Mar 24 2009 Jonathan Dieter <jdieter@gmail.com> - 3.4-14
- Add support for rpms with sha256 file digests

* Fri Mar 06 2009 Jesse Keating <jkeating@redhat.com> - 3.4-13
- Rebuild for new rpm libs

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jul 13 2008 Jonathan Dieter <jdieter@gmail.com> - 3.4-11
- Rebuild for rpm 4.6

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.4-10
- Autorebuild for GCC 4.3

* Mon Jan  7 2008 Jonathan Dieter <jdieter@gmail.com> - 3.4-9
- Add patch that allows deltarpm to rebuild rpms from deltarpms that have
  had the rpm signature added after their creation.  The code came from
  upstream.
- Drop nodoc patch added in 3.4-4 as most packages in repository have been
  updated since April-May 2007 and this patch was supposed to be temporary.

* Wed Aug 29 2007 Jonathan Dieter <jdieter@gmail.com> - 3.4-6
- Bring in popt-devel in BuildRequires to fix build in x86_64

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 3.4-5
- Rebuild for selinux ppc32 issue.

* Wed Jul 11 2007 Jonathan Dieter <jdieter@gmail.com> - 3.4-4
- Fix prelink bug
- Ignore verify bits on doc files as they were set incorrectly in older
  versions of rpm.  Without this patch, deltarpm will not delta doc files
  in rpm created before April-May 2007

* Tue Jun  5 2007 Jeremy Katz <katzj@redhat.com> - 3.4-3
- include colored binaries from non-multilib-dirs so that deltas can work 
  on multilib platforms

* Wed May 09 2007 Adam Jackson <ajax@redhat.com> 3.4-2
- Add -a flag to work around multilib ignorance. (#238964)

* Tue Mar 06 2007 Adam Jackson <ajax@redhat.com> 3.4-1
- Update to 3.4 (#231154)

* Mon Feb 12 2007 Adam Jackson <ajax@redhat.com> 3.3-7
- Add RPM_OPT_FLAGS to make line. (#227380)

* Mon Feb 05 2007 Adam Jackson <ajax@redhat.com> 3.3-6
- Fix rpm db corruption in rpmdumpheader.  (#227326)

* Mon Sep 11 2006 Mihai Ibanescu <misa@redhat.com> - 3.3-5
- Rebuilding for new toolset

* Thu Aug 17 2006 Mihai Ibanescu <misa@redhat.com> - 3.3-4
- Removing BuildRequires: gcc

* Tue Aug 15 2006 Mihai Ibanescu <misa@redhat.com> - 3.3-3
- Fedora packaging guidelines build

* Tue Aug  8 2006 Mihai Ibanescu <misa@redhat.com> - 3.3-2
- Added BuildRequires: rpm-devel, gcc

* Sat Dec 03 2005 Dries Verachtert <dries@ulyssis.org> - 3.3-1 - 3768/dries
- Initial package.
