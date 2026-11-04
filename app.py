import streamlit as st
from datetime import datetime

# Configuración inicial del SAM basada en el calendario provisto
if 'participantes' not in st.session_state:
    st.session_state.participantes = [
        {"mano": 1, "nombre": "Persona 1", "fecha_reparto": "05 Sep 2026", "estado": "🔴 Pendiente", "fecha_pago": "-"},
        {"mano": 2, "nombre": "Persona 2", "fecha_reparto": "05 Oct 2026", "estado": "🔴 Pendiente", "fecha_pago": "-"},
        {"mano": 3, "nombre": "María", "fecha_reparto": "05 Nov 2026", "estado": "🔴 Pendiente", "fecha_pago": "-"},
        {"mano": 4, "nombre": "Alejandra", "fecha_reparto": "05 Dic 2026", "estado": "🔴 Pendiente", "fecha_pago": "-"},
        {"mano": 5, "nombre": "Theo", "fecha_reparto": "05 Ene 2027", "estado": "🔴 Pendiente", "fecha_pago": "-"},
        {"mano": 6, "nombre": "Teilor", "fecha_reparto": "05 Feb 2027", "estado": "🔴 Pendiente", "fecha_pago": "-"},
        {"mano": 7, "nombre": "Eduardo", "fecha_reparto": "05 Mar 2027", "estado": "🔴 Pendiente", "fecha_pago": "-"},
        {"mano": 8, "nombre": "Daniela", "fecha_reparto": "05 Abr 2027", "estado": "🔴 Pendiente", "fecha_pago": "-"},
        {"mano": 9, "nombre": "Johnny", "fecha_reparto": "05 May 2027", "estado": "🔴 Pendiente", "fecha_pago": "-"},
        {"mano": 10, "nombre": "Andreina", "fecha_reparto": "05 Jun 2027", "estado": "🔴 Pendiente", "fecha_pago": "-"},
        {"mano": 11, "nombre": "Vanessa", "fecha_reparto": "05 Jul 2027", "estado": "🔴 Pendiente", "fecha_pago": "-"}
    ]

st.title("💰 Gestor Automatizado de SAM")
st.write("Sube el comprobante de transferencia para actualizar la lista de WhatsApp al instante.")

# Componente para cargar el comprobante
comprobante = st.file_uploader("📸 Cargar comprobante de pago (Imagen/PDF)", type=["png", "jpg", "jpeg", "pdf"])

if comprobante is not None:
    st.success("Comprobante recibido con éxito.")
    
    # Selector manual de asignación rápido (optimiza el flujo si hay nombres similares)
    nombres_lista = [p["nombre"] for p in st.session_state.participantes]
    seleccionado = st.selectbox("Confirmar quién realizó el pago:", nombres_lista)
    fecha_hoy = datetime.today().strftime('%d/%m/%Y')
    
    if st.button("Registrar Pago"):
        for p in st.session_state.participantes:
            if p["nombre"] == seleccionado:
                p["estado"] = "🟢 Pagado"
                p["fecha_pago"] = f"Pagó el {fecha_hoy}"
        st.balloons()

# Construcción dinámica del mensaje de WhatsApp
total_pagados = sum(1 for p in st.session_state.participantes if p["estado"] == "🟢 Pagado")
recaudado = total_pagados * 100000

msg = "💰 *CONTROL DE PAGO - SAM COMPLETO* 💰\n"
msg += f"Cuota Mensual: $100.000 | Total Recaudado: ${recaudado:,}\n"
msg += f"Al día: {total_pagados} / 11 personas\n"
msg += "-----------------------------------------\n"
msg += "*ESTADO DE REPARTO & MANOS:*\n\n"

for p in st.session_state.participantes:
    emoji = "[🟢]" if "🟢" in p["estado"] else "[🔴]"
    detalle_pago = f" - _{p['fecha_pago']}_" if p["fecha_pago"] != "-" else " - _Falta pago_"
    msg += f"{p['mano']}️⃣ {emoji} *{p['fecha_reparto']}:* {p['nombre']}{detalle_pago}\n"

msg += "-----------------------------------------\n"
msg += "🔄 _Mensaje actualizado automáticamente._"

# Cuadro de salida listo para copiar
st.subheader("📋 Mensaje para WhatsApp listo")
st.text_area("Copia el texto de abajo:", value=msg, height=350)
