# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name activemodel

# Circular dependency with rubygem-railties.
%bcond_with bootstrap

Name: rubygem-%{gem_name}
Version: 8.0.2
Release: 3%{?dist}
Summary: A toolkit for building modeling frameworks (part of Rails)
License: MIT
URL: https://rubyonrails.org
Source0: https://rubygems.org/gems/%{gem_name}-%{version}%{?prerelease}.gem
# The gem doesn't ship with the test suite.
# git clone https://github.com/rails/rails.git && cd rails/activemodel
# git archive -v -o activemodel-8.0.2-tests.tar.gz v8.0.2 test/
Source1: %{gem_name}-%{version}%{?prerelease}-tests.tar.gz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 2.2.2
BuildRequires: rubygem(activesupport) = %{version}
%{!?with_bootstrap:BuildRequires: rubygem(railties) = %{version}}
BuildRequires: rubygem(bcrypt) => 3.1.2
BuildArch: noarch

%description
A toolkit for building modeling frameworks like Active Record. Rich support
for attributes, callbacks, validations, serialization, internationalization,
and testing.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b1

%build
gem build ../%{gem_name}-%{version}.gemspec
%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
( cd .%{gem_instdir}
cp -a %{builddir}/test .

mkdir ../tools
# Fake test_common.rb. It does not provide any functionality besides
# `force_skip` alias.
touch ../tools/test_common.rb
# Netiher strict_warnings.rb appears to be useful.
touch ../tools/strict_warnings.rb

%if %{with bootstrap}
# This depends on rubygem-railties.
mv ./test/cases/railtie_test.rb{,.disable}
%endif

# Run test in order, otherwise we get a lot of errors.
ruby -Ilib:test -e "Dir.glob('./test/**/*_test.rb').sort.each {|t| require t}"
)

%files
%dir %{gem_instdir}
%license %{gem_instdir}/MIT-LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.rdoc

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 04 2025 Vít Ondruch <vondruch@redhat.com> - 8.0.2-1
- Update to Active Model 8.0.2.
  Related: rhbz#2238177

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Nov 05 2024 Vít Ondruch <vondruch@redhat.com> - 7.0.8-5
- Fix Ruby 3.4 compatibility.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Sep 10 2023 Pavel Valena <pvalena@redhat.com> - 7.0.8-1
- Update to activemodel 7.0.8.

* Mon Aug 28 2023 Pavel Valena <pvalena@redhat.com> - 7.0.7.2-1
- Update to activemodel 7.0.7.2.

* Thu Aug 10 2023 Pavel Valena <pvalena@redhat.com> - 7.0.7-1
- Update to activemodel 7.0.7.

* Sun Jul 23 2023 Pavel Valena <pvalena@redhat.com> - 7.0.6-1
- Update to activemodel 7.0.6.

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 30 2023 Pavel Valena <pvalena@redhat.com> - 7.0.5-1
- Update to activemodel 7.0.5.

* Tue Mar 14 2023 Pavel Valena <pvalena@redhat.com> - 7.0.4.3-1
- Update to activemodel 7.0.4.3.

* Wed Jan 25 2023 Pavel Valena <pvalena@redhat.com> - 7.0.4.2-1
- Update to activemodel 7.0.4.2.

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Sep 15 2022 Pavel Valena <pvalena@redhat.com> - 7.0.4-1
- Update to activemodel 7.0.4.

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Mar 14 2022 Pavel Valena <pvalena@redhat.com> - 7.0.2.3-1
- Update to activemodel 7.0.2.3.

* Wed Feb 09 2022 Pavel Valena <pvalena@redhat.com> - 7.0.2-1
- Update to activemodel 7.0.2.

* Thu Feb 03 2022 Pavel Valena <pvalena@redhat.com> - 7.0.1-1
- Update to activemodel 7.0.1.

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Sep 17 2021 Pavel Valena <pvalena@redhat.com> - 6.1.4.1-1
- Update to activemodel 6.1.4.1.

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 30 2021 Pavel Valena <pvalena@redhat.com> - 6.1.4-1
- Update to activemodel 6.1.4.

* Tue May 18 2021 Pavel Valena <pvalena@redhat.com> - 6.1.3.2-1
- Update to activemodel 6.1.3.2.

* Fri Apr 09 2021 Pavel Valena <pvalena@redhat.com> - 6.1.3.1-1
- Update to activemodel 6.1.3.1.

* Thu Feb 18 2021 Pavel Valena <pvalena@redhat.com> - 6.1.3-1
- Update to activemodel 6.1.3.

