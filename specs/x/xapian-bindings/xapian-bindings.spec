# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global tcl_version 8.6
%global tcl_sitearch %{_libdir}/tcl%{tcl_version}

Name:          xapian-bindings
Version:       1.4.29
Release: 6%{?dist}
Summary:       Bindings for the Xapian Probabilistic Information Retrieval Library

# Automatically converted from old format: GPLv2+ - review is highly recommended.
License:       GPL-2.0-or-later
URL:           https://www.xapian.org/
Source0:       https://www.oligarchy.co.uk/xapian/%{version}/%{name}-%{version}.tar.xz

BuildRequires: gcc-c++
BuildRequires: libuuid-devel
BuildRequires: make
BuildRequires: python3-devel python3-setuptools python3-sphinx
BuildRequires: ruby ruby-devel rubygems rubygem-rdoc rubygem-json
BuildRequires: tcl-devel
BuildRequires: xapian-core-devel
BuildRequires: zlib-devel

# Filter private-shared-object-provides
%{?filter_setup}

%description
Xapian is an Open Source Probabilistic Information Retrieval Library. It
offers a highly adaptable toolkit that allows developers to easily add advanced
indexing and search facilities to applications. This package provides the
files needed for scripts which use Xapian.

%package -n python3-xapian
Summary:       Python 3 bindings for Xapian
Requires:      %{name} = %{version}-%{release}
%{?python_provide:%python_provide python3-xapian}

%description -n python3-xapian
Xapian is an Open Source Probabilistic Information Retrieval framework. It
offers a highly adaptable toolkit that allows developers to easily add advanced
indexing and search facilities to applications. This package provides the
bindings needed for developing Python3 scripts which use Xapian.

%package ruby
Summary:       Files needed for developing Ruby scripts which use Xapian
Requires:      %{name} = %{version}-%{release}
Requires:      ruby-libs

%description ruby
Xapian is an Open Source Probabilistic Information Retrieval framework. It
offers a highly adaptable toolkit that allows developers to easily add advanced
indexing and search facilities to applications. This package provides the
files needed for developing Ruby scripts which use Xapian

%package -n tcl-xapian
Summary:       Files needed for developing TCL scripts which use Xapian
Requires:      %{name} = %{version}-%{release}
Requires:      tcl >= %{tcl_version}

%description -n tcl-xapian
Xapian is an Open Source Probabilistic Information Retrieval framework. It
offers a highly adaptable toolkit that allows developers to easily add advanced
indexing and search facilities to applications. This package provides the
files needed for developing TCL scripts which use Xapian

%prep
%autosetup -p1

# There is no sphinx.main in Sphinx 2
sed -i 's/sphinx\.main/sphinx.cmd.build.main/g' $(grep -r 'sphinx\.main' -l)
sed -i 's/import sphinx/import sphinx.cmd.build/g' $(grep -r 'import sphinx' -l)

%build
export PYTHON3_LIB=%{python3_sitelib}
export RUBY_LIB=%{ruby_vendorlibdir}
export RUBY_LIB_ARCH=%{ruby_vendorarchdir}
export TCL_LIB=%{tcl_sitearch}

%configure --with-python3 --with-ruby --with-tcl

%{make_build}

%install
%{make_install}

# Remove the dev docs, we pick them up below
rm -rf %{buildroot}%{_datadir}/doc/%{name}

%check
#make check

%files
%license COPYING
%doc AUTHORS NEWS README

%files -n python3-xapian
%{python3_sitelib}/xapian/

%files ruby
%{ruby_vendorarchdir}/_xapian.so
%{ruby_vendorlibdir}/xapian.rb

%files -n tcl-xapian
%{tcl_sitearch}/xapian%{version}/

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.4.29-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.4.29-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.4.29-2
- Rebuilt for Python 3.14

* Thu May 01 2025 Christiano Anderson <chris@christiano.dev> - 1.4.29-1
- Update to 1.4.29

* Sun Mar 30 2025 Christiano Anderson <chris@christiano.dev> - 1.4.27-1
- Update to 1.4.27

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 08 2025 Vít Ondruch <vondruch@redhat.com> - 1.4.26-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.4

* Sun Aug 18 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 1.4.26-2
- TCL bindings should require TCL

* Fri Aug 16 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 1.4.26-1
- Update to 1.4.26

* Fri Jul 26 2024 Miroslav Suchý <msuchy@redhat.com> - 1.4.23-5
- convert license to SPDX

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.4.23-3
- Rebuilt for Python 3.13

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jul 25 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 1.4.23-1
- Update 1.4.23

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 1.4.22-2
- Rebuilt for Python 3.12

