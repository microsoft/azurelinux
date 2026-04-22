# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from activestorage-0.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name activestorage

# openh264 coded is not available in buildroot, while it can be obtained e.g.
# from:
# https://codecs.fedoraproject.org/openh264/43/x86_64/Packages/o/openh264-2.6.0-2.fc43.x86_64.rpm
%bcond_with openh264

# TODO: Re-enable recompilation if possible. Currently, we don't have rollup.js
# in Fedora and therefore it requires network access. Still good for checking
# the results
%bcond_with js_recompilation

Name: rubygem-%{gem_name}
Version: 8.0.2
Release: 3%{?dist}
Summary: Local and cloud file storage framework
License: MIT
URL: https://rubyonrails.org
Source0: https://rubygems.org/gems/%{gem_name}-%{version}%{?prerelease}.gem
# git clone https://github.com/rails/rails.git && cd rails/activestorage
# git archive -v -o activestorage-8.0.2-tests.tar.gz v8.0.2 test/
Source1: %{gem_name}-%{version}%{?prerelease}-tests.tar.gz
# Source code of pregenerated JS files.
# git clone https://github.com/rails/rails.git && cd rails/activestorage
# git archive -v -o activestorage-8.0.2-js.tar.gz v8.0.2 package.json rollup.config.js
Source2: %{gem_name}-%{version}%{?prerelease}-js.tar.gz

BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(actionmailer) = %{version}
BuildRequires: rubygem(activerecord) = %{version}
BuildRequires: rubygem(activejob) = %{version}
BuildRequires: rubygem(bundler)
BuildRequires: rubygem(marcel)
BuildRequires: rubygem(railties) = %{version}
BuildRequires: rubygem(sprockets-rails)
BuildRequires: rubygem(image_processing)
BuildRequires: rubygem(sqlite3)
# Required to pass some of the test/models/variant_test.rb
# https://github.com/rails/rails/issues/44395
BuildRequires: vips-magick
BuildRequires: %{_bindir}/ffmpeg
BuildRequires: %{_bindir}/ffprobe
BuildRequires: %{_bindir}/mutool
BuildRequires: %{_bindir}/pdftoppm
%{?with_openh264:BuildRequires: openh264}
%{?with_js_recompilation:BuildRequires: %{_bindir}/npm}
# Used for creating file previews
Suggests: %{_bindir}/mutool
Suggests: %{_bindir}/pdftoppm
Suggests: %{_bindir}/ffmpeg
Suggests: %{_bindir}/ffprobe
# Codec for video analysis
Suggests: openh264

BuildArch: noarch

%description
Attach cloud and local files in Rails applications.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}%{?prerelease} -b1 -b2

%build
%if %{with js_recompilation}
# Recompile the embedded JS files from sources.
#
# This is practice suggested by packaging guidelines:
# https://fedoraproject.org/wiki/Packaging:Guidelines#Use_of_pregenerated_code

find app/assets/ -type f -exec sha512sum {} \;

rm -rf app/assets/

cp -a %{builddir}/rollup.config.js .

# TODO: This requires network access. Use Fedora rollup.js if it becomes
# available eventually
npm install
npx rollup --config rollup.config.js

# For comparison with the orginal checksum above.
find app/assets/ -type f -exec sha512sum {} \;
%endif

