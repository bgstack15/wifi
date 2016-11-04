Name:		wifi
Version:	0.1
#Release:	1%{?dist}
Release:	1
Summary:	Wifi Configurator for bgstack15

Group:		Applications/Internet
License:	CC BY-SA 4.0
URL:		https://bgstack15.wordpress.com/
Source0:	wifi.tgz

BuildRequires:	python3-devel
Requires:	python34
Packager:	Bgstack15 <bgstack15@gmail.com>
Buildarch:	noarch

%define _unpackaged_files_terminate_build 0
%description
Wifi provides a small python script that reads config files for specific networks. Adapt to your needs.

%prep
%setup


%build

%install
rsync -a . %{buildroot}/

%clean
rm -rf %{buildroot}

%post

%preun

%files
/README.md
/usr/wifi/inc/scrub.py
%doc %attr(444, -, -) /usr/wifi/inc/scrub.txt
/usr/wifi/inc/localize_git.sh
%config /usr/wifi/networks/sample.wifi
%config /usr/wifi/networks/campus.wifi
%doc %attr(444, -, -) /usr/wifi/packaging.txt
/usr/wifi/docs/nmcli.md
/usr/wifi/docs/wifi.spec
/usr/wifi/docs/wnic.md
/usr/wifi/wifi.py
%verify(link) /usr/bin/wifi

%changelog
* Thu Nov 3 2016 B Stack <bgstack15@gmail.com>
- Wrote initial rpm package
