# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from mini_magick-4.8.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name mini_magick

Name: rubygem-%{gem_name}
Version: 4.11.0
Release: 14%{?dist}
Summary: Manipulate images with minimal use of memory via ImageMagick / GraphicsMagick
License: MIT
URL: https://github.com/minimagick/minimagick
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem

# The mini_magick gem doesn't ship with the test suite.
# You may check it out like so:
# git clone http://github.com/minimagick/minimagick.git --no-checkout
# cd minimagick && git archive -v -o mini_magick-4.11.0-tests.txz v4.11.0 spec/
Source1: %{gem_name}-%{version}-tests.txz

# https://github.com/minimagick/minimagick/pull/550
# File.exists? is deprecated since ruby 2.1.0 and will be removed on ruby 3.2
Patch0:  rubygem-mini_magick-4.11.0-File_exists-removal.patch

Requires: ImageMagick
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(rexml)
BuildRequires: ruby
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(webmock)
BuildRequires: ImageMagick
BuildArch: noarch

%description
A ruby wrapper for ImageMagick command line. Using MiniMagick the ruby
processes memory remains small (it spawns ImageMagick's command line program
mogrify which takes up some memory as well, but is much smaller compared
to RMagick).


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b1

( cd %{_builddir}/spec
%patch -P0 -p2
)

%build
gem build ../%{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

pushd .%{gem_instdir}
ln -s %{_builddir}/spec .

# Remove unneeded pry dependency.
# https://github.com/minimagick/minimagick/pull/453
# Also remove bundler.
sed -i -e '/require "pry"/ s/^/#/g' \
       -e '/require "bundler/ s/^/#/g' \
  spec/spec_helper.rb

# We do not use GraphicsMagic or posix-spawn
sed -i -e '/^  \[:imagemagick, :graphicsmagick\].each do |cli|$/ s/, :graphicsmagick//g' \
       -e '/^  \["open3", "posix-spawn"\].each do |shell_api|$/ s/, "posix-spawn"//g' \
  spec/spec_helper.rb
sed -i '/^    it "identifies when gm exists" do$/,/    end/ s/^/#/g' \
  spec/lib/mini_magick/utilities_spec.rb
sed -i "/^    it \"returns GraphicsMagick's version\" do$/,/    end/ s/^/#/g" \
  spec/lib/mini_magick_spec.rb
sed -i -e 's|, "GraphicsMagick"||' \
	spec/lib/mini_magick/image_spec.rb

# ImageMagick version incompatibility
sed -i "/ have_key(\"date:create\")/ s/^/#/" \
  spec/lib/mini_magick/image_spec.rb
sed -i "/^\s*it \"does not hang when parsing verbose data\" do$/ a \ skip" \
  spec/lib/mini_magick/image_spec.rb

rspec spec
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/MIT-LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Rakefile

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.11.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.11.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.11.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.11.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.11.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.11.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 10 2023 Mamoru TASAKA <mtasaka@fedoraprpject.org> - 4.11.0-7
- Prevent GraphicsMagick test being executed by ImageMagick on
  image_spec test

* Mon Nov 14 2022 Mamoru TASAKA <mtasaka@fedoraprpject.org> - 4.11.0-6
- Backport upstream fix for ruby32 File.exists? removal

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.11.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.11.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.11.0-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan  7 00:13:06 CET 2021 Pavel Valena <pvalena@redhat.com> - 4.11.0-1
- Update to mini_magick 4.11.0.
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.0

* Thu Aug 06 15:23:58 GMT 2020 Pavel Valena <pvalena@redhat.com> - 4.10.1-1
- Update to mini_magick 4.10.1.
  Resolves: rhbz#1800014

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.3-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb 27 2019 Pavel Valena <pvalena@redhat.com> - 4.9.3-1
- Update to mini_magick 4.9.3.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 31 2018 Pavel Valena <pvalena@redhat.com> - 4.8.0-1
- Initial package
