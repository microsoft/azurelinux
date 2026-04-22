# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from tzinfo-0.3.26.gem by gem2rpm -*- rpm-spec -*-
%global gem_name tzinfo

Name: rubygem-%{gem_name}
Version: 2.0.6
Release: 7%{?dist}
Summary: Time Zone Library
License: MIT
URL: https://tzinfo.github.io
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Gem file does not contain a test suite, you can create it like so:
# git clone https://github.com/tzinfo/tzinfo.git --no-checkout
# cd tzinfo && git archive -v -o tzinfo-2.0.6-tests.txz v2.0.6 test/
Source1: %{gem_name}-%{version}-tests.txz
# tzdata might not be available on the system, but users still might prefer
# to use tzinfo-data gem (although it is not available in Fedora).
# https://fedoraproject.org/wiki/Changes/AllowRemovalOfTzdata
Recommends: tzdata
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(concurrent-ruby)
BuildArch: noarch

%description
TZInfo provides access to time zone data and allows times to be converted
using time zone rules.


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
pushd .%{gem_instdir}
ln -s %{_builddir}/test .

# We don't want to use bundler
sed -i "/raise 'Tests must be run with bundler/ s/^/#/" \
  test/test_utils.rb

export RUBYOPT="-Ilib"

ruby test/ts_all_ruby_format1.rb
ruby test/ts_all_ruby_format2.rb
ruby test/ts_all_zoneinfo.rb

# Test with system tzdata.
sed -i '/zoneinfo_path/ s|= .*|= "%{_datadir}/zoneinfo"|' test/ts_all_zoneinfo.rb

# The test is designed to run with internal zoneinfo fixtures, therefore there
# might be test failures.
# https://github.com/tzinfo/tzinfo/issues/141
ruby test/ts_all_zoneinfo.rb || :
popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.yardopts
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGES.md
%doc %{gem_instdir}/README.md

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 27 2023 Vít Ondruch <vondruch@redhat.com> - 2.0.6-1
- Add soft dependency on tzdata, which might not be available on the system.
- Update to TZInfo 2.0.6.
  Resolves: rhbz#2165247

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 22 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.5-2
- Fix include issue on test with ruby32

* Tue Sep 06 2022 Vít Ondruch <vondruch@redhat.com> - 2.0.5-1
- Update to TZInfo 2.0.5.
  Resolves: rhbz#2108737

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 31 2020 Pavel Valena <pavel.valena@email.com> - 2.0.4-1
- Update to tzinfo 2.0.4.
  Resolves: rhbz#1908521

* Fri Nov 13 00:58:17 CET 2020 Pavel Valena <pvalena@redhat.com> - 2.0.3-1
- Update to tzinfo 2.0.3.
  Resolves: rhbz#1895701

* Fri Oct 30 21:10:27 CET 2020 Pavel Valena <pvalena@redhat.com> - 2.0.2-1
- Update to tzinfo 2.0.2.
  Resolves: rhbz#1820389

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Feb 03 2020 Pavel Valena <pvalena@redhat.com> - 2.0.1-1
- Update to tzinfo 2.0.1.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon May 28 2018 Vít Ondruch <vondruch@redhat.com> - 1.2.5-1
- Update to TZInfo 1.2.5.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 25 2014 Josef Stribny <jstribny@redhat.com> - 1.2.2-1
- Update to 1.2.2

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 17 2014 Josef Stribny <jstribny@redhat.com> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1
- Patch tzinfo to use Minitest 5

* Thu Apr 10 2014 Josef Stribny <jstribny@redhat.com> - 1.1.0-1
- Update to tzinfo 1.1.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Josef Stribny <jstribny@redhat.com> - 0.3.37-1
- Update to tzinfo 0.3.37.

* Mon Feb 25 2013 Vít Ondruch <vondruch@redhat.com> - 0.3.35-1
- Update to tzinfo 0.3.35.

* Mon Feb 25 2013 Vít Ondruch <vondruch@redhat.com> - 0.3.34-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Vít Ondruch <vondruch@redhat.com> - 0.3.34-1
- Update to tzinfo 0.3.34.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.30-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 19 2012 Vít Ondruch <vondruch@redhat.com> - 0.3.30-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 06 2011 Vít Ondruch <vondruch@redhat.com> - 0.3.30-1
- Update to tzinfo 0.3.30.

* Sun Apr 10 2011  <Minnikhanov@gmail.com> - 0.3.26-1
- Updated mail to latest upstream release (v.0.3.26 2011-04-01)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011  <Minnikhanov@gmail.com> - 0.3.24-2
- Fix Comment 3 #668098. https://bugzilla.redhat.com/show_bug.cgi?id=668098#c3 

* Tue Jan 18 2011  <Minnikhanov@gmail.com> - 0.3.24-1
- Updated mail to latest upstream release

* Sat Jan 08 2011  <Minnikhanov@gmail.com> - 0.3.23-1
- Initial package

