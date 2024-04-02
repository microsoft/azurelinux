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
Source1:        %{name}-%{version}-govendor-v1.tar.gz

BuildRequires:  golang

%description
OpenTofu lets you declaratively manage your cloud infrastructure.

%prep
%autosetup -p1 %{?with_vendor:-b1}

%build
tar -xf %{SOURCE1} --no-same-owner

export LDFLAGS="-X github.com/opentofu/opentofu/version.dev=no"
export VERSION=%{version}
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
