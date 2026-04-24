# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name cucumber

%bcond_with bootstrap

Name: rubygem-%{gem_name}
Version: 7.1.0
Release: 15%{?dist}
Summary: Tool to execute plain-text documents as functional tests
License: MIT
URL: https://cucumber.io/
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone --no-checkout https://github.com/cucumber/cucumber-ruby.git
# git -C cucumber-ruby archive -v -o rubygem-cucumber-7.1.0-spec.txz v7.1.0 spec/ cucumber.yml
Source1: %{name}-%{version}-spec.txz
# git clone --no-checkout https://github.com/cucumber/cucumber-ruby.git
# git -C cucumber-ruby archive -v -o rubygem-cucumber-7.1.0-features.txz v7.1.0 features/
Source2: %{name}-%{version}-features.txz
# Fix Ruby 3.4 compatibility due to `Hash.new` now accepting `:capacity`
# keyword option.
# https://github.com/cucumber/cucumber-ruby/pull/1757/commits/87a375822f0f1d76fa464423f9743e36c5036713
Patch0: rubygem-cucumber-9.2.0-Pass-hash-through-as-explicit-hash-to-avoid-unknown-keyword.patch
# Fix Ruby 3.4 backtrace formatting compatibility.
# https://github.com/cucumber/cucumber-ruby/pull/1771/commits/398eb7080936481b6b8c4921ff59aea7a8951883
Patch1: rubygem-cucumber-9.2.0-Fix-error-backtrace-formatting-on-Ruby-3-4.patch
# Fix Ruby 3.4 Hash#inspect compatibility.
# https://github.com/cucumber/cucumber-ruby/pull/1771/commits/b9065c96098b893c75fcbb41b7558332b3bfd23b
Patch2: rubygem-cucumber-9.2.0-CI-support-Ruby-3-4-Hash-inspect.patch
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
# Aruba has circular dependency with Cucumber.
%if %{without bootstrap}
BuildRequires: rubygem(aruba)
%endif
BuildRequires: rubygem(base64)
BuildRequires: rubygem(builder)
BuildRequires: rubygem(cucumber-core)
BuildRequires: rubygem(cucumber-wire)
BuildRequires: rubygem(cucumber-create-meta)
BuildRequires: rubygem(multi_test)
BuildRequires: rubygem(mime-types)
BuildRequires: rubygem(webrick)
BuildRequires: rubygem(nokogiri)
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(rake)
BuildArch: noarch

%description
Cucumber lets software development teams describe how software should behave
in plain text. The text is written in a business-readable domain-specific
language and serves as documentation, automated tests and development-aid.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b 1 -b 2

%patch 0 -p1
%patch 1 -p1

(
cd %{builddir}
%patch 2 -p1
)

# The rubygem-cucumber-html-formatter is currently not packaged in Fedora.
%gemspec_remove_dep -g cucumber-html-formatter

# Relax requires.
%gemspec_remove_dep -g diff-lcs "~> 1.4", ">= 1.4.4"
%gemspec_add_dep -g diff-lcs ">= 1.3"

%gemspec_remove_dep -g cucumber-gherkin "~> 22.0", ">= 22.0.0"
%gemspec_add_dep -g cucumber-gherkin ">= 20.0"

%gemspec_remove_dep -g cucumber-cucumber-expressions "~> 14.0", ">= 14.0.0"
%gemspec_add_dep -g cucumber-cucumber-expressions ">= 12.1"

%gemspec_remove_dep -g cucumber-messages "~> 17.1", ">= 17.1.1"
%gemspec_add_dep -g cucumber-messages ">= 17.0"

%gemspec_add_dep -g base64 ">= 0.2.0"

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
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
pushd .%{gem_instdir}
# Cucumber.yml is needed for both test suites.
# Used as fixture for rspec and options for cucumber.
ln -s %{_builddir}/cucumber.yml cucumber.yml

ln -s %{_builddir}/spec spec
# We don't need Pry.
sed -i '/require.*pry/ s/^/#/' spec/spec_helper.rb

rspec -Ilib spec

%if %{without bootstrap}
ln -s %{_builddir}/features features

# Skip the test that requires rubygem-cucumber-html-formatter,
# which is currently not packaged in Fedora.
sed -i -e '/^  Scenario: output html to stdout$/i @skip' \
    features/docs/formatters/html.feature

# Use RUBYOPT to make sure that the Cucumber from current directory has
# precedence over system Cucumber, which is pulled in as Aruba dependency.
RUBYOPT=-Ilib cucumber --tags 'not @skip'
%endif
popd

