#
# Conditional build:
%bcond_without	doc		# without documentation (HOWTOS) which needed TeX
%bcond_without	dist_kernel	# without distribution kernel
#
%define		_snap			0
%define		iptables_version	1.3.0
%define		llh_version		7:2.6.10.0-1
%define		name6			ip6tables
%define		l7_version		1.0
#
Summary:	Extensible packet filtering system && extensible NAT system
Summary(pl):	System filtrowania pakietСw oraz system translacji adresСw (NAT)
Summary(pt_BR):	Ferramenta para controlar a filtragem de pacotes no kernel-2.6.x
Summary(ru):	Утилиты для управления пакетными фильтрами ядра Linux
Summary(uk):	Утил╕ти для керування пакетними ф╕льтрами ядра Linux
Summary(zh_CN):	Linuxдз╨к╟Э╧Щбк╧эюМ╧╓╬ъ
Name:		iptables
Version:	%{iptables_version}
%define		_rel	0.1
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://ftp.netfilter.org/pub/iptables/iptables-%{version}.tar.bz2
# Source0-md5:	a072c0f09f1b289cb7af56f76407d033
#Source0:	http://www.netfilter.org/files/%{name}-%{version}.tar.bz2
Source1:	cvs://cvs.samba.org/netfilter/%{name}-howtos.tar.bz2
# Source1-md5:	2ed2b452daefe70ededd75dc0061fd07
Source2:	%{name}.init
Source3:	%{name6}.init
Patch0:		%{name}-Makefile.patch
#Patch1:		%{name}-pom-ng-%{_snap}.patch
Patch2:		%{name}-1.2.9-imq1.diff
Patch3:		%{name}-debug.patch
Patch4:		%{name}-layer7-%{l7_version}.patch
Patch5:		grsecurity-1.2.11-iptables.patch
URL:		http://www.netfilter.org/
Vendor:		Netfilter mailing list <netfilter@lists.samba.org>
%if %{with doc}
BuildRequires:	sgml-tools
BuildRequires:	sgmls
BuildRequires:	tetex-dvips
BuildRequires:	tetex-format-latex
BuildRequires:	tetex-latex
BuildRequires:	tetex-tex-babel
BuildRequires:	sed >= 4.0
%endif
%if %{with dist_kernel} && %{_snap} != 0
BuildRequires:	kernel-headers(netfilter) = %{_snap}
BuildRequires:	kernel-source
Requires:	kernel(netfilter) = %{_snap}
%endif
BuildRequires:	linux-libc-headers >= %{llh_version}
BuildConflicts:	kernel-headers < 2.3.0
Provides:	firewall-userspace-tool
Obsoletes:	netfilter
Obsoletes:	ipchains
Obsoletes:	iptables24-compat
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An extensible NAT system, and an extensible packet filtering system.
Replacement of ipchains in 2.4 and higher kernels.

%description -l pl
Wydajny system translacji adresСw (NAT) oraz system filtrowania
pakietСw. Zamiennik ipchains w j╠drach 2.4 i nowszych.

%description -l pt_BR
Esta И a ferramenta que controla o cСdigo de filtragem de pacotes do
kernel 2.4, obsoletando ipchains. Com esta ferramenta vocЙ pode
configurar filtros de pacotes, NAT, mascaramento (masquerading),
regras dinБmicas (stateful inspection), etc.

%description -l ru
iptables управляют кодом фильтрации сетевых пакетов в ядре Linux. Они
позволяют вам устанавливать межсетевые экраны (firewalls) и IP
маскарадинг, и т.п.

%description -l uk
iptables управляють кодом ф╕льтрац╕╖ пакет╕в мереж╕ в ядр╕ Linux. Вони
дозволяють вам встановлювати м╕жмережев╕ екрани (firewalls) та IP
маскарадинг, тощо.

%package devel
Summary:	Libraries and headers for developing iptables extensions
Summary(pl):	Biblioteki i nagЁСwki do tworzenia rozszerzeЯ iptables
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	iptables24-devel

%description devel
Libraries and headers for developing iptables extensions.

%description devel -l pl
Biblioteki i pliki nagЁСwkowe niezbЙdne do tworzenia rozszerzeЯ dla
iptables.

%package init
Summary:	Iptables init (RedHat style)
Summary(pl):	Iptables init (w stylu RedHata)
Group:		Networking/Admin
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}
Obsoletes:	firewall-init
Obsoletes:	firewall-init-ipchains
Obsoletes:	iptables24-init

%description init
Iptables-init is meant to provide an alternate way than firewall-init
to start and stop packet filtering through iptables(8).

%description init -l pl
Iptables-init ma na celu udostЙpnienie alternatywnego w stosunku do
firewall-init sposobu wЁ╠czania i wyЁ╠czania filtrСw IP j╠dra poprzez
iptables(8).

%prep
%setup -q -n %{name}-%{version} -a1
%patch0 -p1
#%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

# removed broken ...
#%rm -f extensions/.set-test

chmod 755 extensions/.*-test*

%build
%{__make} all experimental \
	CC="%{__cc}" \
	COPT_FLAGS="%{rpmcflags} -D%{!?debug:N}DEBUG" \
	KERNEL_DIR="%{_kernelsrcdir}" \
	LIBDIR="%{_libdir}" \
	LDLIBS="-ldl"

%if %{with doc}
%{__make} -C iptables-howtos
sed -i 's:$(HTML_HOWTOS)::g; s:$(PSUS_HOWTOS)::g' iptables-howtos/Makefile
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_initrddir},%{_includedir},%{_libdir},%{_mandir}/man3}

echo ".so iptables-save.8" > %{name6}-save.8
echo ".so iptables-restore.8" > %{name6}-restore.8

%{__make} install install-experimental \
	DESTDIR=$RPM_BUILD_ROOT \
	BINDIR=%{_sbindir} \
	MANDIR=%{_mandir} \
	LIBDIR=%{_libdir}

echo ".so iptables.8" > $RPM_BUILD_ROOT%{_mandir}/man8/%{name6}.8

install -d $RPM_BUILD_ROOT%{_sysconfdir}/l7-protocols

# Devel stuff
cp -a include/{lib*,ip*} $RPM_BUILD_ROOT%{_includedir}
install lib*/lib*.a $RPM_BUILD_ROOT%{_libdir}
install libipq/*.3 $RPM_BUILD_ROOT%{_mandir}/man3

install %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT%{_initrddir}/%{name6}

%clean
rm -rf $RPM_BUILD_ROOT

%post init
/sbin/chkconfig --add %{name}
/sbin/chkconfig --add %{name6}

%preun init
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del %{name}
	/sbin/chkconfig --del %{name6}
fi

%files
%defattr(644,root,root,755)
%{?with_doc:%doc iptables-howtos/{NAT,networking-concepts,packet-filtering}-HOWTO*}
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/iptables
%attr(755,root,root) %{_libdir}/iptables/*.so
%{_mandir}/man8/*

%files devel
%defattr(644,root,root,755)
%{?with_doc:%doc iptables-howtos/netfilter-hacking-HOWTO*}
%{_libdir}/lib*.a
%{_includedir}/*.h
%dir %{_includedir}/libip*
%{_includedir}/libip*/*.h
%{_mandir}/man3/*

%files init
%defattr(644,root,root,755)
%attr(754,root,root) %{_initrddir}/*
