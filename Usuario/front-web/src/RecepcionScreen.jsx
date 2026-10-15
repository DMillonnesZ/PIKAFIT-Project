import React, { useState } from 'react';

export default function RecepcionScreen() {
  const [codigo, setCodigo] = useState('');
  const [mensaje, setMensaje] = useState('');
  const [esValido, setEsValido] = useState(null);

  const handleValidar = () => {
    // Simulación de llamada al backend (Spring Boot)
    if (codigo === 'ABC123') {
      setMensaje('✅ Autorizado: Luis Vasquez');
      setEsValido(true);
    } else {
      setMensaje('❌ Pase inválido o expirado');
      setEsValido(false);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '400px', margin: '0 auto', textAlign: 'center' }}>
      <h2>Validación de Pases - Clínica</h2>
      <input
        type="text"
        placeholder="Escanear QR o ingresar código"
        value={codigo}
        onChange={(e) => setCodigo(e.target.value)}
        style={{ padding: '10px', width: '100%', marginBottom: '10px', borderRadius: '5px', border: '1px solid #ccc' }}
      />
      <button onClick={handleValidar} style={{ padding: '10px', width: '100%', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>
        Validar Pase
      </button>
      {mensaje && (
        <p style={{ marginTop: '20px', fontWeight: 'bold', color: esValido ? 'green' : 'red' }}>
          {mensaje}
        </p>
      )}
    </div>
  );
}