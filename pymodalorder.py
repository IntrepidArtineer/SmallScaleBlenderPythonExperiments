import bpy

from bpy.props import (PointerProperty,
                       FloatProperty
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )

class SerialProperties(PropertyGroup):
    example_float: FloatProperty(
        name="User Input Float",
        description="Float to send to new item",
        default = 0.0
    )


class ModalOperator(bpy.types.Operator):
    bl_idname = "object.modal_operator"
    bl_label = "Simple Modal Operator"

    def __init__(self):
        print("Start")

    def __del__(self):
        print("End")

    def execute(self, context):
        context.object.location.x = self.value / 100.0
        return {'FINISHED'}

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':  # Apply
            self.value = event.mouse_x
            context.scene.serialtool.example_float = event.mouse_x
            self.execute(context)
        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancel
            context.object.location.x = self.init_loc_x
            context.scene.serialtool.example_float = self.init_loc_x
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.init_loc_x = context.object.location.x
        self.value = event.mouse_x
        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class SERIAL_PT_MainPanel(Panel):
    bl_label = "Serial Panel"
    bl_idname = "SERIAL_PT_MainPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Serial" #You can replace serial in this line with any other word you want
    #bl_context = "objectmode"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        serialtool = scene.serialtool

        layout.prop(serialtool, "example_float")
        layout.operator("object.modal_operator")

classes = ( #list all your classes here so you don't have to register them individually later
    ModalOperator,
    SerialProperties,
    SERIAL_PT_MainPanel, #Order matters here
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

# test call
#bpy.ops.object.modal_operator('INVOKE_DEFAULT')
if __name__ == "__main__":
    register()