Vendor:         Microsoft Corporation
Distribution:   Mariner
%global git0 https://github.com/rootless-containers/%{name}
%global commit0 4367de7c3361c344155220a4e999ffd7432dad81
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

# Used for comparing with latest upstream tag
# to decide whether to autobuild (non-rawhide only)
%define built_tag v1.1.8
%define built_tag_strip %(b=%{built_tag}; echo ${b:1})
%define download_url %{git0}/archive/%{built_tag}.tar.gz

Name: slirp4netns
Version: 1.1.8
Release: 3%{?dist}
# no go-md2man in ppc64
ExcludeArch: ppc64
Summary: slirp for network namespaces
License: GPLv2
URL: %{git0}
Source0: %{download_url}#/%{name}-%{version}.tar.gz
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc
BuildRequires: glib2-devel
BuildRequires: git
BuildRequires: go-md2man
BuildRequires: libcap-devel
BuildRequires: libseccomp-devel
BuildRequires: libslirp-devel
BuildRequires: make

%description
slirp for network namespaces, without copying buffers across the namespaces.

%package devel
Summary: %{summary}
BuildArch: noarch

%description devel
%{summary}

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.

%prep
%autosetup -Sgit -n %{name}-%{built_tag_strip}

%build
./autogen.sh
./configure --prefix=%{_usr} --libdir=%{_libdir}
%{__make} generate-man

%install
make DESTDIR=%{buildroot} install install-man

%check

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz

%changelog
* Tue Nov 01 2022 Ameya Usgaonkar <ausgaonkar@microsoft.com> - 1.1.8-3
- Move to core packages

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.8-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Dec  3 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.1.8-1
- autobuilt v1.1.8

* Wed Nov 25 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.1.7-1
- autobuilt v1.1.7

* Thu Nov  5 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.1.6-1
- autobuilt v1.1.6

* Wed Sep  2 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.1.4-1
- autobuilt v1.1.4

* Tue Aug 25 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.1.4-2
- rebuild for centos8

* Mon Jul 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.1.4-1
- autobuilt v1.1.4

* Tue Jul 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.1.2-1
- autobuilt v1.1.2

* Fri Jun 05 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.1.1-1
- autobuilt v1.1.1

* Thu Jun 04 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.1.0-1
- autobuilt v1.1.0

* Tue Jun 02 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.1.0-0.3.beta.2
- use correct beta tag

* Tue Jun 02 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.1.0-0.3.beta.1
- autobuilt v1.1.0-beta.2

* Sun May 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.0.1-0.2.beta.1
- autobuilt v1.1.0-beta.1

* Mon Apr 27 2020 Dan Walsh <dwalsh@fedoraproject.org> - 1.0.1-1.git4367de7
- bump to 1.0.1

* Fri Apr 03 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-1
- built v1.0.0

* Mon Mar 23 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-0.1.beta.0
- built v1.0.0-beta.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.3-6.0.dev.gita8414d1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Dec 18 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.4.3-5.0.dev.gita8414d1
- autobuilt a8414d1

* Wed Dec 18 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.4.3-4.0.dev.gite6b31fe
- autobuilt e6b31fe

* Fri Dec 13 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.4.3-3.0.dev.gitdad442a
- autobuilt dad442a

* Thu Dec 12 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.4.3-2.0.dev.gite14da48
- bump to 0.4.3
- autobuilt e14da48

* Wed Dec 11 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.4.2-6.0.dev.git1fea75f
- autobuilt 1fea75f

* Thu Nov 21 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.4.2-5.0.dev.git21fdece
- autobuilt 21fdece

* Mon Nov 04 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.4.2-4.0.dev.git0186bac
- autobuilt 0186bac

* Thu Oct 31 2019 Jindrich Novy <jnovy@redhat.com> - 0.4.2-3.0.dev.git3527c98
- add BR: libseccomp-devel

* Fri Oct 18 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.4.2-2.0.dev.git3527c98
- bump to 0.4.2
- autobuilt 3527c98

* Wed Oct 02 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.4.1-3.0.dev.gite8759b9
- autobuilt e8759b9

* Fri Aug 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.1-2.0.dev.gitf9503fe
- bump to 0.4.1
- autobuilt f9503fe

* Fri Aug 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.0-25.1.dev.gitd2e449b
- autobuilt d2e449b

* Thu Aug 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.0-24.1.dev.git1a96e26
- autobuilt 1a96e26

* Sun Aug 25 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.0-23.1.dev.git29db6bd
- autobuilt 29db6bd

* Fri Aug 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.0-22.1.dev.git4e51172
- autobuilt 4e51172

* Wed Aug 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.0-21.1.dev.git56c8370
- autobuilt 56c8370

* Sun Aug 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.0-20.1.dev.gitbbd6f25
- autobuilt bbd6f25

* Thu Aug 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.0-19.1.dev.gited51817
- autobuilt ed51817

* Tue Jul 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.0-18.1.dev.gitaacef69
- autobuilt aacef69

* Tue Jul 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.0-17.1.dev.git1dfc6f6
- autobuilt 1dfc6f6

* Sun Jul 28 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.0-16.1.dev.git96ff33c
- autobuilt 96ff33c

* Sat Jul 27 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.0-15.1.dev.gitb911c9a
- autobuilt b911c9a

* Sat Jul 27 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.0-14.1.dev.gitd23723e
- autobuilt d23723e

* Fri Jul 26 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.0-13.1.dev.git10c0ee5
- autobuilt 10c0ee5

* Thu Jul 25 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.0-12.1.dev.git87a4bf7
- autobuilt 87a4bf7

* Wed Jul 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.0-11.1.dev.git85efff0
- autobuilt 85efff0

* Wed Jul 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.0-10.1.dev.git4f5a083
- autobuilt 4f5a083

* Tue Jul 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.0-9.1.dev.git62cbdd3
- bump to 0.4.0
- autobuilt 62cbdd3

* Tue Jul 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.3.0-8.1.dev.gitbf199bb
- autobuilt bf199bb

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.3.0-7.1.dev.git2f857ec
- autobuilt 5c690f7
- autobuilt 2f857ec

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.3.0-6.1.dev.gitd34e916
- autobuilt 5c690f7
- autobuilt d34e916

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.3.0-5.1.dev.git6612517
- autobuilt 5c690f7
- autobuilt 6612517

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.3.0-4.1.dev.gitf34ad90
- autobuilt 5c690f7
- autobuilt f34ad90

* Sun Jul 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.3.0-3.1.dev.git5c690f7
- autobuilt 5c690f7

* Wed Jul 10 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.3.0-2.1.dev.git4889f52
- built 4889f52
- hook up to autobuild

* Wed May 15 2019 Dan Walsh <dwalsh@fedoraproject.org> - v0.3.0-2
- Update to released version

* Wed Feb 27 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.3.0-1.alpha.2
- make version tag consistent with upstream

* Sun Feb 17 2019 Dan Walsh <dwalsh@fedoraproject.org> - v0.3.0-alpha.2
- Latest release

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1-3.dev.git0037042
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 20 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1-2.dev.git0037042
- built 0037042

* Fri Jul 27 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1-1.dev.gitc4e1bc5
- Resolves: #1609595 - initial upload
- First package for Fedora
