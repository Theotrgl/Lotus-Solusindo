# Generated by Django 5.0.3 on 2024-04-03 16:05


import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import django_measurement.models
import djmoney.models.fields
import djmoney.models.validators
import measurement.measures.mass
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('cust_id', models.AutoField(primary_key=True, serialize=False)),
                ('nama_pt', models.CharField(max_length=255)),
                ('telp', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('terms_of_payment', models.CharField(max_length=15)),
                ('pengiriman', models.CharField(max_length=50)),
                ('npwp', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Kecamatan',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Kecamatan',
                'verbose_name_plural': 'Kecamatan',
            },
        ),
        migrations.CreateModel(
            name='Kota',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Kota/Kabupaten',
                'verbose_name_plural': 'Kota/Kabupaten',
            },
        ),
        migrations.CreateModel(
            name='LogBook',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('instansi_asal', models.CharField(max_length=255, null=True)),
                ('nama', models.CharField(max_length=50, null=True)),
                ('email', models.EmailField(max_length=100)),
                ('tujuan', models.CharField(choices=[('meeting', 'Meeting'), ('survey', 'Survey'), ('interview', 'Interview'), ('lainnya', 'Lainnya')], max_length=20, null=True)),
                ('tujuan_lainnya', models.CharField(blank=True, max_length=200, null=True)),
                ('nama_dikunjungi', models.CharField(max_length=50, null=True)),
                ('tipe', models.CharField(choices=[('unscheduled', 'Unscheduled'), ('scheduled', 'Scheduled')], max_length=15)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('telp', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
            ],
            options={
                'verbose_name': 'Log Book',
                'verbose_name_plural': 'Log Books',
            },
        ),
        migrations.CreateModel(
            name='Messenger',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('color', models.CharField(default='#3a87ad', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Provinsi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Provinsi',
                'verbose_name_plural': 'Provinsi',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('supp_id', models.AutoField(primary_key=True, serialize=False)),
                ('nama_pt', models.CharField(max_length=255)),
                ('telp', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('terms_of_payment', models.CharField(max_length=50)),
                ('pengiriman', models.CharField(max_length=50, null=True)),
                ('npwp', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerPIC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('telp', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('Role', models.CharField(max_length=50)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.customer')),
            ],
            options={
                'verbose_name': 'Customer PIC',
                'verbose_name_plural': 'Customer PICs',
            },
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('SKU', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('upload_type', models.CharField(default='manual', max_length=10)),
                ('Tanggal', models.DateField(default=django.utils.timezone.now)),
                ('tanggal_pemesanan', models.DateField(default=django.utils.timezone.now, null=True)),
                ('nama', models.CharField(max_length=255)),
                ('catatan', models.CharField(max_length=500, null=True)),
                ('quantity', models.IntegerField()),
                ('unit', models.CharField(max_length=10)),
                ('price_currency', djmoney.models.fields.CurrencyField(choices=[('CNY', 'Chinese Yuan (CNY)'), ('IDR', 'Indonesian Rupiah (IDR)'), ('TWD', 'New Taiwan Dollar (TWD)'), ('SGD', 'Singapore Dollar (SGD)'), ('USD', 'US Dollar (USD)')], default='IDR', editable=False, max_length=3)),
                ('price', djmoney.models.fields.MoneyField(decimal_places=2, default_currency='IDR', max_digits=15, validators=[djmoney.models.validators.MinMoneyValidator(0)])),
                ('gambar', models.ImageField(max_length=500, upload_to='')),
                ('is_approved', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.category')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='page1.customer')),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
            },
        ),
        migrations.CreateModel(
            name='ItemChangeLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('field_changed', models.CharField(max_length=100)),
                ('old_value', models.TextField(blank=True, null=True)),
                ('new_value', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.items')),
            ],
        ),
        migrations.CreateModel(
            name='ItemSumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jenis_sumber', models.CharField(choices=[('Online Store', 'Online Store'), ('Rabrik', 'Pabrik'), ('Reseller', 'Reseller'), ('Grosir', 'Grosir')], max_length=30)),
                ('nama_perusahaan', models.CharField(max_length=255)),
                ('telp', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.items')),
            ],
            options={
                'verbose_name': 'Item Sumber',
                'verbose_name_plural': 'Items Sources',
            },
        ),
        migrations.CreateModel(
            name='Kelurahan',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('kecamatan_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.kecamatan')),
            ],
            options={
                'verbose_name': 'Kelurahan/Desa',
                'verbose_name_plural': 'Kelurahan/Desa',
            },
        ),
        migrations.AddField(
            model_name='kecamatan',
            name='kota_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.kota'),
        ),
        migrations.CreateModel(
            name='DeliveryAddresses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', models.CharField(max_length=500)),
                ('kecamatan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.kecamatan')),
                ('kelurahan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.kelurahan')),
                ('kota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.kota')),
                ('provinsi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.provinsi')),
            ],
            options={
                'verbose_name': 'Delivery Address',
                'verbose_name_plural': 'Delivery Addresses',
            },
        ),
        migrations.AddField(
            model_name='kota',
            name='provinsi_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.provinsi'),
        ),
        migrations.CreateModel(
            name='CustomerAlamat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('penagihan', 'Alamat Penagihan'), ('pengiriman', 'Alamat Pengiriman')], max_length=15)),
                ('detail', models.CharField(max_length=500)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.customer')),
                ('kecamatan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.kecamatan')),
                ('kelurahan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.kelurahan')),
                ('kota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.kota')),
                ('provinsi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.provinsi')),
            ],
            options={
                'verbose_name': 'Customer Address',
                'verbose_name_plural': 'Customer Addresses',
            },
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revenue_PO_currency', djmoney.models.fields.CurrencyField(choices=[('CNY', 'Chinese Yuan (CNY)'), ('IDR', 'Indonesian Rupiah (IDR)'), ('TWD', 'New Taiwan Dollar (TWD)'), ('SGD', 'Singapore Dollar (SGD)'), ('USD', 'US Dollar (USD)')], default='IDR', editable=False, max_length=3, null=True)),
                ('revenue_PO', djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default_currency='IDR', max_digits=15, null=True, validators=[djmoney.models.validators.MinMoneyValidator(0)])),
                ('nomor_PO', models.IntegerField(blank=True, null=True)),
                ('tanggal_PO', models.DateField(blank=True, null=True)),
                ('tanggal_process', models.DateField(blank=True, null=True)),
                ('tanggal_input_accurate', models.DateField(blank=True, null=True)),
                ('tanggal_pengiriman_barang', models.DateField(blank=True, null=True)),
                ('tanggal_pengiriman_invoice', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('order', 'Order Created'), ('pending', 'Pending'), ('process', 'Process'), ('accurate', 'Accurate'), ('pengiriman', 'Pengiriman Barang'), ('invoice', 'Pengiriman Invoice'), ('complete', 'Completed')], max_length=30)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.items')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.supplier')),
            ],
            options={
                'verbose_name': 'Purchase Order',
                'verbose_name_plural': 'Purchase Orders',
            },
        ),
        migrations.CreateModel(
            name='SupplierAlamat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('penagihan', 'Alamat Penagihan'), ('pengiriman', 'Alamat Pengiriman')], max_length=15)),
                ('detail', models.CharField(max_length=500)),
                ('kecamatan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.kecamatan')),
                ('kelurahan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.kelurahan')),
                ('kota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.kota')),
                ('provinsi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.provinsi')),
                ('supplier_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.supplier')),
            ],
            options={
                'verbose_name': 'Supplier Address',
                'verbose_name_plural': 'Supplier Addresses',
            },
        ),
        migrations.CreateModel(
            name='SupplierPIC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('telp', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('Role', models.CharField(max_length=50)),
                ('supplier_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.supplier')),
            ],
            options={
                'verbose_name': 'Supplier PIC',
                'verbose_name_plural': 'Supplier PICs',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('groups', models.ManyToManyField(blank=True, related_name='custom_user_set', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='custom_user_set', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserActionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=255)),
                ('payload', models.TextField(blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Action Log',
                'verbose_name_plural': 'User Action Logs',
            },
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('model', models.CharField(max_length=100)),
                ('jenis', models.CharField(choices=[('truck', 'Truck'), ('mobil', 'Mobil'), ('motor', 'Motor'), ('ojek_online', 'Ojek Online')], max_length=20)),
                ('nomor_plat', models.CharField(max_length=11)),
                ('messenger', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vehicles', to='page1.messenger')),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=30, null=True)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('keterangan', models.CharField(max_length=500, null=True)),
                ('package_name', models.CharField(max_length=100, null=True)),
                ('package_dimensions', models.CharField(max_length=100, null=True)),
                ('package_mass', django_measurement.models.MeasurementField(measurement=measurement.measures.mass.Mass, null=True)),
                ('destination', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='delivery_destination', to='page1.deliveryaddresses')),
                ('start_location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='delivery_start_location', to='page1.deliveryaddresses')),
                ('messenger', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='page1.messenger')),
                ('vehicle', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='page1.vehicle')),
            ],
            options={
                'verbose_name': 'Delivery Order',
                'verbose_name_plural': 'Delivery Orders',
            },
        ),
        migrations.CreateModel(
            name='WorkOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revenue_PO_currency', djmoney.models.fields.CurrencyField(choices=[('CNY', 'Chinese Yuan (CNY)'), ('IDR', 'Indonesian Rupiah (IDR)'), ('TWD', 'New Taiwan Dollar (TWD)'), ('SGD', 'Singapore Dollar (SGD)'), ('USD', 'US Dollar (USD)')], default='IDR', editable=False, max_length=3, null=True)),
                ('revenue_PO', djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default_currency='IDR', max_digits=15, null=True, validators=[djmoney.models.validators.MinMoneyValidator(0)])),
                ('nomor_PO', models.IntegerField(blank=True, null=True)),
                ('tanggal_PO', models.DateField(blank=True, null=True)),
                ('tanggal_process', models.DateField(blank=True, null=True)),
                ('tanggal_input_accurate', models.DateField(blank=True, null=True)),
                ('tanggal_pengiriman_barang', models.DateField(blank=True, null=True)),
                ('tanggal_pengiriman_invoice', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('order', 'Order Created'), ('pending', 'Pending'), ('process', 'Process'), ('accurate', 'Accurate'), ('pengiriman', 'Pengiriman Barang'), ('invoice', 'Pengiriman Invoice'), ('complete', 'Completed')], max_length=30)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.customer')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page1.items')),
            ],
            options={
                'verbose_name': 'Work Order',
                'verbose_name_plural': 'Work Orders',
            },
        ),
    ]
