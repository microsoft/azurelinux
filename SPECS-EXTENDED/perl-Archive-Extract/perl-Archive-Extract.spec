# Enable LZMA and XZ support via pure-Perl implementation
%if 0%{?rhel}
%bcond_with perl_Archive_Extract_enables_perl_xz
%else
%bcond_without perl_Archive_Extract_enables_perl_xz
%endif

Name:           perl-Archive-Extract
# Epoch to compete with core module from perl.spec
Version:        0.88
Release:        13%{?dist}
Summary:        Generic archive extracting mechanism
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://metacpan.org/release/Archive-Extract
Source0:        https://cpan.metacpan.org/authors/id/B/BI/BINGOS/Archive-Extract-%{version}.tar.gz#/perl-Archive-Extract-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
# Run-time:
# Prefer Archive::Tar to suppress warnings, bug #1217352, CPAN RT#104121
BuildRequires:  perl(Archive::Tar)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(deprecate)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec) >= 0.82
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(if)
BuildRequires:  perl(IPC::Cmd) >= 0.64
BuildRequires:  perl(Locale::Maketext::Simple)
BuildRequires:  perl(Module::Load::Conditional) >= 0.66
BuildRequires:  perl(Params::Check) >= 0.07
BuildRequires:  perl(vars)
# Tests:
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(File::Spec::Unix)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

Requires:       perl(deprecate)
# Prefer Archive::Tar to suppress warnings, bug #1217352, CPAN RT#104121
Requires:       perl(Archive::Tar)
Requires:       perl(File::Spec) >= 0.82
Requires:       perl(IPC::Cmd) >= 0.64
Requires:       perl(Module::Load::Conditional) >= 0.66
Requires:       perl(Params::Check) >= 0.07
# Decompressors:
Requires:       %{name}-bz2
Requires:       %{name}-gz
Requires:       %{name}-lzma
Requires:       %{name}-tar
Requires:       %{name}-tbz
Requires:       %{name}-tgz
Requires:       %{name}-txz
Requires:       %{name}-Z
Requires:       %{name}-zip
Requires:       %{name}-xz

# Filter under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((File::Spec|IPC::Cmd|Module::Load::Conditional|Params::Check)\\)$

%description
Archive::Extract is a generic archive extraction mechanism.  It allows you to
extract any archive file of the type .tar, .tar.gz, .gz, .Z, tar.bz2, .tbz,
.bz2, .zip, .xz,, .txz, .tar.xz, or .lzma without having to worry how it does
so, or use different interfaces for each type by using either perl modules, or
command-line tools on your system.

# Decompressors:
# bz2:  bunzip2 || IO::Uncompress::Bunzip2
%package bz2-bunzip2
Summary:    Bzip2 decompressor for %{name} via bunzip2
Provides:   %{name}-bz2 = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}
Requires:   bzip2
%description bz2-bunzip2
%{summary}.

%package bz2-IO-Uncompress-Bunzip2
Summary:    Bzip2 decompressor for %{name} via IO::Uncompress::Bunzip2
Provides:   %{name}-bz2 = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}
Requires:   perl(IO::Uncompress::Bunzip2)
%description bz2-IO-Uncompress-Bunzip2
%{summary}.

# gz:   gzip || Compress::Zlib
%package gz-gzip
Summary:    Gzip decompressor for %{name} via gzip
Provides:   %{name}-gz = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}
Requires:   gzip
%description gz-gzip
%{summary}.

%package gz-Compress-Zlib
Summary:    Gzip decompressor for %{name} via Compress::Zlib
Provides:   %{name}-gz = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}
Requires:   perl(Compress::Zlib)
%description gz-Compress-Zlib
%{summary}.

# lzma: unlzma || IO::Uncompress::UnLzma || Compress::unLZMA
%package lzma-unlzma
Summary:    Lzma decompressor for %{name} via unlzma
Provides:   %{name}-lzma = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}
Requires:   xz-lzma-compat
%description lzma-unlzma
%{summary}.

%if %{with perl_Archive_Extract_enables_perl_xz}
%package lzma-IO-Uncompress-UnLzma
Summary:    Lzma decompressor for %{name} via IO::Uncompress::UnLzma
Provides:   %{name}-lzma = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}
Requires:   perl(IO::Uncompress::UnLzma)
# perl-Extract-Archive-lzma-Compress-unLZMA removed because Compress::unLZMA
# is not yet packaged
Obsoletes:  perl-Archive-Extract-lzma-Compress-unLZMA < 1:0.80-8
%description lzma-IO-Uncompress-UnLzma
%{summary}.
%endif

