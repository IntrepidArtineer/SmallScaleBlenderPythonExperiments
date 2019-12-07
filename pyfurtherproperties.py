bl_info = {
    "name": "Add a Sidebar Tab and a Panel",
    "description": "Demonstration of Adding a Sidebar Tab and Panel to Blender",
    "author": "IntrepidArtineer",
    "version": (0, 0, 1),
    "blender": (2, 81, 0),
    "location": "3D View > Tools",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development"
}


import bpy

from bpy.props import (StringProperty, #These will get used later, and they're pretty common so might as well have them
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )

# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

class SerialProperties(PropertyGroup):     
    serial_freeze_bool: BoolProperty( #This property just demonstrates how to make a check box. It doesn't do anything else yet
        name="Freeze",
        description="Temporarily Stop All Transmission",
        default = True
        )
    serial_receiving_profiles: EnumProperty( #This creates an EnumProperty. It looks like a Visual Studio ComboBox when drawn
        name="Receiving Profile",
        description="Pick a receiving Profile",
        items=[ ('OP40', "3D Mouse", ""),
                ('OP50', "Human Doll", ""),
                ('OP60', "Dog Doll", ""),
                ('OP70', "Dragon Doll", ""),
                ('OP80', "Horse Doll", ""),
                ('OP90', "Lemur Foot Prototype No. 1", "")
                ]
        )
    my_path: StringProperty( #Use this to declare a property for opening a file path
        name = "Profile File",
        description="Choose a directory",
        default="",
        maxlen=1024,
        subtype='DIR_PATH' #This line is what makes a difference
        )
    data_value_int: IntProperty(
        name = "Received Data As Int",
        description = "Received Data Value As An Integer",
        default = 0,
        )

# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------
     
class SERIAL_PT_MainPanel(Panel): #It's imprtant to have PT somewhere in the panel name
    bl_label = "Serial Panel"
    bl_idname = "SERIAL_PT_MainPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Serial" #You can replace serial in this line with any other word you want
    bl_context = "objectmode"
    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        serialtool = scene.serialtool
        
        layout.prop(serialtool, "serial_freeze_bool") #This adds the property as a checkbox to the layout of the panel as it is drawn.
        layout.prop(serialtool, "serial_receiving_profiles")
        layout.prop(serialtool, "my_path") #This comes complete with a label giving the property's name and a button to open a file browser window
        layout.prop(serialtool, "data_value_int")


# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = ( #list all your classes here so you don't have to register them individually later
    SerialProperties,
    SERIAL_PT_MainPanel
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.serialtool = PointerProperty(type=SerialProperties) #You have to tell Blender what the properties apply to

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.serialtool #Don't forget to unregister your stuff when it's time to

if __name__ == "__main__":
    register()