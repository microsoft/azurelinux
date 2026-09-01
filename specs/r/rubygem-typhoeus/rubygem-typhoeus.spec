# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name typhoeus

Name: rubygem-%{gem_name}
Version: 1.4.0
Release: 15%{?dist}
Summary: Parallel HTTP library on top of libcurl multi
License: MIT
URL: https://github.com/typhoeus/typhoeus
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Fix Ruby 3.0 compatibility.
# https://github.com/typhoeus/typhoeus/pull/668
Patch0: typhoeus-1.4.0-Fix-Ruby-3-0-compatibility.patch
# Fix testsuite assertion with curl 8.9
# https://github.com/typhoeus/typhoeus/pull/724/
Patch1: typhoeus-1.4.0-support-curl-8_9-msg.patch
# Fix Rack 3 compatibility
# https://github.com/typhoeus/typhoeus/pull/731
Patch2: rubygem-typhoeus-1.4.1-Fix-Rack-3-compatibility.patch
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(dalli)
BuildRequires: rubygem(ethon) >= 0.7.0
BuildRequires: rubygem(faraday)
BuildRequires: rubygem(redis)
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(sinatra)
BuildRequires: rubygem(webrick)
# For Rack 3+ compatibility, where Rackup is split into separate rubygem-rackup
# package.
BuildRequires: %{_bindir}/rackup
BuildArch: noarch

%description
Like a modern code version of the mythical beast with 100 serpent heads,
Typhoeus runs HTTP requests in parallel while cleanly encapsulating handling
logic.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}

%patch 0 -p1
%patch 1 -p1
%patch 2 -p1

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

# Drop shebang.
sed -i -e '/^#!/d' %{buildroot}%{gem_instdir}/spec/support/server.rb


%check
pushd .%{gem_instdir}
# Don't use Bundler.
sed -i -e '/[bB]undler/ s/^/#/' spec/spec_helper.rb

rspec spec
popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/CONTRIBUTING.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Guardfile
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/UPGRADE.md
%{gem_instdir}/perf
%{gem_instdir}/spec
%{gem_instdir}/typhoeus.gemspec

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 18 2025 Vít Ondruch <vondruch@redhat.com> - 1.4.0-14
- Fix Rack 3 compatibility

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Aug 02 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.0-12
- Apply upstream PR to support curl 8.9 error message for test

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 14 17:55:07 CET 2021 Vít Ondruch <vondruch@redhat.com> - 1.4.0-3
- Fix FTBFS due to Ruby 3.0 incompatibility.

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 24 2020 Vít Ondruch <vondruch@redhat.com> - 1.4.0-1
- Update to Typhoeus 1.4.0.
  Resolves: rhbz#1833320

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Mar 01 2019 Vít Ondruch <vondruch@redhat.com> - 1.3.1-1
- Update to Typhoeus 1.3.1.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue May 17 2016 Jun Aruga <jaruga@redhat.com> - 1.0.2-1
- Update to Typhoeus 1.0.2.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jul 09 2015 Vít Ondruch <vondruch@redhat.com> - 0.7.2-1
- Update to Typhoeus 0.7.2.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Vít Ondruch <vondruch@redhat.com> - 0.6.8-1
- Update to Typhoeus 0.6.8.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 15 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.6.2-1
- Updated to 0.6.2 to satisfy new Webmock.

* Fri Mar 08 2013 Vít Ondruch <vondruch@redhat.com> - 0.3.3-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 01 2012 Vít Ondruch <vondruch@redhat.com> - 0.3.3-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 28 2011 Vít Ondruch <vondruch@redhat.com> - 0.3.3-1
- Updated to typhoeus 0.3.3.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 10 2011 Michal Fojtik <mfojtik@redhat.com> - 0.2.0-1
- Version bump

* Thu Oct 14 2010 Michal Fojtik <mfojtik@redhat.com> - 0.1.31-3
- Preserved failing test files (thx. to mtasaka)
- Fixed macros usage
- Replaced path with macro
- Removed libcurl from requires

* Wed Oct 13 2010 Michal Fojtik <mfojtik@redhat.com> - 0.1.31-2
- Fixed License to MIT
- Fixed libcurl BuildRequire
- Gem now recompiles with correct GCC flags
- Directory issues should be fixed
- Removed -devel subpackage
- Added tests


* Wed Oct 06 2010 Michal Fojtik <mfojtik@redhat.com> - 0.1.31-1
- Initial package
