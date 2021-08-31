%define debug_package %{nil}

Summary:        CRI tools
Name:           cri-tools
Version:        1.21.0
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://github.com/kubernetes-sigs/cri-tools
#Source0:       https://github.com/kubernetes-sigs/cri-tools/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Source1:        crictl.yaml

BuildRequires:  golang

%description
cri-tools aims to provide a series of debugging and validation tools for Kubelet CRI, which includes:
crictl: CLI for kubelet CRI.
critest: validation test suites for kubelet CRI.

%prep
%setup -qn %{name}-%{version}

%build
make %{?_smp_mflags}


%install
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_lib}/.build-id
mkdir -p %{buildroot}%{_docdir}/cri-tools
mkdir -p %{buildroot}%{_datadir}/licenses/cri-tools
mkdir -p %{buildroot}/man/man1
mkdir -p %{buildroot}%{_sysconfdir}

make install DESTDIR=%{buildroot} BINDIR=%{_bindir}
cp CHANGELOG.md %{buildroot}%{_docdir}/cri-tools
cp LICENSE %{buildroot}%{_datadir}/licenses/cri-tools
cp CHANGELOG.md %{buildroot}%{_docdir}/cri-tools
cp CONTRIBUTING.md %{buildroot}%{_docdir}/cri-tools
cp OWNERS %{buildroot}%{_docdir}/cri-tools
cp README.md %{buildroot}%{_docdir}/cri-tools
cp code-of-conduct.md %{buildroot}%{_docdir}/cri-tools
cp docs/validation.md %{buildroot}%{_docdir}/cri-tools
cp docs/roadmap.md %{buildroot}%{_docdir}/cri-tools
cp %{SOURCE1} %{buildroot}%{_sysconfdir}

%files
%defattr(-,root,root)
%license LICENSE
%{_datadir}/%{name}
%{_sysconfdir}/crictl.yaml
%{_bindir}
%{_docdir}/*
%{_datadir}/licenses/*
/man/man1/

%clean
rm -rf %{buildroot}/*

%changelog
* Thu Aug 26 2021 Vincent Nguyen <vinguyen@microsoft.com> 1.21.0-1
- update to latest crictl tool version 1.21.0.

* Tue Jun 08 2021 Henry Beberman <henry.beberman@microsoft.com> 1.11.1-8
- Increment release to force republishing using golang 1.15.13.

* Mon Apr 26 2021 Nicolas Guibourge <nicolasg@microsoft.com> 1.11.1-7
- Increment release to force republishing using golang 1.15.11.

* Thu Dec 10 2020 Andrew Phelps <anphel@microsoft.com> 1.11.1-6
- Increment release to force republishing using golang 1.15.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.11.1-5
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 1.11.1-4
- Renaming go to golang

* Thu Apr 09 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.11.1-3
- Fixed "Source0" and "URL" tags.
- License verified.
- Removed "%%define sha1".

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.11.1-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Jul 26 2018 Tapas Kundu <tkundu@vmware.com> 1.11.1-1
- Initial build added for Photon.
