bl_info = {
    "name": "Get Snapshot of Arduino Values",
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

#Referenced this: https://create.arduino.cc/projecthub/cmbrooks/serial-pong-72670c?ref=search&ref_id=serial%20pong&offset=0

import bpy
import serial
import time

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
    serial_int1: IntProperty(
        name="serial intvalue 1",
        description="",
        default=0
        )
    serial_int2: IntProperty(
        name="serial intvalue 2",
        description="",
        default=0
    )

# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------

class WM_OT_Serial(Operator):
    bl_label = "Off"
    bl_idname = "wm.serial"

    def read_serial(self, device):
        #Read serial data
        device.readline()
        time.sleep(2)
        raw_line = device.readline()
        line = str(raw_line)
        line = line[2:] #Remove the unicode characters
        line = line[:-5] #Remove the cariage return and newline from the end of the string
        data = line.split(" ")
        #Convert parsed strings into integers
        try:
            print(raw_line)
            print(line)
            p1_pot = int(data[0])
            p2_pot = int(data[1])
            print("arbuckle")
            return p1_pot, p2_pot, True
        except:
            return -1, -1, False

    def execute(self, context):
        scene = context.scene
        serialtool = scene.serialtool
        
# Start main program
        try:
            print("bawk")
            serial_device = serial.Serial()
            print("quack")
            serial_device.baudrate = 9600
            serial_device.port = 'COM5'
            serial_device.timeout = 1
            print("bark")
            if serial_device.isOpen():
                pass
            else:
                serial_device.open()
            print("jet set radio")
            serial_device.readline()
            print("moo")
        except:
            print("No serial device found")
            #exit()

        p1_pot, p2_pot, data_received = self.read_serial(serial_device)
        if data_received == True:
            serialtool.serial_int1 = int(p1_pot)
            serialtool.serial_int2 = int(p2_pot)
            serial_device.close()

        return {'FINISHED'}

# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------
     
class SERIAL_PT_MainPanel(Panel):
    bl_label = "Serial Panel"
    bl_idname = "SERIAL_PT_MainPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Serial"
    bl_context = "objectmode"
    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        serialtool = scene.serialtool
        layout.operator("wm.serial")
        layout.prop(serialtool, "serial_int1")
        layout.prop(serialtool, "serial_int2")

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    SerialProperties,
    SERIAL_PT_MainPanel,
    WM_OT_Serial,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.serialtool = PointerProperty(type=SerialProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.serialtool

if __name__ == "__main__":
    register()