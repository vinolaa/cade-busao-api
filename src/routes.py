from flask import Blueprint, request, make_response, jsonify

from src.settings.cors_headers import add_cors_headers

from src.services.auth_service import AuthService
from src.services.profile_service import ProfileService

api = Blueprint('api', __name__)


@api.route('/auth', methods=['OPTIONS', 'POST'])
def auth():
    if request.method == 'OPTIONS':
        return add_cors_headers(make_response())

    payload = request.get_json()
    method = payload.get('method')

    auth_service = AuthService()

    res = None
    if method == 'login':
        res = auth_service.login(payload.get('login'), payload.get('senha'))
    elif method == 'register':
        res = auth_service.register(payload.get('login'),
                                    payload.get('senha'),
                                    payload.get('confirmSenha'),
                                    payload.get('email'))

    return add_cors_headers(jsonify(res))


@api.route('/perfil/completar', methods=['OPTIONS', 'POST'])
def perfil_completar():
    if request.method == 'OPTIONS':
        return add_cors_headers(make_response())

    payload = request.get_json()

    perfil_service = ProfileService()

    res = perfil_service.completar_perfil(payload)
    return add_cors_headers(jsonify(res))
