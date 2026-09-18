# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from concurrent-ruby-1.0.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name concurrent-ruby

Name: rubygem-%{gem_name}
Version: 1.3.5
Release: 2%{?dist}
Summary: Modern concurrency tools for Ruby
License: MIT
URL: http://www.concurrent-ruby.com
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/ruby-concurrency/concurrent-ruby.git && cd concurrent-ruby
# git archive -v -o concurrent-ruby-1.3.5-specs.tar.gz v1.3.5 spec/
Source1: %{gem_name}-%{version}-specs.tar.gz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 1.9.3
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(timecop)
BuildArch: noarch

%description
Modern concurrency tools including agents, futures, promises, thread pools,
actors, supervisors, and more.

Inspired by Erlang, Clojure, Go, JavaScript, actors, and classic concurrency
patterns.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b 1

# Remove bundled .jar
%gemspec_remove_file 'lib/concurrent-ruby/concurrent/concurrent_ruby.jar'

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


%check
( cd .%{gem_instdir}
ln -s %{builddir}/spec spec

# We don't have the C extension and the condition is broken with 1.3.5
# https://github.com/ruby-concurrency/concurrent-ruby/issues/1080
sed -i 's/allow_c_extensions/c_extensions_loaded/' \
  spec/concurrent/atomic/atomic_{fixnum,reference,boolean}_spec.rb

# Exclude the -edge test cases.
#
# Require path must be exported due to
# spec/concurrent/executor/executor_service_shared.rb spawning new Ruby instance
RUBYOPT=-Ilib/concurrent-ruby rspec -rspec_helper \
  -fd \
  --exclude-pattern 'spec/concurrent/{actor_spec.rb,channel_spec.rb,lazy_register_spec.rb,channel/**/*,edge/**/*,processing_actor_spec.rb,promises_spec.rb,throttle_spec.rb,cancellation_spec.rb,executor/wrapping_executor_spec.rb}' \
  spec

)

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE.txt
# Containst just some Java sources. Very likely included by mistake.
%exclude %{gem_instdir}/ext
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jan 20 2025 Vít Ondruch <vondruch@redhat.com> - 1.3.5-1
- Update to Concurrent Ruby 1.3.5.
  Resolves: rhbz#2066526

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Feb 28 2022 Vít Ondruch <vondruch@redhat.com> - 1.1.9-1
- Update to Concurrent Ruby 1.1.9.
  Resolves: rhbz#1801443

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 16 2019 Vít Ondruch <vondruch@redhat.com> - 1.1.5-1
- Update to Concurrent Ruby 1.1.5.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 09 2017 Vít Ondruch <vondruch@redhat.com> - 1.0.5-1
- Update to Concurrent Ruby 1.0.5.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 03 2017 Vít Ondruch <vondruch@redhat.com> - 1.0.4-1
- Update to Concurrent Ruby 1.0.4.

* Mon Jul 04 2016 Vít Ondruch <vondruch@redhat.com> - 1.0.2-1
- Update to Concurrent Ruby 1.0.2.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 23 2015 Vít Ondruch <vondruch@redhat.com> - 1.0.0-1
- Initial package
