{
    'name': 'Optimo',
    'author': 'OPTESIS SA',
    'version': '2.0.0',
    'category': 'Asset',
    'description': """
Ce module permet de faire l'inventaire des immobilisations de votre entreprise d'une manière structurée, fiable et intuitive
""",
    'summary': 'Module d\'inventaire ',
    'sequence': 9,
    'depends': ['base','account_asset','product', 'account',
    ],
    'data': [
      'security/security.xml',
      'security/ir.model.access.csv',
      'views/optesis_views.xml',
      'views/employee.xml',
      'views/site.xml',
      'views/direction.xml',
      'views/document.xml',
      'views/optesis.xml',
      'views/transfert.xml',
      'views/res_config_settings_views.xml',
      'security/multi_company_view.xml',
      'views/sequence_control.xml',
      'views/sequence_transfert.xml',

    ],
    'test': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
