#
# Conditional build:
# _without_tex - without TeX documentation (HOWTOS)
# _without_dist_kernel - without distribution kernel
#
Summary:	Extensible packet filtering system && extensible NAT system
Summary(pl):	System filtrowania pakietСw oraz system translacji adresСw (NAT)
Summary(pt_BR):	Ferramenta para controlar a filtragem de pacotes no kernel-2.4.x
Summary(ru):	Утилиты для управления пакетными фильтрами ядра Linux
Summary(uk):	Утил╕ти для керування пакетними ф╕льтрами ядра Linux
Summary(zh_CN):	Linuxдз╨к╟Э╧Щбк╧эюМ╧╓╬ъ
Name:		iptables
Version:	1.2.8
%define		_rel	1
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Networking/Daemons
URL:		http://www.netfilter.org/
Vendor:		Netfilter mailing list <netfilter@lists.samba.org>
# Source0-md5:	cf62ebdabf05ccc5479334cc04fa993c
Source0:	http://www.netfilter.org/files/%{name}-%{version}.tar.bz2
# Source1-md5:	2ed2b452daefe70ededd75dc0061fd07
Source1:	http://ep09.kernel.pl/~djrzulf/%{name}-howtos.tar.bz2
#Source1:	cvs://cvs.samba.org/netfilter/%{name}-howtos.tar.bz2
Patch0:		%{name}-man.patch
Patch1:		http://luxik.cdi.cz/~patrick/imq/iptables-1.2.6a-imq.diff-3
%{?!_without_tex:BuildRequires:	sgml-tools}
%{?!_without_tex:BuildRequires:	sgmls}
%{?!_without_tex:BuildRequires:	tetex-latex}
%{?!_without_tex:BuildRequires:	tetex-dvips}
%{?!_without_tex:BuildRequires:	tetex-format-latex}
%{?!_without_tex:BuildRequires:	tetex-tex-babel}
%{?!_without_dist_kernel:BuildRequires: kernel-headers >= 2.3.0}
BuildRequires:	%{__perl}
BuildRequires:	groff
BuildConflicts:	kernel-headers < 2.5.0
Obsoletes:	netfilter
Obsoletes:	ipchains
BuildConflicts:	kernel < 2.5.0
Provides:	firewall-userspace-tool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An extensible NAT system, and an extensible packet filtering system.
Replacement of ipchains in 2.4 kernels.

%description -l pl
Wydajny system translacji adresСw (NAT) oraz system filtrowania
pakietСw. Zamiennik ipchains w j╠drach 2.4

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
Requires:	%{name} = %{version}

%description devel
Libraries and headers for developing iptables extensions.

%description devel -l pl
Biblioteki i pliki nagЁСwkowe niezbЙdne do tworzenia rozszerzeЯ dla
iptables.

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1

chmod 755 extensions/.*-test*
mv -f extensions/.NETLINK.test extensions/.NETLINK-test
%{__perl} -pi -e 's/\$\(HTML_HOWTOS\)//g; s/\$\(PSUS_HOWTOS\)//g' iptables-howtos/Makefile

%build
%{__make} depend 2> /dev/null || :
%{__make} CC="%{__cc}" \
	COPT_FLAGS="%{rpmcflags} -D%{!?debug:N}DEBUG" \
	LIBDIR="%{_libdir}" \
	LDLIBS="-ldl" \
	all experimental

%{?!_without_tex:%{__make} -C iptables-howtos}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/iptables,%{_mandir}/man3}

echo ".so iptables-save.8" > ip6tables-save.8
echo ".so iptables-restore.8" > ip6tables-restore.8

%{__make} install install-experimental \
	DESTDIR=$RPM_BUILD_ROOT \
	BINDIR=%{_sbindir} \
	MANDIR=%{_mandir} \
	LIBDIR=%{_libdir}

echo ".so iptables.8" > $RPM_BUILD_ROOT%{_mandir}/man8/ip6tables.8

# Devel stuff
cp -a include/* $RPM_BUILD_ROOT%{_includedir}/iptables
install lib*/lib*.a $RPM_BUILD_ROOT%{_libdir}
install libipq/*.3 $RPM_BUILD_ROOT%{_mandir}/man3

#%%{!?_without_patchedkernel:install ippool/lib*.a $RPM_BUILD_ROOT%{_libdir}}
#%%{!?_without_patchedkernel:install ippool/ippool $RPM_BUILD_ROOT%{_sbindir}}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc KNOWN_BUGS
%{?!_without_tex:%doc iptables-howtos/{NAT,networking-concepts,packet-filtering}-HOWTO*}

%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/iptables
%attr(755,root,root) %{_libdir}/iptables/*.so

%{_mandir}/man8/*

%files devel
%defattr(644,root,root,755)
%{?!_without_tex:%doc iptables-howtos/netfilter-hacking-HOWTO*}
%{_libdir}/lib*.a
%{_includedir}/iptables
%{_mandir}/man3/*
