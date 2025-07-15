# NOTE:
# there's no maintainer for the pecl project, so consider this
# extension dead.
%define		php_name	php%{?php_suffix}
%define		modname	msession
%define		status		stable
Summary:	%{modname} - extension module for PHP
Summary(pl.UTF-8):	%{modname} - moduł msession dla PHP
Name:		%{php_name}-pecl-%{modname}
Version:	1.0
Release:	5
License:	PHP 3.01
Group:		Development/Languages/PHP
# extracted from php-5.1.2 sources as pecl/msession appears to be older
Source0:	%{modname}.tar.bz2
# Source0-md5:	a256f635be818a7247d7be15061256f0
Patch0:		msession-shared-lib.patch
URL:		http://pecl.php.net/package/msession/
BuildRequires:	phoenix-devel
BuildRequires:	%{php_name}-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
Provides:	php(msession)
Obsoletes:	php-msession
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
msession is a high speed session daemon which can run either locally
or remotely. It is designed to provide consistent session management
for a PHP web farm.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
Moduł PHP dodający umożliwiający korzystanie z demona msession. Jest
to demon szybkiej obsługi sesji, który może działać lokalnie lub na
innej maszynie. Służy do zapewniania spójnej obsługi sesji dla farmy
serwerów.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -q -n %{modname}
%patch -P0 -p3

%build
phpize
%configure \
	--with-msession=shared,/usr
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
