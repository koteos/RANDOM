Option Explicit

Dim CATIA, doc, measure5, measure6, finalValue

Set CATIA = GetObject(, "CATIA.Application")
If CATIA Is Nothing Then
    WScript.Echo "CATIA no está ejecutándose."
    WScript.Quit 1
End If

Set doc = CATIA.ActiveDocument
If doc Is Nothing Then
    WScript.Echo "No hay documento activo."
    WScript.Quit 1
End If

measure5 = Null
measure6 = Null

On Error Resume Next
If Not doc.Measurements Is Nothing Then
    measure5 = doc.Measurements.Item("MeasureBetween.5").Value
    measure6 = doc.Measurements.Item("MeasureBetween.6").Value
End If
On Error GoTo 0

If Not IsNumeric(measure5) Or Not IsNumeric(measure6) Then
    WScript.Echo "Medidas no numéricas encontradas."
    WScript.Quit 1
End If

finalValue = (((CDbl(measure5) - 270) * 0.7539) * CDbl(measure6)) / 250
WScript.Echo "Valor final (R) = " & finalValue