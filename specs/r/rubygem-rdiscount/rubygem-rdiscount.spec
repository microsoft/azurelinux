# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name rdiscount

Name: rubygem-%{gem_name}
Version: 2.2.7.1
Release: 9%{?dist}
Summary: Fast Implementation of Gruber's Markdown in C
License: BSD-3-Clause
URL: http://dafoster.net/projects/rdiscount/
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby-devel
BuildRequires: libmarkdown-devel
BuildRequires: rubygem(test-unit)
BuildRequires: gcc

%description
RDiscount converts documents in Markdown syntax to HTML.

It uses the excellent Discount processor by David Loren Parsons for this
purpose, and thereby inherits Discount's numerous useful extensions to the
Markdown language.

%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}

# Remove C and header files to unbundle discount-sources
find ext -type f \( -name "*.c" ! -name "rdiscount.c" -o -name "*.h" \) \
  -print -delete > discount_files

%gemspec_remove_file File.read("discount_files").lines(:chomp => true)

sed -i '/create_makefile/i $libs = "-lmarkdown"' ext/extconf.rb

%build
gem build ../%{gem_name}-%{version}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_mandir}/man7
mv %{buildroot}%{gem_instdir}/man/rdiscount.1 %{buildroot}%{_mandir}/man1
mv %{buildroot}%{gem_instdir}/man/markdown.7 %{buildroot}%{_mandir}/man7

# Copy C extensions to the extdir
mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/{gem.build_complete,*.so} %{buildroot}%{gem_extdir_mri}/

# Prevent dangling symlink in -debuginfo (rhbz#878863).
rm -rf %{buildroot}%{gem_instdir}/ext/

mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
pushd .%{gem_instdir}
ruby -I$(dirs +1)%{gem_extdir_mri} -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%{_bindir}/rdiscount
%{gem_extdir_mri}
%license %{gem_instdir}/COPYING
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%{_mandir}/man1/*
# These used to be duplicated by discount package, but they are not anymore.
# Keeping these exluded while trying to figure out what is going on.
# https://bugzilla.redhat.com/show_bug.cgi?id=2140278
%exclude %{_mandir}/man7/markdown.7.gz

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/BUILDING
%doc %{gem_instdir}/README.markdown
%{gem_instdir}/Rakefile
%{gem_instdir}/man
%{gem_instdir}/rdiscount.gemspec
%{gem_instdir}/test

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.7.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 07 2025 Vít Ondruch <vondruch@redhat.com> - 2.2.7.1-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.4

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Vít Ondruch <vondruch@redhat.com> - 2.2.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.3

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 29 2023 Vít Ondruch <vondruch@redhat.com> - 2.2.7.1-1
- Update to RDiscount 2.2.7.1
  Resolves: rhbz#2137386

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 03 2023 Vít Ondruch <vondruch@redhat.com> - 2.2.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.2

* Sun Dec 25 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.0.2-8
- Use %%gem_extdir_mri instead of ext for %%check due to ruby3.2 change
  for ext cleanup during build

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 26 2022 Vít Ondruch <vondruch@redhat.com> - 2.2.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.1

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan  6 2021 Vít Ondruch <vondruch@redhat.com> - 2.2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.0

* Wed Aug 12 2020 Gerd Pokorra <gp@zimt.uni-siegen.de> - 2.2.0.2-1
- Update to 2.2.0.2

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 17 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.0.1-7
- F-32: rebuild against ruby27

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 17 2019 Vít Ondruch <vondruch@redhat.com> - 2.2.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.6

* Mon Jul 23 2018 Gerd Pokorra <gp@zimt.uni-siegen.de> - 2.2.0.1-3
- Patch the testfile and get the tests running again

* Sat Jul 21 2018 Gerd Pokorra <gp@zimt.uni-siegen.de> - 2.2.0.1-2
- Generate the file discount_files

* Sat Jul 21 2018 Gerd Pokorra <gp@zimt.uni-siegen.de> - 2.2.0.1-1
- Update to 2.2.0.1
- Add gcc to BuildRequires

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 2.1.8-7
- Rebuilt for switch to libxcrypt

* Thu Jan 04 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.1.8-6
- F-28: rebuild for ruby25

* Mon Jul 31 2017 Gerd Pokorra <gp@zimt.uni-siegen.de> - 2.1.8-5
- quick workaround to fix the build problem

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 11 2017 Vít Ondruch <vondruch@redhat.com> - 2.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.4

* Wed May 18 2016 Gerd Pokorra <gp@zimt.uni-siegen.de> - 2.1.8-1
- Update to 2.1.8
- Change summary and description tag

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.7.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 11 2016 Vít Ondruch <vondruch@redhat.com> - 2.1.7.1-9
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.3

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.7.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 29 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.1.7.1-7
- Recent usage of %%gem_install to modify source
- Use system libmarkdown

* Thu Jan 29 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.1.7.1-6
- Simply use test-unit

* Fri Jan 16 2015 Vít Ondruch <vondruch@redhat.com> - 2.1.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 25 2014 Gerd Pokorra <gp@zimt.uni-siegen.de> - 2.1.7.1-2
- Rebuilt for Ruby_2.1

* Fri Apr 25 2014 Gerd Pokorra <gp@zimt.uni-siegen.de> - 2.1.7.1-1
- Update to 2.1.7.1

* Thu Apr 17 2014 Vít Ondruch <vondruch@redhat.com> - 2.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Thu Feb 20 2014 Gerd Pokorra <gp@zimt.uni-siegen.de> - 2.1.7-1
- Update to 2.1.7

* Wed May 22 2013 Gerd Pokorra <gp@zimt.uni-siegen.de> - 2.0.7.3-1
- Update to 2.0.7.3
- Exclude man-page /usr/share/man/man7/markdown.7.gz

* Mon Mar 18 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 2.0.7-5
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Mon Mar 18 2013 Gerd Pokorra <gp@zimt.uni-siegen.de> - 2.0.7-4
- Changed from ruby(abi) to ruby(release)
- Changed from macro gem_extdir to gem_extdir_mri

* Wed Feb 13 2013 Gerd Pokorra <gp@zimt.uni-siegen.de> - 2.0.7-3
- Changed back to ruby(abi)

* Thu Feb 07 2013 Gerd Pokorra <gp@zimt.uni-siegen.de> - 2.0.7-1
- Update to 2.0.7
- Add file BUIlDING

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 03 2012 Vít Ondruch <vondruch@redhat.com> - 1.6.3.2-7
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jun 12 2010 Gerd Pokorra <gp@zimt.uni-siegen.de> - 1.6.3.2-4
- removed the unused macro "ruby_sitelib"
- put the file rdiscount.gemspec to the doc-subpackage
- add dependency to the main package for the doc-subpackage

* Thu Jun 10 2010 Gerd Pokorra <gp@zimt.uni-siegen.de> - 1.6.3.2-3
- changed ruby(abi) dependency to be strict
- changed rubygem module related dependency style
- only arch-dependent files are in "ruby_sitearch"
- tests are now successful; "rake test:unit" is used
- "geminstdir" macro is used when possible
- "geminstdir" is owned by package
- ext/ subdirectory is removed form "buildroot" during install; no exclude

* Tue Jun 08 2010 Gerd Pokorra <gp@zimt.uni-siegen.de> - 1.6.3.2-2
- files under ext/ subdirectory excluded
- remove BuildRoot tag
- add "Requires: ruby(abi) >= 1.8"
- use global macro instead of define macro
- changed license tag

* Sun Jun 06 2010 Gerd Pokorra <gp@zimt.uni-siegen.de> - 1.6.3.2-1
- add "BuildRequires: ruby-devel"
- Initial package
