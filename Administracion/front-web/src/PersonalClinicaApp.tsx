import { useEffect, useState, type FormEvent } from 'react'
import { API_URL } from './config/env'

type RolClinica = 'recepcionista_clinica' | 'administrador_clinica'
type Clinica = { id: string; razon_social: string; activa: boolean }
type Personal = {
  id: string; nombres: string; apellidos: string; dni: string; correo: string
  rol: RolClinica; clinica_id: string; activo: boolean
}
type PersonalEntrada = Omit<Personal, 'id' | 'activo'>
type ErrorCampo = { campo: string; mensaje: string }

const formularioVacio: PersonalEntrada = {
  nombres: '', apellidos: '', dni: '', correo: '', rol: 'recepcionista_clinica', clinica_id: '',
}
const clinicasMuestra: Clinica[] = [
  { id: 'demo-clinica', razon_social: 'Clínica Vida Activa', activa: true },
]

function mensajeError(error: unknown) {
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
  const contenido = await respuesta.json().catch(() => null) as
    ({ mensaje?: string; detalles?: ErrorCampo[] } | null)
  if (!respuesta.ok) {
    const campo = contenido?.detalles?.map(item => `${item.campo}: ${item.mensaje}`).join(' · ')
    throw new Error(campo || contenido?.mensaje || 'No se pudo completar la solicitud.')
  }
  return contenido as T
}

