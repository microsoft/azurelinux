# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name pdf-core

Name: rubygem-%{gem_name}
Version: 0.9.0
Release: 12%{?dist}
Summary: PDF::Core is used by Prawn to render PDF documents
# Automatically converted from old format: GPLv2 or GPLv3 or Ruby - review is highly recommended.
License: GPL-2.0-only OR GPL-3.0-only OR Ruby 
URL: https://github.com/prawnpdf/pdf-core
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/prawnpdf/pdf-core && cd pdf-core
# git checkout 0.9.0 && tar czvf pdf-core-0.9.0-specs.tgz spec/
Source1: %{gem_name}-%{version}-specs.tgz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel >= 1.3.6
BuildRequires: ruby >= 1.9.3
BuildRequires: rubygem(pdf-reader) => 1.2
BuildRequires: rubygem(pdf-inspector) => 1.1.0
BuildRequires: rubygem(rspec)

BuildArch: noarch

%description
PDF::Core is used by Prawn to render PDF documents.


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
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


%check
pushd .%{gem_instdir}
# Symlinking does not work for this test suite
cp -r %{_builddir}/spec .

# get rid of bundler
sed -i -e "s/require 'bundler'//" spec/spec_helper.rb
sed -i -e 's/Bundler.setup//' spec/spec_helper.rb
rspec spec
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%license %{gem_instdir}/LICENSE
%doc %{gem_instdir}/COPYING
%doc %{gem_instdir}/GPLv2
%doc %{gem_instdir}/GPLv3

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/%{gem_name}.gemspec

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 07 2024 Miroslav Suchý <msuchy@redhat.com> - 0.9.0-10
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 1 2021 Christopher Brown <chris.brown@redhat.com> - 0.9.0-1
- Update to 0.9.0

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Oct 25 2018 Pavel Valena <pvalena@redhat.com> - 0.8.1-1
- Update to pdf-core 0.8.1.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 27 2018 Vít Ondruch <vondruch@redhat.com> - 0.6.1-5
- Remove unneeded SimpleCov build dependency.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jun 15 2016 Fabio Alessandro Locati <me@fale.io> - 0.6.1-1
- Update to 0.6.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Aug 24 2015 Josef Stribny <jstribny@redhat.com> - 0.6.0-1
- Update to 0.6.0

* Mon Jun 22 2015 Josef Stribny <jstribny@redhat.com> - 0.5.1-1
- Update to 0.5.1

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 05 2014 Josef Stribny <jstribny@redhat.com> - 0.2.5-1
- Initial package
