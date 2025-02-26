"""flow views tests"""
from django.test import TestCase
from django.urls import reverse

from authentik.core.tests.utils import create_test_flow
from authentik.flows.models import Flow, FlowDesignation
from authentik.flows.planner import FlowPlan
from authentik.flows.views.executor import SESSION_KEY_PLAN


class TestHelperView(TestCase):
    """Test helper views logic"""

    def test_default_view(self):
        """Test that ToDefaultFlow returns the expected URL"""
        Flow.objects.filter(designation=FlowDesignation.INVALIDATION).delete()
        flow = create_test_flow(FlowDesignation.INVALIDATION)
        response = self.client.get(
            reverse("authentik_flows:default-invalidation"),
        )
        expected_url = reverse("authentik_core:if-flow", kwargs={"flow_slug": flow.slug})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_url)

    def test_default_view_invalid_plan(self):
        """Test that ToDefaultFlow returns the expected URL (with an invalid plan)"""
        Flow.objects.filter(designation=FlowDesignation.INVALIDATION).delete()
        flow = create_test_flow(FlowDesignation.INVALIDATION)
        plan = FlowPlan(flow_pk=flow.pk.hex + "aa")
        session = self.client.session
        session[SESSION_KEY_PLAN] = plan
        session.save()

        response = self.client.get(
            reverse("authentik_flows:default-invalidation"),
        )
        expected_url = reverse("authentik_core:if-flow", kwargs={"flow_slug": flow.slug})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_url)
