# -*- coding: utf-8 -*-
from odoo import models, fields, api
# from odoo.addons.eastlog_import.models.eastlog_ie_user_model_dict import  gen_model_dict


def gen_model_dict():
    user_model_dict = {
        u'eastlog_user': {
        'title_rows' : [0], 
#         'begin_data_row_offset_with_title_row' :2,
        'sheet_names':lambda self,wb: [wb.sheet_names()[0]],
        'model':'res.users',
        'context':{'no_reset_password':True},
        'fields' : [
                ('login',{'func':None,'xl_title':u'login','key':True ,'required':True}),
                ('name', {'func':None, 'xl_title':u'name','key':True,'required':True}),
#                 ('birth_day',{'func':birth_day_,'xl_title':u'ngày sinh', 'offset_write_xl_diff':4,}),
                ('password_crypt',{'required':True, 'xl_title':u'password_crypt'}),
                ('partner_id',{'key':False,'required':True, 'xl_title':'partner_id', 'func': lambda v,n,s:int(v)}),
#                 ('lang',{'set_val':'vi_VN'}),
#                 ('phone',{'func':None,'xl_title':u'Số điện thoại','key':False, 'offset_write_xl_diff':1}),
#                 ('cac_sep_ids',{'key':False,'required':False,'allow_create':False,
#                                         'fields':[
#                                                  ('login',{'xl_title':u'Cấp trên',  'key':True, 'required':True, 'st_is_x2m_field':True}),
#                                                  ]
#                 }),  
#                 ('groups_id',{'key':False,
#                                     'offset_write_xl_diff':2,
#                                     'offset_write_xl':3,
#                                     'required':False ,
#                                     'remove_all_or_just_add_one_x2m': 'add_one',
#                                     'fields':[
#                                              ('name',{'xl_title':u'groups_id',  'key':True, 'required': True,'st_is_x2m_field':True}),     
#                                               ]
#                                     }
#                  ),  
#                  ('job_id',{'key':False,'required':False,
#                                    'fields':[
#                                                 ('name',{'xl_title':u'Chức vụ',  'key':True, 'required':True, 'func':lambda v,n: u'Nhân viên' if v==False else v }),
#                                                ]
#                 }),  
#                 ('department_id',{'key':False,'required':True,'raise_if_False':True,
#                                            'fields':[
#                                                     ('name',{'xl_title':u'Bộ Phận',  'key':True, 'required': True}),
#                                                     ]
#                                                  }),  
#                 ('partner_id',{'key':False,'required':False,
#                                'fields':[
#                                 ('name',{'xl_title':None,  'key':True, 'required': True, 'func':lambda val,needdata: needdata['vof_dict']['name']['val']}),
#                                 ('email',{'xl_title':None,  'key':True, 'required': True, 'func':lambda val,needdata: needdata['vof_dict']['login']['val']}),
# #                                 ('department_id',{'xl_title':None,  'key':False, 'required': True, 'func':lambda val,needdata: needdata['vof_dict']['department_id']['val']}),
# #                                 ('parent_id',{'key':False,'required':False,
# #                                             'fields':[
# #                                                      ('name',{'xl_title':None,  'key':True, 'required': True, 'func':lambda val,needdata: needdata['vof_dict']['department_id']['fields']['name']['val'] }),
# #                                                        
# #                                                      ]
# #                                 }),  
#                                               
#                                         ]
#                                     }
#                  ),  
                      ]
                },#End users'
  
  
  
  
        
        
        }
    return user_model_dict
class ImportExcel(models.Model):
    _inherit = 'importexcel.importexcel' 
    import_key = fields.Selection(selection_add=[('eastlog_user', 'eastlog_user')])
    def gen_model_dict(self):
        rs = super(ImportExcel, self).gen_model_dict()
        rs.update(gen_model_dict())

        return rs