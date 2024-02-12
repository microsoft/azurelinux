# git tag
#%%global git_commit trace-cmd-v2.6.2
#%%global git_commit 57371aaa2f469d0ba15fd85276deca7bfdd7ce36

%global srcversion 3.2

Name: trace-cmd
Version: %{srcversion}
Release: 3%{?dist}
License: LGPL-2.1-only AND LGPL-2.1-or-later AND GPL-2.0-only AND GPL-2.0-or-later
Summary: A user interface to Ftrace

ExcludeArch: %{ix86} %{arm}

URL: http://git.kernel.org/?p=linux/kernel/git/rostedt/trace-cmd.git;a=summary
# If upstream does not provide tarballs, to generate:
# git clone https://git.kernel.org/pub/scm/utils/trace-cmd/trace-cmd.git
# cd trace-cmd
# git archive --prefix=trace-cmd-%%{version}/ -o trace-cmd-v%%{version}.tar.gz %%{git_commit}
Source0: https://git.kernel.org/pub/scm/utils/trace-cmd/trace-cmd.git/snapshot/trace-cmd-v%{srcversion}.tar.gz#/%{name}-%{version}.tar.gz
Source1: trace-cmd.conf
Source2: trace-cmd.service
Source3: 98-trace-cmd.rules

BuildRequires: make
BuildRequires: gcc
BuildRequires: xmlto
BuildRequires: asciidoc
BuildRequires: mlocate
BuildRequires: graphviz doxygen
BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: libtraceevent-devel >= 1.8.0
BuildRequires: libtracefs-devel >= 1.8.0
BuildRequires: audit-libs-devel
BuildRequires: chrpath
BuildRequires: swig
BuildRequires: systemd-rpm-macros
BuildRequires: libtracecmd-devel
BuildRequires: libzstd-devel

%description
trace-cmd is a user interface to Ftrace. Instead of needing to use the
debugfs directly, trace-cmd will handle of setting of options and
tracers and will record into a data file.

%package python3
Summary: Python plugin support for trace-cmd
Requires: trace-cmd%{_isa} = %{version}-%{release}
BuildRequires: python3-devel

%description  python3
Python plugin support for trace-cmd

%prep
%autosetup -n %{name}-v%{srcversion}
cp %{SOURCE1} .
cp %{SOURCE2} .
cp %{SOURCE3} .

%build
# MANPAGE_DOCBOOK_XSL define is hack to avoid using locate
MANPAGE_DOCBOOK_XSL=`rpm -ql docbook-style-xsl | grep manpages/docbook.xsl`
CFLAGS="%{optflags} -D_GNU_SOURCE" LDFLAGS="%{build_ldflags}" BUILD_TYPE=Release \
  make V=9999999999 MANPAGE_DOCBOOK_XSL=$MANPAGE_DOCBOOK_XSL \
  prefix=%{_prefix} libdir=%{_libdir} \
  PYTHON_VERS=python3 all_cmd doc
