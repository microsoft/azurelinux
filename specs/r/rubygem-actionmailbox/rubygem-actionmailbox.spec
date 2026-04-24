# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name actionmailbox

Name: rubygem-%{gem_name}
Version: 8.0.2
Release: 3%{?dist}
Summary: Inbound email handling framework
License: MIT
URL: https://rubyonrails.org
Source0: https://rubygems.org/gems/%{gem_name}-%{version}%{?prerelease}.gem
# git clone http://github.com/rails/rails.git && cd rails/actionmailbox
# git archive -v -o actionmailbox-8.0.2-tests.tar.gz v8.0.2 test/
Source1: actionmailbox-%{version}%{?prerelease}-tests.tar.gz

BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 3.2.0
BuildRequires: rubygem(actionmailer) = %{version}
BuildRequires: rubygem(activerecord) = %{version}
BuildRequires: rubygem(activestorage) = %{version}
BuildRequires: rubygem(bundler)
BuildRequires: rubygem(railties) = %{version}
BuildRequires: rubygem(sqlite3)
BuildRequires: rubygem(webmock)
BuildArch: noarch

%description
Receive and process incoming emails in Rails applications.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}%{?prerelease} -b1

%build
gem build ../%{gem_name}-%{version}%{?prerelease}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
( cd .%{gem_instdir}/
cp -a %{_builddir}/test .

mkdir ../tools
# Fake test_common.rb. It does not provide any functionality besides
# `force_skip` alias.
touch ../tools/test_common.rb
# Netiher strict_warnings.rb appears to be useful.
touch ../tools/strict_warnings.rb

export BUNDLE_GEMFILE=${PWD}/../Gemfile

cat > $BUNDLE_GEMFILE <<EOF
gem "railties"
gem "actionmailer"
gem "activerecord"
gem "activestorage"
gem "sqlite3"
gem "webmock"
EOF

# Remove asset pipeline initializer
echo > test/dummy/config/initializers/assets.rb

ruby -Itest -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
)

%files
%dir %{gem_instdir}
%license %{gem_instdir}/MIT-LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/app
%{gem_instdir}/config
%{gem_instdir}/db
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 09 2025 Vít Ondruch <vondruch@redhat.com> - 8.0.2-1
- Update to Action Mailbox 8.0.2.
  Related: rhbz#2238177

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Sep 10 2023 Pavel Valena <pvalena@redhat.com> - 7.0.8-1
- Update to actionmailbox 7.0.8.

* Mon Aug 28 2023 Pavel Valena <pvalena@redhat.com> - 7.0.7.2-1
- Update to actionmailbox 7.0.7.2.

* Thu Aug 10 2023 Pavel Valena <pvalena@redhat.com> - 7.0.7-1
- Update to actionmailbox 7.0.7.

* Sun Jul 23 2023 Pavel Valena <pvalena@redhat.com> - 7.0.6-1
- Update to actionmailbox 7.0.6.

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 30 2023 Pavel Valena <pvalena@redhat.com> - 7.0.5-1
- Update to actionmailbox 7.0.5.

* Tue Mar 14 2023 Pavel Valena <pvalena@redhat.com> - 7.0.4.3-1
- Update to actionmailbox 7.0.4.3.

* Wed Jan 25 2023 Pavel Valena <pvalena@redhat.com> - 7.0.4.2-1
- Update to actionmailbox 7.0.4.2.

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Sep 15 2022 Pavel Valena <pvalena@redhat.com> - 7.0.4-1
- Update to actionmailbox 7.0.4.

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Mar 14 2022 Pavel Valena <pvalena@redhat.com> - 7.0.2.3-1
- Update to actionmailbox 7.0.2.3.

* Wed Feb 09 2022 Pavel Valena <pvalena@redhat.com> - 7.0.2-1
- Update to actionmailbox 7.0.2.

* Thu Feb 03 2022 Pavel Valena <pvalena@redhat.com> - 7.0.1-1
- Update to actionmailbox 7.0.1.

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Sep 17 2021 Pavel Valena <pvalena@redhat.com> - 6.1.4.1-1
- Update to actionmailbox 6.1.4.1.

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 30 2021 Pavel Valena <pvalena@redhat.com> - 6.1.4-1
- Update to actionmailbox 6.1.4.

* Tue May 18 2021 Pavel Valena <pvalena@redhat.com> - 6.1.3.2-1
- Update to actionmailbox 6.1.3.2.

* Fri Apr 09 2021 Pavel Valena <pvalena@redhat.com> - 6.1.3.1-1
- Update to actionmailbox 6.1.3.1.

* Thu Feb 18 2021 Pavel Valena <pvalena@redhat.com> - 6.1.3-1
- Update to actionmailbox 6.1.3.

* Mon Feb 15 2021 Pavel Valena <pvalena@redhat.com> - 6.1.2.1-1
- Update to actionmailbox 6.1.2.1.

* Wed Jan 27 2021 Pavel Valena <pvalena@redhat.com> - 6.1.1-1
- Update to actionmailbox 6.1.1.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct  8 12:00:49 CEST 2020 Pavel Valena <pvalena@redhat.com> - 6.0.3.4-1
- Update to actionmailbox 6.0.3.4.
  Resolves: rhbz#1877507

* Tue Sep 22 01:15:13 CEST 2020 Pavel Valena <pvalena@redhat.com> - 6.0.3.3-1
- Update to actionmailbox 6.0.3.3.
  Resolves: rhbz#1877507

* Mon Aug 17 05:14:02 GMT 2020 Pavel Valena <pvalena@redhat.com> - 6.0.3.2-1
- Update to actionmailbox 6.0.3.2.

* Mon Aug 03 07:01:37 GMT 2020 Pavel Valena <pvalena@redhat.com> - 6.0.3.1-1
- Initial package: ActionMailbox 6.0.3.1.
