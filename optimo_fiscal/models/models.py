# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)

class OptesisAsset(models.Model):
    _inherit = "optesis.asset.asset"
    _description = "optesis asset inherit"

   
    is_taxable = fields.Boolean(string="Taxable",compute='_compute_famille',store=True)
    num_compte = fields.Char(string='Compte', related='family_id.num_compte')
    propriete = fields.Boolean(string="Propriété")
    tax_ok = fields.Integer("Cocher",compute='_compute_famille',store=True)
    base_taxable = fields.Float(string='Base Taxable',compute="_compute_calculate_base",store=True)
    cel_vel = fields.Float(string='CEL VEL',compute="_compute_calculate_base",store=True)
    taux_cel_vel = fields.Float("Taux Cel VL",compute='_compute_calculate_base')
    commune = fields.Many2one(comodel_name="optesis.commune", string="Commune",related="site.commune_id")

       
    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('optesis.asset.asset') or '/'
        vals['asset_number'] = seq
        vals['name'] = vals['code_bar'] or "/"
        res = super(OptesisAsset, self).create(vals)
        if res.is_taxable == True: 
            _logger.info('test anta res yes we can %s',res.site.address)

            self.env['optesis.etat.cel'].create({
                'asset_id':res.id,
                'num_compte':res.num_compte,
                'product_id':res.product_id.name,
                'category_id':res.family_id.name,
                'valeur_brute':res.value,
                'is_taxable': res.is_taxable,
                'base_taxable':res.base_taxable,
                'propriete':res.propriete,
                'cel_vel':res.cel_vel,
                'commune':res.commune.name,
                'taux_cel_vel':res.taux_cel_vel,
                'site':res.site,
                'address':res.site.address,
                'nnicad':res.site.description,
            })
        return res
    
    @api.multi
    def write(self,values):
        # your logic goes here
        override_write = super(OptesisAsset,self).write(values)
        if override_write:                                  
            resultat = self.env['optesis.etat.cel'].search([('asset_id.id', '=', self.id)], limit=1)
            _logger.info('test anta res yes we can %s',resultat.base_taxable) 
            if self.id == resultat.asset_id.id:
                _logger.info('test anta res yes we can %s',resultat.base_taxable)
                _logger.info('test anta res yes we can %s',resultat.asset_id.id)
                _logger.info('Never giv up %s',self.value)
                for record in resultat:
                    record.write({
                        'asset_id':self.id,
                        'num_compte':self.num_compte,
                        'product_id':self.product_id.name,
                        'category_id':self.family_id.name,
                        'valeur_brute':self.value,
                        'is_taxable': self.is_taxable,
                        'base_taxable':self.base_taxable,
                        'propriete':self.propriete,
                        'cel_vel':self.cel_vel,
                        'commune':self.commune.name,
                        'taux_cel_vel':self.taux_cel_vel,

                    })     
        return override_write

    

    
    
   
    
  
    
    
    
    @api.one
    @api.depends("family_id")
    #@api.onchange("category_id")
    def _compute_famille(self):
        fam = self.env["optesis.family"].browse(self.family_id.id)
      
        for rec in self.family_id:
            if rec.num_compte.startswith('22') or rec.num_compte.startswith('23'):
                _logger.info('valeur Numcompte %s',rec.num_compte)
                self.base_taxable = 0.07 * self.value
                self.tax_ok = 1
                self.is_taxable = True
            else:
                #_logger.info('you have a mistake')
                self.tax_ok = 0
           
    @api.one   
    @api.depends("value","tax_ok")           
    #@api.onchange('value')
    def _compute_calculate_base(self):
        if self.value and self.tax_ok == 1:
            self.base_taxable = 0.07 * self.value
            self.taux_cel_vel = 7

            if self.propriete == False:
                self.cel_vel = 0.15 * self.base_taxable
                self.taux_cel_vel = 15
            else:
                self.cel_vel = 0.2 * self.base_taxable
                self.taux_cel_vel = 20
    
    @api.depends("is_taxable")
    @api.onchange('is_taxable')
    def celNull(self):
        if self.is_taxable == False:
            self.base_taxable = 0
            self.cel_vel = 0
        else:
            if self.propriete == False:
                self.cel_vel = 0.15 * self.base_taxable
                self.taux_cel_vel = 15
            else:
                self.cel_vel = 0.2 * self.base_taxable
                self.taux_cel_vel = 20
            
    
    
    @api.depends("value","tax_ok","propriete")      
    #@api.onchange('propriete')
    def _computeCalculateCelVel(self):
        if self.propriete:
            if self.is_taxable:
                self.cel_vel = 0.2 * self.base_taxable
            else:
                self.base_taxable = 0
                self.cel_vel = 0
        else:
             if self.is_taxable:
                self.cel_vel = 0.15 * self.base_taxable
            
