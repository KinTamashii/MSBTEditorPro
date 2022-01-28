# MSBTEditorPro
IcySon55's Msbt Editor rewritten in python with extra features such as a readable control code format as well as import/export features.

Original Editor: (https://github.com/IcySon55/3DLandMSBTeditor)


## New Features

    Importing from CSV
    
    Auto Formatting (from "Clean" CSV)
    
    Batch Import/Export
    
    Readable Code Format
    
## Code Format Examples
 
    0E00 0000 0000 0600 0200 0200 6830 → <Ruby="{2:2}と">
 
    0E00 0000 0300 0400 2C64 FFFF → <Color="#2c64ffff">
    
    0E00 0000 0400 0000 → <PageBreak>
    
    0E00 0800 0000 0200 0C00 → <unk[8:0:12]>
    
## Usage
 
    python3.10 msbt_editor_pro.py


##Requirements

    Python 3.10
