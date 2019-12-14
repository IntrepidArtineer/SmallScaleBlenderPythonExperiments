#Original code from here:https://blog.hamaluik.ca/posts/dynamic-blender-properties/
#Modified to work for Blender 2.81, December 13, 2019

import bpy
from bpy.props import FloatProperty, StringProperty, IntProperty, BoolProperty, PointerProperty
from bpy.types import PropertyGroup

# TODO: load dynamically at runtime from a JSON file!
bpy.propertyGroupLayouts = {
    "Health": [
        { "name": "current", "type": "float" },
        { "name": "max", "type": "float" }
    ],
    "Character": [
        { "name": "first_name", "type": "string" },
        { "name": "last_name", "type": "string" }
    ],
    "Potentiometer": [
        { "name": "value", "type": "int"},
    ]
}
bpy.samplePropertyGroups = {}

class MULTI_PT_SamplePanel(bpy.types.Panel):
    bl_label = "Sample Panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        # use our layout definition to dynamically create our panel items
        for groupName, attributeDefinitions in bpy.propertyGroupLayouts.items():
            # get the instance of our group
            # dynamic equivalent of `obj.samplePropertyGroup` from before
            propertyGroup = getattr(obj, groupName)

            # start laying this group out
            col = layout.column()
            col.label(text=groupName)

            # loop through all the attributes and show them
            for attributeDefinition in attributeDefinitions:
                col.prop(propertyGroup, attributeDefinition["name"])

            # draw a separation between groups
            layout.separator()

classes = (
    MULTI_PT_SamplePanel,
)

def register():

    #Blender 2.81
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    # iterate over our list of property groups
    for groupName, attributeDefinitions in bpy.propertyGroupLayouts.items():
        # build the attribute dictionary for this group
        attributes = {}
        for attributeDefinition in attributeDefinitions:
            attType = attributeDefinition['type']
            attName = attributeDefinition['name']
            if attType == 'float':
                attributes[attName] = FloatProperty(name=attName.title())
            elif attType == 'string':
                attributes[attName] = StringProperty(name=attName.title())
            elif attType == 'int':
                attributes[attName] = IntProperty(name=attName.title())
            elif attType == 'bool':
                attributes[attName] = BoolProperty(name=attName.title())
            else:
                raise TypeError('Unsupported type (%s) for %s on %s!' % (attType, attName, groupName))

        # now build the property group class
        propertyGroupClass = type(groupName, (PropertyGroup,), attributes)

        # register it with Blender
        #bpy.utils.register_class(propertyGroupClass)
        register_class(propertyGroupClass)

        # apply it to all Objects
        setattr(bpy.types.Object, groupName, PointerProperty(type=propertyGroupClass))

        # store it for later
        bpy.samplePropertyGroups[groupName] = propertyGroupClass

def unregister():
    #Blender 2.81
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    # unregister the panel class
    #bpy.utils.unregister_class(SamplePanel)

    # unregister our components
    try:
        for key, value in bpy.samplePropertyGroups.items():
            delattr(bpy.types.Object, key)
            unregister_class(value)
    except UnboundLocalError:
        pass
    bpy.samplePropertyGroups = {}

if __name__ == "__main__":
    register()