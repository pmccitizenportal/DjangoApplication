from django import template

register = template.Library()

@register.filter(name='static_image_url')
def static_image_url(app_name):
    app_images = {
        'Property Tax': '/static/images/property_tax.png',
        'Water Billing System': '/static/images/water_billing_system.png',
        'Participatory Budget': '/static/images/participatory_budget.png',
        'Complaint Management System': '/static/images/complaint_management_system.png',
        'Legal Department': '/static/images/legal_department.png',
        'Shahari Garib Yojana': '/static/images/sgy.png',
        'Local Body Tax': '/static/images/lbt.png',
        'Slum Department Billing': '/static/images/slum.png',
        'Hawkers Management System': '/static/images/hawkers.png',
        'Building Permission': '/static/images/building_permit.png',
        'Geographic Information System': '/static/images/gis.png',
        'Chatbot': '/static/images/chatbot.png',
    }
    return app_images.get(app_name, '/static/images/chatbot.png')

@register.filter(name='application_url')
def application_url(app_name):
    # app_images = {
    #     'Property Tax': 'property_tax',
    #     'Water Billing System': 'water_billing_system',
    #     'Participatory Budget': 'participatory_budget',
    #     'Complaint Management System': 'complaint_management_system',
    #     'Legal Department': 'legal_department',
    #     'Shahari Garib Yojana': 'shahari_garib_yojana',
    #     'Local Body Tax': 'local_body_tax',
    #     'Slum Department Billing': 'slum_department_billing',
    #     'Hawkers Management System': 'hawkers_management_system',
    #     'Building Permission': 'building_permission',
    #     'Geographic Information System': 'geographic_information_system',
    #     'Chatbot': 'chatbot',
    # }
    app_images = {
        'Property Tax': 'water_billing_system',
        'Water Billing System': 'water_billing_system',
        'Participatory Budget': 'water_billing_system',
        'Complaint Management System': 'water_billing_system',
        'Legal Department': 'water_billing_system',
        'Shahari Garib Yojana': 'water_billing_system',
        'Local Body Tax': 'water_billing_system',
        'Slum Department Billing': 'water_billing_system',
        'Hawkers Management System': 'water_billing_system',
        'Building Permission': 'water_billing_system',
        'Geographic Information System': 'water_billing_system',
        'Chatbot': 'water_billing_system',
    }
    return app_images.get(app_name, 'home')