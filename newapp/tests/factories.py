"""factory boy provide a way to automatically populates test db with data.
for more research go through the factory boy documentation."""
import factory

from newapp.models import (
    Attribute,
    AttributeValue,
    Category,
    Product,
    ProductImage,
    ProductLine,
    ProductLineAttributeValue,
    ProductType,
)


class CategoryFactory(factory.django.DjangoModelFactory):
    """Factory boy for category model"""

    class Meta:
        model = Category

    # this is used to create unique category name and slug
    name = factory.Sequence(lambda n: "test_category_%d" % n)
    slug = factory.Sequence(lambda n: "test_slug_%d" % n)
    is_active = True


class ProductTypeFactory(factory.django.DjangoModelFactory):
    """Factory boy for ProductType model"""

    class Meta:
        model = ProductType
        skip_postgeneration_save = True

    name = factory.Sequence(lambda n: "test_type_name_%d" % n)

    @factory.post_generation
    def attribute(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.attribute.add(*extracted)
        self.save()


class ProductFactory(factory.django.DjangoModelFactory):
    """Factory boy for Product model"""

    class Meta:
        model = Product
        skip_postgeneration_save = True

    name = factory.Sequence(lambda n: "test_product_name_%d" % n)
    pid = factory.Sequence(lambda n: "0000_%d" % n)
    slug = "test-slug"
    description = "test_description"
    category = factory.SubFactory(CategoryFactory)
    is_active = True
    is_digital = False
    product_type = factory.SubFactory(ProductTypeFactory)

    @factory.post_generation
    def attribute_value(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.attribute_value.add(*extracted)
        self.save()


class ProductLineFactory(factory.django.DjangoModelFactory):
    """Factory boy for ProductLine model"""

    class Meta:
        model = ProductLine
        skip_postgeneration_save = True

    price = 10.00
    sku = "12345"
    stock_qty = 1
    product = factory.SubFactory(ProductFactory)
    is_active = True
    weight = 100
    product_type = factory.SubFactory(ProductTypeFactory)

    @factory.post_generation
    def attribute_value(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.attribute_value.add(*extracted)
        self.save()


class ProductImageFactory(factory.django.DjangoModelFactory):
    """Factory boy for ProductImage model"""

    class Meta:
        model = ProductImage

    alternative_text = "test alternative text"
    url = "test.jpg"
    product_line = factory.SubFactory(ProductLineFactory)


class AttributeFactory(factory.django.DjangoModelFactory):
    """Factory boy for Attribute model"""

    class Meta:
        model = Attribute

    name = "attribute_name_test"
    description = "attr_description_test"


class AttributeValueFactory(factory.django.DjangoModelFactory):
    """Factory boy for AttributeValue model"""

    class Meta:
        model = AttributeValue

    attribute_value = "attr_test"
    attribute = factory.SubFactory(AttributeFactory)


class ProductLineAttributeValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLineAttributeValue

    attribute_value = factory.SubFactory(AttributeValueFactory)
    product_line = factory.SubFactory(ProductLineFactory)
