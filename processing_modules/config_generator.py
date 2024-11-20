
from configparser import ConfigParser
from encrypt_decrypt_data import encrypt
#Get the configparser object
config_object = ConfigParser()
from query import ins_cred
#Assume we need 2 sections in the config file, let's call them USERINFO and SERVERCONFIG


password = encrypt("password")
host     = encrypt("localhost")
dbname   = encrypt("postgres")
user     = encrypt("postgres")


config_object["DBCONFIG"] = \
{
    "dbname"  : dbname,
    "user"    : user,
    "password": password,
    "host"    : host,
    "port"    : 5432
}


config_object["STATIC_IMAGE_PATHS"]= \
{
   "homepage_background_image"  :"static/home_background.png",
   "otherpage_background_image" :"static/other_page.jpeg",
   "image_html_placeholder_icon":"static/image_icon.png" 
}




#Write the above sections to config.ini file
with open('config.ini', 'w') as conf:
    config_object.write(conf)