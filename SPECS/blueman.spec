# Review request: https://bugzilla.redhat.com/show_bug.cgi?id=489564

%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(0)")}

%global commit 8901d72533d173ad0736909ed4e9a9176e5de07b 
%global shortcommit %(c=%{commit}; echo ${c:0:7}) 

Name:           blueman
Version:        1.23
Release:        9%{?dist}
Summary:        GTK+ Bluetooth Manager

Group:          Applications/System
License:        GPLv3+
URL:            http://blueman-project.org/
Source0:        https://github.com/blueman-project/%{name}/archive/%{commit}/%{name}-%{commit}.tar.gz
# The statusicon uses blueman-tray, but this icon is not provided by the package
Patch0:         blueman-1.23-statusicon.patch
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  gtk2-devel >= 2.12
BuildRequires:  pygtk2-devel >= 2.12
BuildRequires:  Pyrex >= 0.9.8.0
BuildRequires:  startup-notification-devel >= 0.9
BuildRequires:  pygobject2-devel >= 2.12
BuildRequires:  bluez-libs-devel >= 4.21
BuildRequires:  intltool >= 0.35.0
BuildRequires:  dbus-python-devel
BuildRequires:  python-devel >= 2.5
BuildRequires:  desktop-file-utils
BuildRequires:  bluez >= 4.25
#BuildRequires:  libtool
BuildRequires:  notify-python

Requires:       python >= 2.5
Requires:       bluez >= 4.25
#Requires:       obex-data-server >= 0.4.3
Requires:       pygtk2 >= 2.12
Requires:       dbus
Requires:       notify-python
#Requires:       gnome-python2-gconf
#Requires:       gnome-python2-gnome
Requires:       PolicyKit-authentication-agent
Requires:       desktop-notification-daemon
#Requires:       gvfs-obexftp
Requires:       pulseaudio-libs-glib2

Provides:       dbus-bluez-pin-helper

%description
Blueman is a tool to use Bluetooth devices. It is designed to provide simple,
yet effective means for controlling BlueZ API and simplifying bluetooth tasks
such as:
- Connecting to 3G/EDGE/GPRS via dial-up
- Connecting to/Creating bluetooth networks
- Connecting to input devices
- Connecting to audio devices
- Sending/Receiving/Browsing files via OBEX
- Pairing


%package        nautilus
Summary:        Blueman Nautilus plugin
Group:          User Interface/Desktops
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       nautilus-sendto%{?_isa}

%description    nautilus
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -qn %{name}-%{commit}
#%patch0 -p1


%build
./autogen.sh --disable-static --disable-polkit
#make dist
#%configure --disable-static --disable-polkit
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

desktop-file-install --vendor="" \
 --add-category="GTK;GNOME;" \
 --add-only-show-in="GNOME;XFCE;LXDE" \
 --delete-original \
 --dir=$RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/  \
 $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart//blueman.desktop

desktop-file-install --vendor=""     \
 --delete-original     \
 --dir=$RPM_BUILD_ROOT%{_datadir}/applications  \
 $RPM_BUILD_ROOT%{_datadir}/applications/blueman-manager.desktop
%find_lang %{name}