gem build ../%{gem_name}-%{version}%{?prerelease}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
( cd .%{gem_instdir}
cp -a %{builddir}/test .

mkdir ../tools
# Fake test_common.rb. It does not provide any functionality besides
# `force_skip` alias.
touch ../tools/test_common.rb
# Netiher strict_warnings.rb appears to be useful.
touch ../tools/strict_warnings.rb

touch Gemfile
echo 'gem "actionmailer"' >> Gemfile
echo 'gem "activerecord"' >> Gemfile
echo 'gem "activejob"' >> Gemfile
echo 'gem "sprockets-rails"' >> Gemfile
echo 'gem "image_processing"' >> Gemfile
echo 'gem "marcel"' >> Gemfile
echo 'gem "railties"' >> Gemfile
echo 'gem "sqlite3"' >> Gemfile

# `ActiveStorage::Service::AzureStorageService` is deprecated and we would need
# `azure-storage-blob` gem to make this work => just ignore the test.
sed -i '/test "azure service is deprecated" do/a\    skip' \
  test/service/configurator_test.rb

# test/javascript_package_test.rb requires rollup.js, which we don't have.
# OTOH, if we had it, we would recomplie the sources and the test would have
# less value.
mv test/javascript_package_test.rb{,.disable}

# The `ffprobe` output does not containe `display_aspect_ratio` for some
# reason. Is it missing codec or error?
sed -i '/test "analyzing a video" do/,/^  end$/ {
  /display_aspect_ratio/ s/^/#/
}' test/analyzer/video_analyzer_test.rb

# Disable tests that require openh264
%if %{without openh264}
sed -i \
  -e '/"video\.mp4"/i\    skip' \
  -e '/"rotated_video\.mp4"/i\    skip' \
  -e '/"video_with_rectangular_samples\.mp4"/i\    skip' \
  -e '/"video_with_undefined_display_aspect_ratio\.mp4"/i\    skip' \
  -e '/"video_without_audio_stream\.mp4"/i\    skip' \
  test/analyzer/video_analyzer_test.rb \
  test/previewer/video_previewer_test.rb \
  test/models/preview_test.rb \
  test/models/representation_test.rb \
  test/models/variant_with_record_test.rb \
%endif

export RUBYOPT="-I${PWD}/lib"
export BUNDLE_GEMFILE=${PWD}/Gemfile

bundle exec ruby -Itest -ractive_storage/engine -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
)

%files
%dir %{gem_instdir}
%license %{gem_instdir}/MIT-LICENSE
%{gem_instdir}/app
%{gem_instdir}/config
%{gem_instdir}/db
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 09 2025 Vít Ondruch <vondruch@redhat.com> - 8.0.2-1
- Update to Active Storage 8.0.2.
  Related: rhbz#2238177

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Nov 10 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 7.0.8-5
- Add BR: rubygem(mutex_m) explicitly for ruby34

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Sep 10 2023 Pavel Valena <pvalena@redhat.com> - 7.0.8-1
- Update to activestorage 7.0.8.

* Mon Aug 28 2023 Pavel Valena <pvalena@redhat.com> - 7.0.7.2-1
- Update to activestorage 7.0.7.2.

* Thu Aug 10 2023 Pavel Valena <pvalena@redhat.com> - 7.0.7-1
- Update to activestorage 7.0.7.

* Sun Jul 23 2023 Pavel Valena <pvalena@redhat.com> - 7.0.6-1
- Update to activestorage 7.0.6.

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 30 2023 Pavel Valena <pvalena@redhat.com> - 7.0.5-1
- Update to activestorage 7.0.5.

* Tue Mar 14 2023 Pavel Valena <pvalena@redhat.com> - 7.0.4.3-1
- Update to activestorage 7.0.4.3.

* Wed Jan 25 2023 Pavel Valena <pvalena@redhat.com> - 7.0.4.2-1
- Update to activestorage 7.0.4.2.

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Sep 15 2022 Pavel Valena <pvalena@redhat.com> - 7.0.4-1
- Update to activestorage 7.0.4.

* Tue Aug 02 2022 Vít Ondruch <vondruch@redhat.com> - 7.0.2.3-3
- Fix Minitest 5.16+ compatibility.
  Resolves: rhbz#2113686

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Mar 14 2022 Pavel Valena <pvalena@redhat.com> - 7.0.2.3-1
- Update to activestorage 7.0.2.3.

* Wed Feb 09 2022 Pavel Valena <pvalena@redhat.com> - 7.0.2-1
- Update to activestorage 7.0.2.

