# Generated by Django 5.0.4 on 2024-04-22 11:09

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import portal_360.models
import re
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyTaxAccountStatement',
            fields=[
                ('statement_id', models.AutoField(primary_key=True, serialize=False)),
                ('property_id', models.IntegerField()),
                ('due_date', models.DateField()),
                ('payment_date', models.DateField()),
                ('challan_number', models.CharField(blank=True, max_length=100, null=True)),
                ('transaction_number', models.CharField(blank=True, max_length=100, null=True)),
                ('base_value', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('floor_factor', models.DecimalField(blank=True, decimal_places=3, max_digits=5, null=True)),
                ('age_factor', models.DecimalField(blank=True, decimal_places=3, max_digits=5, null=True)),
                ('property_type_id', models.IntegerField()),
                ('property_type', models.CharField(max_length=100)),
                ('building_type_value', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('carpet_area', models.DecimalField(decimal_places=2, max_digits=10)),
                ('capital_value', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('tax_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('tax_rate_id', models.IntegerField()),
                ('property_tax', models.DecimalField(decimal_places=2, max_digits=15)),
                ('discount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('penalty_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('bill_amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=15)),
                ('pending_amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('payment_status', models.CharField(blank=True, choices=[('paid', 'Paid'), ('partial', 'Partial'), ('unpaid', 'Unpaid')], max_length=50, null=True)),
                ('payment_method', models.CharField(choices=[('cash', 'Cash'), ('debit_card', 'Debit Card'), ('online_banking', 'Online Banking'), ('cheque', 'Cheque'), ('credit_card', 'Credit Card')], max_length=20)),
            ],
            options={
                'db_table': 'property_tax_account_statement',
            },
        ),
        migrations.CreateModel(
            name='PropertyTaxActiveVerificationHistory',
            fields=[
                ('verification_id', models.AutoField(primary_key=True, serialize=False)),
                ('verification_date', models.DateTimeField()),
                ('verification_status', models.CharField(max_length=100)),
                ('verifier_name', models.CharField(max_length=100)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('notices_docs_uploaded', models.BooleanField()),
            ],
            options={
                'db_table': 'property_tax_active_vertification_history',
            },
        ),
        migrations.CreateModel(
            name='PropertyTaxApplicationForm',
            fields=[
                ('form_id', models.AutoField(primary_key=True, serialize=False)),
                ('form_number', models.CharField(max_length=100, unique=True)),
                ('form_name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'property_tax_application_form',
            },
        ),
        migrations.CreateModel(
            name='PropertyTaxConstructionType',
            fields=[
                ('construction_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('construction_type', models.CharField(choices=[('rcc', 'RCC'), ('patra_shed', 'Patra Shed'), ('load_bearing', 'Load bearing'), ('office', 'Office'), ('open_plot', 'Open Plot')], max_length=100)),
            ],
            options={
                'db_table': 'property_tax_construction_type',
            },
        ),
        migrations.CreateModel(
            name='PropertyTaxPropertySubtype',
            fields=[
                ('property_subtype_id', models.AutoField(primary_key=True, serialize=False)),
                ('property_subtype', models.CharField(choices=[('flat', 'Flat'), ('individual', 'Individual'), ('office', 'Office'), ('open_plot', 'Open Plot')], max_length=100)),
                ('property_type_id', models.IntegerField()),
                ('property_type', models.CharField(choices=[('residential', 'Residential'), ('non-residential', 'Non-Residential')], max_length=100)),
            ],
            options={
                'db_table': 'property_tax.property_tax_property_subtype',
            },
        ),
        migrations.CreateModel(
            name='PropertyTaxPropertyType',
            fields=[
                ('property_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('property_type', models.CharField(choices=[('residential', 'Residential'), ('non-residential', 'Non-Residential')], max_length=100)),
            ],
            options={
                'db_table': 'property_tax_property_type',
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(default=None, help_text='Please enter your username', max_length=150, unique=True)),
                ('department', models.TextField(blank=True, help_text='Please enter your department, if PMC employee.')),
                ('mobile_number', models.CharField(blank=True, help_text='Enter mobile number with country code', max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('aadhar_card_id', models.CharField(blank=True, default=None, max_length=12, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Aadhar card number must be 12 digits.', regex='^\\d{12}$')])),
                ('pan_card_id', models.CharField(blank=True, default=None, max_length=10, null=True, unique=True, validators=[django.core.validators.RegexValidator(message="PAN card number must be in the format: 'ABCDE1234F'.", regex='^[A-Z]{5}\\d{4}[A-Z]$')])),
                ('ration_card_id', models.CharField(blank=True, default=None, max_length=12, null=True, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), 'Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.', 'invalid')])),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default=None, max_length=10)),
                ('dob', models.DateField(default=None, help_text='Enter your date of birth.', null=True)),
                ('place_of_birth', models.CharField(default=None, help_text='Enter your place of birth.', max_length=100, null=True)),
                ('nationality', models.CharField(choices=[('', 'Select Nationality'), ('Afghan', 'Afghan'), ('Albanian', 'Albanian'), ('Algerian', 'Algerian'), ('American', 'American'), ('Andorran', 'Andorran'), ('Angolan', 'Angolan'), ('Anguillan', 'Anguillan'), ('Citizen of Antigua and Barbuda', 'Citizen of Antigua and Barbuda'), ('Argentine', 'Argentine'), ('Armenian', 'Armenian'), ('Australian', 'Australian'), ('Austrian', 'Austrian'), ('Azerbaijani', 'Azerbaijani'), ('Bahamian', 'Bahamian'), ('Bahraini', 'Bahraini'), ('Bangladeshi', 'Bangladeshi'), ('Barbadian', 'Barbadian'), ('Belarusian', 'Belarusian'), ('Belgian', 'Belgian'), ('Belizean', 'Belizean'), ('Beninese', 'Beninese'), ('Bermudian', 'Bermudian'), ('Bhutanese', 'Bhutanese'), ('Bolivian', 'Bolivian'), ('Citizen of Bosnia and Herzegovina', 'Citizen of Bosnia and Herzegovina'), ('Botswanan', 'Botswanan'), ('Brazilian', 'Brazilian'), ('British', 'British'), ('Virgin Islander', 'Virgin Islander'), ('Bruneian', 'Bruneian'), ('Bulgarian', 'Bulgarian'), ('Burkinan', 'Burkinan'), ('Burmese', 'Burmese'), ('Burundian', 'Burundian'), ('Cambodian', 'Cambodian'), ('Cameroonian', 'Cameroonian'), ('Canadian', 'Canadian'), ('Cape Verdean', 'Cape Verdean'), ('Cayman Islander', 'Cayman Islander'), ('Central African', 'Central African'), ('Chadian', 'Chadian'), ('Chilean', 'Chilean'), ('Chinese', 'Chinese'), ('Colombian', 'Colombian'), ('Comoran', 'Comoran'), ('Congolese (Congo)', 'Congolese (Congo)'), ('Congolese (DRC)', 'Congolese (DRC)'), ('Cook Islander', 'Cook Islander'), ('Costa Rican', 'Costa Rican'), ('Croatian', 'Croatian'), ('Cuban', 'Cuban'), ('Cymraes', 'Cymraes'), ('Cymro', 'Cymro'), ('Cypriot', 'Cypriot'), ('Czech', 'Czech'), ('Danish', 'Danish'), ('Djiboutian', 'Djiboutian'), ('Dominican', 'Dominican'), ('Citizen of the Dominican Republic', 'Citizen of the Dominican Republic'), ('Dutch East', 'Dutch East'), ('Timorese', 'Timorese'), ('Ecuadorean', 'Ecuadorean'), ('Egyptian', 'Egyptian'), ('Emirati', 'Emirati'), ('English', 'English'), ('Equatorial', 'Equatorial'), ('Guinean', 'Guinean'), ('Eritrean', 'Eritrean'), ('Estonian', 'Estonian'), ('Ethiopian', 'Ethiopian'), ('Faroese', 'Faroese'), ('Fijian', 'Fijian'), ('Filipino', 'Filipino'), ('Finnish', 'Finnish'), ('French', 'French'), ('Gabonese', 'Gabonese'), ('Gambian', 'Gambian'), ('Georgian', 'Georgian'), ('German', 'German'), ('Ghanaian', 'Ghanaian'), ('Gibraltarian', 'Gibraltarian'), ('Greek', 'Greek'), ('Greenlandic', 'Greenlandic'), ('Grenadian', 'Grenadian'), ('Guamanian', 'Guamanian'), ('Guatemalan', 'Guatemalan'), ('Citizen of Guinea-Bissau', 'Citizen of Guinea-Bissau'), ('Guinean', 'Guinean'), ('Guyanese', 'Guyanese'), ('Haitian', 'Haitian'), ('Honduran', 'Honduran'), ('Hong Konger', 'Hong Konger'), ('Hungarian', 'Hungarian'), ('Icelandic', 'Icelandic'), ('Indian', 'Indian'), ('Indonesian', 'Indonesian'), ('Iranian', 'Iranian'), ('Iraqi', 'Iraqi'), ('Irish', 'Irish'), ('Israeli', 'Israeli'), ('Italian', 'Italian'), ('Ivorian', 'Ivorian'), ('Jamaican', 'Jamaican'), ('Japanese', 'Japanese'), ('Jordanian', 'Jordanian'), ('Kazakh', 'Kazakh'), ('Kenyan', 'Kenyan'), ('Kittitian', 'Kittitian'), ('Citizen of Kiribati', 'Citizen of Kiribati'), ('Kosovan', 'Kosovan'), ('Kuwaiti', 'Kuwaiti'), ('Kyrgyz', 'Kyrgyz'), ('Lao Latvian', 'Lao Latvian'), ('Lebanese', 'Lebanese'), ('Liberian', 'Liberian'), ('Libyan', 'Libyan'), ('Liechtenstein citizen', 'Liechtenstein citizen'), ('Lithuanian', 'Lithuanian'), ('Luxembourger', 'Luxembourger'), ('Macanese', 'Macanese'), ('Macedonian', 'Macedonian'), ('Malagasy', 'Malagasy'), ('Malawian', 'Malawian'), ('Malaysian', 'Malaysian'), ('Maldivian', 'Maldivian'), ('Malian', 'Malian'), ('Maltese', 'Maltese'), ('Marshallese', 'Marshallese'), ('Martiniquais', 'Martiniquais'), ('Mauritanian', 'Mauritanian'), ('Mauritian', 'Mauritian'), ('Mexican', 'Mexican'), ('Micronesian', 'Micronesian'), ('Moldovan', 'Moldovan'), ('Monegasque', 'Monegasque'), ('Mongolian', 'Mongolian'), ('Montenegrin', 'Montenegrin'), ('Montserratian', 'Montserratian'), ('Moroccan', 'Moroccan'), ('Mosotho', 'Mosotho'), ('Mozambican', 'Mozambican'), ('Namibian', 'Namibian'), ('Nauruan', 'Nauruan'), ('Nepalese', 'Nepalese'), ('New Zealander', 'New Zealander'), ('Nicaraguan', 'Nicaraguan'), ('Nigerian', 'Nigerian'), ('Nigerien', 'Nigerien'), ('Niuean', 'Niuean'), ('North Korean', 'North Korean'), ('Northern Irish', 'Northern Irish'), ('Norwegian', 'Norwegian'), ('Omani', 'Omani'), ('Pakistani', 'Pakistani'), ('Palauan', 'Palauan'), ('Palestinian', 'Palestinian'), ('Panamanian', 'Panamanian'), ('Papua', 'Papua'), ('New Guinean', 'New Guinean'), ('Paraguayan', 'Paraguayan'), ('Peruvian', 'Peruvian'), ('Pitcairn Islander', 'Pitcairn Islander'), ('Polish', 'Polish'), ('Portuguese', 'Portuguese'), ('Prydeinig', 'Prydeinig'), ('Puerto Rican', 'Puerto Rican'), ('Qatari', 'Qatari'), ('Romanian', 'Romanian'), ('Russian', 'Russian'), ('Rwandan', 'Rwandan'), ('Salvadorean', 'Salvadorean'), ('Sammarinese', 'Sammarinese'), ('Samoan', 'Samoan'), ('Sao Tomean', 'Sao Tomean'), ('Saudi', 'Saudi'), ('Arabian', 'Arabian'), ('Scottish', 'Scottish'), ('Senegalese', 'Senegalese'), ('Serbian', 'Serbian'), ('Citizen of Seychelles', 'Citizen of Seychelles'), ('Sierra Leonean', 'Sierra Leonean'), ('Singaporean', 'Singaporean'), ('Slovak', 'Slovak'), ('Slovenian', 'Slovenian'), ('Solomon Islander', 'Solomon Islander'), ('Somali', 'Somali'), ('South African', 'South African'), ('South Korean', 'South Korean'), ('South Sudanese', 'South Sudanese'), ('Spanish', 'Spanish'), ('Sri Lankan', 'Sri Lankan'), ('St Helenian', 'St Helenian'), ('St Lucian', 'St Lucian'), ('Stateless', 'Stateless'), ('Sudanese', 'Sudanese'), ('Surinamese', 'Surinamese'), ('Swazi', 'Swazi'), ('Swedish', 'Swedish'), ('Swiss', 'Swiss'), ('Syrian', 'Syrian'), ('Taiwanese', 'Taiwanese'), ('Tajik', 'Tajik'), ('Tanzanian', 'Tanzanian'), ('Thai', 'Thai'), ('Togolese', 'Togolese'), ('Tongan', 'Tongan'), ('Trinidadian', 'Trinidadian'), ('Tristanian', 'Tristanian'), ('Tunisian', 'Tunisian'), ('Turkish', 'Turkish'), ('Turkmen', 'Turkmen'), ('Turks and Caicos Islander', 'Turks and Caicos Islander'), ('Tuvaluan', 'Tuvaluan'), ('Ugandan', 'Ugandan'), ('Ukrainian', 'Ukrainian'), ('Uruguayan', 'Uruguayan'), ('Uzbek', 'Uzbek'), ('Vatican citizen', 'Vatican citizen'), ('Citizen of Vanuatu', 'Citizen of Vanuatu'), ('Venezuelan', 'Venezuelan'), ('Vietnamese', 'Vietnamese'), ('Vincentian', 'Vincentian'), ('Wallisian', 'Wallisian'), ('Welsh', 'Welsh'), ('Yemeni', 'Yemeni'), ('Zambian', 'Zambian'), ('Zimbabwean', 'Zimbabwean')], default=None, help_text='Enter your nationality.', max_length=100, null=True)),
                ('address', models.TextField(default=None, help_text='Enter your address.', null=True)),
                ('government_id', models.CharField(choices=[('aadhar', 'Aadhar Card'), ('pan', 'PAN Card'), ('ration', 'Ration Card')], default=None, max_length=20, null=True)),
                ('marital_status', models.CharField(choices=[('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced'), ('widowed', 'Widowed')], default=None, max_length=15, null=True)),
                ('spouse_name', models.CharField(blank=True, default=None, help_text="Enter spouse's name if applicable.", max_length=100, null=True)),
                ('children_details', models.JSONField(blank=True, default=None, help_text="Enter children's names and ages as JSON.", null=True)),
                ('employment_type', models.CharField(default=None, help_text='Enter your employment type.', max_length=50, null=True)),
                ('occupation', models.CharField(default=None, help_text='Enter your occupation.', max_length=100, null=True)),
                ('number_of_family_members', models.IntegerField(default=0, null=True)),
                ('pin_code', models.CharField(default=None, max_length=6, null=True, validators=[django.core.validators.RegexValidator(message='Enter a valid 6-digit pin code.', regex='^\\d{6}$')])),
                ('city', models.CharField(default=None, max_length=100, null=True)),
                ('state', models.CharField(default=None, max_length=100, null=True)),
                ('latitude', models.DecimalField(decimal_places=6, default=None, max_digits=9, null=True)),
                ('longitude', models.DecimalField(decimal_places=6, default=None, max_digits=9, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'users',
            },
            managers=[
                ('objects', portal_360.models.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='PropertyTaxPropertyDetail',
            fields=[
                ('property_id', models.AutoField(primary_key=True, serialize=False)),
                ('peth_name', models.CharField(max_length=255)),
                ('peth_id', models.IntegerField()),
                ('ward_name', models.CharField(max_length=100)),
                ('ward_id', models.IntegerField()),
                ('address', models.TextField(blank=True)),
                ('pincode', models.CharField(max_length=10)),
                ('pincode_id', models.IntegerField()),
                ('year_of_occupancy', models.IntegerField()),
                ('floor_number', models.IntegerField()),
                ('construction_year', models.IntegerField()),
                ('construction_type', models.CharField(choices=[('rcc', 'RCC'), ('patra_shed', 'Patra Shed'), ('load_bearing', 'Load bearing'), ('office', 'Office'), ('open_plot', 'Open Plot')], max_length=100)),
                ('construction_type_id', models.IntegerField()),
                ('property_type', models.CharField(choices=[('residential', 'Residential'), ('non-residential', 'Non-Residential')], max_length=100)),
                ('property_type_id', models.IntegerField()),
                ('property_subtype', models.CharField(choices=[('flat', 'Flat'), ('individual', 'Individual'), ('office', 'Office'), ('open_plot', 'Open Plot')], max_length=100)),
                ('property_subtype_id', models.IntegerField()),
                ('tax_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('tax_rate_id', models.IntegerField()),
                ('length', models.DecimalField(decimal_places=2, max_digits=10)),
                ('width', models.DecimalField(decimal_places=2, max_digits=10)),
                ('carpet_area', models.DecimalField(decimal_places=2, max_digits=10)),
                ('no_of_parking_spaces', models.IntegerField()),
                ('is_parking', models.BooleanField(default=False)),
                ('is_rental', models.BooleanField(default=False)),
                ('no_of_floors', models.IntegerField()),
                ('gis_id', models.CharField(blank=True, max_length=100, null=True)),
                ('base_value', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('market_value', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_tax_property_detail', to=settings.AUTH_USER_MODEL)),
                ('verification_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_tax_verification', to='portal_360.propertytaxactiveverificationhistory')),
            ],
            options={
                'db_table': 'property_tax_property_detail',
            },
        ),
        migrations.CreateModel(
            name='PropertyTaxPropertyAddress',
            fields=[
                ('address_id', models.AutoField(primary_key=True, serialize=False)),
                ('floor_number', models.IntegerField()),
                ('flat_number', models.CharField(max_length=100)),
                ('property_name', models.CharField(max_length=255)),
                ('property_type', models.CharField(max_length=100)),
                ('landmark', models.CharField(blank=True, max_length=255, null=True)),
                ('peth_name', models.CharField(max_length=255)),
                ('ward_name', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('property_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_tax_property_address', to='portal_360.propertytaxpropertydetail')),
            ],
            options={
                'db_table': 'property_tax_property_address',
            },
        ),
        migrations.CreateModel(
            name='PropertyTaxInactiveVerificationHistory',
            fields=[
                ('verification_id', models.AutoField(primary_key=True, serialize=False)),
                ('verification_date', models.DateTimeField()),
                ('verification_status', models.CharField(max_length=100)),
                ('verifier_name', models.CharField(max_length=100)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('notices_docs_uploaded', models.BooleanField()),
                ('property_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_tax_inactive_property_vertification', to='portal_360.propertytaxpropertydetail')),
            ],
            options={
                'db_table': 'property_tax_inactive_property_vertification',
            },
        ),
        migrations.CreateModel(
            name='PropertyTaxApplicationFormHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_number', models.CharField(max_length=100)),
                ('form_type', models.CharField(max_length=100)),
                ('date_of_application', models.DateField()),
                ('status', models.CharField(max_length=100)),
                ('date_of_disposal', models.DateField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True)),
                ('notices_docs_uploaded', models.BooleanField(default=False)),
                ('property_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_tax_application_form', to='portal_360.propertytaxpropertydetail')),
            ],
            options={
                'db_table': 'property_tax_application_form_history',
            },
        ),
        migrations.AddField(
            model_name='propertytaxactiveverificationhistory',
            name='property_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_tax_property_verfiication', to='portal_360.propertytaxpropertydetail'),
        ),
        migrations.CreateModel(
            name='PropertyTaxTaxRate',
            fields=[
                ('tax_id', models.AutoField(primary_key=True, serialize=False)),
                ('tax_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('property_type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_type_tax_rates', to='portal_360.propertytaxpropertytype')),
            ],
            options={
                'db_table': 'property_tax_tax_rate',
            },
        ),
        migrations.CreateModel(
            name='WaterBillingMeter',
            fields=[
                ('meter_id', models.AutoField(primary_key=True, serialize=False)),
                ('installation_date', models.DateField()),
                ('location', models.CharField(max_length=255)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('connection_status', models.CharField(max_length=100)),
                ('meter_size', models.CharField(max_length=100)),
                ('ae_name', models.CharField(max_length=100)),
                ('je_name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meters', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'water_billing_system_meter',
            },
        ),
        migrations.CreateModel(
            name='WaterBillingBilling',
            fields=[
                ('bill_id', models.AutoField(primary_key=True, serialize=False)),
                ('bill_date', models.DateField(blank=True, null=True)),
                ('from_date', models.DateField(blank=True, null=True)),
                ('month', models.CharField(blank=True, null=True)),
                ('year', models.CharField(blank=True, null=True)),
                ('to_date', models.DateField(blank=True, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('bill_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('penalty', models.DecimalField(decimal_places=2, max_digits=7)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='water_billing_billing', to=settings.AUTH_USER_MODEL)),
                ('meter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='water_billing_meter', to='portal_360.waterbillingmeter')),
            ],
            options={
                'db_table': 'water_billing_system_billing',
            },
        ),
        migrations.CreateModel(
            name='WaterBillingMeterService',
            fields=[
                ('service_id', models.AutoField(primary_key=True, serialize=False)),
                ('service_date', models.DateField()),
                ('service_type', models.CharField(choices=[('installation', 'Installation'), ('repair', 'Repair'), ('maintenance', 'Maintenance')], max_length=20)),
                ('service_details', models.TextField()),
                ('service_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('completed', 'Completed'), ('ongoing', 'On-Going')])),
                ('meter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='water_billing_service', to='portal_360.waterbillingmeter')),
            ],
            options={
                'db_table': 'water_billing_system_meter_service',
            },
        ),
        migrations.CreateModel(
            name='WaterBillingPayment',
            fields=[
                ('payment_id', models.AutoField(primary_key=True, serialize=False)),
                ('payment_date', models.DateField()),
                ('trans_id', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(choices=[('cash', 'Cash'), ('debit_card', 'Debit Card'), ('online_banking', 'Online Banking'), ('cheque', 'Cheque'), ('credit_card', 'Credit Card')], max_length=20)),
                ('payment_status', models.CharField(choices=[('paid', 'paid'), ('unpaid', 'Unpaid')], max_length=20)),
                ('remarks', models.TextField()),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='water_billing_payment', to='portal_360.waterbillingbilling')),
            ],
            options={
                'db_table': 'water_billing_system_payment',
            },
        ),
        migrations.CreateModel(
            name='WaterBillingReading',
            fields=[
                ('reading_id', models.AutoField(primary_key=True, serialize=False)),
                ('reading_date', models.DateField()),
                ('reading_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('reader_name', models.CharField(max_length=100)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('meter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='water_billing_readings', to='portal_360.waterbillingmeter')),
            ],
            options={
                'db_table': 'water_billing_system_meter_reading',
            },
        ),
        migrations.CreateModel(
            name='ApplicationUsage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application_name', models.CharField(max_length=255)),
                ('usage_count', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'application_name')},
            },
        ),
    ]
