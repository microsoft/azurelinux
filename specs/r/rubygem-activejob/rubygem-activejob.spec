# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from activejob-4.2.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name activejob

Name: rubygem-%{gem_name}
Version: 8.0.2
Release: 3%{?dist}
Summary: Job framework with pluggable queues
License: MIT
URL: https://rubyonrails.org
Source0: https://rubygems.org/gems/%{gem_name}-%{version}%{?prerelease}.gem
# git clone https://github.com/rails/rails.git && cd rails/activejob
# git archive -v -o activejob-8.0.2-tests.tar.gz v8.0.2 test/
Source1: %{gem_name}-%{version}%{?prerelease}-tests.tar.gz

BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 3.2.0
BuildRequires: rubygem(activesupport) = %{version}
BuildRequires: rubygem(globalid)
BuildRequires: rubygem(zeitwerk)
BuildRequires: tzdata
BuildArch: noarch

%description
Declare job classes that can be run by a variety of queuing backends.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}%{?prerelease} -b1

%build
gem build ../%{gem_name}-%{version}%{?prerelease}.gemspec
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

# We don't have isneakers in Fedora.
sed -i '/ActiveJob::QueueAdapters::SneakersAdapter/ d' test/cases/exceptions_test.rb

ADAPTERS='async inline test'
for ADAPTER in ${ADAPTERS}; do
  # Reject test cases similarly to what upstream does:
  # https://github.com/rails/rails/blob/ce359806416550c3b1b790c116aee5f0f9a182d4/activejob/Rakefile#L39-L42
  AJ_ADAPTER=${ADAPTER} ruby -Ilib:test -e '
    Dir.glob("./test/cases/**/*_test.rb").reject { |t|
      (t.include?("delayed_job") && ENV["AJ_ADAPTER"] != "delayed_job") ||
      (t.include?("async") && ENV["AJ_ADAPTER"] != "async")
    }.each { |t| require t }'

  # Do not execute integration tests, otherwise Rails's generators are required.
  # AJ_INTEGRATION_TESTS=1 AJ_ADAPTER=${ADAPTER} ruby -Ilib:test -e 'Dir.glob "./test/integration/**/*_test.rb", &method(:require)'
done
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
%doc %{gem_instdir}/README.md

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 04 2025 Vít Ondruch <vondruch@redhat.com> - 8.0.2-1
- Update to Action Job 8.0.2.
  Related: rhbz#2238177

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Nov 04 2024 Vít Ondruch <vondruch@redhat.com> - 7.0.8-5
- Fix compatibility with Ruby 3.4.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Sep 10 2023 Pavel Valena <pvalena@redhat.com> - 7.0.8-1
- Update to activejob 7.0.8.

* Mon Aug 28 2023 Pavel Valena <pvalena@redhat.com> - 7.0.7.2-1
- Update to activejob 7.0.7.2.

* Thu Aug 10 2023 Pavel Valena <pvalena@redhat.com> - 7.0.7-1
- Update to activejob 7.0.7.

* Sun Jul 23 2023 Pavel Valena <pvalena@redhat.com> - 7.0.6-1
- Update to activejob 7.0.6.

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 30 2023 Pavel Valena <pvalena@redhat.com> - 7.0.5-1
- Update to activejob 7.0.5.

* Tue Mar 14 2023 Pavel Valena <pvalena@redhat.com> - 7.0.4.3-1
- Update to activejob 7.0.4.3.

* Wed Jan 25 2023 Pavel Valena <pvalena@redhat.com> - 7.0.4.2-1
- Update to activejob 7.0.4.2.

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Sep 15 2022 Pavel Valena <pvalena@redhat.com> - 7.0.4-1
- Update to activejob 7.0.4.

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Mar 14 2022 Pavel Valena <pvalena@redhat.com> - 7.0.2.3-1
- Update to activejob 7.0.2.3.

* Wed Feb 09 2022 Pavel Valena <pvalena@redhat.com> - 7.0.2-1
- Update to activejob 7.0.2.

* Thu Feb 03 2022 Pavel Valena <pvalena@redhat.com> - 7.0.1-1
- Update to activejob 7.0.1.

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Sep 17 2021 Pavel Valena <pvalena@redhat.com> - 6.1.4.1-1
- Update to activejob 6.1.4.1.

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 30 2021 Pavel Valena <pvalena@redhat.com> - 6.1.4-1
- Update to activejob 6.1.4.

* Tue May 18 2021 Pavel Valena <pvalena@redhat.com> - 6.1.3.2-1
- Update to activejob 6.1.3.2.

* Fri Apr 09 2021 Pavel Valena <pvalena@redhat.com> - 6.1.3.1-1
- Update to activejob 6.1.3.1.

