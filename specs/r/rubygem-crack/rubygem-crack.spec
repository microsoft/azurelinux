# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name crack

Name: rubygem-%{gem_name}
Version: 1.0.0
Release: 4%{?dist}
Summary: Really simple JSON and XML parsing, ripped from Merb and Rails
License: MIT
URL: https://github.com/jnunemaker/crack
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/jnunemaker/crack.git && cd crack
# git archive -v -o crack-1.0.0-tests.tar.gz v1.0.0 test/
Source1: crack-%{version}-tests.tar.gz
# Fix REXML 3.4.3+ compatibility.
# https://github.com/jnunemaker/crack/pull/85
Patch0: rubygem-crack-1.0.1-Handle-new-No-root-element-error-from-REXML-84.patch
BuildRequires: rubygems-devel
BuildRequires: rubygem(bigdecimal)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(rexml)
BuildArch: noarch
#BZ 781829
Epoch: 1

%description
Really simple JSON and XML parsing, ripped from Merb and Rails.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{epoch}:%{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b 1

%patch 0 -p1

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
pushd .%{gem_instdir}
ln -s %{_builddir}/test test

ruby -Ilib:test -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/History
%doc %{gem_instdir}/README.md

%changelog
* Fri Oct 31 2025 Vít Ondruch <vondruch@redhat.com> - 1:1.0.0-4
- Fix REXML 3.4.3+ compatibility.

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Vít Ondruch <vondruch@redhat.com> - 1:1.0.0-1
- Update to crack 0.4.5.
  Resolves: rhbz#2261064

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 11 2022 Vít Ondruch <vondruch@redhat.com> - 1:0.4.5-5
- Fix Ruby 3.1 / Psych 4.0 compatibility.

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 08 2021 Vít Ondruch <vondruch@redhat.com> - 1:0.4.5-1
- Update to crack 0.4.5.
  Resolves: rhbz#1287909

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Apr 11 2016 Vít Ondruch <vondruch@redhat.com> - 1:0.4.2-4
- Explicitly set rubygem(bigdecimal) dependency.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jul 14 2014 Vít Ondruch <vondruch@redhat.com> - 1:0.4.2-1
- Update to crack 0.4.2.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Vít Ondruch <vondruch@redhat.com> - 1:0.3.2-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to crack 0.3.2.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 14 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1:0.3.1-3
- Properly require the main package (with epoch) from the -doc subpackage.

* Wed Mar 07 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1:0.3.1-2
- Update to 0.3.1

* Sun Feb 05 2012 <stahnma@fedoraproject.org> - 0.1.8-5
- Revert back to 0.1.8 as HTTParty can't use crack > 0.1.8

* Wed Dec 28 2011 <stahnma@fedoraproject.org> - 0.3.1-1
- Update to 0.3.1
- Fix bz #715704

* Thu Nov 10 2011 Michael Stahnke <mastahnke@gmail.com> - 0.1.8-3
- rebuilt

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 23 2010 Michael Stahnke <stahnma@fedoraproject.org> - 0.1.8-1
- Broke package into main and doc
- Added tests
