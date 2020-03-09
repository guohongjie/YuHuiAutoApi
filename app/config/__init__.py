#-*-coding:utf-8 -*-
from config import TestingConfig
from app.config.getDataFromXml import get_from_xml
host = get_from_xml(gen="service")["host"]
port = get_from_xml(gen="service")["port"]
user = get_from_xml(gen="service")["user"]
pwd = get_from_xml(gen="service")["pwd"]
database = get_from_xml(gen="service")["database"]
database2 = get_from_xml(gen="service")["database2"]
charset = get_from_xml(gen="service")["charset"]
redis_hosts = get_from_xml(gen="redis")["host"]
redis_port = get_from_xml(gen="redis")["port"]
redis_db = get_from_xml(gen="redis")["db"]
__all__ = ['TestingConfig']
