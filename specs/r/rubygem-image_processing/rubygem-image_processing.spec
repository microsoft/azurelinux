# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from image_processing-1.11.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name image_processing

# dhash-vips gem is not in Fedora yet
%bcond_with dhash-vips

Name: rubygem-%{gem_name}
Version: 1.12.2
Release: 10%{?dist}
Summary: High-level wrapper for processing images for the web with ImageMagick or libvips
License: MIT
URL: https://github.com/janko/image_processing
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Tests are not shipped with the gem, you may check them out like so:
# git clone --no-checkout https://github.com/janko/image_processing
# git -C image_processing archive -v -o image_processing-1.12.2-tests.txz v1.12.2 test/
Source1: %{gem_name}-%{version}-tests.txz
# Fix compatibility with Minitest 5.19+
# https://github.com/janko/image_processing/pull/114
Patch0: rubygem-image_processing-1.12.2-Fix-compatibility-with-Minitest-5.19.patch

BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 2.3
BuildRequires: rubygem(minitest) >= 5.8
BuildRequires: rubygem(mini_magick)
%if %{with dhash-vips}
BuildRequires: rubygem(dhash-vips)
%endif
BuildRequires: rubygem(ruby-vips)
BuildArch: noarch

%description
High-level wrapper for processing images for the web with ImageMagick or
libvips.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b1

pushd %{_builddir}
%patch 0 -p1
popd

# dhash-vips is not in Fedora yet.
%if %{without dhash-vips}
%gemspec_remove_dep -d -g dhash-vips
%endif

%build
gem build ../%{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
ln -s %{_builddir}/test .

# Tests dependencies that are not needed
sed -i '/require .minitest.hooks/ s/^/#/g' test/test_helper.rb
sed -i '/require .minispec-metadata/ s/^/#/g' test/test_helper.rb
sed -i '/require .bundler./ s/^/#/g' test/test_helper.rb

%if %{without dhash-vips}
sed -i -e '/require .dhash-vips./ s/^/#/g' \
    -e '/^  def distance(image1, image2)/ a \
    skip ' test/test_helper.rb

%endif

# Use the RUBY_ENGINE check to avoid phashion dependency
sed -i '/RUBY_ENGINE == "jruby"/ s/jruby/ruby/' test/test_helper.rb

# Test output has changed with vips or rubygems-vips version
# https://github.com/janko/image_processing/issues/98
sed -i '/it "raises correct Vips::Error on unknown saver" do/ a\
  skip ' test/vips_test.rb

ruby -Ilib:test -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE.txt
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md
%{gem_instdir}/%{gem_name}.gemspec

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 31 2023 Vít Ondruch <vondruch@redhat.com> - 1.12.2-4
- Fix FTBFS due to incompatibility with Minitest 5.19+.

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jul 26 2022 Pavel Valena <pvalena@redhat.com> - 1.12.2-1
- Update to image_processing 1.12.2.
Resolves: CVE-2022-24720

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 11 2020 Pavel Valena <pvalena@redhat.com> - 1.11.0-2
- Initial package
  Resolves: rhbz#1869719
