# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from haml-2.2.14.gem by gem2rpm -*- rpm-spec -*-
%global gem_name haml

Name: rubygem-%{gem_name}
Version: 5.2.2
Release: 13%{?dist}
Summary: An elegant, structured (X)HTML/XML templating engine
License: MIT and WTFPL
URL: http://haml.info/
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone --no-checkout https://github.com/haml/haml.git
# git -C haml archive -v -o haml-5.2.2-tests.txz v5.2.2 test/
Source1: %{gem_name}-%{version}-tests.txz
# Explicitly include ostruct due to json 2.7.2 change
Patch0:  rubygem-haml-5.2.2-explicit-ostruct-dep.patch
# Support ruby3.4 Hash#inspect format change
# Note that haml 6.0 changes codebase a lot and
# the file modified in the patch no longer exists:
# https://github.com/haml/haml/commit/11bb81149f4b048fe9282ed9be0dd10bfbc710b2
Patch1:  rubygem-haml-5.2.2-ruby34-hash-inspect-formatting-change.patch
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(activemodel)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(railties)
BuildRequires: rubygem(temple)
BuildRequires: rubygem(tilt)
BuildArch: noarch

%description
Haml (HTML Abstraction Markup Language) is a layer on top of HTML or XML
that's designed to express the structure documents in a non-repetitive,
elegant, easy way by using indentation rather than closing
tags and allowing Ruby to be embedded with ease.
It was originally envisioned as a plugin for Ruby on Rails, but it can
function as a stand-alone templating engine.

%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b 1
(
cd %{_builddir}
%patch 0 -p1
%patch 1 -p1
)

%build
gem build ../%{gem_name}-%{version}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
pushd .%{gem_instdir}
# Link test suite into the place.
ln -s %{_builddir}/test .

# Get rid of Bundler.
sed -i '/[bB]undler/ s/^/#/' test/test_helper.rb

# We don't care about code coverage
sed -i '/[Ss]imple[Cc]ov/ s/^/#/g' test/test_helper.rb

# Disable test_annotated_template_names that's not working (removed in next release)
mv test/template_test.rb{,.disable}

# Avoid `ActionView::Template::Error: unknown keyword: :has_strict_locals`
# error in Rails 8, which intoduced this kwarg:
# https://github.com/rails/rails/commit/bbe7d19e11d1cd6374c667c38428c0c783bed3b5
# Just FTR, this file was dropped in more recent HAML:
# https://github.com/haml/haml/commit/11bb81149f4b048fe9282ed9be0dd10bfbc710b2#diff-2acf37380293c4739141a2f05134fa30a6d8f2716e5574a9598265fbf86a0854
sed -i '/def _run/ s/add_to_stack: true, &block/add_to_stack: true, has_strict_locals: false, \&block/' \
  test/helpers_for_rails_test.rb

# options_test.rb must be executed in isolation in order to prevent load
# order issues.
# https://github.com/haml/haml/issues/943
ruby -Ilib:test -e '(Dir.glob("./test/*_test.rb") - %w[./test/options_test.rb]).each {|f| require f }'
ruby -Ilib:test -e 'require "./test/options_test.rb"'
popd

%files
%dir %{gem_instdir}
%{_bindir}/haml
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/MIT-LICENSE
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_libdir}/haml/.gitattributes
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/FAQ.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/REFERENCE.md
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/TODO
%{gem_instdir}/benchmark.rb
%{gem_instdir}/haml.gemspec
%{gem_instdir}/yard
%exclude %{gem_instdir}/yard/default/.gitignore

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 23 2025 Vít Ondruch <vondruch@redhat.com> - 5.2.2-12
- Fix Ruby on Rails 8 compatibility.

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 06 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.2.2-10
- Support ruby34 Hash inspect formatting change for testsuite

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat May 04 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.2.2-8
- Explicitly include ostruct due to json 2.7.2 change

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Sep 17 2021 Pavel Valena <pvalena@redhat.com> - 5.2.2-1
- Update to haml 5.2.2.
  Resolves: rhbz#1710827

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 23 2018 Vít Ondruch <vondruch@redhat.com> - 5.0.4-1
- Update to Haml 5.0.4.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Vít Ondruch <vondruch@redhat.com> - 5.0.1-2
- options_test.rb must be executed in isolation.