for i in python/*.py ; do 
    sed -i 's/env python2/python3/g' $i
done
chrpath --delete tracecmd/trace-cmd

%install
make libdir=%{_libdir} prefix=%{_prefix} V=1 DESTDIR=%{buildroot}/ CFLAGS="%{optflags} -D_GNU_SOURCE" LDFLAGS="%{build_ldflags} -z muldefs " BUILD_TYPE=Release install install_doc install_python
find %{buildroot}%{_mandir} -type f | xargs chmod u-x,g-x,o-x
find %{buildroot}%{_datadir} -type f | xargs chmod u-x,g-x,o-x
find %{buildroot}%{_libdir} -type f -iname "*.so" | xargs chmod 0755
mkdir -p -m755 %{buildroot}/%{_sysconfdir}/sysconfig/
mkdir -p -m755 %{buildroot}/%{_unitdir}/
mkdir -p -m755 %{buildroot}/%{_udevrulesdir}/
install -p -m 644 trace-cmd.conf %{buildroot}/%{_sysconfdir}/sysconfig/
install -p -m 644 trace-cmd.service %{buildroot}/%{_unitdir}/
install -p -m 644 98-trace-cmd.rules %{buildroot}/%{_udevrulesdir}/
rm -rf %{buildroot}/%{_docdir}/libtracecmd-doc
rm -rf %{buildroot}/%{_mandir}/man3/*

%preun
%systemd_preun %{name}.service

%files
%doc COPYING COPYING.LIB README
%{_bindir}/trace-cmd
%{_mandir}/man1/%{name}*
%{_mandir}/man5/%{name}*
%{_docdir}/trace-cmd/trace-cmd*.html
%{_sysconfdir}/bash_completion.d/trace-cmd.bash
%{_sysconfdir}/sysconfig/trace-cmd.conf
%{_unitdir}/trace-cmd.service
%{_udevrulesdir}/98-trace-cmd.rules

%files python3
%doc Documentation/README.PythonPlugin
%{_libdir}/%{name}/python/

%changelog
* Mon Feb 12 2024 Aadhar Agarwal <aadagarwal@microsoft.com> - 3.2-3
- Initial CBL-Mariner import from Fedora 40 (license: MIT)
- License Verified

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 23 2024 Zamir SUN <sztsian@gmail.com> - 3.2
- Update to 3.2 (#2213350)

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 22 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 3.1.6-3
- Remove lingering kernelshark dependencies

* Mon Jun 05 2023 Zamir SUN <sztsian@gmail.com> - 3.1.6-2
- SPDX migration

* Tue Apr 18 2023 Zamir SUN <sztsian@gmail.com> - 3.1.6-1
- Update to 3.1.6

* Fri Mar 31 2023 Jerome Marchand <jmarchan@redhat.com> - 3.1.4-3
- Fix build: RHBZ#2171770
- Also remove explicit lib dependency that fedpkg lint complains about.

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Oct 11 2022 Zamir SUN <sztsian@gmail.com> - 3.1.4-1
- Update to 3.1.4

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Apr 15 2022 Zamir SUN <sztsian@gmail.com> - 3.0.3-2
- Get rid of the libtracecmd man pages

* Wed Apr 13 2022 Zamir SUN <sztsian@gmail.com> - 3.0.3-1
- Update to 3.0.3

* Fri Mar 18 2022 KUDOH Takashi <t-kudoh@fujitsu.com> - 2.9.7-2
- Add flight recoder service

* Wed Feb 16 2022 Zamir SUN <sztsian@gmail.com> - 2.9.7-1
- Update to 2.9.7

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Apr 23 2021 Jerome Marchand <jmarchan@redhat.com> - 2.9.2-3
- Build w/o rpath as per Fedora packaging guideline

* Mon Mar 29 2021 Zamir SUN <sztsian@gmail.com> - 2.9.2-2
- Fix dependency of libtracecmd
- Resolves https://bugzilla.redhat.com/show_bug.cgi?id=1943919

* Fri Mar 26 2021 Zamir SUN <sztsian@gmail.com> - 2.9.2-1
- Update to 2.9.2

* Wed Mar 24 2021 Jerome Marchand <jmarchan@redhat.com> - 2.9.1-6
- Build with external libtraceevent and libtracefs

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 02 2020 Zamir SUN <sztsian@gmail.com> - 2.9.1-4
- Move %{_libdir}/trace-cmd/python/ to trace-cmd-python3

* Mon Oct 12 2020 Zamir SUN <sztsian@gmail.com> - 2.9.1-3
- Temporary move libtraceevent back to trace-cmd/plugins to mitigate the conflicts

* Tue Sep 29 2020 Zamir SUN <sztsian@gmail.com> - 2.9.1-2
- Remove kernelsharl as it's now separate package

* Fri Aug 07 2020 Zamir SUN <sztsian@gmail.com> - 2.9.1-1
- Update to 2.9.1

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Jeff Law <law@redhat.com> - 2.8.3-3
- TRACECMD_LIBRARY can reference things in TRACEEVENT_LIBRARY, so
  link TRACEEVENT_LIBRARY after TRACECMD_LIBRARY.

* Tue Apr 21 2020 Björn Esser <besser82@fedoraproject.org> - 2.8.3-2
- Rebuild (json-c)

* Sat Feb 08 2020 Zamir SUN <sztsian@gmail.com> - 2.8.3-1
- Update to 2.8
- Add workaround to resolve gcc 10 multiple definition of `common_type_field' problem
- Resolves 1794296
- Resolves 1727368

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.7-8
- Rebuilt for Python 3.8

* Wed Aug 07 2019 Zamir SUN <sztsian@gmail.com> - 2.7-7
- Fix more python2 residuals.
- Fixes 1738158

* Sat Aug 03 2019 Zamir SUN <sztsian@gmail.com> - 2.7-6
- Switch the python plugin to python3

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 02 2018 Zamir SUN <sztsian@gmail.com> - 2.7-2
- Add python plugins

* Fri Mar 02 2018 Zamir SUN <sztsian@gmail.com> - 2.7-1
- Update to 2.7
- Remove Groups tag

* Fri Feb 23 2018 Florian Weimer <fweimer@redhat.com> - 2.6.2-3
- Use LDFLAGS from redhat-rpm-config

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Nov 11 2017 Zamir SUN <zsun@fedoraproject.org> - 2.6.2-1
- Rebase to 2.6.2.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 23 2017 Zamir SUN <zsun@fedoraproject.org> - 2.6.1-1
- Rebase to 2.6.1.

* Thu Mar 30 2017 Zamir SUN <zsun@fedoraproject.org> - 2.6-4.20170330git013205
- Rebase to newest upstream version to include various bug fixes.

* Mon Mar 27 2017 Zamir SUN <zsun@fedoraproject.org> - 2.6-4
- Fix bz1389219 segmentation fault in trace-cmd snapshot

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Oct 19 2016 Zamir SUN <zsun@fedoraproject.org> - 2.6-2
- Add bz1386451-trace-cmd-record-crash-f-before-e.patch
- Fix rpmlint error unstripped-binary-or-object
- Resolves: rhbz#1386451

* Thu Aug 18 2016 Jon Stanley <jonstanley@gmail.com> - 2.6-1
- Upgrade to uptream 2.6
- Rebase distro patch
- Resolves: rhbz#1365951

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Jon Stanley <jonstanley@gmail.com> - 2.2.1-2
- Remove addition to %%files - not needed with Makefile patch

* Tue Jul 23 2013 Dwight Engen <dwight.engen@oracle.com> - 2.2.1-1
- Update to 2.2.1

* Wed Feb 13 2013 Jon Stanley <jonstanley@gmail.com> - 2.1.0-1
- Update to latest upstream

* Thu Sep 13 2012 Jon Stanley <jonstanley@gmail.com> - 1.2-4.20120606git8266dff
- Remove %%defattr

* Thu Sep 06 2012 Jon Stanley <jonstanley@gmail.com> - 1.2-3.20120606git8266dff
- More review fixups

* Tue Aug 28 2012 Jon Stanley <jonstanley@gmail.com> - 1.2-2.20120606git8266dff
- Rebase to git snapshot so it builds
- Fix license tag per review
- Move plugin dir per review

* Mon Aug 27 2012 Jon Stanley <jonstanley@gmail.com> - 1.2-1
- Rebase to 1.2
- Makefile now supports CFLAGS, drop patch

* Sat Feb 19 2011 Jon Stanley <jonstanley@gmail.com> - 1.0.5-1
- Rebase to 1.0.5
- Add Makefile patch to support passing RPM_OPT_FLAGS
- Add kernelshark subpackage
- Initial Fedora version

* Mon Jul 5 2010 John Kacur <jkacur@redhat.com> - 1.0.4-7
- Rebasing to trace-cmd-1.0.4

* Wed Jun 16 2010 John Kacur <jkacur@redhat.com>
- Rebasing to trace-cmd-1.0.2
- Added parse-events-Do-not-fail-on-FORMAT-TOO-BIG-event-err.patch
- Added trace-cmd-Prevent-latency-tracer-plugins-from-doing-.patch
- Added trace-cmd-Prevent-print_graph_duration-buffer-overfl.patch

* Wed Jun 9 2010 John Kacur <jkacur@redhat.com>
- Added trace-cmd-Makefile-EXTRAVERSION-should-be-set-withou.patch
- Added trace-cmd-Makefile-use-a-substitution-reference.patch
- add-DESTDIR-to-make.patch
- Related: rhbz599507

* Fri Jun 4 2010 John Kacur <jkacur@redhat.com>
- Updating to trace-cmd-1.0.1
- Related: rhbz599507

* Wed Apr 21 2010 John Kacur <jkacur@redhat.com>
- Using trick from William Cohen to avoid the "locate" problem.

* Fri Apr 16 2010 John Kacur <jkacur@redhat.com>
- Update the source to the 1.0.0 version
- Many fixes to the spec file.

* Mon Apr 12 2010 William Cohen <wcohen@redhat.com>
- Include manpages in the package.

* Fri Apr 9 2010 John Kacur <jkacur@redhat.com>
- disabled #patch01
- Updated the trace-cmd source
- Changed version to 0.7.0
- Added bogus patch to satisfy rpm requirements
- Related:bz519630

* Mon Mar 15 2010 John Kacur <jkacur@redhat.com>
- disabled trace-cmd_rusage.patch
- Updated the trace-cmd source
- Related:bz519630

* Fri Nov 16 2007 Luis Claudio R. Goncalves <lgoncalv@redhat.com> - 1.0-1%{?dist}
- Initial packaging
- Added a patch to display rusage information