%files
%dir %{gem_instdir}
%{_bindir}/cucumber
%license %{gem_instdir}/LICENSE
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/CHANGELOG.md

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 03 2025 Vít Ondruch <vondruch@redhat.com> - 7.1.0-12
- Fix Ruby 3.4 backtrace and Hash#inspect formatting compatibility.

* Thu Nov 28 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 7.1.0-11
- Add base64 dependency explicitly for ruby34

* Fri Nov 01 2024 Vít Ondruch <vondruch@redhat.com> - 7.1.0-10
- Fix Ruby 3.4 compatibility due to `Hash.new` now accepting `:capacity`
  keyword option.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jan 30 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 7.1.0-3
- BR: rubygem(rake) due to recent rubygem(rspec-core) dependency change

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Oct 27 2021 Jarek Prokop <jprokop@redhat.com> - 7.1.0-1
- Update to cucumber 7.1.0.

* Mon Sep 06 2021 Pavel Valena <pvalena@redhat.com> - 7.0.0-1
- Update to cucumber 7.0.0.
  Resolves: rhbz#1842885

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-9
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb 27 2019 Vít Ondruch <vondruch@redhat.com> - 3.1.2-5
- Properly filter Ruby StdLib locations from backtrace.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Sep 14 2018 Vít Ondruch <vondruch@redhat.com> - 3.1.2-3
- Remove step argument test case to tix FTBFS.

* Fri Sep 07 2018 Vít Ondruch <vondruch@redhat.com> - 3.1.2-2
- Fix wire protocol.

* Thu Aug 23 2018 Jaroslav Prokop <jar.prokop@volny.cz> - 3.1.2-1
- Update to Cucumber 3.1.2.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 20 2017 Vít Ondruch <vondruch@redhat.com> - 2.4.0-1
- Update to Cucumber 2.4.0.

* Thu Nov 24 2016 Vít Ondruch <vondruch@redhat.com> - 2.3.3-2
- Fix FTBFS.

* Tue Apr 05 2016 Vít Ondruch <vondruch@redhat.com> - 2.3.3-1
- Update to Cucumber 2.3.3.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 16 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.18-1
- 1.3.18
  ref: https://github.com/cucumber/cucumber/issues/781

* Wed Jun 18 2014 Josef Stribny <jstribny@redhat.com> - 1.3.15-1
- Update to cucumber 1.3.15

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Feb 23 2013 Vít Ondruch <vondruch@redhat.com> - 1.2.1-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Drop useless build requires.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Mo Morsi <mmorsi@redhat.com> - 1.2.1-1
- Update cucumber to version 1.2.1

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 27 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 1.1.9-1
- Update cucumber to version 1.1.9

* Wed Feb 01 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.0.1-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 12 2011 Mo Morsi <mmorsi@redhat.com> - 1.0.1-1
- update to latest upstream release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Michal Fojtik <mfojtik@redhat.com> - 0.10.0-1
- Version bump

* Mon Sep 27 2010 Michal Fojtik <mfojtik@redhat.com> - 0.9.0-4
- Fixed JSON version again

* Fri Sep 24 2010 Michal Fojtik <mfojtik@redhat.com> - 0.9.0-3
- Fixed JSON version

* Fri Sep 24 2010 Michal Fojtik <mfojtik@redhat.com> - 0.9.0-2
- Fixed gherkin version in dependency list

* Fri Sep 24 2010 Michal Fojtik <mfojtik@redhat.com> - 0.9.0-1
- Version bump to match upstream
- Fixed dependency issue with new gherkin package

* Wed Aug 04 2010 Michal Fojtik <mfojtik@redhat.com> - 0.8.3-4
- Fixed JSON version

* Wed Aug 04 2010 Michal Fojtik <mfojtik@redhat.com> - 0.8.3-3
- Removed JSON patch (JSON updated in Fedora)

* Sun Aug 01 2010 Michal Fojtik <mfojtik@redhat.com> - 0.8.3-2
- Patched Rakefile and replaced rspec beta version dependency
- Patched Rakefile and downgraded JSON dependency

* Wed Jun 30 2010 Michal Fojtik <mfojtik@redhat.com> - 0.8.3-1
- Newer release

* Sun Oct 18 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.4.2-1
- Newer release

* Mon Oct 12 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.4.0-1
- Newer release

* Fri Jun 26 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.3.10-3
- Get rid of duplicate files (thanks to Mamoru Tasaka)

* Mon Jun 08 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.3.10-2
- Use geminstdir macro where appropriate
- Do not move examples around
- Depend on ruby(abi)
- Replace defines with globals

* Fri Jun 05 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.3.10-1
- Package generated by gem2rpm
- Move examples into documentation
- Remove empty files
- Fix up License
