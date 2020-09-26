import bpy

# TODO: bpy.data.materials["Material"].node_tree.nodes["Principled BSDF"]
# TODO: bpy.data.materials.new("VoronoiSimple")

mater = bpy.data.materials["Material"]
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
