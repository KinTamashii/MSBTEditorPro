# MSBTEditorPro
IcySon55's Msbt Editor rewritten in python with extra features such as a readable control code format as well as import/export features.

Original Editor: (https://github.com/IcySon55/3DLandMSBTeditor)


# New Features

    Importing from CSV
    
    Importing to and Exporting (via Auto Formatting) from clean .txt files.
    
    Batch Import/Export
    
    Readable Code Format
    
# Code Format Examples
 
    0E00 0000 0000 0600 0200 0200 6830 → <Ruby="{2:2}と">
 
    0E00 0000 0300 0400 2C64 FFFF → <Color="#2c64ffff">
    
    0E00 0000 0400 0000 → <PageBreak>
    
    0E00 0800 0000 0200 0C00 → <unk[8:0:12]>
    
# Usage
   ## Execute
    python3.10 msbt_editor_pro.py
    
   ## Clean Strings
   After exporting msbt to a "clean" .txt file, the first line will include a mode for the Auto Formatter to use when the file is imported again.
   By default this is 0, which adds in PageBreaks and newlines (calculated by approximating the text width) in addition to the original codes.
   Mode 1 only adds the newlines and original codes.
   Mode 2 only adds the original codes.
   Mode 3 doesn't format the strings.


# Requirements

    Python 3.10
    pillow
