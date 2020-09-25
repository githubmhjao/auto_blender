import bpy

# TODO: set node location
# TODO: bpy.data.materials["Material"].node_tree.nodes["Principled BSDF"]

current_mater = bpy.context.object.active_material
shade_bsdf = current_mater.node_tree.nodes.get("Principled BSDF")

input_tex_coord = current_mater.node_tree.nodes.new("ShaderNodeTexCoord")
input_tex_coord.location = ()
vecto_mapping = current_mater.node_tree.nodes.new("ShaderNodeMapping")

textu_voronoi = current_mater.node_tree.nodes.new("ShaderNodeTexVoronoi")
textu_voronoi.feature = "DISTANCE_TO_EDGE"

conve_val_rgb = current_mater.node_tree.nodes.new("ShaderNodeValToRGB")
conve_val_rgb.color_ramp.elements[0].position = 0.02
conve_val_rgb.color_ramp.elements[1].position = 0.1


vecto_bump = current_mater.node_tree.nodes.new("ShaderNodeBump")

current_mater.node_tree.links.new(input_tex_coord.outputs[3], vecto_mapping.inputs[0])
current_mater.node_tree.links.new(vecto_mapping.outputs[0], textu_voronoi.inputs[0])
current_mater.node_tree.links.new(textu_voronoi.outputs[0], conve_val_rgb.inputs[0])
current_mater.node_tree.links.new(conve_val_rgb.outputs[0], vecto_bump.inputs[2])
current_mater.node_tree.links.new(vecto_bump.outputs[0], shade_bsdf.inputs[19])
current_mater.node_tree.links.new(conve_val_rgb.outputs[0], shade_bsdf.inputs[0])
