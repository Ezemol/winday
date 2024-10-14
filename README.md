Templates:
layout.html: Es la base de todos los templates
login.html: Login template
register.html: Register template
index.html: Página principal


Que hace cada función?
index: Es la página principal que le aparece al usuario.
login_view: Es la función que se encarga de loguear al user.
logout_view: Es la función que se encarga de desloguear al user.
register: Es la función que se encarga de registrar un nuevo user.

API's:
follow_user: Es la función que se encarga de guardar o borrar el follow a otro user. Necesita un modelo Profile.
profile: Muestra el perfil de un usuario en específico.
profile_connections: Muestra una lista con los seguidores o seguidos de un usuario.

favorite: Es la función que se encarga de agregar los puntos favoritos marcados por cada user. Para esto va a usar un model, llamado Location.
show_calendary: Renderiza una página con un calendario para todas las fechas importantes de un user.
save_calendary: Es la función que se encarga de guardar las fechas o eventos que un usuario quiera.
new_comment: Es la función que se encarga de guardar un comentario hecho por un user. Usa un modelo Comment
location_review: Es la función que se encarga de guardar la reseña hecha por un usuario. Usa un modelo Location
find_wind: Es la función que se encarga de encontrar el viento en la localidad marcada por el user.
following_page: Muestra lista con los followers o followings de un user.
sell_page: Renderiza página de ventas.

Necesito usar rutas API's para conseguir los datos del viento y de las localizaciones.