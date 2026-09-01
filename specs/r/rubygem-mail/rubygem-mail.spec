# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from mail-2.3.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name mail

Name: rubygem-%{gem_name}
Version: 2.8.1
Release: 6%{?dist}
Summary: Mail provides a nice Ruby DSL for making, sending and reading emails
License: MIT
URL: https://github.com/mikel/mail
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Specs are not shipped with the gem. You can get them like so:
# git clone https://github.com/mikel/mail.git --no-checkout
# cd mail && git archive -v -o mail-2.8.1-specs.txz 2.8.1 spec/
Source1: %{gem_name}-%{version}-specs.txz
BuildRequires: rubygem(net-smtp)
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(mini_mime)
BuildRequires: rubygem(rspec)
BuildArch: noarch

%description
A really Ruby Mail handler.

%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b1

%gemspec_add_file 'lib/mail/yaml.rb'

%build
gem build ../%{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
ln -s %{_builddir}/spec .

# We don't want benchmarks
sed -i -e '/require..rspec.benchmark/ s/^/#/' \
       -e '/include.RSpec..Benchmark/ s/^/#/' \
  spec/spec_helper.rb

rspec spec
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/MIT-LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Sep 21 2023 Pavel Valena <pvalena@redhat.com> - 2.8.1-1
- Update to mail 2.8.1.
  Resolves: rhbz#2150476

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Mar 23 2022 Vít Ondruch <vondruch@redhat.com> - 2.7.1-6
- Add `rubygem(net-snmp)` dependency for Ruby 3.1 compatibility.
- Fix Psych 4.0+ compatibility.

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 08 2020 Pavel Valena <pvalena@redhat.com> - 2.7.1-1
- Update to mail 2.7.1.
  Resolves: rhbz#1446187

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 23 2017 Vít Ondruch <vondruch@redhat.com> - 2.6.4-2
- Fix Ruby 2.4 deprecation warnings.

* Thu Jun 30 2016 Vít Ondruch <vondruch@redhat.com> - 2.6.4-1
- Update to Mail 2.6.4.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 18 2015 Vít Ondruch <vondruch@redhat.com> - 2.6.3-1
- Update to Mail 2.6.3.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 15 2013 Vít Ondruch <vondruch@redhat.com> - 2.5.4-1
- Update to mail 2.5.4.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 19 2013 Vít Ondruch <vondruch@redhat.com> - 2.5.3-1
- Update to Mail 2.5.3.

* Tue Mar 05 2013 Vít Ondruch <vondruch@redhat.com> - 2.4.4-4
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 09 2012 Vít Ondruch <vondruch@redhat.com> - 2.4.4-1
- Update to Mail 2.4.4.

* Tue Jan 31 2012 Vít Ondruch <vondruch@redhat.com> - 2.3.0-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed May 04 2011  <Minnikhanov@gmail.com> - 2.3.0-1
- Updated mail to latest upstream release (v.2.3.0 2011-04-27)
- Test excluded. May be need Zentest >= 4.4.0 and rubygem(rcov).

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011  <Minnikhanov@gmail.com> - 2.2.15-2
- Fix Comment 18 #665560. https://bugzilla.redhat.com/show_bug.cgi?id=665560#c18 
- Remove create Gemfile.lock at prep-section.

* Sat Jan 29 2011  <Minnikhanov@gmail.com> - 2.2.15-1
- Updated mail to latest upstream release (v.2.2.15 2011-01-25)

* Thu Jan 27 2011  <Minnikhanov@gmail.com> - 2.2.14-5
- Fix Comment 14 #665560. https://bugzilla.redhat.com/show_bug.cgi?id=665560#c14 

* Mon Jan 24 2011  <Minnikhanov@gmail.com> - 2.2.14-4
- Fix Comment 12 #665560. https://bugzilla.redhat.com/show_bug.cgi?id=665560#c12 

* Sun Jan 23 2011  <Minnikhanov@gmail.com> - 2.2.14-3
- 'BuildRequires:' correct wrong tag 'BuildRequires(check):'. 

* Sat Jan 22 2011  <Minnikhanov@gmail.com> - 2.2.14-2
- Fix Comment 6 #665560. https://bugzilla.redhat.com/show_bug.cgi?id=665560#c6 

* Thu Jan 13 2011  <Minnikhanov@gmail.com> - 2.2.14-1
- Updated mail to latest upstream release

* Fri Dec 24 2010  <Minnikhanov@gmail.com> - 2.2.13-1
- Initial package

