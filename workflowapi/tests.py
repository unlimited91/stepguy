from django.test import TestCase

# Create your tests here.
from django.test import TestCase

from django.contrib.auth.models import User
from django.urls import reverse

from userman.models import ApiKey
from workflowops.models import Workflow, WorkflowDSL


def create_active_user():
    user = User.objects.create(
        username='admin',
        password='admin',
        email='i@sayan.com',
    )
    return user


class WorkflowApiTests(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            username='admin',
            password='admin',
            email='i@sayan.com',
        )
        self.apikey = ApiKey.objects.create(
            api_key='random',
            user=self.user,
        )
        self.workflow_dsl = WorkflowDSL.objects.create(
            file_type=WorkflowDSL.FileTypeChoices.yaml,
            file='/tmp/Lee',
            user=self.user
        )
        self.workflow = Workflow.objects.create(
            workflow_namespace='scale_compute',
            user=self.user,
            version=Workflow.VersionChoices.v1,
            workflow_dsl=self.workflow_dsl,
            inputs='compute_id:compute_storage'
        )

    def test_api_key_save(self):
        self.assertEquals(self.apikey.api_key, 'random')

    def test_initiate_workflow(self):
        post_data = {
            "workflow_namespace": "scale_compute",
            "inputs": {
                "compute_id": "az-123456",
                "compute_storage": "100g"
            }
        }
        response = self.client.post(
            reverse('workflowapi:initiate-workflow'),
            data=post_data,
            content_type='application/json',
            HTTP_X_APIKEY='random'
        )
        self.assertEqual(response.status_code, 200)