function PersonalClinicaApp() {
  const token = sessionStorage.getItem('pikafit_admin_access') ?? ''
  const demo = !token
  const [clinicas, setClinicas] = useState<Clinica[]>(demo ? clinicasMuestra : [])
  const [personal, setPersonal] = useState<Personal[]>([])
  const [formulario, setFormulario] = useState<PersonalEntrada>(formularioVacio)
  const [editado, setEditado] = useState<string | null>(null)
  const [error, setError] = useState('')
  const [aviso, setAviso] = useState('')
  const [cargando, setCargando] = useState(false)

  async function cargar() {
    if (!token) return
    const [clinicasActuales, cuentas] = await Promise.all([
      solicitar<Clinica[]>('clinicas/', token),
      solicitar<Personal[]>('personal-clinica/', token),
    ])
    setClinicas(clinicasActuales)
    setPersonal(cuentas)
  }

  useEffect(() => {
    if (token) void cargar().catch(cause => setError(mensajeError(cause)))
  }, [token])

  function editar(cuenta: Personal) {
    setEditado(cuenta.id)
    setFormulario({
      nombres: cuenta.nombres, apellidos: cuenta.apellidos, dni: cuenta.dni,
      correo: cuenta.correo, rol: cuenta.rol, clinica_id: cuenta.clinica_id,
    })
    setError(''); setAviso('')
  }

  function cancelar() {
    setEditado(null); setFormulario(formularioVacio)
  }

  async function guardar(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setError(''); setAviso(''); setCargando(true)
    try {
      const datos = {
        ...formulario,
        nombres: formulario.nombres.trim(), apellidos: formulario.apellidos.trim(),
        correo: formulario.correo.trim().toLowerCase(),
      }
      if (!/^[0-9]{8}$/.test(datos.dni)) throw new Error('El DNI debe tener 8 dígitos.')
      if (!clinicas.some(clinica => clinica.id === datos.clinica_id && clinica.activa))
        throw new Error('Selecciona una clínica activa.')
      if (personal.some(cuenta => cuenta.correo === datos.correo && cuenta.id !== editado))
        throw new Error('El correo ya está registrado.')
      if (personal.some(cuenta => cuenta.dni === datos.dni && cuenta.id !== editado))
        throw new Error('El DNI ya está registrado.')
      if (demo) {
        setPersonal(actual => editado
          ? actual.map(cuenta => cuenta.id === editado ? { ...cuenta, ...datos } : cuenta)
          : [...actual, { id: crypto.randomUUID(), ...datos, activo: true }])
      } else {
        await solicitar(editado ? `personal-clinica/${editado}/` : 'personal-clinica/',
          token, editado ? 'PATCH' : 'POST', datos)
        await cargar()
      }
      setAviso(editado ? 'Cuenta actualizada.' : 'Cuenta creada. El personal definirá su contraseña mediante el enlace de recuperación.')
      cancelar()
    } catch (cause) { setError(mensajeError(cause)) } finally { setCargando(false) }
  }

  async function desactivar(cuenta: Personal) {
    setError(''); setAviso(''); setCargando(true)
    try {
      if (demo) setPersonal(actual => actual.map(item => item.id === cuenta.id ? { ...item, activo: false } : item))
      else { await solicitar(`personal-clinica/${cuenta.id}/`, token, 'DELETE'); await cargar() }
      setAviso('Cuenta desactivada. Su historial se conserva y la sesión anterior queda invalidada.')
      if (editado === cuenta.id) cancelar()
    } catch (cause) { setError(mensajeError(cause)) } finally { setCargando(false) }
  }

  return <div className="seccion-personal">
    {demo && <p className="modo-demo">Vista de demostración: inicia sesión con una cuenta de Administración para guardar en el servidor.</p>}
    {error && <p className="mensaje error" role="alert">{error}</p>}
    {aviso && <p className="mensaje exito" role="status">{aviso}</p>}
    <div className="columnas">
      <section className="panel">
        <h2>{editado ? 'Editar personal de clínica' : 'Alta del personal de clínica'}</h2>
        <p>Registra recepcionistas y administradores de una clínica afiliada activa.</p>
        <form onSubmit={guardar}>
          <label>Nombres<input required maxLength={80} value={formulario.nombres} onChange={e => setFormulario({ ...formulario, nombres: e.target.value })} /></label>
          <label>Apellidos<input required maxLength={80} value={formulario.apellidos} onChange={e => setFormulario({ ...formulario, apellidos: e.target.value })} /></label>
          <label>DNI<input required inputMode="numeric" pattern="[0-9]{8}" maxLength={8} value={formulario.dni} onChange={e => setFormulario({ ...formulario, dni: e.target.value.replace(/\D/g, '') })} /></label>
          <label>Correo<input required type="email" value={formulario.correo} onChange={e => setFormulario({ ...formulario, correo: e.target.value })} /></label>
          <label>Rol<select required value={formulario.rol} onChange={e => setFormulario({ ...formulario, rol: e.target.value as RolClinica })}><option value="recepcionista_clinica">Recepción de clínica</option><option value="administrador_clinica">Administración de clínica</option></select></label>
          <label>Clínica afiliada<select required value={formulario.clinica_id} onChange={e => setFormulario({ ...formulario, clinica_id: e.target.value })}><option value="">Selecciona una clínica</option>{clinicas.filter(c => c.activa).map(c => <option key={c.id} value={c.id}>{c.razon_social}</option>)}</select></label>
          <div className="acciones"><button disabled={cargando || !clinicas.some(c => c.activa)}>{editado ? 'Guardar cambios' : 'Crear cuenta'}</button>{editado && <button className="secundario" type="button" onClick={cancelar}>Cancelar</button>}</div>
        </form>
      </section>
      <section className="panel">
        <h2>Cuentas del personal</h2>
        <ul className="lista">{personal.map(cuenta => <li key={cuenta.id}>
          <div><strong>{cuenta.apellidos}, {cuenta.nombres}</strong><small>{cuenta.correo} · DNI {cuenta.dni}</small><small>{cuenta.rol === 'recepcionista_clinica' ? 'Recepción' : 'Administración'} · {clinicas.find(c => c.id === cuenta.clinica_id)?.razon_social ?? 'Clínica no disponible'}</small><span className={cuenta.activo ? 'estado activo' : 'estado'}>{cuenta.activo ? 'Activa' : 'Inactiva'}</span></div>
          <div className="fila-acciones"><button className="enlace" type="button" onClick={() => editar(cuenta)}>Editar</button>{cuenta.activo && <button className="enlace peligro" type="button" disabled={cargando} onClick={() => void desactivar(cuenta)}>Desactivar</button>}</div>
        </li>)}</ul>
        {!personal.length && <p>Aún no hay personal registrado.</p>}
      </section>
    </div>
  </div>
}

export default PersonalClinicaApp
