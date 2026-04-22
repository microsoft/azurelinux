# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name httpclient

%global rubyabi 1.8

%if 0%{?rhel}
%bcond_with tests
%else
%bcond_without tests
%endif


Summary:        HTTP Client interface for ruby
Name:           rubygem-%{gem_name}
Version:        2.8.3
Release: 17%{?dist}
# httpclient is licensed under Ruby license from 2003 or later.
License:        Ruby
URL:            https://github.com/nahi/httpclient
Source0:        http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
Requires:       ruby(release)
BuildRequires:  rubygems-devel
%if %{with tests}
BuildRequires:  rubygem(mutex_m)
BuildRequires:  rubygem(test-unit)
BuildRequires:  rubygem(http-cookie)
BuildRequires:  rubygem(webrick)
%endif
BuildArch:      noarch

%description
an interface to HTTP Client for the ruby language

%package doc
Summary:   Documentation for %{name}
Requires:  %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
%setup -q -n  %{gem_name}-%{version}

%build
gem build ../%{gem_name}-%{version}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

# Remove backup and yardoc files
find %{buildroot}/%{gem_instdir} -type f -name "*~" -delete
rm -rf %{buildroot}%{gem_instdir}/.yardoc

# Fix anything executable that does not have a shebang
for file in `find %{buildroot}/%{gem_instdir} -type f -perm /a+x`; do
    [ -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 644 $file
done

# Find files with a shebang that do not have executable permissions
for file in `find %{buildroot}/%{gem_instdir} -type f ! -perm /a+x -name "*.rb"`; do
    [ ! -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 755 $file
done

# Find files that have non-standard-executable-perm
find %{buildroot}/%{gem_instdir} -type f -perm /g+wx -exec chmod -v g-w {} \;

# Find files that are not readable
find %{buildroot}/%{gem_instdir} -type f ! -perm /go+r -exec chmod -v go+r {} \;

%if %{with tests}
%check
pushd %{buildroot}%{gem_instdir}
# All the tests in test_auth.rb were being bypassed
#  but on Ruby 1.8, the bypass didn't work and would fail.
# Just remove the file since it was being bypassed anyway.
rm -f test/test_auth.rb
ruby -Ilib -e 'Dir.glob "./test/test_*.rb", &method(:require)' -- \
  --ignore-name /^test_post_async_with_default_internal$/ \
  --ignore-name /^test_timeout$/ \
  --ignore-name /^test_tcp_keepalive$/ \
  --ignore-name /^test_sync$/ \
  --ignore-name /^test_proxy_ssl$/ \
  --ignore-name /^test_cert_store$/ \
  --ignore-name /^test_verification_without_httpclient$/ \
  --ignore-name /^test_verification$/ \
  --ignore-name /^test_set_default_paths$/ \
  --ignore-name /^test_allow_tlsv1$/ \
  --ignore-name /^test_no_sslv3$/ \
  --ignore-name /^test_post_connection_check$/ \
  --ignore-name /^test_debug_dev$/ \
  --ignore-name /^test_ciphers$/ \
  --ignore-name /^test_redirect_see_other$/ \
  --ignore-name /^test_post_follow_redirect$/ \
  --ignore-name /^test_put$/ \
  --ignore-name /^test_post_empty$/ \
  --ignore-name /^test_post_content$/ \
popd
%endif

%files
%dir %{gem_instdir}
%{gem_instdir}/bin/
%{gem_instdir}/lib/
%doc %{gem_instdir}/sample
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/test


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Nov 20 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.8.3-14
- Add BR: rubygem(mutex_m) explicitly

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 2.8.3-13
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Feb 02 2021 Troy Dawson <tdawson@redhat.com> - 2.8.3-4
- Fix FTBFS (#1923647)
- Add rubygem-webrick as a BuildRequires

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Nov 20 2020 Troy Dawson <tdawson@redhat.com> - 2.8.3-2
- Make tests optional
- No tests for RHEL

* Wed Aug 05 2020 Troy Dawson <tdawson@redhat.com> - 2.8.3-1
- Update to 2.8.3

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Apr 29 2016 Troy Dawson <tdawson@redhat.com> - 2.8.0-1
- Update to 2.8.0

* Tue Feb 16 2016 Troy Dawson <tdawson@redhat.com> - 2.7.1-1
- Updated to 2.7.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 21 2015 Troy Dawson <tdawson@redhat.com> - 2.6.0.1-1
- Updated to 2.6.0.1

* Tue Jul 21 2015 Troy Dawson <tdawson@redhat.com> - 2.5.1-4
- Changed check from testrb2 to ruby

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Oct 20 2014 Troy Dawson <tdawson@redhat.com> - 2.5.1-2
- EPEL6 need rubygem-rdoc

* Mon Oct 20 2014 Troy Dawson <tdawson@redhat.com> - 2.5.1-1
- Update to 2.5.1 

* Mon Oct 20 2014 Troy Dawson <tdawson@redhat.com> - 2.4.0-3
- Update spec to follow latest guidelines

* Wed Oct 15 2014 Troy Dawson <tdawson@redhat.com> - 2.4.0-2
- Fix spec make it build and install on epel7 and older versions of fedora

* Fri Jun 13 2014 Troy Dawson <tdawson@redhat.com> - 2.4.0-1
- Update to latest upstream

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Jan 31 2014 Adam Miller <maxamillion@fedoraproject.org> - 2.3.4.1-1
- Update to latest upstream

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 13 2013 Troy Dawson <tdawson@redhat.com> - 2.3.2-6
- Fix to make it build/install on F19+

* Thu Feb 28 2013 Troy Dawson <tdawson@redhat.com> - 2.3.2-5
- Fix check to work on EPEL6

* Wed Feb 27 2013 Troy Dawson <tdawson@redhat.com> - 2.3.2-4
- Set License to (Ruby or BSD) and Public Domain

* Tue Feb 05 2013 Troy Dawson <tdawson@redhat.com> - 2.3.2-3
- Fix URL
- Removed line that changed /usr/bin/env to /usr/bin/ruby

* Mon Jan 21 2013 Troy Dawson <tdawson@redhat.com> - 2.3.2-2
- Add Check section
- Put docs in own rpm

* Mon Jan 07 2013 Troy Dawson <tdawson@redhat.com> - 2.3.2-1
- Update to 2.3.2
- Change spec to Fedora ruby standards

* Mon Sep 19 2011 Scott Henson <shenson@redhat.com> - 2.2.1-1
- Initial Packaging

