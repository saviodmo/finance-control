from django.template.defaultfilters import slugify


def slug_pre_save(signal, instance, sender, **kwargs):
    try:
        campo = instance.person
    except:
        campo = instance.titulo

    if not instance.slug:
        slug = slugify(campo)
        new_slug = slug
        counter = 0

        while sender.objects.filter(slug=new_slug).exclude(id=instance.id).count() > 0:
            counter += 1
            new_slug = '%s-%d' % (slug, counter)
        instance.slug = new_slug
