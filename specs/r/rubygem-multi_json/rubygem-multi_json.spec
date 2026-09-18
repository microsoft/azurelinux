# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from multi_json-1.0.3.gem by gem2rpm -*- rpm-spec -*-
%global gem_name multi_json

Name: rubygem-%{gem_name}
Version: 1.15.0
Release: 12%{?dist}
Summary: A common interface to multiple JSON libraries
License: MIT
URL: https://github.com/intridea/multi_json
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/intridea/multi_json.git && cd multi_json
# git archive -v -o multi_json-1.15.0-spec.tar.gz v1.15.0 spec/
Source1: %{gem_name}-%{version}-spec.tar.gz
# Fix RSpec 3.11.0+ compatibility due to improved kwargs handling.
# https://github.com/intridea/multi_json/pull/205
Patch0: rubygem-mulit_json-1.15.0-RSpec-3.11.0-distinguishes-between-hashed-and-Ruby-3.patch
BuildRequires: ruby(release)
BuildRequires: rubygems-devel >= 1.3.5
BuildRequires: ruby
BuildRequires: rubygem(rspec)
BuildArch: noarch
# OkJson is allowed to be bundled:
# https://fedorahosted.org/fpc/ticket/113
Provides: bundled(okjson) = 45

%description
A common interface to multiple JSON libraries, including Oj, Yajl, the JSON
gem (with C-extensions), the pure-Ruby JSON gem, NSJSONSerialization, gson.rb,
JrJackson, and OkJson.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b 1

pushd %{_builddir}
%patch 0 -p1
popd

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
ln -s %{_builddir}/spec spec

# json_pures is not available on Fedora.
sed -i "/require.*json\/pure/ s/^/#/" spec/multi_json_spec.rb
sed -i "s/JsonPure/OkJson/" spec/multi_json_spec.rb
sed -i "s/json_pure/ok_json/" spec/multi_json_spec.rb
# oj is not available on Fedora.
sed -i "/expect(MultiJson.adapter.to_s).to eq('MultiJson::Adapters::Oj')/ s/Oj/JsonGem/" spec/multi_json_spec.rb

# Execute main test suite.
SKIP_ADAPTERS=jr_jackson rspec spec/{multi_json,options_cache}_spec.rb

# json_pure adapter does not support skipping :/
mv spec/json_pure_adapter_spec.rb{,.disable}

# Adapters have to be tested separately, but disable test of engines
# unsupported on Fedora (they may cause test suite to fail).
for adapter in spec/*_adapter_spec.rb; do
  SKIP_ADAPTERS=json_pure,gson,jr_jackson,nsjsonserialization,oj,yajl rspec $adapter
done

popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE.md
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/README.md

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Sep 06 2022 Vít Ondruch <vondruch@redhat.com> - 1.15.0-6
- Fix RSpec 3.11.0+ compatibility.
  Resolves: rhbz#2113694

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Nov 06 2020 Vít Ondruch <vondruch@redhat.com> - 1.15.0-1
- Update to MultiJSON 1.15.0.
  Resolves: rhbz#1855521
- Drop `BR: rubygem(json_pure)`.

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Apr 15 2020 Vít Ondruch <vondruch@redhat.com> - 1.14.1-1
- Update to MultiJSON 1.14.1.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 23 2018 Vít Ondruch <vondruch@redhat.com> - 1.13.1-1
- Update to MultiJSON 1.13.1.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Oct 12 2016 Vít Ondruch <vondruch@redhat.com> - 1.12.1-1
- Update to MultiJSON 1.12.1.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 02 2015 Vít Ondruch <vondruch@redhat.com> - 1.10.1-1
- Update to MultiJSON 1.10.1.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 12 2014 Vít Ondruch <vondruch@redhat.com> - 1.8.4-1
- Update to multi_json 1.8.4.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 14 2013 Vít Ondruch <vondruch@redhat.com> - 1.7.7-1
- Update to multi_json 1.7.7.

* Wed Mar 20 2013 Vít Ondruch <vondruch@redhat.com> - 1.7.1-1
- Update to multi_json 1.7.1.

* Tue Feb 26 2013 Vít Ondruch <vondruch@redhat.com> - 1.3.6-4
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3.6-1
- Update to multi_json 1.3.6.
- Switch to rubygem(rspec) from rubygem(rspec-core).

* Tue Jan 24 2012 Vít Ondruch <vondruch@redhat.com> - 1.0.3-5
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 11 2011 Vít Ondruch <vondruch@redhat.com> - 1.0.3-3
- Removed useless shebang.

* Fri Nov 11 2011 Vít Ondruch <vondruch@redhat.com> - 1.0.3-2
- Review fixes.

* Fri Jul 08 2011 Vít Ondruch <vondruch@redhat.com> - 1.0.3-1
- Initial package
