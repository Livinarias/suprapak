# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class DataSheetLine(models.Model):
    _name = 'data.sheet.line'
    _description = 'Data sheet line'

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company.id)
    product_id = fields.Many2one('product.product', 'Product', required=True)
    product_qty = fields.Float('Quantity', required=True, digits='Product Unit of Measure', default=1.00)
    uom_id = fields.Many2one('uom.uom', 'Unit of measure', required=True)
    uom_categ_id = fields.Many2one('uom.category', 'Uom category')
    field_char = fields.Char('Field', default='None')

    # cost = fields.Float('Cost', digits='Account')
    # One2many
    sheet_id = fields.Many2one('data.sheet', 'Sheet')
    roll_id = fields.Many2one('data.sheet', 'Sheet')
    for_bag_id = fields.Many2one('data.sheet', 'Sheet')
    for_superlon_id = fields.Many2one('data.sheet', 'Sheet')
    refile_id = fields.Many2one('data.sheet','Sheet')
    revision_id = fields.Many2one('data.sheet','Sheet')
    gluped_id = fields.Many2one('data.sheet','Sheet')
    gluped2_id = fields.Many2one('data.sheet','Sheet')
    movie_type_product_id = fields.Many2one('data.sheet','Sheet')


    @api.onchange('product_id')
    def _oncahnge_product_id(self):
        if self.product_id:
            self.uom_id = self.product_id.uom_id
            self.uom_categ_id = self.product_id.uom_id.category_id


