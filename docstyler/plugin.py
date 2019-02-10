# coding: utf-8

"""
Copyright (c) 2019 Heini Fagerlund
BSD-3 License
(https://github.com/hfagerlund/mkdocs-docstyler-plugin/blob/master/LICENSE)
"""

import os
import re
import sys

from mkdocs import utils
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options

import jinja2
from jinja2 import Environment, FileSystemLoader


class docStyler(BasePlugin):
    """
    Adds persistent, preferred and/or alternate external 
    stylesheet links to custom themes for MkDocs.
    """
    config_scheme = (
        ('site_url', config_options.Type(utils.string_types, default='')),
        ('alternate_styles', config_options.Type((list), default=None)),
        ('persistent_styles', config_options.Type(list)),
        ('preferred_styles', config_options.Type(list)),
        )
    
    def on_config(self, config, **kwargs):
        self.check_theme_compatibility(config)
        self.check_config_titles(config)
        self.check_config_paths(config)
        return config
     
    def check_theme_compatibility(self, config):
        """Checks whether theme dir is writable."""
        theme_dir = config['theme'].dirs[0]

        if not os.access(theme_dir, os.W_OK):
            sys.exit("Error: docstyler plugin cannot write to theme \
                      directory... Perhaps you are using a built-in \
                      theme: 'mkdocs' or 'readthedocs'? \
                      Please try using a third-party/custom theme instead.")
            
    def check_config_titles(self, config):
        """
        Enforces non-null title attribute values
        for alternate and preferred stylesheets.
        """
        for style in self.config['alternate_styles'] or \
                self.config['preferred_styles']:
            if 'title_attr' not in style or not style['title_attr'] \
                    or style['title_attr'] is None:
                raise ValueError('Alternate and preferred stylesheets must \
                        have a \'title\' attribute value.')
        
    def check_config_paths(self, config):
        """Enforces non-null path attribute values."""
        for style in self.config['alternate_styles'] or \
                self.config['persistent_styles'] or \
                self.config['preferred_styles']:
            if 'path' not in style or not style['path'] or \
                    style['path'] is None:
                raise ValueError('All stylesheets must have \
                        a \'path\' attribute value.')
            
    def add_styles(self, config, stylesheet_type, base_url):
        """
        Creates array of config option values to pass to plugin template.
        """
        styles_array = []
        for stylesheet in self.config[stylesheet_type]:
            stylesheet_path = stylesheet['path']
            stylesheet_url = base_url + stylesheet_path
            #Check for (optional) media types.
            if 'media_attr' not in stylesheet or \
                    not stylesheet['media_attr'] or \
                    stylesheet['media_attr'] is None:
                stylesheet_media = None
            else:
                stylesheet_media = stylesheet['media_attr']
            
            if stylesheet_type == "persistent_styles":
                styles_array.append([stylesheet_url, stylesheet_media])
            else:
                stylesheet_title = stylesheet['title_attr']
                styles_array.append([stylesheet_url, 
                                     stylesheet_title, 
                                     stylesheet_media])
        return styles_array

    def on_pre_template(self, template, template_name, config):
        #Build URLs to stylesheets.
        if self.config['site_url'] is not None:
            base_url = self.config['site_url']
        else:
            base_url = "/"
            
        #Build array of config option values for each stylesheet type.
        persistent_styles_array = []
        preferred_styles_array = []
        alternative_styles_array = []
        if self.config['persistent_styles'] is not None:
            persistent_styles_array = self.add_styles(config, \
                                                      'persistent_styles', \
                                                      base_url)
        if self.config['preferred_styles'] is not None:
            preferred_styles_array = self.add_styles(config, \
                                                     'preferred_styles', \
                                                     base_url)
        if self.config['alternate_styles'] is not None:
            alternative_styles_array = self.add_styles(config, \
                                                       'alternate_styles', \
                                                       base_url)
        
        output_text = ""
        #Load plugin templates.
        environment = jinja2.Environment(loader=jinja2.FileSystemLoader(
                                         os.path.join(
                                                 os.path.dirname(__file__), 
                                                 "templates")))
        #Render config values in plugin template.
        output_text = environment.get_template("styles.html").render(
                persistent_styles=persistent_styles_array, 
                preferred_styles=preferred_styles_array, 
                alternative_styles=alternative_styles_array)

        theme_dir = config['theme'].dirs[0]
        with open(theme_dir + '/custom_styles.html', "w") as writable_file:
            print(output_text, file=writable_file)
        
        #Include plugin template.
        include_text = """{% extends "base.html" %}
{% block styles %}
    {{ super() }}
        {%- if 'docstyler' in config['plugins'] %}
            {% include "custom_styles.html" %}
        {%- endif %}
{% endblock styles %}"""
        
        with open(theme_dir + '/main.html', "w") as modifiable_file:
            print(include_text, file=modifiable_file)
            
        return template
 