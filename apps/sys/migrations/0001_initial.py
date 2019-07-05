# Generated by Django 2.0 on 2019-07-03 07:41

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import utils.storage


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('del_flag', models.BooleanField(default=False, help_text='已删除', verbose_name='已删除')),
                ('remark', models.CharField(blank=True, help_text='备注', max_length=150, null=True, verbose_name='备注')),
                ('age', models.IntegerField(default='1', verbose_name='年龄')),
                ('head_pic', models.ImageField(blank=True, null=True, storage=utils.storage.ImageStorage(), upload_to='img', verbose_name='图片url')),
                ('nickname', models.CharField(help_text='用户昵称', max_length=15, verbose_name='用户昵称')),
            ],
            options={
                'verbose_name': '员工',
                'verbose_name_plural': '员工管理',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('del_flag', models.BooleanField(default=False, help_text='已删除', verbose_name='已删除')),
                ('remark', models.CharField(blank=True, help_text='备注', max_length=150, null=True, verbose_name='备注')),
                ('dep_id', models.AutoField(help_text='部门id', primary_key=True, serialize=False, verbose_name='部门编号')),
                ('dep_type', models.IntegerField(choices=[(0, '分公司'), (1, '校区'), (2, '部门')], null=True, verbose_name='类型')),
                ('dep_name', models.CharField(help_text='部门名称', max_length=10, verbose_name='部门名称')),
                ('dep_tel', models.CharField(help_text='电话', max_length=15, null=True, verbose_name='电话')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='department_creator', to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
                ('operator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='department_operator', to=settings.AUTH_USER_MODEL, verbose_name='更新人')),
            ],
            options={
                'verbose_name': '部门',
                'verbose_name_plural': '部门管理',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('del_flag', models.BooleanField(default=False, help_text='已删除', verbose_name='已删除')),
                ('remark', models.CharField(blank=True, help_text='备注', max_length=150, null=True, verbose_name='备注')),
                ('org_id', models.AutoField(help_text='组织id', primary_key=True, serialize=False, verbose_name='组织编号')),
                ('org_name', models.CharField(help_text='公司名称', max_length=20, verbose_name='公司名称')),
                ('org_add', models.CharField(blank=True, help_text='公司地址', max_length=50, null=True, verbose_name='公司地址')),
                ('contacts_man', models.CharField(help_text='公司联系人', max_length=6, verbose_name='公司联系人')),
                ('contacts_tel', models.CharField(help_text='联系人电话', max_length=30, verbose_name='联系人电话')),
                ('legal_person', models.CharField(blank=True, help_text='公司法人', max_length=6, null=True, verbose_name='公司法人')),
            ],
            options={
                'verbose_name': '公司',
                'verbose_name_plural': '公司管理',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('role_id', models.AutoField(help_text='角色id', primary_key=True, serialize=False, verbose_name='角色编号')),
                ('role_name', models.CharField(help_text='角色名称', max_length=10, verbose_name='角色名称')),
            ],
            options={
                'verbose_name': '角色',
                'verbose_name_plural': '角色管理',
            },
        ),
        migrations.AddField(
            model_name='department',
            name='org',
            field=models.ForeignKey(help_text='公司id', on_delete=django.db.models.deletion.DO_NOTHING, to='sys.Organization', verbose_name='公司名称'),
        ),
        migrations.AddField(
            model_name='department',
            name='superior',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='sys.Department', verbose_name='上级部门'),
        ),
        migrations.AddField(
            model_name='user',
            name='dep',
            field=models.ForeignKey(help_text='部门id', on_delete=django.db.models.deletion.DO_NOTHING, to='sys.Department', verbose_name='所属部门'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='role_id',
            field=models.ManyToManyField(to='sys.Role', verbose_name='角色'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]