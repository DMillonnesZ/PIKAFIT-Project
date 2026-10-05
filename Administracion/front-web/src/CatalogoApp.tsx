import { useEffect, useState, type FormEvent } from 'react'
import { API_URL } from './config/env'
import './catalogo.css'

type Sede = { id: string; nombre: string; direccion: string; activa: boolean }
type Clinica = {
  id: string; razon_social: string; ruc: string
  direccion: string; telefono: string; activa: boolean
}
type SedeDatos = Omit<Sede, 'id'>
type ClinicaDatos = Omit<Clinica, 'id'>

const sedeVacia: SedeDatos = { nombre: '', direccion: '', activa: true }
const clinicaVacia: ClinicaDatos = {
  razon_social: '', ruc: '', direccion: '', telefono: '', activa: true,
}
const sedesMuestra: Sede[] = [
  { id: 'demo-sede-1', nombre: 'Sede Centro', direccion: 'Av. Principal 120', activa: true },
  { id: 'demo-sede-2', nombre: 'Sede Norte', direccion: 'Jr. Los Álamos 45', activa: false },
]
const clinicasMuestra: Clinica[] = [
  { id: 'demo-clinica-1', razon_social: 'Clínica Vida Activa',
    ruc: '20100070970', direccion: 'Av. Salud 300', telefono: '014567890', activa: true },
]

function mensajeError(data: unknown): string {
  if (!data || typeof data !== 'object') return 'No se pudo completar la solicitud.'
  const valor = data as { mensaje?: string; detalles?: Record<string, string[]> }
  if (valor.mensaje) return valor.mensaje
  if (valor.detalles) return Object.entries(valor.detalles)
    .map(([campo, errores]) => campo + ': ' + errores.join(', ')).join(' · ')
  return 'No se pudo completar la solicitud.'
}

async function solicitar<T>(ruta: string, token: string, metodo = 'GET', datos?: object): Promise<T> {
  const respuesta = await fetch(API_URL.replace(/\/$/, '') + '/api/v1/' + ruta, {
    method: metodo,
    headers: {
      Authorization: 'Bearer ' + token,
      ...(datos ? { 'Content-Type': 'application/json' } : {}),
    },
    body: datos ? JSON.stringify(datos) : undefined,
  })
  const contenido = await respuesta.json().catch(() => null)
  if (!respuesta.ok) throw new Error(mensajeError(contenido))
  return contenido as T
}

