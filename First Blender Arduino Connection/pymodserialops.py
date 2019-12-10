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
import serial

ser = serial.Serial()

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
    serial_int: IntProperty(
        name="intvalue",
        description="",
        default=0
        )

# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------

def getValues():
    
    ser.write(b'g')
    arduinoData = ser.readline().decode('ascii')
    return arduinoData

class ModalOperator(bpy.types.Operator):
    bl_idname = "scene.modal_operator"
    bl_label = "Simple Modal Operator"
    
    def __init__(self):
        print("Start")
    
    def __del__(self):
        print("End")
    
    def execute(self, context):
        
        context.object.location.x = self.value / 100.0
        
        scene = context.scene
        serialtool = scene.serialtool
        ser.baudrate = 9600
        ser.port = 'COM5'
        ser.timeout = 1
        
        if ser.is_open == False:
            ser.open()
        b = ser.readline()
        str_rn = b.decode()
        strexa = str_rn.rstrip()
        if strexa == '':
            serialtool.serial_int = serialtool.serial_int
        else:
            serialtool.serial_int = int(strexa)
        return {'FINISHED'}
    
    def modal(self, context, event):
        scene = context.scene
        if event.type == 'MOUSEMOVE': #Apply
            self.value = event.mouse_x
            self.execute(context)
        elif event.type == 'LEFTMOUSE': #confirm
            scene = context.scene
            serialtool = scene.serialtool
            b = ser.readline()
            str_rn = b.decode()
            strexa = str_rn.rstrip()
            if strexa == '':
                serialtool.serial_int = serialtool.serial_int
            else:
                serialtool.serial_int = int(strexa)
            ser.close()
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}: #cancell
            context.object.location.x = self.init_loc_x
            ser.close()
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.init_loc_x = context.object.location.x
        self.value = event.mouse_x
        self.execute(context)

        context.window_manager.modal_handler_add(self)
        
        ser.baudrate = 9600
        ser.port = 'COM5'
        ser.timeout = 1
        #ser.open()
        
        return {'RUNNING_MODAL'}

# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------
     
class SERIAL_PT_MainPanel(Panel): #It's important to have PT somewhere in the panel name
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
        layout.prop(serialtool, "serial_int")
        layout.operator("scene.modal_operator")


# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = ( #list all your classes here so you don't have to register them individually later
    SerialProperties,
    ModalOperator,
    SERIAL_PT_MainPanel
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.serialtool = PointerProperty(type=SerialProperties) #You have to tell Blender what the properties apply to
    ser.baudrate = 9600
    ser.port = 'COM5'
    ser.timeout = 1
    #ser.open()

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.serialtool #Don't forget to unregister your stuff when it's time to

if __name__ == "__main__":
    register()