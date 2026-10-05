import { useEffect, useMemo, useState, type FormEvent } from 'react'
import { API_URL } from './config/env'

type Sede = { id: string; nombre: string; activa: boolean }
type Plan = { id: string; nombre: string; duracion_dias: number; precio: string; activo: boolean }
type Membresia = { id: string; plan_id: string; fecha_inicio: string; fecha_fin: string; activa: boolean }
type Socio = {
  id: string; nombres: string; apellidos: string; dni: string; correo: string
  sede_id: string; activo: boolean; membresia?: Membresia | null
}
type DatosSocio = Omit<Socio, 'id' | 'activo' | 'membresia'> & {
  plan_id: string; fecha_inicio: string; fecha_fin: string
}
type ErrorAPI = Error & { codigo?: string; socio?: Socio }

const planesDemo: Plan[] = [
  { id: 'demo-plan-mensual', nombre: 'Mensual', duracion_dias: 30, precio: '89.00', activo: true },
  { id: 'demo-plan-trimestral', nombre: 'Trimestral', duracion_dias: 90, precio: '225.00', activo: true },
]
const sedesDemo: Sede[] = [{ id: 'demo-sede', nombre: 'Sede Centro', activa: true }]

function fechaLocal(fecha: Date) {
  return `${fecha.getFullYear()}-${String(fecha.getMonth() + 1).padStart(2, '0')}-${String(fecha.getDate()).padStart(2, '0')}`
}

function finSegunPlan(inicio: string, duracion: number) {
  if (!inicio || !duracion) return ''
  const [anio, mes, dia] = inicio.split('-').map(Number)
  const fin = new Date(anio, mes - 1, dia + duracion - 1)
  return fechaLocal(fin)
}

function errorVisible(error: unknown) {
  return error instanceof Error ? error.message : 'No se pudo completar la solicitud.'
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
  const contenido = await respuesta.json().catch(() => null) as (Record<string, unknown> | null)
  if (!respuesta.ok) {
    const error = new Error(String(contenido?.mensaje ?? 'No se pudo completar la solicitud.')) as ErrorAPI
    error.codigo = String(contenido?.codigo ?? '')
    error.socio = contenido?.socio as Socio | undefined
    throw error
  }
  return contenido as T
}

