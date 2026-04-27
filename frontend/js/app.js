const API = 'http://127.0.0.1:5000'
let salonSeleccionado = null

// ── NAVEGACIÓN ──
function toggleMenu(id) {
    document.querySelectorAll('.nav-dropdown').forEach(d => {
        if (d.id !== id) d.classList.remove('open')
    })
    document.getElementById(id).classList.toggle('open')
}

document.addEventListener('click', function (e) {
    if (!e.target.closest('.nav-dropdown')) {
        document.querySelectorAll('.nav-dropdown').forEach(d => d.classList.remove('open'))
    }
})

function mostrarVista(nombre) {
    document.querySelectorAll('.vista').forEach(v => v.classList.remove('activa'))
    document.getElementById('vista-' + nombre).classList.add('activa')
    cerrarTodosMenus()
    if (nombre === 'salones') cargarSalones()
    if (nombre === 'alumnos') cargarAlumnos()
    if (nombre === 'materias') cargarMaterias()
    if (nombre === 'calificaciones') {
        cargarSelectorSalon()
        cargarCalificaciones()
    }
}

function cerrarTodosMenus() {
    document.querySelectorAll('.nav-dropdown').forEach(d => d.classList.remove('open'))
}

// ── MODALES ──
function abrirModal(id) {
    cerrarTodosMenus()
    document.getElementById(id).classList.add('open')
    if (id === 'modal-alumno') cargarSalonesEnSelect('alumno-salon')
    if (id === 'modal-calificacion') {
        cargarAlumnosEnSelect('cal-alumno')
        cargarMateriasEnSelect('cal-materia')
    }
}

function cerrarModal(id) {
    document.getElementById(id).classList.remove('open')
    limpiarModal(id)
}

function limpiarModal(id) {
    document.querySelectorAll('#' + id + ' input').forEach(i => i.value = '')
}

// ── FILTRO DE BUSQUEDA ──
function filtrarTabla(input, tablaId) {
    const texto = input.value.toLowerCase()
    const filas = document.querySelectorAll('#' + tablaId + ' tbody tr')
    filas.forEach(fila => {
        fila.style.display = fila.textContent.toLowerCase().includes(texto) ? '' : 'none'
    })
}

// ════════════════════════════════
// ── SALONES ──
// ════════════════════════════════

async function cargarSalones() {
    const res = await fetch(API + '/api/salones')
    const salones = await res.json()
    const body = document.getElementById('body-salones')

    if (salones.length === 0) {
        body.innerHTML = '<tr><td colspan="4" class="empty-state">No hay salones registrados</td></tr>'
        return
    }

    body.innerHTML = salones.map(s => `
        <tr>
            <td>${s.nombre}</td>
            <td>${s.grado}</td>
            <td>${s.turno}</td>
            <td>
                <div class="row-actions">
                    <button class="row-btn" onclick="editarSalon(${s.id}, '${s.nombre}', '${s.grado}', '${s.turno}')">Editar</button>
                    <button class="row-btn danger" onclick="eliminarSalon(${s.id})">Eliminar</button>
                </div>
            </td>
        </tr>
    `).join('')

    actualizarStats()
}

let salonEditandoId = null

function editarSalon(id, nombre, grado, turno) {
    salonEditandoId = id
    document.getElementById('titulo-modal-salon').textContent = 'Editar salón'
    document.getElementById('salon-nombre').value = nombre
    document.getElementById('salon-grado').value = grado
    document.getElementById('salon-turno').value = turno
    document.getElementById('modal-salon').classList.add('open')
}

async function guardarSalon() {
    const nombre = document.getElementById('salon-nombre').value.trim()
    const grado = document.getElementById('salon-grado').value.trim()
    const turno = document.getElementById('salon-turno').value

    if (!nombre || !grado) return alert('Completa todos los campos')

    const metodo = salonEditandoId ? 'PUT' : 'POST'
    const url = salonEditandoId ? API + '/api/salones/' + salonEditandoId : API + '/api/salones'

    await fetch(url, {
        method: metodo,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre, grado, turno })
    })

    salonEditandoId = null
    document.getElementById('titulo-modal-salon').textContent = 'Nuevo salón'
    cerrarModal('modal-salon')
    cargarSalones()
}

async function eliminarSalon(id) {
    if (!confirm('¿Eliminar este salón?')) return
    await fetch(API + '/api/salones/' + id, { method: 'DELETE' })
    cargarSalones()
}