* Mon Feb 15 2021 Pavel Valena <pvalena@redhat.com> - 6.1.2.1-1
- Update to activemodel 6.1.2.1.

* Wed Jan 27 2021 Pavel Valena <pvalena@redhat.com> - 6.1.1-1
- Update to activemodel 6.1.1.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct  8 10:54:54 CEST 2020 Pavel Valena <pvalena@redhat.com> - 6.0.3.4-1
- Update to activemodel 6.0.3.4.
  Resolves: rhbz#1877543

* Fri Sep 18 18:07:35 CEST 2020 Pavel Valena <pvalena@redhat.com> - 6.0.3.3-1
- Update to activemodel 6.0.3.3.
  Resolves: rhbz#1877543

* Mon Aug 17 04:49:08 GMT 2020 Pavel Valena <pvalena@redhat.com> - 6.0.3.2-1
- Update to activemodel 6.0.3.2.
  Resolves: rhbz#1742793

* Mon Aug 03 07:01:37 GMT 2020 Pavel Valena <pvalena@redhat.com> - 6.0.3.1-2
- Update to ActiveModel 6.0.3.1.
  Resolves: rhbz#1742793

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Mar 28 2019 Pavel Valena <pvalena@redhat.com> - 5.2.3-2
- Enable tests.

* Thu Mar 28 2019 Pavel Valena <pvalena@redhat.com> - 5.2.3-1
- Update to Active Model 5.2.3.

* Mon Mar 18 2019 Pavel Valena <pvalena@redhat.com> - 5.2.2.1-2
- Enable tests.

* Thu Mar 14 2019 Pavel Valena <pvalena@redhat.com> - 5.2.2.1-1
- Update to Active Model 5.2.2.1.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 05 2018 Pavel Valena <pvalena@redhat.com> - 5.2.2-2
- Update to Active Model 5.2.2.

* Thu Aug 09 2018 Pavel Valena <pvalena@redhat.com> - 5.2.1-2
- Enable tests.

* Wed Aug 08 2018 Pavel Valena <pvalena@redhat.com> - 5.2.1-1
- Update to Active Model 5.2.1.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 23 2018 Pavel Valena <pvalena@redhat.com> - 5.2.0-1
- Update to Active Model 5.2.0.

* Fri Feb 16 2018 Pavel Valena <pvalena@redhat.com> - 5.1.5-1
- Update to Active Model 5.1.5.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 11 2017 Pavel Valena <pvalena@redhat.com> - 5.1.4-1
- Update to Active Model 5.1.4.

* Tue Aug 08 2017 Pavel Valena <pvalena@redhat.com> - 5.1.3-1
- Update to Active Model 5.1.3.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 27 2017 Pavel Valena <pvalena@redhat.com> - 5.1.2-1
- Update to Active Model 5.1.2.

* Mon May 22 2017 Pavel Valena <pvalena@redhat.com> - 5.1.1-1
- Update to Active Model 5.1.1.

* Thu Mar 02 2017 Pavel Valena <pvalena@redhat.com> - 5.0.2-1
- Update to Active Model 5.0.2.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 02 2017 Pavel Valena <pvalena@redhat.com> - 5.0.1-1
- Update to Active Model 5.0.1.

* Mon Aug 15 2016 Pavel Valena <pvalena@redhat.com> - 5.0.0.1-1
- Update to Activemodel 5.0.0.1

* Mon Jul 04 2016 Vít Ondruch <vondruch@redhat.com> - 5.0.0-1
- Update to ActiveModel 5.0.0.

* Tue Mar 08 2016 Pavel Valena <pvalena@redhat.com> - 4.2.6-1
- Update to activemodel 4.2.6

* Wed Mar 02 2016 Pavel Valena <pvalena@redhat.com> - 4.2.5.2-1
- Update to activemodel 4.2.5.2

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Pavel Valena <pvalena@redhat.com> - 4.2.5.1-1
- Update to activemodel 4.2.5.1

* Wed Nov 18 2015 Pavel Valena <pvalena@redhat.com> - 4.2.5-1
- Update to activemodel 4.2.5

* Wed Aug 26 2015 Josef Stribny <jstribny@redhat.com> - 4.2.4-1
- Update to activemodel 4.2.4

* Tue Jun 30 2015 Josef Stribny <jstribny@redhat.com> - 4.2.3-1
- Update to activemodel 4.2.3

* Mon Jun 22 2015 Josef Stribny <jstribny@redhat.com> - 4.2.2-1
- Update to activemodel 4.2.2

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 20 2015 Josef Stribny <jstribny@redhat.com> - 4.2.1-2
- Fix: update tests

