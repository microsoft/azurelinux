Summary:        Test spec file with supported and unsupported architectures inside the "ExclusiveArch" tag
Name:           supported_unsupported_architectures
Version:        1.0.0
Release:        1%{?dist}
License:        MIT
URL:            https://test.com
Group:          Test
Vendor:         Microsoft
Distribution:   Azure Linux

BuildArch:      noarch

# Must contain only architectures not supported by Azure Linux!
ExcludeArch:    i686

# Must contain an architecture for each of the supported builds of Azure Linux!
ExclusiveArch:  x86_64 aarch64

%description
Test spec. Make sure "ExclusiveArch" contains an entry for each architecture supported by Azure Linux!

%prep

%build

%install

%files
%defattr(-,root,root)

%changelog
* Mon Oct 11 2021 Pawel Winogrodzki <pawelwi@microsoft.com> 1.0.0-1
- Creation of the test spec.

