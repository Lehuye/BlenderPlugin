import bpy
import math
from mathutils import Vector


# =========================================================
# 1. 创建多边形 Operator（等边三角体）
# =========================================================
class OBJECT_OT_create_polygon(bpy.types.Operator):
    """创建等边三角体"""
    bl_idname = "object.create_polygon"
    bl_label = "创建等边三角体"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        # 三角形边长
        side = 2.0
        h = side * math.sqrt(3) / 2

        # 顶点坐标（等边三角形 + 挤出）
        verts = [
            Vector((0, 0, 0)),
            Vector((side, 0, 0)),
            Vector((side / 2, h, 0)),
            Vector((side / 2, h / 3, 1.5)),     # 顶部挤出的点，形成三角体
        ]

        # 面
        faces = [
            (0, 1, 2),
            (0, 1, 3),
            (1, 2, 3),
            (2, 0, 3),
        ]

        mesh = bpy.data.meshes.new("Equilateral_Tetra")
        mesh.from_pydata(verts, [], faces)
        mesh.update()

        obj = bpy.data.objects.new("Tetrahedron", mesh)
        context.collection.objects.link(obj)
        context.view_layer.objects.active = obj

        return {'FINISHED'}
