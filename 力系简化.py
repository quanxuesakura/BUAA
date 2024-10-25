import tkinter as tk
from fractions import Fraction


# 向量类
class Vector3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def moment(self, reference_point):
        lever_arm = self - reference_point
        return Vector3D(
            lever_arm.y * self.z - lever_arm.z * self.y,
            lever_arm.z * self.x - lever_arm.x * self.z,
            lever_arm.x * self.y - lever_arm.y * self.x,
        )


# 力类
class Force:
    def __init__(self, fx, fy, fz, point):
        self.vector = Vector3D(fx, fy, fz)
        self.point = Vector3D(*point)

    def moment(self, reference_point):
        lever_arm = self.point - reference_point  # 使用作用点与简化点的差向量
        return Vector3D(
            lever_arm.y * self.vector.z - lever_arm.z * self.vector.y,
            lever_arm.z * self.vector.x - lever_arm.x * self.vector.z,
            lever_arm.x * self.vector.y - lever_arm.y * self.vector.x,
        )


def calculate_resultant(forces, reference_point):
    resultant = Vector3D(0, 0, 0)
    total_moment = Vector3D(0, 0, 0)

    for force in forces:
        resultant += force.vector
        total_moment += force.moment(reference_point)

    return resultant, total_moment


class ForceSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("力系简化计算器")

        # 力的输入框
        self.force_entries = []
        self.frame_forces = tk.Frame(self.root)
        self.frame_forces.pack(pady=10)

        self.add_force_button = tk.Button(
            self.frame_forces, text="添加力", command=self.add_force_entry
        )
        self.add_force_button.grid(row=0, column=0)

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack(pady=10)

        # 简化点输入框
        self.simplify_point_frame = tk.Frame(self.root)
        self.simplify_point_frame.pack(pady=10)

        tk.Label(self.simplify_point_frame, text="简化点 (x, y, z):").grid(
            row=0, column=0
        )
        self.simplify_x_entry = tk.Entry(self.simplify_point_frame, width=5)
        self.simplify_y_entry = tk.Entry(self.simplify_point_frame, width=5)
        self.simplify_z_entry = tk.Entry(self.simplify_point_frame, width=5)

        self.simplify_x_entry.grid(row=0, column=1)
        self.simplify_y_entry.grid(row=0, column=2)
        self.simplify_z_entry.grid(row=0, column=3)

        self.calculate_button = tk.Button(
            self.root, text="计算", command=self.calculate
        )
        self.calculate_button.pack(pady=10)

    def add_force_entry(self):
        row_idx = len(self.force_entries) + 1
        force_frame = tk.Frame(self.frame_forces)
        force_frame.grid(row=row_idx, column=0, columnspan=7)

        # 添加标签与输入框
        tk.Label(force_frame, text="Fx:").grid(row=0, column=0)
        tk.Label(force_frame, text="Fy:").grid(row=0, column=1)
        tk.Label(force_frame, text="Fz:").grid(row=0, column=2)
        tk.Label(force_frame, text="Px:").grid(row=0, column=3)
        tk.Label(force_frame, text="Py:").grid(row=0, column=4)
        tk.Label(force_frame, text="Pz:").grid(row=0, column=5)

        # 力的分量输入框
        fx_entry = tk.Entry(force_frame, width=5)
        fy_entry = tk.Entry(force_frame, width=5)
        fz_entry = tk.Entry(force_frame, width=5)

        # 力的作用点输入框
        px_entry = tk.Entry(force_frame, width=5)
        py_entry = tk.Entry(force_frame, width=5)
        pz_entry = tk.Entry(force_frame, width=5)

        # 布局
        fx_entry.grid(row=1, column=0)
        fy_entry.grid(row=1, column=1)
        fz_entry.grid(row=1, column=2)
        px_entry.grid(row=1, column=3)
        py_entry.grid(row=1, column=4)
        pz_entry.grid(row=1, column=5)

        # 添加减少力按钮
        remove_button = tk.Button(
            force_frame,
            text="删除",
            command=lambda: self.remove_force_entry(force_frame),
        )
        remove_button.grid(row=1, column=6, padx=5)

        self.force_entries.append(
            (fx_entry, fy_entry, fz_entry, px_entry, py_entry, pz_entry)
        )

    def remove_force_entry(self, force_frame):
        # 从窗口中移除对应的力条目
        force_frame.destroy()  # 删除输入框和按钮
        # 同时也从记录中移除
        self.force_entries = [
            entry for entry in self.force_entries if entry[0].master is not force_frame
        ]

    def format_result(self, value):
        # 将值转换为分数形式
        if isinstance(value, int):
            return f"{value}"
        elif value.is_integer():
            return f"{int(value)}"
        else:
            return str(Fraction(value).limit_denominator())

    def calculate(self):
        forces = []
        for (
            fx_entry,
            fy_entry,
            fz_entry,
            px_entry,
            py_entry,
            pz_entry,
        ) in self.force_entries:
            # 获取输入，若为空则默认为0
            fx = float(fx_entry.get()) if fx_entry.get() else 0.0
            fy = float(fy_entry.get()) if fy_entry.get() else 0.0
            fz = float(fz_entry.get()) if fz_entry.get() else 0.0
            px = float(px_entry.get()) if px_entry.get() else 0.0
            py = float(py_entry.get()) if py_entry.get() else 0.0
            pz = float(pz_entry.get()) if pz_entry.get() else 0.0
            forces.append(Force(fx, fy, fz, (px, py, pz)))  # 使用输入的作用点

        # 获得简化点的坐标，若为空则默认为0
        sx = float(self.simplify_x_entry.get()) if self.simplify_x_entry.get() else 0.0
        sy = float(self.simplify_y_entry.get()) if self.simplify_y_entry.get() else 0.0
        sz = float(self.simplify_z_entry.get()) if self.simplify_z_entry.get() else 0.0
        simplify_point = Vector3D(sx, sy, sz)

        # 计算合力和主矩
        resultant, moment = calculate_resultant(forces, simplify_point)

        result_msg = f"合力: ({self.format_result(resultant.x)}, {self.format_result(resultant.y)}, {self.format_result(resultant.z)})\n"
        result_msg += f"主矩: ({self.format_result(moment.x)}, {self.format_result(moment.y)}, {self.format_result(moment.z)})\n"

        # 判断合力是否为零
        if resultant.x == 0 and resultant.y == 0 and resultant.z == 0:
            result_msg += "不存在简化中心"
        else:
            # 计算简化中心
            center_of_simplification = Vector3D(
                moment.x / resultant.x, moment.y / resultant.y, moment.z / resultant.z
            )
            result_msg += f"简化中心: ({self.format_result(center_of_simplification.x)}, {self.format_result(center_of_simplification.y)}, {self.format_result(center_of_simplification.z)})"

        self.result_label.config(text=result_msg)


if __name__ == "__main__":
    root = tk.Tk()
    app = ForceSystemApp(root)
    root.mainloop()