%if %{with perl_Archive_Extract_enables_perl_xz}
# Compress::unLZMA not yet packaged
#%%package lzma-Compress-unLZMA
#Summary:    Lzma decompressor for %%{name} via Compress::unLZMA
#Provides:   %%{name}-lzma = %%{version}-%%{release}
#Requires:   %%{name} = %%{version}-%%{release}
#Requires:   perl(Compress::unLZMA)
#%%description lzma-Compress-unLZMA
#%%{summary}.
%endif

# tar:  tar || Archive::Tar
%package tar-tar
Summary:    Tar decompressor for %{name} via tar
Provides:   %{name}-tar = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}
Requires:   tar
%description tar-tar
%{summary}.

%package tar-Archive-Tar
Summary:    Tar decompressor for %{name} via Archive::Tar
Provides:   %{name}-tar = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}
Requires:   perl(Archive::Tar)
%description tar-Archive-Tar
%{summary}.

# tbz:  (tar && bunzip2) || (Archive::Tar && IO::Uncompress::Bunzip2)
%package tbz-tar-bunzip2
Summary:    Bzipped-tar decompressor for %{name} via tar an bunzip2
Provides:   %{name}-tbz = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}
Requires:   tar
Requires:   bzip2
%description tbz-tar-bunzip2
%{summary}.

%package tbz-Archive-Tar-IO-Uncompress-Bunzip2
Summary:    Bzipped-tar decompressor for %{name} via Archive::Tar and IO::Uncompress::Bunzip2
Provides:   %{name}-tbz = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}
Requires:   perl(Archive::Tar)
Requires:   perl(IO::Uncompress::Bunzip2)
%description tbz-Archive-Tar-IO-Uncompress-Bunzip2
Bzipped-tar decompressor for %{name} via Archive::Tar and
IO::Uncompress::Bunzip2.

# tgz:  (tar && gzip) || (Archive::Tar && (Compress::Zlib || IO::Zlib))
%package tgz-tar-gzip
Summary:    Gzipped-tar decompressor for %{name} via tar and gzip
Provides:   %{name}-tgz = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}
Requires:   tar
Requires:   gzip
%description tgz-tar-gzip
%{summary}.

%package tgz-Archive-Tar-Compress-Zlib
Summary:    Gzipped-tar decompressor for %{name} via Archive::Tar and Compress::Zlib
Provides:   %{name}-tgz = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}
Requires:   perl(Archive::Tar)
Requires:   perl(Compress::Zlib)
%description tgz-Archive-Tar-Compress-Zlib
Gzipped-tar decompressor for %{name} via Archive::Tar and
Compress::Zlib.

%package tgz-Archive-Tar-IO-Zlib
Summary:    Gzipped-tar decompressor for %{name} via Archive::Tar and IO::Zlib
Provides:   %{name}-tgz = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}
Requires:   perl(Archive::Tar)
Requires:   perl(IO::Zlib)
%description tgz-Archive-Tar-IO-Zlib
%{summary}.

# txz:  (tar && unxz) || (Archive::Tar && IO::Uncompress::UnXz)
%package txz-tar-unxz
Summary:    Xzed-tar decompressor for %{name} via tar and unxz
Provides:   %{name}-txz = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}
Requires:   tar
Requires:   xz
%description txz-tar-unxz
%{summary}.

%if %{with perl_Archive_Extract_enables_perl_xz}
%package txz-Archive-Tar-IO-Uncompress-UnXz
Summary:    Xzed-tar decompressor for %{name} via Archive::Tar and IO::Uncompress::UnXz
Provides:   %{name}-txz = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}
Requires:   perl(Archive::Tar)
Requires:   perl(IO::Uncompress::UnXz)
%description txz-Archive-Tar-IO-Uncompress-UnXz
Xzed-tar decompressor for %{name} via Archive::Tar and
IO::Uncompress::UnXz.
%endif

# Z:    uncompress || Compress::Zlib
%package Z-uncompress
Summary:    Z decompressor for %{name} via uncompress
Provides:   %{name}-Z = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}
Requires:   ncompress
%description Z-uncompress
%{summary}.

%package Z-Compress-Zlib
Summary:    Z decompressor for %{name} via Compress::Zlib
Provides:   %{name}-Z = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}
Requires:   perl(Compress::Zlib)
%description Z-Compress-Zlib
%{summary}.

# zip:  unzip || Archive::Zip
%package zip-unzip
Summary:    ZIP decompressor for %{name} via unzip
Provides:   %{name}-zip = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}
Requires:   unzip
%description zip-unzip
%{summary}.

%package zip-Archive-Zip
Summary:    ZIP decompressor for %{name} via Archive::Zip
Provides:   %{name}-zip = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}
Requires:   perl(Archive::Zip)
%description zip-Archive-Zip
%{summary}.

