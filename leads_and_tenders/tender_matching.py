from leads_and_tenders.models import Tender, SP_Tender
from service_provider.models import ServiceProvider, PlanSubscription
from django.utils import timezone
from django.db import transaction


class MatchingTool:
    # This function searches the keywords table in the db if
    # they match the assigned keywordTags to the tenders.
    def matchTendersToSP(self):
        # section below pulls all assigned keywords to the tenders as per the
        # keywordTags field in the tenders db table.
        unmatched_tenders = Tender.objects.filter(closingDate__gt=timezone.now())
        subscriptions = PlanSubscription.objects.filter(status=1).distinct()

        for tender in unmatched_tenders:
            tender_provinces = tender.tenderProvince.all()
            tender_keywords = tender.assigned_keywords.all()

            for subscription in subscriptions:
                sp = subscription.sp
                sp_provinces = sp.provinces.all()
                sp_keywords = sp.business_keywords.all()

                matched_provinces = tender_provinces.intersection(sp_provinces)
                matched_keywords = tender_keywords.intersection(sp_keywords)

                if len(matched_provinces) > 0:
                    if len(matched_keywords) > 0:
                        with transaction.atomic():
                            if SP_Tender.objects.filter(service_provider=sp, tender=tender).exists() == False:
                                SP_Tender.objects.create(service_provider=sp, tender=tender)
                                













