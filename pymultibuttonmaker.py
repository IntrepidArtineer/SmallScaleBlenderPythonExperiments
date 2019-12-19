import bpy

#Original Code found here: https://blender.stackexchange.com/questions/57545/can-i-make-a-ui-button-that-makes-buttons-in-a-panel
#Updated for Blender 2.81 by IntrepidArtisan on 12/19/19, who did not write the original code

# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

class SceneItems(bpy.types.PropertyGroup):
    value: bpy.props.IntProperty()

# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------

class MAKER_OT_AddButtonOperator(bpy.types.Operator):
    bl_idname = "scene.add_button_operator"
    bl_label = "Add Button"

    def execute(self, context):
        id = len(context.scene.buttonCollection)
        new = context.scene.buttonCollection.add()
        new.name = str(id)
        new.value = id
        return {'FINISHED'}

class MAKER_OT_ButtonOperator(bpy.types.Operator):
    bl_idname = "scene.button_operator"
    bl_label = "Button"

    id = bpy.props.IntProperty()

    def execute(self, context):
        print("Pressed button ", self.id)
        return {'FINISHED'}

# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------

class MAKER_PT_FancyPanel(bpy.types.Panel):
    bl_label = "Fancy Panel"
    bl_idname = "MAKER_PT_FancyPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Maker"
    bl_context = "objectmode"

    def draw(self, context):
        self.layout.operator("scene.add_button_operator")
        for item in context.scene.buttonCollection:
               self.layout.operator("scene.button_operator", text="Button #"+item.name).id = item.value

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    SceneItems,
    MAKER_OT_AddButtonOperator,
    MAKER_OT_ButtonOperator,
    MAKER_PT_FancyPanel
)

def register():

    #Blender 2.81
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.buttonCollection = bpy.props.CollectionProperty(type=SceneItems)

def unregister():
    #Blender 2.81
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.buttonCollection

if __name__ == "__main__":
    register()