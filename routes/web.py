''' Web Routes '''
from masonite.helpers.routes import get, post, group

ROUTES = [
    get('/', 'HomeController@index').name('welcome'),
    get('/login', 'LoginController@show'),
    get('/logout', 'LoginController@logout').middleware('auth'),
    post('/login', 'LoginController@store'),
    get('/register', 'RegisterController@show'),
    post('/register', 'RegisterController@store'),
]
