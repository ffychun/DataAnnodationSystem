from django.db import models

class Admin(models.Model):
    userID = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=100)

class User(models.Model):
    PERMISSION_CHOICES = (
        (0, '发布者'),
        (1, '标注者'),
    )
    LEVEL_CHOICES = (
        (1, '等级1'),
        (2, '等级2'),
        (3, '等级3'),
        (4, '等级4'),
        (5, '等级5')
    )
    GENDER_CHOICES = (
        (1, '男'),
        (2, '女')
    )
    userID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    permission = models.PositiveSmallIntegerField(choices=PERMISSION_CHOICES)
    level = models.IntegerField(choices=LEVEL_CHOICES, default=1)
    status = models.CharField(max_length=50, blank=True)
    gender = models.IntegerField(blank=True, null= True,choices=GENDER_CHOICES)
    email = models.EmailField()
    phone = models.CharField(max_length=11, blank=True)
    password = models.CharField(max_length=512)
    resumePath = models.TextField(blank=True)
    approvalResult = models.CharField(max_length=20, blank=True)
    headSculpturePath = models.CharField(max_length=200, default="static/images/ico_uer.gif")

class Task(models.Model):
    taskId = models.AutoField(primary_key=True) #任务id
    taskTitle = models.CharField(max_length=200, default=None) #任务名称
    taskDescription = models.TextField() #任务描述
    taskNumber = models.IntegerField(default=1) #任务数量
    taskRemainingNumber = models.IntegerField(default=None) #剩余任务数量
    taskRank = models.IntegerField() #需要匹配的标注者最低等级
    taskTypesChoices = (
        (0, '文本'),
        (1, '图像'),
        (2, '音频'),
    )
    taskType = models.PositiveSmallIntegerField(choices=taskTypesChoices, default=0) #任务类型
    perTaskPaid = models.DecimalField(max_digits=10, decimal_places=2) #一单位任务报酬
    createTime = models.DateTimeField(blank=True) #任务创建时间
    userID = models.ForeignKey(User, to_field='userID', on_delete=models.CASCADE) #发布任务的用户id
    task_status = models.CharField(max_length=50, default="已发布", null=False)
    modifyTime = models.DateTimeField(blank=True, null=True) #任务修改时间

class Order(models.Model):
    ORDER_STATES = (
        (0, '进行中'),
        (1, '已完成'),
        (2, '已取消'),
        (3, '申诉中'),
    )

    PAY_METHODS = (
        (0, '未支付'),
        (1, '支付宝'),
        (2, '微信'),
    )

    order_id = models.CharField(max_length=20, unique=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='published_orders')
    labeler = models.ForeignKey(User, on_delete=models.CASCADE, related_name='labeled_orders')
    order_state = models.IntegerField(choices=ORDER_STATES)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    create_time = models.DateTimeField(auto_now_add=True)
    submit_time = models.DateTimeField(null=True, blank=True)
    pay_method = models.IntegerField(choices=PAY_METHODS)
    result_path = models.CharField(max_length=1024)
    dataset_path = models.CharField(max_length=1024)