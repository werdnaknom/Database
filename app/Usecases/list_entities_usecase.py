from app.Responses.responses import ResponseSuccess
from app.UseCases.usecase import UseCase


class ListUseCase(UseCase):

    def __init__(self, repo):
        self.repo = repo

    def process_request(self, request_object):
        entity_products = self.repo.list(filters=request_object.filters)
        return ResponseSuccess(entity_products)