* Fri Mar 20 2015 Josef Stribny <jstribny@redhat.com> - 4.2.1-1
- Update to activemodel 4.2.1

* Mon Feb 09 2015 Josef Stribny <jstribny@redhat.com> - 4.2.0-1
- Update to activemodel 4.2.0

* Mon Aug 25 2014 Josef Stribny <jstribny@redhat.com> - 4.1.5-1
- Update to activemodel 4.1.5

* Fri Jul 04 2014 Josef Stribny <jstribny@redhat.com> - 4.1.4-1
- Update to activemodel 4.1.4
- Stabilize test suite

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 17 2014 Josef Stribny <jstribny@redhat.com> - 4.1.1-1
- Update to ActiveModel 4.1.1

* Thu Apr 17 2014 Josef Stribny <jstribny@redhat.com> - 4.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Fri Apr 11 2014 Josef Stribny <jstribny@redhat.com> - 4.1.0-1
- Update to ActiveModel 4.1.0

* Wed Feb 26 2014 Josef Stribny <jstribny@redhat.com> - 4.0.3-1
- Update to ActiveModel 4.0.3

* Thu Dec 05 2013 Josef Stribny <jstribny@redhat.com> - 4.0.2-1
- Update to ActiveModel 4.0.2
- Fix changelog

* Mon Nov 11 2013 Josef Stribny <jstribny@redhat.com> - 4.0.1-1
- Update to ActiveModel 4.0.1

* Tue Jul 30 2013 Josef Stribny <jstribny@redhat.com> - 4.0.0-1
- Update to ActiveModel 4.0.0.

* Tue Mar 19 2013 Vít Ondruch <vondruch@redhat.com> - 3.2.13-1
- Update to ActiveModel 3.2.13.

* Mon Mar 04 2013 Vít Ondruch <vondruch@redhat.com> - 3.2.12-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Tue Feb 12 2013 Vít Ondruch <vondruch@redhat.com> - 3.2.12-1
- Update to ActiveModel 3.2.12.

* Wed Jan 09 2013 Vít Ondruch <vondruch@redhat.com> - 3.2.11-1
- Update to ActiveModel 3.2.11.

* Thu Jan 03 2013 Vít Ondruch <vondruch@redhat.com> - 3.2.10-1
- Update to ActiveModel 3.2.10.

* Sat Oct 13 2012 Vít Ondruch <vondruch@redhat.com> - 3.2.8-3
- Fixed the Builder dependencies in .gemspec file.

* Sat Oct 13 2012 Vít Ondruch <vondruch@redhat.com> - 3.2.8-2
- Relaxed Builder dependnecy.

* Mon Aug 13 2012 Vít Ondruch <vondruch@redhat.com> - 3.2.8-1
- Update to ActiveModel 3.2.8.

* Mon Jul 30 2012 Vít Ondruch <vondruch@redhat.com> - 3.2.7-1
- Update to ActiveModel 3.2.7.

* Wed Jul 18 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 3.2.6-1
- Update to ActiveModel 3.2.6.
- Remove no longer needed I18n dependency.

* Fri Jun 15 2012 Vít Ondruch <vondruch@redhat.com> - 3.0.15-1
- Update to ActiveModel 3.0.15.

* Fri Jun 01 2012 Vít Ondruch <vondruch@redhat.com> - 3.0.13-1
- Update to ActiveModel 3.0.13.

* Tue Jan 24 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 3.0.11-1
- Rebuilt for Ruby 1.9.3.
- Update to ActiveModel 3.0.11.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 22 2011 Vít Ondruch <vondruch@redhat.com> - 3.0.10-1
- Update to ActiveModel 3.0.10

* Mon Jul 04 2011 Vít Ondruch <vondruch@redhat.com> - 3.0.9-1
- Update to ActiveModel 3.0.9

* Fri Mar 25 2011 Vít Ondruch <vondruch@redhat.com> - 3.0.5-1
- Update to ActiveModel 3.0.5

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb 03 2011 Vít Ondruch <vondruch@redhat.com> - 3.0.3-3
- Removed unnecessary clean section.

* Mon Jan 31 2011 Vít Ondruch <vondruch@redhat.com> - 3.0.3-2
- Added build dependencies.

* Tue Jan 25 2011 Vít Ondruch <vondruch@redhat.com> - 3.0.3-1
- Upgraded to activemodel 3.0.3
- Added documentation subpackage
- Added test execution during build
- Removed unnecessary cleanup from install section

* Tue Oct 26 2010 Jozef Zigmund <jzigmund@dhcp-29-238.brq.redhat.com> - 3.0.1-1
- Initial package
