# -*- coding: utf-8 -*-  
import os, sys, time
from jinja2 import Template
import file_helper

def gen_config(template_path, data_path, config_path):
    template_config = file_helper.read_file_all(template_path)
    data_json = file_helper.read_file_json(data_path)
    print(data_json)

    template = Template(template_config)
    config = template.render(data = data_json)
    print(config)

    file_helper.save_file(config_path, config)

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("not args")
    
    t = time.time()

    baseDir = sys.path[0] + '/../'
    gen_config(baseDir + "config.py.template", baseDir + "config.py.data", baseDir + "config.py")

    print("total run time:")
    e = time.time()
    print(e-t)
