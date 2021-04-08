import os

from django.conf import settings
from django.template import Origin, TemplateDoesNotExist
from django.template.loaders.filesystem import Loader as BaseLoader


class Loader(BaseLoader):

    def get_dirs(self):
        return [settings.TEMPLATES_DIR, ]

    def get_template_sources(self, template_name):
        """
        Return an Origin object pointing to an absolute path in each directory
        in template_dirs. For security reasons, if a path doesn't lie inside
        one of the template_dirs it is excluded from the result set.
        """
        for template_dir in self.get_dirs():
            name = os.path.join(template_dir, template_name)

            yield Origin(
                name=name,
                template_name=template_name,
                loader=self,
            )

    def get_contents(self, origin):
        try:
            with open(origin.name, encoding=self.engine.file_charset) as fp:
                template_content = fp.read()
                template_content = template_content.replace("</head>",
                                         "<!--Hello You--></head>")
                print(template_content)
                return template_content
        except FileNotFoundError:
            raise TemplateDoesNotExist(origin)
