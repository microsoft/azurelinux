# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           waf
Version:        2.1.9
Release:        1%{?dist}
Summary:        A Python-based build system
# The entire source code is BSD apart from pproc.py (taken from Python 2.5)
# Automatically converted from old format: BSD and Python - review is highly recommended.
License:        LicenseRef-Callaway-BSD AND LicenseRef-Callaway-Python
URL:            https://waf.io/
# Original tarfile can be found at
# https://waf.io/waf-%%{version}.tar.bz2
# We remove waf logos, licensed CC BY-NC
Source:         waf-%{version}.stripped.tar.bz2
Source1:        unpack_wafdir.py
# also search for waflib in /usr/share/waf
Patch0:         waf-2.0.18-libdir.patch
# do not try to use the (removed) waf logos
Patch1:         waf-2.0.18-logo.patch
# do not add -W when running sphinx-build
Patch2:         waf-2.0.18-sphinx-no-W.patch

# Enable building without html docs (e.g. in case no recent sphinx is
# available)
%bcond_without docs

BuildArch:      noarch
BuildRequires:  python3-devel
%if %{with docs}
BuildRequires:  python3-sphinx
BuildRequires:  graphviz
BuildRequires:  ImageMagick
%endif # with docs

# waf-2.0.18-2 in F32 the first python3-only version (i.e. not having
# a -python3 subpackage). Do not hardcode that as Obsoletes: though,
# to be able to roll out e.g. a 2.0.19 for older Fedora branches, but
# maintain upgradability
Provides:       %{name}-python3 = %{version}-%{release}
Obsoletes:      %{name}-python3 < %{version}-%{release}

%if "%{?python3_version}" != ""
# Seems like automatic ABI dependency is not detected since the files
# are going to a non-standard location
Requires:       python(abi) = %{python3_version}
%endif

# the demo suite contains a perl module, which draws in unwanted
# provides and requires
%global __requires_exclude_from ^%{_docdir}/.*$
%global __provides_exclude_from ^%{_docdir}/.*$

%global _description %{expand:
Waf is a Python-based framework for configuring, compiling and
installing applications. It is a replacement for other tools such as
Autotools, Scons, CMake or Ant.}

%description %_description


%if %{with docs}
%package -n %{name}-doc
Summary:        Documentation for %{name}
Requires:       %{name} = %{version}-%{release}

%description -n %{name}-doc %_description

This package contains the HTML documentation for %{name}.
%endif # with docs


%prep
%autosetup -p1


