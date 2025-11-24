import bpy
import math

# ==================== 1. 注册场景属性（不变）====================

bpy.types.Scene.cell_length = bpy.props.FloatProperty(
    name="单元格边长",
    description="每个单元格的单条边长度（米）",
    default=2.0,
    min=0.01
)
bpy.types.Scene.wall_height = bpy.props.FloatProperty(
    name="墙体高度",
    description="墙体的高度（米）",
    default=5.0,
    min=0.01
)
bpy.types.Scene.wall_thickness = bpy.props.FloatProperty(
    name="墙体厚度",
    description="墙体的厚度（米）",
    default=0.2,
    min=0.01
)
bpy.types.Scene.row_count = bpy.props.IntProperty(
    name="行数",
    description="单元格的行数（Y轴方向）",
    default=20,
    min=1
)
bpy.types.Scene.col_count = bpy.props.IntProperty(
    name="列数",
    description="单元格的列数（X轴方向）",
    default=20,
    min=1
)
bpy.types.Scene.edge_count = bpy.props.IntProperty(
    name="单元格边数",
    description="每个单元格的边数（4=四边形，6=六边形等）",
    default=4,
    min=3
)

# ==================== 2. 核心工具函数（不变）====================
def calculate_cell_center(row, col, rows, cols, cell_len, wall_height):
    ccx = cell_len
    ccy = cell_len
    offset_x = (col - (cols - 1) / 2) * ccx
    offset_y = (row - (rows - 1) / 2) * ccy
    cell_center_z = wall_height / 2
    return (offset_x, offset_y, cell_center_z)

def calculate_edge_params(cell_center, edge_index, edges, cell_len, wall_thk, wall_h):
    center_x, center_y, center_z = cell_center
    edges_degree = 360 / edges
    cell_half_length = cell_len / 2
    edges_offset = wall_thk / 2

    edge_rad = math.radians(edge_index * edges_degree)
    dir_rad = edge_rad + math.radians(90)
    distance = cell_half_length - edges_offset

    edge_x = center_x + math.cos(dir_rad) * distance
    edge_y = center_y + math.sin(dir_rad) * distance
    edge_center = (edge_x, edge_y, center_z)

    edge_rotation = edge_rad
    scale_x = cell_half_length
    scale_y = wall_thk / 2
    scale_z = wall_h / 2
    edge_scale = (scale_x, scale_y, scale_z)

    return edge_center, edge_rotation, edge_scale

# ==================== 3. 优化核心：关联复制生成墙体（仅创建1个原型）====================
class MESH_OT_generate_maze_grid(bpy.types.Operator):
    bl_idname = "mesh.generate_maze_grid"
    bl_label = "生成多边形迷宫"
    bl_description = "按行列生成多边形单元格迷宫（关联复制优化，仅墙体）"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene

        # 读取参数（局部变量）
        _cell_len = scene.cell_length
        _wall_h = scene.wall_height
        _wall_thk = scene.wall_thickness
        _rows = scene.row_count
        _cols = scene.col_count
        _edges = scene.edge_count

        # 清空旧墙体（包括原型和关联体）
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
        except RuntimeError:
            pass
        for obj in bpy.data.objects:
            if obj.type == 'MESH' and obj.name.startswith(('Cell_', 'Wall_Prototype')):
                obj.select_set(True)
            else:
                obj.select_set(False)
        bpy.ops.object.delete()

        # 打印生成信息
        print(f"=== 开始生成迷宫（关联复制优化）===")
        print(f"参数：{_rows}行 × {_cols}列，{_edges}边，边长{_cell_len}m，墙厚{_wall_thk}m，墙高{_wall_h}m")

        # -------------------------- 关键优化：创建1个墙体原型 --------------------------
        # 原型位置暂时设为(0,0,0)，后续关联复制后再调整
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        wall_prototype = context.active_object
        wall_prototype.name = "Wall_Prototype"  # 原型命名，方便后续识别
        # 原型默认缩放（后续关联体可单独修改缩放，不影响原型）
        wall_prototype.scale = (1, 1, 1)

        # -------------------------- 关联复制批量生成墙体 --------------------------
        total_walls = 0  # 统计总墙数
        for row in range(_rows):
            for col in range(_cols):
                # 计算单元格中心点
                cell_center = calculate_cell_center(
                    row=row, col=col, rows=_rows, cols=_cols,
                    cell_len=_cell_len, wall_height=_wall_h
                )

                # 为每条边生成关联墙体
                for edge_idx in range(_edges):
                    edge_center, edge_rot, edge_scale = calculate_edge_params(
                        cell_center=cell_center, edge_index=edge_idx,
                        edges=_edges, cell_len=_cell_len,
                        wall_thk=_wall_thk, wall_h=_wall_h
                    )

                    # 关联复制（Shift+D，仅复制物体数据引用，不复制网格数据）
                    bpy.ops.object.duplicate_move_linked(
                        OBJECT_OT_duplicate={"linked": True},  # 关键：linked=True 关联复制
                        TRANSFORM_OT_translate={"value": (0, 0, 0)}  # 先不移动，后续统一设置位置
                    )

                    # 获取关联体，设置位置、旋转、缩放
                    linked_wall = context.active_object
                    linked_wall.location = edge_center  # 位置
                    linked_wall.rotation_euler = (0.0, 0.0, edge_rot)  # 旋转（绕Z轴）
                    linked_wall.scale = edge_scale  # 缩放（每条边可能不同，单独设置）
                    linked_wall.name = f"Cell_R{row}_C{col}_Edge{edge_idx}_Wall"  # 关联体命名

                    total_walls += 1

        # -------------------------- 隐藏原型（可选，不影响使用） --------------------------
        wall_prototype.hide_viewport = True  # 视图中隐藏原型
        wall_prototype.hide_render = True    # 渲染时隐藏原型

        # 生成完成提示
        total_cells = _rows * _cols
        self.report({'INFO'}, f"迷宫生成完成！{total_cells}单元格，{total_walls}面墙（关联复制优化）")
        print(f"=== 迷宫生成完成 ===")
        print(f"优化效果：仅创建1个网格数据，减少{total_walls-1}个重复网格占用")

        return {'FINISHED'}