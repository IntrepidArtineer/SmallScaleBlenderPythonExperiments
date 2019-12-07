#Copied from here: https://blenderartists.org/t/creating-collectionproperties-for-custom-uilist-classes/615645
#But adjustments had to be made to make it work in Blender 2.81 for some reason

import bpy
import random
from bpy.props import IntProperty, EnumProperty, CollectionProperty, PointerProperty
from bpy.types import PropertyGroup, UIList, Panel, Operator


class ExampleEntry(PropertyGroup):
    type = EnumProperty(
        items=(
            ('A', "Option A", ""),
            ('B', "Option B", ""),
        )
    )
    val = IntProperty()
    

class ExampleGroup(PropertyGroup):
    coll = CollectionProperty(type=ExampleEntry)
    index = IntProperty()


class SCENE_UL_list(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(item, "name", text="", emboss=False)
            layout.prop(item, "val", text="")
            layout.prop(item, "type", text="")
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)


class SCENE_OT_list_populate(Operator):
    bl_idname = "scene.list_populate"
    bl_label = "Populate list"
    
    def execute(self, context):
        for i in range(3):
            item = context.scene.prop_group.coll.add()
            item.name = random.sample(("foo", "bar", "asdf"), 1)[0]
            item.val = random.randint(1, 100)
            item.type = 'A' if random.random() > 0.5 else 'B'
            
        return {'FINISHED'}

class SCENE_PT_list(Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "UIList Panel"
    bl_idname = "SCENE_PT_list"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        sce = context.scene

        layout.operator("scene.list_populate")
        layout.template_list("SCENE_UL_list", "", sce.prop_group, "coll", sce.prop_group, "index")

classes = ( #list all your classes here so you don't have to register them individually later
    ExampleEntry,
    ExampleGroup,
    SCENE_UL_list,
    SCENE_OT_list_populate,
    SCENE_PT_list
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.prop_group = PointerProperty(type=ExampleGroup)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.prop_group

if __name__ == "__main__":
    register()