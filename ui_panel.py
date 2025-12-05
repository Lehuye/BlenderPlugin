# 面板UI文件，定义插件在侧边栏显示的面板和按钮
import bpy  # Blender Python API

# # 定义一个枚举属性用于 Tab 切换
# bpy.types.Scene.lehuye_tab = bpy.props.EnumProperty(
#     name="功能分类",
#     description="选择功能分类",
#     items=[
#         ('MATERIAL', "材质相关", "与材质相关的操作"),
#         ('ORIGIN', "轴心相关", "与轴心相关的操作")
#     ],
#     default='MATERIAL'
# )

class MaterialPanel(bpy.types.Panel):
    bl_label = "材质工具"
    bl_idname = "VIEW3D_PT_material_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lehuye'

    def draw(self, context):
        layout = self.layout
        layout.operator("material.clear_all", text="移除所有材质")

# 面板类：在侧栏显示轴心工具
class OriginPanel(bpy.types.Panel):
    bl_label = "轴心工具"
    bl_idname = "VIEW3D_PT_origin_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lehuye'

    def draw(self, context):
        layout = self.layout
        layout.operator("origin.to_geometry", text="几何中心")
        layout.operator("origin.to_mass", text="质心")
        layout.operator("origin.to_cursor", text="原点（3D光标）")
        layout.operator("origin.to_volume", text="体积中心")

# 生成楼梯面板
class VIEW3D_PT_stairs_panel(bpy.types.Panel):
    bl_label = "Stair Generator"
    bl_idname = "VIEW3D_PT_stairs_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lehuye'

    def draw(self, context):
        layout = self.layout
        layout.label(text="Generate a staircase")
        layout.operator("object.generate_stairs")
        layout.label(text="Generate a staircase by Panel")
        layout.operator("object.generate_stair_plane")

# 创建多边形
class CreatePolygonPanel(bpy.types.Panel):
    bl_label = "创建多边形"
    bl_idname = "Create_Polygon_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type =  'UI'
    bl_category = 'Lehuye'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.create_polygon", text="创建等边三角体")

# 整理模型
class FixModelPanel(bpy.types.Panel):
    bl_label = "修复模型"
    bl_idname = "VIEW3D_PT_fix_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lehuye'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.fix_model", text="修复模型")

# 面板类：在侧栏显示文本输入框和按钮
class TextPanel(bpy.types.Panel):
    bl_label = "文本工具"
    bl_idname = "VIEW3D_PT_text_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lehuye'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # ---------------------
        # 单对象重命名
        # ---------------------
        # layout.label(text="单对象重命名")
        # layout.prop(scene, "rename_text", text="新名称")
        # layout.operator("object.rename_selected", text="重命名选中对象")
        # layout.separator()

        # ---------------------
        # 批量编号重命名
        # ---------------------
        layout.label(text="批量编号重命名")
        layout.prop(scene, "rename_text", text="名称主体")  # 使用同一个 rename_text
        layout.prop(scene, "rename_pos", text="编号位置")  # Enum: PREFIX / SUFFIX
        layout.prop(scene, "rename_start", text="起始编号")
        layout.prop(scene, "rename_order", text="顺序")     # Enum: ASC / DESC
        layout.operator("object.rename_selected", text="执行批量重命名")
        layout.separator()

# 快速生成四壁面板
class GenerateMazePanel(bpy.types.Panel):
    bl_label = "快速生成迷宫"
    bl_idname = "MESH_PT_generate_maze_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lehuye'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="多边形迷宫参数（仅墙体）")
        # 新增：单元格边数控件
        layout.prop(scene, "edge_count", text="单元格边数")
        # 原有参数控件（名称与ultrs.py一致）
        layout.prop(scene, "cell_length", text="单元格边长 (m)")
        layout.prop(scene, "wall_thickness", text="墙体厚度 (m)")
        layout.prop(scene, "wall_height", text="墙体高度 (m)")
        layout.prop(scene, "row_count", text="行数")
        layout.prop(scene, "col_count", text="列数")
        # 调用运算符（ID与ultrs.py一致）
        layout.operator("mesh.generate_maze_grid", text="生成迷宫")

# 通过DXF文件生成3D
class DXFGeneratorPanel(bpy.types.Panel):
    bl_label = "DXF 生成 3D"
    bl_idname = "VIEW3D_PT_generate_from_dxf"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lehuye'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="上传 DXF 并生成 3D")
        layout.prop(scene, "dxf_filepath", text="选择文件")
        layout.prop(scene, "level_height", text="楼层高度 (m)")
        layout.prop(scene, "wall_thickness", text="墙体厚度 (m)")
        layout.operator("object.generate_from_dxf", text="生成 3D 墙体")

def unregister_panel_props():
    del bpy.types.Scene.lehuye_tab
