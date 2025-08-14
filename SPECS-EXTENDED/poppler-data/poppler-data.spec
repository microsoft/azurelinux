Summary:        Encoding files for use with poppler
Name:           poppler-data
Version:        0.4.11
Release:        1%{?dist}
License:        (GPL-2.0-only OR GPL-3.0-only) AND BSD-3-Clause
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Libraries
URL:            https://poppler.freedesktop.org/
Source0:        https://poppler.freedesktop.org/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  git
BuildRequires:  pkgconfig

%description
This package consists of encoding files for use with poppler. The encoding
files are optional and poppler will automatically read them if they are present.

When installed, the encoding files enables poppler to correctly render both CJK
and Cyrillic characters properly.

%package devel
Summary:        Devel files for %{name}
Requires:       %{name} = %{version}-%{release}

%description devel
This sub-package currently contains only pkgconfig file, which can be used with
pkgconfig utility allowing your software to be build with poppler-data.

%prep
%autosetup -S git

%build
# NOTE: Nothing to do here - we are packaging the content only.

%install
%make_install prefix=%{_prefix}

%files
%license COPYING COPYING.adobe COPYING.gpl2
%{_datadir}/poppler/

%files devel
%{_datadir}/pkgconfig/poppler-data.pc

%changelog
* Mon Aug 12 2025 Ruiyang Li <ruiyli@microsoft.com> - 0.4.11-1
- Original version for Azure Linux
- License Verified
