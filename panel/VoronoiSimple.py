import bpy


class MyProperties(bpy.types.PropertyGroup):
    
    my_string : bpy.props.StringProperty(name= "Name", default="ShaderName")
    
    my_float_vector : bpy.props.FloatVectorProperty(name= "Color", subtype="COLOR_GAMMA", size=4, default=(0.8, 0.8, 0.8, 1))

    
class ADDONNAME_PT_main_panel(bpy.types.Panel):
    bl_label = "Hello World Panel"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "AutoShader"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        
        layout.prop(mytool, "my_string")
        layout.prop(mytool, "my_float_vector")
        
        layout.operator("addonname.myop_operator")
        

class ADDONNAME_OT_my_op(bpy.types.Operator):
    bl_label = "Create Shader"
    bl_idname = "addonname.myop_operator"
    
    def execute(self, context):
        def create_shader(name, color):
            mater = bpy.data.materials.new(name)
            mater.use_nodes = True
            shade_bsdf = mater.node_tree.nodes.get("Principled BSDF")

            input_tex_coord = mater.node_tree.nodes.new("ShaderNodeTexCoord")
            vecto_mapping = mater.node_tree.nodes.new("ShaderNodeMapping")

            textu_voronoi = mater.node_tree.nodes.new("ShaderNodeTexVoronoi")
            textu_voronoi.feature = "DISTANCE_TO_EDGE"

            conve_val_rgb = mater.node_tree.nodes.new("ShaderNodeValToRGB")
            conve_val_rgb.color_ramp.elements[0].position = 0.02
            conve_val_rgb.color_ramp.elements[1].position = 0.1

            vecto_bump = mater.node_tree.nodes.new("ShaderNodeBump")

            mater.node_tree.links.new(input_tex_coord.outputs[3], vecto_mapping.inputs[0])
            mater.node_tree.links.new(vecto_mapping.outputs[0], textu_voronoi.inputs[0])
            mater.node_tree.links.new(textu_voronoi.outputs[0], conve_val_rgb.inputs[0])
            mater.node_tree.links.new(conve_val_rgb.outputs[0], vecto_bump.inputs[2])
            mater.node_tree.links.new(vecto_bump.outputs[0], shade_bsdf.inputs[19])
            mater.node_tree.links.new(conve_val_rgb.outputs[0], shade_bsdf.inputs[0])

            nodes_list = [input_tex_coord, vecto_mapping, textu_voronoi, conve_val_rgb, vecto_bump]
            for i, node in enumerate(nodes_list):
                node.location = (-(len(nodes_list)-i) * 200, 300)

        scene = context.scene
        mytool = scene.my_tool
        
        create_shader(mytool.my_string, mytool.my_float_vector)
        
        return {'FINISHED'}
    
    
classes = [MyProperties, ADDONNAME_PT_main_panel, ADDONNAME_OT_my_op]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.Scene.my_tool = bpy.props.PointerProperty(type= MyProperties)
 
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        del bpy.types.Scene.my_tool


if __name__ == "__main__":
    register()
