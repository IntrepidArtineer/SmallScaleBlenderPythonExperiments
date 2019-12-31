#Original code from here: https://devtalk.blender.org/t/multiple-operator-modal-timers/8336
#Updated for Blender 2.81 by IntrepidArtisan, who did not write the original code.

import bpy

from bpy.props import (StringProperty, #These will get used later, and they're pretty common so might as well have them
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       CollectionProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       UIList,
                       )

# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------



# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------

class SCENE_OT_ModalTimerOperator1(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_timer_operator_1"
    bl_label = "Modal Timer Operator 1"

    _timer = None

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':
            # This timer event gets triggered from wm.modal_timer_operator_2
            print("event timer")

        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(1.0, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
    
    
class SCENE_OT_ModalTimerOperator2(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_timer_operator_2"
    bl_label = "Modal Timer Operator 2"

    _timer = None

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':
            pass

        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(5.0, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

    
# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------
#Added this panel for accessability - IA
class EXAMPLE_PT_MainPanel(Panel): #It's important to have PT somewhere in the panel name
    bl_label = "Example Panel"
    bl_idname = "EXAMPLE_PT_MainPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Example" #You can replace serial in this line with any other word you want
    bl_context = "objectmode"
    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.object

        layout.operator("wm.modal_timer_operator_1")
        layout.operator("wm.modal_timer_operator_2")

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = ( #list all your classes here so you don't have to register them individually later
    SCENE_OT_ModalTimerOperator1,
    SCENE_OT_ModalTimerOperator2,
    EXAMPLE_PT_MainPanel, #Order matters here
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    register()