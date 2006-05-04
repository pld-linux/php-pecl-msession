# NOTE:
# there's no maintainer for the pecl project, so consider this
# extension dead.
%define		_modname	msession
%define		_status		stable
%define		_sysconfdir	/etc/php
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)
Summary:	msession extension module for PHP
Summary(pl):	Modu³ msession dla PHP
Name:		php-pecl-%{_modname}
Version:	1.0
Release:	0.1
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	%{_modname}.tar.bz2
# Source0-md5:	3a5b6bf9aa3c7d1abac18a5b484c0897
URL:		http://pecl.php.net/package/msession/
BuildRequires:	phoenix-devel
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.254
%{?requires_php_extension}
Requires:	%{_sysconfdir}/conf.d
Provides:	php-msession = 4:5.1.2-9
Obsoletes:	php-msession
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a dynamic shared object (DSO) for PHP that will allow you to
use msession. msession is a high speed session daemon which can run
either locally or remotely. It is designed to provide consistent
session management for a PHP web farm.

In PECL status of this extension is: %{_status}.

%description -l pl
Modu³ PHP dodaj±cy umo¿liwiaj±cy korzystanie z demona msession. Jest
to demon szybkiej obs³ugi sesji, który mo¿e dzia³aæ lokalnie lub na
innej maszynie. S³u¿y do zapewniania spójnej obs³ugi sesji dla farmy
serwerów.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -n %{_modname}

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/conf.d,%{extensionsdir}}

install modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
