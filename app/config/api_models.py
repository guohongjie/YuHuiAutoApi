#-*-coding:utf-8 -*-
from app import db
class Project(db.Model):
    __tablename__ = "project_api"  # 表名
    id = db.Column(db.Integer,primary_key=True)#序号ID
    project = db.Column(db.String(100), unique=True) # 项目
    project_en = db.Column(db.String(100)) # 项目_英文
    domain = db.Column(db.String(100))
    description = db.Column(db.Text)#项目描述
    use_status = db.Column(db.Integer,default=0)
    test_group = db.Column(db.String(100))
    startDate = db.Column(db.DateTime)  # 起始日期
    endDate = db.Column(db.DateTime)  # 终止日期
    def __init__(self,project,description,domain,project_en,test_group,startDate,endDate,use_status=0):
        self.project = project
        self.description = description
        self.domain = domain
        self.project_en = project_en
        self.use_status = use_status
        self.test_group = test_group
        self.startDate = startDate
        self.endDate = endDate
    def __repr__(self):
        return '<Case %r>'%(self.project)
class runSuiteProject(db.Model):
    
    __tablename__ = "runSuiteProject"  # 表名
    id = db.Column(db.Integer,primary_key=True)#序号ID
    project = db.Column(db.String(100), unique=True) # 项目
    project_en = db.Column(db.String(100), unique=True) # 项目_英文
    domain = db.Column(db.String(100))
    description = db.Column(db.Text)#项目描述
    use_status = db.Column(db.Boolean,default=0)
    def __init__(self,project,description,domain,project_en,use_status=0):
        self.project = project
        self.description = description
        self.domain = domain
        self.project_en = project_en
        self.use_status = use_status
    def __repr__(self):
        return '<Case %r>'%(self.name)
class Run_Suite(db.Model):
    __tablename__ = "RunSuite"
    id = db.Column(db.Integer, primary_key=True)  # 序号ID
    user = db.Column(db.String(100), unique=True) # 所属用户
    test_group = db.Column(db.String(100), unique=True) # 所属组别
    suiteName = db.Column(db.String(200), unique=True) # 流程名称
    suiteDatas = db.Column(db.Text)  #流程数据
    modifyCount = db.Column(db.Integer)  #修改次数
    domain = db.Column(db.String(100))
    statu = db.Column(db.Boolean,default=0)
    description = db.Column(db.Text)    #流程描述
    def __init__(self,user,test_group,suiteName,suiteDatas,modifyCount,domain=None,statu=None,description=None):
        self.user = user
        self.test_group = test_group
        self.suiteName = suiteName
        self.suiteDatas = suiteDatas
        self.modifyCount = modifyCount
        self.domain = domain
        self.statu = statu
        self.description = description
class Case_Http_API(db.Model):
    __tablename__ = "case_http_api" #表名
    id = db.Column(db.Integer,primary_key=True)#序号ID
    project = db.Column(db.String(100),db.ForeignKey('project_api.project'))#项目
    case_api = db.Column(db.String(100))#接口名称
    description = db.Column(db.Text)#用例描述
    case_host = db.Column(db.String(500))#请求链接
    case_url = db.Column(db.String(500))#请求链接
    method = db.Column(db.String(10))#请求方式
    params = db.Column(db.Text)#请求参数KEY
    headers = db.Column(db.Text)#请求参数headers
    cookies = db.Column(db.Text)#请求参数cookies
    response = db.Column(db.Text)#预期结果
    status = db.Column(db.Boolean,default=0)
    isLogin = db.Column(db.Boolean,default=0)
    account_project = db.Column(db.String(100))
    account_username = db.Column(db.String(100))
    account_passwd = db.Column(db.String(100))
    isSchedule = db.Column(db.Boolean,default=0)
    checkAssert = db.Column(db.String(100))
    test_env = db.Column(db.String(100))
    test_group = db.Column(db.String(100))
    tester = db.Column(db.String(100))
    def __init__(self,project,case_api,params,case_host,
                 headers,cookies,description,case_url,
                 method,response,status=0,isLogin=0,
                 account_project=account_project,isSchedule=isSchedule,
                 account_username=account_username,checkAssert=checkAssert,
                 account_passwd=account_passwd,
                 test_env=test_env,test_group=test_group,tester=tester):
        self.project = project
        self.case_api = case_api
        self.description = description
        self.case_url = case_url
        self.method = method
        self.response = response
        self.status = status
        self.params = params
        self.case_host = case_host
        self.headers = headers
        self.cookies = cookies
        self.isLogin = isLogin
        self.test_env = test_env
        self.test_group = test_group
        self.account_project = account_project
        self.account_username = account_username
        self.account_passwd = account_passwd
        self.tester = tester
        self.checkAssert = checkAssert
        self.isSchedule = isSchedule

    def __repr__(self):
        """返回打印数据"""
        return '<Case %r>'%self.project

