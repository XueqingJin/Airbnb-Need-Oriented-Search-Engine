# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 14:56:05 2019

@author: Yifan Ren
"""
import os
from web_interaction import main

if __name__=="__main__":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./APIK/My First Project-de96be40a9c0.json"
    main()