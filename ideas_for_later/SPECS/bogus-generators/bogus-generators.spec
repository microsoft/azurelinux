Summary:        Bogus provides and requires generator
Name:           bogus-generators
Version:        1.0.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://www.microsoft.com
Source0:        bogusgenerators.attr

%description
Tool to generate bogus RPM provides, requires, etc.

%prep

%build
# No-op

%install
install -Dpm0644 -t %{buildroot}%{_fileattrsdir} %{SOURCE0}

%files
%{_fileattrsdir}/*

%changelog
* Wed Mar 06 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.0-1
- Original version for CBL-Mariner.