class SuiteDatas(db.Model):
    __tablename__ = "suiteDatas"  # 表名
    id = db.Column(db.Integer, primary_key=True)  # 序号ID
    api_id = db.Column(db.Integer,db.ForeignKey('case_http_api.id'))
    suiteData = db.Column(db.Text)  #流程数据
    suiteName = db.Column(db.String(100))
    def __init__(self,id,api_id,suiteData,suiteName):
        self.id = id
        self.api_id = api_id
        self.suiteData = suiteData
        self.suiteName = suiteName
class Login_Base_Project(db.Model):
    __tablename__ = "login_base_project"  # 表名
    id = db.Column(db.Integer,primary_key=True)#序号ID
    project = db.Column(db.String(100))
    status = db.Column(db.Boolean, default=0)
    def __init__(self,project,status):
        self.project = project
        self.status = status
class Web_Model_Set(db.Model):
    
    __tablename__ = "model_set"  # 表明
    id = db.Column(db.Integer, primary_key=True)  # 序号ID
    modelName = db.Column(db.String(100))
    modelLink = db.Column(db.String(500))
    modelStatus = db.Column(db.Boolean, default=0)
    isAdmin = db.Column(db.Boolean, default=0)
    levelName = db.Column(db.String(100))
    def __init__(self,modelName,modelLink,modelStatus,levelName,isAdmin):
        self.modelName = modelName
        self.modelLink = modelLink
        self.modelStatus = modelStatus
        self.levelName = levelName
        self.isAdmin = isAdmin
    def __repr__(self):
        return '<Case %r>'%(self.modelName)
class Test_Env(db.Model):
    
    __tablename__ = "test_env"  # 表名
    id = db.Column(db.Integer,primary_key=True)#序号ID
    env_flag = db.Column(db.String(100)) # 测试环境
    env_num = db.Column(db.String(100))  # 测试环境编号
    def __init__(self,env_flag,env_num):
        self.env_flag = env_flag
        self.env_num = env_num
    def __repr__(self):
        return '<Case %r>'%(self.env_flag)
class Test_User_Reg(db.Model):
    
    __tablename__ = "telephone"
    id = db.Column(db.Integer,primary_key=True) #序号ID
    phone = db.Column(db.String(11)) #手机号
    type = db.Column(db.Integer,default=0) #注册类型
    env = db.Column(db.String(10)) #环境
    description = db.Column(db.Text) #备注
    def __init__(self,phone,type=None,env=None,description=None):
        self.phone = phone
        self.type = type
        self.env = env
        self.description = description
class Key_Value(db.Model):
    
    __tablename__ = "key_value"
    id = db.Column(db.Integer,primary_key=True) #序号ID
    user_key = db.Column(db.String(100)) #手机号
    status = db.Column(db.Integer,default=0) #注册类型
    user_value = db.Column(db.String(500)) #环境
    def __init__(self,id,user_key,user_value,status=1):
        self.id = id
        self.user_key = user_key
        self.user_value = user_value
        self.status = status
class is_Make_User(db.Model):
    
    __tablename__ = "isMakeUser"
    id = db.Column(db.Integer, primary_key=True)  # 序号ID
    project_en = db.Column(db.String(100), unique=True) # 项目_英文
    isMake = db.Column(db.Boolean, default=0)
    def __init__(self,id,project_en,isMake=0):
        self.id = id
        self.project_en = project_en
        self.isMake = isMake
class Test_Domain(db.Model):
    __tablename__ = "test_domain"
    id = db.Column(db.Integer, primary_key=True)  # 序号ID
    domain = db.Column(db.String(100), unique=True)  # 项目
    statu = db.Column(db.Boolean, default=0)
    def __init__(self, id, domain, statu=0):
        self.id = id
        self.domain = domain
        self.statu = statu
class Test_Report(db.Model):
    __tablename__ = "test_report"
    id = db.Column(db.Integer, primary_key=True)  # 序号ID
    domain = db.Column(db.String(100))  # 项目
    developer = db.Column(db.String(100))  # 项目
    report_url = db.Column(db.String(100))  # 项目
    success_count = db.Column(db.String(100))  # 项目
    fail_count = db.Column(db.String(100))  # 项目
    mistake_count = db.Column(db.String(100))  # 项目
    cookies = db.Column(db.String(100))  # 项目
    createDate = db.Column(db.DateTime)  # 项目
    type = db.Column(db.String(100))  # 项目
    def __init__(self,domain,developer,report_url,success_count,
                 fail_count,mistake_count,cookies,type):
        self.domain = domain
        self.developer = developer
        self.report_url = report_url
        self.success_count = success_count
        self.fail_count = fail_count
        self.mistake_count = mistake_count
        self.cookies = cookies
        self.type = type