# xz:   unxz || IO::Uncompress::UnXz
%package xz-unxz
Summary:    Xz decompressor for %{name} via unxz
Provides:   %{name}-xz = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}
Requires:   xz
%description xz-unxz
%{summary}.

%if %{with perl_Archive_Extract_enables_perl_xz}
%package xz-IO-Uncompress-UnXz
Summary:    Xz decompressor for %{name} via IO::Uncompress::UnXz
Provides:   %{name}-xz = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}
Requires:   perl(IO::Uncompress::UnXz)
%description xz-IO-Uncompress-UnXz
%{summary}.
%endif

%prep
%setup -q -n Archive-Extract-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc CHANGES README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files bz2-bunzip2
%files bz2-IO-Uncompress-Bunzip2
%files gz-gzip
%files gz-Compress-Zlib
%files lzma-unlzma
%if %{with perl_Archive_Extract_enables_perl_xz}
%files lzma-IO-Uncompress-UnLzma
%endif
%if %{with perl_Archive_Extract_enables_perl_xz}
#%%files lzma-Compress-unLZMA
%endif
%files tar-tar
%files tar-Archive-Tar
%files tbz-tar-bunzip2
%files tbz-Archive-Tar-IO-Uncompress-Bunzip2
%files tgz-tar-gzip
%files tgz-Archive-Tar-Compress-Zlib
%files tgz-Archive-Tar-IO-Zlib
%files txz-tar-unxz
%if %{with perl_Archive_Extract_enables_perl_xz}
%files txz-Archive-Tar-IO-Uncompress-UnXz
%endif
%files Z-uncompress
%files Z-Compress-Zlib
%files zip-unzip
%files zip-Archive-Zip
%files xz-unxz
%if %{with perl_Archive_Extract_enables_perl_xz}
%files xz-IO-Uncompress-UnXz
%endif

%changelog
* Fri Dec 20 2024 Jyoti kanase <v-jykanase@microsoft.com> -  0.88 - 13
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.88-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.88-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.88-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.88-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.88-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Oct 25 2022 Michal Josef Špaček <mspacek@redhat.com> - 1:0.88-7
- Update license to SPDX

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.88-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.88-5
- Perl 5.36 rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.88-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.88-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.88-2
- Perl 5.34 rebuild

* Thu May 06 2021 Michal Josef Špaček <mspacek@redhat.com> - 1:0.88-1
- 0.88 bump

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.86-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.86-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.86-3
- Perl 5.32 rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.86-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 10 2019 Petr Pisar <ppisar@redhat.com> - 1:0.86-1
- 0.86 bump

* Thu Dec 05 2019 Petr Pisar <ppisar@redhat.com> - 1:0.84-1
- 0.84 bump

* Mon Nov 25 2019 Petr Pisar <ppisar@redhat.com> - 1:0.82-1
- 0.82 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.80-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.80-10
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.80-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Sep 06 2018 Petr Pisar <ppisar@redhat.com> - 1:0.80-8
- Remove perl-Extract-Archive-lzma-Compress-unLZMA subpackage because
  Compress::unLZMA is not packaged

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.80-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.80-6
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.80-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.80-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.80-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.80-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 19 2017 Petr Pisar <ppisar@redhat.com> - 1:0.80-1
- 0.80 bump

* Fri Jul 29 2016 Petr Pisar <ppisar@redhat.com> - 1:0.78-1
- 0.78 bump

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.76-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.76-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 07 2015 Petr Pisar <ppisar@redhat.com> - 1:0.76-1
- 0.76 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.74-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.74-4
- Perl 5.22 rebuild

* Thu Apr 30 2015 Petr Pisar <ppisar@redhat.com> - 1:0.74-3
- Fix a typo, unxz is provided by xz

* Thu Apr 30 2015 Petr Pisar <ppisar@redhat.com> - 1:0.74-2
- Prefer Archive::Tar (bug #1217352)

* Fri Nov 21 2014 Petr Pisar <ppisar@redhat.com> - 1:0.74-1
- 0.74 bump

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:0.72-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.72-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 30 2014 Petr Pisar <ppisar@redhat.com> - 1:0.72-1
- 0.72 bump

* Mon Nov 18 2013 Petr Pisar <ppisar@redhat.com> - 1:0.70-1
- 0.70 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.68-291
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 1:0.68-290
- Increase release to favour standalone package

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1:0.68-3
- Perl 5.18 rebuild

* Tue May 28 2013 Petr Pisar <ppisar@redhat.com> - 1:0.68-2
- Correct typo in dependencies

* Fri Mar 15 2013 Petr Pisar <ppisar@redhat.com> - 1:0.68-1
- 0.68 bump

* Mon Feb 11 2013 Petr Pisar <ppisar@redhat.com> 0.66-1
- Specfile autogenerated by cpanspec 1.78.