* Thu May 18 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 1.4.22-1
- Update to 1.4.22

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Aug 02 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 1.4.20-1
- Update to 1.4.20

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.4.19-2
- Rebuilt for Python 3.11

* Tue Mar 29 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 1.4.19-1
- Update to 1.4.19

* Thu Jan 27 2022 Vít Ondruch <vondruch@redhat.com> - 1.4.18-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.1

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jun 26 2021 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.4.18-3
- Rebuild with C++ 11.1

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.4.18-2
- Rebuilt for Python 3.10

* Sun Mar 07 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 1.4.18-1
- Update to 1.4.18

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Sep 21 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 1.4.17-1
- Update to 1.4.17

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.4.14-4
- Rebuilt for Python 3.9

* Mon Feb 17 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 1.4.14-3
- Fix python3 conditioals so python3 bindings are built again

* Sun Feb 16 2020 Denis Arnaud <denis.arnaud_fedora@m4x.org> 1.4.14-2
- Dropped supprt for Python 2

* Mon Feb 10 2020 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.14-1
- Update to 1.4.14

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Nov 16 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.13-2
- Drop python2 bindings

* Thu Oct 17 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.13-1
- Update to 1.4.13

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.4.12-3
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Wed Aug 21 2019 Miro Hrončok <mhroncok@redhat.com> - 1.4.12-2
- Rebuilt for Python 3.8

* Tue Aug 20 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.12-1
- Update to 1.4.12

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.4.11-3
- Rebuilt for Python 3.8

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 16 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.11-1
- Update to 1.4.11

* Mon Feb 11 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.10-1
- Update to 1.4.10

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 19 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.9-1
- Update to 1.4.9

* Tue Aug 14 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.7-1
- Update to 1.4.7

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.6-2
- Re-enable py2 support on rawhide

* Tue Jul  3 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.6-1
- Update to 1.4.6
- Add py2/py3 conditionals, build just py3 on F-29+, py2/py3 on older Fedora

* Thu Jun 14 2018 Miro Hrončok <mhroncok@redhat.com> - 1.4.5-5
- Rebuilt for Python 3.7

