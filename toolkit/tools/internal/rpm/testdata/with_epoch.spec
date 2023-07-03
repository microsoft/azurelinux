Summary:        Test spec file with with no default package
Name:           with_epoch
Epoch:          1
Version:        1.0.0
Release:        1%{?dist}
License:        MIT
URL:            https://test.com
Group:          Test
Vendor:         Microsoft
Distribution:   Mariner

%description
Test spec. Make sure the default package is built and the 'Epoch' equals 1!

%prep

%build

%install

%files
%defattr(-,root,root)

%changelog
* Wed Jun 21 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.0-1
- Creation of the test spec.
