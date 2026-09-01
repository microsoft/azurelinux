# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name tilt

# When we are bootstrapping, we drop some dependencies, and/or build time tests.
%bcond_with bootstrap

Name: rubygem-%{gem_name}
Version: 2.2.0
Release: 5%{?dist}
Summary: Generic interface to multiple Ruby template engines
License: MIT
URL: https://github.com/jeremyevans/tilt
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Man pages were dropped by upstream :'(
# https://github.com/jeremyevans/tilt/issues/7
## git clone https://github.com/jeremyevans/tilt.git && cd tilt
## git archive -v -o tilt-2.2.0-man.tar.gz v2.2.0 man/
#Source1: %%{gem_name}-%%{version}-man.tar.gz

# git clone https://github.com/jeremyevans/tilt.git && cd tilt
# git archive -v -o tilt-2.2.0-test.tar.gz v2.2.0 test/
Source2: %{gem_name}-%{version}-test.tar.gz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
# These templating engines are removed or deprecated in Fedora.
# BuildRequires: rubygem(coffee-script)
# BuildRequires: rubygem(erubis)
# BuildRequires: rubygem(maruku)
# BuildRequires: rubygem(wikicloth)
BuildRequires: rubygem(creole)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(nokogiri)
BuildRequires: rubygem(erubi)
BuildRequires: rubygem(builder)
BuildRequires: rubygem(RedCloth)
BuildRequires: rubygem(redcarpet)
BuildRequires: rubygem(kramdown)
BuildRequires: rubygem(rdiscount)
BuildRequires: rubygem(liquid)
BuildRequires: rubygem(sassc)
BuildRequires: rubygem(asciidoctor)
BuildRequires: rubygem(prawn)
BuildRequires: rubygem(pdf-reader)
%if %{without bootstrap}
BuildRequires: rubygem(haml)
BuildRequires: rubygem(slim)
%endif
## To generate man pages.
#BuildRequires: /usr/bin/ronn
BuildArch: noarch

%description
Generic interface to multiple Ruby template engines.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b 2

%build
# Create the gem as gem install only works on a gem file
gem build ../%{gem_name}-%{version}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

# Fix shebang.
sed -i -e 's|/usr/bin/env ruby|/usr/bin/ruby|' %{buildroot}%{gem_instdir}/bin/tilt

## Generate man pages.
#pushd %{_builddir}
#  ronn --manual="Tilt Manual" --organization="Tilt %{version}" -r man/*.ronn
#
#  mkdir -p %{buildroot}%{_mandir}/man1
#  mv man/*.1 %{buildroot}%{_mandir}/man1
#popd

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%if %{without bootstrap}
%check
pushd .%{gem_instdir}
cp -a %{_builddir}/test test

LANG=C.UTF-8 ruby -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd
%endif

%files
%dir %{gem_instdir}
%{_bindir}/tilt
%license %{gem_instdir}/COPYING
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
#%%doc %%{_mandir}/man1/*

%files doc
%doc %{gem_docdir}


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Aug 22 2023 Vít Ondruch <vondruch@redhat.com> - 2.2.0-1
- Update to Tilt 2.2.0.
  Resolves: rhbz#2170954

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Vít Ondruch <vondruch@redhat.com> - 2.0.11-1
- Update to Tilt 2.0.11.
  Resolves: rhbz#2110035

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed May 19 2021 Pavel Valena <pvalena@redhat.com> - 2.0.10-5
- Remove maruku gem integration, as it is orphaned in Fedora.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 18 2021 Vít Ondruch <vondruch@redhat.com> - 2.0.10-3
- Fix Ruby 3.0 compatibility.

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Apr 30 2020 Vít Ondruch <vondruch@redhat.com> - 2.0.10-1
- Update to tilt 2.0.10.
  Resolves: rhbz#1754628

* Thu Apr 30 2020 Vít Ondruch <vondruch@redhat.com> - 2.0.8-8
- Fix FTBFS due to updated AsciiDoctor.
  Resovles: rhbz#1800040

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.0.8-4
- Use C.UTF-8 locale
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Aug 07 2017 František Dvořák <valtri@civ.zcu.cz> - 2.0.8-1
- Update to 2.0.8 (#1474335)
- Improve bootstrap macro logic (#1460283)
- Fix script interpreter

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Apr 26 2017 František Dvořák <valtri@civ.zcu.cz> - 2.0.7-1
- Update to tilt 2.0.7.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Sep 19 2016 Greg Hellings <greg.hellings@gmail.com> - 2.0.5-1
- New upstream version 2.0.5

* Wed Jun 01 2016 Greg Hellings <greg.hellings@gmail.com> - 2.0.4-1
- Update to tilt 2.0.4.

* Fri May 13 2016 Vít Ondruch <vondruch@redhat.com> - 2.0.3-1
- Update to tilt 2.0.3.
- Use NodeJS for build instead of therubyracer.
- Add man pages.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Sep 15 2015 Vít Ondruch <vondruch@redhat.com> - 2.0.1-1
- Update to tilt 2.0.1.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jan 21 2015 Vít Ondruch <vondruch@redhat.com> - 1.4.1-2
- Make the test suite MiniTest 5.x compatible to fix the FTBFS.

* Thu Jun 19 2014 Vít Ondruch <vondruch@redhat.com> - 1.4.1-1
- Update to tilt 1.4.1.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 15 2013 Vít Ondruch <vondruch@redhat.com> - 1.3.7-2
- Enable test suite.

* Mon Apr 15 2013 Vít Ondruch <vondruch@redhat.com> - 1.3.7-1
- Update to tilt 1.3.7.

* Mon Apr 15 2013 Vít Ondruch <vondruch@redhat.com> - 1.3.5-2
- Fix unowned directory (rhbz#912046).

* Thu Mar 07 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3.5-1
- Updated to Tilt 1.3.5.
- Remove patches merged upstream.

* Thu Feb 28 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3.3-7
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jul 23 2012 Vít Ondruch <vondruch@redhat.com> - 1.3.3-5
- Fixes RDoc >= 3.10 compatibility.
- Enabled coffee-script and redcarpet tests.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 03 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3.3-3
- Allowed running the tests.

* Tue Jan 24 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3.3-2
- Rebuilt for Ruby 1.9.3.
- Introduced %%bootstrap macro to deal with dependency loop for BuildRequires.

* Mon Jan 16 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3.3-1
- Updated to tilt 1.3.3.
- Removed patch that fixed BZ #715713, as it is a part of this version.
- Excluded unnecessary files.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Vít Ondruch <vondruch@redhat.com> - 1.3.2-1
- Updated to the tilt 1.3.2.
- Test suite for erubis, haml, builder and RedCloth template engines enabled.

* Fri Jun 24 2011 Vít Ondruch <vondruch@redhat.com> - 1.2.2-3
- Fixes FTBFS (rhbz#715713).

* Thu Feb 10 2011 Vít Ondruch <vondruch@redhat.com> - 1.2.2-2
- Test moved to doc subpackage
- %%{gem_name} macro used whenever possible.

* Mon Feb 07 2011 Vít Ondruch <vondruch@redhat.com> - 1.2.2-1
- Initial package
