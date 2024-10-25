document.addEventListener('DOMContentLoaded', () => {

    favoriteDiv = document.querySelector('#favorite-div');
    location = document.querySelector('#location');
    userId = favoriteDiv.getAttribute('data-user-id');

    FavoriteDiv.innerHTML = `
        <button id="favorite-button-${location}">Add to favorite</button>
    `

    document.querySelector(`#favorite-button-${location}`).addEventListener('click', () => {
        changeFavorite(userId, location);
    });


    function changeFavorite(userId, location) {
        fetch(`/favorite/${location}`, {
            method: 'POST',
            headers: {
                'Content-type': 'aplication/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
            // TODO
        })
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