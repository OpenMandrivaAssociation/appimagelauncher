%define oname AppImageLauncher
Name:		appimagelauncher
Version:	3.0.0
Release:	0.alpha.1
License:	MIT
Summary:	AppImage system intergation
URL:		https://github.com/TheAssassin/AppImageLauncher
Source:		https://github.com/TheAssassin/AppImageLauncher/archive/refs/tags/v3.0.0-alpha-1/%{oname}-3.0.0-alpha-1.tar.gz
Source1:	https://github.com/AppImageCommunity/AppImageUpdate/archive/refs/heads/main.tar.gz
Source2:	https://github.com/AppImageCommunity/zsync2/archive/4e549b676bee6455c7557c26ca4b5a10217eb4d9.tar.gz
Source3:	https://github.com/libcpr/cpr/archive/db351ffbbadc6c4e9239daaa26e9aefa9f0ec82d.tar.gz
Source4:	https://github.com/google/googletest/archive/ec44c6c1675c25b9827aacd08c02433cccde7780.tar.gz
Source5:	https://github.com/Taywee/args/archive/b50b5c45ba1134e9f9b3fdf6f12d75ff725857bc.tar.gz
Patch0:		appimagelauncher-static-helpers.patch
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	patchelf
BuildRequires:	pkgconfig(libappimage)
BuildRequires:	%{_lib}appimage-static-devel
BuildRequires:	glibc-static-devel
BuildRequires:	stdc++-static-devel
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(fuse3)
BuildRequires:	pkgconfig(libarchive)
BuildRequires:	pkgconfig(xpm)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5DBus)
BuildRequires:	pkgconfig(Qt5Quick)
BuildRequires:	pkgconfig(Qt5QuickWidgets)
BuildRequires:	pkgconfig(gpgme) >= 1.10.0
BuildRequires:	pkgconfig(openssl)
BuildRequires:	qmake5
BuildRequires:	cmake(nlohmann_json)
BuildRequires:	boost-devel
BuildRequires:	git-core
BuildRequires:	argagg
BuildRequires:	qt5-linguist-tools
# For xxd
BuildRequires:	vim

%description
Integrate AppImages to your application launcher with one click, and manage, update and remove them from there. 
Double-click AppImages to open them, without having to make them executable first.

AppImageLauncher plays well with other applications managing AppImages, for example app stores. 
However, it doesn't depend on any of those, and can run completely standalone.

%prep
%setup -q -n %{oname}-3.0.0-alpha-1
if ! [ -d .git ]; then
	# Make stupid version checker happy
	git init
	git add .
	git config user.email info@openmandriva.org
	git config user.name "OpenMandriva Builder"
	git commit -m "Import to make version checker happy"
fi

tar xf %{S:1}
rmdir lib/AppImageUpdate
mv AppImageUpdate-main lib/AppImageUpdate

tar xf %{S:2}
rmdir lib/AppImageUpdate/lib/zsync2
mv zsync2-* lib/AppImageUpdate/lib/zsync2

tar xf %{S:3}
rmdir lib/AppImageUpdate/lib/zsync2/lib/cpr
mv cpr-* lib/AppImageUpdate/lib/zsync2/lib/cpr

tar xf %{S:4}
rmdir lib/AppImageUpdate/lib/zsync2/lib/gtest
mv googletest-* lib/AppImageUpdate/lib/zsync2/lib/gtest

tar xf %{S:5}
rmdir lib/AppImageUpdate/lib/zsync2/lib/args
mv args-* lib/AppImageUpdate/lib/zsync2/lib/args

%autopatch -p1

export CXXFLAGS="%{optflags} -I$(pwd)/lib/AppImageUpdate/lib/zsync2/include -Wno-error=deprecated-declarations"
%cmake \
	-DUSE_SYSTEM_LIBAPPIMAGE:BOOL=TRUE \
%ifarch %{aarch64}
	-Dbuild_32bit_preload_library:BOOL=FALSE \
%endif
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build
install -c -m 755 build/lib/AppImageUpdate/src/updater/libappimageupdate.so %{buildroot}%{_libdir}/
install -c -m 755 build/lib/AppImageUpdate/src/qt-ui/libappimageupdate-qt.so %{buildroot}%{_libdir}/

%files
%{_bindir}/AppImageLauncher
%{_bindir}/AppImageLauncherSettings
%{_bindir}/ail-cli
%{_bindir}/appimagelauncherd
%{_prefix}/lib/binfmt.d/appimagelauncher.conf
%{_userunitdir}/appimagelauncherd.service
%{_libdir}/appimagelauncher
%{_libdir}/libappimageupdate.so
%{_libdir}/libappimageupdate-qt.so
%{_datadir}/appimagelauncher
%{_datadir}/applications/appimagelauncher.desktop
%{_datadir}/applications/appimagelaunchersettings.desktop
%{_datadir}/icons/hicolor/*/*/AppImageLauncher.*
%{_mandir}/man1/AppImageLauncher.1*
%{_datadir}/mime/packages/appimage.xml
