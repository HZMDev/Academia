# -*- coding: utf-8 -*-

from odoo import models, fields, api

""""
Curso
• name: cadena, obligatorio, no repetido. Nombre del curso.
• plazas: entero, obligatorio. Número máximo de plazas disponibles.
• precio_hora: real, obligatorio, valor por defecto 4,5€. Coste por hora de docencia.

Asignatura
• name: cadena, obligatorio. Nombre de la asignatura.
• descripción: texto largo. Descripción de la asignatura.
• horas: entero, obligatorio. Número de horas de la asignatura
• precio: real, calculado. Precio total, número de horas por el precio hora del curso
asociado.

Evaluación
• fecha: fecha, obligatorio, Día en el que se realiza la evaluación.
• responsable: cadena, obligatorio. Nombre de la persona encargada de realizar la
evaluación.
• tipo: selección, Tipo de evaluación. Los valores disponibles son: o – Ordinaria, f –
Final, e – Extraordinaria. Valor por defecto “final”.

Evaluación
• fecha: fecha, obligatorio, Día en el que se realiza la evaluación.
• responsable: cadena, obligatorio. Nombre de la persona encargada de realizar la
evaluación.
• tipo: selección, Tipo de evaluación. Los valores disponibles son: o – Ordinaria, f –
Final, e – Extraordinaria. Valor por defecto “final”.
"""

class curso(models.Model):
    _name='academia.curso'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description='Gestion de un curso'

    sequence = fields.Integer(string="Secuencia", default=10)
    name=fields.Char(string='Nombre', required=True)
    plazas = fields.Integer(string='Plazas', required=True)
    precio_hora = fields.Float(string='Precio Hora', default=4.5)

    alumno_ids = fields.One2many('academia.alumno', 'curso_id', string="Alumnos")

    alumnos_totales = fields.Integer(string="Alumnos Totales", compute='_get_alumnos_totales')

    horas_totales = fields.Integer(string="Horas Totales", compute='_get_horas_totales')

    asignatura_ids = fields.One2many('academia.asignatura', 'curso_id', string="Asignaturas")

    @api.depends('alumno_ids')
    def _get_alumnos_totales(self):
        for curso in self:
            curso.alumnos_totales = len(curso.alumno_ids)

    @api.depends('asignatura_ids')
    def _get_horas_totales(self):
        for curso in self:
          for asignatura in curso.asignatura_ids:
              curso.horas_totales+=asignatura.horas

    def get_alumnos(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Alumnos',
            'view_mode': 'tree,form',
            'res_model': 'academia.alumno',
            'domain': [('curso_id', '=', self.id)],
            'target' : 'current',
        }
    
class profesor(models.Model):
    _name='academia.profesor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description='Gestion de un profesor'
    _order="name"

    sequence = fields.Integer(string="Secuencia", default=10)

    name=fields.Char(string='DNI', required=True)
    nombre = fields.Char(string='Nombre', required=True)
    apellidos = fields.Char(string='Apellidos', required=True)
    telefono_contacto = fields.Char(string='Telefono Contacto', required=True)

    #Relaciones
    asignatura_ids = fields.One2many('academia.asignatura', 'profesor_id', string="Asignaturas")
    evaluacion_ids = fields.One2many('academia.evaluacion', 'profesor_id', string="Evaluaciones")


class asignatura(models.Model):
    _name='academia.asignatura'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description='Gestion de una asignatura'
    
    sequence = fields.Integer(string="Secuencia", default=10)
    name=fields.Char(string='Nombre', required=True)
    descripcion = fields.Char(string='Descripcion')
    horas = fields.Integer(string='Horas', required=True)
    precio = fields.Float(string='Precio', compute='_get_precio')

    #Relaciones
    curso_id = fields.Many2one('academia.curso', string="Curso")
    profesor_id = fields.Many2one('academia.profesor', string="Profesor")
    evaluacion_ids = fields.Many2many('academia.evaluacion', string="Evaluaciones")
    alumno_ids = fields.Many2many('academia.alumno', string="Alumnos")

    @api.depends('curso_id')
    def _get_precio(self):
        for asignatura in self:
            asignatura.precio=asignatura.horas * asignatura.curso_id.precio_hora


class evaluacion(models.Model):
    _name='academia.evaluacion'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description='Gestion de una evaluacion'
    _order='fecha'

    sequence = fields.Integer(string="Secuencia", default=10)
    fecha = fields.Date(string='Fecha', required=True, help='Dia en que se realiza evaluacion')
    tipo = fields.Selection(string='Tipo', selection=[('o', 'Ordinaria'),('f', 'Final'),('e', 'Extraordinaria')], default='f')
    comentarios = fields.Char(string='Comentarios', help="Comentarios de la evaluacion", translate=True)

    #Relaciones
    asignatura_ids = fields.Many2many('academia.asignatura', string="Asignaturas")
    profesor_id = fields.Many2one('academia.profesor', string="DNI del profesor responsable")

    asignaturas_totales = fields.Integer(string="Asignaturas Totales", compute="_get_asignaturas_totales")

    @api.depends('asignatura_ids')
    def _get_asignaturas_totales(self):
        for evaluacion in self:
            evaluacion.asignaturas_totales = len(evaluacion.asignatura_ids)


class alumno(models.Model):
    _name='academia.alumno'
    _description='Gestion de un alumno'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order="name, fecha_nacimiento"

    sequence = fields.Integer(string="Secuencia", default=10)
    name=fields.Char(string='DNI', required=True)
    nombre = fields.Char(string='Nombre', required=True)
    apellidos = fields.Char(string='Apellidos', required=True) 
    telefono_contacto = fields.Char(string='Telefono Contacto', required=True)
    fecha_nacimiento = fields.Date(string="Fecha de Nacimiento", required=True)
    
    asignaturas_totales = fields.Integer(string="Asignaturas Totales", compute="_get_asignaturas_totales")

    #Relaciones
    asignatura_ids = fields.Many2many('academia.asignatura', string="Asignaturas")
    curso_id = fields.Many2one('academia.curso', string="Curso")

    @api.depends('asignatura_ids')
    def _get_asignaturas_totales(self):
        for alumno in self:
            alumno.asignaturas_totales = len(alumno.asignatura_ids)