* Thu Feb 18 2021 Pavel Valena <pvalena@redhat.com> - 6.1.3-1
- Update to activejob 6.1.3.

* Mon Feb 15 2021 Pavel Valena <pvalena@redhat.com> - 6.1.2.1-1
- Update to activejob 6.1.2.1.

* Wed Jan 27 2021 Pavel Valena <pvalena@redhat.com> - 6.1.1-1
- Update to activejob 6.1.1.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct  8 10:51:00 CEST 2020 Pavel Valena <pvalena@redhat.com> - 6.0.3.4-1
- Update to activejob 6.0.3.4.
  Resolves: rhbz#1886135

* Fri Sep 18 18:03:51 CEST 2020 Pavel Valena <pvalena@redhat.com> - 6.0.3.3-1
- Update to activejob 6.0.3.3.
  Resolves: rhbz#1877504

* Mon Aug 17 04:45:46 GMT 2020 Pavel Valena <pvalena@redhat.com> - 6.0.3.2-1
- Update to activejob 6.0.3.2.
  Resolves: rhbz#1742792

* Mon Aug 03 07:01:37 GMT 2020 Pavel Valena <pvalena@redhat.com> - 6.0.3.1-1
- Update to ActiveJob 6.0.3.1.
  Resolves: rhbz#1742792

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Mar 28 2019 Pavel Valena <pvalena@redhat.com> - 5.2.3-1
- Update to Active Job 5.2.3.

* Thu Mar 14 2019 Pavel Valena <pvalena@redhat.com> - 5.2.2.1-1
- Update to Active Job 5.2.2.1.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 05 2018 Pavel Valena <pvalena@redhat.com> - 5.2.2-1
- Update to Active Job 5.2.2.

* Wed Aug 08 2018 Pavel Valena <pvalena@redhat.com> - 5.2.1-1
- Update to Active Job 5.2.1.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 23 2018 Pavel Valena <pvalena@redhat.com> - 5.2.0-1
- Update to Active Job 5.2.0.

* Fri Feb 16 2018 Pavel Valena <pvalena@redhat.com> - 5.1.5-1
- Update to Active Job 5.1.5.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 11 2017 Pavel Valena <pvalena@redhat.com> - 5.1.4-1
- Update to Active Job 5.1.4.

* Tue Aug 08 2017 Pavel Valena <pvalena@redhat.com> - 5.1.3-1
- Update to Active Job 5.1.3.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 27 2017 Pavel Valena <pvalena@redhat.com> - 5.1.2-1
- Update to Active Job 5.1.2.

* Mon May 22 2017 Pavel Valena <pvalena@redhat.com> - 5.1.1-1
- Update to Active Job 5.1.1.

* Thu Mar 02 2017 Pavel Valena <pvalena@redhat.com> - 5.0.2-1
- Update to Active Job 5.0.2.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 02 2017 Pavel Valena <pvalena@redhat.com> - 5.0.1-1
- Update to Active Job 5.0.1.
- Fix warnings: Fixnum and Bignum are deprecated in Ruby trunk

* Mon Aug 15 2016 Pavel Valena <pvalena@redhat.com> - 5.0.0.1-1
- Update to Activejob 5.0.0.1

* Fri Jul 08 2016 Jun Aruga <jaruga@redhat.com> - 5.0.0-1
- Update to activejob 5.0.0

* Tue Mar 08 2016 Pavel Valena <pvalena@redhat.com> - 4.2.6-1
- Update to activejob 4.2.6

* Wed Mar 02 2016 Pavel Valena <pvalena@redhat.com> - 4.2.5.2-1
- Update to activejob 4.2.5.2

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Pavel Valena <pvalena@redhat.com> - 4.2.5.1-1
- Update to activejob 4.2.5.1

* Wed Nov 18 2015 Pavel Valena <pvalena@redhat.com> - 4.2.5-1
- Update to activejob 4.2.5

* Wed Aug 26 2015 Josef Stribny <jstribny@redhat.com> - 4.2.4-1
- Update to activejob 4.2.4

* Tue Jun 30 2015 Josef Stribny <jstribny@redhat.com> - 4.2.3-1
- Update to activejob 4.2.3

* Mon Jun 22 2015 Josef Stribny <jstribny@redhat.com> - 4.2.2-1
- Update to activejob 4.2.2

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 20 2015 Josef Stribny <jstribny@redhat.com> - 4.2.1-1
- Update to activejob 4.2.1

* Thu Jan 22 2015 Vít Ondruch <vondruch@redhat.com> - 4.2.0-1
- Initial package
