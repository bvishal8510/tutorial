from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)
    # print('77777777777777777777777')
    class Meta:
        model = User
        # print('66666666666666666666666')
        fields = ('url','id', 'username', 'snippets')

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.CharField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')
    # print('7888888888888888888888888')
    class Meta:
        model = Snippet
        # print("44444444444444444444444444444444")
        # fields = ('id','owner', 'title', 'code', 'linenos', 'language', 'style',)
        fields = ('url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style')


    def create(self, validated_data):

        # print("1111111111111111111111111111111111111111111111111111111111111111111111111111")
        print(validated_data)
        # print("1111111111111111111111111111111111111111111111111111111111111111111111111111")
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance