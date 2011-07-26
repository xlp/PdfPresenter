#!/bin/sh

export LC_ALL=C

# track return code
rc=0

#TODO check if packages are already installed
echo "Installing required packages"
# install required packages
# check if ubuntu (:sudo) or debian (:su) is running
/usr/bin/lsb_release -i|/bin/grep "Ubuntu" && PRIV="/usr/bin/sudo -i"
/usr/bin/lsb_release -i|/bin/grep "Debian" && PRIV="/bin/su root -c"
$PRIV "/usr/bin/aptitude install libpoppler-qt4-dev pyqt4-dev-tools python-qt4-dev python-sip-dev"
# install pypoppler-qt4
/usr/bin/wget http://pyqt4-extrawidgets.googlecode.com/files/pypoppler-qt4-20962-fixed.tar.gz
/bin/tar xvzf pypoppler-qt4-20962-fixed.tar.gz 
/bin/rm -f pypoppler-qt4-20962-fixed.tar.gz
cd pypoppler-qt4
echo "Configuring pypoppler-qt4 ..."
/usr/bin/python configure.py
/usr/bin/make
echo "Installing pypoppler-qt4 ..."
$PRIV "/usr/bin/make install"
cd -
# prepare start of pdfpresenter.py
/bin/chmod +x pdfpresenter.py
echo "
[x] DONE

Usage:
1. Run: ./pdfpresenter.py
2. Focus on black window
3. Press 'o' to open a file
4. Move presentation view to projector/external display
5. Press 'f' to enter fullscreen mode
6. Wait for caching to finish
7. Use right/left arrow keys to go to next/previous slide"

exit $rc
