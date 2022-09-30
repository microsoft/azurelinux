%global gem_name mustache
Summary:        Mustache is a framework-agnostic way to render logic-free views
Name:           rubygem-%{gem_name}
Version:        1.1.1
Release:        4%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/mustache/mustache
Source0:        https://github.com/mustache/mustache/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
# Fix test race condition.
# https://github.com/mustache/mustache/pull/258
Patch0:         rubygem-mustache-1.1.1-Fix-test-race-condition.patch
BuildRequires:  ruby(release)
BuildRequires:  rubygems-devel
BuildRequires:  ruby
BuildRequires:  rubygem-minitest
BuildArch:      noarch

%description
Inspired by ctemplate, Mustache is a framework-agnostic way to render
logic-free views.

As ctemplates says, "It emphasizes separating logic from presentation:
it is impossible to embed application logic in this template
language.

Think of Mustache as a replacement for your views. Instead of views
consisting of ERB or HAML with random helpers and arbitrary logic,
your views are broken into two parts: a Ruby class and an HTML
template.

%package       doc
Summary:       Documentation for %{name}
Requires:      %{name} = %{version}-%{release}
BuildArch:     noarch

%description doc
Documentation for %{name}.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
gem build %{gem_name}

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# Install man pages
mkdir -p %{buildroot}%{_mandir}/man5
cp -a .%{gem_instdir}/man/mustache.5 %{buildroot}%{_mandir}/man5
mkdir -p %{buildroot}%{_mandir}/man1
cp -a .%{gem_instdir}/man/mustache.1 %{buildroot}%{_mandir}/man1

# Install documentation
cp -a .%{gem_instdir}/man/*.html .

%check
pushd .%{gem_instdir}
# Code coverage is not really interesting for Fedora.
sed -i '/simplecov/,/^end$/ s/^/#/' test/helper.rb

# UTF8 environment has to be set.
# https://github.com/mustache/mustache/issues/208
LANG=C.UTF-8 ruby -Ilib -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%doc *.html
%{_bindir}/mustache
%license %{gem_instdir}/LICENSE
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_instdir}/man
%doc %{_mandir}/man1/*
%doc %{_mandir}/man5/*
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/test

%changelog
* Wed Sep 28 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.1.1-4
- Cleanup SPEC file and move to SPECS directory from Extended.

* Tue Mar 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.1.1-3
- License verified.
- Build from .tar.gz source.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.1-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Apr 27 2020 Vít Ondruch <vondruch@redhat.com> - 1.1.1-1
- Update to Mustache 1.1.1.
  Resolves: rhbz#1321203
  Resolves: rhbz#1800018

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.0.2-7
- Use C.UTF-8 locale
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 25 2015 Vít Ondruch <vondruch@redhat.com> - 1.0.2-1
- Update to Mustache 1.0.2.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 20 2014 Vít Ondruch <vondruch@redhat.com> - 0.99.5-1
- Update to Mustache 0.99.5.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 04 2013 Vít Ondruch <vondruch@redhat.com> - 0.99.4-8
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Sep 20 2012 Vít Ondruch <vondruch@redhat.com> - 0.99.4-6
- Fix mustache executable for Ruby 1.9.3 (rhbz#859025).

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 17 2012 Vít Ondruch <vondruch@redhat.com> - 0.99.4-4
- Compatibility fixes with older Fedoras and RHELs.
- Add missing .gemspec.

* Fri Jan 20 2012 Vít Ondruch <vondruch@redhat.com> - 0.99.4-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 27 2011 Vít Ondruch <vondruch@redhat.com> - 0.99.4-1
- Update to Mustache 0.99.4
- Dropped optional Sinatra dependency.
- Removed deprecated %%clean section.
- Added man pages.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 10 2010 Jozef Zigmund <jzigmund@redhat.com> - 0.11.2-4
- Corrected ruby(abi) require

* Mon Nov 8 2010 Jozef Zigmund <jzigmund@redhat.com> - 0.11.2-3
- Added README.md, LICENSE with macro doc
- Replaced macro {gemdir}/gems/{gemname}-{version}/ by macro dir {geminstdir}
- Added lib, bin to macro {geminstdir}
- Added subpackage doc with folders: man, test and doc

* Mon Oct 18 2010 Jozef Zigmund <jzigmund@redhat.com> - 0.11.2-2
- Repair URL Source0
- Remove "Mustache is a" from Summary
- Add Require: rubygem(sinatra)

* Mon Oct 18 2010 Jozef Zigmund <jzigmund@redhat.com> - 0.11.2-1
- Initial package
