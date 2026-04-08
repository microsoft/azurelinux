#
# Interface versions exposed by PHP:
# 
%php_core_api @PHP_APIVER@
%php_zend_api @PHP_ZENDVER@
%php_pdo_api  @PHP_PDOVER@
%php_version  @PHP_VERSION@

%php_extdir    %{_libdir}/php/modules
%php_ztsextdir %{_libdir}/php-zts/modules

%php_inidir    %{_sysconfdir}/php.d
%php_ztsinidir %{_sysconfdir}/php-zts.d

%php_incldir    %{_includedir}/php
%php_ztsincldir %{_includedir}/php-zts/php

%__php         %{_bindir}/php
%__ztsphp      %{_bindir}/zts-php

%__phpize      %{_bindir}/phpize
%__ztsphpize   %{_bindir}/zts-phpize

%__phpconfig    %{_bindir}/php-config
%__ztsphpconfig %{_bindir}/zts-php-config

%pecl_xmldir   %{_sharedstatedir}/php/peclxml
