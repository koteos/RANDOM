import { useState } from 'react';
import { Line, Bar } from 'react-chartjs-2';
import 'chart.js/auto';

export default function FlujoCajaApp() {
  const [facturas, setFacturas] = useState([
    { cliente: 'HEINEKEN', fecha: '2025-05-10', monto: 250000, diasPago: 30 },
    { cliente: 'BIMBO', fecha: '2025-05-15', monto: 180000, diasPago: 45 },
    { cliente: 'COPPEL', fecha: '2025-06-05', monto: 220000, diasPago: 60 },
    { cliente: 'LACOMER', fecha: '2025-06-20', monto: 150000, diasPago: 30 },
    { cliente: 'AUDI', fecha: '2025-07-01', monto: 300000, diasPago: 90 },
  ]);

  const [gastoFijo, setGastoFijo] = useState(170000);

  const handleFacturaChange = (index, field, value) => {
    const newFacturas = [...facturas];
    newFacturas[index][field] = field === 'monto' || field === 'diasPago' ? parseFloat(value) : value;
    setFacturas(newFacturas);
  };

  const addFactura = () => {
    setFacturas([...facturas, { cliente: '', fecha: '2025-05-01', monto: 0, diasPago: 30 }]);
  };

  const meses = ['2025-05', '2025-06', '2025-07', '2025-08', '2025-09', '2025-10'];
  const ingresos = meses.map((mes) => {
    return facturas.reduce((acc, f) => {
      const fechaPago = new Date(new Date(f.fecha).getTime() + f.diasPago * 86400000);
      const claveMes = fechaPago.toISOString().slice(0, 7);
      return claveMes === mes ? acc + f.monto : acc;
    }, 0);
  });

  const egresos = meses.map(() => gastoFijo);
  const flujoNeto = ingresos.map((ing, i) => ing - egresos[i]);
  const flujoAcumulado = flujoNeto.reduce((acc, val, i) => {
    acc.push((acc[i - 1] || 0) + val);
    return acc;
  }, []);

  const data = {
    labels: meses,
    datasets: [
      {
        type: 'bar',
        label: 'Ingresos',
        data: ingresos,
        backgroundColor: 'rgba(0, 200, 83, 0.7)',
      },
      {
        type: 'bar',
        label: 'Egresos',
        data: egresos.map(e => -e),
        backgroundColor: 'rgba(244, 67, 54, 0.7)',
      },
      {
        type: 'line',
        label: 'Flujo Acumulado',
        data: flujoAcumulado,
        borderColor: 'rgba(33, 150, 243, 1)',
        borderWidth: 2,
        fill: false,
      },
    ],
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Simulador de Flujo de Efectivo</h1>

      <div className="space-y-4 mb-8">
        <h2 className="text-xl font-semibold">Facturas</h2>
        {facturas.map((factura, index) => (
          <div key={index} className="grid grid-cols-4 gap-4 mb-2">
            <input type="text" value={factura.cliente} onChange={(e) => handleFacturaChange(index, 'cliente', e.target.value)} className="border p-1" />
            <input type="date" value={factura.fecha} onChange={(e) => handleFacturaChange(index, 'fecha', e.target.value)} className="border p-1" />
            <input type="number" value={factura.monto} onChange={(e) => handleFacturaChange(index, 'monto', e.target.value)} className="border p-1" />
            <input type="number" value={factura.diasPago} onChange={(e) => handleFacturaChange(index, 'diasPago', e.target.value)} className="border p-1" />
          </div>
        ))}
        <button onClick={addFactura} className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">+ Agregar Factura</button>
      </div>

      <div className="mb-8">
        <h2 className="text-xl font-semibold">Gastos Fijos Mensuales</h2>
        <input type="number" value={gastoFijo} onChange={(e) => setGastoFijo(parseFloat(e.target.value))} className="border p-2 mt-2 w-full" />
      </div>

      <Bar data={data} options={{ responsive: true }} />
      <Line data={data} options={{ responsive: true, plugins: { legend: { position: 'bottom' } } }} />
    </div>
  );
}
