from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from words.models import Folder, Word
from words.serializers import FolderSerializer, WordSerializer, WordGroupingSerializer
from words.utils.word_grouping import group_words_by_prefix


class FolderViewSet(viewsets.ModelViewSet):
    queryset = Folder.objects.all().order_by("-name")
    serializer_class = FolderSerializer

    @action(detail=False, methods=('post',), serializer_class=WordGroupingSerializer)
    def group_words(self, request, *args, **kwargs):
        serializer = WordGroupingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = group_words_by_prefix(serializer.validated_data['words'])

        folder_names = result.keys()

        Folder.objects.bulk_create([Folder(name=name) for name in folder_names], ignore_conflicts=True)

        # We need explicitly fetch for folder names as not every db will return auto ID when ignore_conflicts=True
        folder_map = dict(Folder.objects.filter(name__in=folder_names).values_list('name', 'id'))

        Word.objects.bulk_create(self._iter_flat_word_models(folder_map, result), ignore_conflicts=True)

        return Response(result)

    def _iter_flat_word_models(self, folder_map, grouped_words):
        for folder_name, words in grouped_words.items():
            for word in words:
                yield Word(folder_id=folder_map[folder_name], content=word)

class WordViewSet(viewsets.ModelViewSet):
    queryset = Word.objects.all().order_by("-content")
    serializer_class = WordSerializer