class DataSheet(models.Model):
    _name = 'data.sheet'
    _description = 'Data sheet'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    def _compute_production_ids(self):
        mp_obj = self.env['mrp.production']
        ids = self.bom_ids.ids
        mp = mp_obj.search([('bom_id', 'in', ids)])
        self.production_ids = mp

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company.id)
    opportunity_id = fields.Many2one('crm.lead', 'Opportunity')
    state = fields.Selection([('draft', 'Quote sheet'), ('sample', 'Sample Tab'),
                              ('order', 'Order Tab')],
                             'state', copy=False, default='draft')
    type_sheet = fields.Selection([('review', 'Review'), ('technical', 'Technical Approval'), ('design', 'Design approval'),
                                   ('approved','Approved'),('rejected','Rejected'),('obsolete','Obsolete'),
                                   ('rejected ','Rejected Technical '),('rejected_d','Rejected Design')], 'Type sheet')
    name = fields.Char('Name')
    product_id = fields.Many2one('product.template', 'Product')
    priority = fields.Selection([('0', 'Normal'), ('1', 'Low'), ('2', 'High'), ('3', 'Very High')], 'Priority')
    # Info Customer
    partner_id = fields.Many2one('res.partner', 'Customer')
    commentary = fields.Char('Commentary')
    product_code = fields.Char('Product code', help='Customer product code')
    sector = fields.Char('Sector')
    team_id = fields.Many2one('crm.team', 'Zone')
    currency_id = fields.Many2one('res.currency', 'Currency')
    # sheet line
    line_ids = fields.One2many('data.sheet.line', 'sheet_id', 'Bills of Materials')
    # One2many
    roll_ids = fields.One2many('data.sheet.line', 'roll_id', 'Rolls')
    for_bag_ids = fields.One2many('data.sheet.line','for_bag_id','Bag')
    for_superlon_ids = fields.One2many('data.sheet.line','for_superlon_id','Superlon')
    refile_ids = fields.One2many('data.sheet.line','refile_id','Refile')
    revision_ids = fields.One2many('data.sheet.line','revision_id','Refile')
    gluped_ids = fields.One2many('data.sheet.line','gluped_id','Gluped 1 to 2')
    gluped2_ids = fields.One2many('data.sheet.line','gluped2_id','Gluped 2 to 3')
    movie_type_product_ids = fields.One2many('data.sheet.line','movie_type_product_id','Product of Movie Type')
    # Info Tec
    print_class = fields.Selection([('external','External'),('internal','Internal')],'Print Class')
    print_type = fields.Many2one('print.type','Print Type')
    uom_id = fields.Many2one('uom.uom', 'Unit of measure')
    product_type_id = fields.Many2one('data.product.type', 'Product line')
    drawn_type_id = fields.Many2one('data.drawn.type', 'Draw type')
    movie_type_id = fields.Many2one('data.movie.type', 'Movie type')
    movie_type_products_ids = fields.Many2many('product.product','sheet_product_rel','sheet_id','product_id','Product for Movie Type')
    color_movie_id = fields.Many2one('data.movie.color', 'Color movie')
    chemical_composition = fields.Many2one('chemical.composition','Chemical Composition')
    # Info cant
    specification_width_id = fields.Many2one('specification.width','Specification width')
    specification_width_name = fields.Char('Long Planned')
    specification_long_id = fields.Many2one('specification.long','Specification long')
    caliber_id = fields.Many2one('data.caliber.type', 'Specification caliber')
    tolerance_width = fields.Float('Tolerance width')
    tolerance_long = fields.Float('Tolerance long')
    tolerance_caliber = fields.Float('Tolerance caliber')
    # Bool
    tongue = fields.Boolean('Tongue')
    thermal_adhesive = fields.Boolean('Thermal adhesive')
    print = fields.Boolean('Print')
    no_print = fields.Boolean('Without Print')
    rhombus = fields.Boolean('Rhombus')
    guillotine = fields.Boolean('Requires Guillotine')
    guillotine_mm = fields.Float('mm')
    # Comments
    comments = fields.Text('Comments')
    # Button
    quotation_count = fields.Integer(compute='_compute_sale_data', string="Number of Quotations")
    order_ids = fields.One2many('sale.order', 'sheet_id', string='Orders')
    photo = fields.Binary()
    tag_form_id = fields.Many2one('data.tag.form','Tag Form')
    material_id = fields.Many2one('data.material','Material')
    application_id = fields.Many2one('data.application.mode','Application Mode')
    position_id = fields.Many2one('data.application.position','Application Position')
    content_id = fields.Many2one('data.application.contents','Package Contents')
    quantity = fields.Char('Quantity')
    form_id = fields.Many2one('data.form','Form')
    overlap_id = fields.Many2one('width.overlap','Width Overlap')
    tolerance_overlap = fields.Float('Tolerance Overlap')
    overlap_location_id = fields.Many2one('overlap.location','Overlap Location')
    bom_id = fields.Many2one('mrp.bom', 'Actual BOM')
    bom_ids = fields.One2many('mrp.bom', 'sheet_id', 'Record')
    routing_id = fields.Many2one('mrp.routing','Routings')
    routings_ids = fields.Many2many('mrp.routing','sheet_routing_rel','sheet_id','routing_id','Routing')
    average_label_weight = fields.Float('Average Lable Weight', compute = '_compute_average_label_weight')
    roll_weight = fields.Float('Roll Weight', compute = '_compute_roll_weight')
    presentation_id = fields.Many2one('presentation','Presentation')
    presentation = fields.Char()
    meter_per_roll = fields.Char('Meters per roll')
    core_diameter_id = fields.Many2one('core.diameter','Core Diameter')
    embossing_number_id = fields.Many2one('embossing.number', 'Embossing Number')
    number_splices_id = fields.Many2one('number.splices','Number Splices')
    splice_type_id = fields.Many2one('splice.type','Splice Type')
    splicing_tape_id = fields.Many2one('splicing.tape','Splicing tape')
    seal_type_id = fields.Many2one('seal.type','Seal Type')
    sealing_tab = fields.Float('Sealing Tab')
    seal = fields.Char()
    mold_id = fields.Many2one('preformed','Mold')
    bottom_diameter = fields.Float('Bottom Diameter')
    upper_diameter = fields.Float('Upper Diameter')
    tab_length = fields.Float('Tab Length')
    band_height = fields.Float('Band Height')
    product = fields.Char('Product')
    long_modification = fields.Float('Long Modification')
    barcode_type_id = fields.Many2one('barcode.type','Barcode Type')
    barcode_number = fields.Integer('Number')
    mechanic_plan_id = fields.Many2one('mechanic.plan')
    mechanic_plan_ids = fields.Many2many('mechanic.plan','sheet_mechanic_rel','sheet_id','mechanic_id','Mechanic Plan')
    microperforated = fields.Boolean('Microperforated')
    microperforated_id = fields.Many2one('microperforated')
    microperforated_ids = fields.Many2many('microperforated','sheet_microperfored_rel','sheed_id','microperfored_id','Microperfored')
    drawn = fields.Boolean('Drawn')
    drawn_presentation_id = fields.Many2one('drawn.presentation','Drawn Presentation')
    waistband = fields.Boolean('Waistband')
    rod_number = fields.Integer('Rod Number')
    photo_format = fields.Binary('Photo Format')
    adhesive_type_id = fields.Many2one('adhesive.type','Adhesive Type')
    adhesive_type_selector = fields.Char()
    cold_foil = fields.Boolean('Cold Foil')
    cold_foil_id = fields.Many2one('cold.foil','Cold Foil Type')
    cold_foil_selector = fields.Char()
    cold_foil_width = fields.Integer('Cold Foil Width')
    cast = fields.Boolean('Cast & Cure')
    cast_reference = fields.Char('Reference')
    cast_width = fields.Char('Width Cast & Cure')
    ink_ids = fields.Many2many('inks','sheet_inks_rel','shhet_id','inks_id','Inks')
    required_match_print = fields.Boolean('required match Print')
    designer = fields.Many2one('designer', 'Designer')
    datetime = fields.Datetime('Date and Hour')
    Customer = fields.Many2one('res.partner','Customer')
    sign_customer = fields.Binary('Sign Customer')
    deliver_to = fields.Many2one('res.partner','Deliver to')
    sign_designer = fields.Binary('Sign Designer')
    vendor_date = fields.Date('Application date vendor')
    date_recieved_approved = fields.Date('Date Recieved Approved')
    observations = fields.Char('Observations')
    color_scale_id = fields.Many2one('color.scale','Color scale/check mark')
    complexity = fields.Selection([('poca','poca'),('baja','Baja'),('media','Media'),('alta','Alta')])
    control_change_id = fields.Many2one('control.change')
    control_changes_ids = fields.Many2many('control.change','sheet_control_rel','sheet_id','control_change_id')
    change_observation = fields.Char('Observations')
    separator_id = fields.Many2one('product.product','Separator')
    core_diameter = fields.Char('Core Diameter')
    width_core = fields.Float('Width Core')
    bag = fields.Many2one('product.product','Bag')
    box = fields.Many2one('product.product','Box')
    superlon = fields.Many2one('product.product','Superlon')
    tape_id = fields.Many2one('tape','Tape')#depende rollo....
    print_id = fields.Many2one('print.color')
    prints_ids = fields.Many2many('print.color','sheet_print_rel','sheet_id','print_id','Print Colors')
    plane_art = fields.Binary('Plane Art')
    funtional_test = fields.Binary('Funtional Test')
    repeat_id = fields.Many2one('repeat','Roller')
    room_large = fields.Char('Room Large')
    large_planned = fields.Char('Large Planned')
    gluped_id = fields.Many2one('product.product')
    for_rolls_ids = fields.Many2many('product.product','sheet_gluped_rel','sheet_id','gluped_id','For Rolls')
    for_bags_ids = fields.Many2many('product.product','sheet_gluped_rel','sheet_id','gluped_id','For Bags')
    for_superlon_id = fields.Many2one('product.product')
    for_superlons_ids = fields.Many2many('product.product','sheet_superlon_rel','sheet_id','for_superlon_id','For Superlon')
    for_box = fields.Selection([('supra','SUPRAPAK 2" 100 m BLANCA'),('supra2','SUPRAPAK 2" 100 m TRANSPARENTE')],'For Box')
    refiles_ids = fields.Many2many('product.product', 'sheet_gluped_rel', 'sheet_id', 'gluped_id', 'Tapes')
    revisions_ids = fields.Many2many('product.product','sheet_gluped_rel','sheet_id','gluped_id','Revisión')
    glupeds_ids = fields.Many2many('product.product','sheet_gluped_rel','sheet_id','gluped_id','Gluped 1 to 2')
    glupeds2_ids = fields.Many2many('product.product','sheet_gluped_rel','sheet_id','gluped_id','Gluped 3 to 4')
    # Production
    production_ids = fields.One2many('mrp.production', 'sheet_id', 'Productions', compute='_compute_production_ids')

    @api.onchange('specification_long_id')
    def _onchange_specification_long_id(self):
        if self.specification_long_id:
            self.tolerance_long = self.specification_long_id.tolerance

    @api.onchange('width_core')
    def _onchange_width_core(self):
        if self.width_core:
            self.width_core += 4

    @api.onchange('repeat_id')
    def _onchange_repeat_id(self):
        if self.repeat_id:
            self.room_large = self.repeat_id.room_large
            self.large_planned = self.repeat_id.large_planned

    @api.onchange('presentation_id')
    def _onchange_presentation_id(self):
        if self.presentation_id:
            self.presentation = self.presentation_id.name

    @api.depends('specification_width_id.name', 'specification_long_id.name', 'overlap_id.name', 'guillotine_mm',
                 'movie_type_id.density', 'movie_type_id.density', 'caliber_id.name', 'sealing_tab')
    def _compute_roll_weight(self):
        self.roll_weight = (self.specification_width_id.name + self.overlap_id.name / 2) * (
                    (self.specification_long_id.name + self.sealing_tab + self.guillotine_mm) *
                    (self.caliber_id.name * 0.04) * (self.movie_type_id.density))

    @api.depends('specification_width_id.name','specification_long_id.name','overlap_id.name','guillotine_mm',
                 'movie_type_id.density','movie_type_id.density','caliber_id.name','sealing_tab')
    def _compute_average_label_weight(self):
       self.average_label_weight = (self.specification_width_id.name+self.overlap_id.name/2)*(
               (self.specification_long_id.name+self.sealing_tab + self.guillotine_mm)*
                (self.caliber_id.name*0.04)*(self.movie_type_id.density))/1000

    @api.onchange('seal_type_id')
    def _onchange_seal_type_id(self):
        if self.seal_type_id:
            self.seal = self.seal_type_id.name

    @api.onchange('specification_width_id')
    def _onchange_specification_width_id(self):
        if self.specification_width_id:
            self.tolerance_width = self.specification_width_id.tolerance

    @api.onchange('adhesive_type_id')
    def _oncahnge_adhesive_type_id(self):
        if self.adhesive_type_id:
            self.adhesive_type_selector = self.adhesive_type_id.name

    @api.onchange('cold_foil_id')
    def _oncahnge_cold_foil_id(self):
        if self.cold_foil_id:
            self.cold_foil_selector = self.cold_foil_id.name

    @api.onchange('mold_id')
    def _onchange_mold_id(self):
        if self.mold_id:
            self.bottom_diameter = self.mold_id.bottom_diameter
            self.upper_diameter = self.mold_id.upper_diameter
            self.tab_length = self.mold_id.tab_length
            self.band_height = self.mold_id.band_height
            self.product = self.mold_id.product

    @api.onchange('overlap_id')
    def _onchange_overlap_id(self):
        if self.overlap_id:
            self.tolerance_overlap = self.overlap_id.tolerance

    def _compute_sale_data(self):
        for lead in self:
            lead.quotation_count = len(lead.order_ids)

    """@api.onchange('movie_type_id')
    def _onchange_movie_type_id(self):
        if self.movie_type_id:
            self.color_movie_id = self.movie_type_id.color_id"""

    @api.onchange('caliber_id')
    def _onchange_caliber_id(self):
        if self.caliber_id:
            self.tolerance_caliber = self.caliber_id.tolerance

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.uom_id = self.product_id.uom_id.id

    @api.onchange('bag')
    def _onchange_many2one(self):
        values = []
        if self.bag:
            self.line_ids.search([('field_char', '=', 'bag')]).unlink()
            dic = {
                'field_char': 'bag',
                'product_id': self.bag.id,
                'product_qty': 1,
                'uom_id': self.bag.uom_id.id
            }
            values.append((0, 0, dic))
        if values:
            self.write({'line_ids': values})


    @api.onchange('separator_id')
    def _onchange_many2one(self):
        values = []
        if self.separator_id:
            self.line_ids.search([('field_char', '=', 'separator_id')]).unlink()
            dic = {
                'field_char': 'separator_id',
                'product_id': self.separator_id.id,
                'product_qty': 1,
                'uom_id': self.separator_id.uom_id.id
            }
            values.append((0, 0, dic))
        if values:
            self.write({'line_ids': values})

    @api.onchange('box')
    def _onchange_many2one(self):
        values = []
        if self.box:
            self.line_ids.search([('field_char', '=', 'box')]).unlink()
            dic = {
                'field_char': 'box',
                'product_id': self.box.id,
                'product_qty': 1,
                'uom_id': self.box.uom_id.id
            }
            values.append((0, 0, dic))
        if values:
            self.write({'line_ids': values})

    @api.onchange('superlon')
    def _onchange_many2one(self):
        values = []
        if self.superlon:
            self.line_ids.search([('field_char', '=', 'superlon')]).unlink()
            dic = {
                'field_char': 'superlon',
                'product_id': self.superlon.id,
                'product_qty': 1,
                'uom_id': self.superlon.uom_id.id
            }
            values.append((0, 0, dic))
        if values:
            self.write({'line_ids': values})


    @api.onchange('roll_ids')
    def _onchange_one2many(self):
        for line in self.roll_ids:
            line.sheet_id = self


    @api.onchange('for_bag_ids')
    def _onchange_one2many(self):
        for line in self.for_bag_ids:
            line.sheet_id = self\


    @api.onchange('for_superlon_ids')
    def _onchange_one2many(self):
        for line in self.for_superlon_ids:
            line.sheet_id = self


    @api.onchange('refile_ids')
    def _onchange_one2many(self):
        for line in self.refile_ids:
            line.sheet_id = self


    @api.onchange('revision_ids')
    def _onchange_one2many(self):
        for line in self.revision_ids:
            line.sheet_id = self


    @api.onchange('gluped_ids')
    def _onchange_one2many(self):
        for line in self.revision_ids:
            line.sheet_id = self


    @api.onchange('gluped2_ids')
    def _onchange_one2many(self):
        for line in self.gluped2_ids:
            line.sheet_id = self


    @api.onchange('movie_type_product_ids')
    def _onchange_one2many(self):
        for line in self.movie_type_product_ids:
            line.sheet_id = self


    """def write(self, values):
        res = super(DataSheet, self).write(values)
        self.action_create_quotation()
        return res"""

    def action_create_quotation(self):
        so_obj = self.env['sale.order']
        for record in self:
            if not record.partner_id:
                raise ValidationError("Por favor asignar un cliente")
            vals = {
                'product_id': record.product_id.id,
                'product_uom': record.uom_id.id,
                'material_id' : record.material_id.id,
                'drawn_type_id': record.drawn_type_id.id,
                'movie_type_id': record.movie_type_id.id,
                'specification_width': record.specification_width_id.id,
                'specification_long': record.specification_long_id.id,
                'caliber_id': record.caliber_id.id,
                'tongue': record.tongue,
                'thermal_adhesive': record.thermal_adhesive,
            }
            val = {
                'opportunity_id': record.opportunity_id.id if record.opportunity_id else None,
                'partner_id': record.partner_id.id,
                'origin': record.name,
                'company_id': self.company_id.id or self.env.company.id,
                'sheet_id': record.id,
                'order_line': [(0, 0, vals)],
            }
            so = so_obj.create(val)
            so.order_line.product_id_change()

    def action_sale_quotations_new(self):
        '''if not self.partner_id:
            return self.env.ref("sale_crm.crm_quotation_partner_action").read()[0]
        else:
            return self.action_new_quotation()'''
        self.action_create_quotation()

    def action_new_quotation(self):
        action = self.env.ref("sale_crm.sale_action_quotations_new").read()[0]
        vals = {
            'product_id': self.product_id.id,
            'product_uom': self.uom_id.id,
            'material_id' : self.material_id.id,
            'drawn_type_id': self.drawn_type_id.id,
            'movie_type_id': self.movie_type_id.id,
            'specification_width': self.specification_width_id.id,
            'specification_long': self.specification_long_id.id,
            'caliber_id': self.caliber_id.id,
        }
        action['context'] = {
            'search_default_opportunity_id': self.opportunity_id.id,
            'default_opportunity_id': self.opportunity_id.id,
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_origin': self.name,
            'default_company_id': self.company_id.id or self.env.company.id,
            'default_sheet_id': self.id,
            'default_order_line': [(0, 0, vals)],
        }
        return action

    def action_view_sale_quotation(self):
        action = self.env.ref('sale.action_quotations_with_onboarding').read()[0]
        action['context'] = {
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_sheet_id': self.id
        }
        action['domain'] = [('sheet_id', '=', self.id)]
        quotations = self.mapped('order_ids')
        if len(quotations) == 1:
            action['views'] = [(self.env.ref('sale.view_order_form').id, 'form')]
            action['res_id'] = quotations.id
        return action

    def action_bom_line(self):
        mrp_object = self.env['mrp.bom']
        for record in self:
            valores = []
            for line in record.line_ids:
                dic = {
                    'product_id': line.product_id.id,
                    'product_qty': line.product_qty,
                    'product_uom_id': line.uom_id.id
                }
                valores.append((0, 0, dic))
            valor = {
                'product_tmpl_id': record.product_id.id,
                'bom_line_ids': valores,
                'routing_id': record.routing_id.id,
                'sheet_id': record.id,
                'code': record.name or ''
            }
            record.bom_id = mrp_object.create(valor)
        return True