function CatalogoApp() {
  // HU-001 conectará aquí la sesión del administrador cuando llegue a develop.
  const token = sessionStorage.getItem('pikafit_admin_access') ?? ''
  const demostracion = !token
  const [sedes, setSedes] = useState<Sede[]>(demostracion ? sedesMuestra : [])
  const [clinicas, setClinicas] = useState<Clinica[]>(demostracion ? clinicasMuestra : [])
  const [sedeForm, setSedeForm] = useState<SedeDatos>(sedeVacia)
  const [clinicaForm, setClinicaForm] = useState<ClinicaDatos>(clinicaVacia)
  const [sedeEditada, setSedeEditada] = useState<string | null>(null)
  const [clinicaEditada, setClinicaEditada] = useState<string | null>(null)
  const [error, setError] = useState('')
  const [aviso, setAviso] = useState('')
  const [cargando, setCargando] = useState(false)

  useEffect(() => {
    if (!token) return
    Promise.all([
      solicitar<Sede[]>('sedes/', token),
      solicitar<Clinica[]>('clinicas/', token),
    ]).then(([s, c]) => { setSedes(s); setClinicas(c) })
      .catch((cause: unknown) => setError(cause instanceof Error ? cause.message : 'No se pudieron cargar los catálogos.'))
  }, [token])

  function informar(mensaje: string) { setError(''); setAviso(mensaje) }

  async function guardarSede(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    setCargando(true)
    try {
      const datos = { ...sedeForm, nombre: sedeForm.nombre.trim(), direccion: sedeForm.direccion.trim() }
      if (!datos.nombre || !datos.direccion) throw new Error('Nombre y dirección son obligatorios.')
      if (demostracion) setSedes(actuales => sedeEditada
        ? actuales.map(s => s.id === sedeEditada ? { ...s, ...datos } : s)
        : [...actuales, { id: crypto.randomUUID(), ...datos }])
      else {
        await solicitar<Sede>(sedeEditada ? 'sedes/' + sedeEditada + '/' : 'sedes/',
          token, sedeEditada ? 'PATCH' : 'POST', datos)
        setSedes(await solicitar<Sede[]>('sedes/', token))
      }
      setSedeForm(sedeVacia)
      setSedeEditada(null)
      informar('Sede guardada.')
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'No se pudo guardar la sede.')
    } finally { setCargando(false) }
  }

  async function guardarClinica(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    setCargando(true)
    try {
      const datos = {
        ...clinicaForm,
        razon_social: clinicaForm.razon_social.trim(), ruc: clinicaForm.ruc.trim(),
        direccion: clinicaForm.direccion.trim(), telefono: clinicaForm.telefono.trim(),
      }
      if (!datos.razon_social || !datos.direccion || !datos.telefono)
        throw new Error('Razón social, dirección y teléfono son obligatorios.')
      if (!/^(10|15|20)[0-9]{9}$/.test(datos.ruc))
        throw new Error('El RUC debe tener 11 dígitos y un prefijo válido.')
      if (clinicas.some(c => c.ruc === datos.ruc && c.id !== clinicaEditada))
        throw new Error('El RUC ya está registrado.')
      if (demostracion) setClinicas(actuales => clinicaEditada
        ? actuales.map(c => c.id === clinicaEditada ? { ...c, ...datos } : c)
        : [...actuales, { id: crypto.randomUUID(), ...datos }])
      else {
        await solicitar<Clinica>(clinicaEditada ? 'clinicas/' + clinicaEditada + '/' : 'clinicas/',
          token, clinicaEditada ? 'PATCH' : 'POST', datos)
        setClinicas(await solicitar<Clinica[]>('clinicas/', token))
      }
      setClinicaForm(clinicaVacia)
      setClinicaEditada(null)
      informar('Clínica guardada.')
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'No se pudo guardar la clínica.')
    } finally { setCargando(false) }
  }

  async function desactivar(tipo: 'sede' | 'clinica', id: string) {
    setError('')
    setCargando(true)
    try {
      if (demostracion) {
        if (tipo === 'sede') setSedes(actuales => actuales.map(s => s.id === id ? { ...s, activa: false } : s))
        else setClinicas(actuales => actuales.map(c => c.id === id ? { ...c, activa: false } : c))
      } else {
        await solicitar((tipo === 'sede' ? 'sedes/' : 'clinicas/') + id + '/', token, 'DELETE')
        if (tipo === 'sede') setSedes(await solicitar<Sede[]>('sedes/', token))
        else setClinicas(await solicitar<Clinica[]>('clinicas/', token))
      }
      informar((tipo === 'sede' ? 'Sede' : 'Clínica') + ' desactivada. Su historial se conserva.')
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'No se pudo desactivar.')
    } finally { setCargando(false) }
  }

  return <main className="pagina">
    <header className="encabezado">
      <div className="marca">P</div>
      <div><p className="eyebrow">PikaFit · Administración</p>
        <h1>Sedes y clínicas afiliadas</h1>
        <p>Gestiona los lugares de atención sin eliminar su historial.</p></div>
    </header>
    {demostracion && <p className="modo-demo">Vista de demostración: los cambios se muestran solo aquí hasta integrar el inicio de sesión del personal.</p>}
    {error && <p className="mensaje error" role="alert">{error}</p>}
    {aviso && <p className="mensaje exito" role="status">{aviso}</p>}
    <div className="columnas">
      <section className="panel">
        <h2>Sedes</h2>
        <form onSubmit={guardarSede}>
          <label>Nombre<input value={sedeForm.nombre} maxLength={120} required onChange={e => setSedeForm({ ...sedeForm, nombre: e.target.value })} /></label>
          <label>Dirección<input value={sedeForm.direccion} maxLength={255} required onChange={e => setSedeForm({ ...sedeForm, direccion: e.target.value })} /></label>
          <label>Estado<select value={sedeForm.activa ? 'activa' : 'inactiva'} onChange={e => setSedeForm({ ...sedeForm, activa: e.target.value === 'activa' })}><option value="activa">Activa</option><option value="inactiva">Inactiva</option></select></label>
          <div className="acciones"><button disabled={cargando}>{sedeEditada ? 'Guardar cambios' : 'Registrar sede'}</button>
            {sedeEditada && <button type="button" className="secundario" onClick={() => { setSedeEditada(null); setSedeForm(sedeVacia) }}>Cancelar</button>}</div>
        </form>
        <ul className="lista">{sedes.map(s => <li key={s.id}>
          <div><strong>{s.nombre}</strong><small>{s.direccion}</small><span className={s.activa ? 'estado activo' : 'estado'}>{s.activa ? 'Activa' : 'Inactiva'}</span></div>
          <div className="fila-acciones"><button type="button" className="enlace" onClick={() => { setSedeEditada(s.id); setSedeForm({ nombre: s.nombre, direccion: s.direccion, activa: s.activa }) }}>Editar</button>
            {s.activa && <button type="button" className="enlace peligro" disabled={cargando} onClick={() => void desactivar('sede', s.id)}>Desactivar</button>}</div>
        </li>)}</ul>
      </section>
      <section className="panel">
        <h2>Clínicas afiliadas</h2>
        <form onSubmit={guardarClinica}>
          <label>Razón social<input value={clinicaForm.razon_social} maxLength={160} required onChange={e => setClinicaForm({ ...clinicaForm, razon_social: e.target.value })} /></label>
          <label>RUC<input value={clinicaForm.ruc} inputMode="numeric" maxLength={11} required onChange={e => setClinicaForm({ ...clinicaForm, ruc: e.target.value })} /></label>
          <label>Dirección<input value={clinicaForm.direccion} maxLength={255} required onChange={e => setClinicaForm({ ...clinicaForm, direccion: e.target.value })} /></label>
          <label>Teléfono<input value={clinicaForm.telefono} maxLength={30} required onChange={e => setClinicaForm({ ...clinicaForm, telefono: e.target.value })} /></label>
          <label>Estado<select value={clinicaForm.activa ? 'activa' : 'inactiva'} onChange={e => setClinicaForm({ ...clinicaForm, activa: e.target.value === 'activa' })}><option value="activa">Activa</option><option value="inactiva">Inactiva</option></select></label>
          <div className="acciones"><button disabled={cargando}>{clinicaEditada ? 'Guardar cambios' : 'Registrar clínica'}</button>
            {clinicaEditada && <button type="button" className="secundario" onClick={() => { setClinicaEditada(null); setClinicaForm(clinicaVacia) }}>Cancelar</button>}</div>
        </form>
        <ul className="lista">{clinicas.map(c => <li key={c.id}>
          <div><strong>{c.razon_social}</strong><small>RUC {c.ruc} · {c.telefono}</small><small>{c.direccion}</small><span className={c.activa ? 'estado activo' : 'estado'}>{c.activa ? 'Activa' : 'Inactiva'}</span></div>
          <div className="fila-acciones"><button type="button" className="enlace" onClick={() => { setClinicaEditada(c.id); setClinicaForm({ razon_social: c.razon_social, ruc: c.ruc, direccion: c.direccion, telefono: c.telefono, activa: c.activa }) }}>Editar</button>
            {c.activa && <button type="button" className="enlace peligro" disabled={cargando} onClick={() => void desactivar('clinica', c.id)}>Desactivar</button>}</div>
        </li>)}</ul>
      </section>
    </div>
  </main>
}

export default CatalogoApp
