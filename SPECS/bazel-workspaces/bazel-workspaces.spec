#
# spec file for package bazel-workspaces
#
# Copyright (c) 2020 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

%define commit  7c8f2656c458e1fc3c5177f1ab92a6f8563c0ca6
Summary:        Bazel workspaces for libraries packaged in CBL-Mariner
Name:           bazel-workspaces
Version:        20200113
Release:        2%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools/Building
URL:            https://github.com/kubic-project/bazel-workspaces
# There are no official source tarball releases for this version. The source tarbll is grabbed from this
# following commit based on the changelog history
#Source0:       https://github.com/kubic-project/%{name}/archive/7c8f2656c458e1fc3c5177f1ab92a6f8563c0ca6.tar.gz
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  fdupes
BuildArch:      noarch

%description
Bazel workspaces for libraries packaged in CBL-Mariner which allow to link those
libraries dynamically to software build by Bazel.

%prep
%setup -q -c

%build

%install
cd %{name}-%{commit}
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -R * %{buildroot}%{_datadir}/%{name}
rm -f %{buildroot}%{_datadir}/%{name}/{LICENSE,README.md}
cp LICENSE README.md ..

%files
%license LICENSE
%doc README.md
%{_datadir}/%{name}

%changelog
* Tue Oct 12 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200113-2
- Switching to using a single digit for the 'Release' tag.

* Mon Jun 21 2021 Henry Li <lihl@microsoft.com> - 20200113-1.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- License Verified
- Fix Source URL

* Mon Jan 13 2020 mrostecki@opensuse.org
- Update to version 20200113:
  * Add workspace for re2
  * Add workspace for OpenSSL

* Mon Nov  4 2019 mrostecki@opensuse.org
- Update to version 20191105:
  * googletest: Separate gtest_main and gmock_main from gtest and
    gmock

* Mon Nov  4 2019 mrostecki@opensuse.org
- Update to version 20191104:
  * googletest: Define separate gtest and gmock libraries
  * Add workspace for prometheus-cpp
  * Add workspace for upb
  * nanopb: Fix library name
  * Add workspace for grpc
  * Add workspace for nanopb

* Fri Oct 11 2019 mrostecki@opensuse.org
- Update to version 20191011:
  * Add workspace for msgpack

* Thu Oct 10 2019 mrostecki@opensuse.org
- Update to version 20191010:
  * sql-parser: Fix headers directory

* Thu Oct 10 2019 mrostecki@opensuse.org
- Update to version 20191010:
  * Add workspace for http-parser
  * Add workspace for sql-parser

* Thu Sep 26 2019 mrostecki@opensuse.org
- Update to version 20190926:
  * jwt_verify_lib: Fix the library name
  * Add workspace for jwt_verify_lib
  * Add workspace for luajit
  * Add workspace for curl
  * Add workspace for libevent
  * benchmark: Add linkopts
  * benchmark: Add benchmark_main library
  * Add workspace for benchmark
  * gtest: Make libraries public and dynamically linked
  * gtest: Add gtest_main library
  * Add workspace for openssl-cbs
  * Add workspace for bsslwrapper
  * Add workspace for googletest
  * Add workspace for libcircllhist
  * Add workspace for yaml-cpp
  * Add workspace for gperftools
  * Add workspace for c-ares
  * Add workspace for rapidjson
  * Add workspace for libprotobuf-mutator

* Fri Sep 20 2019 Michał Rostecki <mrostecki@opensuse.org>
- Initial release
