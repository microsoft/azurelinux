# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from em-http-request-1.1.5.gem by gem2rpm -*- rpm-spec -*-
%global gem_name em-http-request

Name: rubygem-%{gem_name}
Version: 1.1.7
Release: 14%{?dist}
Summary: EventMachine based, async HTTP Request client
License: MIT
URL: http://github.com/igrigorik/em-http-request
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Since Ruby 3.0 keyword arguments need to be explicitly declared
# PR: https://github.com/igrigorik/em-http-request/pull/344
Patch0: %{name}-%{version}-explicit-keyword-argument.patch
Patch1: em-http-request-1.1.7-Also-stop-the-HTTP-parser-in-addition-to-resetting.patch
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(eventmachine)
BuildRequires: rubygem(multi_json)
BuildRequires: rubygem(em-socksify)
BuildRequires: rubygem(addressable)
BuildRequires: rubygem(cookiejar)
BuildRequires: rubygem(http_parser.rb)
BuildRequires: rubygem(rack)
BuildRequires: rubygem(webrick)
BuildRequires: %{_bindir}/ping
BuildRequires: rubygem(rspec)

BuildArch: noarch

%description
EventMachine based, async HTTP Request client.


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
# Create the gem as gem install only works on a gem file
gem build ../%{gem_name}-%{version}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


# Have networking enabled in your mock config before testing
%check
# Check section disabled: Tests fail due to lacking network access, and get stuck until they hit mock's 24 hour timeout.
exit 0

pushd .%{gem_instdir}
# We are trying not to use bundler when not needed
sed -i "/require 'bundler\/setup'/ s/^/#/" spec/helper.rb
# Mongrel is deprecated so we are using WEBrick server
sed -i 's/Mongrel/WEBrick/' spec/stallion.rb
# Missing require on pathname in client spec
sed -i "/^require 'helper'/i require 'pathname'" spec/client_spec.rb

# Fails, not quite sure why :/
sed -i '/it "should report error if connection was closed by server on client keepalive requests" do/ ,/^  end$/ s/^/#/' spec/client_spec.rb

# These tests fail on WEBrick but on Puma the tests are passing.
sed -i '/it "should set content-length to 0 on posts with empty bodies" do/ ,/^  end$/ s/^/#/' spec/client_spec.rb
sed -i '/it "should fail GET on invalid host" do/ ,/^  end$/ s/^/#/' spec/dns_spec.rb
sed -i '/it "should keep default https port in redirect url that include it"/ ,/^  end$/ s/^/#/' spec/redirect_spec.rb
sed -i '/it "should keep default http port in redirect url that include it"/ ,/^  end$/ s/^/#/' spec/redirect_spec.rb
# Got a different message than expected with WEBrick, works on Puma
sed -i '/it "should fail gracefully on an invalid host in Location header" do/ ,/^  end$/ s/^/#/' spec/dns_spec.rb

# One of tests expects UTF-8 encoding.
LANG=C.UTF-8 rspec spec -f d
popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%{gem_instdir}/benchmarks
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/Changelog.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/em-http-request.gemspec
%{gem_instdir}/examples
%{gem_instdir}/spec

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 22 2023 Jarek Prokop <jprokop@redhat.com> - 1.1.7-9
- Fix FTBFS due to updated rubygem-http_parser.rb.

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 4 2021 Jaroslav Prokop <jprokop@redhat.com> - 1.1.7-3
- Use explicit keyword declaration in stallion.rb.
  resolves rhbz#1924714

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 30 2020 Jaroslav Prokop <jar.prokop@volny.cz> - 1.1.7-1
- Update to version 1.1.7
  resolves rhbz#1842726

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.1.5-5
- Use C.UTF-8 locale
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Sat Jul 14 2018 Jaroslav Prokop <jar.prokop@volny.cz> - 1.1.5-4
- Delete "Requires: rubygem(cookiejar)".

  Bug#1561487 regarding this issue was fixed.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 28 2018 Jaroslav Prokop <jar.prokop@volny.cz> - 1.1.5-2
- Add rubygem(cookiejar) require, for more info see comment
  at the require.

* Tue Feb 20 2018 Jaroslav Prokop <jar.prokop@volny.cz> - 1.1.5-1
- Initial package
