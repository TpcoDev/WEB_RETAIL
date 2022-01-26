# -*- coding: utf-8 -*-

import uuid
from odoo import http
from odoo.http import request, Response
import jsonschema
from jsonschema import validate
import json


class OdooController(http.Controller):

    @http.route('/tpco/odoo/enrolamiento', auth="public", type="json", method=['POST'], csrf=False)
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
                post = post['params']

                product_tmpl = http.request.env['product.template']
                tipo_prenda = http.request.env['tipo.prenda']
                marca = http.request.env['marca']
                tamanno = http.request.env['tamanno']
                origen = http.request.env['origen']
                color = http.request.env['color']
                genero = http.request.env['genero']

                obj_tipo_prenda = tipo_prenda.sudo().search(
                    [('name', '=', post['params']['detalleActivos'][0]['tipoPrenda'])])
                if not obj_tipo_prenda:
                    tipo_prenda_nuevo = tipo_prenda.sudo().create(
                        {'name': post['params']['detalleActivos'][0]['tipoPrenda']})
                    tipo_prenda_id = tipo_prenda_nuevo.id
                else:
                    tipo_prenda_id = obj_tipo_prenda.id

                obj_marca = marca.sudo().search([('name', '=', post['params']['detalleActivos'][0]['marca'])])
                if not obj_marca:
                    marca_nuevo = marca.sudo().create({'name': post['params']['detalleActivos'][0]['marca']})
                    marca_id = marca_nuevo.id
                else:
                    marca_id = obj_marca.id

                obj_tamanno = tamanno.sudo().search([('name', '=', post['params']['detalleActivos'][0]['tamaño'])])
                if not obj_tamanno:
                    tamanno_nuevo = tamanno.sudo().create({'name': post['params']['detalleActivos'][0]['tamaño']})
                    tamanno_id = tamanno_nuevo.id
                else:
                    tamanno_id = obj_tamanno.id

                obj_origen = tipo_prenda.sudo().search([('name', '=', post['params']['detalleActivos'][0]['origen'])])
                if not obj_origen:
                    origen_nuevo = origen.sudo().create({'name': post['params']['detalleActivos'][0]['origen']})
                    origen_id = origen_nuevo.id
                else:
                    origen_id = obj_origen.id

                obj_color = color.sudo().search([('name', '=', post['params']['detalleActivos'][0]['color'])])
                if not obj_color:
                    color_nuevo = color.sudo().create({'name': post['params']['detalleActivos'][0]['color']})
                    color_id = color_nuevo.id
                else:
                    color_id = obj_color.id

                obj_genero = genero.sudo().search([('name', '=', post['params']['detalleActivos'][0]['genero'])])
                if not obj_genero:
                    genero_nuevo = genero.sudo().create({'name': post['params']['detalleActivos'][0]['genero']})
                    genero_id = genero_nuevo.id
                else:
                    genero_id = obj_genero.id

                product_tmpl_nuevo = product_tmpl.sudo().create({
                    'name': post['params']['detalleActivos'][0]['nombreActivo'],
                    'tipo_prenda_id': tipo_prenda_id,
                    'marca_id': marca_id,
                    'tamanno_id': tamanno_id,
                    'origen_id': origen_id,
                    'color_id': color_id,
                    'genero_id': genero_id
                })

                return {
                    "idEnrolamiento": product_tmpl_nuevo.id,
                    "fechaOperacion": product_tmpl_nuevo.create_date,
                    "detalleActivos": [
                        {
                            "EPCCode": post['params']['detalleActivos'][0]['DetalleEpc'][0]['EPCCode'],
                            "codigo": 0,
                            "mensaje": "Activo enrolado"
                        }
                    ]
                }

        except Exception as e:
            mensaje_error = {
                "Token": as_token,
                "RespCode": -5,
                "RespMessage": "Rechazado: Autenticación fallida"
            }
            # self.create_message_log("ws001", as_token, post, 'RECHAZADO', str(e))
            mensaje_error['RespMessage'] = f"Error: {str(e)}"
            return mensaje_error
