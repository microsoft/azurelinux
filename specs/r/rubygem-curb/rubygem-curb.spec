# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from curb-0.7.7.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name curb

Name: rubygem-%{gem_name}
Version: 1.0.5
Release: 10%{?dist}
Summary: Ruby libcurl bindings
License: Ruby
URL: https://github.com/taf2/curb
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Make sure no external connectivity is needed to pass the test suite.
# https://github.com/taf2/curb/pull/448
Patch0: rubygem-curb-1.0.5-Use-TestServlet-url-instead-of-external-connectivity.patch
# Fix build with curl 8.7 and above
# https://github.com/taf2/curb/issues/451
# https://github.com/taf2/curb/pull/453
Patch1: rubygem-curb-1.0.5-fix-callback-function-read_data_handler.patch
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby-devel
BuildRequires: rubygem(test-unit)
BuildRequires: rubygem(webrick)
BuildRequires: libcurl-devel
# https://github.com/taf2/curb/blob/13144ec5d50ffea0460298cc5de8a0b33db78d22/tests/tc_curl_multi.rb#L42
BuildRequires: %{_sbindir}/ss
BuildRequires: gcc

%description
Curb (probably CUrl-RuBy or something) provides Ruby-language bindings for the
libcurl(3), a fully-featured client-side URL transfer library. cURL and
libcurl live at http://curl.haxx.se/.


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

%build
gem build ../%{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/{gem.build_complete,*.so} %{buildroot}%{gem_extdir_mri}/

# Prevent dangling symlink in -debuginfo (rhbz#878863).
rm -rf %{buildroot}%{gem_instdir}/ext/


%check
pushd .%{gem_instdir}
# Enable mistakenly disabled test case
# https://github.com/taf2/curb/issues/447
sed -i '/omit/ s/^/#/' tests/tc_curl_multi.rb

ruby -I$(dirs +1)%{gem_extdir_mri} -e 'Dir.glob "./tests/tc_*.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%{gem_extdir_mri}
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.markdown
%{gem_instdir}/Rakefile
%{gem_instdir}/doc.rb
%{gem_instdir}/tests

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 07 2025 Vít Ondruch <vondruch@redhat.com> - 1.0.5-7
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.4

* Wed Jul 24 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.5-6
- Apply upstram PR to build with curl 8.7+

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Vít Ondruch <vondruch@redhat.com> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.3

* Fri Dec 01 2023 Vít Ondruch <vondruch@redhat.com> - 1.0.5-1
- Update to curb 1.0.5.
  Resolves: rhbz#2156782

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 03 2023 Vít Ondruch <vondruch@redhat.com> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.2

* Sun Dec 25 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.1-2
- Use %%gem_extdir_mri due to ruby3.2 change
  for ext cleanup during build

* Mon Aug 08 2022 Vít Ondruch <vondruch@redhat.com> - 1.0.1-1
- Update to curb 1.0.1.
  Resolves: rhbz#2080496
  Resolves: rhbz#2113691

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 26 2022 Pavel Valena <pvalena@redhat.com> - 1.0.0-1
- Update to curb 1.0.0.
  Resolves: rhbz#2041001

* Wed Jan 26 2022 Vít Ondruch <vondruch@redhat.com> - 0.9.11-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.1

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan  6 2021 Vít Ondruch <vondruch@redhat.com> - 0.9.11-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.0

* Tue Nov 17 02:07:47 CET 2020 Pavel Valena <pvalena@redhat.com> - 0.9.11-1
- Update to curb 0.9.11.
  Resolves: rhbz#1893785

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 21 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.9.10-2
- Modify test suite for ruby27 a bit
- Rebuild against ruby27

* Wed Nov 13 2019 Steve Traylen <steve.traylen@cern.ch> - 0.9.10-1
- Update to curb 0.9.10.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 27 2019 Pavel Valena <pvalena@redhat.com> - 0.9.9-1
- Update to curb 0.9.9.

* Tue Mar 05 2019 Pavel Valena <pvalena@redhat.com> - 0.9.8-1
- Update to curb 0.9.8.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 17 2019 Vít Ondruch <vondruch@redhat.com> - 0.9.7-1
- Update to curb 0.9.7.

* Thu Jan 17 2019 Vít Ondruch <vondruch@redhat.com> - 0.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.6

* Sat Aug 11 2018 Vít Ondruch <vondruch@redhat.com> - 0.9.6-2
- Add missing BR: gcc to fix FTBFS (rhbz#1606181).

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 30 2018 Steve Traylen <steve.traylen@cern.ch> - 0.9.6-1
- Update to curb 0.9.6.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 0.9.4-3
- Rebuilt for switch to libxcrypt

* Thu Jan 04 2018 Vít Ondruch <vondruch@redhat.com> - 0.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.5

* Fri Nov 03 2017 Steve Traylen <steve.traylen@cern.ch> - 0.9.4-1
- Update to curb 0.9.4.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 10 2017 Vít Ondruch <vondruch@redhat.com> - 0.9.3-1
- Update to curb 0.9.3.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 07 2016 Vít Ondruch <vondruch@redhat.com> - 0.8.8-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.3

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 2 2015 Steve Traylen <steve.traylen@cern.ch> - 0.8.8-1
- Upstream 0.8.8

* Mon Mar 23 2015 Steve Traylen <steve.traylen@cern.ch> - 0.8.7-1
- Upstream 0.8.7

* Thu Jan 15 2015 Vít Ondruch <vondruch@redhat.com> - 0.8.6-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 4 2014 Steve Traylen <steve.traylen@cern.ch> - 0.8.6-1
- Upstream 0.8.6, update to new ruby guidelines.

* Tue Jun 17 2014 Vít Ondruch <vondruch@redhat.com> - 0.8.5-3
- Place extension into correct location.
- Prevent dangling symlinks in -debuginfo.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Steve Traylen <steve.traylen@cern.ch> - 0.8.5-1
- Update to 0.8.5, avoid minitest-5 for now.

* Wed Apr 9 2014 Steve Traylen <steve.traylen@cern.ch> - 0.8.4-2
- Now really works on EPEL6.

* Tue Mar 11 2014 Steve Traylen <steve.traylen@cern.ch> - 0.8.4-1
- Update to curb 0.8.4, fix to latest ruby guidelines.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 08 2013 Vít Ondruch <vondruch@redhat.com> - 0.8.3-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 20 2012 Vít Ondruch <vondruch@redhat.com> - 0.8.3-1
- Update to curb 0.8.3.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 01 2012 Vít Ondruch <vondruch@redhat.com> - 0.7.10-4
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Feb 25 2011 Shreyank Gupta <sgupta@redhat.com> - 0.7.10-2
- not excluding .require_paths

* Fri Feb 25 2011 Shreyank Gupta <sgupta@redhat.com> - 0.7.10-1
- New upstream 0.7.10

* Wed Jul 21 2010 Shreyank Gupta <sgupta@redhat.com> - 0.7.7.1-4
- Remove unneeded .require_paths file

* Tue Jul 20 2010 Shreyank Gupta <sgupta@redhat.com> - 0.7.7.1-3
- Remove unneeded .o and .so files from ext/ directory
- No rake test for ppc64

* Mon Jul 19 2010 Shreyank Gupta <sgupta@redhat.com> - 0.7.7.1-2
- Install gem file under %%gemdir and then copy to %%buildroot
- Moving .so to %%ruby_sitearch
- BuildRequires: rubygem(rake)

* Fri Jul 02 2010 Shreyank Gupta <sgupta@redhat.com> - 0.7.7.1-1
- Initial package
