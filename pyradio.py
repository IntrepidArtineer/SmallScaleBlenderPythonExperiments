#Original Code: https://b3d.interplanety.org/en/creating-radio-buttons-in-the-blender-add-ons-interface/
#Code has been updated for Blender 2.81
#Updated by IntrepidArtisan, who is not the author of the original code

import bpy
import math

from math import isclose
from mathutils import Matrix, Vector

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
    bl_idname = "object.rotation"
    bl_label = "Rotate"
    
    def create_z_orient(self,rot_vec):
        x_dir_p = Vector(( 1.0,  0.0,  0.0))
        y_dir_p = Vector(( 0.0,  1.0,  0.0))
        z_dir_p = Vector(( 0.0,  0.0,  1.0))
        tol = 0.001
        rx, ry, rz = rot_vec
        if isclose(rx, 0.0, abs_tol=tol) and isclose(ry, 0.0, abs_tol=tol):
            if isclose(rz, 0.0, abs_tol=tol) or isclose(rz, 1.0, abs_tol=tol):
                return Matrix((x_dir_p, y_dir_p, z_dir_p))  # 3x3 identity
        new_z = rot_vec.copy()  # rot_vec already normalized
        new_y = new_z.cross(z_dir_p)
        new_y_eq_0_0_0 = True
        for v in new_y:
            if not isclose(v, 0.0, abs_tol=tol):
                new_y_eq_0_0_0 = False
                break
        if new_y_eq_0_0_0:
            new_y = y_dir_p
        new_x = new_y.cross(new_z)
        new_x.normalize()
        new_y.normalize()
        return Matrix(((new_x.x, new_y.x, new_z.x),
                       (new_x.y, new_y.y, new_z.y),
                       (new_x.z, new_y.z, new_z.z)))
 
    def execute(self, context):
        rotationvalue = int(context.window_manager.interface_vars.angles)
        if context.window_manager.interface_vars.direction == 'ccw':
            rotationvalue = -rotationvalue
        bpy.ops.transform.rotate(value=rotationvalue*math.pi/180, orient_matrix=(self.create_z_orient(rot_vec=((0.0, 0.0, 1.0)))), orient_axis='Z')
        return {'FINISHED'}

# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------
 
class EXAMPLE_PT_RotationPanel(bpy.types.Panel):
    bl_context = "objectmode"
    bl_idname = "object.rotationpanel"
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