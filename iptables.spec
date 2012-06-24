#
# Conditional build:
# _without_patchedkernel - without ippool, prestate, log (which requires patched 2.4.x kernel)
# _without_howto - without documentation (HOWTOS) which needed TeX.
#
%define		netfilter_snap	0
# % define		netfilter_snap	20030616
%define		iptables_version	1.2.8
Summary:	Extensible packet filtering system && extensible NAT system
Summary(pl):	System filtrowania pakiet�w oraz system translacji adres�w (NAT)
Summary(pt_BR):	Ferramenta para controlar a filtragem de pacotes no kernel-2.4.x
Summary(ru):	������� ��� ���������� ��������� ��������� ���� Linux
Summary(uk):	���̦�� ��� ��������� ��������� Ʀ������� ���� Linux
Summary(zh_CN):	Linux�ں˰����˹�����
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
Source0:	http://www.netfilter.org/files/%{name}-%{version}.tar.bz2
# Source0-md5:	cf62ebdabf05ccc5479334cc04fa993c
Source1:	cvs://cvs.samba.org/netfilter/%{name}-howtos.tar.bz2
# Source1-md5:	2ed2b452daefe70ededd75dc0061fd07
Source2:	%{name}.init
Patch0:		%{name}-man.patch
Patch3:		http://trash.net/~kaber/imq/pom-20030625.diff
Patch4:		grsecurity-%{iptables_version}-iptables.patch
# CVS up-to-date
Patch9:		iptables-1.2.8-CVS-20030715.patch
# patches from netfilter
Patch10:	ipt_REJECT-fake-source.patch.userspace
Patch11:	mark-bitwise-ops.patch.userspace
Patch12:	raw.patch.userspace
Patch13:	raw.patch.ipv6.userspace
Patch14:	40_nf-log.patch.userspace
%{?!_without_howto:BuildRequires:	sgml-tools}
%{?!_without_howto:BuildRequires:	sgmls}
%{?!_without_howto:BuildRequires:	tetex-latex}
%{?!_without_howto:BuildRequires:	tetex-dvips}
BuildRequires:	perl
%if %{netfilter_snap} != 0
%{!?_without_patchedkernel:BuildRequires:	kernel-headers(netfilter) = %{iptables_version}-%{netfilter_snap}}
%else
%{!?_without_patchedkernel:BuildRequires:	kernel-headers(netfilter) = %{iptables_version}}
%endif
%{!?_without_patchedkernel:BuildRequires:       kernel-source}
BuildConflicts:	kernel-headers < 2.3.0
Obsoletes:	netfilter
Obsoletes:	ipchains
%if %{netfilter_snap} != 0
%{!?_without_patchedkernel:Requires:	kernel(netfilter) = %{iptables_version}-%{netfilter_snap}}
%else
%{!?_without_patchedkernel:Requires:	kernel(netfilter) = %{iptables_version}}
%endif

Provides:	firewall-userspace-tool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc

%description
An extensible NAT system, and an extensible packet filtering system.
Replacement of ipchains in 2.4 kernels.

%description -l pl
Wydajny system translacji adres�w (NAT) oraz system filtrowania
pakiet�w. Zamiennik ipchains w j�drach 2.4

%description -l pt_BR
Esta � a ferramenta que controla o c�digo de filtragem de pacotes do
kernel 2.4, obsoletando ipchains. Com esta ferramenta voc� pode
configurar filtros de pacotes, NAT, mascaramento (masquerading),
regras din�micas (stateful inspection), etc.

%description -l ru
iptables ��������� ����� ���������� ������� ������� � ���� Linux. ���
��������� ��� ������������� ���������� ������ (firewalls) � IP
�����������, � �.�.

%description -l uk
iptables ���������� ����� Ʀ�����æ� ����Ԧ� ����֦ � ��Ҧ Linux. ����
���������� ��� ������������� ͦ�������צ ������ (firewalls) �� IP
�����������, ����.

%package devel
Summary:	Libraries and headers for developing iptables extensions
Summary(pl):	Biblioteki i nag��wki do tworzenia rozszerze� iptables
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Libraries and headers for developing iptables extensions.

%description devel -l pl
Biblioteki i pliki nag��wkowe niezb�dne do tworzenia rozszerze� dla
iptables.

%package init
Summary:	Iptables init (RedHat style)
Summary(pl):	Iptables init (w stylu RedHata)
Group:		Networking/Admin
Requires(post,preun):   /sbin/chkconfig
Requires:	%{name}
Obsoletes:	firewall-init

%description init
Iptable-init is meant to provide an alternate way than firewall-init
to start and stop packet filtering through iptables(8).

%description init -l pl
Iptable-init ma na celu umozliwic alternatywny w stosunku do
firewall-init spos�b startowania i stopowania filtr�w IP j�dra
poprzez iptables(8).

%prep
%setup -q -a1
%patch0 -p1
%{!?_without_patchedkernel:%patch3 -p1}
patch -p1 < userspace/IMQ.patch.userspace
%{!?_without_patchedkernel:%patch4 -p1}
%{!?_without_patchedkernel:%patch9 -p1}
%{!?_without_patchedkernel:%patch10 -p1}
%{!?_without_patchedkernel:%patch11 -p1}
%{!?_without_patchedkernel:%patch12 -p1}
%{!?_without_patchedkernel:%patch13 -p1}
%{!?_without_patchedkernel:%patch14 -p1}

chmod 755 extensions/.*-test*
perl -pi -e 's/\$\(HTML_HOWTOS\)//g; s/\$\(PSUS_HOWTOS\)//g' iptables-howtos/Makefile

%build
%{__make} depend 2> /dev/null || :
%{__make} CC="%{__cc}" \
	COPT_FLAGS="%{rpmcflags} -D%{!?debug:N}DEBUG" \
	LIBDIR="%{_libdir}" \
	all experimental

%{?!_without_howto:%{__make} -C iptables-howtos}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/iptables,%{_mandir}/man3,%{_initrddir}}

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

%{!?_without_patchedkernel:install ippool/lib*.a $RPM_BUILD_ROOT%{_libdir}}
%{!?_without_patchedkernel:install ippool/ippool $RPM_BUILD_ROOT%{_sbindir}}

install %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}/iptables

%clean
rm -rf $RPM_BUILD_ROOT

%post init
/sbin/chkconfig --add %{name}

%preun init
/sbin/chkconfig --del %{name}

%files
%defattr(644,root,root,755)
%doc KNOWN_BUGS
%{?!_without_howto:%doc iptables-howtos/{NAT,networking-concepts,packet-filtering}-HOWTO*}

%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/iptables
%attr(755,root,root) %{_libdir}/iptables/*.so

%{_mandir}/man8/*

%files devel
%defattr(644,root,root,755)
%{?!_without_howto:%doc iptables-howtos/netfilter-hacking-HOWTO*}
%{_libdir}/lib*.a
%{_includedir}/iptables
%{_mandir}/man3/*

%files init
%attr(755,root,root) %{_initrddir}/iptables