* Thu Feb 03 2022 Pavel Valena <pvalena@redhat.com> - 7.0.1-1
- Update to activestorage 7.0.1.

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Sep 17 2021 Pavel Valena <pvalena@redhat.com> - 6.1.4.1-1
- Update to activestorage 6.1.4.1.

* Tue Aug 31 2021 Vít Ondruch <vondruch@redhat.com> - 6.1.4-3
- Re-enable TIFF test after ImageMagick issues were resolved.
  Related: rhbz#1993193

* Fri Aug 06 2021 Vít Ondruch <vondruch@redhat.com> - 6.1.4-2
- Disable flaky TIFF test.
  Resolves: rhbz#1987926

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 30 2021 Pavel Valena <pvalena@redhat.com> - 6.1.4-1
- Update to activestorage 6.1.4.

* Tue May 18 2021 Pavel Valena <pvalena@redhat.com> - 6.1.3.2-1
- Update to activestorage 6.1.3.2.

* Fri Apr 16 2021 Pavel Valena <pvalena@redhat.com> - 6.1.3.1-2
- Relax mini_mime dependency.

* Fri Apr 09 2021 Pavel Valena <pvalena@redhat.com> - 6.1.3.1-1
- Update to activestorage 6.1.3.1.

* Thu Feb 18 2021 Pavel Valena <pvalena@redhat.com> - 6.1.3-1
- Update to activestorage 6.1.3.

* Mon Feb 15 2021 Pavel Valena <pvalena@redhat.com> - 6.1.2.1-1
- Update to activestorage 6.1.2.1.

* Wed Jan 27 2021 Pavel Valena <pvalena@redhat.com> - 6.1.1-1
- Update to activestorage 6.1.1.
  Resolves: rhbz#1906180

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct  8 11:56:48 CEST 2020 Pavel Valena <pvalena@redhat.com> - 6.0.3.4-1
- Update to activestorage 6.0.3.4.
  Resolves: rhbz#1877544

* Tue Sep 22 01:10:44 CEST 2020 Pavel Valena <pvalena@redhat.com> - 6.0.3.3-1
- Update to activestorage 6.0.3.3.
  Resolves: rhbz#1877544

* Mon Aug 17 05:23:03 GMT 2020 Pavel Valena <pvalena@redhat.com> - 6.0.3.2-1
- Update to activestorage 6.0.3.2.
  Resolves: rhbz#1742796

* Mon Aug 03 07:01:37 GMT 2020 Pavel Valena <pvalena@redhat.com> - 6.0.3.1-1
- Update to ActiveStorage 6.0.3.1.
  Resolves: rhbz#1742796

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 20 2019 Tom Callaway <spot@fedoraproject.org> - 5.2.3-4
- rebuild for new rubygem-connection_pool

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Mar 28 2019 Pavel Valena <pvalena@redhat.com> - 5.2.3-2
- Enable tests.

* Thu Mar 28 2019 Pavel Valena <pvalena@redhat.com> - 5.2.3-1
- Update to Active Storage 5.2.3.

* Mon Mar 18 2019 Pavel Valena <pvalena@redhat.com> - 5.2.2.1-2
- Enable tests.

* Thu Mar 14 2019 Pavel Valena <pvalena@redhat.com> - 5.2.2.1-1
- Update to Active Storage 5.2.2.1.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 05 2018 Pavel Valena <pvalena@redhat.com> - 5.2.2-2
- Update to Active Storage 5.2.2.

* Thu Aug 09 2018 Pavel Valena <pvalena@redhat.com> - 5.2.1-2
- Enable tests.

* Wed Aug 08 2018 Pavel Valena <pvalena@redhat.com> - 5.2.1-1
- Update to Active Storage 5.2.1.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue May 29 2018 Pavel Valena <pvalena@redhat.com> - 5.2.0-2
- Enable tests.

* Wed May 02 2018 Pavel Valena <pvalena@redhat.com> - 5.2.0-1
- Update to Active Storage 5.2.0.
- Moved to Rails repository.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Aug 28 2017 Vít Ondruch <vondruch@redhat.com> - 0.1-1
- Initial package
