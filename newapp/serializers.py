from rest_framework import serializers

from .models import Attribute, AttributeValue, Category, Product, ProductImage, ProductLine


class CategorySerializer(serializers.ModelSerializer):
    """serializes category objects"""

    category_name = serializers.CharField(source="name")

    class Meta:
        model = Category
        fields = ["category_name", "slug"]


class ProductImageSerializer(serializers.ModelSerializer):
    """serializes product images"""

    class Meta:
        model = ProductImage
        exclude = ("id", "product_line")


class AttributeSerializer(serializers.ModelSerializer):
    """Serializes attribute objects"""

    class Meta:
        model = Attribute
        fields = ("name",)


class AttributeValueSerializer(serializers.ModelSerializer):
    """Serializes attributeValue objects"""

    attribute = AttributeSerializer(many=False)

    class Meta:
        model = AttributeValue
        fields = ("attribute", "attribute_value")


class ProductLineSerializer(serializers.ModelSerializer):
    """serializes Product line objects"""

    product_image = ProductImageSerializer(many=True)
    attribute_value = AttributeValueSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = (
            "price",
            "sku",
            "stock_qty",
            "order",
            "product_image",
            "attribute_value",
        )

    # code for customizing the serializer data
    def to_representation(self, instance):
        data = super().to_representation(instance)
        av_data = data.pop("attribute_value")
        attr_values = {}
        for key in av_data:
            attr_values.update({key["attribute"]["id"]: key["attribute_value"]})
        data.update({"specification": attr_values})

        return data


class ProductSerializer(serializers.ModelSerializer):
    """serializes product objects"""

    # name mapping and flattening
    product_line = ProductLineSerializer(many=True)
    attribute = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "name",
            "slug",
            "pid",
            "description",
            "product_line",
            "attribute",
        )

    # custom field with serializermethod field
    def get_attribute(self, obj):
        attribute = Attribute.objects.filter(product_type_attribute__product__id=obj.id)
        return AttributeSerializer(attribute, many=True).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        av_data = data.pop("attribute")
        attr_values = {}
        for key in av_data:
            attr_values.update({key["id"]: key["name"]})
        data.update({"type specification": attr_values})

        return data


class ProductLineCategorySerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = (
            "price",
            "product_image",
        )


class ProductCategorySerializer(serializers.ModelSerializer):
    product_line = ProductLineCategorySerializer(many=True)

    class Meta:
        model = Product
        fields = (
            "name",
            "slug",
            "pid",
            "created_at",
            "product_line",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        x = data.pop("product_line")
        if x:
            price = x[0]["price"]
            image = x[0]["product_image"]
            data.update({"price": price})
            data.update({"image": image})

        return data