class DataProductType(models.Model):
    _name = 'data.product.type'
    _description = 'Product type'

    name = fields.Char('Name')
    code = fields.Char('Code')


class DataDrawType(models.Model):
    _name = 'data.drawn.type'
    _description = 'Drawing type'

    name = fields.Char('Name')
    code = fields.Char('Code')


class DataMovieColor(models.Model):
    _name = 'data.movie.color'
    _description = 'Movie color'

    name = fields.Char('Name')
    code = fields.Char('Code')


class DataMovieType(models.Model):
    _name = 'data.movie.type'
    _description = 'Movie type'

    name = fields.Char('Name')
    density = fields.Float('Density')
    code = fields.Char('Code')
    color_id = fields.Many2one('data.movie.color', 'Color')
    transversal = fields.Char('Transversal')
    longitudinal = fields.Char('Longitudinal')


class DataCaliberType(models.Model):
    _name = 'data.caliber.type'
    _description = 'Caliber type'

    name = fields.Float('Caliber')
    code = fields.Char('Code')
    tolerance = fields.Float('Tolerance')


class DataForm(models.Model):
    _name = 'data.form'
    _description = 'Form'

    name = fields.Char('Form')
    code = fields.Char('code')


class DataTagForm(models.Model):
    _name = 'data.tag.form'
    _description = 'Tag Form'

    name = fields.Char('Tag Form')
    code = fields.Char('code')


