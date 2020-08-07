Summary:    Converts markdown into roff (man pages)
Name:       go-md2man
Version:    2.0.0
Release:    4%{?dist}
License:    MIT
Group:      Tools/Container

#Source0:       https://github.com/cpuguy83/go-md2man/archive/v2.0.0.tar.gz
Source0:        go-md2man-2.0.0.tar.gz
URL:            https://github.com/cpuguy83/go-md2man
Vendor:         Microsoft Corporation
Distribution:   Mariner

BuildRequires: golang
BuildRequires: which

# required packages on install
Requires: /bin/sh

Provides:       golang-github-cpuguy83-md2man

%description
Converts markdown into roff (man pages)

%define OUR_GOPATH %{_topdir}/.gopath

%prep
%setup -q -n %{name}-%{version} -c

%build
export GOPATH=%{OUR_GOPATH}
export GOCACHE=%{OUR_GOPATH}/.cache
export CGO_ENABLED=0
export GO111MODULE=on

cd %{_topdir}/BUILD/%{name}-%{version}/go-md2man-2.0.0
go build -mod vendor -o go-md2man

%install
mkdir -p "%{buildroot}%{_bindir}"
cp -aT go-md2man-2.0.0/go-md2man %{buildroot}%{_bindir}/go-md2man

# copy legal files
mkdir -p %{buildroot}/usr/share/doc/%{name}-%{version}
cp go-md2man-2.0.0/LICENSE.md %{buildroot}/usr/share/doc/%{name}-%{version}/LICENSE.md

%files
%license /usr/share/doc/%{name}-%{version}/LICENSE.md
%{_bindir}/go-md2man

%changelog
* Wed May 20 2020 Joe Schmitt <joschmit@microsoft.com> 2.0.0-4
- Remove reliance on existing GOPATH environment variable.
* Sat May 09 00:21:37 PST 2020 Nick Samson <nisamson@microsoft.com> - 2.0.0-3
- Added %%license line automatically
* Fri May 01 2020 Emre Girgin <mrgirgin@microsoft.com> 2.0.0-2
- Renaming go to golang
* Fri Apr 03 2020 Mohan Datla <mdatla@microsoft.com> 2.0.0-1
- Original version for CBL-Mariner.
