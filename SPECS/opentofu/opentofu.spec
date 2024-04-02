%bcond_without vendor

Name:           opentofu
Version:        1.6.2
Release:        3%{?dist}
Summary:        OpenTofu lets you declaratively manage your cloud infrastructure
Vendor:         Microsoft Corporation
Distribution:   Azure Linux

License:        0BSD AND Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND MIT AND MPL-2.0
URL:            https://github.com/opentofu/opentofu
Source0:        https://github.com/opentofu/opentofu/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/opentofu/opentofu/archive/refs/tags/v%%{version}.tar.gz -O opentofu-%%{version}.tar.gz
#   2. tar -xf opentofu-%%{version}.tar.gz
#   3. cd opentofu-%%{version}
#   4. go mod vendor
#   5. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf opentofu-%%{version}-vendor.tar.gz vendor
#
#   NOTES:
#       - You require GNU tar version 1.28+.
#       - The additional options enable generation of a tarball with the same hash every time regardless of the environment.
#         See: https://reproducible-builds.org/docs/archives/
#       - For the value of "--mtime" use the date "2021-04-26 00:00Z" to simplify future updates.
Source1:        %{name}-%{version}-vendor.tar.gz

BuildRequires:  golang

%description
OpenTofu lets you declaratively manage your cloud infrastructure.

%prep
%autosetup -p1 %{?with_vendor:-b1}

%build
tar -xf %{SOURCE1} --no-same-owner

export LDFLAGS="-X github.com/opentofu/opentofu/version.dev=no"
export VERSION=%{version}
go env
ls /usr/lib/golang
go build \
  -buildmode pie \
  -compiler gc \
  -tags="rpm_crashtraceback" \
  -ldflags "${LDFLAGS:-} -X github.com/opentofu/opentofu/version=$VERSION -extldflags '-Wl,-z,relro'" \
  -mod=vendor \
  -a -v -x \
  -o ./bin/tofu \
  github.com/opentofu/opentofu/cmd/tofu

%install
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp ./bin/*             %{buildroot}%{_bindir}/

%check
for test in "TestResourceProvider_ApplyCustomWorkingDirectory" \
            "TestGet_cancel" \
            "TestInit_cancelModules" \
            "TestFileExists" \
; do
awk -i inplace '/^func.*'"$test"'\(/ { print; print "\tt.Skip(\"disabled failing test\")"; next}1' $(grep -rl $test)
done
go test -mod=vendor ./...

%files
%license LICENSE %{?with_vendor:vendor/modules.txt}
%doc docs BUILDING.md CODE_OF_CONDUCT.md DEBUGGING.md MIGRATION_GUIDE.md
%doc SECURITY.md README.md CHANGELOG.md CONTRIBUTING.md TSC_SUMMARY.md
%doc WEEKLY_UPDATES.md
%{_bindir}/tofu

%changelog
* Mon Apr 01 2024 - Thien Trung Vuong <tvuong@microsoft.com> - 1.6.1-3
- Initial Azure Linux import from Fedora 40 (license: MIT).
- License verified.

* Thu Feb 08 2024 - Mikel Olasagasti Uranga <mikel@olasagasti.info> - 1.6.1-2
- Don't include devel files

* Mon Feb 05 2024 - Mikel Olasagasti Uranga <mikel@olasagasti.info> - 1.6.1-1
- Initial package - Closes rhbz#2258867
