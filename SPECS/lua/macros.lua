%lua_version %{lua: print(string.sub(_VERSION, 5))}

%lua_libdir %{_libdir}/lua/%{lua_version}
%lua_pkgdir %{_datadir}/lua/%{lua_version}

%lua_requires \
%if 0%{?fedora} >= 16 || 0%{?rhel} >= 7 \
Requires: lua(abi) = %{lua_version} \
%else \
Requires: lua >= %{lua_version} \
Requires: lua < %{lua: os.setlocale('C'); print(string.sub(_VERSION, 5) + 0.1)} \
%endif \
%{nil}
