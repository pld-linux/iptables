#
# TODO:
#		- update kernel-net-(ipt_)p2p and remove 1.2.9-ipt_p2p.patch
#
# Conditional build:
%bcond_without	patchedkernel	# without ippool, prestate, log (which requires patched 2.4.x kernel)
%bcond_without	doc 		# without documentation (HOWTOS) which needed TeX.
#
%define		netfilter_snap		20040316
%define		iptables_version	1.2.9
#
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
Source0:	%{name}-%{iptables_version}_%{netfilter_snap}.tar.bz2
%else
Source0:	http://www.netfilter.org/files/%{name}-%{version}.tar.bz2
%endif
Source1:	cvs://cvs.samba.org/netfilter/%{name}-howtos.tar.bz2
# Source1-md5:	2ed2b452daefe70ededd75dc0061fd07
Source2:	%{name}.init
Patch1:		%{name}-gkh-fix.patch
Patch2:		%{name}-dstlimit.patch
Patch3:		%{name}-1.2.9-ipt_p2p.patch
Patch4:		%{name}-1.2.9-ipt_imq.patch
%if %{with doc}
BuildRequires:	sgml-tools
BuildRequires:	sgmls
BuildRequires:	tetex-latex
BuildRequires:	tetex-tex-babel
BuildRequires:	tetex-dvips
%endif
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
Requires:	%{name} = %{version}-%{release}

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
Requires(post,preun):   /sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Obsoletes:	firewall-init

%description init
Iptables-init is meant to provide an alternate way than firewall-init
to start and stop packet filtering through iptables(8).

%description init -l pl
Iptablea-init ma na celu udostЙpnienie alternatywnego w stosunku do
firewall-init sposobu wЁ╠czania i wyЁ╠czania filtrСw IP j╠dra poprzez
iptables(8).

%prep
%setup -q -a1
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p1

# removed broken ...
#%rm -f extensions/.set-test

chmod 755 extensions/.*-test*
perl -pi -e 's/\$\(HTML_HOWTOS\)//g; s/\$\(PSUS_HOWTOS\)//g' iptables-howtos/Makefile

%build
ln -sf %{_kernelsrcdir}/include/asm-%{_arch} include/asm

%{__make} depend 2> /dev/null || :
%{__make} CC="%{__cc}" \
	LIBDIR="%{_libdir}" \
	all experimental \
	COPT_FLAGS="%{rpmcflags} -D%{!?debug:N}DEBUG"

%{?with_doc:%{__make} -C iptables-howtos}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/iptables,%{_mandir}/man3,%{_initrddir}}
install %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}/iptables

echo ".so iptables-save.8" > ip6tables-save.8
echo ".so iptables-restore.8" > ip6tables-restore.8

%{__make} install install-experimental \
	DESTDIR=$RPM_BUILD_ROOT \
	BINDIR=%{_sbindir} \
	MANDIR=%{_mandir} \
	LIBDIR=%{_libdir}

echo ".so iptables.8" > $RPM_BUILD_ROOT%{_mandir}/man8/ip6tables.8

# Devel stuff
cp -a include/{lib*,ip*} $RPM_BUILD_ROOT%{_includedir}/iptables
install lib*/lib*.a $RPM_BUILD_ROOT%{_libdir}
install libipq/*.3 $RPM_BUILD_ROOT%{_mandir}/man3

##%{?with_patchedkernel:install ippool/lib*.a $RPM_BUILD_ROOT%{_libdir}}
##%{?with_patchedkernel:install ippool/ippool $RPM_BUILD_ROOT%{_sbindir}}

%clean
rm -rf $RPM_BUILD_ROOT

%post init
/sbin/chkconfig --add %{name}

%preun init
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc 
%{?with_doc:%doc iptables-howtos/{NAT,networking-concepts,packet-filtering}-HOWTO*}
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/iptables
%attr(755,root,root) %{_libdir}/iptables/*.so
%{_mandir}/man8/*

%files devel
%defattr(644,root,root,755)
%{?with_doc:%doc iptables-howtos/netfilter-hacking-HOWTO*}
%{_libdir}/lib*.a
%{_includedir}/iptables
%{_mandir}/man3/*

%files init
%defattr(644,root,root,755)
%attr(750,root,root) %{_initrddir}/iptables
