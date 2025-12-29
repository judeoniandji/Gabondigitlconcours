from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Paiement
from django.db.models.query import QuerySet
from .serializers import PaiementSerializer
from .airtel import initiate_airtel_payment

class PaiementViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[Paiement] = Paiement._default_manager.all()
    serializer_class = PaiementSerializer

    @action(detail=False, methods=['post'])
    def airtel(self, request):
        msisdn = request.data.get('msisdn')
        amount = request.data.get('amount')
        reference = request.data.get('reference')
        concours_id = request.data.get('concours_id')
        candidat_id = request.data.get('candidat_id')
        if not all([msisdn, amount, reference, concours_id, candidat_id]):
            return Response({'detail': 'Paramètres requis manquants'}, status=status.HTTP_400_BAD_REQUEST)
        v = str(msisdn).replace(' ', '')
        if v.startswith('+'):
            import re
            if not re.fullmatch(r'\+241\d{8}', v):
                return Response({'detail': 'Numéro Airtel invalide. Format: +241 suivi de 8 chiffres'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            import re
            if not re.fullmatch(r'\d{8}', v):
                return Response({'detail': 'Numéro Airtel invalide. Format: 8 chiffres (ex: 06234567)'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            result = initiate_airtel_payment(msisdn, amount, reference)
            paiement = Paiement._default_manager.create(
                candidat_id=candidat_id,
                concours_id=concours_id,
                montant=amount,
                reference=reference,
                statut='en_attente',
            )
            return Response({'paiement_id': paiement.id, 'airtel': result})
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
