Vendor:         Microsoft Corporation
Distribution:   Mariner
%global gem_name pry

Name: rubygem-%{gem_name}
Version: 0.13.1
Release: 3%{?dist}
Summary: An IRB alternative and runtime developer console
License: MIT
URL: https://pry.github.io/
Source0: https://github.com/pry/pry/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires: git
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(bundler)
BuildRequires: rubygem-coderay >= 1.1.0
BuildRequires: rubygem-method_source >= 0.8.1
BuildRequires: rubygem(rspec)
# editor specs fail if no editor is available (soft requirement)
BuildRequires: vi
# https://github.com/pry/pry/pull/1498
Provides: bundled(rubygem-slop) = 3.4.0
BuildArch: noarch

%description
Pry is a runtime developer console and IRB alternative with powerful
introspection capabilities. Pry aims to be more than an IRB replacement. It is
an attempt to bring REPL driven programming to the Ruby language.

%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/
#add lib files to buildroot from Source0
cp -a lib/ %{buildroot}%{gem_instdir}/
#add CHANGELOG, README and License files to buildroot from Source0
cp CHANGELOG.md %{buildroot}%{gem_instdir}/
cp README.md %{buildroot}%{gem_instdir}/
cp LICENSE %{buildroot}%{gem_instdir}/

mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
pushd .%{gem_instdir}
ln -s %{_builddir}/spec spec

# Rakefile is used by editor test.
touch Rakefile

# Original test suite is run from non-versioned directory:
# https://github.com/pry/pry/blob/9d9ae4a0b0bd487bb41170c834b3fa417e161f23/spec/cli_spec.rb#L219
sed -i '/pry\/foo/ s/pry/pry-%{version}/' spec/cli_spec.rb

# The bundler is required just to make /spec/integration/bundler_spec.rb pass.
RUBYOPT=-rbundler rspec -rspec_helper spec
popd

%files
%dir %{gem_instdir}
%{_bindir}/pry
%license %{gem_instdir}/LICENSE
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md

%changelog
* Tue Mar 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 0.13.1-3
- License verified.
- Build from .tar.gz source.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.13.1-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Apr 20 2020 Vít Ondruch <vondruch@redhat.com> - 0.13.1-1
- Update to Pry 0.13.1.
  Resolves: rhbz#1493806
  Resovles: rhbz#1800023

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 24 2017 Vít Ondruch <vondruch@redhat.com> - 0.10.4-2
- Fix Ruby 2.4 compatibility.

* Fri Oct 14 2016 Vít Ondruch <vondruch@redhat.com> - 0.10.4-1
- Update to Pry 0.10.4.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Dec 09 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.10.1-1
- Update to latest upstream release (RHBZ #1108177)
- Remove gem2rpm auto-generated comment
- Update URL to latest upstream location
- Add generate-test-tarball.sh script since upstream no longer ships the tests
- Adjustments for https://fedoraproject.org/wiki/Changes/Ruby_2.1
- Use gem unpack / setup / build per Ruby packaging guidelines
- Use %%license tag

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.12.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 03 2014 Vít Ondruch <vondruch@redhat.com> - 0.9.12.6-1
- Update to Pry 0.9.12.6.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.9.12-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Updated to Pry 0.9.12.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jul 31 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.9.10-1
- Initial package