%build
extras=
for f in waflib/extras/*.py ; do
  f=$(basename "$f" .py);
  if [ "$f" != "__init__" ]; then
    extras="${extras:+$extras,}$f" ;
  fi
done
%{__python3} ./waf-light --make-waf --strip --tools="$extras"

%if %{with docs}
# build html docs
export WAFDIR=$(pwd)
pushd docs/sphinx
%{__python3} ../../waf -v configure build
popd
%endif # with docs


%install
%{__python3} %{S:1} _temp
pushd _temp
find . -name '*.py' -printf '%%P\0' |
  xargs -0 -I{} install -m 0644 -p -D {} %{buildroot}%{_datadir}/waf3/{}
popd

# install the frontend
install -m 0755 -p -D waf-light %{buildroot}%{_bindir}/waf
ln -s waf %{buildroot}%{_bindir}/waf-3
ln -s waf %{buildroot}%{_bindir}/waf-%{python3_version}

# remove shebangs from and fix EOL for all scripts in wafadmin
find %{buildroot}%{_datadir}/ -name '*.py' \
     -exec sed -i -e '1{/^#!/d}' -e 's|\r$||g' {} \;

# fix waf script shebang line
sed -i "1c#! %{__python3}" %{buildroot}%{_bindir}/waf

# remove x-bits from everything going to doc
find demos utils -type f -exec chmod 0644 {} \;

# fix shebang lines in the demos
find demos \( -name '*.py' -o -name '*.py.in' -o -name 'wscript' -o -name 'wscript_build' \) \
  -exec sed -e '1{/^#!/d}' -e '1i#!%{__python3}' -i {} \;

# remove hidden file
rm -f docs/sphinx/build/html/.buildinfo

# do byte compilation
%py_byte_compile %{__python3} %{buildroot}%{_datadir}/waf3


%files
%doc README.md ChangeLog demos
%{_bindir}/waf-%{python3_version}
%{_bindir}/waf-3
%{_bindir}/waf
%{_datadir}/waf3


%if %{with docs}
%files -n %{name}-doc
%doc docs/sphinx/build/html
%endif # with docs


%changelog
* Sat Nov 15 2025 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.9-1
- Update to 2.1.9.

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.1.6-4
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.1.6-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jun 20 2025 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.6-1
- Update to 2.1.6.

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 2.1.5-2
- Rebuilt for Python 3.14

* Sun Mar  9 2025 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.5-1
- Update to 2.1.5.

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Sep  7 2024 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.2-1
- Update to 2.1.2.

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 2.0.27-4
- convert license to SPDX

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.0.27-2
- Rebuilt for Python 3.13

* Thu Apr  4 2024 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.27-1
- Update to 2.0.27.

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Oct 22 2023 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.26-1
- Update to 2.0.26.

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 2.0.25-3
- Rebuilt for Python 3.12

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan  5 2023 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.25-1
- Update to 2.0.25.

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.0.24-2
- Rebuilt for Python 3.11

* Sat May 28 2022 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.24-1
- Update to 2.0.24.

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 22 2021 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.23-1
- Update to 2.0.23.

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.0.22-2
- Rebuilt for Python 3.10

* Tue Feb  2 2021 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.22-1
- Update to 2.0.22.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 16 2020 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.21-1
- Update to 2.0.21.

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 25 2020 Miro Hrončok <mhroncok@redhat.com> - 2.0.20-2
- Rebuilt for Python 3.9

* Tue Apr 14 2020 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.20-1
- Update to 2.0.20.

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 28 2019 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.19-1
- Update to 2.0.19.

* Tue Oct  8 2019 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.18-2
- Make waf Python3-only (#1753963).
- Spec file modernization and cleanups.

* Sat Oct  5 2019 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.18-1
- Update to 2.0.18.

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.0.17-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.0.17-3
- Rebuilt for Python 3.8

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun  5 2019 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.17-1
- Update to 2.0.17.

* Sun May 19 2019 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.16-1
- Update to 2.0.16.

* Wed May 15 2019 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.15-1
- Update to 2.0.15.

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Dec 30 2018 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.14-1
- Update to 2.0.14.

* Mon Nov 12 2018 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.12-1
- Update to 2.0.12.

* Wed Aug 15 2018 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.10-1
- Update to 2.0.10.

* Fri Jul 20 2018 Thomas Moschny <thomas.moschny@gmx.de> - 1.9.14-2
- Spec file cleanups.
- Add unpack_wafdir.py (rhbz#1509550).
- Fix rpmlint issue (rhbz#1509716).
- Fix doc building (rhbz#1512232).

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.14-1.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.9.14-1.2
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.14-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Oct 21 2017 Thomas Moschny <thomas.moschny@gmx.de> - 1.9.14-1
- Update to 1.9.14.

* Wed Aug 30 2017 Thomas Moschny <thomas.moschny@gmx.de> - 1.9.13-1
- Update to 1.9.13.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.12-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun  4 2017 Thomas Moschny <thomas.moschny@gmx.de> - 1.9.12-1
- Update to 1.9.12.

* Mon May 15 2017 Thomas Moschny <thomas.moschny@gmx.de> - 1.9.11-1
- Update to 1.9.11.

* Sun Apr 23 2017 Thomas Moschny <thomas.moschny@gmx.de> - 1.9.10-1
- Update to 1.9.10.

* Wed Apr  5 2017 Thomas Moschny <thomas.moschny@gmx.de> - 1.9.9-1
- Update to 1.9.9.
- Use alternatives to manage %%{_bindir}/waf (rhbz#1404699).

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.7-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.9.7-1.1
- Rebuild for Python 3.6

* Wed Dec 14 2016 Thomas Moschny <thomas.moschny@gmx.de> - 1.9.7-1
- Update to 1.9.7.

* Sat Dec  3 2016 Thomas Moschny <thomas.moschny@gmx.de> - 1.9.6-1
- Update to 1.9.6.

* Mon Oct 10 2016 Thomas Moschny <thomas.moschny@gmx.de> - 1.9.5-1
- Update to 1.9.5.

* Sat Sep 24 2016 Thomas Moschny <thomas.moschny@gmx.de> - 1.9.4-1
- Update to 1.9.4.

* Sat Aug 27 2016 Thomas Moschny <thomas.moschny@gmx.de> - 1.9.3-1
- Update to 1.9.3.

* Thu Aug  4 2016 Thomas Moschny <thomas.moschny@gmx.de> - 1.9.2-1
- Update to 1.9.2.

* Thu Aug  4 2016 Thomas Moschny <thomas.moschny@gmx.de> - 1.9.1-1
- Update to 1.9.1.
- Fix some rpmlint warnings.

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.22-1.1
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Jul  4 2016 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.22-1
- Update to 1.8.22.

* Tue May 24 2016 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.21-1
- Update to 1.8.21.

* Mon Mar  7 2016 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.20-1
- Update to 1.8.20.

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.19-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Feb  1 2016 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.19-1
- Update to 1.8.19.

* Sat Jan  9 2016 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.18-1
- Update to 1.8.18.

* Sat Dec 19 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.17-1
- Update to 1.8.17.

* Fri Nov 20 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.16-1
- Update to 1.8.16.
- Remove patch applied upstream.

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.15-2.1
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Sat Oct 24 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.15-2
- Update Sphinx config patch to also work with Sphinx 1.1.

* Sat Oct 24 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.15-1
- Update to 1.8.15.

* Sun Oct 11 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.14-1
- Update to 1.8.14.
- Include waf-2 and waf-3 symlinks, respectively.
- Add basic doc files to the python3 subpackage.

* Sat Jul 25 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.12-1
- Update to 1.8.12.

* Mon Jun 22 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.11-2
- Patch to remove -W from sphinx-build call, in order to build with
  older sphinx.
- Rebase libdir patch.

* Mon Jun 22 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.11-1
- Update to 1.8.11.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.9-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May  1 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.9-1
- Update to 1.8.9.
- Update upstream URL.

* Sun Apr 19 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.8-2
- Project moved to github.

* Sun Apr 19 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.8-1
- Update to 1.8.8.
- Apply updated Python packaging guidelines.

* Sun Mar  1 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.7-1
- Update to 1.8.7.

* Sun Feb 22 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.6-1
- Update to 1.8.6.

* Thu Dec 18 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.5-1
- Update to 1.8.5.

* Sat Nov 22 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.4-1
- Update to 1.8.4.

* Sun Oct 12 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.2-1
- Update to 1.8.2.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.16-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 1.7.16-1.1
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri Mar 21 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.16-1
- Update to 1.7.16.
- Update download URL.

* Sat Jan 25 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.15-1
- Update to 1.7.15.
- Modernize spec file.

* Tue Jan  7 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.14-1
- Update to 1.7.14.

* Tue Sep 10 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.13-1
- Update to 1.7.13.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.11-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun May 26 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.11-1
- Update to 1.7.11.

* Fri Mar 22 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.10-1
- Update to 1.7.10.

* Sat Mar  9 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.9-2
- Add fix for FTBFS bug rhbz#914566.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.9-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 13 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.9-1
- Update to 1.7.9.

* Fri Dec 21 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.8-1
- Update to 1.7.8.

* Sun Dec 16 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.7-1
- Update to 1.7.7.

* Tue Nov 20 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.6-1
- Update to 1.7.6.

* Tue Oct  2 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.5-1
- Update to 1.7.5.

* Wed Sep 26 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.4-1
- Update to 1.7.4.

* Mon Aug  6 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.2-1
- Update to 1.7.2.

* Sat Aug  4 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.1-1
- Update to 1.7.1.
- Remove rhel logic from with_python3 conditional.

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 1.7.0-1.2
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.0-1
- Update to 1.7.0.

* Sat Jun 16 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.0-0.2.pre5
- Update to 1.7.0pre5.

* Thu Jun  7 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.0-0.1.pre4
- Update to 1.7.0pre4.

* Thu Jun  7 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.0-0.2.pre3
- Add patch for waf issue #1171.
- Spec file fixes.

* Thu Jun  7 2012 Michel Salim <salimma@fedoraproject.org> - 1.7.0-0.1.pre3
- Update to 1.7.0pre3
- Spec clean-up
- Rename -docs subpackage to -doc, per guidelines

* Mon Feb  6 2012 Michel Salim <salimma@fedoraproject.org> - 1.6.11-1
- Update to 1.6.11
- Build in verbose mode

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Dec 18 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.6.10-1
- Update to 1.6.10.
- Remove patch applied upstream.

* Sat Nov 26 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.6.9-1
- Update to 1.6.9.
- Patch to not use the logo (which has been removed) in the docs.

* Mon Oct  3 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.6.8-1
- Update to 1.6.8.
- Use rpm 4.9.X style provides/requires filtering.
- Move Python3 version to a subpackage.
- Move HTML documentation to a subpackage.

* Sat Jun 18 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.6.6-1
- Update to 1.6.6.
- Remove unused extras/subprocess.py.
- Small patch for syntax errors.

* Sun Apr 17 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.6.4-1
- Update to 1.6.4.

* Sat Apr  9 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.6.3-2
- Use python-sphinx10 where available.
- Turn off standard brp-python-bytecompile only when building the
  python3 subpackage.

* Sat Feb 19 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.6.3-1
- Update to 1.6.3.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 22 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.6.2-4
- Update libdir patch for py3k.
- Add patch to fix syntax error in extras/boost.py.
- Remove hidden file.

* Fri Jan 21 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.6.2-3
- Make waf compatible with python3, if available.

* Tue Jan 18 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.6.2-2
- Enable building without html docs.

* Sat Jan 15 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.6.2-1
- Update to 1.6.2.
- Generate and include html docs.
- Upstream removed the 'install' target, so we need to copy waflib
  manually.
- The bash completion file is not provided anymore.

* Fri Oct  1 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.19-1
- Update to 1.5.19.

* Fri Jul 30 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.18-3
- Require 'python(abi)' instead of 'python-abi', seems more common
  now.

* Fri Jul 30 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.18-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 11 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.18-1
- Update to 1.5.18.

* Mon May 24 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.17-1
- Update to 1.5.17.
- Add patch from issue 682 to install 3rd party tools.

* Mon Apr  5 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.15-1
- Update to 1.5.15.

* Sun Mar  7 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.14-1
- Update to 1.5.14.

* Wed Mar  3 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.13-1
- Update to 1.5.13.

* Sun Feb 14 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.12-1
- Update to 1.5.12.

* Mon Jan 18 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.11-1
- Update to 1.5.11.
- Use %%global instead of %%define.

* Mon Nov 16 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.10-1
- Update to 1.5.10.

* Mon Aug 31 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.9-1
- Update to 1.5.9.
- Rebase libdir patch.

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 11 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.8-1
- Update to 1.5.8.

* Tue May  5 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.6-1
- Update to 1.5.6.

* Mon Apr 20 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.5-1
- Update to 1.5.5.

* Tue Apr  7 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.4-1
- Update to 1.5.4.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb  2 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.3-1
- Update to 1.5.3, which contains various enhancements and bugfixes,
  see http://waf.googlecode.com/svn/trunk/ChangeLog for a list of
  changes.

* Fri Jan 16 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.2-2
- Remove the documentation again, as it is under CC-BY-NC-ND. Also
  remove it from the tarfile.

* Fri Jan 16 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.2-1
- Update to 1.5.2.
- Generate html documentation (though without highlighting).

* Fri Dec 19 2008 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.1-1
- Update to 1.5.1.

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.4.4-2
- Rebuild for Python 2.6

* Sun Aug 31 2008 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.4-1
- Update to 1.4.4:
  - python 2.3 compatibility was restored
  - task randomization was removed
  - the vala tool was updated

* Sat Jun 28 2008 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.3-1
- Update to 1.4.3.
- Remove fcntl patch (fixed upstream).
- Prefix has to be set in a configure step now.
- Pack the bash completion file.

* Mon May 26 2008 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.2-2
- Patch: stdout might not be a terminal.

* Sat May 17 2008 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.2-1
- Update to 1.4.2.
- Remove shebang lines from files in wafadmin after installation, not
  before, otherwise install will re-add them.

* Sun May  4 2008 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.1-1
- Update to upstream version 1.4.1.

* Sat Apr 19 2008 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.0-1
- Update to upstream version 1.4.0.

* Wed Apr  9 2008 Thomas Moschny <thomas.moschny@gmx.de> - 1.3.2-6
- Upstream patch to fix latex dependency scanning: trunk rev 2340.

* Sun Feb 10 2008 Thomas Moschny <thomas.moschny@gmx.de> - 1.3.2-5
- Update to 1.3.2.
- Remove version and revision information from path to waf cache.

* Fri Feb  1 2008 Michel Salim <michel.sylvan@gmail.com> - 1.3.1-4
- Upstream patch to fix check_tool('gnome'): trunk rev 2219

* Mon Jan 28 2008 Michel Salim <michel.sylvan@gmail.com> - 1.3.1-3
- Fix python-abi requirement so it can be parsed before python is installed
- rpmlint tidying-up

* Fri Jan 25 2008 Michel Salim <michel.sylvan@gmail.com> - 1.3.1-2
- Merge in changes from Thomas Mochny <thomas.moschny@gmx.de>:
  * WAF cache moved from /usr/lib to /usr/share
  * Remove shebangs from scripts not meant from users, rather than
    making them executable
  * Include tools and demos

* Sun Jan 20 2008 Michel Salim <michel.sylvan@gmail.com> - 1.3.1-1
- Initial Fedora package
