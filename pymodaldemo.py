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

class EXAMPLE_OT_MyOperator(Operator):
    """Modal Tester"""
    bl_idname = "scene.myoperator"
    bl_label = "myoperator"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return {'FINISHED'}
    
    def modal(self, context, event):
        scene = context.scene
        if event.type == 'WHEELUPMOUSE':
            scene.serialtool.example_float += 0.2
        elif event.type == 'WHEELDOWNMOUSE':
            scene.serialtool.example_float -= 0.2
        elif event.type == 'LEFTMOUSE':
            print('test')
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            return {'CANCELLED'}
        else:
            return {'RUNNING_MODAL'}
        
        return {'RUNNING_MODAL'}
    
    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self) #THIS LINE IS IMPORTANT
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
        layout.operator("scene.myoperator")


classes = ( #list all your classes here so you don't have to register them individually later
    EXAMPLE_OT_MyOperator,
    SerialProperties,
    SERIAL_PT_MainPanel, #Order matters here
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
    del bpy.types.Scene.serialtool

if __name__ == "__main__":
    register()