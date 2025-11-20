#!/bin/bash

# App name
PROJECT_NAME=$(grep 'APP_NAME' ./src/utils/constant.py | awk -F'=' '{print $2}' | tr -d ' "' | xargs)
VERSION=$(grep '__version__' ./src/version.py | awk -F'=' '{print $2}' | tr -d ' "' | xargs)
BITCOIN_NETWORK=$(grep '__network__' ./src/flavour.py | awk -F'=' '{print $2}' | tr -d ' "' | xargs)
echo $BITCOIN_NETWORK
APPDIR="AppDir"
ICON_DIR="$APPDIR/usr/share/icons/hicolor/256x256/apps"
ICON_NAME="iriswallet.png"
PROJECT_NAME_WITH_VERSION="${PROJECT_NAME}-${VERSION}"
#remove already exits file and dir
rm -rf build
rm -rf dist
rm -rf AppDir
rm -rf *.AppImage  # Full path to the icon file

# Ensure the necessary development packages are installed
#if ! dpkg -s python3-dev &> /dev/null; then
#    echo "python3.12-dev not found. Installing..."
#    sudo apt-get install python3-dev
#fi

# Ensure the libfuse2 package is installed
#if ! dpkg -s libfuse2 &> /dev/null; then
#    echo "libfuse2 not found. Installing..."
#    sudo apt-get install libfuse2
#fi

# Ensure the AppImage tools are installed
if ! command -v appimagetool &> /dev/null; then
    echo "appimagetool not found. Downloading..."
    wget -q https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage
    if [ ! -f appimagetool-x86_64.AppImage ]; then
        echo "Error: Failed to download appimagetool."
        exit 1
    fi
    chmod +x appimagetool-x86_64.AppImage
    APPIMAGETOOL=./appimagetool-x86_64.AppImage
else
    APPIMAGETOOL=$(which appimagetool)
fi

# Run PyInstaller
poetry run pyinstaller iris_wallet_desktop.spec

# Verify the build was successful
if [ ! -d "dist/$PROJECT_NAME" ]; then
    echo "Error: PyInstaller build failed."
    exit 1
fi

# Create AppDir structure
mkdir -p $APPDIR/usr/bin
mkdir -p $ICON_DIR

# Copy application files
cp -r dist/$PROJECT_NAME/* $APPDIR/usr/bin/

# Copy icon
cp ./src/assets/icons/$BITCOIN_NETWORK-icon.png $ICON_DIR/$ICON_NAME
cp ./src/assets/icons/$BITCOIN_NETWORK-icon.png $APPDIR/iriswallet_icon.png

# Create .desktop file
cat > $APPDIR/$PROJECT_NAME.desktop << EOF
[Desktop Entry]
Name=$PROJECT_NAME_WITH_VERSION
Exec=AppRun
Icon=iriswallet_icon
Type=Application
Categories=Utility;
EOF

# Create AppRun file
cat > $APPDIR/AppRun << EOF
#!/bin/bash
HERE="\$(dirname "\$(readlink -f "\${0}")")"

# Set environment variables for file paths
export XDG_DOWNLOAD_DIR="\$HOME/Downloads"

exec "\$HERE/usr/bin/$PROJECT_NAME" "\$@"
EOF
chmod +x $APPDIR/AppRun

# Build the AppImage
if [ -f "$APPIMAGETOOL" ]; then
    echo "Building AppImage..."
    $APPIMAGETOOL $APPDIR
else
    echo "Error: appimagetool not found."
    exit 1
fi

echo "AppImage created successfully."
