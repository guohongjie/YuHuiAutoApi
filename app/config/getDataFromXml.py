#!/usr/bin/python
#-*-coding:utf-8 -*-
import xml.etree.ElementTree as ET
import os
def get_data_params(file,gen):
    tree = ET.parse(file)
    root = tree.getroot()
    s = [dict(simgleMobile)
         for simgleMobile in map(lambda x:[(y.tag,y.text) for y in x],
            [datas for datas in root.findall(gen) if datas.attrib["use"]=="true"])][0] \
        if len([datas for datas in root.findall(gen)  if datas.attrib["use"]=="true" ])==1 else 0
    if s:
        return s
    else:
        raise Exception,'Error :   <Datas use="true">存在多个配置,只能存在一个使用配置！'
def get_from_xml(gen):
    p, f = os.path.split(os.path.abspath(__file__))
    xmlFile = p + "/config.xml"
    return get_data_params(xmlFile,gen)

if __name__ == "__main__":
    print get_data_params("config.xml", gen="service")["host"]