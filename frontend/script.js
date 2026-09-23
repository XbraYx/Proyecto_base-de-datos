
const API_URL = "http://127.0.0.1:5000";


// =====================================================
// CARGAR TODOS LOS PAQUETES
// =====================================================

async function cargarPaquetes() {

    const container = document.getElementById("packagesContainer");

    container.innerHTML = "Cargando...";

    try {

        const response = await fetch(
            `${API_URL}/api/paquetes`
        );

        if (!response.ok) {
            throw new Error("Error al consultar la API");
        }

        const paquetes = await response.json();

        container.innerHTML = "";

        if (paquetes.length === 0) {

            container.innerHTML = `
                <p>No hay paquetes registrados.</p>
            `;

            return;
        }

        paquetes.forEach(paquete => {

            const card = document.createElement("div");

            card.classList.add("package-card");

            card.innerHTML = `
                <h3>${paquete.tracking_number}</h3>

                <p>
                    <strong>Cliente:</strong>
                    ${paquete.cliente}
                </p>

                <p>
                    <strong>Estado:</strong>
                    ${paquete.estado}
                </p>

                <p>
                    <strong>Drone:</strong>
                    ${paquete.drone ?? "Sin asignar"}
                </p>

                <p>
                    <strong>Origen:</strong>
                    ${paquete.origin}
                </p>

                <p>
                    <strong>Destino:</strong>
                    ${paquete.destination}
                </p>
            `;

            container.appendChild(card);
        });

    } catch (error) {

        console.error(error);

        container.innerHTML = `
            <p>
                No fue posible conectar con el servidor.
            </p>
        `;
    }
}


// =====================================================
// BUSCAR PAQUETE
// =====================================================

async function buscarPaquete() {

    const input = document.getElementById("trackingInput");

    const trackingNumber = input.value.trim();

    const message = document.getElementById("message");

    const packageInfo = document.getElementById("packageInfo");


    if (!trackingNumber) {

        message.textContent =
            "Introduce un número de rastreo.";

        return;
    }


    message.textContent = "Buscando...";

    packageInfo.classList.add("hidden");


    try {

        const response = await fetch(
            `${API_URL}/api/paquetes`
        );


        if (!response.ok) {
            throw new Error("Error en la API");
        }


        const paquetes = await response.json();


        const paquete = paquetes.find(
            p => p.tracking_number === trackingNumber
        );


        if (!paquete) {

            message.textContent =
                "No se encontró el paquete.";

            return;
        }


        // Mostrar información

        document.getElementById("trackingNumber").textContent =
            paquete.tracking_number;

        document.getElementById("client").textContent =
            paquete.cliente;

        document.getElementById("status").textContent =
            paquete.estado;

        document.getElementById("drone").textContent =
            paquete.drone ?? "Sin asignar";

        document.getElementById("origin").textContent =
            paquete.origin;

        document.getElementById("destination").textContent =
            paquete.destination;

        document.getElementById("weight").textContent =
            `${paquete.weight_kg} kg`;

        document.getElementById("delivery").textContent =
            paquete.estimated_delivery ?? "No disponible";


        packageInfo.classList.remove("hidden");

        message.textContent = "";


    } catch (error) {

        console.error(error);

        message.textContent =
            "No fue posible conectar con el servidor.";
    }
}


// =====================================================
// CARGAR PAQUETES AL ABRIR LA PÁGINA
// =====================================================

document.addEventListener(
    "DOMContentLoaded",
    cargarPaquetes
);