* Fri Mar  9 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.5-4
- Add gcc BR

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.4.5-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Mon Jan 29 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.5-1
- Update to 1.4.5

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.4.4-6
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.4.4-5
- Python 2 binary package renamed to python2-xapian-bindings
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.4.4-2
- Rebuild due to bug in RPM (RHBZ #1468476)

* Tue May 16 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.4-1
- Update to 1.4.4

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Feb  4 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.3-1
- Update to 1.4.3

* Sat Jan 14 2017 Vít Ondruch <vondruch@redhat.com> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.4

* Thu Dec 22 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.1-1
- Update to 1.4.1
- Enable python3 bindings (rhbz #1282057)

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.23-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Jul  5 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.23-1
- Update to 1.2.23

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 14 2016 Vít Ondruch <vondruch@redhat.com> - 1.2.22-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.3

* Wed Jan  6 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.22-1
- Update to 1.2.22
- Use %%license

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 15 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.21-1
- Update to 1.2.21

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.2.20-2
- Rebuilt for GCC 5 C++11 ABI change

* Sat Mar 21 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.20-1
- Update to 1.2.20

* Tue Jan 20 2015 Vít Ondruch <vondruch@redhat.com> - 1.2.19-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Tue Nov 11 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.19-1
- Update to 1.2.19

* Mon Sep  1 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.18-2
- Set tcl version as macro rather than static

* Mon Sep  1 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.18-1
- Update to 1.2.18

* Wed Aug 20 2014 Kevin Fenzi <kevin@scrye.com> - 1.2.17-5
- Rebuild for rpm bug 1131892

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 29 2014 Vít Ondruch <vondruch@redhat.com> - 1.2.17-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Sat Feb 15 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.17-1
- Update to 1.2.17

* Sun Jan 12 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.16-1
- Update to 1.2.16

* Fri Aug 23 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.15-1
- Update to 1.2.15

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Mar 23 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.14-1
- Update to 1.2.14

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul  4 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.12-1
- Update to 1.2.12
- Drop php bindings due to license issue RHBZ #836112

* Sun Apr 29 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.9-1
- Update to 1.2.9

* Wed Feb 08 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.8-3
- Rebuilt for Ruby 1.9.3.

* Sun Jan 22 2012 Remi Collet <remi@fedoraproject.org> - 1.2.8-2
- build against PHP 5.4
- fix php ABI check
- extension not loadable, must be fixed
- add filter for private-shared-object-provides

* Sat Jan 21 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.8-1
- Update to 1.2.8

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 18 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.7-1
- Update to 1.2.7

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 16 2011 Peter Robinson<pbrobinson@fedoraproject.org> 1.2.4-1
- Update to new 1.2.4 release
- enable tcl and php bindings

* Mon Aug 30 2010 Peter Robinson<pbrobinson@fedoraproject.org> 1.2.3-1
- Update to new stable 1.2.3 release

* Sun Aug  1 2010 Peter Robinson<pbrobinson@fedoraproject.org> 1.2.2-3
- Bump build

* Fri Jul 23 2010 Peter Robinson<pbrobinson@fedoraproject.org> 1.2.2-2
- Bump build

* Fri Jul 23 2010 Peter Robinson<pbrobinson@fedoraproject.org> 1.2.2-1
- Update to new stable 1.2.2 release

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri May  7 2010 Peter Robinson<pbrobinson@fedoraproject.org> 1.2.0-2
- Add new dependencies

* Fri May  7 2010 Peter Robinson<pbrobinson@fedoraproject.org> 1.2.0-1
- Update to new stable 1.2.0 release

* Sun Mar 21 2010 Peter Robinson<pbrobinson@fedoraproject.org> 1.0.18-1
- Update to 1.0.18

* Sat Jan  9 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.17-3
- Updated to the new python sysarch spec file reqs

* Wed Dec  2 2009 Peter Robinson<pbrobinson@fedoraproject.org> 1.0.17-2
- Drop upstreamed patch

* Wed Dec  2 2009 Peter Robinson<pbrobinson@fedoraproject.org> 1.0.17-1
- Update to 1.0.17

* Sat Sep 19 2009 Peter Robinson<pbrobinson@fedoraproject.org> 1.0.16-1
- Update to 1.0.16, some spec file cleanups

* Sun Sep  6 2009 Peter Robinson<pbrobinson@fedoraproject.org> 1.0.15-2
- Patch to fix python bindings build

* Thu Aug 27 2009 Peter Robinson<pbrobinson@fedoraproject.org> 1.0.15-1
- Update to 1.0.15

* Wed Jul 29 2009 Peter Robinson<pbrobinson@fedoraproject.org> 1.0.14-1
- Update to 1.0.14

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun  5 2009 Peter Robinson<pbrobinson@fedoraproject.org> 1.0.13-1
- Update to 1.0.13

* Sun Apr 19 2009 Peter Robinson<pbrobinson@fedoraproject.org> 1.0.12-1
- Update to 1.0.12

* Tue Apr 07 2009 Peter Robinson<pbrobinson@fedoraproject.org> 1.0.11-2
- Obsolete pyxapian

* Mon Apr 06 2009 Peter Robinson<pbrobinson@fedoraproject.org> 1.0.11-1
- Update to 1.0.11

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> 1.0.9-2
- Rebuild for Python 2.6

* Sat Nov 29 2008 Adel Gadllah <adel.gadllah@gmail.com> 1.0.9-1
- Update to 1.0.9

* Sat Oct 11 2008 Adel Gadllah <adel.gadllah@gmail.com> 1.0.8-1
- Update to 1.0.8

* Mon Jul 28 2008 Adel Gadllah <adel.gadllah@gmail.com> 1.0.7-2
- Enable ruby bindings RH #456951, patch by Scott Seago

* Sun Jul 20 2008 Adel Gadllah <adel.gadllah@gmail.com> 1.0.7-1
- Update to 1.0.7

* Sun Mar 30 2008 Adel Gadllah <adel.gadllah@gmail.com> 1.0.6-1
- Update to 1.0.6

* Sat Feb 09 2008 Adel Gadllah <adel.gadllah@gmail.com> 1.0.5-2
- Rebuild for gcc-4.3

* Thu Dec 27 2007 Adel Gadllah <adel.gadllah@gmail.com> 1.0.5-1
- Update to 1.0.5

* Tue Oct 30 2007 Adel Gadllah <adel.gadllah@gmail.com> 1.0.4-1
- Update to 1.0.4

* Thu Aug 16 2007 Adel Gadllah <adel.gadllah@gmail.com> 1.0.2-4
- License is GPLv2+ not GPLv2

* Sun Aug 12 2007 Adel Gadllah <adel.gadllah@gmail.com> 1.0.2-3
- Remove vendor tag RH #251832

* Wed Aug 08 2007 Adel Gadllah <adel.gadllah@gmail.com> 1.0.2-2
- Fix license tag
- Minor cleanups
- Add disttag

* Fri Jul 13 2007 Marco Pesenti Gritti <mpg@redhat.com> - 1.0.2-1
- Update to 1.0.2

* Tue Jun 19 2007 Marco Pesenti Gritti <mpg@redhat.com> 1.0.1-2
- Remove req on xapian-bindings

* Mon Jun 18 2007 Marco Pesenti Gritti <mpg@redhat.com> 1.0.1-1
- Initial build
