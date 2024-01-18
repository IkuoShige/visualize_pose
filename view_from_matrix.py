import vtk
import sys

def create_axes_actor(color, length=1.0):
    actor = vtk.vtkAxesActor()
    actor.SetTotalLength(length, length, length)
    actor.GetXAxisCaptionActor2D().GetCaptionTextProperty().SetColor(color)
    actor.GetYAxisCaptionActor2D().GetCaptionTextProperty().SetColor(color)
    actor.GetZAxisCaptionActor2D().GetCaptionTextProperty().SetColor(color)
    return actor

def main():
    """
    Usage:
    python from_matrix.py 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1
    python3 from_matrix.py 0.866 0.5 0 0 -0.5 0.866 0 0 0 0 1 0 0 0 0 1
    """
    # 引数の数を検証
    if len(sys.argv) != 17:
        print("Usage: python from_matrix.py m00 m01 m02 m03 m10 m11 m12 m13 m20 m21 m22 m23 m30 m31 m32 m33")
        print("Please provide 16 numbers for the 4x4 rotation matrix.")
        sys.exit(1)

    # 引数を行列に変換
    rotation_matrix = vtk.vtkMatrix4x4()
    try:
        for i in range(4):
            for j in range(4):
                value = float(sys.argv[i*4 + j + 1])
                rotation_matrix.SetElement(i, j, value)
    except ValueError as e:
        print("Error: All arguments must be numbers.")
        sys.exit(1)

    # 座標軸のアクター作成
    actor = create_axes_actor([1, 0, 0])

    # アクターの位置と姿勢を設定
    transform = vtk.vtkTransform()
    transform.SetMatrix(rotation_matrix)
    actor.SetUserTransform(transform)

    # レンダラとレンダーウィンドウの設定
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    renderer.SetBackground(0.1, 0.1, 0.1)

    # レンダーウィンドウインタラクタの設定
    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)

    # カメラの設定
    camera = renderer.MakeCamera()
    camera.SetPosition(1, 1, 1)
    camera.SetFocalPoint(0, 0, 0)
    camera.SetViewUp(0, 0, 1)
    renderer.SetActiveCamera(camera)

    # アクターの位置と姿勢を設定
    transform = vtk.vtkTransform()
    transform.SetMatrix(rotation_matrix)
    actor.SetUserTransform(transform)

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
