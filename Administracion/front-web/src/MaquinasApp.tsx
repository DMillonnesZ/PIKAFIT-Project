import { useEffect, useState, type FormEvent } from 'react'
import { API_URL } from './config/env'

type Estado = 'operativa' | 'mantenimiento' | 'fuera_servicio'
type Sede = { id: string; nombre: string; activa: boolean }
type Maquina = {
  id: string; codigo: string; nombre: string; numero_serie: string
  grupo_muscular: string; sede_id: string; estado: Estado
}
type Entrada = Omit<Maquina, 'id'>
type ErrorCampo = { campo: string; mensaje: string }

const vacio: Entrada = {
  codigo: '', nombre: '', numero_serie: '', grupo_muscular: '', sede_id: '', estado: 'operativa',
}
const api = API_URL.replace(/\/$/, '') + '/api/v1/'

async function solicitar<T>(ruta: string, token: string, metodo = 'GET', datos?: object): Promise<T> {
  const respuesta = await fetch(api + ruta, {
    method: metodo,
    headers: {
      Authorization: `Bearer ${token}`,
      ...(datos ? { 'Content-Type': 'application/json' } : {}),
    },
    body: datos ? JSON.stringify(datos) : undefined,
  })
  const contenido = await respuesta.json().catch(() => null) as
    ({ mensaje?: string; detalles?: ErrorCampo[] } | null)
  if (!respuesta.ok) {
    const campos = contenido?.detalles?.map(item => `${item.campo}: ${item.mensaje}`).join(' · ')
    throw new Error(campos || contenido?.mensaje || 'No se pudo completar la solicitud.')
  }
  return contenido as T
}

function MaquinasApp() {
  const token = sessionStorage.getItem('pikafit_admin_access') ?? ''
  const [sedes, setSedes] = useState<Sede[]>([])
  const [maquinas, setMaquinas] = useState<Maquina[]>([])
  const [formulario, setFormulario] = useState<Entrada>(vacio)
  const [error, setError] = useState('')
  const [aviso, setAviso] = useState('')
  const [cargando, setCargando] = useState(false)

  useEffect(() => {
    if (!token) return
    Promise.all([
      solicitar<Sede[]>('sedes/?activas=true', token),
      solicitar<Maquina[]>('maquinas/', token),
    ]).then(([activas, registradas]) => {
      setSedes(activas)
      setMaquinas(registradas)
    }).catch(cause => setError(cause instanceof Error ? cause.message : 'No se pudieron cargar las máquinas.'))
  }, [token])

  async function guardar(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError(''); setAviso(''); setCargando(true)
    try {
      if (!token) throw new Error('Inicia sesión como administrador para registrar máquinas.')
      const datos = {
        ...formulario,
        codigo: formulario.codigo.trim().toUpperCase(),
        nombre: formulario.nombre.trim(),
        numero_serie: formulario.numero_serie.trim().toUpperCase(),
        grupo_muscular: formulario.grupo_muscular.trim(),
      }
      if (!datos.codigo || !datos.nombre || !datos.numero_serie || !datos.grupo_muscular)
        throw new Error('Completa todos los datos de la máquina.')
      if (!sedes.some(sede => sede.id === datos.sede_id && sede.activa))
        throw new Error('Selecciona una sede activa.')
      await solicitar<Maquina>('maquinas/', token, 'POST', datos)
      setMaquinas(await solicitar<Maquina[]>('maquinas/', token))
      setFormulario(vacio)
      setAviso('Máquina registrada con un QR único.')
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'No se pudo registrar la máquina.')
    } finally { setCargando(false) }
  }

  return <div className="seccion-maquinas">
    {!token && <p className="modo-demo">Inicia sesión en Administración para registrar máquinas y descargar sus QR.</p>}
    {error && <p className="mensaje error" role="alert">{error}</p>}
    {aviso && <p className="mensaje exito" role="status">{aviso}</p>}
    <div className="columnas">
      <section className="panel">
        <h2>Registrar máquina</h2>
        <p>Elige una sede activa. El código QR se genera al guardar.</p>
        <form onSubmit={guardar}>
          <label>Código<input required maxLength={40} value={formulario.codigo} onChange={e => setFormulario({ ...formulario, codigo: e.target.value })} /></label>
          <label>Nombre<input required maxLength={120} value={formulario.nombre} onChange={e => setFormulario({ ...formulario, nombre: e.target.value })} /></label>
          <label>Número de serie<input required maxLength={80} value={formulario.numero_serie} onChange={e => setFormulario({ ...formulario, numero_serie: e.target.value })} /></label>
          <label>Grupo muscular<input required maxLength={80} value={formulario.grupo_muscular} onChange={e => setFormulario({ ...formulario, grupo_muscular: e.target.value })} /></label>
          <label>Sede<select required value={formulario.sede_id} onChange={e => setFormulario({ ...formulario, sede_id: e.target.value })}>
            <option value="">Selecciona una sede activa</option>
            {sedes.filter(s => s.activa).map(s => <option key={s.id} value={s.id}>{s.nombre}</option>)}
          </select></label>
          <label>Estado inicial<select value={formulario.estado} onChange={e => setFormulario({ ...formulario, estado: e.target.value as Estado })}>
            <option value="operativa">Operativa</option>
            <option value="mantenimiento">En mantenimiento</option>
            <option value="fuera_servicio">Fuera de servicio</option>
          </select></label>
          <div className="acciones"><button disabled={cargando || !token || !sedes.some(s => s.activa)}>Registrar máquina</button></div>
        </form>
      </section>
      <section className="panel">
        <h2>Máquinas registradas</h2>
        <ul className="lista">{maquinas.map(m => <li key={m.id}>
          <div><strong>{m.codigo} · {m.nombre}</strong><small>Serie {m.numero_serie} · {m.grupo_muscular}</small>
            <small>{sedes.find(s => s.id === m.sede_id)?.nombre ?? 'Sede histórica'}</small>
            <span className={m.estado === 'operativa' ? 'estado activo' : 'estado'}>{m.estado.replace('_', ' ')}</span>
          </div>
        </li>)}</ul>
        {!maquinas.length && <p>Aún no hay máquinas registradas.</p>}
      </section>
    </div>
  </div>
}

export default MaquinasApp
