from dataclasses import dataclass

from panda3d.core import TransparencyAttrib, ConfigVariableBool

from direct.showbase.DirectObject import DirectObject

from direct.gui import DirectGuiGlobals as DGG
DGG.BELOW = "below"

from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectCheckBox import DirectCheckBox
from DirectGuiExtension.DirectMenuItem import DirectMenuItem, DirectMenuItemEntry, DirectMenuItemSubMenu, DirectMenuSeparator
from DirectGuiExtension.DirectMenuBar import DirectMenuBar

@dataclass
class MenuItem:
    name: str
    entry_dict: dict

class FrameMenuBar(DirectMenuBar):
    def __init__(self, entries=[]):
        screenWidthPx = base.getSize()[0]

        #
        # Menubar
        #
        DirectMenuBar.__init__(
            self,
            frameColor=(0.25, 0.25, 0.25, 1),
            frameSize=(0,screenWidthPx,-12, 12),
            scale=(1,1,1),
            autoUpdateFrameSize=False,
            #pos=(0, 0, -12),
            itemMargin=(2,2,2,2),
            parent=base.pixel2d,
            menuItems=self.__get_menu_entries(entries)
            )

    def get_menu(self, name):
        return next(filter(
            lambda item: item["text"] == name,
            self["menuItems"]))

    def __get_menu_entries(self, entries):
        self.entries = entries
        menu_items = []

        for item in self.entries:
            menu_item_entries = self.__create_menu_item_entries(item.entry_dict)
            menu_item = self.__create_menu_item(item.name, menu_item_entries)
            menu_items.append(menu_item)

        return menu_items

    def set_entries(self, entries):
        for item in self["menuItems"]:
            item.destroy()

        self["menuItems"] = self.__get_menu_entries(entries)

    #TODO: This doesn't work yet, at least not for sub-menus
    '''
    def update_entry(self, entries):
        new_entries = self["menuItems"]
        for item in entries:
            menu_item_entries = self.__create_menu_item_entries(item.entry_dict)
            menu_item = self.__create_menu_item(item.name, menu_item_entries)

            existing_entry = self.get_menu(item.name)
            if existing_entry:
                new_entries[new_entries.index(existing_entry)] = menu_item
                self.removeItem(existing_entry)
                existing_entry.destroy()

        self["menuItems"] = new_entries
    '''

    def __create_menu_item_entries(self, entries):
        menu_entries = []
        for entry_name, entry in entries.items():
            if type(entry) == str:
                if entry == "---":
                    menu_entries.append(DirectMenuSeparator())
                else:
                    menu_entries.append(DirectMenuItemEntry(
                        entry_name, base.messenger.send, [entry]))
            elif type(entry) == list:
                menu_entries.append(DirectMenuItemEntry(entry_name, *entry))
            elif type(entry) == dict:
                sub_entries = self.__create_menu_item_entries(entry)
                menu_entries.append(
                    DirectMenuItemSubMenu(entry_name, sub_entries))
        return menu_entries

    def __create_menu_item(self, text, entries):
        color = (
            (0.25, 0.25, 0.25, 1), # Normal
            (0.35, 0.35, 1, 1), # Click
            (0.25, 0.25, 1, 1), # Hover
            (0.1, 0.1, 0.1, 1)) # Disabled

        sepColor = (0.7, 0.7, 0.7, 1)

        return DirectMenuItem(
            text=text,
            text_fg=(1,1,1,1),
            text_scale=0.8,
            items=entries,
            frameSize=(0,65/21,-7/21,17/21),
            frameColor=color,
            scale=21,
            relief=DGG.FLAT,
            item_text_fg=(1,1,1,1),
            item_text_scale=0.8,
            item_relief=DGG.FLAT,
            item_pad=(0.2, 0.2),
            itemFrameColor=color,
            separatorFrameColor=sepColor,
            popupMenu_itemMargin=(0,0,-.1,-.1),
            popupMenu_frameColor=color,
            highlightColor=color[2])
