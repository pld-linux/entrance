Summary:	Enlightened display manager
Name:		entrance
Version:	0.9.0
%define _snap	20050106
Release:	0.%{_snap}.0.1
License:	BSD
Group:		X11/Applications
#Source0:	http://dl.sourceforge.net/enlightenment/%{name}-%{version}.tar.gz
Source0:	ftp://ftp.sparky.homelinux.org/pub/e17/%{name}-%{version}-%{_snap}.tar.gz
# Source0-md5:	22bd32b41c655089ae9a1591da462a01
URL:		http://enlightenment.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	esmart-devel
BuildRequires:	libtool
BuildRequires:	pam-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Entrance is the Enlightenment Display Manager. And like Enlightenment,
it takes beauty and customization to levels that KDM and GDM can only
dream about...and without the bloat.

%prep
%setup -q -n %{name}

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-xsession=/etc/X11/xdm/Xsession
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING* README
%{_sysconfdir}/entrance_config.db
#/etc/rc.d/init.d/entrance
%{_sysconfdir}/pam.d/entrance
%attr(755,root,root) %{_bindir}/entrance*
%attr(755,root,root) %{_sbindir}/entranced
%{_datadir}/%{name}