class DataMaterial(models.Model):
    _name = 'data.material'
    _description = 'Material'

    name = fields.Char('Material')
    code = fields.Char('code')


class DataAplication(models.Model):
    _name = 'data.application.mode'
    _description = 'Aplication Mode'

    name = fields.Char('Application Mode')
    code = fields.Char('code')


class DataAplicationPosition(models.Model):
    _name = 'data.application.position'
    _description = 'Application Position'

    name = fields.Char('Aplication Position')
    code = fields.Char('code')


class DataContents(models.Model):
    _name = 'data.application.contents'
    _description = 'Package Contents'

    name = fields.Char('Package Contents')
    code = fields.Char('code')


class PrintType(models.Model):
    _name = 'print.type'
    _description = 'Print Type'

    name = fields.Char('Print Type')
    code = fields.Char('code')


class ChemicalComposition(models.Model):
    _name = 'chemical.composition'
    _description = 'Chemical Composition'

    name = fields.Char('Chemical Composition')
    code = fields.Char('code')


class SpecificationWidth(models.Model):
    _name = 'specification.width'
    _description = 'Specification Width'

    name = fields.Float('Specification Width')
    code = fields.Char('code')
    tolerance = fields.Float('Tolerance')


class SpecificationLong(models.Model):
    _name = 'specification.long'
    _description = 'Specification Long'

    name = fields.Float('Specification Long')
    tolerance = fields.Float("Tolerance")
    code = fields.Char('code')


