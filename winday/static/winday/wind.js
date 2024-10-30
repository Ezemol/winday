document.addEventListener('DOMContentLoaded', () => {

    const favoriteDiv = document.querySelector('#favorite-div');
    const location = document.querySelector('#location');
    const userId = favoriteDiv.getAttribute('data-user-id');
    let isFav = favoriteDiv.getAttribute('data-location-fav') === 'true';

    if (favoriteDiv) {
        favoriteDiv.innerHTML = `
            <button id="favorite-button" class="fav-button follow-button">
                ${isFav ? "Eliminar de favoritos" : "Agregar a favoritos"}
            </button>
        `;

        document.querySelector(`#favorite-button`).addEventListener('click', () => {
            let action = isFav ? "Eliminar de favoritos" : "Agregar a favoritos";
            console.log(action);

            changeFavorite(userId, location);
        });
    }

    function changeFavorite(userId, location) {
        fetch(`/favorite/${location}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                location:location
            }) 
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);

            if (result.is_fav !== undefined) {
                isFav = result.is_fav;
                document.querySelector(`#favorite-button`).innerHTML = 
                `${isFav ? "Eliminar de favoritos" : "Agregar a favoritos"}`;
            }
        })
        .catch(error => {
            console.error('Error', error);
            alert('Hubo un error inentando agregar/quitar lugar de tus favoritos.');
        });
    }

    // Funcion para obtener csrf token
    function getCookie(name) {
        let cookieValue = null;  // Inicializa el valor del cookie
        if (document.cookie && document.cookie !== '') {  // Verifica si hay cookies
            const cookies = document.cookie.split(';');  // Separa las cookies en un array
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();  // Limpia los espacios en blanco
                if (cookie.substring(0, name.length + 1) === (name + '=')) {  // Busca la cookie por su nombre
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));  // Decodifica el valor de la cookie
                    break;  // Sale del bucle una vez encontrada
                }
            }
        }
        return cookieValue;  // Devuelve el valor de la cookie
    }
});