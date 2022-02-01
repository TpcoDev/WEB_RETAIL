# -*- coding: utf-8 -*-

import uuid
from odoo import http
from odoo.http import request, Response
import jsonschema
from jsonschema import validate
import json


class DescarteController(http.Controller):

    @http.route('/tpco/odoo/ws002', auth="public", type="json", method=['POST'], csrf=False)
    def descarte(self, **post):
        post = json.loads(http.request.httprequest.data)
        res = {}
        as_token = uuid.uuid4().hex
        mensaje_error = {
            "Token": as_token,
            "RespCode": -1,
            "RespMessage": "Error de conexión"
        }

        try:
            myapikey = request.httprequest.headers.get("Authorization")
            if not myapikey:
                # self.create_message_log("ws001", as_token, post, 'RECHAZADO', 'API KEY no existe')
                mensaje_error['RespCode'] = -2
                mensaje_error['RespMessage'] = f"Rechazado: API KEY no existe"
                return mensaje_error

            user_id = request.env["res.users.apikeys"]._check_credentials(scope="rpc", key=myapikey)
            request.uid = user_id
            if user_id:
                res['token'] = as_token

                stock_scrap = request.env['stock.scrap']
                obj_stock_scrap = stock_scrap.sudo().search([('lot_id', '=', post['EPCCode'])])
                if not obj_stock_scrap:
                    obj_scrap = obj_stock_scrap.sudo().create({'lot_id': post['EPCCode']})
                else:
                    mensaje_error_existencia = {
                        "Token": as_token,
                        "RespCode": -3,
                        "RespMessage": "Rechazado: Ya existe el registro que pretende crear"
                    }
                    return mensaje_error_existencia

                mensaje_correcto = {
                    "Token": as_token,
                    'idDescarte': obj_scrap.id,
                    'fechaOperacion:': obj_scrap.create_date,
                    'user': obj_scrap.user,
                    'idHandheld': obj_scrap.idHandheld,
                    'EPCCode': obj_scrap.EPCCode,
                    'codigo': 0,
                    'mensaje': "Activo descartado de inventario"
                }
                return mensaje_correcto

        except Exception as e:
            mensaje_error = {
                "Token": as_token,
                "RespCode": -5,
                "RespMessage": "Rechazado: Autenticación fallida"
            }
            mensaje_error['RespMessage'] = f"Error: {str(e)}"
            return mensaje_error