// ════════════════════════════════
// ── ALUMNOS ──
// ════════════════════════════════

async function cargarAlumnos() {
    const res = await fetch(API + '/api/alumnos')
    const alumnos = await res.json()
    const body = document.getElementById('body-alumnos')

    if (alumnos.length === 0) {
        body.innerHTML = '<tr><td colspan="5" class="empty-state">No hay alumnos registrados</td></tr>'
        return
    }

    body.innerHTML = alumnos.map(a => `
        <tr>
            <td>${a.matricula}</td>
            <td>${a.nombre}</td>
            <td>${a.apellido}</td>
            <td>${a.salon_nombre || '—'}</td>
            <td>
                <div class="row-actions">
                    <button class="row-btn" onclick="editarAlumno(${a.id}, '${a.nombre}', '${a.apellido}', '${a.matricula}', ${a.salon_id})">Editar</button>
                    <button class="row-btn danger" onclick="eliminarAlumno(${a.id})">Eliminar</button>
                </div>
            </td>
        </tr>
    `).join('')

    actualizarStats()
}

let alumnoEditandoId = null

function editarAlumno(id, nombre, apellido, matricula, salon_id) {
    alumnoEditandoId = id
    document.getElementById('titulo-modal-alumno').textContent = 'Editar alumno'
    document.getElementById('alumno-nombre').value = nombre
    document.getElementById('alumno-apellido').value = apellido
    document.getElementById('alumno-matricula').value = matricula
    cargarSalonesEnSelect('alumno-salon', salon_id)
    document.getElementById('modal-alumno').classList.add('open')
}

async function guardarAlumno() {
    const nombre = document.getElementById('alumno-nombre').value.trim()
    const apellido = document.getElementById('alumno-apellido').value.trim()
    const matricula = document.getElementById('alumno-matricula').value.trim()
    const salon_id = document.getElementById('alumno-salon').value

    if (!nombre || !apellido || !matricula || !salon_id) return alert('Completa todos los campos')

    const metodo = alumnoEditandoId ? 'PUT' : 'POST'
    const url = alumnoEditandoId ? API + '/api/alumnos/' + alumnoEditandoId : API + '/api/alumnos'

    await fetch(url, {
        method: metodo,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre, apellido, matricula, salon_id: parseInt(salon_id) })
    })

    alumnoEditandoId = null
    document.getElementById('titulo-modal-alumno').textContent = 'Nuevo alumno'
    cerrarModal('modal-alumno')
    cargarAlumnos()
}

async function eliminarAlumno(id) {
    if (!confirm('¿Eliminar este alumno?')) return
    await fetch(API + '/api/alumnos/' + id, { method: 'DELETE' })
    cargarAlumnos()
}

// ════════════════════════════════
// ── MATERIAS ──
// ════════════════════════════════

async function cargarMaterias() {
    const res = await fetch(API + '/api/materias')
    const materias = await res.json()
    const body = document.getElementById('body-materias')

    if (materias.length === 0) {
        body.innerHTML = '<tr><td colspan="3" class="empty-state">No hay materias registradas</td></tr>'
        return
    }

    body.innerHTML = materias.map(m => `
        <tr>
            <td>${m.nombre}</td>
            <td>${m.min_aprobatorio}</td>
            <td>
                <div class="row-actions">
                    <button class="row-btn danger" onclick="eliminarMateria(${m.id})">Eliminar</button>
                </div>
            </td>
        </tr>
    `).join('')

    actualizarStats()
}

async function guardarMateria() {
    const nombre = document.getElementById('materia-nombre').value.trim()
    const min_aprobatorio = parseFloat(document.getElementById('materia-min').value)

    if (!nombre) return alert('Escribe el nombre de la materia')

    await fetch(API + '/api/materias', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre, min_aprobatorio })
    })

    cerrarModal('modal-materia')
    cargarMaterias()
}

async function eliminarMateria(id) {
    if (!confirm('¿Eliminar esta materia?')) return
    await fetch(API + '/api/materias/' + id, { method: 'DELETE' })
    cargarMaterias()
}

// ════════════════════════════════
// ── CALIFICACIONES ──
// ════════════════════════════════

