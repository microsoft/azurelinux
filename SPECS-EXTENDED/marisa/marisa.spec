Vendor:         Microsoft Corporation
Distribution:   Mariner

# disable python2 by default
%bcond_with python2

Name:          marisa
Version:       0.2.4
Release:       45%{?dist}
Summary:       Static and spece-efficient trie data structure library

License:       BSD or LGPLv2+
URL:  https://code.google.com/p/marisa-trie
# Currently the working URL is
# https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/marisa-trie/%%{name}-%%{version}.tar.gz
Source0: https://marisa-trie.googlecode.com/files/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires: swig
BuildRequires: perl-devel
BuildRequires: perl-generators
%if %{with python2}
BuildRequires: python2-devel
%endif
BuildRequires: python3-devel
BuildRequires: ruby-devel

%description
Matching Algorithm with Recursively Implemented StorAge (MARISA) is a
static and space-efficient trie data structure. And libmarisa is a C++
library to provide an implementation of MARISA. Also, the package of
libmarisa contains a set of command line tools for building and
operating a MARISA-based dictionary.

A MARISA-based dictionary supports not only lookup but also reverse
lookup, common prefix search and predictive search.


%package devel
Summary:       Development files for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package tools
Summary:       Tools for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description tools
The %{name}-tools package contains tools for developing applications
that use %{name}.


%package perl
Summary:       Perl language binding for marisa
Requires:      %{name} = %{version}-%{release}

%description perl
Perl language binding for marisa


%if %{with python2}
%package -n python2-%{name}
Summary:       Python language binding for marisa
Requires:      %{name} = %{version}-%{release}
# Remove before F30
Provides:      %{name}-python = %{version}-%{release}
Provides:      %{name}-python%{?_isa} = %{version}-%{release}
Obsoletes:     %{name}-python < %{version}-%{release}
%{?python_provide:%python_provide python2-%{name}}

%description -n python2-%{name}
Python 2 language binding for marisa
%endif


%package -n python3-%{name}
Summary:       Python 3 language binding for marisa
Requires:      %{name} = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}}

%description -n python3-%{name}
Python 3 language binding for marisa


%package ruby
Summary: Ruby language binding for marisa
Requires:      %{name} = %{version}-%{release}
Requires:      ruby(release)

%description ruby
Ruby language binding for groonga


%prep
%autosetup


%build
%set_build_flags

%configure --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

# build Perl bindings
pushd bindings/perl
%{__perl} Makefile.PL INC="-I%{_builddir}/%{name}-%{version}/lib" LIBS="-L%{_builddir}/%{name}-%{version}/lib/.libs -lmarisa" INSTALLDIRS=vendor
make %{?_smp_mflags}
popd

# build Python bindings
# Regenerate Python bindings
make --directory=bindings swig-python

pushd bindings/python
%if %{with python2}
%{__python2} setup.py build_ext --include-dirs="%{_builddir}/%{name}-%{version}/lib" --library-dirs="%{_builddir}/%{name}-%{version}/lib/.libs"
%py2_build
%endif

%{__python3} setup.py build_ext --include-dirs="%{_builddir}/%{name}-%{version}/lib" --library-dirs="%{_builddir}/%{name}-%{version}/lib/.libs"
%py3_build
popd

# build Ruby bindings
# Regenerate ruby bindings
pushd bindings
make swig-ruby
popd

pushd bindings/ruby
ruby extconf.rb --with-opt-include="%{_builddir}/%{name}-%{version}/lib" --with-opt-lib="%{_builddir}/%{name}-%{version}/lib/.libs" --vendor
make
popd

%install
%make_install INSTALL="install -p"

