# -*- coding: utf-8 -*-

import uuid
from odoo import http
from odoo.http import request, Response
import jsonschema
from jsonschema import validate
import json


class EnrolamientoController(http.Controller):

    @http.route('/tpco/odoo/ws001', auth="public", type="json", method=['POST'], csrf=False)
    def enrolamiento(self, **post):

        post = json.loads(request.httprequest.data)
        res = {}
        as_token = uuid.uuid4().hex
        mensaje_error = {
            "Token": as_token,
            "RespCode": -1,
            "RespMessage": "Error de conexión"
        }
        mensaje_correcto = {
            "Token": as_token,
            "RespCode": 0,
            "RespMessage": "Producto se agregó correctamente"
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

                product_tmpl = request.env['product.template']
                tipo_prenda = request.env['tipo.prenda']
                marca = request.env['marca']
                tamanno = request.env['tamanno']
                origen = request.env['origen']
                color = request.env['color']
                genero = request.env['genero']

                for detalle in post['params']['detalleActivos']:
                    product_tmpl_nuevo = product_tmpl.search([('default_code', '=', detalle['SKU'])], limit=1)
                    if not product_tmpl_nuevo:
                        obj_tipo_prenda = tipo_prenda.sudo().search(
                            [('name', '=', detalle['tipoPrenda'])])
                        if not obj_tipo_prenda:
                            obj_tipo_prenda = tipo_prenda.sudo().create(
                                {'name': detalle['tipoPrenda']})

                        obj_marca = marca.sudo().search([('name', '=', detalle['marca'])])
                        if not obj_marca:
                            obj_marca = marca.sudo().create({'name': detalle['marca']})

                        obj_tamanno = tamanno.sudo().search(
                            [('name', '=', detalle['tamanno'])])
                        if not obj_tamanno:
                            obj_tamanno = tamanno.sudo().create(
                                {'name': detalle['tamanno']})

                        obj_origen = tipo_prenda.sudo().search(
                            [('name', '=', detalle['origen'])])
                        if not obj_origen:
                            obj_origen = origen.sudo().create({'name': detalle['origen']})

                        obj_color = color.sudo().search([('name', '=', detalle['color'])])
                        if not obj_color:
                            obj_color = color.sudo().create({'name': detalle['color']})

                        obj_genero = genero.sudo().search(
                            [('name', '=', detalle['genero'])])
                        if not obj_genero:
                            obj_genero = genero.sudo().create({'name': detalle['genero']})

                        product_tmpl_nuevo = product_tmpl.sudo().create({
                            'name': detalle['nombreActivo'],
                            'default_code': detalle['SKU'],
                            'tipo_prenda_id': obj_tipo_prenda.id,
                            'marca_id': obj_marca.id,
                            'tamanno_id': obj_tamanno.id,
                            'origen_id': obj_origen.id,
                            'color_id': obj_color.id,
                            'genero_id': obj_genero.id,
                            'list_price': 1.00,
                            'standard_price': 0.00,
                            'use_expiration_date': False,
                            'tracking': 'serial',
                            'purchase_ok': True,
                            'sale_ok': True,
                            'type': 'product'

                        })

                    return mensaje_correcto
                else:
                    mensaje_error = {
                        "Token": as_token,
                        "RespCode": -3,
                        "RespMessage": "Rechazado: Ya existe el registro que pretende crear"
                    }
                    return mensaje_error

        except Exception as e:
            mensaje_error = {
                "Token": as_token,
                "RespCode": -5,
                "RespMessage": "Rechazado: Autenticación fallida"
            }
            mensaje_error['RespMessage'] = f"Error: {str(e)}"
            return mensaje_error