class EtatCel(models.Model):
    _name = "optesis.etat.cel"
    #_inherit ='optesis.asset.asset'
    _description = "Etat Cel VL"    
    asset_id = fields.Many2one('optesis.asset.asset',ondelete="cascade")
    autres_id = fields.Many2one('optesis.autres',ondelete="cascade")
    product_id = fields.Char(string="Standard")
    num_compte = fields.Char('Numero de compte',)
    valeur_brute = fields.Float(string="Valeur Brute")
    category_id = fields.Char(string="Famille")
    is_taxable = fields.Boolean('Taxable')
    base_taxable = fields.Float(string='Base Taxable')
    propriete = fields.Boolean(string="Propriété")
    cel_vel = fields.Float(string='CEL VEL')
    site = fields.Many2one(comodel_name="optesis.site",)
    address = fields.Char(String="Addresse")
    nnicad = fields.Char(String="N° NICAD")
    taux_cel_vel = fields.Float("Taux Cel VL")

    commune = fields.Char(string="Commune")
    
    

    

    
    
class OptesisAutres(models.Model):
    _name = "optesis.autres"
    _description = "optesis autres locations/mise en disposition"

    name = fields.Char(string='Bailleurs')
    product_id = fields.Many2one(comodel_name="optesis.product", string="Standard")
    
    site = fields.Many2one(comodel_name="optesis.site", string="Site")
    commune = fields.Many2one(comodel_name="optesis.commune", string="Commune",related="site.commune_id")
    building = fields.Many2one(comodel_name="optesis.building", string="Bâtiment")
    level = fields.Many2one(comodel_name="optesis.level", string="Niveau")
    date_debut = fields.Date(string="Date debut")
   
    valeur_mensuelle = fields.Float("Valeur Locative")
    valeur_anuelle = fields.Float("Base taxable")
    taux_cel_vel = fields.Integer("Taux Cel VL")
    date_end = fields.Date(string="Date de Fin")
    cel_vl = fields.Integer("CEL VL")
    
    duree_in_months = fields.Float('Duree')
    company_id = fields.Many2one('res.company', 'Company', copy=False, readonly=True,
                                 default=lambda self: self.env.user.company_id)
    @api.model
    def create(self, vals):
        # Here you can do any code that effect before createion of tax record
        res = super(OptesisAutres, self).create(vals)
        self.env['optesis.etat.cel'].create({
                'autres_id':res.id,
                'num_compte':res.product_id.category_id.num_compte,
                'product_id':res.product_id.name,
                'category_id':res.product_id.category_id.name,
                'valeur_brute':res.valeur_mensuelle,
                'is_taxable': True,
                'base_taxable':res.valeur_anuelle,
                'propriete':False,
                'taux_cel_vel':res.taux_cel_vel,
                'cel_vel':res.cel_vl,
                'commune':res.commune.name,
                
          
                
            })
        return res
    
    @api.multi
    def write(self,values):
        # your logic goes here
        override_write = super(OptesisAutres,self).write(values)
        if override_write:                                  
            resultat = self.env['optesis.etat.cel'].search([('autres_id.id', '=', self.id)], limit=1)
            _logger.info('test anta res yes we can %s',resultat.base_taxable) 
            if self.id == resultat.autres_id.id:
                #_logger.info('test anta res yes we can %s',resultat.base_taxable)
                #_logger.info('test anta res yes we can %s',resultat.asset_id.id)
                #_logger.info('Never giv up %s',self.value)
                for record in resultat:
                    record.write({
                        'autres_id':self.id,
                        'num_compte':self.product_id.category_id.num_compte,
                        'product_id':self.product_id.name,
                        'category_id':self.product_id.category_id.name,
                        'valeur_brute':self.valeur_mensuelle,
                        'is_taxable': True,
                        'base_taxable':self.valeur_anuelle,
                        'propriete':False,
                        'taux_cel_vel':self.taux_cel_vel,
                        'cel_vel':self.cel_vl,
                        'commune':self.commune.name,
                

                    })     
        return override_write

    #asset_id = fields.Many2one('optesis.asset.asset', 'Immo')
    #this function is to calculate the month duration
    @api.onchange("date_debut","date_end")
    def duree_locations(self):
        fmt = '%Y-%m-%d'
        if self.date_debut and self.date_end:
        
            daysDiff = str((self.date_end.month)-(self.date_debut.month))
            self.duree_in_months = float(daysDiff) + 1

       
            
    @api.onchange("valeur_mensuelle","duree_in_months")
    def valeurAnnuelle(self):
        if self.valeur_mensuelle and self.duree_in_months:
            self.valeur_anuelle = self.valeur_mensuelle * self.duree_in_months
            self.taux_cel_vel = 15
            
    @api.onchange("valeur_mensuelle")
    def valeurCelvl(self):
        if self.valeur_mensuelle:
            self.cel_vl = self.valeur_anuelle * (self.taux_cel_vel/100)