# install Perl bindings
pushd bindings/perl
%make_install INSTALL="install -p"
# Remove hidden files
rm -f %{buildroot}%{perl_vendorarch}/auto/marisa/.packlist
%{_fixperms} -c %{buildroot}%{perl_vendorarch}/*
popd

# install Python bindings
pushd bindings/python
%if %{with python2}
%py2_install
%endif
%py3_install
popd

# install Ruby bindings
pushd bindings/ruby
%make_install INSTALL="install -p"
popd

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name 'perllocal.pod' -exec rm -f {} ';'
rm -f $RPM_BUILD_ROOT%{perl_vendorarch}/sample.pl


%ldconfig_scriptlets


%files
%doc docs/style.css AUTHORS README docs/readme.en.html
%lang(ja) %doc docs/readme.ja.html
%license COPYING
%{_libdir}/libmarisa.so.*

%files devel
%{_includedir}/marisa*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files tools
%{_bindir}/marisa-benchmark
%{_bindir}/marisa-build
%{_bindir}/marisa-common-prefix-search
%{_bindir}/marisa-dump
%{_bindir}/marisa-lookup
%{_bindir}/marisa-predictive-search
%{_bindir}/marisa-reverse-lookup

%files perl
%{perl_vendorarch}/marisa.pm
%{perl_vendorarch}/auto/marisa

%if %{with python2}
%files -n python2-%{name}
%{python2_sitearch}/_marisa.so
%{python2_sitearch}/marisa.py*
%{python2_sitearch}/marisa-0.0.0-py2.?.egg-info
%endif

%files -n python3-%{name}
%{python3_sitearch}/__pycache__/marisa*
%{python3_sitearch}/_marisa*.so
%{python3_sitearch}/marisa.py
%{python3_sitearch}/marisa-0.0.0-py3.?.egg-info

%files ruby
%{ruby_vendorarchdir}/marisa.so

%changelog
* Mon Mar 15 2021 Henry Li <lihl@microsoft.com> - 0.2.4-45
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Fix distro condition checking

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 18 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.2.4-43
- F-32: rebuild against ruby27

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.2.4-42
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.2.4-41
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.2.4-39
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.2.4-37
- F-30: rebuild against ruby26

* Wed Aug 01 2018 Takao Fujiwara <fujiwara@redhat.com> - 0.2.4-36
- disable python2 for RHEL8

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 03 2018 Petr Pisar <ppisar@redhat.com> - 0.2.4-34
- Perl 5.28 rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.2.4-33
- Perl 5.28 rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.2.4-32
- Rebuilt for Python 3.7

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 0.2.4-30
- Rebuilt for switch to libxcrypt

* Fri Jan 05 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.2.4-29
- F-28: rebuild for ruby25

* Thu Dec 14 2017 Parag Nemade <pnemade AT redhat DOT com> - 0.2.4-28
- Few more cleanups to spec file

* Thu Dec 14 2017 Parag Nemade <pnemade AT redhat DOT com> - 0.2.4-27
- Correct the conditional builds for fedora and rhel
- Remove Group tag as its no longer needed
- added %%license macro for license files
- Correct the license tag
- Added fileslists more verbose for subpackages

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.2.4-26
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.2.4-25
- Python 2 binary package renamed to python2-marisa
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.2.4-22
- Perl 5.26 rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.2.4-20
- F-26: rebuild for ruby24

* Thu Dec 22 2016 Miro Hrončok <mhroncok@redhat.com> - 0.2.4-19
- Rebuild for Python 3.6

* Fri Nov 11 2016 Iryna Shcherbina <ishcherb@redhat.com> - 0.2.4-18
- Regenerate Python binding files with newer swig
- Provide Python 3 subpackage

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-17
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.2.4-16
- Perl 5.24 rebuild

* Mon May  9 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 0.2.4-15
- Fix packaging of marisa-perl (#1246698)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 12 2016 Vít Ondruch <vondruch@redhat.com> - 0.2.4-13
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.3

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.2.4-11
- Perl 5.22 rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.2.4-10
- Rebuilt for GCC 5 C++11 ABI change

* Fri Jan 16 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.2.4-9
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.2.4-8
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May  3 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.2.4-5
- Ruby: Rebuild for ruby 2.1 / rubygems 2.2
- Ruby: regenerate binding files with newer swig for -Werror=format-security
- Perl: don't use %%prefix/local, move installation directory to vendor directory

* Tue Aug 13 2013 Daiki Ueno <dueno@redhat.com> - 0.2.4-4
- disable workaround for ruby bindings needed for F19 (Closes:#992166)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.2.4-2
- Perl 5.18 rebuild

* Thu May  2 2013 Daiki Ueno <dueno@redhat.com> - 0.2.4-1
- new upstream release

* Wed Mar 20 2013 Vít Ondruch <vondruch@redhat.com> - 0.2.2-2
- Move Ruby bindings into correct location.

* Thu Mar 14 2013 Daiki Ueno <dueno@redhat.com> - 0.2.2-1
- new upstream release
- for Fedora 19 or later, use 'ruby(release)' instead of 'ruby(abi)',
  and also update the required Ruby ABI/release version to 2.0.0

* Thu Feb  7 2013 Daiki Ueno <dueno@redhat.com> - 0.2.1-3
- add perl, python, ruby bindings

* Fri Feb  1 2013 Daiki Ueno <dueno@redhat.com> - 0.2.1-2
- remove unnesseary BR
- don't embed rpath in executables
- add docs
- drop buildroot cleanup
- preserve timestamp when make install

* Thu Jan 24 2013 Daiki Ueno <dueno@redhat.com> - 0.2.1-1
- initial packaging
