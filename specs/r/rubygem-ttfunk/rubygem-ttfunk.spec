# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name ttfunk

Summary: Font Metrics Parser for Prawn
Name: rubygem-%{gem_name}
Version: 1.7.0
Release: 14%{?dist}
# Automatically converted from old format: GPLv2 or GPLv3 or Ruby - review is highly recommended.
License: GPL-2.0-only OR GPL-3.0-only OR Ruby
URL: https://github.com/prawnpdf/ttfunk
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# Test suite is not packaged with the gem, you may check out it like so:
# git clone --no-checkout https://github.com/prawnpdf/ttfunk
# cd ttfunk && git archive -v -o ttfunk-1.7.0-spec.txz 1.7.0 spec
Source1: %{gem_name}-%{version}-spec.txz
# Reduired by: lib/ttfunk/table/cff/dict.rb
Requires: rubygem(bigdecimal)
BuildRequires: ruby
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygems
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(bigdecimal)
BuildArch: noarch

%description
TTFunk is a TrueType font parser written in pure ruby.

%package doc
BuildArch:  noarch
Requires:   %{name} = %{version}-%{release}
Summary:    Documentation for rubygem-%{gem_name}

%description doc
This package contains documentation for rubygem-%{gem_name}.

%prep
%setup -q -n %{gem_name}-%{version} -b1

%build
gem build ../%{gem_name}-%{version}.gemspec

%gem_install
rm -rf ./%{gem_dir}/gems/%{gem_name}-%{version}/.yardoc

%check
pushd .%{gem_instdir}
ln -s %{_builddir}/spec .

rspec spec
popd

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

%files
%license %{gem_instdir}/{COPYING,GPLv2,GPLv3,LICENSE}
%dir %{gem_instdir}
%{gem_instdir}/lib
%exclude %{gem_cache}
%exclude %{gem_instdir}/.*
%{gem_spec}

%files doc
%doc %{gem_instdir}/{README.md,CHANGELOG.md}
%doc %{gem_docdir}


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 07 2024 Miroslav Suchý <msuchy@redhat.com> - 1.7.0-11
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 12 18:41:28 CET 2021 Vít Ondruch <vondruch@redhat.com> - 1.7.0-2
- Add `BR: rubygem(bigdecimal)`.

* Tue Dec 29 2020 Christopher Brown <chris.brown@redhat.com> - 1.7.0-1
- Update to 1.7.0

* Mon Aug 03 06:53:36 GMT 2020 Pavel Valena <pvalena@redhat.com> - 1.6.2.1-1
- Update to ttfunk 1.6.2.1.
  Resolves: rhbz#1787872

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 15 2018 Christopher Brown <chris.brown@redhat.com> - 1.5.1-1
- Update to 1.5.1

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Miroslav Suchý 1.4.0-1
- rebase to ttfunk-1.4.0

* Tue Feb 11 2014 Miroslav Suchý <msuchy@redhat.com> 1.1.0-1
- new package built with tito

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Josef Stribny <jstribny@redhat.com> - 1.0.3-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Aug 16 2012 Miroslav Suchý <msuchy@redhat.com> 1.0.3-4
- 845805 - move CHANGELOG to -doc package (msuchy@redhat.com)

* Thu Aug 16 2012 Miroslav Suchý <msuchy@redhat.com> 1.0.3-3
- 845805 - move README.rdoc to -doc subpackage (msuchy@redhat.com)
- 845805 - mark gem_docdir as %%doc and exclude gem_cache (msuchy@redhat.com)

* Thu Aug 09 2012 Miroslav Suchý <msuchy@redhat.com> 1.0.3-2
- fix spec for fedora review (msuchy@redhat.com)

* Sun Aug 05 2012 Miroslav Suchý <msuchy@redhat.com> 1.0.3-1
- new package built with tito

