# A Presentation View for PDF Presentations based on PyQt4 and Poppler

## Prerequisites
Needs pypoppler-qt4, get it [here](http://pyqt4-extrawidgets.googlecode.com/files/pypoppler-qt4-20962-fixed.tar.gz)
and install:
python configure.py
make
sudo make install

## Usage:
1. Run: python pdfpresenter.py
2. Move presentation view (black window) to projector/external display
3. Press 'f' to enter fullscreen mode
4. Press 'o' to open a file
5. Wait for caching to finish
6. Use right/left arrow keys to go to next/previous slide
7. Press 'q' to quit

## Notes:
1. Open presentation
2. Edit notes for each slide
3. Press ctrl+s to save notes

## TODO:
- Stopwatch
- Caching in background thread

## Screenshots:
[Screenshot 1](https://github.com/xlp/PdfPresenter/blob/master/screenshot1.png)
Right side is projector, left side is "your" view.