* Tue Jul 18 2017 Vít Ondruch <vondruch@redhat.com> - 5.0.1-1
- Update to Haml 5.0.1.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Oct 13 2016 Vít Ondruch <vondruch@redhat.com> - 4.0.7-1
- Update to Haml 4.0.7.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 17 2014 Mo Morsi <mmorsi@redhat.com> - 4.0.5-4
- Remove old hpricot/ruby_parser (html2haml extracted to seperate gem)

* Thu Jun 12 2014 Mo Morsi <mmorsi@redhat.com> - 4.0.5-3
- Incorporate upstream patch + changes for minitest 5

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan 22 2014 Mo Morsi <mmorsi@redhat.com> - 4.0.5-1
- Update to version 4.0.5

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 12 2013 Vít Ondruch <vondruch@redhat.com> - 3.1.7-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Mo Morsi <mmorsi@redhat.com> - 3.1.7-1
- updated to latest upstream release

* Fri Jul 27 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 3.1.6-1
- Updated to Haml 3.1.6.
- Removed patch that is included in this upstream release.
- Introduced -doc subpackage.
- Simplified the test running.
- Adjusted Requires accordingly.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 01 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 3.1.2-5
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Mo Morsi <mmorsi@redhat.com> - 3.1.2-3
- remove fssm dependency as upstream project no longer bundles it
  (sass, which is vendored by haml upstream, still depends on it)

* Fri Jul 22 2011 Chris Lalancette <clalance@redhat.com> - 3.1.2-2
- Fix up the sass includes

* Mon Jul 11 2011 Mo Morsi <mmorsi@redhat.com> - 3.1.2-1
- updated to latest upstream release

* Tue Mar 29 2011 Mo Morsi <mmorsi@redhat.com> - 3.0.25-1
- updated to latest upstream release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Aug 26 2010 Matthew Kent <mkent@magoazul.com> - 3.0.17-1
- New upstream version.
- Include VERSION and VERSION_NAME in main package (#627454).
- Exclude vendored copy of fssm.

* Thu Aug 12 2010 Matthew Kent <mkent@magoazul.com> - 3.0.15-2
- New BR on rubygem-erubis and ruby_parser.

* Wed Jul 28 2010 Matthew Kent <mkent@magoazul.com> - 3.0.15-1
- New upstream version.
- New dependencies on yard/maruku.

* Tue May 4 2010 Matthew Kent <mkent@magoazul.com> - 2.2.24-1
- New upstream version - minor bugfixes and improvements.
- Drop unused sitelib macro.
- No backup files to cleanup now.

* Mon Jan 04 2010 Michal Babej <mbabej@redhat.com> - 2.2.20-1
- update to new upstream release

* Mon Jan 04 2010 Michal Babej <mbabej@redhat.com> - 2.2.16-1
- update to new upstream release
- get rid of test_files macro
- add shebang/permission handling from Jeroen van Meeuwen

* Fri Dec 04 2009 Michal Babej <mbabej@redhat.com> - 2.2.15-2
- change %%define to %%global
- change license to "MIT and WTFPL" (test/haml/spec/README.md)
- add Requires on hpricot for html2haml
- change %%gem_dir to %%gem_instdir where appropriate

* Wed Dec 02 2009 Michal Babej <mbabej@redhat.com> - 2.2.15-1
- Update to new upstream release
- URL changed by upstream

* Wed Dec 02 2009 Michal Babej <mbabej@redhat.com> - 2.2.14-1
- Initial package
