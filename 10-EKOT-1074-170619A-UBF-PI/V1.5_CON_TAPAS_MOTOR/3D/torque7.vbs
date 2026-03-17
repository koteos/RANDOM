Option Explicit

Dim CATIA, doc
Dim valor_LARGO, valor_PALANCA

' Definiciones de las Restricciones y el valor centinela
Const CONSTRAINT_NAME_LARGO = "Offset.35"
Const CONSTRAINT_NAME_PALANCA = "Offset.36"
Const NOT_FOUND_VALUE = -99999

' 1. Conexión a CATIA
Set CATIA = GetObject(, "CATIA.Application")
If CATIA Is Nothing Then
    WScript.Echo "CATIA no está ejecutándose. Inicie CATIA V5 y abra su archivo."
    WScript.Quit 1
End If

Set doc = CATIA.ActiveDocument
If doc Is Nothing Then
    WScript.Echo "No hay documento activo."
    WScript.Quit 1
End If

WScript.Echo "Documento activo: " & doc.Name & " (Buscando Restricciones)"

valor_LARGO = NOT_FOUND_VALUE
valor_PALANCA = NOT_FOUND_VALUE

' Intentar forzar la actualización para asegurar que las restricciones estén frescas
On Error Resume Next
doc.Update
On Error GoTo 0

' -------------------------------------------------------------------
' ## Búsqueda de Restricciones
' -------------------------------------------------------------------

valor_LARGO = GetConstraintValue(doc, CONSTRAINT_NAME_LARGO)
valor_PALANCA = GetConstraintValue(doc, CONSTRAINT_NAME_PALANCA)

WScript.Echo "Lecturas finales -> " & CONSTRAINT_NAME_LARGO & "=" & SafeCStr(valor_LARGO) & " " & CONSTRAINT_NAME_PALANCA & "=" & SafeCStr(valor_PALANCA)

' -------------------------------------------------------------------
' ## Validación y Cálculo Final
' -------------------------------------------------------------------

If valor_LARGO = NOT_FOUND_VALUE Or valor_PALANCA = NOT_FOUND_VALUE Then
    WScript.Echo "FALLA: No se pudieron obtener ambas restricciones numéricas."
    WScript.Echo "Verifique los nombres: " & CONSTRAINT_NAME_LARGO & " y " & CONSTRAINT_NAME_PALANCA
    WScript.Quit 1
End If

Dim finalValue
' Asegurar conversión a Double para la fórmula.
finalValue = (((CDbl(valor_LARGO) - 270) * 0.7539) * CDbl(valor_PALANCA)) / 250
WScript.Echo "---"
WScript.Echo "Cálculo final exitoso."
WScript.Echo "Valor final (R) = " & finalValue


' -------------------------------------------------------------------
' ## Funciones de Utilidad
' -------------------------------------------------------------------

Function GetConstraintValue(docToSearch, constraintName)
    ' Busca el valor de la restricción navegando el ensamblaje.
    
    Dim catiaProduct
    Dim valor
    Dim constraintObj
    Dim comp
    Dim compPart
    
    valor = NOT_FOUND_VALUE
    
    ' 1. Intentar buscar en el documento activo (Product/Part principal)
    On Error Resume Next
    
    ' Buscar en el nivel del producto principal (constraints de ensamblaje)
    If Not docToSearch.Product Is Nothing Then
        Set constraintObj = docToSearch.Product.Constraints.Item(constraintName)
        If Not constraintObj Is Nothing Then
            valor = constraintObj.Value.Value ' Acceso para Assembly Constraint
            If valor <> 0 Then GetConstraintValue = valor: Exit Function
        End If
    End If

    ' Buscar en el nivel de la parte principal (constraints de pieza)
    If Not docToSearch.Part Is Nothing Then
        Set constraintObj = docToSearch.Part.Constraints.Item(constraintName)
        If Not constraintObj Is Nothing Then
            valor = constraintObj.Dimension.Value ' Acceso para Part Constraint
            If valor <> 0 Then GetConstraintValue = valor: Exit Function
        End If
    End If
    On Error GoTo 0
    
    ' 2. Si es un Producto, buscar en los componentes anidados
    On Error Resume Next
    Set catiaProduct = docToSearch.Product
    On Error GoTo 0
    
    If Not catiaProduct Is Nothing Then
        For Each comp In catiaProduct.Products
            ' **ACCESO CRÍTICO: FORZAR ACCESO AL OBJETO PART**
            On Error Resume Next
            Set compPart = comp.ReferenceProduct.Parent.Part
            On Error GoTo 0
            
            If Not compPart Is Nothing Then
                ' Buscar la restricción en la colección Constraints de la Part
                On Error Resume Next
                Set constraintObj = compPart.Constraints.Item(constraintName)
                On Error GoTo 0
                
                If Not constraintObj Is Nothing Then
                    valor = constraintObj.Dimension.Value
                    If valor <> 0 Then
                        GetConstraintValue = valor
                        Exit Function
                    End If
                End If
            End If
        Next
    End If
    
    GetConstraintValue = valor
    
End Function

Function SafeCStr(v)
    ' Evita el error 800A005E y muestra diagnóstico.
    If IsNull(v) Or v = NOT_FOUND_VALUE Then
        SafeCStr = "NO ENCONTRADA"
    Else
        SafeCStr = CStr(v)
    End If
End Function