from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import HuntLog, WantedCriminal
from .serializers import HuntLogSerializer, WantedCriminalSerializer

BOOL_VALUES = {'true': True, '1': True, 'false': False, '0': False}
SORT_VALUES = {'reward', '-reward'}


def parse_int(params, key):
    value = params.get(key)
    if value is None or value == '':
        return None
    try:
        number = int(value)
    except ValueError:
        raise ValidationError({key: 'Must be an integer.'})
    if number < 0:
        raise ValidationError({key: 'Must not be negative.'})
    return number


def parse_bool(params, key):
    value = params.get(key)
    if value is None or value == '':
        return None
    if value.lower() not in BOOL_VALUES:
        raise ValidationError({key: 'Must be true or false.'})
    return BOOL_VALUES[value.lower()]


class CriminalListView(APIView):
    serializer_class = WantedCriminalSerializer

    # GET /api/criminals/?min_reward=&max_reward=&armed=&has_crew=&escape_master=&sort=
    @extend_schema(responses=WantedCriminalSerializer(many=True), parameters=[
        OpenApiParameter('min_reward', int),
        OpenApiParameter('max_reward', int),
        OpenApiParameter('armed', bool),
        OpenApiParameter('has_crew', bool),
        OpenApiParameter('escape_master', bool),
        OpenApiParameter('sort', str, enum=sorted(SORT_VALUES)),
    ])
    def get(self, request):
        params = request.query_params
        criminals = WantedCriminal.objects.all()

        min_reward = parse_int(params, 'min_reward')
        if min_reward is not None:
            criminals = criminals.filter(reward__gte=min_reward)
        max_reward = parse_int(params, 'max_reward')
        if max_reward is not None:
            criminals = criminals.filter(reward__lte=max_reward)

        for field in ('armed', 'has_crew', 'escape_master'):
            value = parse_bool(params, field)
            if value is not None:
                criminals = criminals.filter(**{field: value})

        sort = params.get('sort')
        if sort:
            if sort not in SORT_VALUES:
                raise ValidationError({'sort': 'Must be reward or -reward.'})
            criminals = criminals.order_by(sort, 'id')
        else:
            criminals = criminals.order_by('id')

        return Response(WantedCriminalSerializer(criminals, many=True).data)


class CriminalDetailView(APIView):
    serializer_class = WantedCriminalSerializer

    # GET /api/criminals/<id>/
    def get(self, request, pk):
        criminal = get_object_or_404(WantedCriminal, pk=pk)
        return Response(WantedCriminalSerializer(criminal).data)


class HuntListView(APIView):
    serializer_class = HuntLogSerializer

    # GET /api/hunts/?criminal_id=
    @extend_schema(responses=HuntLogSerializer(many=True),
                   parameters=[OpenApiParameter('criminal_id', int)])
    def get(self, request):
        hunts = HuntLog.objects.order_by('id')
        criminal_id = parse_int(request.query_params, 'criminal_id')
        if criminal_id is not None:
            if not WantedCriminal.objects.filter(pk=criminal_id).exists():
                raise NotFound(f'Criminal {criminal_id} not found.')
            hunts = hunts.filter(criminal_id=criminal_id)
        return Response(HuntLogSerializer(hunts, many=True).data)

    # POST /api/hunts/
    def post(self, request):
        serializer = HuntLogSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class HuntDetailView(APIView):
    serializer_class = HuntLogSerializer

    # GET /api/hunts/<id>/
    def get(self, request, pk):
        hunt = get_object_or_404(HuntLog, pk=pk)
        return Response(HuntLogSerializer(hunt).data)

    # PATCH /api/hunts/<id>/
    def patch(self, request, pk):
        hunt = get_object_or_404(HuntLog, pk=pk)
        serializer = HuntLogSerializer(hunt, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # DELETE /api/hunts/<id>/
    def delete(self, request, pk):
        hunt = get_object_or_404(HuntLog, pk=pk)
        hunt.delete()
        return Response(status=204)