# we need to own this, not only because of SELinux
mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/%{name}
touch $RPM_BUILD_ROOT%{_sharedstatedir}/%{name}/network.state

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%defattr(-,root,root,-)
#%doc AUTHORS ChangeLog COPYING
%doc COPYING
%{_bindir}/*
%{python_sitelib}/blueman
%{python_sitearch}/*.so
%{_libexecdir}/blueman-mechanism
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.blueman.Mechanism.conf
%{_sysconfdir}/xdg/autostart/blueman.desktop
%{_datadir}/applications/blueman-manager.desktop
%{_datadir}/polkit-1/actions/org.blueman.policy
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/%{name}/
%{_datadir}/dbus-1/services/blueman-applet.service
%{_datadir}/dbus-1/system-services/org.blueman.Mechanism.service
#%{_datadir}/hal/fdi/information/20thirdparty/11-blueman-bnep.fdi
%{_mandir}/man1/*
%dir %{_sharedstatedir}/%{name}
%ghost %attr(0644,root,root) %{_sharedstatedir}/%{name}/network.state

%files nautilus
%defattr(-,root,root,-)
%{_libdir}/nautilus-sendto/plugins/libnstblueman.so

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 27 2012 Christoph Wickert <cwickert@fedoraproject.org> - 1.23-5
- Require pulseaudio-libs-glib2 (#856270)

* Sat Oct 06 2012 Christoph Wickert <cwickert@fedoraproject.org> - 1.23-4
- No longer require gnome-session
- Require gvfs-obexftp, needed when launching file managers from blueman

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 06 2012 Christoph Wickert <cwickert@fedoraproject.org> - 1.23-2
- Own /var/lib/blueman and /var/lib/blueman/network.state (#818528)

* Thu Apr 26 2012 Christoph Wickert <cwickert@fedoraproject.org> - 1.23-1
- Update to 1.23
- Drop upstreamed PulseAudio patch
- Fix statusicon
- Autostart blueman not only in GNOME but also in Xfce and LXDE
- Enhance description

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Sep 21 2011 Juan Rodriguez <nushio@fedoraproject.org> 1.21-10
- Rebuilt and retagged

* Wed Mar 16 2011 Juan Rodriguez <nushio@fedoraproject.org> 1.21-9
- Fixes PolicyKit dependency

* Wed Mar 16 2011 Juan Rodriguez <nushio@fedoraproject.org> 1.21-8
- Removes HAL Dependency

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 31 2010 David Malcolm <dmalcolm@redhat.com> - 1.21-6
- fix capitalization of specfile name

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.21-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sat Feb 20 2010 Juan Rodriguez <nushio@fedoraproject.org> - 1.21-4
- Removed explicit dependency for Pulseaudio

* Mon Dec 21 2009 Juan Rodriguez <nushio@fedoraproject.org> - 1.21-3
- Disabled PolKit

* Thu Nov 12 2009 Juan Rodriguez <nushio@fedoraproject.org> - 1.21-2
- Fixes segfault
- Removes notification-daemon requirement
- Disables HAL and enabled PolKit1 for Fedora 12

* Sun Oct 18 2009 Juan Rodriguez <nushio@gmail.com> - 1.21-1
- Bumping to the latest Blueman. 

* Tue Jun 23 2009 Juan Rodriguez <nushio@gmail.com> - 1.10-3
- Added Provides dbus-bluez-pin-helper

* Mon May 15 2009 Juan Rodriguez <nushio@gmail.com> - 1.10-2
- Replaced tabs with spaces
- Changed summary & Description
- Hid the patch, as its no longer needed.

* Mon Apr 27 2009 Michal Ingeli <mi@v3.sk> - 1.10-1
- upgraded to blueman 1.10
- removed obsolete bugfix patch

* Mon Mar 23 2009 Juan Rodriguez <nushio@fedoraproject.org> - 1.02-9
- Added --disable-static
- Fixed directory permissions

* Sun Mar 15 2009 Juan Rodriguez <nushio@fedoraproject.org> - 1.02-8
- Added requires gnome-session and PolicyKit.
- Fixed entries that would cause files inside /usr/share/blueman not have a proper owner.
- Touches directories before gtk-update-icon-cache runs

* Sun Mar 15 2009 Christian Krause <chkr@plauener.de> - 1.02-7
- Fixes compiling on other architectures. 
- Uses Rajeesh's patch

* Wed Mar 11 2009 Juan Rodriguez <nushio@fedoraproject.org> - 1.02-6
- Using upstream tar.gz instead of patched one.

* Wed Mar 11 2009 Juan Rodriguez <nushio@fedoraproject.org> - 1.02-5
- Changed license to GPLv3+
- Removed *.a files
- Wildcard usage on Man and Executables
- Changed gtk2 to gtk2-devel on BuildRequires
- Added dbus-python-devel dependency

* Wed Mar 11 2009 Juan Rodriguez <nushio@fedoraproject.org> - 1.02-4
- Added patch
- Removed xdg .desktop file
- Made it autostart on Gnome login

* Wed Mar 11 2009 Juan Rodriguez <nushio@fedoraproject.org> - 1.02-3
- Used dynamic files
- Added Python path

* Wed Mar 11 2009 Juan Rodriguez <nushio@fedoraproject.org> - 1.02-2
- Added BuildRequires and Requires

* Tue Mar 10 2009 Juan Rodriguez <nushio@fedoraproject.org> - 1.02-1
- Updating to Blueman 1.02
- See http://blueman-project.org/ for changelog.

* Wed Feb 18 2009 Juan Rodriguez <nushio@fedoraproject.org> - 1.01-1
- Initial RPM release
- See http://blueman-project.org/ for changelog.

