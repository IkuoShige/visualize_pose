import vtk
import sys

def create_axes_actor(color, length=1.0):
    actor = vtk.vtkAxesActor()
    actor.SetTotalLength(length, length, length)
    actor.GetXAxisCaptionActor2D().GetCaptionTextProperty().SetColor(color)
    actor.GetYAxisCaptionActor2D().GetCaptionTextProperty().SetColor(color)
    actor.GetZAxisCaptionActor2D().GetCaptionTextProperty().SetColor(color)
    return actor

def quaternion_to_matrix(q):
    q0, q1, q2, q3 = q
    sqw = q0 * q0
    sqx = q1 * q1
    sqy = q2 * q2
    sqz = q3 * q3

    # 回転行列
    matrix = vtk.vtkMatrix4x4()
    matrix.SetElement(0, 0, sqx - sqy - sqz + sqw)
    matrix.SetElement(1, 1, -sqx + sqy - sqz + sqw)
    matrix.SetElement(2, 2, -sqx - sqy + sqz + sqw)

    tmp1 = q1 * q2
    tmp2 = q0 * q3
    matrix.SetElement(1, 0, 2.0 * (tmp1 + tmp2))
    matrix.SetElement(0, 1, 2.0 * (tmp1 - tmp2))

    tmp1 = q1 * q3
    tmp2 = q0 * q2
    matrix.SetElement(2, 0, 2.0 * (tmp1 - tmp2))
    matrix.SetElement(0, 2, 2.0 * (tmp1 + tmp2))

    tmp1 = q2 * q3
    tmp2 = q0 * q1
    matrix.SetElement(2, 1, 2.0 * (tmp1 + tmp2))
    matrix.SetElement(1, 2, 2.0 * (tmp1 - tmp2))

    return matrix

def main():
    """
    Usage:
    python3 view_from_quaternion.py 0 0 0 1
    python3 view_from_quaternion.py 0.707 0 0 0.707
    """
    # クォータニオン
    quaternion = [float(sys.argv[4]), float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])]

    # クォータニオンから回転行列への変換
    rotation_matrix = quaternion_to_matrix(quaternion)

    # 座標軸のアクター作成
    actor = create_axes_actor([1, 0, 0])

    # レンダラとレンダーウィンドウの設定
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    renderer.SetBackground(0.1, 0.1, 0.1)

    # カメラの設定
    camera = renderer.MakeCamera()
    camera.SetPosition(1, 1, 1-0.707)
    camera.SetFocalPoint(0, 0, 0)
    camera.SetViewUp(0, 0, 1)
    renderer.SetActiveCamera(camera)

    # アクターの位置と姿勢を設定
    transform = vtk.vtkTransform()
    transform.SetMatrix(rotation_matrix)
    actor.SetUserTransform(transform)

    # レンダーウィンドウインタラクタの設定
    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)

    # 基準座標軸のアクターを追加
    base_axes_actor = create_axes_actor([0, 0, 1], 0.5)
    renderer.AddActor(base_axes_actor)

    # 座標軸のアクターを追加
    renderer.AddActor(actor)

    # ビューの初期化
    render_window.Render()

    # インタラクション開始
    render_window_interactor.Start()

if __name__ == "__main__":
    main()
