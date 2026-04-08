# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from mime-types-1.16.gem by gem2rpm -*- rpm-spec -*-
%global gem_name mime-types


Summary: The mime-types library provides a library
Name: rubygem-%{gem_name}
Version: 3.4.1
Release: 7%{?dist}
License: MIT
URL: https://github.com/mime-types/ruby-mime-types/
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: rubygems-devel
BuildRequires: ruby(release)
BuildRequires: ruby >= 2.0
BuildRequires: rubygem(mime-types-data)
BuildRequires: rubygem(minitest)
BuildArch: noarch

%description
The mime-types library provides a library and registry for information about
MIME content type definitions. It can be used to determine defined filename
extensions for MIME types, or to use filename extensions to look up the likely
MIME type definitions.
Version 3.0 is a major release that requires Ruby 2.0 compatibility and
removes deprecated functions. The columnar registry format introduced
in 2.6 has been made the primary format; the registry data has been
extracted from this library and put into {mime-types-data}[https://github.com/mime-types/mime-types-data].
Additionally, mime-types is now licensed exclusively under the MIT licence and
there is a code of conduct in effect. There are a number of other smaller
changes described in the History file.

%package doc
Summary: Documentation for %{name}

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}
mv ../%{gem_name}-%{version}.gemspec .

%build
gem build %{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

# These aren't executables
find %{buildroot}%{gem_instdir}/{Rakefile,test} -type f | \
  xargs -n 1 sed -i  -e '/^#! \/usr\/bin\/env .*/d'

%check
pushd .%{gem_instdir}

# We don't have these rubygem packages in Fedora yet.
sed -i -e '/^require..minitest-bonus-assertions.$/ s/^/#/' \
    -e '/^require..minitest\/hooks.$/ s/^/#/' \
    -e '/^require..minitest\/focus.$/ s/^/#/' \
    -e '/^require..minitest\/rg.$/ s/^/#/' \
    -e '/^require..fivemat\/minitest\/autorun.$/ s/^/#/' \
  test/minitest_helper.rb

# Add assert_has_keys manually not to load minitest-bonus-assertions.
# https://github.com/halostatue/minitest-bonus-assertions/blob/v2.0/lib/minitest-bonus-assertions.rb#L53-57
cat << EOF >> test/minitest_helper.rb

def assert_has_keys obj, keys, msg = nil
  keys = [ keys ] unless keys.kind_of?(Array)
  keys.all? { |key| assert obj.key?(key) }
end
EOF

# We don't have minitest-hooks in Fedora yet.
mv test/test_mime_types_cache.rb{,.disable}

ruby -Ilib:test -rminitest/autorun -e 'Dir.glob "./test/**/test_*.rb", &method(:require)'

popd

%files
%license %{gem_instdir}/Licence.md
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_instdir}/Code-of-Conduct.md
%doc %{gem_instdir}/Contributing.md
%doc %{gem_instdir}/History.md
%doc %{gem_instdir}/README.rdoc
%{gem_instdir}/Rakefile
%{gem_instdir}/Manifest.txt
%{gem_instdir}/test
%doc %{gem_docdir}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Aug 18 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.1-1
- 3.4.1

* Sun Jul 31 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.1-7
- Backport upstream patch for YAML.safe_load behavior change
  on psych 3

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Feb 03 2020 Pavel Valena <pvalena@redhat.com> - 3.3.1-1
- Update to mime-types 3.3.1.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jul 23 2019 Pavel Valena <pvalena@redhat.com> - 3.2.2-1
- Update to mime-types 3.2.2.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul 14 2016 Jun Aruga <jaruga@redhat.com> - 3.1-1
- Update to mime-types 3.1.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 16 2014 Vít Ondruch <vondruch@redhat.com> - 1.25.1-1
- Update to mime-types 1.25.1.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 28 2013 Vít Ondruch <vondruch@redhat.com> - 1.19-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 26 2012 Vít Ondruch <vondruch@redhat.com> - 1.19-1
- Update to mime-types 1.19.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 31 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.16-7
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 08 2011 Mo Morsi <mmorsi@redhat.com> - 1.16-5
- Replace BR(check) with BR

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 30 2009 Matthew Kent <mkent@magoazul.com> - 1.16-3
- Remove needless rcov task in Rakefile causing issue (#544964).

* Sun Dec 27 2009 Matthew Kent <mkent@magoazul.com> - 1.16-2
- Fix license (#544964).
- Add note about rcov warning in test phase (#544964).

* Sun Dec 06 2009 Matthew Kent <mkent@magoazul.com> - 1.16-1
- Initial package
