#
# Conditional build:
%bcond_without patchedkernel	# without ippool, prestate, log (which requires patched 2.4.x kernel)
%bcond_without howto 		# without documentation (HOWTOS) which needed TeX.
#
%define		netfilter_snap		20040216
%define		iptables_version	1.2.9
Summary:	Extensible packet filtering system && extensible NAT system
Summary(pl):	System filtrowania pakietСw oraz system translacji adresСw (NAT)
Summary(pt_BR):	Ferramenta para controlar a filtragem de pacotes no kernel-2.4.x
Summary(ru):	Утилиты для управления пакетными фильтрами ядра Linux
Summary(uk):	Утил╕ти для керування пакетними ф╕льтрами ядра Linux
Summary(zh_CN):	Linuxдз╨к╟Э╧Щбк╧эюМ╧╓╬ъ
Name:		iptables
%if %{netfilter_snap} != 0
Version:	%{iptables_version}_%{netfilter_snap}
%else
Version:	%{iptables_version}
%endif
%define		_rel	1
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Networking/Daemons
URL:		http://www.netfilter.org/
Vendor:		Netfilter mailing list <netfilter@lists.samba.org>
%if %{netfilter_snap} != 0
Source0:	%{name}-%{version}.tar.bz2
%else
Source0:	http://www.netfilter.org/files/%{name}-%{version}.tar.bz2
%endif
Source1:	cvs://cvs.samba.org/netfilter/%{name}-howtos.tar.bz2
# Source1-md5:	2ed2b452daefe70ededd75dc0061fd07
Patch1:		%{name}-1.2.9-ipt_p2p.patch
#Patch2:		ip_queue_vwmark.patch.userspace
#Patch3:		ipt_REJECT-fake-source.patch.userspace
#Patch4:		mark-bitwise-ops.patch.userspace

Patch10:	%{name}-gkh-fix.patch

%{?with_howto:BuildRequires:	sgml-tools}
%{?with_howto:BuildRequires:	sgmls}
%{?with_howto:BuildRequires:	tetex-latex}
%{?with_howto:BuildRequires:	tetex-tex-babel}
%{?with_howto:BuildRequires:	tetex-dvips}
BuildRequires:	perl-base
%if %{netfilter_snap} != 0
%{?with_patchedkernel:BuildRequires:	kernel-headers(netfilter) = %{netfilter_snap}}
%endif
BuildConflicts:	kernel-headers < 2.3.0
Obsoletes:	netfilter
Obsoletes:	ipchains
%if %{netfilter_snap} != 0
%{?with_patchedkernel:Requires:	kernel(netfilter) = %{netfilter_snap}}
%endif

Provides:	firewall-userspace-tool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc

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
%patch1 -p1

%patch10 -p1

#%%patch2 -p1
#%%patch3 -p1
#%%patch4 -p1

# removed broken ...
rm -rf ipset

chmod 755 extensions/.*-test*
perl -pi -e 's/\$\(HTML_HOWTOS\)//g; s/\$\(PSUS_HOWTOS\)//g' iptables-howtos/Makefile

%build
rm -f include/asm
ln -s %{_kernelsrcdir}/include/asm-%{_arch} include/asm

%{__make} depend 2> /dev/null || :
%{__make} CC="%{__cc}" \
	LIBDIR="%{_libdir}" \
	all experimental
#	COPT_FLAGS="%{rpmcflags} -D%{!?debug:N}DEBUG" \

%{?with_howto:%{__make} -C iptables-howtos}

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
#install lib*/lib*.a $RPM_BUILD_ROOT%{_libdir}
install libipq/*.3 $RPM_BUILD_ROOT%{_mandir}/man3

##%{?with_patchedkernel:install ippool/lib*.a $RPM_BUILD_ROOT%{_libdir}}
##%{?with_patchedkernel:install ippool/ippool $RPM_BUILD_ROOT%{_sbindir}}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc 
%{?with_howto:%doc iptables-howtos/{NAT,networking-concepts,packet-filtering}-HOWTO*}

%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/iptables
%attr(755,root,root) %{_libdir}/iptables/*.so

%{_mandir}/man8/*

%files devel
%defattr(644,root,root,755)
%{?with_howto:%doc iptables-howtos/netfilter-hacking-HOWTO*}
#%%{_libdir}/lib*.a
%{_includedir}/iptables
%{_mandir}/man3/*
