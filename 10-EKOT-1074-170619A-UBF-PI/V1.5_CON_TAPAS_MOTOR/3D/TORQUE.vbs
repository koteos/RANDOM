Option Explicit

Dim CATIA, doc
On Error Resume Next
Set CATIA = GetObject(, "CATIA.Application")
If CATIA Is Nothing Then
    WScript.Echo "CATIA no está ejecutándose."
    WScript.Quit 1
End If
On Error GoTo 0

Set doc = CATIA.ActiveDocument
If doc Is Nothing Then
    WScript.Echo "No hay documento activo."
    WScript.Quit 1
End If

' Función para obtener valores de medidas por nombre (adaptar según versión)
Dim measCol, measure5, measure6
Set measCol = doc.Measurements
If measCol Is Nothing Then
    WScript.Echo "No se pudo obtener la colección de medidas."
    WScript.Quit 1
End If

measure5 = CDbl(GetMeasurementValue(measCol, "MeasureBetween.5"))
measure6 = CDbl(GetMeasurementValue(measCol, "MeasureBetween.6"))

If IsNumeric(measure5) = False Or IsNumeric(measure6) = False Then
    WScript.Echo "Lecturas inválidas de medidas."
    WScript.Quit 1
End If

Dim delta, resultIntermedio, resultadoFinal, finalValue
delta = measure5 - 270
resultIntermedio = delta * 0.7539
resultadoFinal = resultIntermedio * measure6
finalValue = resultadoFinal / 250

' Crear o actualizar parámetro R
Dim part
Set part = doc.Part
If part Is Nothing Then
    Set part = doc
End If

Dim paramR
On Error Resume Next
Set paramR = part.Parameters.Item("R")
If paramR Is Nothing Then
    Set paramR = part.Parameters.CreateReal("R")
End If
On Error GoTo 0

paramR.Value = finalValue
part.Update

WScript.Echo "Cálculo completado. Valor final (R) = " & finalValue
' Función auxiliar
Function GetMeasurementValue(measCol, name)
    Dim m
    On Error Resume Next
    Set m = measCol.Item(name)
    If Not m Is Nothing Then
        GetMeasurementValue = m.Value
    Else
        GetMeasurementValue = Null
    End If
    On Error GoTo 0
End Function