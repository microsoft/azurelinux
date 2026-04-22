# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global src_name GitLab-API-v4


Name:           perl-%{src_name}
Version:        0.27
Release: 9%{?dist}
Summary:        Complete GitLab API v4 client

# Automatically converted from old format: GPL+ or Artistic - review is highly recommended.
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/%{src_name}

# Doesn't work.  :(
# Source0:      https://www.cpan.org/modules/by-module/GitLab/%%{src_name}-%%{version}.tar.gz
Source0:        https://cpan.metacpan.org/authors/id/B/BL/BLUEFEET/%{src_name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  coreutils
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.8.0
BuildRequires:  perl(Carp)
BuildRequires:  perl(Const::Fast)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(HTTP::Tiny)
BuildRequires:  perl(HTTP::Tiny::Multipart)
BuildRequires:  perl(IO::Prompter)
BuildRequires:  perl(IPC::Cmd)
BuildRequires:  perl(JSON::MaybeXS)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Log::Any)
BuildRequires:  perl(Log::Any::Adapter)
BuildRequires:  perl(Log::Any::Adapter::Screen)
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(Module::Build::Tiny) >= 0.035
BuildRequires:  perl(Moo)
BuildRequires:  perl(Path::Tiny)
BuildRequires:  perl(Pod::Usage)
BuildRequires:  perl(Test2::Require::AuthorTesting)
BuildRequires:  perl(Test2::V0)
BuildRequires:  perl(Try::Tiny)
BuildRequires:  perl(Types::Common::Numeric)
BuildRequires:  perl(Types::Common::String)
BuildRequires:  perl(Types::Standard)
BuildRequires:  perl(URI)
BuildRequires:  perl(URI::Escape)
BuildRequires:  perl(YAML::XS)
BuildRequires:  perl(namespace::clean)
BuildRequires:  perl(strict)
BuildRequires:  perl(strictures) >= 2


%description
This module provides a one-to-one interface with the GitLab API v4.
Much is not documented here as it would just be duplicating GitLab's
own API Documentation.


%prep
%autosetup -n %{src_name}-%{version} -p 1


%build
perl Build.PL --installdirs=vendor
./Build


%install
./Build install --destdir=%{buildroot} --create_packlist=0
%{_fixperms} %{buildroot}/*


%check
./Build test


%files
%doc Changes README.md
%license LICENSE
%{perl_vendorlib}/*
%{_bindir}/*
%{_mandir}/man*/*


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Aug 06 2024 Miroslav Suchý <msuchy@redhat.com> - 0.27-6
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 08 2023 Björn Esser <besser82@fedoraproject.org> - 0.27-1
- 0.27 bump
  Fixes: rhbz#2213352

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.26-5
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.26-2
- Perl 5.34 rebuild

* Tue May 11 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.26-1
- 0.26 bump
- License changed from 'GPLv3+' to 'GPL+ or Artistic'

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-2
- Perl 5.32 rebuild

* Thu Feb 13 2020 Björn Esser <besser82@fedoraproject.org> - 0.25-1
- New upstream release (#1802340)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.23-1
- New upstream release (#1763344)

* Wed Oct 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.22-1
- New upstream release (#1752080)

* Thu Aug 29 2019 Björn Esser <besser82@fedoraproject.org> - 0.21-1
- New upstream release (#1747004)

* Wed Jul 24 2019 Björn Esser <besser82@fedoraproject.org> - 0.20-1
- New upstream release (#1732684)

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.19-3
- Perl 5.30 rebuild

* Sat May 18 2019 Björn Esser <besser82@fedoraproject.org> - 0.19-2
- License changed to GPLv3+

* Sat May 18 2019 Björn Esser <besser82@fedoraproject.org> - 0.19-1
- New upstream release (#1711471)

* Thu Apr 04 2019 Björn Esser <besser82@fedoraproject.org> - 0.18-1
- New upstream release (#1696124)

* Mon Feb 25 2019 Björn Esser <besser82@fedoraproject.org> - 0.17-1
- Bump release to stable (#1680372)

* Sun Feb 24 2019 Björn Esser <besser82@fedoraproject.org> - 0.17-0.3
- Changes as suggested in review (#1680372)
- Add a set of explicit BuildRequires

* Sun Feb 24 2019 Björn Esser <besser82@fedoraproject.org> - 0.17-0.2
- Add explicit perl module compat requires

* Sun Feb 24 2019 Björn Esser <besser82@fedoraproject.org> - 0.17-0.1
- Initial rpm release (#1680372)
