# git tag
#%%global git_commit trace-cmd-v2.6.2
#%%global git_commit 57371aaa2f469d0ba15fd85276deca7bfdd7ce36

Name:          trace-cmd
Version:       3.2
Release:       1%{?dist}
License:       LGPL-2.1-only AND LGPL-2.1-or-later AND GPL-2.0-only AND GPL-2.0-or-later
Summary:       A user interface to Ftrace

ExcludeArch:   %{ix86} %{arm}

# If upstream does not provide tarballs, to generate:
# git clone https://git.kernel.org/pub/scm/utils/trace-cmd/trace-cmd.git
# cd trace-cmd
# git archive --prefix=trace-cmd-%%{version}/ -o trace-cmd-v%%{version}.tar.gz %%{git_commit}
URL:           http://git.kernel.org/?p=linux/kernel/git/rostedt/trace-cmd.git;a=summary
Source0:       https://git.kernel.org/pub/scm/utils/trace-cmd/trace-cmd.git/snapshot/trace-cmd-v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:       trace-cmd.conf
Source2:       trace-cmd.service
Source3:       98-trace-cmd.rules

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
%autosetup -n %{name}-v%{version}
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
make libdir=%{_libdir} prefix=%{_prefix} PYTHON_VERS=python3 V=1 DESTDIR=%{buildroot}/ CFLAGS="%{optflags} -D_GNU_SOURCE" LDFLAGS="%{build_ldflags} -z muldefs " BUILD_TYPE=Release install install_doc install_python
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
* Mon Feb 12 2024 Aadhar Agarwal <aadagarwal@microsoft.com> - 3.2-1
- Initial Azure Linux import from Fedora 40 (license: MIT)
- License Verified