class WidthOverlap(models.Model):
    _name = 'width.overlap'
    _description = 'Width Overlap'

    name = fields.Float('Width Overlap')
    tolerance = fields.Char('Tolerance')
    code = fields.Char('code')


class OverlapLocation(models.Model):
    _name = 'overlap.location'
    _description = 'Overlap Location'

    name = fields.Char('Overlap Location')
    code = fields.Char('code')


class Presentation(models.Model):
    _name = 'presentation'
    _description = 'Presentation'

    name = fields.Char('Presentation')
    code = fields.Char('code')


class CoreDiameter(models.Model):
    _name = 'core.diameter'
    _description = 'Core Diameter'

    name = fields.Char('Core Diameter')
    code = fields.Char('code')


class EmbossingNumber(models.Model):
    _name = 'embossing.number'
    _description = 'Embossing Number'

    name = fields.Char('Embossing Number')
    code = fields.Char('code')


class NumberSplices(models.Model):
    _name = 'number.splices'
    _description = 'Number of splices'

    name = fields.Char('Number splices')
    code = fields.Char('code')


class SpliceType(models.Model):
    _name = 'splice.type'
    _description = 'Splice type'

    name = fields.Char('Splice type')
    code = fields.Char('code')


class SplicingTape(models.Model):
    _name = 'splicing.tape'
    _description = 'Splicing tape'

    name = fields.Char('Splicing tape')
    code = fields.Char('code')


