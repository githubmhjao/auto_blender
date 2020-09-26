import bpy

# TODO: bpy.data.materials["Material"].node_tree.nodes["Principled BSDF"]
# TODO: bpy.data.objects['Cube'].active_material

mater = bpy.data.materials.new("VoronoiCrackle")
bpy.data.objects['Cube'].active_material = mater
mater.use_nodes = True
shade_bsdf = mater.node_tree.nodes.get("Principled BSDF")

input_tex_coord = mater.node_tree.nodes.new("ShaderNodeTexCoord")
vecto_mapping = mater.node_tree.nodes.new("ShaderNodeMapping")
input_value = mater.node_tree.nodes.new("ShaderNodeValue")
input_value.outputs[0].default_value = 5

textu_voronoi_F1 = mater.node_tree.nodes.new("ShaderNodeTexVoronoi")
textu_voronoi_F1.distance = "CHEBYCHEV"

textu_voronoi_F2 = mater.node_tree.nodes.new("ShaderNodeTexVoronoi")
textu_voronoi_F2.feature = "F2"
textu_voronoi_F2.distance = "CHEBYCHEV"

conve_math = mater.node_tree.nodes.new("ShaderNodeMath")
conve_math.operation = "SUBTRACT"

conve_val_rgb = mater.node_tree.nodes.new("ShaderNodeValToRGB")
conve_val_rgb.color_ramp.elements[0].position = 0.02
conve_val_rgb.color_ramp.elements[1].position = 0.1

vecto_bump = mater.node_tree.nodes.new("ShaderNodeBump")

mater.node_tree.links.new(input_tex_coord.outputs[3], vecto_mapping.inputs[0])
mater.node_tree.links.new(vecto_mapping.outputs[0], textu_voronoi_F1.inputs[0])
mater.node_tree.links.new(vecto_mapping.outputs[0], textu_voronoi_F2.inputs[0])
mater.node_tree.links.new(input_value.outputs[0], textu_voronoi_F1.inputs[1])
mater.node_tree.links.new(input_value.outputs[0], textu_voronoi_F2.inputs[1])
mater.node_tree.links.new(textu_voronoi_F2.outputs[0], conve_math.inputs[0])
mater.node_tree.links.new(textu_voronoi_F1.outputs[0], conve_math.inputs[1])
mater.node_tree.links.new(conve_math.outputs[0], conve_val_rgb.inputs[0])
mater.node_tree.links.new(conve_val_rgb.outputs[0], vecto_bump.inputs[2])
mater.node_tree.links.new(vecto_bump.outputs[0], shade_bsdf.inputs[19])

nodes_list = [input_tex_coord, vecto_mapping, input_value, textu_voronoi_F1, textu_voronoi_F2, conve_math, conve_val_rgb, vecto_bump]
for i, node in enumerate(nodes_list):
  node.location = (-(len(nodes_list)-i) * 200, 300)
