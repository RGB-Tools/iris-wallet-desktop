#!/bin/sh
# App name
PROJECT_NAME=$(grep 'APP_NAME' ./src/utils/constant.py | awk -F'=' '{print $2}' | tr -d ' "' | xargs)
VERSION=$(grep '__version__' ./src/version.py | awk -F'=' '{print $2}' | tr -d ' "' | xargs)
BITCOIN_NETWORK=$(grep '__network__' ./src/flavour.py | awk -F'=' '{print $2}' | tr -d ' "' | xargs)
echo $BITCOIN_NETWORK
if [ -f "$PROJECT_NAME.deb" ]; then
    rm -rf "$PROJECT_NAME.deb"
else
    echo "File not found: ./$PROJECT_NAME.deb"
fi

#remove already exits file and dir
rm -rf build
rm -rf dist
rm -rf package

#check fpm installed
fpm --version

poetry run pyinstaller iris_wallet_desktop.spec

# Create folders
[ -e package ] && rm -r package
mkdir -p package/opt
mkdir -p package/usr/share/applications
mkdir -p package/usr/share/icons/hicolor/scalable/apps

# Copy the executable
cp -r dist/$PROJECT_NAME package/opt/$PROJECT_NAME
chmod +x package/opt/$PROJECT_NAME/$PROJECT_NAME

# Copy the icon
cp ./src/assets/icons/$BITCOIN_NETWORK-icon.svg package/usr/share/icons/hicolor/scalable/apps/iriswallet_icon.svg
# Create the desktop entry
cat <<EOF >package/usr/share/applications/$PROJECT_NAME.desktop
[Desktop Entry]
Version=$VERSION
Type=Application
Name=$PROJECT_NAME
Comment=IrisWallet - A cryptocurrency wallet application.
Path=/opt/$PROJECT_NAME
Exec=/opt/$PROJECT_NAME/$PROJECT_NAME
Icon=iriswallet_icon.svg
License=MIT
Description=IrisWallet - A cryptocurrency wallet application.
Categories=Utility;
EOF

# Set permissions
find package/opt/$PROJECT_NAME -type f -exec chmod 755 -- {} +
find package/opt/$PROJECT_NAME -type d -exec chmod 755 -- {} +
find package/usr/share -type f -exec chmod 644 -- {} +

# Create .fpm configuration file
cat <<EOF >./.fpm
-C package
-s dir
-t deb
-n $PROJECT_NAME
-v $VERSION
-p $PROJECT_NAME.deb
EOF

fpm
