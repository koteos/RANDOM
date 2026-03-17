Option Explicit

Dim CATIA, doc
Dim measure5, measure6

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
Dim measCol
Set measCol = doc.Measurements
If Not measCol Is Nothing Then
    Dim v
    v = GetMeasurementValue(measCol, "MeasureBetween.5")
    If IsNumeric(v) Then measure5 = CDbl(v)
    v = GetMeasurementValue(measCol, "MeasureBetween.6")
    If IsNumeric(v) Then measure6 = CDbl(v)
End If
On Error GoTo 0

WScript.Echo "Lecturas global -> measure5=" & CStr(measure5) & " measure6=" & CStr(measure6)

If Not IsNumeric(measure5) Or Not IsNumeric(measure6) Then
    ' Intentar en primer nivel de componentes
    Dim prod, comp, v2
    Set prod = doc.Product
    If Not prod Is Nothing Then
        For Each comp In prod.Products
            Dim cMeas
            On Error Resume Next
            Set cMeas = comp.Measurements
            If Not cMeas Is Nothing Then
                v2 = GetMeasurementValue(cMeas, "MeasureBetween.5")
                If IsNumeric(v2) Then measure5 = CDbl(v2)
                v2 = GetMeasurementValue(cMeas, "MeasureBetween.6")
                If IsNumeric(v2) Then measure6 = CDbl(v2)
            End If
            On Error GoTo 0
            If IsNumeric(measure5) And IsNumeric(measure6) Then Exit For
        Next
    End If
End If

WScript.Echo "Lecturas finales -> measure5=" & CStr(measure5) & " measure6=" & CStr(measure6)

If Not IsNumeric(measure5) Or Not IsNumeric(measure6) Then
    WScript.Echo "No se pudieron obtener medidas numéricas."
    WScript.Quit 1
End If

Dim finalValue
finalValue = (((CDbl(measure5) - 270) * 0.7539) * CDbl(measure6)) / 250
WScript.Echo "Valor final (R) = " & finalValue

Function GetMeasurementValue(measCol, name)
    Dim m
    On Error Resume Next
    Set m = measCol.Item(name)
    If Not m Is Nothing Then
        GetMeasurementValue = m.Value
    Else
        GetMeasurementValue = Null
    End If
    On Error Goto 0
End Function