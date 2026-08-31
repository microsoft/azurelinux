# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name eventmachine

# This enables to run full test suite, where network connection is available.
# However, it must be disabled for Koji build.
%{!?network: %global network 0}

Name: rubygem-%{gem_name}
Version: 1.2.7
Release: 30%{?dist}
Summary: Ruby/EventMachine library
# Automatically converted from old format: GPLv2 or Ruby - review is highly recommended.
License: GPL-2.0-only OR Ruby
URL: http://rubyeventmachine.com
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Fix compatibility with OpenSSL 1.1.1.
# https://github.com/eventmachine/eventmachine/pull/789
Patch0: rubygem-eventmachine-1.2.7-OpenSSL-1.1.0-test-updates.patch
# https://github.com/eventmachine/eventmachine/pull/867/commits/0904385936ef4ecae4519f4f7b8f829a3608afcd
Patch1: rubygem-eventmachine-1.2.7-Update-runtime-files-for-TLS13-no-SSL-OpenSSL-lib-info.patch
# https://github.com/eventmachine/eventmachine/pull/867/commits/fc95df7a31ae5694f6a762c0c3d4f5c79c3ee40b
Patch2: rubygem-eventmachine-1.2.7-Move-console-SSL-Info-code-to-em_test_helper.patch
# https://github.com/eventmachine/eventmachine/pull/867/commits/dd6cec8d5278e11f2a1752aa7b4a712d53b1f1d3
Patch3: rubygem-eventmachine-1.2.7-Openssl-1.1.1-updates.patch
# Extend certificate length.
# https://github.com/eventmachine/eventmachine/pull/923
Patch4: rubygem-eventmachine-1.2.7-Increase-certificate-length.patch
# Fix `test_case_insensitivity(TestSslProtocols)` test case.
# This small change is part of big upstream commit:
# https://github.com/eventmachine/eventmachine/pull/868/commits/a7da18ed78a60f25162c944f497154f7769f08f0
Patch5: rubygem-eventmachine-1.2.7-Bump-TLS-version.patch
# Fix intermittent tests.
# https://github.com/eventmachine/eventmachine/pull/870
Patch6: rubygem-eventmachine-1.2.7-Fix-intermittent-tests.patch
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby-devel
# Compiler is required for build of gem binary extension.
# https://fedoraproject.org/wiki/Packaging:C_and_C++#BuildRequires_and_Requires
BuildRequires: gcc-c++
# Enables SSL support.
BuildRequires: openssl-devel
BuildRequires: rubygem(test-unit)

%description
EventMachine implements a fast, single-threaded engine for arbitrary network
communications. It's extremely easy to use in Ruby. EventMachine wraps all
interactions with IP sockets, allowing programs to concentrate on the
implementation of network protocols. It can be used to create both network
servers and clients. To create a server or client, a Ruby program only needs
to specify the IP address and port, and provide a Module that implements the
communications protocol. Implementations of several standard network protocols
are provided with the package, primarily to serve as examples. The real goal
of EventMachine is to enable programs to easily interface with other programs
using TCP/IP, especially if custom protocols are required.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}

# Make the package compliant with Fedora's crypto policies.
# https://fedoraproject.org/wiki/Packaging:CryptoPolicies
sed -i '/SSL_CTX_set_cipher_list/ s/".*"/"PROFILE=SYSTEM"/' ext/ssl.cpp

%patch 0 -p1
%patch 1 -p1
%patch 2 -p1
%patch 3 -p1
%patch 4 -p1
%patch 5 -p1
%patch 6 -p1

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

mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/{gem.build_complete,*.so} %{buildroot}%{gem_extdir_mri}/

# Prevent dangling symlink in -debuginfo (rhbz#878863).
rm -rf %{buildroot}%{gem_instdir}/ext/

%check
pushd .%{gem_instdir}

ruby -Ilib:$(dirs +1)%{gem_extdir_mri}:tests -e "Dir.glob './tests/**/test_*.rb', &method(:require)" -- \
  --verbose \
  --ignore-name /^test_.*v3.*$/ \
  --ignore-name /^test_no_ecdh_curve$/ \
  --ignore-name=/^test_cookie$/ \
  --ignore-name=/^test_http_client$/ \
  --ignore-name=/^test_http_client_1$/ \
  --ignore-name=/^test_http_client_2$/ \
  --ignore-name=/^test_version_1_0$/ \
  --ignore-name=/^test_https_get$/ \
  --ignore-name=/^test_get$/ \
  --ignore-name=/^test_get_pipeline$/ \
  --ignore-name=/^test_ipv6_udp_local_server$/ \
  `# Ruby 3.0 related test failure` \
  `# https://github.com/eventmachine/eventmachine/issues/941` \
  --ignore-name=/^test_em_system_pid$/ \
%if 0%{network} < 1
  --ignore-name=/^test_a$/ \
  --ignore-name=/^test_a_pair$/ \
  --ignore-name=/^test_bad_host$/ \
  --ignore-name=/^test_failure_timer_cleanup$/ \
  --ignore-name=/^test_timer_cleanup$/ \
  --ignore-name=/^test_nameserver$/ \
  --ignore-name=/^test_invalid_address_bind_connect_dst$/ \
  --ignore-name=/^test_invalid_address_bind_connect_src$/ \
%endif