class Seal_Type(models.Model):
    _name = 'seal.type'
    _description = 'Seal Type'

    name = fields.Char('Seal Type')
    seal = fields.Float('Seal')
    code = fields.Char('code')


class Preformed(models.Model):
    _name = 'preformed'
    _description = 'Preformed Table'

    name = fields.Char('Mold')
    bottom_diameter = fields.Float('Bottom Diameter')
    upper_diameter = fields.Float('Upper Diameter')
    tab_length = fields.Float('Tab Length')
    band_height = fields.Float('Band Height')
    product = fields.Char('Product')


class BarcodeType(models.Model):
    _name = 'barcode.type'
    _description = 'Barcode Type'

    name = fields.Char('Barcode Type')
    code = fields.Char('code')


class MechanicPlan(models.Model):
    _name = 'mechanic.plan'
    _description = 'Mechanic Plan'

    name = fields.Binary('Mechanic Plan')
    code = fields.Char('code')


class Microperforated(models.Model):
    _name = 'microperforated'
    _description = 'Microperforated'

    name = fields.Char('code')
    cross = fields.Char('Cross')
    logitudinal = fields.Char('Longitudinal')


class GraphitePresentation(models.Model):
    _name = 'drawn.presentation'
    _description = 'Drawn Presentation'

    name = fields.Char('Drawn Presentation')
    drawn_type = fields.Char('Drawn Type')
    code = fields.Char('code')


