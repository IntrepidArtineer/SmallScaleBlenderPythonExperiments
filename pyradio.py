import bpy
import math

# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

class InterfaceVars(bpy.types.PropertyGroup):
    angles: bpy.props.EnumProperty(
        items=[
            ('15', '15', '15', '', 0),
            ('30', '30', '30', '', 1),
            ('60', '60', '60', '', 2),
            ('90', '90', '90', '', 3),
            ('120', '120', '120', '', 4),
        ],
        default='15'
    )
    direction: bpy.props.EnumProperty(
        items=[
            ('cw', '', 'CW', 'LOOP_FORWARDS', 0),
            ('ccw', '', 'CCW', 'LOOP_BACK', 1)
        ],
        default='cw'
    )

# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------
    
class EXAMPLE_OT_Rotation(bpy.types.Operator):
    bl_idname = "object.examplerotation"
    bl_label = "Rotate"
 
    def execute(self, context):
        rotationvalue = int(context.window_manager.interface_vars.angles)
        if context.window_manager.interface_vars.direction == 'ccw':
            rotationvalue = -rotationvalue
        bpy.ops.transform.rotate(value=rotationvalue*math.pi/180, axis=(0, 0, 1)) 
        return {'FINISHED'}

# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------
 
class EXAMPLE_PT_RotationPanel(bpy.types.Panel):
    bl_context = "objectmode"
    bl_idname = "object.examplerotationpanel"
    bl_label = "RotationPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    #bl_category = "ExampleRotationPanel" #no idea what this line actually does, but the compiler didn't like it so I commented it out
 
    def draw(self, context):
        row = self.layout.row()
        row.prop(context.window_manager.interface_vars, 'angles', expand=True)
        row.prop(context.window_manager.interface_vars, 'direction', expand=True)
        self.layout.operator("object.rotation", text="Rotate")
    
# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = ( #list all your classes here so you don't have to register them individually later
    InterfaceVars,
    EXAMPLE_OT_Rotation,
    EXAMPLE_PT_RotationPanel,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.WindowManager.interface_vars = bpy.props.PointerProperty(type=InterfaceVars)
    
def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.WindowManager.interface_vars
    
if __name__ == "__main__":
    register()