function SociosApp() {
  const token = sessionStorage.getItem('pikafit_admin_access') ?? ''
  const demo = !token
  const hoy = fechaLocal(new Date())
  const [planes, setPlanes] = useState<Plan[]>(demo ? planesDemo : [])
  const [sedes, setSedes] = useState<Sede[]>(demo ? sedesDemo : [])
  const [socios, setSocios] = useState<Socio[]>([])
  const [planEditado, setPlanEditado] = useState<string | null>(null)
  const [planForm, setPlanForm] = useState({ nombre: '', duracion_dias: 30, precio: '0.00', activo: true })
  const [socioForm, setSocioForm] = useState<DatosSocio>({
    nombres: '', apellidos: '', dni: '', correo: '', sede_id: '', plan_id: '', fecha_inicio: hoy, fecha_fin: '',
  })
  const [renovarId, setRenovarId] = useState<string | null>(null)
  const [error, setError] = useState('')
  const [aviso, setAviso] = useState('')
  const [cargando, setCargando] = useState(false)
  const planesActivos = useMemo(() => planes.filter(plan => plan.activo), [planes])

  async function cargar() {
    if (!token) return
    const [p, s, u] = await Promise.all([
      solicitar<Plan[]>('planes/?inactivos=true', token),
      solicitar<Sede[]>('sedes/?activas=true', token),
      solicitar<Socio[]>('socios/', token),
    ])
    setPlanes(p)
    setSedes(s)
    setSocios(u)
  }

  useEffect(() => {
    if (token) void cargar().catch(cause => setError(errorVisible(cause)))
  }, [token])

  function cambiarPlan(planId: string) {
    const plan = planesActivos.find(item => item.id === planId)
    setSocioForm(actual => ({
      ...actual, plan_id: planId,
      fecha_fin: finSegunPlan(actual.fecha_inicio, plan?.duracion_dias ?? 0),
    }))
  }

  function cambiarInicio(inicio: string) {
    const plan = planesActivos.find(item => item.id === socioForm.plan_id)
    setSocioForm(actual => ({ ...actual, fecha_inicio: inicio, fecha_fin: finSegunPlan(inicio, plan?.duracion_dias ?? 0) }))
  }

  async function guardarPlan(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setError(''); setAviso(''); setCargando(true)
    try {
      const datos = { ...planForm, nombre: planForm.nombre.trim(), duracion_dias: Number(planForm.duracion_dias), precio: Number(planForm.precio).toFixed(2) }
      if (demo) {
        setPlanes(current => planEditado
          ? current.map(plan => plan.id === planEditado ? { ...plan, ...datos } : plan)
          : [...current, { id: crypto.randomUUID(), ...datos }])
      } else {
        await solicitar<Plan>(planEditado ? `planes/${planEditado}/` : 'planes/', token, planEditado ? 'PATCH' : 'POST', datos)
        await cargar()
      }
      setPlanEditado(null); setPlanForm({ nombre: '', duracion_dias: 30, precio: '0.00', activo: true }); setAviso('Plan guardado.')
    } catch (cause) { setError(errorVisible(cause)) } finally { setCargando(false) }
  }

  async function desactivarPlan(plan: Plan) {
    setError(''); setCargando(true)
    try {
      if (demo) setPlanes(current => current.map(item => item.id === plan.id ? { ...item, activo: false } : item))
      else { await solicitar<Plan>(`planes/${plan.id}/`, token, 'DELETE'); await cargar() }
      setAviso('Plan desactivado. Se conserva en las membresías existentes.')
    } catch (cause) { setError(errorVisible(cause)) } finally { setCargando(false) }
  }

  async function guardarSocio(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setError(''); setAviso(''); setCargando(true)
    const datos = { ...socioForm, nombres: socioForm.nombres.trim(), apellidos: socioForm.apellidos.trim(), correo: socioForm.correo.trim().toLowerCase() }
    try {
      if (demo) {
        const nuevo: Socio = { ...datos, id: crypto.randomUUID(), activo: true, membresia: { id: crypto.randomUUID(), plan_id: datos.plan_id, fecha_inicio: datos.fecha_inicio, fecha_fin: datos.fecha_fin, activa: true } }
        setSocios(current => [...current, nuevo]); setAviso('Socio y membresía guardados en esta vista de demostración.')
      } else {
        const ruta = renovarId ? `socios/${renovarId}/` : 'socios/'
        await solicitar(ruta, token, 'POST', datos)
        setRenovarId(null); setAviso('Socio activado con su membresía.'); await cargar()
      }
      setSocioForm(actual => ({ ...actual, nombres: '', apellidos: '', dni: '', correo: '' }))
    } catch (cause) {
      const fallo = cause as ErrorAPI
      if (fallo.codigo === 'RENOVACION_DISPONIBLE' && fallo.socio) {
        setRenovarId(fallo.socio.id)
        setError(`Ya existe ${fallo.socio.nombres} ${fallo.socio.apellidos} con membresía vencida. Usa “Renovar membresía” para conservar su cuenta e historial.`)
      } else setError(errorVisible(cause))
    } finally { setCargando(false) }
  }

  return <div className="seccion-socios">
    {demo && <p className="modo-demo">Vista de demostración: inicia sesión con HU-001 para guardar los cambios en el servidor.</p>}
    {error && <p className="mensaje error" role="alert">{error}</p>}
    {aviso && <p className="mensaje exito" role="status">{aviso}</p>}
    <div className="columnas">
      <section className="panel">
        <h2>Catálogo de planes</h2>
        <form onSubmit={guardarPlan}>
          <label>Nombre del plan<input required maxLength={100} value={planForm.nombre} onChange={e => setPlanForm({ ...planForm, nombre: e.target.value })} /></label>
          <label>Duración en días<input required type="number" min="1" max="3650" value={planForm.duracion_dias} onChange={e => setPlanForm({ ...planForm, duracion_dias: Number(e.target.value) })} /></label>
          <label>Precio<input required type="number" min="0" step="0.01" value={planForm.precio} onChange={e => setPlanForm({ ...planForm, precio: e.target.value })} /></label>
          <label>Estado<select value={planForm.activo ? 'activo' : 'inactivo'} onChange={e => setPlanForm({ ...planForm, activo: e.target.value === 'activo' })}><option value="activo">Activo</option><option value="inactivo">Inactivo</option></select></label>
          <div className="acciones"><button disabled={cargando}>{planEditado ? 'Guardar cambios' : 'Crear plan'}</button>{planEditado && <button type="button" className="secundario" onClick={() => { setPlanEditado(null); setPlanForm({ nombre: '', duracion_dias: 30, precio: '0.00', activo: true }) }}>Cancelar</button>}</div>
        </form>
        <ul className="lista">{planes.map(plan => <li key={plan.id}><div><strong>{plan.nombre}</strong><small>{plan.duracion_dias} días · S/ {plan.precio}</small><span className={plan.activo ? 'estado activo' : 'estado'}>{plan.activo ? 'Activo' : 'Inactivo'}</span></div><div className="fila-acciones"><button type="button" className="enlace" onClick={() => { setPlanEditado(plan.id); setPlanForm({ nombre: plan.nombre, duracion_dias: plan.duracion_dias, precio: plan.precio, activo: plan.activo }) }}>Editar</button>{plan.activo && <button type="button" className="enlace peligro" disabled={cargando} onClick={() => void desactivarPlan(plan)}>Desactivar</button>}</div></li>)}</ul>
      </section>
      <section className="panel">
        <h2>{renovarId ? 'Renovar membresía' : 'Activar socio'}</h2>
        <p>Registra los datos del socio, asígnale una sede y un plan vigente.</p>
        <form onSubmit={guardarSocio}>
          <label>Nombres<input required maxLength={100} value={socioForm.nombres} onChange={e => setSocioForm({ ...socioForm, nombres: e.target.value })} /></label>
          <label>Apellidos<input required maxLength={120} value={socioForm.apellidos} onChange={e => setSocioForm({ ...socioForm, apellidos: e.target.value })} /></label>
          <label>DNI<input required inputMode="numeric" pattern="[0-9]{8}" maxLength={8} value={socioForm.dni} onChange={e => setSocioForm({ ...socioForm, dni: e.target.value.replace(/\D/g, '') })} /></label>
          <label>Correo de Google<input required type="email" value={socioForm.correo} onChange={e => setSocioForm({ ...socioForm, correo: e.target.value })} /></label>
          <label>Sede<select required value={socioForm.sede_id} onChange={e => setSocioForm({ ...socioForm, sede_id: e.target.value })}><option value="">Selecciona sede</option>{sedes.filter(sede => sede.activa).map(sede => <option key={sede.id} value={sede.id}>{sede.nombre}</option>)}</select></label>
          <label>Plan<select required value={socioForm.plan_id} onChange={e => cambiarPlan(e.target.value)}><option value="">Selecciona plan</option>{planesActivos.map(plan => <option key={plan.id} value={plan.id}>{plan.nombre} · S/ {plan.precio}</option>)}</select></label>
          <label>Inicio de membresía<input required type="date" min={hoy} value={socioForm.fecha_inicio} onChange={e => cambiarInicio(e.target.value)} /></label>
          <label>Fin de membresía<input required type="date" readOnly value={socioForm.fecha_fin} /></label>
          <div className="acciones"><button disabled={cargando || (!demo && (!sedes.length || !planesActivos.length))}>{renovarId ? 'Renovar membresía' : 'Activar socio'}</button>{renovarId && <button type="button" className="secundario" onClick={() => setRenovarId(null)}>Cancelar renovación</button>}</div>
        </form>
      </section>
    </div>
    <section className="panel panel-socios-lista"><h2>Socios registrados</h2><ul className="lista">{socios.map(socio => <li key={socio.id}><div><strong>{socio.apellidos}, {socio.nombres}</strong><small>DNI {socio.dni} · {socio.correo}</small><small>{socio.membresia ? `Membresía: ${socio.membresia.fecha_inicio} al ${socio.membresia.fecha_fin}` : 'Sin membresía registrada'}</small><span className={socio.activo ? 'estado activo' : 'estado'}>{socio.activo ? 'Cuenta activa' : 'Cuenta inactiva'}</span></div></li>)}</ul></section>
  </div>
}

export default SociosApp
