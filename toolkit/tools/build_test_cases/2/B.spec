Summary:        Test package B
Name:           B
Epoch:          1
Version:        1.0.0
Release:        1%{?dist}
License:        MIT
URL:            https://test.com
Group:          Test
Vendor:         Microsoft
Distribution:   Azure Linux

%description
Test spec B.

%prep

%build

%install
echo "Test" > c
install -D c %{buildroot}/a/b/c

%check

%files
%defattr(-,root,root)
/a/b/c

%changelog
* Tue Aug 20 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.0-1
- Spec created.
