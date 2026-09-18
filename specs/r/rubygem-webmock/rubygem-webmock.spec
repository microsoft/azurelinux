# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from webmock-1.7.6.gem by gem2rpm -*- rpm-spec -*-
%global gem_name webmock

# Disable HTTP clients integration tests we don't have in Fedora.
%bcond_with    async_http
%bcond_without curb
%bcond_without em_http_request
%bcond_without excon
%bcond_with    http_rb
%bcond_without httpclient
%bcond_with    manticore
%bcond_without net_http
%bcond_with    patron
%bcond_without typhoeus

Name: rubygem-%{gem_name}
Version: 3.23.1
Release: 4%{?dist}
Summary: Library for stubbing HTTP requests in Ruby
License: MIT
URL: https://github.com/bblimke/webmock
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/bblimke/webmock.git && cd webmock
# git archive -v -o webmock-3.23.1-tests.tar.gz v3.23.1 minitest/ spec/ test/
Source1: %{gem_name}-%{version}-tests.tar.gz
# Revert dependency on rspec-retry, because it is not available in Fedora
Patch0: rubygem-webmock-3.23.1-Revert-Retry-timed-out-real-requests-when-running-we.patch
# Fix REXML 3.3.3+ compatibility.
# https://github.com/bblimke/webmock/pull/1066
Patch1: rubygem-webmock-3.23.1-Rescue-exceptions.patch
# https://github.com/bblimke/webmock/pull/1074
# support ruby3.4 hash inspect change
Patch2: rubygem-webmock-pr1074-ruby34-hash-inspect-change.patch
# https://github.com/bblimke/webmock/pull/1081
# ruby34 removes deprecated net-http constants
Patch3: rubygem-webmock-pr1081-ruby34-net-http-constants.patch
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(addressable)
BuildRequires: rubygem(crack)
BuildRequires: rubygem(hashdiff)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(rack)
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(test-unit)
BuildRequires: rubygem(webrick)

%{?with_async_http:BuildRequires: rubygem(async-http)}
%{?with_curb:BuildRequires: rubygem(curb)}
%{?with_em_http_request:BuildRequires: rubygem(em-http-request)}
%{?with_excon:BuildRequires: rubygem(excon)}
%{?with_http_rb:BuildRequires: rubygem(http_rb)}
%{?with_httpclient:BuildRequires: rubygem(httpclient)}
%{?with_manticore:BuildRequires: rubygem(manticore)}
%{?with_patron:BuildRequires: rubygem(patron)}
%{?with_typhoeus:BuildRequires: rubygem(typhoeus)}
BuildArch: noarch

%description
WebMock allows stubbing HTTP requests and setting expectations on HTTP
requests.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b 1

# JSON is required by lib/webmock/request_body_diff.rb
%gemspec_add_dep -g json

%patch 1 -p1
%patch 3 -p1

pushd %{builddir}
%patch 0 -p1
%patch 2 -p1
popd

%build
gem build ../%{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Run the test suite
%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

pushd .%{gem_instdir}

ln -s %{builddir}/minitest minitest
ln -s %{builddir}/spec spec
ln -s %{builddir}/test test

ruby -e 'Dir.glob "./minitest/**/*.rb", &method(:require)'
ruby -e 'Dir.glob "./test/**/test_*.rb", &method(:require)'

# Create list of dependencies to ignore based on bcond flags.
ignore_list=(
%{with_async_http_client}
%{with_curb}
%{with_em_http_request}
%{with_excon}
%{with_http_rb}
%{with_httpclient}
%{with_manticore}
%{with_net_http}
%{with_patron}
%{with_typhoeus}
)
ignore_list=($(echo ${ignore_list[*]} | \
  sed 's/1//g' | \
  sed -r 's/%\{with_([^{]*)\}/\1/g'
))

# Remove unavailable dependencies based on ignore_list.
for i in ${ignore_list[*]}; do
  sed -i "/$i/ s/^/#/" spec/spec_helper.rb
done

# and we don't care about code quality, that's upstream business.
rspec spec --exclude-pattern 'spec/{quality_spec.rb,acceptance/**/*}'

# Run acceptance test for each http client independently.
for t in spec/acceptance/*/; do
  acceptance_test=$(basename ${t})
  if [[ " ${ignore_list[*]} " =~ " ${acceptance_test} " ]]; then
    echo "* ${acceptance_test} acceptance test ignored due to missing dependency"
    continue
  fi
  rspec ${t}
done

popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.23.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.23.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Nov 18 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.23.1-2
- Apply upstream patch for ruby34 hash inspect formatting change
- Apply upstream patch for ruby34 net-http legacy constants removal

* Tue Sep 10 2024 Vít Ondruch <vondruch@redhat.com> - 3.23.1-1
- Update to WebMock 3.23.1.
  Resolves: rhbz#2235050

* Tue Sep 10 2024 Vít Ondruch <vondruch@redhat.com> - 3.18.1-4
- Fix REXML 3.3.3+ compatibility.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Aug 21 2023 Vít Ondruch <vondruch@redhat.com> - 3.18.1-1
- Update to WebMock 3.18.1.
  Resolves: rhbz#2113829

* Mon Aug 21 2023 Vít Ondruch <vondruch@redhat.com> - 3.14.0-5
- Fix FTBFS due to rubygem-minitest 5.19+.

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.14.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Mar 02 2022 Vít Ondruch <vondruch@redhat.com> - 3.14.0-1
- Fix FTBFS caused by latest RSpec.
- Selectively disable acceptance tests.
- Update to WebMock 3.14.0.
  Resolves: rhbz#1922849

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 13 2021 Vít Ondruch <vondruch@redhat.com> - 3.11.1-1
- Update to WebMock 3.11.1.
  Resolves: rhbz#1878462

* Wed Aug 26 2020 Vít Ondruch <vondruch@redhat.com> - 3.8.3-1
- Update to WebMock 3.8.3.
  Resolves: rhbz#1717226

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 04 2019 Pavel Valena <pvalena@redhat.com> - 3.5.1-1
- Update to WebMock 3.5.1.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Feb 07 2017 Vít Ondruch <vondruch@redhat.com> - 2.3.2-1
- Updated to webmock 2.3.2.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.21.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Sep 01 2015 Vít Ondruch <vondruch@redhat.com> - 1.21.0-1
- Updated to webmock 1.21.0.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jan 21 2014 Mo Morsi <mmorsi@redhat.com> - 1.17.1-1
- Update to version 1.17.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Vít Ondruch <vondruch@redhat.com> - 1.9.0-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Mo Morsi <mmorsi@redhat.com> - 1.9.0-1
- Updated to webmock 1.9.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 02 2012 Vít Ondruch <vondruch@redhat.com> - 1.8.7-1
- Updated to webmock 1.8.7.

* Mon Feb 13 2012 Mo Morsi <mmorsi@redhat.com> - 1.7.10-1
- Update to latest upstream release
- Build against ruby 1.9

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 03 2011 Mo Morsi <mmorsi@redhat.com> - 1.7.6-2
- Update to conform to guidelines

* Wed Sep 28 2011 Mo Morsi <mmorsi@redhat.com> - 1.7.6-1
- Initial package
