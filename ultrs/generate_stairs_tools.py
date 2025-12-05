import bpy

# 楼梯属性挂载到 Scene
bpy.types.Scene.total_height = bpy.props.FloatProperty(
    name="Total Height",
    description="Total height of the staircase (Z axis)",
    default=3.0,
    min=0.1
)

bpy.types.Scene.step_height = bpy.props.FloatProperty(
    name="Step Height",
    description="Height of each step",
    default=0.2,
    min=0.01
)

bpy.types.Scene.step_width = bpy.props.FloatProperty(
    name="Step Width",
    description="Width of each step (X axis)",
    default=1.0,
    min=0.1
)

bpy.types.Scene.step_length = bpy.props.FloatProperty(
    name="Step Length",
    description="Depth of each step (Y axis)",
    default=0.3,
    min=0.1
)

class OBJECT_OT_generate_stairs(bpy.types.Operator):

    def execute(self, context):
        # 删除已有楼梯（可选）
        for obj in context.scene.objects:
            if obj.get("is_generated_stairs"):
                bpy.data.objects.remove(obj, do_unlink=True)

        # 计算阶数
        steps_count = int(self.total_height / self.step_height)
        if steps_count < 1:
            self.report({'ERROR'}, "Total height too small for step height")
            return {'CANCELLED'}

        # 创建每个台阶
        for i in range(steps_count):
            bpy.ops.mesh.primitive_cube_add(
                size=1,
                enter_editmode=False,
                location=(0, i * self.step_length + self.step_length / 2, i * self.step_height + self.step_height / 2)
            )
            step = context.active_object
            step.scale = (self.step_width / 2, self.step_length / 2, self.step_height / 2)
            step["is_generated_stairs"] = True  # 标记为生成的楼梯

        self.report({'INFO'}, f"Generated {steps_count} steps")
        return {'FINISHED'}
