Summary:	extensible packet filtering system && extensible NAT system
Summary(pl):	system filtrowania pakietów oraz system translacji adresów (NAT)
Name:		iptables
Version:	1.2
Release:	4
License:	GPL
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
URL:		http://netfilter.kernelnotes.org/
Vendor:		Netfilter mailing list <netfilter@lists.samba.org>
Source0:	http://netfilter.kernelnotes.org/%{name}-%{version}.tar.bz2
Source1:	cvs://cvs.samba.org/netfilter/%{name}-howtos.tar.bz2
Patch0:		%{name}-CVS-20010216.patch.gz
Patch1:		%{name}-ip6libdir.patch
Patch2:		%{name}-ipv6-icmp.patch
BuildRequires:	sgml-tools
BuildRequires:	sgmls
BuildRequires:	mysql-devel
#Requires:	kernel >= 2.4.0test9
Obsoletes:	netfilter
Obsoletes:	ipchains
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc

%description
An extensible NAT system, and an extensible packet filtering system.

%description -l pl
Wydajny system translacji adresów (NAT) oraz system filtrowania
pakietów.

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1
chmod 755 extensions/.[a-zA-Z]*-test*
perl -pi -e 's/\$\(HTML_HOWTOS\)//g; s/\$\(PSUS_HOWTOS\)//g' iptables-howtos/Makefile

%build
%{__make} depend 2> /dev/null || :
%{__make} COPT_FLAGS="$RPM_OPT_FLAGS" \
	LIBDIR="%{_libdir}" \
	all

%{__make} -C iptables-howtos

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT \
	BINDIR=%{_sbindir} \
	MANDIR=%{_mandir} \
	LIBDIR=%{_libdir}

install ip6tables $RPM_BUILD_ROOT%{_sbindir}/
install ippool/ippool $RPM_BUILD_ROOT%{_sbindir}/

gzip -9 KNOWN_BUGS iptables-howtos/*.{txt,ps}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc KNOWN_BUGS.gz iptables-howtos/*.gz

%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/iptables/*.so

%{_mandir}/man*/*