# TODO: This fails on ppc64 :/
# Moreover it appears abandoned upstream:
# https://github.com/eventmachine/eventmachine/issues/924
#EM_PURE_RUBY=true ruby -Ilib:tests -e "(Dir.glob('./tests/**/test_pure*.rb') + Dir.glob('./tests/**/test_ssl*.rb')).each {|f| require f}" -- \
#   --verbose \
#   --ignore-name /^test_.*v3.*$/ \
#   --ignore-name /^test_no_ecdh_curve$/ \
popd

%files
%dir %{gem_instdir}
%{gem_extdir_mri}
%license %{gem_instdir}/GNU
%license %{gem_instdir}/LICENSE

%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/docs
%{gem_instdir}/examples
# TODO: Hmm, we can build also JRuby bindigs.
%{gem_instdir}/java
%{gem_instdir}/rakelib
%{gem_instdir}/tests

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 07 2025 Vít Ondruch <vondruch@redhat.com> - 1.2.7-28
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.4

* Wed Aug 07 2024 Miroslav Suchý <msuchy@redhat.com> - 1.2.7-27
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Vít Ondruch <vondruch@redhat.com> - 1.2.7-23
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.3

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 03 2023 Vít Ondruch <vondruch@redhat.com> - 1.2.7-20
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.2

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 26 2022 Vít Ondruch <vondruch@redhat.com> - 1.2.7-18
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.1

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.2.7-16
- Rebuilt with OpenSSL 3.0.0

* Wed Aug 04 2021 Vít Ondruch <vondruch@redhat.com> - 1.2.7-15
- Fix intermittent errors.
  Resolves: rhbz#1987936

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Feb 12 2021 Vít Ondruch <vondruch@redhat.com> - 1.2.7-14
- Disable `test_em_system_pid(TestProcesses)` unconditionaly.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan  7 03:18:28 CET 2021 Pavel Valena <pvalena@redhat.com> - 1.2.7-12
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.0

* Wed Jan 06 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> -1.2.7-11
- F-34: rebuild against ruby30
- ruby30: disable one more test for now

* Tue Aug 04 2020 Vít Ondruch <vondruch@redhat.com> - 1.2.7-10
- Disable two more test cases failing without network connectivity with
  systemd-resolved.
  Resolves: rhbz#1866021
- Adjust to tightened Fedora crypto policies.
  Resovles: rhbz#1863726

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-9
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 16 2020 Vít Ondruch <vondruch@redhat.com> - 1.2.7-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.7

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 17 2019 Vít Ondruch <vondruch@redhat.com> - 1.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.6
- Fix OpenSSL 1.1.1 compatibility.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 30 2018 Pavel Valena <pvalena@redhat.com> - 1.2.7-1
- Update to eventmachine 1.2.7.

* Wed May 02 2018 Pavel Valena <pvalena@redhat.com> - 1.2.6-1
- Update to eventmachine 1.2.6.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 1.2.5-3
- Rebuilt for switch to libxcrypt

* Thu Jan 04 2018 Vít Ondruch <vondruch@redhat.com> - 1.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.5

* Tue Aug 22 2017 Vít Ondruch <vondruch@redhat.com> - 1.2.5-1
- Update to EventMachine 1.2.5.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Mar 23 2017 Vít Ondruch <vondruch@redhat.com> - 1.2.3-1
- Update to EventMachine 1.2.3.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 14 2017 Dan Horák <dan[at]danny.cz> - 1.2.1-3
- Disable IPv6 test requiring network connectivity

* Tue Jan 10 2017 Vít Ondruch <vondruch@redhat.com> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.4

* Thu Dec 08 2016 Vít Ondruch <vondruch@redhat.com> - 1.2.1-1
- Update to EventMachine 1.2.1.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 07 2016 Vít Ondruch <vondruch@redhat.com> - 1.0.8-1
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.3
- Update to EventMachine 1.0.8.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 04 2015 Kalev Lember <kalevlember@gmail.com> - 1.0.6-2
- Rebuilt for GCC 5 C++11 ABI change

* Wed Feb 04 2015 Vít Ondruch <vondruch@redhat.com> - 1.0.6-1
- Update to EventMachine 1.0.6.

* Sat Jan 17 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.4-1
- 1.0.4 (https://github.com/eventmachine/eventmachine/issues/495)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 11 2014 Vít Ondruch <vondruch@redhat.com> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr 11 2013 Vít Ondruch <vondruch@redhat.com> - 1.0.3-1
- Update to eventmachine 1.0.3.

* Thu Feb 28 2013 Vít Ondruch <vondruch@redhat.com> - 1.0.1-1
- Update to eventmachine 1.0.1.
- Enable SSL support.

* Wed Feb 27 2013 Vít Ondruch <vondruch@redhat.com> - 1.0.0-1
- Update to eventmachine 1.0.0.

* Wed Feb 27 2013 Vít Ondruch <vondruch@redhat.com> - 0.12.10-9
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 19 2012 Vít Ondruch <vondruch@redhat.com> - 0.12.10-6
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 31 2010 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.12.10-3
- More review fixes

* Sun Jan 31 2010 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.12.10-2
- Review fixes (#556433)

* Mon Jan 18 2010 Ruben Kerkhof <ruben@rubenkerkhof.com> - 0.12.10-1
- Initial package
