# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name prawn

Summary: A fast and nimble PDF generator for Ruby
Name: rubygem-%{gem_name}
Version: 2.4.0
Release: 14%{?dist}
# afm files are licensed by APAFML, the rest of package is GPLv2 or GPLv3 or Ruby
# Automatically converted from old format: (GPLv2 or GPLv3 or Ruby) and APAFML - review is highly recommended.
License: ( GPL-2.0-only OR GPL-3.0-only OR Ruby ) AND APAFML
URL: http://prawnpdf.org
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Not all of data is shipped, but it's needed for the test suite.
# You may check out it like so:
# git clone --no-checkout https://github.com/prawnpdf/prawn.git
# cd prawn && git archive -v -o prawn-2.4.0-data.txz 2.4.0 data
Source1: %{gem_name}-%{version}-data.txz
BuildRequires: ruby
BuildRequires: ruby(release)
BuildRequires: rubygems-devel >= 1.3.6
BuildRequires: rubygem(matrix)
BuildRequires: rubygem(rspec) >= 3.0
BuildRequires: rubygem(ttfunk) >= 1.7
BuildRequires: rubygem(pdf-reader) >= 1.4.0
BuildRequires: rubygem(pdf-inspector) >= 1.2.1
BuildRequires: rubygem(pdf-core) >= 0.9.0
BuildArch: noarch

%description
Prawn is a pure Ruby PDF generation library that provides a lot of great
functionality while trying to remain simple and reasonably performant.
Here are some of the important features we provide:

- Vector drawing support, including lines, polygons, curves, ellipses, etc.
- Extensive text rendering support, including flowing text and limited inline
  formatting options.
- Support for both PDF builtin fonts as well as embedded TrueType fonts
- A variety of low level tools for basic layout needs, including a simple
  grid system
- PNG and JPG image embedding, with flexible scaling options
- Reporting tools for rendering complex data tables, with pagination support
- Security features including encryption and password protection
- Tools for rendering repeatable content (i.e headers, footers, and page
  numbers)
- Comprehensive internationalization features, including full support for UTF-8
  based fonts, right-to-left text rendering, fallback font support,
  and extension points for customizable text wrapping.
- Support for PDF outlines for document navigation
- Low level PDF features, allowing users to create custom extensions
  by dropping down all the way to the PDF object tree layer.
  (Mostly useful to those with knowledge of the PDF specification)
- Lots of other stuff!

%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
%setup -q -n %{gem_name}-%{version} -b1

# matrix is bundled gem since Ruby 3.1.
# https://github.com/prawnpdf/prawn/commit/3658d5125c3b20eb11484c3b039ca6b89dc7d1b7
%gemspec_add_dep -g matrix '~> 0.4'

%build
gem build ../%{gem_name}-%{version}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
rm -rf data
ln -s %{_builddir}/data .

sed -i "/^require 'bundler'/d" ./spec/spec_helper.rb
sed -i "/^Bundler.setup/d" ./spec/spec_helper.rb

# manual_builder dependency is not in Fedora yet
mv spec/prawn_manual_spec.rb{,.disable}

# There are missing font and image files required by test suite.
# These are not bundled in the gem therefore some failures occur.
rspec spec
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%license %{gem_instdir}/{LICENSE,COPYING,GPLv2,GPLv3}
%exclude %{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/data/fonts/*.afm
%exclude %{gem_instdir}/.yardopts

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/spec
%doc %{gem_instdir}/manual
%doc %{gem_instdir}/data/fonts/MustRead.html

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 07 2024 Miroslav Suchý <msuchy@redhat.com> - 2.4.0-12
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 11 2022 Vít Ondruch <vondruch@redhat.com> - 2.4.0-6
- Add matrix dependency for Ruby 3.1 compatibility.

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 12 2021 Vít Ondruch <vondruch@redhat.com> - 2.4.0-2
- Drop buildtime dependency on rubygem(bigdecimal).

* Fri Jan 8 2021 Christopher Brown <chris.brown@redhat.com> - 2.4.0-1
- Update to 2.4.0
  Resolves: rhbz#1911811

* Mon Aug 03 06:49:08 GMT 2020 Pavel Valena <pvalena@redhat.com> - 2.3.0-1
- Update to prawn 2.3.0.
  Resolves: rhbz#1862713

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov 08 2018 Christopher Brown <chris.brown@redhat.com> - 2.2.2-1
- Update to 2.2.2

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 27 2018 Vít Ondruch <vondruch@redhat.com> - 2.1.0-5
- Enable test suite.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jun 15 2016 Fabio Alessandro Locati <me@fale.io> - 2.1.0-1
- Update to 2.1.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Aug 24 2015 Josef Stribny <jstribny@redhat.com> - 2.0.2-1
- Update to 2.0.2

* Mon Jun 22 2015 Josef Stribny <jstribny@redhat.com> - 2.0.1-1
- Update to 2.0.1

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Josef Stribny <jstribny@redhat.com> - 1.2.1-1
- Update to 1.2.1

* Mon Jun 23 2014 Josef Stribny <jstribny@redhat.com> - 1.0.0-1
- Update to final 1.0.0 version

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.7.rc2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 06 2014 Josef Stribny <jstribny@redhat.com> - 1.0.0-0.6.rc2
- Relax rubygem-ttfunk dep

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.5.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 17 2013 Josef Stribny <jstribny@redhat.com> - 1.0.0-0.4.rc2
- Fixed license considering .afm

* Thu May 16 2013 Josef Stribny <jstribny@redhat.com> - 1.0.0-0.3.rc2
- *.ttf fonts and rails.png removal

* Tue Apr 16 2013 Josef Stribny <jstribny@redhat.com> - 1.0.0-0.2.rc2
- Move /data to main package

* Mon Apr 15 2013 Josef Stribny <jstribny@redhat.com> - 1.0.0-0.1.rc2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to Prawn 1.0.0.rc2

* Tue Dec 04 2012 Josef Stribny <jstribny@redhat.com> - 0.12.0-1
- Initial package
