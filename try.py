import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

fm.findSystemFonts(fontpaths=None, fontext="ttf")
for font in fm.findSystemFonts(fontpaths=None, fontext="ttf"):
    print(fm.FontProperties(fname=font).get_name(), font)
