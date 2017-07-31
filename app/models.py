from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class Source(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)
    qq = models.CharField(max_length=64, blank=True, null=True, unique=True)
    weixin = models.CharField(max_length=64, blank=True, null=True, unique=True)
    phone = models.BigIntegerField(blank=True, null=True, unique=True)
    email = models.EmailField(blank=True, null=True)
    source = models.ForeignKey('Source')
    referal_from = models.ForeignKey('Account', blank=True, null=True, related_name='my_referal')
    consult_courses = models.ManyToManyField("Course")
    content = models.TextField(u'首次咨询内容/客户详情')
    status_choices = (
        (0, '已报名'),
        (1, '已退费'),
        (2, '未报名')
    )
    status = models.SmallIntegerField(u'来源',choices=status_choices, default=2)
    tags = models.ManyToManyField('Tag', blank=True)
    consultant = models.ForeignKey('Account', related_name='my_consultant')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "客户信息表"
        verbose_name_plural = "客户信息表"


class PaymentRecord(models.Model):
    customer = models.ForeignKey('Customer')
    class_list = models.ForeignKey('ClassList')
    payment_method_choices = (
        (0, '现金'),
        (1, '微信'),
        (2, '支付宝'),
        (3, '刷卡'),
        (4, '学生贷款'),
    )
    payment_method = models.SmallIntegerField(choices=payment_method_choices)
    payment_type_choices = (
        (0, '报名费'),
        (1, '学费'),
        (2, '退费'),
    )
    payment_type = models.SmallIntegerField(choices=payment_type_choices)
    amount = models.FloatField()


class CustomerFollowUp(models.Model):
    """跟踪记录"""
    customer = models.ForeignKey('Customer')
    content = models.TextField()
    consultant = models.ForeignKey('Account')
    date = models.DateTimeField(auto_now_add=True)
    status_choices = (
        (0, '绝不考虑'),
        (1, '短期内不考虑'),
        (2, '已在其他机构报名'),
        (3, '2周内报名'),
        (4, '已报名'),
        (5, '已试听'),
    )
    status = models.IntegerField(choices=status_choices)


class Course(models.Model):
    name = models.CharField(max_length=128, unique=True)
    period = models.IntegerField(u'周期(月)')
    price = models.FloatField()
    outline = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "课程信息表"
        verbose_name_plural = "课程信息表"


class Branch(models.Model):
    """校区"""
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class ClassList(models.Model):
    course = models.ForeignKey('Course')
    branch = models.ForeignKey('Branch')
    semester = models.IntegerField(u'学期')
    contract = models.ForeignKey('Contract')
    class_type_choices = (
        (0, '周末'),
        (1, '脱产'),
        (2, '网络'),
    )
    class_type = models.IntegerField(choices=class_type_choices)
    max_student_num = models.IntegerField(default=80)
    teachers = models.ManyToManyField('Account')
    start_date = models.DateField(u'开班日期')
    end_date = models.DateField(u'结业日期', blank=True, null=True)

    def __str__(self):
        return "%s(%s)" % (self.course, self.semester)

    class Meta:
        unique_together = ('course', 'branch', 'semester', 'class_type')
        verbose_name = "班级信息表"
        verbose_name_plural = "班级信息表"


class CourseRecord(models.Model):
    """上课记录"""
    class_list = models.ForeignKey('ClassList')
    day_num = models.IntegerField(u'节次')
    name = models.CharField(max_length=128)
    teacher = models.ForeignKey('Account')
    has_homework = models.BooleanField(default=True)
    homework_requirement= models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s(%s)-%s" % (self.class_list, self.day_num, self.name)

    class Meta:
        unique_together = ('class_list', 'day_num')


class Enrollment(models.Model):
    """已报名班级"""
    account = models.ForeignKey('Account')
    class_list = models.ForeignKey('ClassList')
    date = models.DateTimeField(auto_now_add=True)


class StudyRecord(models.Model):
    """学习记录"""
    student = models.ForeignKey('Account')
    course_record = models.ForeignKey('CourseRecord')
    score_choices = (
        (100, 'A+'),
        (90, 'A'),
        (85, 'B+'),
        (70, 'B'),
        (65, 'C+'),
        (60, 'C'),
        (40, 'C-'),
        (-50, 'D'),
        (0, 'N/A'),
        (-100, 'COPY')
    )
    score = models.IntegerField(choices=score_choices)
    show_status_choices = (
        (0, '正常签到'),
        (1, '迟到'),
        (2, '缺勤'),
        (3, 'N/A')
    )
    show_status = models.IntegerField(choices=show_status_choices)
    comment = models.TextField(u'批注', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course_record')


class Contract(models.Model):
    name = models.CharField(max_length=128, unique=True)
    content= models.TextField(u'合同内容')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    """角色：更关注获取menu列表"""
    name = models.CharField(max_length=64, unique=True)
    menus = models.ManyToManyField('Menu', blank=True, null=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    """一级菜单"""
    name = models.CharField(max_length=64)
    url_type_choices = (
        (0, 'absolute'),
        (1, 'relative'),
    )
    url_type = models.IntegerField(choices=url_type_choices,default=1)
    url = models.CharField(max_length=128)
    order = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('url', 'url_type')


class SubMenu(models.Model):
    """二级菜单"""
    menu = models.ForeignKey('Menu')
    name = models.CharField(max_length=64)
    url_type_choices = (
        (0, 'absolute'),
        (1, 'relative'),
    )
    url_type = models.IntegerField(choices=url_type_choices, default=1)
    url = models.CharField(max_length=128)
    order = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('url', 'url_type')


class Account(models.Model):

    username = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.username


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Account1(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=32)
    role = models.ForeignKey("Role", blank=True, null=True)
    customer = models.OneToOneField("Customer", blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.name

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
