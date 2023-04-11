Public Class Form1
    Private Sub CheckBox1_CheckedChanged(sender As Object, e As EventArgs) Handles chkGen1.CheckedChanged

    End Sub

    Private Sub Button2_Click(sender As Object, e As EventArgs) Handles btnClose.Click
        Me.Close()

    End Sub

    Private Sub Button1_Click(sender As Object, e As EventArgs) Handles Button1.Click
        chkGen1.Visible = False
        chkGen2.Visible = False
        chkGen3.Visible = False
        chkGen4.Visible = False
        chkGen5.Visible = False
        chkGen6.Visible = False
        chkGen7.Visible = False
        chkGen8.Visible = False
        chkGen9.Visible = False
        ListBox1.Visible = True
        Button1.Visible = False
        btnClose.Visible = False
    End Sub

    Private Sub Button5_Click(sender As Object, e As EventArgs) Handles btnExit.Click

    End Sub

    Private Sub Button3_Click(sender As Object, e As EventArgs) Handles btnNext.Click

    End Sub
End Class