async function cargarCalificaciones() {
    const body = document.getElementById('body-calificaciones')
    if (!salonSeleccionado) {
        body.innerHTML = '<tr><td colspan="6" class="empty-state">Selecciona un salón para ver las calificaciones</td></tr>'
        return
    }
    const res = await fetch(API + '/api/calificaciones/salon/' + salonSeleccionado)
    const cals = await res.json()

    if (cals.length === 0) {
        body.innerHTML = '<tr><td colspan="6" class="empty-state">No hay calificaciones en este salón</td></tr>'
        return
    }

    body.innerHTML = cals.map(c => `
        <tr>
            <td>${c.alumno_nombre} ${c.alumno_apellido}</td>
            <td>${c.materia_nombre}</td>
            <td>${c.calificacion}</td>
            <td>${c.periodo}</td>
            <td><span class="badge ${c.aprobado ? 'badge-green' : 'badge-red'}">${c.aprobado ? 'Aprobado' : 'Reprobado'}</span></td>
            <td>
                <div class="row-actions">
                    <button class="row-btn danger" onclick="eliminarCalificacion(${c.id})">Eliminar</button>
                </div>
            </td>
        </tr>
    `).join('')
}

async function cargarSelectorSalon() {
    const res = await fetch(API + '/api/salones')
    const salones = await res.json()
    const selector = document.getElementById('selector-salon-cal')
    selector.innerHTML = '<option value="">Seleccionar salón...</option>' +
        salones.map(s => `<option value="${s.id}">${s.nombre} - ${s.grado}</option>`).join('')
}

function cambiarSalon(val) {
    salonSeleccionado = parseInt(val)
    cargarCalificaciones()
}

async function guardarCalificacion() {
    const alumno_id = document.getElementById('cal-alumno').value
    const materia_id = document.getElementById('cal-materia').value
    const calificacion = parseFloat(document.getElementById('cal-calificacion').value)
    const periodo = document.getElementById('cal-periodo').value.trim()

    if (!alumno_id || !materia_id || isNaN(calificacion) || !periodo) return alert('Completa todos los campos')

    const res = await fetch(API + '/api/calificaciones', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ alumno_id: parseInt(alumno_id), materia_id: parseInt(materia_id), calificacion, periodo })
    })

    if (res.status === 500) {
        alert('Ya existe una calificación para este alumno en esta materia y periodo. Si deseas cambiarla, elimina la existente primero.')
        return
    }

    cerrarModal('modal-calificacion')
    cargarCalificaciones()
}

async function eliminarCalificacion(id) {
    if (!confirm('¿Eliminar esta calificación?')) return
    await fetch(API + '/api/calificaciones/' + id, { method: 'DELETE' })
    cargarCalificaciones()
}

// ════════════════════════════════
// ── SELECTS DINÁMICOS ──
// ════════════════════════════════

async function cargarSalonesEnSelect(selectId, valorSeleccionado = null) {
    const res = await fetch(API + '/api/salones')
    const salones = await res.json()
    const select = document.getElementById(selectId)
    select.innerHTML = salones.map(s =>
        `<option value="${s.id}" ${s.id == valorSeleccionado ? 'selected' : ''}>${s.nombre} - ${s.grado}</option>`
    ).join('')
}

async function cargarAlumnosEnSelect(selectId) {
    const res = await fetch(API + '/api/alumnos')
    const alumnos = await res.json()
    const select = document.getElementById(selectId)
    select.innerHTML = alumnos.map(a =>
        `<option value="${a.id}">${a.nombre} ${a.apellido}</option>`
    ).join('')
}

async function cargarMateriasEnSelect(selectId) {
    const res = await fetch(API + '/api/materias')
    const materias = await res.json()
    const select = document.getElementById(selectId)
    select.innerHTML = materias.map(m =>
        `<option value="${m.id}">${m.nombre}</option>`
    ).join('')
}

// ════════════════════════════════
// ── ESTADÍSTICAS ──
// ════════════════════════════════

async function actualizarStats() {
    const [resA, resS, resM] = await Promise.all([
        fetch(API + '/api/alumnos'),
        fetch(API + '/api/salones'),
        fetch(API + '/api/materias')
    ])
    const alumnos = await resA.json()
    const salones = await resS.json()
    const materias = await resM.json()

    document.getElementById('stat-alumnos').textContent = alumnos.length
    document.getElementById('stat-salones').textContent = salones.length
    document.getElementById('stat-materias').textContent = materias.length
}

// ── INICIALIZAR ──
actualizarStats()