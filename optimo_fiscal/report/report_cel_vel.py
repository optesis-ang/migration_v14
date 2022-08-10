import xlwt
from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)

class OptimoFiscalAnnexeXlsx(models.AbstractModel):
    _name = 'report.optimo_fiscal.report_cel_vel'
    _inherit = 'report.report_xlsx.abstract'
    #_inherit = ['report.report_xlsx.abstract', 'report.etat_financiers.tft_xls']
    

    
    file_name = fields.Binary('ANNEXE CEL VL', readonly=True)
    
    def generate_xlsx_report(self, workbook, data, line):
        
       
        format1 = workbook.add_format({
    'bold':     True,
    #'border':   4,
    'align':    'center',
    'valign':   'vcenter',
    
    'font_size': '9',
})
        format2 = workbook.add_format({
        'bold':     True,
        #'border':   4,
        'align':    'center',
        'valign':   'vcenter',

        'font_size': '17',
    })
        format3 = workbook.add_format({
        'bold':     True,
        #'border':   4,
        'align':    'left',
        'valign':   'vcenter',

        'font_size': '9',
    })
        format1.set_font_name('Calibri')
        format1.set_border(2)
        format3.set_font_name('Calibri')
        format3.set_border(2)
        format1.set_top(2)
        format1.set_text_wrap()
        format3.set_text_wrap()
        
           
        sheet = workbook.add_worksheet('ANNEXE CEL VL')


        sheet.set_column('A:B',15)
        sheet.merge_range('A1:AA1', 'ANNEXE CEL VL',format2)
        sheet.merge_range('A2:B4', 'Adresse exacte de l\'immeuble',format1)
        sheet.merge_range('C2:D4', 'N° NICAD',format1)
        sheet.merge_range('E2:F4', 'Commune de situation',format1)
        #sheet.set_column('F:AA',100)
        sheet.merge_range('G2:H4', 'Valeur brute des terrains inscrits  à l\'actif du bilan ',format1)
        sheet.merge_range('I2:J4', 'Valeur brute des constructions inscrites  à l\'actif du bilan  ',format1)
        sheet.merge_range('K2:L4', 'Valeur brute des agencements et installations imposables inscrites à l\'actif du bilan ',format1)
        sheet.merge_range('M2:N4', 'Valeur brute total des terrains constructions agencements et installations',format1)

        sheet.merge_range('O2:P4', 'Valeur locative totale des locaux inscrits au bilan (colonne 7 x7%)',format1)
        sheet.merge_range('Q2:R4', 'Loyer versé par l\'exploitant locataire ',format1)
        sheet.merge_range('S2:T4', 'Loyer estimé pour les locaux occupés à titre gratuit',format1)
        sheet.merge_range('U2:V4', 'Loyer perçu par le loueur professionnel',format1)
        sheet.merge_range('W2:X4', 'CEL propriétaire (colonne 8 x20%)',format1)
        sheet.merge_range('Y2:Z4', 'CEL loueur professionnel (colonne 11 x20%)',format1)
        sheet.merge_range('AA2:AB4', 'CEL locataire (colonne 9 +10 70)  x15%',format1)
        sheet.merge_range('AC2:AD4', 'CEL Totale (colonne 12+13+14)',format1)
        sheet.merge_range('A5:B5', '1',format1)
        sheet.merge_range('C5:D5', '2',format1)
        sheet.merge_range('E5:F5', '3',format1)
        #sheet.set_column('F:AA',100)
        sheet.merge_range('G5:H5', '4',format1)
        sheet.merge_range('I5:J5', '5 ',format1)
        sheet.merge_range('K5:L5', '6',format1)
        sheet.merge_range('M5:N5', '7',format1)
        sheet.merge_range('O5:P5', '8 ',format1)
        sheet.merge_range('Q5:R5', '9',format1)
        sheet.merge_range('S5:T5', '10',format1)
        sheet.merge_range('U5:V5', '11',format1)
        sheet.merge_range('W5:X5', '15',format1)
        sheet.merge_range('Y5:Z5', '13',format1)
        sheet.merge_range('AA5:AB5', '14',format1)
        sheet.merge_range('AC5:AD5', '15',format1)

        row1 = 5
        row2 = 5
        num_set = []
        for lines in line:
             num_set.append(lines.commune)
        table_commune = set(num_set)
        valeur_brute_terrainT = 0
        valeur_brute_constructionT = 0
        valeur_brute_actifT = 0
        valeur_brute_agenceT = 0
        valeur_brute_loyerT = 0
        valeur_brute_elseT = 0
        for val in table_commune:
            valeur_brute_terrain = 0
            valeur_brute_construction = 0
            valeur_brute_actif = 0
            valeur_brute_agence = 0
            valeur_brute_loyer = 0
            valeur_brute_else = 0
            address = ""
            nnicad = ""
            for lines in line:
                 if val == lines.commune:
                    adress = lines.address
                    nnicad = lines.nnicad
                    if lines.num_compte[:-3] =='222':
                        valeur_brute_terrain = valeur_brute_terrain + lines.valeur_brute
                        valeur_brute_terrainT = valeur_brute_terrainT + lines.valeur_brute
                    elif lines.num_compte[:-3] =='231':
                        valeur_brute_construction = valeur_brute_construction + lines.valeur_brute
                        valeur_brute_constructionT = valeur_brute_constructionT + lines.valeur_brute
                    elif lines.num_compte[:-3] =='238':
                        valeur_brute_actif = valeur_brute_actif + lines.valeur_brute
                        valeur_brute_actifT = valeur_brute_actifT + lines.valeur_brute
                    elif lines.num_compte[:-3] =='223':
                        valeur_brute_agence = valeur_brute_agence + lines.valeur_brute
                        valeur_brute_agenceT = valeur_brute_agenceT + lines.valeur_brute
                        
                    elif lines.num_compte[:-3] =='622':
                        valeur_brute_loyer = valeur_brute_loyer + lines.valeur_brute
                        valeur_brute_loyerT = valeur_brute_loyerT + lines.valeur_brute

                        
                    else:
                        valeur_brute_else = valeur_brute_else + lines.valeur_brute
                        valeur_brute_elseT = valeur_brute_elseT + lines.valeur_brute

                        
                   
            sheet.merge_range(row1,0,row2,1,address, format3)
            sheet.merge_range(row1,2,row2,3,nnicad, format3)
            sheet.merge_range(row1,4,row2,5,val, format3)
            sheet.merge_range(row1,6,row2,7,valeur_brute_terrain, format3)
            sheet.merge_range(row1,8,row2,9,valeur_brute_construction, format3)
            sheet.merge_range(row1,10,row2,11,valeur_brute_actif, format3)
            sheet.merge_range(row1,12,row2,13,valeur_brute_agence, format3)
            sheet.merge_range(row1,14,row2,15,valeur_brute_loyer, format3)
            sheet.merge_range(row1,16,row2,17,valeur_brute_else, format3)
            sheet.merge_range(row1,18,row2,19,valeur_brute_else, format3)
            sheet.merge_range(row1,20,row2,21,valeur_brute_else, format3)
            sheet.merge_range(row1,22,row2,23,valeur_brute_else, format3)
            sheet.merge_range(row1,24,row2,25,valeur_brute_else, format3)
            sheet.merge_range(row1,26,row2,27,valeur_brute_else, format3)
            sheet.merge_range(row1,28,row2,29,valeur_brute_terrain, format3)
            row1+=1
            row2+=1

        sheet.merge_range(row1,0,row2,1,'Totaux', format3)
        sheet.merge_range(row1,2,row2,3,'', format3)
        sheet.merge_range(row1,4,row2,5,'', format3)
        sheet.merge_range(row1,6,row2,7,'', format3)
        sheet.merge_range(row1,8,row2,9,'', format3)
        sheet.merge_range(row1,10,row2,11,'', format3)
        sheet.merge_range(row1,12,row2,13,'', format3)
        sheet.merge_range(row1,14,row2,15,'', format3)
        sheet.merge_range(row1,16,row2,17,'', format3)
        sheet.merge_range(row1,18,row2,19,'', format3)
        sheet.merge_range(row1,20,row2,21,'', format3)
        sheet.merge_range(row1,22,row2,23,'', format3)
        sheet.merge_range(row1,24,row2,25,'', format3)
        sheet.merge_range(row1,26,row2,27,'', format3)
        sheet.merge_range(row1,28,row2,29,'', format3)



            

                    