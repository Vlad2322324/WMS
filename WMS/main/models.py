from django.db import models


class SupplierDirectory(models.Model):
    supplier = models.BigIntegerField(primary_key=True)
    name = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = ' Supplier directory'


class Cell(models.Model):
    cell_id = models.BigIntegerField(db_column='cell id', primary_key=True)  # Field renamed to remove unsuitable characters.
    shelf = models.BigIntegerField()
    pallet = models.ForeignKey('Pallet', models.DO_NOTHING, db_column='pallet', blank=True, null=True)
    zone = models.ForeignKey('Zone', models.DO_NOTHING, db_column='zone', blank=True, null=True)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Cell'


class Pallet(models.Model):
    pallet_id = models.BigIntegerField(db_column='pallet id', primary_key=True)  # Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'Pallet'


class ProductDirectory(models.Model):
    product_id = models.BigIntegerField(db_column='product id', primary_key=True)  # Field renamed to remove unsuitable characters.
    barcod = models.BigIntegerField()
    expiration_date = models.BigIntegerField(db_column='expiration date')  # Field renamed to remove unsuitable characters.
    weight = models.BigIntegerField()
    name = models.TextField(db_column='Name')  # Field name made lowercase. This field type is a guess.
    storage_type = models.TextField(db_column='storage type')  # Field renamed to remove unsuitable characters. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Product_directory'


class ProductOnPallet(models.Model):
    pallet_id = models.OneToOneField(Pallet, models.DO_NOTHING, db_column='pallet id', primary_key=True)  # Field renamed to remove unsuitable characters. The composite primary key (pallet id, product id) found, that is not supported. The first column is selected.
    product_id = models.ForeignKey(ProductDirectory, models.DO_NOTHING, db_column='product id')  # Field renamed to remove unsuitable characters.
    quantity = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'Product_on_pallet'
        unique_together = (('pallet_id', 'product_id'),)


class PurchaseOrder(models.Model):
    product_id = models.OneToOneField(ProductDirectory, models.DO_NOTHING, db_column='product id', primary_key=True)  # Field renamed to remove unsuitable characters. The composite primary key (product id, delivery id) found, that is not supported. The first column is selected.
    delivery_id = models.BigIntegerField(db_column='delivery id')  # Field renamed to remove unsuitable characters.
    quantity = models.BigIntegerField()
    amount = models.BigIntegerField()
    supplier = models.ForeignKey(SupplierDirectory, models.DO_NOTHING, db_column='supplier')

    class Meta:
        managed = False
        db_table = 'Purchase_order'
        unique_together = (('product_id', 'delivery_id'),)


class Zone(models.Model):
    zone_id = models.BigIntegerField(db_column='zone id', primary_key=True)  # Field renamed to remove unsuitable characters.

    type = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Zone'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