class AdhesiveType(models.Model):
    _name = 'adhesive.type'
    _description = 'Adhesive Type'

    name = fields.Char('Adhesive Type')
    code = fields.Char('code')


class ColdFoil(models.Model):
    _name = 'cold.foil'
    _description = 'Cold Foil'

    name = fields.Char('Cold Foil')
    code = fields.Char('code')


class Inks(models.Model):
    _name = 'inks'
    _description = 'Special Inks'

    name = fields.Selection([('barnizm','Barniz Mate'),('barnizt','Barniz Textura'),('plata','Plata Espejo'),('polvo','Polvo oro verdoso')],'Ink')
    percentage = fields.Selection([('5','5'),('10','10'),('20','20'),('30','30'),('40','40'),('50','50'),('80','80'),('100','100')],'Percentage')


class Designer(models.Model):
    _name = 'designer'
    _description = 'Designer'

    name = fields.Char('Designer')
    code = fields.Char('code')
    zone = fields.Char('zone')


class ColorScale(models.Model):
    _name = 'color.scale'
    _description = 'Color scale'

    name = fields.Char('Color scale/check mark')


class ControlChange(models.Model):
    _name = 'control.change'
    _description = 'Control Change'

    name = fields.Char('Change')
    date = fields.Date('Date')
    vendor = fields.Many2one('res.partner','Vendor')


class Tape(models.Model):
    _name = 'tape'
    _description = 'Tape'

    name = fields.Char('tape')
    tape_to = fields.Date('Tape to')


class Rewind(models.Model):
    _name = 'rewind'
    _description = 'Rewind'

    name = fields.Char('Rewind')


class PrintColor(models.Model):
    _name = 'print.color'
    _description = 'Print Color'

    name = fields.Many2one('product.product','Color')
    press = fields.Selection([('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8')],'U.Press')
    line = fields.Selection([('bs','BS'),('ba', 'BA'),('uv','UV')],'Line')
    lineatura = fields.Char('Lineatura')
    bcm = fields.Char('BCM')


class Repeat(models.Model):
    _name ='repeat'
    _description = 'Repeat'

    name = fields.Char('Roller')
    room_large = fields.Char('Room Large')
    large_planned = fields.Char('Large Planned')


class ForSuperlon(models.Model):
    _name = 'for.superlon'
    _description = 'For Superlon'

    name = fields.Char('For Superlon')
