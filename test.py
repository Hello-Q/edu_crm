class TestSchema(AutoSchema):
    def get_link(self, path, method, base_url):
        link = super(TestSchema, self).get_link(path, method, base_url)
        get_fields = [
            coreapi.Field('q', location='query', schema=coreschema.String(description=u'filter xxxx')),
        ]
        translation_fields = [
            coreapi.Field('name', location='form', required=True,
                          schema=coreschema.String(description=u'xxxx name',)),
        ]        if link.url == '/api/v1/xxxxx/' and method.lower() == 'get':
            fields = tuple(get_fields) + link.fields        elif link.url == '/api/v1/xxxxx/{id}/translation/':
            fields = tuple(translation_fields) + link.fields        else:
            fields = link.fields

        link = coreapi.Link(
            url=link.url,
            action=link.action,
            encoding=link.encoding,
            fields=fields,
            description=link.description)
        coreapi.document.Link()
        return link